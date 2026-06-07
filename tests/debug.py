#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KACHA 電影文旅地圖 - 調試工具
用於驗證數據完整性和項目狀態
"""

import json
import csv
import os
import sys
from pathlib import Path

def check_file_structure():
    """檢查項目文件結構"""
    print("🔍 檢查項目文件結構...")
    
    required_files = [
        'index.html',
        'style.css', 
        'LocationList.json',
        'tourism-data.json',
        'particles.js'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
        else:
            print(f"✅ {file} - 存在")
    
    if missing_files:
        print(f"❌ 缺失文件: {missing_files}")
        return False
    
    print("✅ 所有必要文件都存在")
    return True

def validate_location_data():
    """驗證位置數據完整性"""
    print("\n📍 驗證位置數據...")
    
    try:
        with open('LocationList.json', 'r', encoding='utf-8') as f:
            locations = json.load(f)
        
        print(f"✅ 成功加載 {len(locations)} 個位置")
        
        # 檢查基本字段
        required_fields = ['film_name', 'lat', 'lng', 'Area']
        invalid_locations = []
        
        for i, loc in enumerate(locations[:10]):  # 檢查前10個
            for field in required_fields:
                if field not in loc or not loc[field]:
                    invalid_locations.append((i, field, loc.get('film_name', 'Unknown')))
        
        if invalid_locations:
            print("❌ 發現無效數據:")
            for idx, field, name in invalid_locations:
                print(f"  - 位置 {idx} ({name}): 缺少 {field}")
        else:
            print("✅ 數據格式正確")
            
        return len(locations)
    except Exception as e:
        print(f"❌ 位置數據錯誤: {e}")
        return 0

def validate_tourism_data():
    """驗證旅遊數據完整性"""
    print("\n🎭 驗證旅遊數據...")
    
    try:
        with open('../data/tourism-data.json', 'r', encoding='utf-8') as f:
            tourism = json.load(f)
        
        sections = ['businesses', 'photoGuides', 'tourismPackages', 'culturalInfo']
        for section in sections:
            if section in tourism:
                print(f"✅ {section}: {len(tourism[section]) if isinstance(tourism[section], (dict, list)) else 'N/A'}")
            else:
                print(f"❌ 缺失 {section}")
        
        return True
    except Exception as e:
        print(f"❌ 旅遊數據錯誤: {e}")
        return False

def check_data_relationships():
    """檢查數據關聯性"""
    print("\n🔗 檢查數據關聯性...")
    
    try:
        # 檢查地區匹配
        with open('LocationList.json', 'r', encoding='utf-8') as f:
            locations = json.load(f)
        
        with open('../data/tourism-data.json', 'r', encoding='utf-8') as f:
            tourism = json.load(f)
        
        # 獲取所有地區
        location_areas = set(loc.get('Area', 'Unknown') for loc in locations)
        tourism_areas = set(tourism['businesses'].keys())
        
        missing_in_tourism = location_areas - tourism_areas
        if missing_in_tourism:
            print(f"❌ 位置數據中的地區但在旅遊數據中缺失: {missing_in_tourism}")
        else:
            print("✅ 地區數據匹配")
            
        return len(missing_in_tourism) == 0
    except Exception as e:
        print(f"❌ 數據關聯檢查錯誤: {e}")
        return False

def test_csv_to_json_conversion():
    """測試CSV到JSON的轉換"""
    print("\n📄 測試CSV數據轉換...")
    
    csv_files = ['test.csv', 'LocationList_20240610.csv', 'imdb_ratings.csv']
    
    for csv_file in csv_files:
        if os.path.exists(csv_file):
            try:
                with open(csv_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    rows = list(reader)
                print(f"✅ {csv_file}: {len(rows)} 行數據")
            except Exception as e:
                print(f"❌ {csv_file}: 讀取錯誤 {e}")
        else:
            print(f"⚠️  {csv_file}: 文件不存在")

def generate_debug_report():
    """生成調試報告"""
    print("\n" + "="*50)
    print("📊 KACHA 項目調試報告")
    print("="*50)
    
    results = {
        'file_structure': check_file_structure(),
        'location_count': validate_location_data(),
        'tourism_data': validate_tourism_data(),
        'data_relationships': check_data_relationships()
    }
    
    test_csv_to_json_conversion()
    
    print("\n📋 總結:")
    print(f"- 文件結構: {'良好' if results['file_structure'] else '有問題'}")
    print(f"- 位置數據: {results['location_count']} 個位置")
    print(f"- 旅遊數據: {'正常' if results['tourism_data'] else '異常'}")
    print(f"- 數據關聯: {'匹配' if results['data_relationships'] else '不匹配'}")
    
    return results

def main():
    """主調試函數"""
    print("🚀 開始KACHA項目調試...")
    
    # 檢查是否在正確目錄
    if not os.path.exists('index.html'):
        print("❌ 請在KACHA項目根目錄運行此腳本")
        sys.exit(1)
    
    results = generate_debug_report()
    
    if all([results['file_structure'], results['tourism_data'], results['data_relationships']]):
        print("\n✅ 項目狀態良好，可以正常運行")
        return 0
    else:
        print("\n⚠️  項目存在問題，需要修復")
        return 1

if __name__ == "__main__":
    exit(main())