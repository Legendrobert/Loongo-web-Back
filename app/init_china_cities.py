# init_china_cities.py
import time
import random
from sqlalchemy.orm import Session
from database import engine, Base, SessionLocal
import models
from utils.cities_utils import get_bing_image_urls, get_ai_city_details

# 创建所有表
Base.metadata.create_all(bind=engine)

# 中国主要城市经纬度数据
def get_city_coordinates():
    # 预设一些主要城市的经纬度数据
    coordinates = {
        "北京": (39.9042, 116.4074),
        "上海": (31.2304, 121.4737),
        "广州": (23.1291, 113.2644),
        "深圳": (22.5431, 114.0579),
        "天津": (39.3434, 117.3616),
        "重庆": (29.4316, 106.9123),
        "杭州": (30.2741, 120.1551),
        "南京": (32.0603, 118.7969),
        "武汉": (30.5928, 114.3055),
        "西安": (34.3416, 108.9398),
        "成都": (30.5728, 104.0668),
        "苏州": (31.2990, 120.5853),
        "沈阳": (41.8057, 123.4315),
        "哈尔滨": (45.8038, 126.5340),
        "长沙": (28.2282, 112.9388),
        "济南": (36.6512, 117.1201),
        "厦门": (24.4792, 118.0894),
        "大连": (38.9140, 121.6147),
        "青岛": (36.0671, 120.3826),
        "郑州": (34.7466, 113.6253),
        "长春": (43.8818, 125.3228),
        "昆明": (25.0389, 102.7183),
        "贵阳": (26.6470, 106.6302),
        "南宁": (22.8170, 108.3665),
        "合肥": (31.8206, 117.2272),
        "福州": (26.0745, 119.2965),
        "南昌": (28.6820, 115.8579),
        "乌鲁木齐": (43.8256, 87.6168),
        "西宁": (36.6178, 101.7781),
        "兰州": (36.0611, 103.8343),
        "银川": (38.4872, 106.2309),
        "太原": (37.8738, 112.5643),
        "石家庄": (38.0428, 114.5149),
        "呼和浩特": (40.8424, 111.7490),
        "拉萨": (29.6500, 91.1000),
        "海口": (20.0442, 110.1995),
        "三亚": (18.2528, 109.5120),
        "桂林": (25.2736, 110.2990),
        "丽江": (26.8721, 100.2376),
        "大理": (25.6065, 100.2679),
        "黄山": (30.1333, 118.1667),
        "张家界": (29.1170, 110.4790),
        "九寨沟": (33.2000, 103.9000),
        "敦煌": (40.1130, 94.6616),
        "苏州": (31.2990, 120.5853),
        "无锡": (31.5689, 120.2991),
        "宁波": (29.8683, 121.5440),
        "绍兴": (30.0302, 120.5970),
        "舟山": (30.0364, 122.1069),
        "黄山": (30.1333, 118.1667),
        "厦门": (24.4792, 118.0894),
        "泉州": (24.9139, 118.5856),
        "景德镇": (29.2691, 117.2058),
        "九江": (29.7050, 116.0019),
        "青岛": (36.0671, 120.3826),
        "烟台": (37.4638, 121.4439),
        "威海": (37.5281, 122.0571),
        "开封": (34.7970, 114.3077),
        "洛阳": (34.6190, 112.4548),
        "宜昌": (30.6927, 111.2866),
        "张家界": (29.1170, 110.4790),
        "凤凰": (27.9482, 109.5996),
        "广州": (23.1291, 113.2644),
        "深圳": (22.5431, 114.0579),
        "珠海": (22.2710, 113.5767),
        "汕头": (23.3535, 116.6820),
        "南宁": (22.8170, 108.3665),
        "桂林": (25.2736, 110.2990),
        "海口": (20.0442, 110.1995),
        "三亚": (18.2528, 109.5120),
        "乐山": (29.5662, 103.7649),
        "峨眉山": (29.6010, 103.3950),
        "遵义": (27.7258, 106.9251),
        "大理": (25.6065, 100.2679),
        "丽江": (26.8721, 100.2376),
        "西双版纳": (22.0074, 100.7984),
        "日喀则": (29.2550, 88.8879),
        "延安": (36.5853, 109.4898),
        "敦煌": (40.1130, 94.6616),
        "嘉峪关": (39.7955, 98.2910),
        "喀什": (39.4700, 75.9800),
        "吐鲁番": (42.9479, 89.1822),
    }
    return coordinates

# 获取城市的最佳游玩季节
def get_best_season(city_name, region):
    # 基于地区和城市特点确定最佳季节
    if region == "华南" or region == "西南":
        if city_name in ["三亚", "海口", "西双版纳"]:
            return "冬季"
        return "春秋"
    elif region == "西北":
        return "春秋"
    elif region in ["华北", "东北"]:
        if city_name in ["哈尔滨", "长春"]:
            return "冬季"  # 冰雪旅游
        return "春夏"
    elif region == "华中" or region == "华东":
        return "春秋"
    else:
        return "春秋"

# 中国各省区城市数据
def get_china_cities_data():
    cities_by_region = {
        "华北": [
            {"name": "北京", "province": "北京市", "is_capital": True, "is_tourist": True},
            {"name": "天津", "province": "天津市", "is_capital": True, "is_tourist": True},
            {"name": "石家庄", "province": "河北省", "is_capital": True, "is_tourist": False},
            {"name": "保定", "province": "河北省", "is_capital": False, "is_tourist": True},
            {"name": "承德", "province": "河北省", "is_capital": False, "is_tourist": True},
            {"name": "太原", "province": "山西省", "is_capital": True, "is_tourist": False},
            {"name": "大同", "province": "山西省", "is_capital": False, "is_tourist": True},
            {"name": "平遥", "province": "山西省", "is_capital": False, "is_tourist": True},
            {"name": "呼和浩特", "province": "内蒙古自治区", "is_capital": True, "is_tourist": False},
            {"name": "包头", "province": "内蒙古自治区", "is_capital": False, "is_tourist": False},
            {"name": "呼伦贝尔", "province": "内蒙古自治区", "is_capital": False, "is_tourist": True},
        ],
        "东北": [
            {"name": "沈阳", "province": "辽宁省", "is_capital": True, "is_tourist": False},
            {"name": "大连", "province": "辽宁省", "is_capital": False, "is_tourist": True},
            {"name": "长春", "province": "吉林省", "is_capital": True, "is_tourist": False},
            {"name": "吉林", "province": "吉林省", "is_capital": False, "is_tourist": True},
            {"name": "哈尔滨", "province": "黑龙江省", "is_capital": True, "is_tourist": True},
        ],
        "华东": [
            {"name": "上海", "province": "上海市", "is_capital": True, "is_tourist": True},
            {"name": "南京", "province": "江苏省", "is_capital": True, "is_tourist": True},
            {"name": "苏州", "province": "江苏省", "is_capital": False, "is_tourist": True},
            {"name": "无锡", "province": "江苏省", "is_capital": False, "is_tourist": True},
            {"name": "杭州", "province": "浙江省", "is_capital": True, "is_tourist": True},
            {"name": "宁波", "province": "浙江省", "is_capital": False, "is_tourist": True},
            {"name": "绍兴", "province": "浙江省", "is_capital": False, "is_tourist": True},
            {"name": "舟山", "province": "浙江省", "is_capital": False, "is_tourist": True},
            {"name": "合肥", "province": "安徽省", "is_capital": True, "is_tourist": False},
            {"name": "黄山", "province": "安徽省", "is_capital": False, "is_tourist": True},
            {"name": "福州", "province": "福建省", "is_capital": True, "is_tourist": False},
            {"name": "厦门", "province": "福建省", "is_capital": False, "is_tourist": True},
            {"name": "泉州", "province": "福建省", "is_capital": False, "is_tourist": True},
            {"name": "南昌", "province": "江西省", "is_capital": True, "is_tourist": False},
            {"name": "景德镇", "province": "江西省", "is_capital": False, "is_tourist": True},
            {"name": "九江", "province": "江西省", "is_capital": False, "is_tourist": True},
            {"name": "济南", "province": "山东省", "is_capital": True, "is_tourist": False},
            {"name": "青岛", "province": "山东省", "is_capital": False, "is_tourist": True},
            {"name": "烟台", "province": "山东省", "is_capital": False, "is_tourist": True},
            {"name": "威海", "province": "山东省", "is_capital": False, "is_tourist": True},
        ],
        "华中": [
            {"name": "郑州", "province": "河南省", "is_capital": True, "is_tourist": False},
            {"name": "开封", "province": "河南省", "is_capital": False, "is_tourist": True},
            {"name": "洛阳", "province": "河南省", "is_capital": False, "is_tourist": True},
            {"name": "武汉", "province": "湖北省", "is_capital": True, "is_tourist": True},
            {"name": "宜昌", "province": "湖北省", "is_capital": False, "is_tourist": True},
            {"name": "长沙", "province": "湖南省", "is_capital": True, "is_tourist": False},
            {"name": "张家界", "province": "湖南省", "is_capital": False, "is_tourist": True},
            {"name": "凤凰", "province": "湖南省", "is_capital": False, "is_tourist": True},
        ],
        "华南": [
            {"name": "广州", "province": "广东省", "is_capital": True, "is_tourist": True},
            {"name": "深圳", "province": "广东省", "is_capital": False, "is_tourist": True},
            {"name": "珠海", "province": "广东省", "is_capital": False, "is_tourist": True},
            {"name": "汕头", "province": "广东省", "is_capital": False, "is_tourist": True},
            {"name": "南宁", "province": "广西壮族自治区", "is_capital": True, "is_tourist": False},
            {"name": "桂林", "province": "广西壮族自治区", "is_capital": False, "is_tourist": True},
            {"name": "海口", "province": "海南省", "is_capital": True, "is_tourist": True},
            {"name": "三亚", "province": "海南省", "is_capital": False, "is_tourist": True},
        ],
        "西南": [
            {"name": "重庆", "province": "重庆市", "is_capital": True, "is_tourist": True},
            {"name": "成都", "province": "四川省", "is_capital": True, "is_tourist": True},
            {"name": "乐山", "province": "四川省", "is_capital": False, "is_tourist": True},
            {"name": "峨眉山", "province": "四川省", "is_capital": False, "is_tourist": True},
            {"name": "九寨沟", "province": "四川省", "is_capital": False, "is_tourist": True},
            {"name": "贵阳", "province": "贵州省", "is_capital": True, "is_tourist": False},
            {"name": "遵义", "province": "贵州省", "is_capital": False, "is_tourist": True},
            {"name": "昆明", "province": "云南省", "is_capital": True, "is_tourist": True},
            {"name": "大理", "province": "云南省", "is_capital": False, "is_tourist": True},
            {"name": "丽江", "province": "云南省", "is_capital": False, "is_tourist": True},
            {"name": "西双版纳", "province": "云南省", "is_capital": False, "is_tourist": True},
            {"name": "拉萨", "province": "西藏自治区", "is_capital": True, "is_tourist": True},
            {"name": "日喀则", "province": "西藏自治区", "is_capital": False, "is_tourist": True},
        ],
        "西北": [
            {"name": "西安", "province": "陕西省", "is_capital": True, "is_tourist": True},
            {"name": "延安", "province": "陕西省", "is_capital": False, "is_tourist": True},
            {"name": "兰州", "province": "甘肃省", "is_capital": True, "is_tourist": False},
            {"name": "敦煌", "province": "甘肃省", "is_capital": False, "is_tourist": True},
            {"name": "嘉峪关", "province": "甘肃省", "is_capital": False, "is_tourist": True},
            {"name": "西宁", "province": "青海省", "is_capital": True, "is_tourist": False},
            {"name": "银川", "province": "宁夏回族自治区", "is_capital": True, "is_tourist": False},
            {"name": "乌鲁木齐", "province": "新疆维吾尔自治区", "is_capital": True, "is_tourist": False},
            {"name": "喀什", "province": "新疆维吾尔自治区", "is_capital": False, "is_tourist": True},
            {"name": "吐鲁番", "province": "新疆维吾尔自治区", "is_capital": False, "is_tourist": True},
        ]
    }
    
    return cities_by_region

# 获取城市描述（手动提供一些特色城市描述，其他使用AI生成）
def get_city_descriptions():
    descriptions = {
        "北京": "中国首都，拥有故宫、长城等众多历史文化遗迹，是中国政治、文化、国际交往中心。",
        "上海": "中国最大经济中心城市，国际金融、贸易、航运中心，融合了东西方文化的国际化大都市。",
        "广州": "中国南大门，历史悠久的商业贸易中心，粤菜和粤式文化的发源地。",
        "深圳": "中国改革开放的窗口城市，科技创新中心，现代化国际大都市。",
        "杭州": "风景秀丽的江南城市，拥有西湖等世界文化遗产，是中国重要的电子商务中心。",
        "西安": "十三朝古都，历史文化名城，兵马俑等历史遗迹闻名于世，是古丝绸之路的起点。",
        "成都": "中国西南地区重要的中心城市，以休闲生活方式著称，是熊猫故乡和天府之国的代表。",
        "重庆": "中国西南地区的经济中心，山城特色明显，以火锅和江景著称。",
        "三亚": "中国著名的热带滨海旅游城市，拥有优美的海滩和热带风光。",
        "桂林": "山水甲天下，山水风光举世闻名，是中国最美的城市之一。",
        "丽江": "保存完好的少数民族古城，纳西族文化和古城风貌吸引了众多游客。",
        "哈尔滨": "中国最北方的大城市，以冰雪节庆和俄罗斯风情建筑闻名。",
    }
    return descriptions

# 初始化城市数据
def init_cities():
    db = SessionLocal()
    try:
        # 获取中国城市数据
        cities_by_region = get_china_cities_data()
        city_coordinates = get_city_coordinates()
        city_descriptions = get_city_descriptions()
        
        # 已添加城市计数
        added_count = 0
        total_count = sum(len(cities) for cities in cities_by_region.values())
        
        # 遍历区域和城市
        for region, cities in cities_by_region.items():
            for city_info in cities:
                city_name = city_info["name"]
                
                # 检查城市是否已存在
                existing_city = db.query(models.City).filter(
                    models.City.name == city_name,
                    models.City.province == city_info["province"]
                ).first()
                
                if existing_city:
                    print(f"城市 {city_name} 已存在，跳过")
                    continue
                
                # 获取城市经纬度
                latitude, longitude = city_coordinates.get(city_name, (0.0, 0.0))
                
                # 获取城市描述
                if city_name in city_descriptions:
                    description = city_descriptions[city_name]
                else:
                    # 尝试使用AI生成城市描述
                    try:
                        ai_details = get_ai_city_details(city_name)
                        description = ai_details.get("site_description", "")
                    except:
                        description = f"{city_name}是{city_info['province']}的{'省会城市' if city_info['is_capital'] else '知名城市'}，位于{region}地区。"
                
                # 获取最佳游玩季节
                best_season = get_best_season(city_name, region)
                
                # 生成随机当前温度（实际应用中应使用天气API）
                current_temperature = round(random.uniform(15.0, 32.0), 1)
                
                # 构建城市信息
                city_data = {
                    "name": city_name,
                    "province": city_info["province"],
                    "region": region,
                    "description": description,
                    "current_temperature": current_temperature,
                    "best_season": best_season,
                    "latitude": latitude,
                    "longitude": longitude,
                }
                
                # 创建城市记录
                new_city = models.City(**city_data)
                db.add(new_city)
                db.flush()  # 刷新以获取ID
                
                # 获取城市图片
                print(f"正在获取 {city_name} 的图片...")
                search_query = f"{city_name} 旅游 风景"
                image_urls = get_bing_image_urls(search_query, count=5)
                
                # 保存图片URL
                for img_url in image_urls:
                    city_image = models.CityImage(
                        city_id=new_city.id,
                        image_url=img_url
                    )
                    db.add(city_image)
                
                # 提交数据库
                db.commit()
                added_count += 1
                print(f"[{added_count}/{total_count}] 添加城市: {city_name} ({city_info['province']})，获取了 {len(image_urls)} 张图片")
                
                # 暂停一下，避免请求过快
                time.sleep(2)
                
        print(f"城市初始化完成！共添加 {added_count} 个城市。")
        
    except Exception as e:
        db.rollback()
        print(f"初始化城市数据时出错: {e}")
    finally:
        db.close()

# 执行初始化
if __name__ == "__main__":
    init_cities()