#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
周易学习技能 - 核心功能测试套件
测试：卦象数据库、每日一卦、交互起卦等核心功能
"""

import sys
import os

# 添加 scripts 目录到路径
SCRIPT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts')
sys.path.insert(0, SCRIPT_DIR)

def test_zhouyi_database_import():
    """测试数据库模块导入"""
    try:
        from zhouyi_database import ZhouyiDatabase
        db = ZhouyiDatabase()
        print("✅ 数据库模块导入成功")
        print(f"   实例化 ZhouyiDatabase 成功")
        return True
    except ImportError as e:
        print(f"❌ 数据库模块导入失败：{e}")
        return False

def test_get_gua_by_name():
    """测试通过名称获取卦象"""
    from zhouyi_database import ZhouyiDatabase
    
    db = ZhouyiDatabase()
    
    # 测试乾卦（单字）
    qian = db.get_gua("乾")
    assert qian is not None, "乾卦数据为空"
    assert '乾' in qian.get('name', ''), "乾卦名称不匹配"
    assert '䷀' in qian.get('hexagram', ''), "乾卦符号不匹配"
    
    # 测试坤卦（单字）
    kun = db.get_gua("坤")
    assert kun is not None, "坤卦数据为空"
    assert '坤' in kun.get('name', ''), "坤卦名称不匹配"
    
    print("✅ 通过名称获取卦象测试通过")
    print(f"   测试卦象：乾、坤")
    return True

def test_gua_data_structure():
    """测试卦象数据结构完整性"""
    from zhouyi_database import ZhouyiDatabase
    
    db = ZhouyiDatabase()
    
    required_fields = ['name', 'hexagram', 'guaci', 'baihua']
    
    # 测试前几个卦象
    test_names = ["乾", "坤"]
    for name in test_names:
        data = db.get_gua(name)
        assert data is not None, f"{name} 数据为空"
        for field in required_fields:
            assert field in data, f"{name} 缺少字段：{field}"
    
    print("✅ 卦象数据结构测试通过")
    print(f"   检查 {len(required_fields)} 个必需字段")
    return True

def test_gua_count():
    """测试卦象数量（至少包含乾、坤）"""
    from zhouyi_database import ZhouyiDatabase
    
    db = ZhouyiDatabase()
    
    # 至少应该有乾和坤
    assert db.get_gua("乾") is not None, "缺少乾卦"
    assert db.get_gua("坤") is not None, "缺少坤卦"
    
    count = len(db.gua_data)
    print("✅ 卦象数量测试通过")
    print(f"   已加载 {count} 个卦象数据")
    return True

def test_database_methods():
    """测试数据库方法"""
    from zhouyi_database import ZhouyiDatabase
    
    db = ZhouyiDatabase()
    
    # 测试所有主要方法存在
    assert hasattr(db, 'get_gua'), "缺少 get_gua 方法"
    assert hasattr(db, 'search_by_theme'), "缺少 search_by_theme 方法"
    
    print("✅ 数据库方法测试通过")
    print("   get_gua, search_by_theme 等方法存在")
    return True

def main():
    """运行所有测试"""
    print("=" * 60)
    print("周易学习技能 - 核心功能测试")
    print("=" * 60)
    print()
    
    tests = [
        test_zhouyi_database_import,
        test_get_gua_by_name,
        test_gua_data_structure,
        test_gua_count,
        test_database_methods,
    ]
    
    passed = 0
    failed = 0
    
    for test_func in tests:
        try:
            result = test_func()
            if result:
                passed += 1
            else:
                failed += 1
        except AssertionError as e:
            print(f"❌ {test_func.__name__} 失败：{e}")
            failed += 1
        except Exception as e:
            print(f"❌ {test_func.__name__} 意外错误：{e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print()
    print("=" * 60)
    print(f"测试完成：✅ {passed} 通过，❌ {failed} 失败")
    print("=" * 60)
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
