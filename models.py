# models.py
from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# 初始化数据库实例
db = SQLAlchemy()


# ==========================================
# 用户模型 (User Model)
# ==========================================

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    # 健康数据
    current_weight = db.Column(db.Float)  # 当前体重（kg）
    target_weight = db.Column(db.Float)  # 目标体重（kg）

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


# ==========================================
# 饮食记录模型 (DietLog Model)
# ==========================================

class DietLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # 识别结果与营养数据
    food_name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    confidence = db.Column(db.Float, nullable=False)

    calories = db.Column(db.Float, nullable=False)
    protein = db.Column(db.Float, nullable=False)
    fat = db.Column(db.Float, nullable=False)
    carbs = db.Column(db.Float, nullable=False)

    image_filename = db.Column(db.String(200))  # 保存图片文件名
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # 关联用户
    user = db.relationship('User', backref=db.backref('diet_logs', lazy=True))

    def __repr__(self):
        return f'<DietLog {self.food_name} for User {self.user_id}>'
