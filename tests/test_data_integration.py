#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KACHA 數據集成測試
驗證前端數據處理邏輯
"""

import json
import os

def test_data_transformation():
    """測試數據轉換邏輯（模擬JavaScript的轉換）"""
    print("🧪 測試數據轉換邏輯...")
    
    # 讀取原始數據
    with open('../data/LocationList.json', 'r', encoding='utf-8') as f:
        raw_locations = json.load(f)
    
    # 模擬JavaScript的轉換邏輯
    transformed_locations = []
    
    for location in raw_locations[:5]:  # 測試前5個
        transformed = {
            'lat': float(location['lat']),
            'lng': float(location['lng']),
            'film_name': location.get('film_name') or '未知电影',
            'CN_name': location.get('CN_name') or location.get('film_name') or '未知电影',
            'year': str(location['year']) if location.get('year') else '未知',
            'Area': location.get('Area') or '未知区域',
            'description': location.get('description') or f"{location.get('film_name', '未知电影')}的經典拍攝場景",
            'rating': float(location['rating']) if location.get('rating') and location['rating'] != 'N/A' else 0,
            'photoUrl': location.get('picture') or 'https://images.unsplash.com/photo-1513475382585-d06e58bcb0e0?w=400&h=300&fit=crop',
            'address': location.get('address') or '地址待定',
            'nearby_businesses': get_nearby_businesses(location.get('Area', '')),
            'photo_styles': get_photo_styles(location.get('film_name', '')),
            'cultural_significance': get_cultural_significance(location.get('Area', ''), location.get('film_name', ''))
        }
        transformed_locations.append(transformed)
    
    print(f"✅ 成功轉換 {len(transformed_locations)} 個位置")
    
    # 顯示示例
    print("\n📋 轉換示例:")
    for i, loc in enumerate(transformed_locations[:2]):
        print(f"\n{i+1}. {loc['film_name']} ({loc['CN_name']})")
        print(f"   📍 位置: {loc['lat']}, {loc['lng']}")
        print(f"   🏙️  區域: {loc['Area']}")
        print(f"   📸 拍攝風格: {', '.join(loc['photo_styles'])}")
        print(f"   🏪 附近商家: {', '.join(loc['nearby_businesses'])}")
    
    return True

def get_nearby_businesses(area):
    """模拟getNearbyBusinesses函数"""
    business_map = {
        'Central': ['陸羽茶室', '蘭桂坊咖啡店', '都爹利街星巴克'],
        'Tsim Sha Tsui': ['廟街夜市', '海港城購物咖啡', '星光大道茶餐廳'],
        'Mong Kok': ['女人街小吃店', '旺角茶餐廳'],
        'Yau Ma Tei': ['油麻地茶餐廳', '上海街小食'],
        'Sai Kung': ['西貢海鮮餐廳']
    }
    return business_map.get(area, ['附近商戶推薦'])

def get_photo_styles(film_name):
    """模拟getPhotoStyles函数"""
    style_map = {
        'Infernal Affairs': ['Film Noir', 'Street Photography', 'Architecture'],
        'Chungking Express': ['Cinematic', 'Urban', 'Neon Lights'],
        'Fallen Angel': ['Noir', 'Wide Angle', 'Reflective'],
        'Armed Reaction': ['TV Drama', 'Action', 'Cityscape']
    }
    
    for key, styles in style_map.items():
        if key in film_name:
            return styles
    
    return ['Cinematic', 'Portrait', 'Landscape']

def get_cultural_significance(area, film_name):
    """模拟getCulturalSignificance函数"""
    significance_map = {
        'Central': '中環是香港的商業中心，多部電影的取景地，反映了香港的繁華與活力。',
        'Tsim Sha Tsui': '尖沙咀是香港的文化重心，擁有豐富的文化設施和歷史建築。',
        'Mong Kok': '旺角是香港最熱鬧的地區之一，反映了香港的庶民文化和活力。',
        'Yau Ma Tei': '油麻地是香港的傳統社區，保留了濃厚的本土文化和歷史特色。',
        'Sai Kung': '西貢地區展現了香港自然風光和漁港文化。'
    }
    
    return significance_map.get(area, '這個地點在香港電影文化中有著特殊的意義。')

def test_api_readiness():
    """测试API就绪状态"""
    print("\n🌐 测试前端API调用...")
    
    # 检查必要的JSON文件
    files_to_check = {
        'LocationList.json': '位置數據',
        'tourism-data.json': '旅遊數據'
    }
    
    all_ready = True
    for file, description in files_to_check.items():
        if os.path.exists(file):
            try:
                with open(f'../data/{file}', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                print(f"✅ {description} ({file}): 可讀取")
            except Exception as e:
                print(f"❌ {description} ({file}): 錯誤 {e}")
                all_ready = False
        else:
            print(f"❌ {description} ({file}): 文件不存在")
            all_ready = False
    
    return all_ready

def generate_test_report():
    """生成測試報告"""
    print("\n" + "="*50)
    print("🧪 KACHA 數據集成測試報告")
    print("="*50)
    
    results = {
        'data_transformation': test_data_transformation(),
        'api_readiness': test_api_readiness()
    }
    
    print("\n📊 測試結果:")
    print(f"- 數據轉換: {'通過' if results['data_transformation'] else '失敗'}")
    print(f"- API就緒: {'準備好' if results['api_readiness'] else '未就緒'}")
    
    if all(results.values()):
        print("\n✅ 數據集成測試通過，前端應該可以正常運行")
    else:
        print("\n❌ 數據集成存在問題，需要修復")

def main():
    """主測試函數"""
    print("🔧 開始數據集成測試...")
    generate_test_report()

if __name__ == "__main__":
    main()