# app.py
import os
import json
import base64
import requests
from datetime import datetime

# Flask 相关导入
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange
from dotenv import load_dotenv

# 阿里 DashScope SDK
from dashscope import Generation

# 本地模块导入
from models import db, User, DietLog
from nutrition.local_nutrition_db import get_nutrition_info
from api.baidu_food_recognition import get_access_token, recognize_ingredient, recognize_dish
# 加载环境变量
load_dotenv()


# 1. 全局配置与初始化


# 百度 API 配置
API_KEY = os.getenv("BAIDU_API_KEY")
SECRET_KEY = os.getenv("BAIDU_SECRET_KEY")

# 文件上传配置
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'gif'}

# Flask App 初始化
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'your-secret-key-here'  # 建议在生产环境中放入 .env

# 数据库配置
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'app.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化扩展
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



# 2. WTForms 表单定义


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    submit = SubmitField('登录')


class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('确认密码', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('注册')


class GoalForm(FlaskForm):
    current_weight = FloatField('当前体重', validators=[
        DataRequired(),
        NumberRange(min=30, max=300, message="体重应在30~300kg之间")
    ])
    target_weight = FloatField('目标体重', validators=[
        DataRequired(),
        NumberRange(min=30, max=300, message="体重应在30~300kg之间")
    ])
    submit = SubmitField('保存目标')



# 3. 工具函数与核心逻辑 (Helpers)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_nutrition_by_ai(food_name):
    """使用阿里 AI 查询食物的每 100g 营养成分"""
    prompt = f"""
    请提供食物“{food_name}”每100克的营养成分数据。
    请严格只返回一个 JSON 格式的对象，不要包含任何多余文字。
    格式要求：{{"calories": 数字, "protein": 数字, "fat": 数字, "carbs": 数字}}
    """
    try:
        response = Generation.call(
            model="qwen-turbo",
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            prompt=prompt
        )
        if response.status_code == 200:
            # 尝试解析 AI 返回的 JSON 字符串
            data = json.loads(response.output.text.strip('`').replace('json', ''))
            return data
    except Exception as e:
        print(f"AI 获取营养成分失败: {e}")
    # 失败则返回默认值
    return {"calories": 0, "protein": 0, "fat": 0, "carbs": 0}


def get_instant_recommendation(user, current_food):
    """
    针对当前识别到的食物提供即时建议
    current_food: 包含 name, calories, protein, fat, carbs 的字典
    """
    prompt = f"""
    作为智能饮食助手，请针对用户刚刚录入的食物给出评价和建议。

    【用户信息】
    - 当前体重：{user.current_weight}kg
    - 目标体重：{user.target_weight}kg

    【当前录入食物】
    - 食物名称：{current_food['name']}
    - 营养成分：热量 {current_food['calories']}kcal, 蛋白质 {current_food['protein']}g, 脂肪 {current_food['fat']}g, 碳水 {current_food['carbs']}g

    【要求】
    1. 基于 TDEE准则 给出“可食用/限量/不推荐”标签（只需在开头给出例如：’TDEE建议：可食用‘）。
    2. 评价该食物是否符合用户的体重目标（例如：减重期是否热量过高？增肌期蛋白质是否足够？）。
    3. 若标签为限量或不推荐，给出平替食物，并说明优点在哪。
    4. 针对用户的增重或减重目标给出今日推荐食谱。
    5. 语气要亲切友好，字数在 100 字左右。
    """
    try:
        response = Generation.call(
            model="qwen-turbo",
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            prompt=prompt
        )
        if response.status_code == 200:
            return response.output.text
        return "识别成功！建议稍后生成。"
    except Exception as e:
        print(f"阿里API调用失败: {e}")
        return "识别成功！由于网络波动，暂时无法生成专业建议。"


def smart_recognize(image_path):
    """核心识别逻辑：结合果蔬识别和菜品识别"""
    # 1. 果蔬识别
    ingredient_result = recognize_ingredient(image_path)
    valid_ingredients = []
    if ingredient_result and "result" in ingredient_result:
        for item in ingredient_result["result"][:3]:
            try:
                conf = float(item.get('score', 0.0))
            except (TypeError, ValueError):
                conf = 0.0
            name = item['name']
            if name != "非果蔬食材" and conf > 0.5:
                valid_ingredients.append((name, conf, "果蔬"))

    # 2. 菜品识别
    dish_result = recognize_dish(image_path)
    valid_dishes = []
    if dish_result and "result" in dish_result:
        for item in dish_result["result"][:3]:
            raw = item.get('score', item.get('probability', 0.0))
            try:
                conf = float(raw)
            except (TypeError, ValueError):
                conf = 0.0
            name = item['name']
            if name != "非菜" and conf > 0.5:
                valid_dishes.append((name, conf, "菜品"))

    # 3. 智能决策
    final_name, final_conf, final_cat = None, 0.0, "未知"

    if valid_dishes:
        final_name, final_conf, final_cat = max(valid_dishes, key=lambda x: x[1])
    elif valid_ingredients:
        final_name, final_conf, final_cat = max(valid_ingredients, key=lambda x: x[1])
    else:
        # 如果都没有高置信度的结果，尝试从所有候选中找一个最高的
        all_candidates = []
        if ingredient_result and "result" in ingredient_result:
            for item in ingredient_result["result"][:3]:
                try:
                    conf = float(item.get('score', 0.0))
                except (TypeError, ValueError):
                    conf = 0.0
                name = item['name']
                if name != "非果蔬食材":
                    all_candidates.append((name, conf, "果蔬"))
        if dish_result and "result" in dish_result:
            for item in dish_result["result"][:3]:
                raw = item.get('score', item.get('probability', 0.0))
                try:
                    conf = float(raw)
                except (TypeError, ValueError):
                    conf = 0.0
                name = item['name']
                if name != "非菜":
                    all_candidates.append((name, conf, "菜品"))

        if all_candidates:
            final_name, final_conf, final_cat = max(all_candidates, key=lambda x: x[1])
        else:
            return None

    # 获取营养信息
    nutrition = get_nutrition_info(final_name)
    if not isinstance(nutrition, dict):
        nutrition = {"calories": 0, "protein": 0, "fat": 0, "carbs": 0}

    return {
        "name": final_name,
        "confidence": final_conf,
        "category": final_cat,
        "nutrition": nutrition,
    }



# 4. 路由与控制器 (Routes)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('注册成功！请设置你的健康目标。')
        # 登录新用户并跳转到目标设置
        login_user(user)
        return redirect(url_for('set_goal'))
    return render_template('register.html', title='注册', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('用户名或密码错误')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html', title='登录', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/set_goal', methods=['GET', 'POST'])
def set_goal():
    form = GoalForm()
    if form.validate_on_submit():
        current_user.current_weight = form.current_weight.data
        current_user.target_weight = form.target_weight.data
        db.session.commit()
        # 更新 current_weight 和 target_weight 变量（虽然这里未使用但保留原有逻辑）
        current_weight = current_user.current_weight
        target_weight = current_user.target_weight
        return redirect(url_for('index'))
    elif request.method == 'GET':
        form.current_weight.data = current_user.current_weight
        form.target_weight.data = current_user.target_weight

    return render_template('set_goal.html', form=form)


@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error="请选择图片")
        file = request.files['file']
        if file.filename == '':
            return render_template('index.html', error="请选择图片")
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            name, ext = os.path.splitext(filename)
            filename = f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}{ext}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            result = smart_recognize(filepath)
            if result:
                # 保存到数据库
                log_entry = DietLog(
                    user_id=current_user.id,
                    food_name=result['name'],
                    category=result['category'],
                    confidence=result['confidence'],
                    calories=result['nutrition']['calories'],
                    protein=result['nutrition']['protein'],
                    fat=result['nutrition']['fat'],
                    carbs=result['nutrition']['carbs'],
                    image_filename=filename
                )
                db.session.add(log_entry)
                db.session.commit()

                # 获取针对当前食物的个性化建议
                instant_advice = get_instant_recommendation(current_user, {
                    'name': result['name'],
                    **result['nutrition']
                })

                recent_logs = DietLog.query.filter_by(user_id=current_user.id) \
                    .order_by(DietLog.timestamp.desc()) \
                    .limit(5).all()

                # 将建议传回前端渲染
                return render_template('index.html',
                                       result=result,
                                       filename=filename,
                                       instant_advice=instant_advice,
                                       recent_logs=recent_logs)
            else:
                return render_template('index.html', error="未识别出有效食物")
        else:
            return render_template('index.html', error="请上传图片（JPG/PNG等）")

    # GET 请求展示历史记录
    recent_logs = DietLog.query.filter_by(user_id=current_user.id) \
        .order_by(DietLog.timestamp.desc()) \
        .limit(5).all()

    return render_template('index.html', recent_logs=recent_logs)


@app.route('/correct_food', methods=['POST'])
@login_required
def correct_food():
    # 获取用户手动输入的新名称
    new_name = request.form.get('new_name')
    # 获取刚才识别记录的 ID（用于更新）
    log_id = request.form.get('log_id')

    if not new_name or not log_id:
        return redirect(url_for('index'))

    # 1. 调用 AI 获取精准营养成分
    new_nutrition = get_nutrition_by_ai(new_name)

    # 2. 更新数据库中的记录
    log_entry = DietLog.query.get(log_id)
    if log_entry and log_entry.user_id == current_user.id:
        log_entry.food_name = new_name
        log_entry.calories = new_nutrition['calories']
        log_entry.protein = new_nutrition['protein']
        log_entry.fat = new_nutrition['fat']
        log_entry.carbs = new_nutrition['carbs']
        db.session.commit()

        # 3. 重新获取个性化建议
        instant_advice = get_instant_recommendation(current_user, {
            'name': new_name,
            **new_nutrition
        })

        # 4. 获取最新的历史记录
        recent_logs = DietLog.query.filter_by(user_id=current_user.id) \
            .order_by(DietLog.timestamp.desc()).limit(10).all()

        # 重新渲染首页，展示修正后的结果
        return render_template('index.html',
                               result={'name': new_name, 'nutrition': new_nutrition},
                               instant_advice=instant_advice,
                               recent_logs=recent_logs)

    return redirect(url_for('index'))



# 5. 主程序入口


if __name__ == '__main__':
    # 初始化数据库
    with app.app_context():
        os.makedirs('instance', exist_ok=True)
        db.create_all()

    app.run(debug=True, host='0.0.0.0', port=5000)
