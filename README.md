智能饮食系统 (Smart Diet System)
智能饮食系统 是一款基于 Python 开发的个人健康管理 Web 应用。它通过多重 AI 技术（图像识别 + 大语言模型）帮助用户记录饮食、分析营养摄入，并根据个人的减脂或增肌目标提供定制化的膳食建议。个人开发项目，欢迎交流学习。

核心功能
智能食物识别：支持用户上传图片或开启摄像头实时拍照，集成百度 AI 接口自动识别果蔬及菜品。

本地数据库：内置常见食物的每 100g 热量、蛋白质、脂肪、碳水数据。

云端 AI 补全：若用户修正识别名称，系统会调用阿里 通义千问 (Qwen-turbo) 实时查询精准营养成分。

个性化 AI 膳食建议：结合用户的当前体重、目标体重及 TDEE 准则，由大模型生成包含“食用建议”、“平替食物”及“今日推荐食谱”的亲切对话式建议。

健康目标管理：支持用户注册登录，设定体重目标，并以进度条形式直观展示减重/增肌进程。

饮食足迹记录：自动保存用户的识别历史，形成每日饮食日志，支持热量摄入统计。

🛠️ 技术栈
后端：Python 3.13, Flask 框架。

数据库：SQLAlchemy (SQLite) 实现用户数据与记录的持久化。

前端：HTML5, CSS3 (采用响应式布局), 原生 JavaScript。

AI 接口：

百度智能云：果蔬识别 & 菜品识别 API。

阿里 DashScope：通义千问大模型 API。

其他：Flask-Login (权限管理), Flask-WTF (表单校验), Pillow (图像处理)。

项目结构：
Plaintext

Smart-diet-system/
├── app.py # Flask 应用核心逻辑与路由
├── models.py # 数据库模型 (User, DietLog)
├── api/ # 第三方 AI 接口集成脚本
├── config/ # API 密钥与环境变量配置
├── nutrition/ # 本地营养数据库与查询算法
├── static/ # 静态资源 (CSS 样式, JS 逻辑, 上传图片)
├── templates/ # HTML 模板文件 (MVC 的 View 层)
├── instance/ # 本地 SQLite 数据库文件
└── requirements.txt # 项目依赖列表

本地部署流程：

1. 克隆项目
   Bash
   git clone https://github.com/Cail321/Smart-diet-system.git
   cd Smart-diet-system
   或直接下载压缩包
2. 安装依赖
   请使用虚拟环境：

Bash

pip install -r requirements.txt 3. 配置环境变量
在项目根目录下创建 .env 文件，并填写您的 API 密钥：

代码段

BAIDU_API_KEY=您的百度 API 密钥
BAIDU_SECRET_KEY=您的百度 Secret 密钥
DASHSCOPE_API_KEY=您的阿里 DashScope 密钥 4. 启动应用
Bash

python app.py
访问浏览器 http://127.0.0.1:5000 即可开始使用。

运行预览：
首页：展示健康数据看板与识别入口。

识别结果：显示识别出的食物名称及其详细营养比例。

AI 建议：提供基于大模型的深度健康点评。

Author: Cail321
