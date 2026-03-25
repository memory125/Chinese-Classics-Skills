#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识图谱构建 - 实体关系网络

功能：
1. 实体提取 (人物、事件、地点、时间)
2. 关系抽取 (师徒、君臣、敌对等)
3. 图谱存储 (JSON/GraphDB)
4. 查询接口 (路径查找、子图提取)
"""

import json
from typing import Dict, List, Optional, Set, Tuple
from pathlib import Path
from datetime import datetime


class KnowledgeGraph:
    """知识图谱构建器"""
    
    def __init__(self, case_db_path: str = None):
        # 加载案例库
        if case_db_path is None:
            case_db_path = Path(__file__).parent.parent / "data" / "cases.json"
        
        self.case_db_path = case_db_path
        self.case_db = self._load_case_db()
        
        # 构建知识图谱
        self.entities = {}  # entity_id -> {type, name, properties}
        self.relations = []  # [(entity1, relation_type, entity2)]
        
        self._build_knowledge_graph()
    
    def _load_case_db(self) -> Dict:
        """加载案例库"""
        if Path(self.case_db_path).exists():
            with open(self.case_db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        print("⚠️ 案例库不存在")
        return {}
    
    def _build_knowledge_graph(self):
        """从案例库构建知识图谱"""
        
        # 定义实体类型
        entity_types = {
            'person': [],      # 人物
            'event': [],       # 事件
            'location': [],    # 地点
            'time_period': []  # 时期
        }
        
        # 遍历所有案例，提取实体和关系
        for case_name, case_data in self.case_db.items():
            # 1. 添加人物实体
            protagonists = case_data.get('protagonists', [])
            for person in protagonists:
                entity_id = f"person:{person}"
                
                if entity_id not in self.entities:
                    self.entities[entity_id] = {
                        'type': 'person',
                        'name': person,
                        'properties': {
                            'cases': [],
                            'period': case_data.get('year', '')
                        }
                    }
                
                # 记录该人物参与的案例
                self.entities[entity_id]['properties']['cases'].append(case_name)
            
            # 2. 添加事件实体
            event_id = f"event:{case_name}"
            self.entities[event_id] = {
                'type': 'event',
                'name': case_data.get('title', ''),
                'properties': {
                    'year': case_data.get('year', ''),
                    'dynasty': case_data.get('dynasty', ''),
                    'volume': case_data.get('volume', ''),
                    'wisdom': case_data.get('key_wisdom', '')[:100] if case_data.get('key_wisdom') else '',
                    'protagonists': protagonists,
                    'outcome': self._determine_outcome(case_data.get('key_wisdom', ''))
                }
            }
            
            # 3. 添加人物 - 事件关系
            for person in protagonists:
                person_id = f"person:{person}"
                event_id = f"event:{case_name}"
                
                self.relations.append((
                    person_id,
                    'participated_in',
                    event_id
                ))
            
            # 4. 添加人物之间的关系 (基于案例中的共同出现)
            if len(protagonists) >= 2:
                for i in range(len(protagonists)):
                    for j in range(i + 1, len(protagonists)):
                        person1 = protagonists[i]
                        person2 = protagonists[j]
                        
                        # 判断关系类型
                        rel_type = self._determine_relationship(case_data.get('key_wisdom', ''), 
                                                               person1, person2)
                        
                        if rel_type:
                            entity1_id = f"person:{person1}"
                            entity2_id = f"person:{person2}"
                            
                            # 避免重复关系
                            relation_exists = any(
                                (r[0] == entity1_id and r[2] == entity2_id) or
                                (r[0] == entity2_id and r[2] == entity1_id)
                                for r in self.relations
                            )
                            
                            if not relation_exists:
                                self.relations.append((entity1_id, rel_type, entity2_id))
    
    def _determine_outcome(self, wisdom: str) -> str:
        """判断事件结果"""
        
        if not wisdom:
            return 'neutral'
        
        success_keywords = ['成功', '胜利', '成就', '崛起', '建立']
        failure_keywords = ['失败', '败亡', '灭亡', '崩溃', '覆灭']
        
        wisdom_lower = wisdom.lower()
        
        for kw in success_keywords:
            if kw in wisdom_lower:
                return 'success'
        
        for kw in failure_keywords:
            if kw in wisdom_lower:
                return 'failure'
        
        return 'neutral'
    
    def _determine_relationship(self, wisdom: str, person1: str, person2: str) -> Optional[str]:
        """判断人物关系类型"""
        
        if not wisdom:
            return None
        
        wisdom_lower = wisdom.lower()
        
        # 盟友关系
        ally_keywords = ['联盟', '合作', '结盟', '联', '同心']
        for kw in ally_keywords:
            if kw in wisdom_lower:
                return 'ally'
        
        # 敌对关系
        enemy_keywords = ['对抗', '战争', '敌对', '战', '败']
        for kw in enemy_keywords:
            if kw in wisdom_lower:
                return 'enemy'
        
        # 君臣/师徒关系 (基于历史常识)
        master_keywords = ['帝', '王', '陛下', '上', '主']
        servant_keywords = ['臣', '将', '相', '师', '徒']
        
        if any(kw in person1 for kw in master_keywords) and \
           any(kw in person2 for kw in servant_keywords):
            return 'master_servant'
        
        return None
    
    def get_entity(self, entity_id: str) -> Optional[Dict]:
        """获取实体信息
        
        Args:
            entity_id: 实体 ID (格式：type:name)
            
        Returns:
            Dict: 实体信息，如果不存在则返回 None
        """
        
        return self.entities.get(entity_id)
    
    def get_entity_by_name(self, name: str, entity_type: str = None) -> List[Dict]:
        """根据名称查找实体
        
        Args:
            name: 实体名称
            entity_type: 实体类型 (可选，过滤用)
            
        Returns:
            List[Dict]: 匹配的实体列表
        """
        
        results = []
        
        for entity_id, entity_data in self.entities.items():
            if entity_data['name'].lower() == name.lower():
                if entity_type is None or entity_data['type'] == entity_type:
                    results.append(entity_data)
        
        return results
    
    def get_relations_for_entity(self, entity_id: str) -> List[Tuple[str, str]]:
        """获取实体的所有关系
        
        Args:
            entity_id: 实体 ID
            
        Returns:
            List[Tuple]: [(related_entity_id, relation_type), ...]
        """
        
        relations = []
        
        for rel in self.relations:
            if rel[0] == entity_id:
                relations.append((rel[2], rel[1]))  # (target_entity, relation_type)
            elif rel[2] == entity_id:
                relations.append((rel[0], rel[1]))
        
        return relations
    
    def find_path(self, start_entity: str, end_entity: str, max_depth: int = 3) -> Optional[List[str]]:
        """查找两个实体之间的最短路径
        
        Args:
            start_entity: 起始实体 ID
            end_entity: 目标实体 ID
            max_depth: 最大搜索深度
            
        Returns:
            List[str]: 路径列表，如果不存在则返回 None
        """
        
        from collections import deque
        
        if start_entity not in self.entities or end_entity not in self.entities:
            return None
        
        # BFS 搜索
        queue = deque([(start_entity, [start_entity])])
        visited = {start_entity}
        
        while queue:
            current, path = queue.popleft()
            
            if len(path) > max_depth + 1:
                continue
            
            if current == end_entity:
                return path
            
            # 获取当前实体的所有邻居
            neighbors = self._get_neighbors(current)
            
            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        return None
    
    def _get_neighbors(self, entity_id: str) -> List[str]:
        """获取实体的所有邻居实体"""
        
        neighbors = set()
        
        for rel in self.relations:
            if rel[0] == entity_id:
                neighbors.add(rel[2])
            elif rel[2] == entity_id:
                neighbors.add(rel[0])
        
        return list(neighbors)
    
    def get_subgraph(self, center_entity: str, radius: int = 2) -> Dict:
        """获取以某个实体为中心的子图
        
        Args:
            center_entity: 中心实体 ID
            radius: 搜索半径
            
        Returns:
            Dict: 子图数据 {entities, relations}
        """
        
        if center_entity not in self.entities:
            return {'error': f'未找到实体"{center_entity}"'}
        
        # BFS 获取范围内的所有实体和关系
        entities_in_subgraph = set()
        relations_in_subgraph = []
        
        queue = [(center_entity, 0)]
        visited = {center_entity}
        
        while queue:
            current, depth = queue.pop(0)
            
            if depth <= radius:
                entities_in_subgraph.add(current)
                
                # 获取邻居
                neighbors = self._get_neighbors(current)
                
                for neighbor in neighbors:
                    if neighbor not in visited and depth < radius:
                        visited.add(neighbor)
                        queue.append((neighbor, depth + 1))
            
            # 添加涉及该实体的关系
            for rel in self.relations:
                if current in [rel[0], rel[2]]:
                    if rel[0] in entities_in_subgraph and rel[2] in entities_in_subgraph:
                        relations_in_subgraph.append(rel)
        
        # 构建子图数据
        subgraph = {
            'center_entity': center_entity,
            'radius': radius,
            'entities': [self.entities[eid] for eid in entities_in_subgraph if eid in self.entities],
            'relations': relations_in_subgraph
        }
        
        return subgraph
    
    def export_to_json(self, output_path: str = None):
        """导出知识图谱为 JSON 格式
        
        Args:
            output_path: 输出文件路径
        """
        
        if output_path is None:
            output_path = Path(__file__).parent.parent / "data" / "knowledge_graph.json"
        
        graph_data = {
            'entities': self.entities,
            'relations': [
                {'source': r[0], 'target': r[2], 'type': r[1]}
                for r in self.relations
            ],
            'statistics': {
                'total_entities': len(self.entities),
                'total_relations': len(self.relations),
                'entity_types': {}
            }
        }
        
        # 统计实体类型分布
        for entity_id, entity_data in self.entities.items():
            entity_type = entity_data['type']
            graph_data['statistics']['entity_types'][entity_type] = \
                graph_data['statistics']['entity_types'].get(entity_type, 0) + 1
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(graph_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 知识图谱已导出到：{output_path}")


# 测试
if __name__ == "__main__":
    kg = KnowledgeGraph()
    
    print("=== 测试：知识图谱 ===\n")
    
    # 1. 统计信息
    print("--- 知识图谱统计 ---")
    print(f"总实体数：{len(kg.entities)}")
    print(f"总关系数：{len(kg.relations)}")
    
    # 2. 查找刘邦
    print("\n--- 查找'刘邦' ---")
    liu_entities = kg.get_entity_by_name('刘邦')
    
    if liu_entities:
        for entity in liu_entities:
            print(f"实体：{entity['name']} (类型：{entity['type']})")
            
            # 获取关系
            relations = kg.get_relations_for_entity(entity['id'])
            print(f"关系数：{len(relations)}")
    
    # 3. 查找路径
    print("\n--- 刘邦 → 项羽 的关系路径 ---")
    path = kg.find_path('person:刘邦', 'person:项羽')
    
    if path:
        print(f"路径：{' → '.join(path)}")
    else:
        print("未找到直接关系")
    
    # 4. 获取子图
    print("\n--- 刘邦为中心的 2 级子图 ---")
    subgraph = kg.get_subgraph('person:刘邦', radius=2)
    
    if 'error' not in subgraph:
        print(f"实体数：{len(subgraph['entities'])}")
        print(f"关系数：{len(subgraph['relations'])}")
