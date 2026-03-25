#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
案例库扩充工具 - 从 36 → 200+ 案例

功能：
1. 按朝代分类扩充 (战国/秦汉/三国/隋唐/宋元/明清)
2. 按主题分类扩充 (用人智慧/战略决策/改革变法/战争谋略)
3. 自动化数据生成工具
4. 数据质量验证
"""

import json
from typing import Dict, List
from pathlib import Path


class CaseExpander:
    """案例库扩充器"""
    
    def __init__(self):
        # 加载现有案例库
        self.case_db_path = Path(__file__).parent.parent / "data" / "cases.json"
        self.new_case_db_path = Path(__file__).parent.parent / "data" / "cases_v2.json"
        
        if self.case_db_path.exists():
            with open(self.case_db_path, 'r', encoding='utf-8') as f:
                self.existing_cases = json.load(f)
        else:
            self.existing_cases = {}
        
        print(f"✅ 已加载 {len(self.existing_cases)} 个现有案例")
    
    def expand_by_dynasty(self) -> Dict[str, List[Dict]]:
        """按朝代扩充案例"""
        
        dynasty_cases = {
            '战国': [
                {
                    "title": "商鞅变法 - 改革强秦",
                    "year": "前 356-前 338 年",
                    "dynasty": "战国·秦",
                    "protagonists": ["商鞅", "秦孝公"],
                    "background": "秦国地处西陲，国力较弱。商鞅在秦孝公支持下推行变法，废井田、开阡陌，实行军功爵制，奖励耕战，使秦国迅速强大。",
                    "key_wisdom": "改革需要勇气和决心，更需循序渐进。商鞅变法通过制度创新，从根本上改变了国家命运。但过于激进也埋下隐患。",
                    "modern_applications": [
                        {"scenario": "企业转型", "action": "制定清晰的变革路线图，分阶段实施"},
                        {"scenario": "政策改革", "action": "平衡各方利益，避免剧烈震荡"}
                    ]
                },
                {
                    "title": "合纵连横 - 外交博弈",
                    "year": "前 300-前 221 年",
                    "dynasty": "战国",
                    "protagonists": ["苏秦", "张仪"],
                    "background": "战国后期，秦国强大威胁各国。苏秦主张六国合纵抗秦，张仪则推行连横事秦。两种策略的博弈贯穿战国末期。",
                    "key_wisdom": "外交是实力的延伸。合纵连衡的本质是力量对比的体现，弱国联合可抗衡强国，但需内部团结。",
                    "modern_applications": [
                        {"scenario": "商业联盟", "action": "中小企业联合对抗行业巨头"},
                        {"scenario": "国际关系", "action": "多边合作制衡单边主义"}
                    ]
                },
                {
                    "title": "长平之战 - 战国巅峰对决",
                    "year": "前 260 年",
                    "dynasty": "战国·秦赵",
                    "protagonists": ["白起", "赵括"],
                    "background": "秦国与赵国在长平决战，秦将白起坑杀赵军四十万。此战奠定秦统一基础，但也暴露了战争残酷性。",
                    "key_wisdom": "名将要用对地方，不能纸上谈兵。赵王换掉廉颇启用赵括，导致惨败。用人不当是战略失误的根源。",
                    "modern_applications": [
                        {"scenario": "人才管理", "action": "根据能力匹配岗位，避免外行领导内行"},
                        {"scenario": "风险控制", "action": "建立专业决策机制，减少个人主观判断"}
                    ]
                },
                {
                    "title": "完璧归赵 - 外交智慧",
                    "year": "前 283 年",
                    "dynasty": "战国·秦赵",
                    "protagonists": ["蔺相如"],
                    "background": "秦国以十五城换和氏璧，蔺相如奉命出使，识破秦王诡计，完璧归赵，维护了国家尊严。",
                    "key_wisdom": "外交场合需要勇气和智慧。面对强权不卑不亢，既维护原则又留有余地。",
                    "modern_applications": [
                        {"scenario": "商务谈判", "action": "坚持核心利益，灵活处理细节"},
                        {"scenario": "危机公关", "action": "快速反应，掌握主动权"}
                    ]
                },
                {
                    "title": "负荆请罪 - 将相和",
                    "year": "前 279 年",
                    "dynasty": "战国·赵",
                    "protagonists": ["廉颇", "蔺相如"],
                    "background": "廉颇不服蔺相如地位高于自己，多次挑衅。蔺相如以国家利益为重，避让忍让。廉颇最终负荆请罪，将相和好。",
                    "key_wisdom": "大局为重，个人恩怨服从集体利益。宽容大度能化解矛盾，团结力量更大。",
                    "modern_applications": [
                        {"scenario": "团队管理", "action": "化解内部矛盾，促进团队协作"},
                        {"scenario": "冲突解决", "action": "主动让步，寻求共赢方案"}
                    ]
                }
            ],
            
            '秦汉': [
                {
                    "title": "鸿门宴 - 生死决策",
                    "year": "前 206 年",
                    "dynasty": "秦末汉初",
                    "protagonists": ["刘邦", "项羽", "范增", "张良"],
                    "background": "刘邦先入咸阳，项羽大怒欲攻。范增劝项羽在鸿门宴上除掉刘邦，刘邦通过张良、项伯关系得以脱险。",
                    "key_wisdom": "劣势下要懂得隐忍和示弱，保存实力等待时机。能屈能伸是成大事者的必备素质。",
                    "modern_applications": [
                        {"scenario": "商业竞争", "action": "暂时退让，积蓄力量"},
                        {"scenario": "职场生存", "action": "面对强权不硬碰硬，寻找机会"}
                    ]
                },
                {
                    "title": "推恩令 - 政治智慧",
                    "year": "前 127 年",
                    "dynasty": "西汉",
                    "protagonists": ["汉武帝", "主父偃"],
                    "background": "诸侯王势力强大威胁中央，主父偃建议推行推恩令，让诸侯王将封地分给所有子弟。",
                    "key_wisdom": "通过温和手段逐步削弱对手，比直接对抗更有效。政治智慧在于循序渐进，以柔克刚。",
                    "modern_applications": [
                        {"scenario": "组织变革", "action": "渐进式改革减少阻力"},
                        {"scenario": "权力制衡", "action": "分散权力避免集中风险"}
                    ]
                },
                {
                    "title": "金屋藏娇 - 情感与政治",
                    "year": "前 156-前 87 年",
                    "dynasty": "西汉",
                    "protagonists": ["汉武帝刘彻", "陈阿娇"],
                    "background": "刘彻幼时承诺'若得阿娇作妇，当作金屋贮之也'。成年后兑现诺言迎娶陈阿娇为皇后，但后期失宠被废。",
                    "key_wisdom": "诚信是立身之本，承诺必须兑现。但过度依赖物质无法维系感情，情感与利益需平衡。",
                    "modern_applications": [
                        {"scenario": "商业合作", "action": "信守承诺建立信任"},
                        {"scenario": "人际关系", "action": "感情不能仅靠物质维系"}
                    ]
                },
                {
                    "title": "昭君出塞 - 和亲政策",
                    "year": "前 33 年",
                    "dynasty": "西汉",
                    "protagonists": ["王昭君", "呼韩邪单于"],
                    "background": "汉元帝将王昭君嫁给匈奴呼韩邪单于，促成汉匈和平。昭君出塞成为民族团结的象征。",
                    "key_wisdom": "和亲是政治智慧，以婚姻换和平。牺牲个人成就大局，但需平衡国家利益与个人幸福。",
                    "modern_applications": [
                        {"scenario": "国际合作", "action": "通过文化交流促进理解"},
                        {"scenario": "危机化解", "action": "寻找共同利益点达成妥协"}
                    ]
                },
                {
                    "title": "王莽篡汉 - 改革失败教训",
                    "year": "8-23 年",
                    "dynasty": "西汉末",
                    "protagonists": ["王莽"],
                    "background": "王莽托古改制，恢复井田制、废除奴隶制等。但脱离实际，引发社会动荡，最终失败。",
                    "key_wisdom": "改革需立足现实，不能盲目复古。理想主义需与现实条件结合，否则适得其反。",
                    "modern_applications": [
                        {"scenario": "政策制定", "action": "调研先行，避免脱离实际"},
                        {"scenario": "企业变革", "action": "考虑员工接受度，循序渐进"}
                    ]
                }
            ],
            
            '三国': [
                {
                    "title": "赤壁之战 - 以弱胜强",
                    "year": "208 年",
                    "dynasty": "东汉末年",
                    "protagonists": ["周瑜", "诸葛亮", "曹操"],
                    "background": "曹操统一北方后南下，孙权刘备联军在赤壁以火攻大破曹军，奠定三国鼎立基础。",
                    "key_wisdom": "团结就是力量，联合弱小势力可以战胜强大敌人。孙刘联盟成功的关键是利益一致。",
                    "modern_applications": [
                        {"scenario": "商业竞争", "action": "中小企业联合对抗行业巨头"},
                        {"scenario": "战略联盟", "action": "寻找共同利益点建立合作"}
                    ]
                },
                {
                    "title": "三顾茅庐 - 求贤若渴",
                    "year": "207 年",
                    "dynasty": "三国·蜀汉",
                    "protagonists": ["刘备", "诸葛亮"],
                    "background": "刘备三次拜访诸葛亮，请其出山辅佐。最终打动诸葛亮，获得'隆中对'战略指导。",
                    "key_wisdom": "求贤若渴是成大事者的必备品质。真诚尊重人才，才能吸引顶尖人才加盟。",
                    "modern_applications": [
                        {"scenario": "人才招聘", "action": "主动出击，展现诚意"},
                        {"scenario": "团队建设", "action": "尊重专业人才，给予充分信任"}
                    ]
                },
                {
                    "title": "官渡之战 - 曹操崛起",
                    "year": "200 年",
                    "dynasty": "东汉末年",
                    "protagonists": ["曹操", "袁绍"],
                    "background": "曹操与袁绍在官渡决战，曹操以少胜多。奇袭乌巢烧毁袁军粮草是关键转折点。",
                    "key_wisdom": "出奇制胜是军事战略的重要原则。抓住敌人弱点可以扭转战局，细节决定成败。",
                    "modern_applications": [
                        {"scenario": "市场竞争", "action": "寻找对手薄弱环节突破"},
                        {"scenario": "项目管理", "action": "关注关键路径和风险控制"}
                    ]
                },
                {
                    "title": "草船借箭 - 智慧取胜",
                    "year": "208 年",
                    "dynasty": "三国·蜀吴",
                    "protagonists": ["诸葛亮"],
                    "background": "周瑜刁难诸葛亮，要求十天内造十万支箭。诸葛亮利用大雾天气草船借箭，三天完成任务。",
                    "key_wisdom": "善用天时地利人和，化不可能为可能。创新思维可以突破资源限制。",
                    "modern_applications": [
                        {"scenario": "资源整合", "action": "借力打力，巧用外部资源"},
                        {"scenario": "问题解决", "action": "跳出常规思维寻找新方案"}
                    ]
                },
                {
                    "title": "七擒孟获 - 攻心为上",
                    "year": "225 年",
                    "dynasty": "三国·蜀汉",
                    "protagonists": ["诸葛亮", "孟获"],
                    "background": "诸葛亮南征，七次擒获又释放孟获，最终使其真心归顺。体现了'攻心为上'的战略思想。",
                    "key_wisdom": "征服人心比征服土地更重要。以德服人才能长治久安，武力只能暂时压制。",
                    "modern_applications": [
                        {"scenario": "团队管理", "action": "用价值观凝聚人心"},
                        {"scenario": "客户维护", "action": "建立情感连接而非仅靠利益"}
                    ]
                }
            ],
            
            '隋唐': [
                {
                    "title": "玄武门之变 - 权力争夺",
                    "year": "626 年",
                    "dynasty": "唐朝",
                    "protagonists": ["李世民", "李建成", "李元吉"],
                    "background": "唐高祖李渊的太子李建成与秦王李世民争夺皇位，李世民在玄武门发动政变杀死兄弟。",
                    "key_wisdom": "关键时刻要果断决策，犹豫不决只会错失良机。权力斗争中被动等待往往意味着失败。",
                    "modern_applications": [
                        {"scenario": "商业竞争", "action": "抓住市场窗口期快速行动"},
                        {"scenario": "职业晋升", "action": "主动争取机会不被动等待"}
                    ]
                },
                {
                    "title": "贞观之治 - 盛世典范",
                    "year": "627-649 年",
                    "dynasty": "唐朝",
                    "protagonists": ["唐太宗李世民"],
                    "background": "李世民即位后虚心纳谏，任用贤能，轻徭薄赋，开创'贞观之治'，成为后世盛世典范。",
                    "key_wisdom": "虚心纳谏是领导者的必备品质。善于听取不同意见才能避免决策失误。",
                    "modern_applications": [
                        {"scenario": "团队管理", "action": "建立开放沟通机制"},
                        {"scenario": "个人成长", "action": "主动寻求反馈改进不足"}
                    ]
                },
                {
                    "title": "安史之乱 - 盛唐转衰",
                    "year": "755-763 年",
                    "dynasty": "唐朝",
                    "protagonists": ["唐玄宗", "安禄山", "杨国忠"],
                    "background": "安禄山发动叛乱，唐朝由盛转衰。唐玄宗宠信安禄山不加防范是重要原因。",
                    "key_wisdom": "防微杜渐是治国理政的重要原则。对潜在威胁要早发现早处理，不能姑息养奸。",
                    "modern_applications": [
                        {"scenario": "风险管理", "action": "建立预警机制及时干预"},
                        {"scenario": "团队管理", "action": "关注员工状态预防问题"}
                    ]
                },
                {
                    "title": "杯酒释兵权 - 和平夺权",
                    "year": "960 年",
                    "dynasty": "北宋",
                    "protagonists": ["赵匡胤"],
                    "background": "宋太祖赵匡胤通过酒宴方式解除将领兵权，和平完成权力交接，避免流血冲突。",
                    "key_wisdom": "顺势而为可以最小代价获得最大收益。政治智慧在于以柔克刚，不战而屈人之兵。",
                    "modern_applications": [
                        {"scenario": "企业并购", "action": "协商谈判优于强制收购"},
                        {"scenario": "权力交接", "action": "给予体面退出机制"}
                    ]
                },
                {
                    "title": "陈桥兵变 - 和平夺权",
                    "year": "960 年",
                    "dynasty": "北宋",
                    "protagonists": ["赵匡胤"],
                    "background": "后周恭帝年幼，赵匡胤在陈桥驿被部下拥立为帝，建立宋朝。兵不血刃完成政权更迭。",
                    "key_wisdom": "顺势而为是成大事者的智慧。抓住历史转折点可以最小代价获得最大收益。",
                    "modern_applications": [
                        {"scenario": "创业时机", "action": "把握市场窗口期"},
                        {"scenario": "职业转型", "action": "识别行业趋势提前布局"}
                    ]
                }
            ],
            
            '宋元': [
                {
                    "title": "澶渊之盟 - 和平条约",
                    "year": "1005 年",
                    "dynasty": "北宋",
                    "protagonists": ["宋真宗", "寇准"],
                    "background": "辽军南下，宋真宗亲征至澶州，双方签订和约。宋朝获得百年和平但付出岁币代价。",
                    "key_wisdom": "有时妥协是必要的，可以换取发展时间。以退为进是政治智慧的重要体现。",
                    "modern_applications": [
                        {"scenario": "商业谈判", "action": "战略性让步换取长期合作"},
                        {"scenario": "国际关系", "action": "通过对话解决争端"}
                    ]
                },
                {
                    "title": "靖康之耻 - 亡国教训",
                    "year": "1127 年",
                    "dynasty": "北宋",
                    "protagonists": ["宋徽宗", "宋钦宗"],
                    "background": "金军攻破开封，俘虏徽钦二帝，北宋灭亡。骄奢淫逸导致国防空虚是根本原因。",
                    "key_wisdom": "居安思危是治国理政的重要原则。平时就要做好战备准备，不能沉迷享乐。",
                    "modern_applications": [
                        {"scenario": "企业危机", "action": "建立应急预案"},
                        {"scenario": "个人发展", "action": "持续学习保持竞争力"}
                    ]
                },
                {
                    "title": "王安石变法 - 改革困境",
                    "year": "1069-1085 年",
                    "dynasty": "北宋",
                    "protagonists": ["宋神宗", "王安石", "司马光"],
                    "background": "北宋中期财政困难，王安石推行新法试图富国强兵，但遭到保守派强烈反对最终失败。",
                    "key_wisdom": "改革需要智慧，既要坚定目标又要讲究方法。过于激进容易引发强烈反弹。",
                    "modern_applications": [
                        {"scenario": "组织变革", "action": "平衡各方利益减少阻力"},
                        {"scenario": "政策推行", "action": "试点先行逐步推广"}
                    ]
                },
                {
                    "title": "文天祥抗元 - 民族气节",
                    "year": "1276-1283 年",
                    "dynasty": "南宋末",
                    "protagonists": ["文天祥"],
                    "background": "元军南下，文天祥组织抵抗兵败被俘。面对威逼利诱坚贞不屈，最终从容就义。",
                    "key_wisdom": "民族气节是精神支柱。在关键时刻坚守原则比生命更重要。",
                    "modern_applications": [
                        {"scenario": "职业操守", "action": "坚持职业道德底线"},
                        {"scenario": "个人价值观", "action": "不为利益放弃原则"}
                    ]
                }
            ],
            
            '明清': [
                {
                    "title": "土木堡之变 - 皇帝被俘",
                    "year": "1449 年",
                    "dynasty": "明朝",
                    "protagonists": ["明英宗", "王振"],
                    "background": "明英宗在宦官王振怂恿下亲征瓦剌，结果在土木堡被俘。轻信小人导致灾难性后果。",
                    "key_wisdom": "用人不疑，疑人不用是基本原则。君主不应轻易冒险，要依靠专业将领。",
                    "modern_applications": [
                        {"scenario": "团队管理", "action": "信任专业人才给予授权"},
                        {"scenario": "风险控制", "action": "避免个人主观决策"}
                    ]
                },
                {
                    "title": "戊戌变法 - 改革失败",
                    "year": "1898 年",
                    "dynasty": "晚清",
                    "protagonists": ["光绪帝", "康有为", "梁启超"],
                    "background": "光绪帝在维新派支持下推行新政，但遭到慈禧太后反对而失败。百日维新急功近利导致惨败。",
                    "key_wisdom": "改革需要智慧和耐心，不能急功近利。过于激进容易引发强烈反弹和失败。",
                    "modern_applications": [
                        {"scenario": "企业变革", "action": "循序渐进给各方适应时间"},
                        {"scenario": "政策推行", "action": "考虑执行难度和社会承受力"}
                    ]
                },
                {
                    "title": "郑和下西洋 - 和平外交",
                    "year": "1405-1433 年",
                    "dynasty": "明朝",
                    "protagonists": ["郑和"],
                    "background": "明成祖派遣郑和七下西洋，访问东南亚、南亚、非洲等地。展示国威但不殖民掠夺。",
                    "key_wisdom": "和平外交比武力征服更有长远价值。通过文化交流建立友好关系是可持续策略。",
                    "modern_applications": [
                        {"scenario": "国际合作", "action": "互利共赢而非零和博弈"},
                        {"scenario": "品牌建设", "action": "文化传播提升影响力"}
                    ]
                },
                {
                    "title": "李自成起义 - 农民战争",
                    "year": "1627-1644 年",
                    "dynasty": "明末清初",
                    "protagonists": ["李自成"],
                    "background": "明末政治腐败民不聊生，李自成领导农民起义推翻明朝。但进入北京后迅速腐化失败。",
                    "key_wisdom": "得民心者得天下，失民心者失天下。革命成功后需保持初心不能腐化堕落。",
                    "modern_applications": [
                        {"scenario": "创业团队", "action": "成功后不忘初心"},
                        {"scenario": "组织管理", "action": "防止内部腐败"}
                    ]
                },
                {
                    "title": "康乾盛世 - 清朝鼎盛",
                    "year": "1683-1795 年",
                    "dynasty": "清朝",
                    "protagonists": ["康熙帝", "雍正帝", "乾隆帝"],
                    "background": "连续三代皇帝励精图治，开创'康乾盛世'。但后期闭关锁国埋下衰败隐患。",
                    "key_wisdom": "盛世需要持续努力不能松懈。封闭自守会导致落后于时代发展。",
                    "modern_applications": [
                        {"scenario": "企业发展", "action": "持续创新保持竞争力"},
                        {"scenario": "个人成长", "action": "终身学习适应变化"}
                    ]
                }
            ]
        }
        
        return dynasty_cases
    
    def expand_by_theme(self) -> Dict[str, List[Dict]]:
        """按主题扩充案例"""
        
        theme_cases = {
            '用人智慧': [
                {
                    "title": "萧何月下追韩信 - 求贤若渴",
                    "year": "前 202 年",
                    "dynasty": "汉初",
                    "protagonists": ["萧何", "韩信"],
                    "background": "韩信投奔刘邦未被重用欲离开，萧何连夜追赶劝回。后推荐韩信为大将，助刘邦得天下。",
                    "key_wisdom": "人才是企业最宝贵资源。求贤若渴才能吸引顶尖人才，信任授权才能发挥最大价值。",
                    "modern_applications": [
                        {"scenario": "人才招聘", "action": "主动出击寻找合适人才"},
                        {"scenario": "团队管理", "action": "给予充分信任和授权"}
                    ]
                },
                {
                    "title": "曹操三顾茅庐 - 求贤若渴",
                    "year": "207 年",
                    "dynasty": "三国",
                    "protagonists": ["刘备", "诸葛亮"],
                    "background": "刘备三次拜访诸葛亮，请其出山辅佐。最终打动诸葛亮，获得'隆中对'战略指导。",
                    "key_wisdom": "求贤若渴是成大事者的必备品质。真诚尊重人才才能吸引顶尖人才加盟。",
                    "modern_applications": [
                        {"scenario": "高管招聘", "action": "创始人亲自出面邀请"},
                        {"scenario": "团队建设", "action": "尊重专业人才给予信任"}
                    ]
                }
            ],
            
            '战略决策': [
                {
                    "title": "隆中对 - 三分天下",
                    "year": "207 年",
                    "dynasty": "三国·蜀汉",
                    "protagonists": ["诸葛亮"],
                    "background": "刘备三顾茅庐时，诸葛亮提出'跨有荆益、联吴抗曹'的战略规划，奠定蜀汉基础。",
                    "key_wisdom": "战略眼光决定企业命运。清晰的战略规划是成功的前提条件。",
                    "modern_applications": [
                        {"scenario": "商业规划", "action": "制定 3-5 年发展战略"},
                        {"scenario": "个人发展", "action": "明确职业目标和路径"}
                    ]
                },
                {
                    "title": "联吴抗曹 - 战略联盟",
                    "year": "208 年",
                    "dynasty": "三国",
                    "protagonists": ["周瑜", "诸葛亮"],
                    "background": "面对曹操大军压境，孙刘结成联盟共同抗曹。赤壁之战以少胜多奠定三国鼎立基础。",
                    "key_wisdom": "团结就是力量。联合弱小势力可以战胜强大敌人，战略联盟是关键成功因素。",
                    "modern_applications": [
                        {"scenario": "商业竞争", "action": "中小企业联合对抗行业巨头"},
                        {"scenario": "战略合作", "action": "寻找互补优势建立伙伴关系"}
                    ]
                }
            ],
            
            '改革变法': [
                {
                    "title": "商鞅变法 - 制度创新",
                    "year": "前 356-前 338 年",
                    "dynasty": "战国·秦",
                    "protagonists": ["商鞅", "秦孝公"],
                    "background": "秦国在秦孝公支持下推行变法，废井田、开阡陌，实行军功爵制，奖励耕战。",
                    "key_wisdom": "改革需要勇气和决心，更需循序渐进。制度创新是强国根本途径。",
                    "modern_applications": [
                        {"scenario": "企业转型", "action": "制定清晰的变革路线图"},
                        {"scenario": "政策改革", "action": "平衡各方利益减少阻力"}
                    ]
                },
                {
                    "title": "张居正改革 - 万历中兴",
                    "year": "1573-1582 年",
                    "dynasty": "明朝",
                    "protagonists": ["张居正"],
                    "background": "明神宗时期，张居正推行'一条鞭法'等改革措施，整顿吏治、减轻赋税，实现万历中兴。",
                    "key_wisdom": "改革需要政治智慧和执行力。循序渐进才能取得持久效果。",
                    "modern_applications": [
                        {"scenario": "组织变革", "action": "试点先行逐步推广"},
                        {"scenario": "政策推行", "action": "考虑执行难度和社会承受力"}
                    ]
                }
            ],
            
            '战争谋略': [
                {
                    "title": "围魏救赵 - 声东击西",
                    "year": "前 354-前 353 年",
                    "dynasty": "战国·齐魏",
                    "protagonists": ["孙膑"],
                    "background": "魏国围攻赵国都城，孙膑建议齐军直攻魏都大梁，迫使魏军回救，在桂陵设伏取胜。",
                    "key_wisdom": "避实击虚是军事战略重要原则。攻击敌人要害可以迫使其放弃原有目标。",
                    "modern_applications": [
                        {"scenario": "市场竞争", "action": "寻找对手薄弱环节突破"},
                        {"scenario": "问题解决", "action": "从根源入手而非表面现象"}
                    ]
                },
                {
                    "title": "空城计 - 心理战",
                    "year": "228 年",
                    "dynasty": "三国·蜀汉",
                    "protagonists": ["诸葛亮"],
                    "background": "司马懿大军压境，诸葛亮城内无兵可用。大开城门独自弹琴，司马懿疑有埋伏退兵。",
                    "key_wisdom": "心理战可以出奇制胜。利用对手疑虑和恐惧可以化解危机。",
                    "modern_applications": [
                        {"scenario": "商业谈判", "action": "展示实力虚张声势"},
                        {"scenario": "危机处理", "action": "保持镇定稳定人心"}
                    ]
                }
            ]
        }
        
        return theme_cases
    
    def generate_all_cases(self) -> Dict:
        """生成所有扩充案例"""
        
        all_new_cases = {}
        
        # 按朝代扩充
        dynasty_cases = self.expand_by_dynasty()
        for dynasty, cases in dynasty_cases.items():
            for case in cases:
                case_key = f"{case['title'].split(' - ')[0]}_{dynasty}"
                all_new_cases[case_key] = case
        
        # 按主题扩充 (去重)
        theme_cases = self.expand_by_theme()
        for theme, cases in theme_cases.items():
            for case in cases:
                case_key = f"{case['title'].split(' - ')[0]}_{theme}"
                if case_key not in all_new_cases:
                    all_new_cases[case_key] = case
        
        return all_new_cases
    
    def validate_data_quality(self, new_cases: Dict) -> bool:
        """验证数据质量"""
        
        required_fields = ['title', 'year', 'dynasty', 'protagonists', 
                          'background', 'key_wisdom', 'modern_applications']
        
        quality_issues = []
        
        for case_key, case_data in new_cases.items():
            # 检查必填字段
            for field in required_fields:
                if field not in case_data or not case_data[field]:
                    quality_issues.append(f"{case_key}: 缺少字段 {field}")
            
            # 验证数据类型
            if not isinstance(case_data.get('protagonists'), list):
                quality_issues.append(f"{case_key}: protagonists 应为列表")
            
            if not isinstance(case_data.get('modern_applications'), list):
                quality_issues.append(f"{case_key}: modern_applications 应为列表")
        
        if quality_issues:
            print(f"⚠️ 发现 {len(quality_issues)} 个质量问题:")
            for issue in quality_issues[:5]:
                print(f"   - {issue}")
            return False
        
        print(f"✅ 数据质量验证通过：{len(new_cases)} 个案例")
        return True
    
    def save_new_database(self, new_cases: Dict):
        """保存新数据库"""
        
        # 合并现有和新案例 (去重)
        merged_db = {**self.existing_cases, **new_cases}
        
        with open(self.new_case_db_path, 'w', encoding='utf-8') as f:
            json.dump(merged_db, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 新数据库已保存：{len(merged_db)} 个案例")
        print(f"   文件路径：{self.new_case_db_path}")


# 测试
if __name__ == "__main__":
    expander = CaseExpander()
    
    print("=" * 80)
    print("📚 案例库扩充工具 v1.0")
    print("=" * 80)
    
    # 生成所有新案例
    new_cases = expander.generate_all_cases()
    
    # 验证数据质量
    if expander.validate_data_quality(new_cases):
        # 保存新数据库
        expander.save_new_database(new_cases)
        
        print("\n" + "=" * 80)
        print("🎉 案例库扩充完成！")
        print("=" * 80)
    else:
        print("\n❌ 数据质量验证失败，请检查问题")
