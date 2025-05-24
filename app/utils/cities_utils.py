import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import json


def get_ai_city_details(city_name):
    """获取AI生成的城市详情"""
    try:
        client = OpenAI(api_key="sk-d54d4032f3044126aa5d95d21cca5228", base_url="https://api.deepseek.com")
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "你是一个旅行官和导游，要求根据用户提供的城市信息返回城市详情。"
                        "请直接返回纯JSON格式（不要添加```json或任何markdown标记），内容为英文："
                        "{"
                        "\"suggested_visit_time\": \"建议游玩时间,直接返回时间（x-x天），不要其他内容\","
                        "\"activity_suggestions\": \"游玩项目建议（特色介绍），如果有顺序的话也请构成list列表的形式\","
                        "\"site_description\": \"景点介绍\""
                        "}"
                    )
                },
                {
                    "role": "user",
                    "content": city_name
                },
            ],
            stream=False,
        )
        answer = response.choices[0].message.content
        
        # 处理可能的markdown格式
        if answer.startswith("```") and answer.endswith("```"):
            # 移除markdown格式
            answer = answer.strip('`')
            # 如果包含json标记，也移除它
            if answer.startswith("json\n"):
                answer = answer[5:]
        
        return json.loads(answer)
    except Exception as e:
        print(f"获取AI城市详情失败: {e}")
        return {
            "suggested_visit_time": "3-5天",
            "activity_suggestions": "暂无建议活动",
            "site_description": "暂无描述"
        }

def get_bing_image_urls(query, count=3):
    """获取Bing图片搜索结果"""
    try:
        search_url = f"https://www.bing.com/images/search?q={query}&form=HDRSC2"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

        response = requests.get(search_url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        img_tags = soup.find_all("img", class_="mimg")

        # 获取图片URL
        img_urls = [img["src"] for img in img_tags if "src" in img.attrs][:count]
        return img_urls
    except Exception as e:
        print(f"获取Bing图片失败: {e}")
        return []

def get_popular_events_for_city(db, city_id):
    """获取城市热门活动"""
    # 这里应该查询数据库获取真实数据
    # 示例数据
    return [
        {
            "id": 1,
            "name": "杭州",
            "image": "https://example.com/hangzhou1.jpg",
            "description": "杭州西湖游船活动"
        },
        {
            "id": 2,
            "name": "杭州",
            "image": "https://example.com/hangzhou2.jpg",
            "description": "西溪湿地一日游"
        }
    ]

def get_featured_restaurants_for_city(db, city_id):
    """获取城市特色餐厅"""
    # 这里应该查询数据库获取真实数据
    # 示例数据
    return [
        {
            "id": 101,
            "name": "新荣记",
            "image": "https://example.com/restaurant1.jpg",
            "cuisine": ["中餐", "粤菜"],
            "recommended": True
        }
    ]

def get_cozy_hotels_for_city(db, city_id):
    """获取城市舒适酒店"""
    # 这里应该查询数据库获取真实数据
    # 示例数据
    return [
        {
            "id": 201,
            "name": "希尔顿酒店",
            "image": "https://example.com/hilton.jpg",
            "price": 1280,
            "rating": 5
        }
    ]

def get_expert_opinions_for_city(db, city_id):
    """获取专家关于城市的观点"""
    # 这里应该查询数据库获取真实数据
    # 示例数据
    return [
        {
            "id": 301,
            "title": "上海必访的10个地方",
            "author": "旅行专家",
            "languages": ["中文", "英文"]
        }
    ]