#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交互式知识图谱可视化 - 使用 pyvis

功能：
1. 生成交互式 HTML 图谱 (可拖拽、缩放)
2. 节点点击显示详细信息
3. 路径高亮显示
4. 支持导出和分享
"""

import json
from typing import Dict, List, Optional, Set, Tuple
from pathlib import Path


class InteractiveGraphVisualizer:
    """交互式图谱可视化器"""
    
    def __init__(self, knowledge_graph):
        self.kg = knowledge_graph
        
        # 尝试导入 pyvis
        try:
            from pyvis.network import Network
            self.has_pyvis = True
            print("✅ pyvis 已安装，支持交互式图谱")
        except ImportError:
            self.has_pyvis = False
            print("⚠️ 未安装 pyvis，请运行：pip3 install pyvis")
    
    def visualize_interactive(self, 
                             output_path: str = None,
                             highlight_entities: List[str] = None,
                             show_relationships: bool = True) -> str:
        """生成交互式 HTML 图谱
        
        Args:
            output_path: 输出文件路径，如果为 None 则自动生成
            highlight_entities: 高亮显示的实体列表
            show_relationships: 是否显示关系连线
            
        Returns:
            str: 生成的 HTML 文件路径
        """
        
        if not self.has_pyvis:
            return "❌ pyvis 未安装，无法生成交互式图谱"
        
        from pyvis.network import Network
        
        # 自动生成输出路径
        if output_path is None:
            base_dir = Path(__file__).parent.parent / "data"
            output_path = str(base_dir / "knowledge_graph_interactive.html")
        
        # 创建网络图 (深色主题)
        net = Network(
            height='750px', 
            width='100%', 
            bgcolor='#1a1a2e', 
            font_color='white',
            directed=False,
            notebook=False
        )
        
        # 添加节点
        for entity_id, entity_data in self.kg.entities.items():
            node_type = entity_data.get('type', 'unknown')
            
            # 根据类型设置颜色
            color_map = {
                'person': '#4ECDC4',      # 人物 - 青色
                'event': '#FF6B6B',       # 事件 - 红色
                'location': '#95E1D3',    # 地点 - 绿色
                'time_period': '#F38181'  # 时期 - 橙色
            }
            
            node_color = color_map.get(node_type, '#9E9E9E')
            
            # 设置节点大小 (影响力大的更大)
            size = 50 if entity_data.get('influence', False) else 30
            
            # 添加节点
            net.add_node(
                entity_id,
                label=entity_data['name'],
                color=node_color,
                size=size,
                title=self._get_entity_tooltip(entity_data),
                shadow=True
            )
        
        # 添加关系连线
        if show_relationships:
            for rel in self.kg.relations:
                entity1_id = rel[0]
                entity2_id = rel[2]
                relation_type = rel[1]
                
                # 根据关系类型设置颜色
                color_map = {
                    'ally': '#4CAF50',        # 盟友 - 绿色
                    'enemy': '#F44336',       # 敌人 - 红色
                    'master_servant': '#FF9800',  # 君臣 - 橙色
                    'participated_in': '#2196F3',  # 参与 - 蓝色
                    'family': '#E91E63'       # 亲属 - 粉色
                }
                
                edge_color = color_map.get(relation_type, '#757575')
                
                net.add_edge(
                    entity1_id,
                    entity2_id,
                    value=2,
                    color=edge_color,
                    title=f"{relation_type}",
                    smooth=True
                )
        
        # 高亮指定实体
        if highlight_entities:
            for entity_id in highlight_entities:
                if net.has_node(entity_id):
                    net.update_node(
                        entity_id,
                        color='#FFD700',  # 金色高亮
                        size=60,
                        shadow=True
                    )
        
        # 添加图例说明
        legend_html = """
        <div style="position: absolute; top: 10px; left: 10px; 
                   background: rgba(255,255,255,0.9); padding: 10px; 
                   border-radius: 5px; font-size: 12px;">
            <h4 style="margin: 0 0 5px 0;">图例</h4>
            <div style="display: flex; align-items: center; margin-bottom: 3px;">
                <span style="width: 12px; height: 12px; background: #4ECDC4; 
                           display: inline-block; margin-right: 5px;"></span>
                人物
            </div>
            <div style="display: flex; align-items: center; margin-bottom: 3px;">
                <span style="width: 12px; height: 12px; background: #FF6B6B; 
                           display: inline-block; margin-right: 5px;"></span>
                事件
            </div>
            <div style="display: flex; align-items: center; margin-bottom: 3px;">
                <span style="width: 12px; height: 12px; background: #4CAF50; 
                           display: inline-block; margin-right: 5px;"></span>
                盟友关系
            </div>
            <div style="display: flex; align-items: center; margin-bottom: 3px;">
                <span style="width: 12px; height: 12px; background: #F44336; 
                           display: inline-block; margin-right: 5px;"></span>
                敌对关系
            </div>
        </div>
        """
        
        net.add_script_tag(legend_html)
        
        # 保存图谱
        net.save_graph(output_path)
        
        print(f"✅ 交互式图谱已生成：{output_path}")
        return output_path
    
    def _get_entity_tooltip(self, entity_data: Dict) -> str:
        """获取实体详细信息 (用于鼠标悬停显示)"""
        
        name = entity_data.get('name', '')
        entity_type = entity_data.get('type', '')
        
        # 提取额外信息
        properties = entity_data.get('properties', {})
        
        tooltip_parts = [f"<strong>{name}</strong> ({entity_type})"]
        
        if 'cases' in properties:
            cases_count = len(properties['cases'])
            tooltip_parts.append(f"参与案例：{cases_count}个")
        
        if 'period' in properties:
            tooltip_parts.append(f"时期：{properties['period']}")
        
        return '<br>'.join(tooltip_parts)
    
    def highlight_path(self, 
                      output_path: str = None,
                      start_entity: str = None,
                      end_entity: str = None) -> str:
        """高亮显示两个实体之间的路径
        
        Args:
            output_path: 输出文件路径
            start_entity: 起始实体 ID
            end_entity: 目标实体 ID
            
        Returns:
            str: 生成的 HTML 文件路径
        """
        
        if not self.has_pyvis:
            return "❌ pyvis 未安装"
        
        from pyvis.network import Network
        
        # 自动生成输出路径
        if output_path is None:
            base_dir = Path(__file__).parent.parent / "data"
            output_path = str(base_dir / "knowledge_graph_highlighted.html")
        
        # 创建网络图
        net = Network(
            height='750px', 
            width='100%', 
            bgcolor='#1a1a2e', 
            font_color='white',
            directed=False,
            notebook=False
        )
        
        # 查找路径
        if start_entity and end_entity:
            path = self.kg.find_path(start_entity, end_entity)
            
            if path:
                print(f"✅ 找到路径：{' → '.join(path)}")
                
                # 高亮路径上的节点和边
                for i in range(len(path) - 1):
                    entity1_id = path[i]
                    entity2_id = path[i + 1]
                    
                    # 高亮节点
                    if net.has_node(entity1_id):
                        net.update_node(
                            entity1_id,
                            color='#FFD700',  # 金色
                            size=50,
                            shadow=True
                        )
                    
                    if net.has_node(entity2_id):
                        net.update_node(
                            entity2_id,
                            color='#FFD700',
                            size=50,
                            shadow=True
                        )
                    
                    # 高亮边
                    net.add_edge(
                        entity1_id,
                        entity2_id,
                        value=3,
                        color='#FFD700',
                        width=4
                    )
            else:
                print(f"⚠️ 未找到 {start_entity} → {end_entity} 的路径")
        
        # 保存图谱
        net.save_graph(output_path)
        
        print(f"✅ 高亮路径图谱已生成：{output_path}")
        return output_path
    
    def export_statistics(self, output_path: str = None) -> Dict:
        """导出图谱统计信息
        
        Args:
            output_path: 输出文件路径
            
        Returns:
            Dict: 统计信息字典
        """
        
        # 计算统计信息
        stats = {
            'total_entities': len(self.kg.entities),
            'total_relations': len(self.kg.relations),
            'entity_types': {},
            'relation_types': {}
        }
        
        # 统计实体类型分布
        for entity_id, entity_data in self.kg.entities.items():
            entity_type = entity_data.get('type', 'unknown')
            stats['entity_types'][entity_type] = \
                stats['entity_types'].get(entity_type, 0) + 1
        
        # 统计关系类型分布
        for rel in self.kg.relations:
            relation_type = rel[1]
            stats['relation_types'][relation_type] = \
                stats['relation_types'].get(relation_type, 0) + 1
        
        # 导出到 JSON
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(stats, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 统计信息已导出：{output_path}")
        
        return stats


# 测试
if __name__ == "__main__":
    from scripts.knowledge_graph import KnowledgeGraph
    
    kg = KnowledgeGraph()
    
    print("=== 交互式图谱可视化测试 ===\n")
    
    # 1. 生成交互式图谱
    visualizer = InteractiveGraphVisualizer(kg)
    
    output_path = visualizer.visualize_interactive(
        highlight_entities=['person:刘邦', 'person:项羽']
    )
    
    print(f"\n生成的文件：{output_path}")
    print("\n💡 提示：在浏览器中打开此 HTML 文件即可查看交互式图谱")
    print("   - 可以拖拽节点调整位置")
    print("   - 可以缩放查看细节")
    print("   - 点击节点查看详细信息")
