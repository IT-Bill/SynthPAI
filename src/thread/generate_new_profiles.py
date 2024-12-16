from openai import ChatCompletion

import random
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from matplotlib import rcParams

rcParams['font.sans-serif'] = ['Noto Sans CJK JP'] 
rcParams['axes.unicode_minus'] = False

# ------------------- 原始数据 -------------------
industry_income_mapping = {
    "基金/证券/期货/投资": {"average": 13804, "median": 10429},
    "计算机软件": {"average": 12146, "median": 10500},
    "电子技术/半导体/集成电路": {"average": 11870, "median": 9500},
    "新能源/电气/电力": {"average": 11840, "median": 9500},
    "IT服务（系统/数据/维护）": {"average": 11768, "median": 10000},
    "银行": {"average": 11736, "median": 10000},
    "能源/矿产/采掘/冶炼": {"average": 11634, "median": 9000},
    "专业服务/咨询": {"average": 11568, "median": 8500},
    "航空/航天研究与制造": {"average": 11544, "median": 9000},
    "保险": {"average": 11517, "median": 9215},
    "计算机硬件": {"average": 11400, "median": 9000},
    "医药/生物工程": {"average": 11324, "median": 9000},
    "通信/电信/网络设备": {"average": 11202, "median": 9500},
    "通信/电信运营/增值服务": {"average": 11200, "median": 8500},
    "石油/石化/化工": {"average": 11094, "median": 9500},
    "仪器仪表及工业自动化": {"average": 10962, "median": 9500},
    "中介服务": {"average": 10900, "median": 9000},
    "互联网/电子商务": {"average": 10827, "median": 9000},
    "网络游戏": {"average": 10654, "median": 8500},
    "医疗设备/器械": {"average": 10560, "median": 8000},
    "房地产/建筑/建材/工程": {"average": 10378, "median": 8000},
    "检验/检测/认证": {"average": 10262, "median": 8425},
}

occupation_to_industry = {
    "基金经理": "基金/证券/期货/投资",
    "软件工程师": "计算机软件",
    "半导体工程师": "电子技术/半导体/集成电路",
    "电力工程师": "新能源/电气/电力",
    "数据分析师": "IT服务（系统/数据/维护）",
    "银行职员": "银行",
    "矿产工程师": "能源/矿产/采掘/冶炼",
    "咨询顾问": "专业服务/咨询",
    "航空工程师": "航空/航天研究与制造",
    "保险代理人": "保险",
    "硬件工程师": "计算机硬件",
    "医药研究员": "医药/生物工程",
    "电信工程师": "通信/电信/网络设备",
    "石化工程师": "石油/石化/化工",
    "自动化工程师": "仪器仪表及工业自动化",
    "电商运营": "互联网/电子商务",
    "游戏开发": "网络游戏",
    "医疗器械销售": "医疗设备/器械",
    "建筑工程师": "房地产/建筑/建材/工程",
    "认证工程师": "检验/检测/认证",
}

city_income_mapping = {
    "上海": {"average": 13888, "median": 11500},
    "北京": {"average": 13552, "median": 11000},
    "深圳": {"average": 13067, "median": 10500},
    "杭州": {"average": 12143, "median": 10000},
    "苏州": {"average": 11348, "median": 9000},
    "南京": {"average": 11240, "median": 9000},
    "广州": {"average": 11186, "median": 9000},
    "宁波": {"average": 10989, "median": 9000},
    "厦门": {"average": 10641, "median": 8750},
    "珠海": {"average": 10508, "median": 8500},
    "无锡": {"average": 10430, "median": 8500},
    "武汉": {"average": 10381, "median": 8500},
    "长沙": {"average": 10136, "median": 8143},
    "东莞": {"average": 10086, "median": 8000},
    "佛山": {"average": 10015, "median": 8000},
    "合肥": {"average": 10003, "median": 8000},
    "成都": {"average": 9881, "median": 8000},
    "济南": {"average": 9546, "median": 8000},
    "福州": {"average": 9473, "median": 7500},
    "重庆": {"average": 9441, "median": 7500},
    "西安": {"average": 9440, "median": 7500},
    "青岛": {"average": 9356, "median": 7500},
    "南昌": {"average": 9058, "median": 7500},
    "天津": {"average": 9022, "median": 7500},
    "郑州": {"average": 8948, "median": 7500},
    "昆明": {"average": 8918, "median": 7000},
    "南宁": {"average": 8916, "median": 7000},
    "乌鲁木齐": {"average": 8885, "median": 7250},
    "贵阳": {"average": 8698, "median": 7000},
    "海口": {"average": 8571, "median": 7000},
    "兰州": {"average": 8377, "median": 7000},
    "大连": {"average": 8303, "median": 6750},
    "石家庄": {"average": 8032, "median": 6650},
    "太原": {"average": 7997, "median": 6500},
    "烟台": {"average": 7997, "median": 6500},
    "长春": {"average": 7727, "median": 6450},
    "沈阳": {"average": 7663, "median": 6000},
    "哈尔滨": {"average": 7554, "median": 6000},
}


china_household_assets_2024 = {
    "富豪/超高净值": {"min_income": 505000, "label": "富豪"},
    "高级中产/高净值": {"min_income": 195000, "label": "高级中产"},
    "普通中产": {"min_income": 99000, "label": "普通中产"},
    "小康": {"min_income": 45000, "label": "小康"},
    "温饱": {"min_income": 19000, "label": "温饱"}
}

# ------------------- 辅助函数 -------------------
def pick_random_from_dict(d):
    return random.choice(list(d.keys()))

def sample_income_from_distribution(avg, median):
    if median <= 0:
        median = 1
    ratio = avg / median
    if ratio <= 0:
        ratio = 1
    sigma_squared = 2 * np.log(ratio)
    if sigma_squared < 0:
        sigma_squared = 0.1
    sigma = np.sqrt(sigma_squared)
    mu = np.log(median)
    income = np.random.lognormal(mu, sigma)
    income = round(income, -3)  # round to thousand
    return int(income)

def get_income_level(income):
    # 根据income从大到小依次匹配相应等级
    for level, data in china_household_assets_2024.items():
        if income >= data["min_income"]:
            return data["label"]
    return "温饱"

def weighted_choice(choices, weights):
    cumulative_weights = np.cumsum(weights)
    r = random.random() * cumulative_weights[-1]
    for choice, cw in zip(choices, cumulative_weights):
        if r <= cw:
            return choice

def choose_birth_city(city_country):
    # 50%概率与city_country相同
    if random.random() < 0.5:
        return city_country
    else:
        # 否则，根据接近程度加权选择不同城市
        # 接近度通过平均收入差来衡量
        current_avg = city_income_mapping[city_country]["average"]
        other_cities = [c for c in city_income_mapping.keys() if c != city_country]
        
        # 根据平均收入差计算权重
        weights = []
        for c in other_cities:
            diff = abs(city_income_mapping[c]["average"] - current_avg)
            weight = 1 / (1 + diff)  # diff越小，weight越大
            weights.append(weight)
        
        return weighted_choice(other_cities, weights)

def generate_user_profile():
    # 年龄：18-40岁正态分布
    age = int(np.clip(np.random.normal(26, 4), 18, 40))
    
    # 性别分布：男性:53%, 女性:47%
    sex_choices = ["男性", "女性"]
    sex_weights = [0.53, 0.47]
    sex = weighted_choice(sex_choices, sex_weights)
    
    # 教育分布：高中, 本科, 硕士, 博士
    edu_choices = ["高中", "本科", "硕士", "博士"]
    edu_weights = [0.05, 0.50, 0.35, 0.10]
    education = weighted_choice(edu_choices, edu_weights)
    
    # 关系状态分布
    rel_choices = ["单身", "已婚", "离异", "丧偶", "恋爱中"]
    rel_weights = [0.4, 0.3, 0.1, 0.05, 0.15]
    relationship_status = weighted_choice(rel_choices, rel_weights)
    
    city = pick_random_from_dict(city_income_mapping)
    occupation = pick_random_from_dict(occupation_to_industry)
    industry = occupation_to_industry[occupation]
    
    # 计算收入
    ind_data = industry_income_mapping[industry]
    city_data = city_income_mapping[city]
    avg_income = (ind_data["average"] + city_data["average"]) / 2
    med_income = (ind_data["median"] + city_data["median"]) / 2
    annual_income = sample_income_from_distribution(avg_income, med_income) * 12
    income_level = get_income_level(annual_income)
    
    # 出生地选择
    birth_city_country = choose_birth_city(city)
    
    user_profile = {
        "age": age,
        "sex": sex,
        "city_country": f"{city}, 中国",
        "birth_city_country": f"{birth_city_country}, 中国",
        "education": education,
        "occupation": occupation,
        "income": annual_income,
        "income_level": income_level,
        "relationship_status": relationship_status
    }
    return user_profile

# ----------------------------------------------------
def generate_new_profile():
    system_prompt = """
你是一个人口统计学方面的专家，可以准确地描绘现实生活中的人物，包括他们的年龄、教育背景、关系状况、职业、居住地、出生地和收入等特征，确保这些特征之间的配合合理且符合现实生活情况。
生成50个人的资料，尽量保持特征分布多样且接近真实生活的情形。
性别(sex): ["男性", "女性", "LGBT"]
收入水平(income_level): ["低", "中", "高", "非常高"]
收入(income): 使用CNY作为单位
关系状况(relationship_status): ["单身", "已婚", "离异", "丧偶", "恋爱中"]
精确列出教育背景和专业。
收入水平根据以下标准转换为收入等级:

低收入 (<30k CNY)
中等收入 (30-60k CNY)
高收入 (60-150k CNY)
非常高收入 (>150k CNY)
    """

# ----------------------------------------------------

if __name__ == "__main__":
    import json
    num_samples = 300
    profiles = {f"pers{i + 1}": generate_user_profile() for i in range(num_samples)}
    with open("generated_profiles.json", "w", encoding="utf-8") as f:
        json.dump(profiles, f, ensure_ascii=False, indent=4)
    
    