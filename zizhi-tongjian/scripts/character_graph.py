#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人物关系图谱 - 使用 NetworkX 构建和可视化历史人物关系网络

功能：
1. 人物关系数据库 (师徒、君臣、敌对、盟友)
2. 图谱可视化 (NetworkX + Matplotlib)
3. 关系查询接口
4. 影响力分析 (中心度计算)
"""

import json
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from datetime import datetime
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # 非交互式后端


class CharacterGraph:
    """人物关系图谱构建器"""
    
    def __init__(self, case_db_path: str = None):
        # 加载案例库
        if case_db_path is None:
            case_db_path = Path(__file__).parent.parent / "data" / "cases.json"
        
        self.case_db_path = case_db_path
        self.case_db = self._load_case_db()
        
        # 构建关系图谱
        self.graph = nx.Graph()
        self._build_graph()
    
    def _load_case_db(self) -> Dict:
        """加载案例库"""
        if Path(self.case_db_path).exists():
            with open(self.case_db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        print("⚠️ 案例库不存在")
        return {}
    
    def _build_graph(self):
        """从案例库构建人物关系图谱"""
        
        # 定义关系类型映射
        relationship_types = {
            '联盟': 'ally',
            '合作': 'ally',
            '结盟': 'ally',
            '对抗': 'enemy',
            '战争': 'enemy',
            '敌对': 'enemy',
            '君臣': 'master_servant',
            '师徒': 'mentor_student',
            '父子': 'family',
            '兄弟': 'family',
        }
        
        # 遍历所有案例，提取人物关系
        for case_name, case_data in self.case_db.items():
            protagonists = case_data.get('protagonists', [])
            wisdom = case_data.get('key_wisdom', '')
            
            if len(protagonists) < 2:
                continue
            
            # 添加人物节点 (如果不存在)
            for person in protagonists:
                if not self.graph.has_node(person):
                    self.graph.add_node(person, 
                                       type='character',
                                       cases=[],
                                       period=case_data.get('year', ''))
                
                # 记录该人物参与的案例
                self.graph.nodes[person]['cases'].append(case_name)
            
            # 添加人物之间的关系边
            for i in range(len(protagonists)):
                for j in range(i + 1, len(protagonists)):
                    person1 = protagonists[i]
                    person2 = protagonists[j]
                    
                    # 判断关系类型
                    rel_type = self._determine_relationship(wisdom, person1, person2)
                    
                    if rel_type:
                        edge_key = tuple(sorted([person1, person2]))
                        
                        if not self.graph.has_edge(*edge_key):
                            self.graph.add_edge(person1, person2, 
                                              type=rel_type,
                                              cases=[case_name])
    
    def _determine_relationship(self, wisdom: str, person1: str, person2: str) -> Optional[str]:
        """根据智慧文本判断人物关系类型"""
        
        if not wisdom:
            return None
        
        wisdom_lower = wisdom.lower()
        
        # 检查盟友关系关键词
        ally_keywords = ['联盟', '合作', '结盟', '联', '同心', '众士慕仰']
        for kw in ally_keywords:
            if kw in wisdom_lower:
                return 'ally'
        
        # 检查敌对关系关键词
        enemy_keywords = ['对抗', '战争', '敌对', '战', '败', '杀']
        for kw in enemy_keywords:
            if kw in wisdom_lower:
                return 'enemy'
        
        # 检查君臣/师徒关系 (基于历史常识)
        master_keywords = ['帝', '王', '陛下', '上', '主']
        servant_keywords = ['臣', '将', '相', '师', '徒']
        
        if any(kw in person1 for kw in master_keywords) and \
           any(kw in person2 for kw in servant_keywords):
            return 'master_servant'
        
        # 默认返回 None (无明确关系)
        return None
    
    def get_relationships(self, character_name: str) -> Dict[str, List[str]]:
        """获取指定人物的所有关系
        
        Args:
            character_name: 人物名称
            
        Returns:
            Dict: 关系分类字典 {relationship_type: [character_names]}
        """
        if not self.graph.has_node(character_name):
            return {'error': f'未找到人物"{character_name}"'}
        
        relationships = {
            'ally': [],      # 盟友
            'enemy': [],     # 敌人
            'master_servant': [],  # 君臣/师徒
            'family': []     # 亲属
        }
        
        for neighbor in self.graph.neighbors(character_name):
            edge_data = self.graph[character_name][neighbor]
            rel_type = edge_data.get('type', 'unknown')
            
            if rel_type in relationships:
                relationships[rel_type].append(neighbor)
        
        return relationships
    
    def get_character_info(self, character_name: str) -> Dict:
        """获取人物详细信息
        
        Args:
            character_name: 人物名称
            
        Returns:
            Dict: 人物信息字典
        """
        if not self.graph.has_node(character_name):
            return {'error': f'未找到人物"{character_name}"'}
        
        node_data = self.graph.nodes[character_name]
        
        # 获取关系统计
        relationships = self.get_relationships(character_name)
        
        # 计算中心度 (影响力指标)
        degree_centrality = nx.degree_centrality(self.graph).get(character_name, 0)
        
        return {
            'name': character_name,
            'period': node_data.get('period', ''),
            'cases_count': len(node_data.get('cases', [])),
            'relationships': relationships,
            'influence_score': degree_centrality,
            'ally_count': len(relationships.get('ally', [])),
            'enemy_count': len(relationships.get('enemy', []))
        }
    
    def visualize_graph(self, output_path: str = None, 
                       highlight_characters: List[str] = None):
        """可视化人物关系图谱
        
        Args:
            output_path: 输出图片路径，如果为 None 则不保存
            highlight_characters: 高亮显示的人物列表
        """
        
        # 创建图形
        plt.figure(figsize=(16, 12))
        
        # 计算节点布局 (力导向布局)
        pos = nx.spring_layout(self.graph, k=2, iterations=50)
        
        # 定义颜色映射
        node_colors = []
        node_sizes = []
        
        for node in self.graph.nodes():
            if highlight_characters and node in highlight_characters:
                node_colors.append('#FF6B6B')  # 高亮红色
                node_sizes.append(1000)
            else:
                node_colors.append('#4ECDC4')   # 默认青色
                node_sizes.append(500)
        
        # 绘制节点
        nx.draw_networkx_nodes(self.graph, pos, 
                              node_color=node_colors,
                              node_size=node_sizes,
                              alpha=0.8)
        
        # 绘制边 (根据关系类型使用不同颜色)
        edges = self.graph.edges()
        edge_colors = []
        
        for edge in edges:
            rel_type = self.graph[edge[0]][edge[1]].get('type', 'unknown')
            
            if rel_type == 'ally':
                edge_colors.append('#4CAF50')  # 盟友 - 绿色
            elif rel_type == 'enemy':
                edge_colors.append('#F44336')  # 敌人 - 红色
            else:
                edge_colors.append('#9E9E9E')  # 其他 - 灰色
        
        nx.draw_networkx_edges(self.graph, pos, 
                              edge_color=edge_colors,
                              width=2,
                              alpha=0.6)
        
        # 绘制标签
        labels = {node: node for node in self.graph.nodes()}
        nx.draw_networkx_labels(self.graph, pos, 
                               labels=labels,
                               font_size=10,
                               font_weight='bold')
        
        # 添加图例
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#FF6B6B', label='高亮人物'),
            Patch(facecolor='#4ECDC4', label='普通人物'),
            Patch(facecolor='#4CAF50', label='盟友关系'),
            Patch(facecolor='#F44336', label='敌对关系'),
            Patch(facecolor='#9E9E9E', label='其他关系')
        ]
        
        plt.legend(handles=legend_elements, loc='upper right')
        
        # 设置标题
        plt.title('历史人物关系图谱\n(节点大小 = 影响力，颜色 = 关系类型)', 
                 fontsize=14, fontweight='bold')
        
        # 隐藏坐标轴
        plt.axis('off')
        
        # 保存或显示
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            print(f"✅ 图谱已保存到：{output_path}")
        else:
            plt.show()
        
        plt.close()
    
    def get_influential_characters(self, top_k: int = 10) -> List[Dict]:
        """获取影响力最高的前 K 个人物
        
        Args:
            top_k: 返回数量
            
        Returns:
            List[Dict]: 人物影响力排行榜
        """
        
        # 计算所有节点的中心度
        centrality = nx.degree_centrality(self.graph)
        
        # 排序并取前 K 个
        sorted_chars = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:top_k]
        
        results = []
        for name, score in sorted_chars:
            info = self.get_character_info(name)
            
            if 'error' not in info:
                results.append({
                    'name': name,
                    'influence_score': round(score * 100, 2),
                    **{k: v for k, v in info.items() if k != 'influence_score'}
                })
        
        return results
    
    def find_shortest_path(self, start: str, end: str) -> Optional[List[str]]:
        """查找两个人物之间的最短关系路径
        
        Args:
            start: 起始人物
            end: 目标人物
            
        Returns:
            List[str]: 路径列表，如果不存在则返回 None
        """
        
        if not self.graph.has_node(start) or not self.graph.has_node(end):
            return None
        
        try:
            path = nx.shortest_path(self.graph, start, end)
            return path
        except nx.NetworkXNoPath:
            return None


# 测试
if __name__ == "__main__":
    graph = CharacterGraph()
    
    print("=== 测试：人物关系图谱 ===\n")
    
    # 1. 获取刘邦的关系
    print("--- 刘邦的人物关系 ---")
    relationships = graph.get_relationships('刘邦')
    
    if 'error' not in relationships:
        print(f"盟友：{relationships['ally'][:3]}...")
        print(f"敌人：{relationships['enemy'][:3]}...")
    
    # 2. 获取人物信息
    print("\n--- 刘邦详细信息 ---")
    info = graph.get_character_info('刘邦')
    
    if 'error' not in info:
        print(f"姓名：{info['name']}")
        print(f"参与案例数：{info['cases_count']}")
        print(f"盟友数量：{info['ally_count']}")
        print(f"敌人数量：{info['enemy_count']}")
    
    # 3. 影响力排行榜
    print("\n--- 影响力前 5 名 ---")
    top_chars = graph.get_influential_characters(5)
    
    for i, char in enumerate(top_chars[:5], 1):
        print(f"{i}. {char['name']} (影响力：{char['influence_score']:.2f})")
    
    # 4. 查找最短路径
    print("\n--- 刘邦 → 项羽 的关系路径 ---")
    path = graph.find_shortest_path('刘邦', '项羽')
    
    if path:
        print(f"路径：{' → '.join(path)}")
    else:
        print("未找到直接关系")
