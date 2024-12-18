from openai import ChatCompletion

import random
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from matplotlib import rcParams

rcParams['font.sans-serif'] = ['SimHei'] 
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
    "通信/电信/网络设备": {"average": 11092, "median": 9500},
    "通信/电信运营/增值服务": {"average": 11054, "median": 9000},
    "石油/石化/化工": {"average": 11042, "median": 9000},
    "仪器仪表及工业自动化": {"average": 10956, "median": 9000},
    "中介服务": {"average": 10830, "median": 8500},
    "互联网/电子商务": {"average": 10802, "median": 9000},
    "网络游戏": {"average": 10654, "median": 8402},
    "医疗设备/器械": {"average": 10643, "median": 8000},
    "房地产/建筑/建材/工程": {"average": 10378, "median": 8425},
    "检测/认证": {"average": 10262, "median": 8425},
    "汽车/摩托车": {"average": 10256, "median": 8492},
    "大型设备/机电设备/重工业": {"average": 10195, "median": 8330},
    "环保": {"average": 10032, "median": 8000},
    "办公用品及设备": {"average": 9784, "median": 6787},
    "贸易/进出口": {"average": 9735, "median": 7844},
    "家居/室内设计/装饰装潢": {"average": 9625, "median": 8000},
    "农/林/牧/渔": {"average": 9580, "median": 7500},
    "耐用消费品": {"average": 9552, "median": 7285},
    "快速消费品": {"average": 9434, "median": 7500},
    "媒体/出版/影视/文化传播": {"average": 9351, "median": 7500},
    "医疗/护理/美容/保健/卫生": {"average": 9337, "median": 7500},
    "教育/培训/院校": {"average": 9304, "median": 7500},
    "交通运输": {"average": 9250, "median": 7500},
    "加工制造（原料加工/模具）": {"average": 9204, "median": 7500},
    "广告/会展/公关": {"average": 9105, "median": 7500},
    "娱乐/体育/休闲": {"average": 9049, "median": 7500},
    "物流/仓储": {"average": 9010, "median": 7500},
    "零售/批发": {"average": 8978, "median": 7500},
    "旅游/度假": {"average": 7939, "median": 6740},
    "印刷/包装/造纸": {"average": 7894, "median": 6500},
    "酒店/餐饮": {"average": 7746, "median": 6000},
    "物业管理/商业中心": {"average": 7360, "median": 6000},
    "教育/学术": {"average": 3000, "median": 2000}  # 新增教育/学术行业
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
    "保险经纪人": "保险",
    "硬件工程师": "计算机硬件",
    "生物工程师": "医药/生物工程",
    "通信设备工程师": "通信/电信/网络设备",
    "电信运营专家": "通信/电信运营/增值服务",
    "化工工程师": "石油/石化/化工",
    "自动化工程师": "仪器仪表及工业自动化",
    "中介服务专员": "中介服务",
    "电商经理": "互联网/电子商务",
    "游戏开发师": "网络游戏",
    "医疗设备工程师": "医疗设备/器械",
    "建筑工程师": "房地产/建筑/建材/工程",
    "质量检测员": "检测/认证",
    "汽车工程师": "汽车/摩托车",
    "机电设备工程师": "大型设备/机电设备/重工业",
    "环保工程师": "环保",
    "办公设备专员": "办公用品及设备",
    "进出口专员": "贸易/进出口",
    "室内设计师": "家居/室内设计/装饰装潢",
    "农牧工程师": "农/林/牧/渔",
    "消费品经理": "耐用消费品",
    "快消品经理": "快速消费品",
    "文化传播专员": "媒体/出版/影视/文化传播",
    "护理师": "医疗/护理/美容/保健/卫生",
    "教育培训师": "教育/培训/院校",
    "交通工程师": "交通运输",
    "模具制造师": "加工制造（原料加工/模具）",
    "广告策划师": "广告/会展/公关",
    "体育教练": "娱乐/体育/休闲",
    "物流专员": "物流/仓储",
    "零售经理": "零售/批发",
    "旅行顾问": "旅游/度假",
    "包装工程师": "印刷/包装/造纸",
    "餐饮经理": "酒店/餐饮",
    "物业管理员": "物业管理/商业中心",
    "学生": "教育/学术"  # 新增学生职业
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
    # 根据年龄确定可选的教育背景
    if age < 22:
        # 18 <= age < 22：高中、本科
        edu_choices = ["高中", "本科"]
        edu_weights = [0.2, 0.8]  # 调整权重以反映年轻人可能更倾向于在读本科
    elif 22 <= age < 25:
        # 22 <= age < 25：本科、硕士
        edu_choices = ["高中", "本科", "硕士"]
        edu_weights = [0.10, 0.70, 0.20]
    else:
        # age >= 25：本科、硕士、博士
        edu_choices = ["高中", "本科", "硕士", "博士"]
        edu_weights = [0.10, 0.60, 0.3, 0.1]
    education = weighted_choice(edu_choices, edu_weights)
    
    # 关系状态分布
    rel_choices = ["单身", "已婚", "离异", "丧偶", "恋爱中"]
    rel_weights = [0.5, 0.3, 0.1, 0.05, 0.05]
    relationship_status = weighted_choice(rel_choices, rel_weights)
    
    city = pick_random_from_dict(city_income_mapping)
    
    # 根据年龄决定是否为学生
    student_probability = np.clip((40 - age) / 22, 0, 0.04)  # 年龄越小，成为学生的概率越高，最高30%
    if random.random() < student_probability:
        occupation = "学生"
    else:
        occupation = pick_random_from_dict(occupation_to_industry)
    
    industry = occupation_to_industry[occupation]
    
    # 计算收入
    if occupation == "学生":
        # 学生收入固定为温饱水平或更低
        annual_income = random.randint(19000, 45000)  # 温饱到小康
        income_level = get_income_level(annual_income)
    else:
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
        "city_country": f"{city}",
        "birth_city_country": f"{birth_city_country}",
        "education": education,
        "occupation": occupation,
        "income": annual_income,
        "income_level": income_level,
        "relationship_status": relationship_status
    }
    return user_profile

def visualize(profiles_dict: dict):
    # ------------------- 数据统计 -------------------
    profiles = list(profiles_dict.values())
    ages = [p["age"] for p in profiles]
    incomes = [p["income"] for p in profiles]
    income_levels = [p["income_level"] for p in profiles]
    sexes = [p["sex"] for p in profiles]
    educations = [p["education"] for p in profiles]
    relationship_statuses = [p["relationship_status"] for p in profiles]
    city_countries = [p["city_country"] for p in profiles]
    birth_city_countries = [p["birth_city_country"] for p in profiles]
    occupations = [p["occupation"] for p in profiles]

    # ------------------- 可视化 -------------------
    fig, axes = plt.subplots(3, 3, figsize=(18, 16))

    # 年龄分布
    axes[0,0].hist(ages, bins=15, color='skyblue', edgecolor='black')
    axes[0,0].set_title("Age Distribution")
    axes[0,0].set_xlabel("Age")
    axes[0,0].set_ylabel("Count")

    # 收入分布
    axes[0,1].hist(incomes, bins=30, color='orange', edgecolor='black')
    axes[0,1].set_title("Income Distribution")
    axes[0,1].set_xlabel("Annual Income")
    axes[0,1].set_ylabel("Count")

    # 收入等级分布
    income_count = Counter(income_levels)
    axes[0,2].bar(income_count.keys(), income_count.values(), color='gray')
    axes[0,2].set_title("Income Level Distribution")
    axes[0,2].set_xlabel("Income Level")
    axes[0,2].set_ylabel("Count")

    # 性别比例
    sex_count = Counter(sexes)
    axes[1,0].pie(sex_count.values(), labels=sex_count.keys(), autopct='%1.1f%%', startangle=90, colors=['lightblue', 'pink', 'purple'])
    axes[1,0].set_title("Sex Distribution")

    # 教育水平
    edu_count = Counter(educations)
    axes[1,1].bar(edu_count.keys(), edu_count.values(), color='cyan')
    axes[1,1].set_title("Education Level Distribution")

    # 关系状态
    rel_count = Counter(relationship_statuses)
    axes[1,2].bar(rel_count.keys(), rel_count.values(), color='yellow')
    axes[1,2].set_title("Relationship Status Distribution")

    # 城市分布
    city_count = Counter(city_countries)
    axes[2,0].barh(city_count.keys(), city_count.values(), color='brown')
    axes[2,0].set_title("City Distribution")

    # 出生地分布
    birth_count = Counter(birth_city_countries)
    axes[2,1].barh(birth_count.keys(), birth_count.values(), color='green')
    axes[2,1].set_title("Birth City Country Distribution")

    # 职业分布
    occ_count = Counter(occupations)
    axes[2,2].barh(list(occ_count.keys()), list(occ_count.values()), color='purple')
    axes[2,2].set_title("Occupation Distribution")

    plt.tight_layout()
    plt.savefig("1.jpg")
    

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
    with open("data/profiles/user_bot_profiles_300.json", "w", encoding="utf-8") as f:
        json.dump(profiles, f, ensure_ascii=False, indent=4)
    
    visualize(profiles)