# nutrition/local_nutrition_db.py

# ==========================================
# 1. 营养数据库 (NUTRITION_DB)
# ==========================================
# 格式: {食物名称: {calories: kcal, protein: g, fat: g, carbs: g}}
# 数据单位均为每 100g

NUTRITION_DB = {
    # --- 主食类 ---
    '白米饭':   {'calories': 116, 'protein': 2.6,  'fat': 0.3,  'carbs': 25.9},
    '糙米饭':   {'calories': 111, 'protein': 2.6,  'fat': 0.9,  'carbs': 23.0},
    '馒头':     {'calories': 223, 'protein': 7.0,  'fat': 1.1,  'carbs': 47.0},
    '全麦面包': {'calories': 247, 'protein': 13.0, 'fat': 3.0,  'carbs': 41.0},
    '燕麦片':   {'calories': 389, 'protein': 16.9, 'fat': 6.9,  'carbs': 66.3},
    '米饭':     {'calories': 116, 'protein': 2.6,  'fat': 0.3,  'carbs': 25.9},
    '面条':     {'calories': 280, 'protein': 8.0,  'fat': 2.0,  'carbs': 58.0},

    # --- 水果类 ---
    '草莓':     {'calories': 32,  'protein': 1.0,  'fat': 0.2,  'carbs': 7.7},
    '苹果':     {'calories': 52,  'protein': 0.3,  'fat': 0.2,  'carbs': 13.0},
    '香蕉':     {'calories': 89,  'protein': 1.1,  'fat': 0.3,  'carbs': 22.8},
    '橙子':     {'calories': 47,  'protein': 0.9,  'fat': 0.1,  'carbs': 11.8},
    '西瓜':     {'calories': 30,  'protein': 0.6,  'fat': 0.2,  'carbs': 7.6},
    '葡萄':     {'calories': 43,  'protein': 0.7,  'fat': 0.2,  'carbs': 10.0},
    '蓝莓':     {'calories': 57,  'protein': 0.7,  'fat': 0.3,  'carbs': 14.5},
    '猕猴桃':   {'calories': 61,  'protein': 1.1,  'fat': 0.5,  'carbs': 14.7},

    # --- 蔬菜类 ---
    '胡萝卜':   {'calories': 41,  'protein': 0.9,  'fat': 0.2,  'carbs': 9.6},
    '生菜':     {'calories': 15,  'protein': 1.4,  'fat': 0.2,  'carbs': 2.9},
    '黄瓜':     {'calories': 16,  'protein': 0.8,  'fat': 0.2,  'carbs': 3.6},
    '西红柿':   {'calories': 20,  'protein': 0.9,  'fat': 0.2,  'carbs': 3.9},
    '土豆':     {'calories': 77,  'protein': 2.0,  'fat': 0.1,  'carbs': 17.2},
    '菠菜':     {'calories': 23,  'protein': 2.9,  'fat': 0.4,  'carbs': 3.6},
    '西兰花':   {'calories': 34,  'protein': 2.8,  'fat': 0.4,  'carbs': 6.6},

    # --- 肉类/菜品 ---
    '红烧肉':   {'calories': 392, 'protein': 29.0, 'fat': 32.0, 'carbs': 5.0},
    '宫保鸡丁': {'calories': 160, 'protein': 20.0, 'fat': 8.0,  'carbs': 2.0},
    '清炒时蔬': {'calories': 60,  'protein': 2.0,  'fat': 4.0,  'carbs': 6.0},
    '煎蛋':     {'calories': 144, 'protein': 13.3, 'fat': 8.8,  'carbs': 2.8},
    '鸡胸肉':   {'calories': 165, 'protein': 31.0, 'fat': 3.6,  'carbs': 0.0},
    '瘦牛肉':   {'calories': 250, 'protein': 26.0, 'fat': 15.0, 'carbs': 0.0},
    '三文鱼':   {'calories': 208, 'protein': 20.0, 'fat': 13.0, 'carbs': 0.0},
    '虾仁':     {'calories': 99,  'protein': 20.0, 'fat': 0.3,  'carbs': 0.0},
    '猪肉':     {'calories': 520, 'protein': 15.0, 'fat': 50.0, 'carbs': 0.0},
    '牛排':     {'calories': 271, 'protein': 26.0, 'fat': 18.0, 'carbs': 0.0},

    # --- 蛋奶豆制品 ---
    '鸡蛋':     {'calories': 155, 'protein': 13.0, 'fat': 11.0, 'carbs': 1.1},
    '牛奶':     {'calories': 61,  'protein': 3.2,  'fat': 3.3,  'carbs': 4.8},
    '豆腐':     {'calories': 81,  'protein': 8.1,  'fat': 4.2,  'carbs': 1.9},
    '豆浆':     {'calories': 30,  'protein': 3.3,  'fat': 0.6,  'carbs': 1.8},
    '希腊酸奶': {'calories': 59,  'protein': 10.0, 'fat': 0.4,  'carbs': 3.6},

    # --- 零食/饮料 ---
    '可口可乐': {'calories': 139, 'protein': 0.0,  'fat': 0.0,  'carbs': 35.0},
    '巧克力':   {'calories': 546, 'protein': 4.9,  'fat': 31.3, 'carbs': 61.0},
    '薯片':     {'calories': 547, 'protein': 7.0,  'fat': 35.0, 'carbs': 54.0},
    '冰淇淋':   {'calories': 207, 'protein': 3.5,  'fat': 11.0, 'carbs': 24.0},
    '能量棒':   {'calories': 450, 'protein': 10.0, 'fat': 15.0, 'carbs': 65.0},

    # --- 默认值 ---
    '默认':     {'calories': 100, 'protein': 5.0,  'fat': 3.0,  'carbs': 15.0}
}


# ==========================================
# 2. 别名映射表 (ALIAS_MAP)
# ==========================================
# key: 用户输入别名 -> value: NUTRITION_DB 标准名称

ALIAS_MAP = {
    # 蔬菜类
    '红萝卜': '胡萝卜',
    '白萝卜': '萝卜',       # 需确保 DB 中存在 '萝卜'
    '青菜':   '小白菜',     # 需确保 DB 中存在 '小白菜'
    '番茄':   '西红柿',
    '马铃薯': '土豆',
    '地瓜':   '红薯',
    '芋头':   '芋艿',

    # 水果类
    '奇异果': '猕猴桃',
    '提子':   '葡萄',
    '橙子':   '橙',
    '桔子':   '橘子',

    # 肉类/菜品
    '鸡腿肉': '鸡胸肉',     # 替代映射
    '牛肉片': '瘦牛肉',
    '鱼块':   '三文鱼',     # 替代映射

    # 饮料
    '可乐': '可口可乐 (330ml)',
    '雪碧': '雪碧 (330ml)', # 需确保 DB 中存在对应条目
}


# ==========================================
# 3. 核心查询函数
# ==========================================

def get_nutrition_info(food_name: str):
    """
    根据食物名称查询营养信息。
    支持：精确匹配、别名转换、模糊匹配（包含匹配）。
    """
    food_name = food_name.strip()

    # 1. 检查别名映射
    if food_name in ALIAS_MAP:
        standard_name = ALIAS_MAP[food_name]
        print(f"💡 别名转换: '{food_name}' -> '{standard_name}'")
        food_name = standard_name

    # 2. 精确匹配
    if food_name in NUTRITION_DB:
        return NUTRITION_DB[food_name]

    # 3. 模糊匹配（匹配 Key 包含输入词的情况）
    for key in NUTRITION_DB:
        # 注意：这里逻辑是 输入 "苹果" -> 匹配库中 "红富士苹果" (若 key 包含 food_name)
        if food_name in key and len(food_name) <= len(key):
            return NUTRITION_DB[key]

    # 4. 未找到，返回默认值
    return NUTRITION_DB["默认"]