#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
industry_classifier.py — 10-Industry Bilingual Classifier & AI-Slop / Domain-Guard Engine
10 大行业中英双语自动识别器、中英对等黑话检测与行业真实合规角标保护引擎
"""

import re
from typing import Dict, List, Optional, Tuple

# ============================================================================
# 1. 10 Major Industries Bilingual Profiles (10大行业中英双语特征库)
# ============================================================================

INDUSTRY_PROFILES: Dict[str, Dict] = {
    "tech_saas_ai": {
        "id": "tech_saas_ai",
        "name_zh": "科技 / SaaS / 人工智能",
        "name_en": "Technology, SaaS & AI",
        "tone_zh": "极客实测与架构干货风（突出延迟、吞吐量、成本降幅与真实部署指标）",
        "tone_en": "Crisp Engineering & Product Proof (focus on P99 latency, throughput, cost cut, and deployment speed)",
        "keywords_zh": [
            "大模型", "算力", "推理", "微服务", "云原生", "数据库", "延迟", "吞吐量",
            "智能体", "开源", "部署", "接口", "算法", "代码", "架构", "冷启动",
            "向量数据库", "私有化", "并发", "基准测试"
        ],
        "keywords_en": [
            "llm", "inference", "latency", "throughput", "microservice", "kubernetes",
            "cloud-native", "api", "sdk", "gpu", "saas", "deployment", "token",
            "architecture", "benchmark", "cold start", "vector database", "zero-copy",
            "sla", "high availability"
        ],
    },
    "industrial_manufacturing": {
        "id": "industrial_manufacturing",
        "name_zh": "智能制造 / 工业工程 / 自动化",
        "name_en": "Industrial, Manufacturing & Automation",
        "tone_zh": "硬核工科与现场实操风（动词 + 硬件/PLC/机构名称 + 精度/节拍/良品率）",
        "tone_en": "Shop-Floor & Mechanical Precision (Verb + hardware/actuator + repeatability, cycle time, and FPY)",
        "keywords_zh": [
            "机械", "自动化", "传感器", "气动", "分选", "产线", "工位", "公差",
            "良品率", "节拍", "电机", "接触器", "互锁", "加工", "夹具", "重复定位精度",
            "伺服", "导轨", "气缸", "电控"
        ],
        "keywords_en": [
            "plc", "scada", "actuator", "sensor", "conveyor", "tolerance",
            "repeatability", "cycle time", "oee", "interlock", "cnc", "robotics",
            "assembly line", "pneumatic", "torque", "first pass yield", "fpy",
            "mtbf", "servo", "encoder"
        ],
    },
    "education_academia": {
        "id": "education_academia",
        "name_zh": "教育 / 学术科研 / 高校竞赛",
        "name_en": "Education, Academia & Campus Competitions",
        "tone_zh": "高校创客答辩与严谨学术风（讲真痛点、亲手做的实验/样机、消融对比与真实经费成本）",
        "tone_en": "Rigorous Academic & Hands-On Pitch (ablation studies, statistical significance, BOM cost, field testing)",
        "keywords_zh": [
            "高校", "课程", "学生", "实训", "实验", "答辩", "竞赛", "论文",
            "样本", "问卷", "教学", "学业", "实验室", "挑战杯", "样机", "消融实验",
            "对照组", "显著性", "物料清单", "实训台"
        ],
        "keywords_en": [
            "curriculum", "student", "pedagogy", "classroom", "ablation", "dataset",
            "hypothesis", "campus", "semester", "prototype", "laboratory", "thesis",
            "peer-reviewed", "syllabus", "ablation study", "control group",
            "statistical significance", "bom cost", "field test", "pedagogical"
        ],
    },
    "finance_consulting": {
        "id": "finance_consulting",
        "name_zh": "金融 / 投资 / 财税与商业咨询",
        "name_en": "Finance, VC, FinTech & Consulting",
        "tone_zh": "投行与咨询结论先行风（一页一结论，直给营收增速、毛利基点、回本周期与合规风控）",
        "tone_en": "Wall Street & MBB Executive Clarity (headline conclusion first, ARR, NDR, bps margin expansion, CAC payback)",
        "keywords_zh": [
            "毛利率", "净利", "现金流", "估值", "融资", "回本周期", "留存率", "财报",
            "审计", "风控", "资产", "收益率", "投资", "组合", "成本", "基点",
            "自由现金流", "净留存", "尽职调查", "合规"
        ],
        "keywords_en": [
            "ebitda", "gaap", "arr", "ndr", "cac", "ltv", "payback", "valuation",
            "portfolio", "audit", "cagr", "margin", "liquidity", "underwriting",
            "fintech", "roi", "net dollar retention", "free cash flow", "bps", "due diligence"
        ],
    },
    "healthcare_biotech": {
        "id": "healthcare_biotech",
        "name_zh": "医疗健康 / 生物医药与临床科研",
        "name_en": "Healthcare, Biotech & MedTech",
        "tone_zh": "严谨临床医学与循证风（基于三甲实测、入组样本量、敏感度/特异度与注册合规）",
        "tone_en": "Evidence-Based Clinical Precision (sample size n, sensitivity/specificity, p-value, regulatory clearance)",
        "keywords_zh": [
            "临床", "医院", "患者", "筛查", "病灶", "诊疗", "敏感度", "特异度",
            "药物", "靶点", "基因", "护理", "医疗器械", "漏诊", "入组", "假阴性",
            "双盲对照", "不良反应", "适应症", "三甲医院"
        ],
        "keywords_en": [
            "clinical", "patient", "cohort", "biomarker", "sensitivity", "specificity",
            "fda", "therapeutic", "diagnostic", "oncology", "pathology", "placebo",
            "trial", "efficacy", "dosage", "double-blind", "progression-free survival",
            "adverse event", "endpoint", "in vitro"
        ],
    },
    "retail_marketing": {
        "id": "retail_marketing",
        "name_zh": "消费零售 / 电商增长与品牌营销",
        "name_en": "Retail, E-Commerce & Brand Marketing",
        "tone_zh": "实战增长与主理人直白风（用转化率、复购率、客单价和真实测评反馈说话）",
        "tone_en": "Direct-to-Consumer Growth & Conversion (ROAS, repeat purchase rate, AOV, creator conversion, inventory turn)",
        "keywords_zh": [
            "电商", "复购", "客单价", "转化率", "门店", "坪效", "种草", "直播",
            "货架", "消费者", "品牌", "大促", "私域", "销量", "爆款", "动销率",
            "首单", "投流", "退货率", "连带率"
        ],
        "keywords_en": [
            "roas", "ecommerce", "omnichannel", "conversion", "retention", "aov",
            "sku", "merchandising", "storefront", "checkout", "influencer", "campaign",
            "shopper", "footfall", "inventory turnover", "repeat purchase", "gmv",
            "ctr", "click-through rate", "return rate"
        ],
    },
    "public_gov_smartcity": {
        "id": "public_gov_smartcity",
        "name_zh": "政务公共事业 / 国企央企与智慧城市",
        "name_en": "Public Sector, GovTech & Smart City",
        "tone_zh": "务实政务与为民服务风（彻底清除洋气伪英文角标，突出办事时限压缩、跨部门打通与群众覆盖面）",
        "tone_en": "Pragmatic Civic Delivery (strip pseudo-startup badges; highlight permit turnaround cut and citizen coverage)",
        "keywords_zh": [
            "政务", "一网通办", "审批", "基层", "网格", "市民", "公共服务", "社区",
            "部门", "党建", "国企", "督导", "便民", "治理", "市政", "最多跑一次",
            "办结率", "营商环境", "政务公开", "民生"
        ],
        "keywords_en": [
            "municipal", "civic", "citizen", "public sector", "permit", "governance",
            "transit", "ordinance", "agency", "inter-agency", "public works", "smart city",
            "procurement", "e-government", "civic tech", "public administration",
            "public service", "infrastructure", "regulatory compliance", "zoning"
        ],
    },
    "architecture_design": {
        "id": "architecture_design",
        "name_zh": "建筑地产 / 空间营造与工业设计",
        "name_en": "Architecture, Real Estate & Industrial Design",
        "tone_zh": "实体质感与工程造物风（讲真实材料工艺、倒角壁厚、采光动线与容积率，拒绝空谈美学闭环）",
        "tone_en": "Tactile Materiality & Spatial Craft (anodized aluminum, wall thickness, daylight factor, circulation, FAR)",
        "keywords_zh": [
            "建筑", "容积率", "户型", "采光", "立面", "材质", "阳极氧化", "倒角",
            "工业设计", "空间", "动线", "结构", "景观", "园区", "人居", "窗墙比",
            "得房率", "壁厚", "装配式", "铝合金"
        ],
        "keywords_en": [
            "facade", "floor plan", "anodized", "chamfer", "ergonomic", "unibody",
            "spatial", "zoning", "daylight", "rendering", "cad", "materiality",
            "cantilever", "urban design", "window-to-wall ratio", "wall thickness",
            "structural engineering", "cross-ventilation", "fenestration", "blueprint"
        ],
    },
    "energy_sustainability_agtech": {
        "id": "energy_sustainability_agtech",
        "name_zh": "新能源 / 碳中和 / 现代农业与环保",
        "name_en": "Clean Energy, ESG, Sustainability & AgTech",
        "tone_zh": "绿色实效与田间实测风（直给度电成本、减排吨数、节水比例与亩产增幅）",
        "tone_en": "Measurable ESG & Field Agronomy (LCOE, tCO2e abated, cycle life, irrigation savings, yield per acre)",
        "keywords_zh": [
            "光伏", "储能", "碳中和", "减排", "度电成本", "农业", "灌溉", "亩产",
            "大棚", "土壤", "水肥", "绿电", "果蔬", "能耗", "回收", "水肥一体化",
            "循环寿命", "碳足迹", "微电网", "滴灌"
        ],
        "keywords_en": [
            "solar", "photovoltaic", "battery", "lcoe", "tco2e", "carbon",
            "esg", "irrigation", "agronomy", "crop", "yield", "greenhouse",
            "renewable", "grid", "emissions", "drip irrigation", "cycle life",
            "soil moisture", "carbon footprint", "scope 1"
        ],
    },
    "media_gaming_hospitality": {
        "id": "media_gaming_hospitality",
        "name_zh": "文娱传媒 / 游戏动漫 / 文旅与创意内容",
        "name_en": "Media, Gaming, Cultural IP & Hospitality",
        "tone_zh": "玩家/游客真实体验风（讲完播率、次留率、战斗帧率、互动玩法与单日客流打卡）",
        "tone_en": "Player & Guest Experience First (hook retention, D1/D7 retention, 60fps gameplay, occupancy, foot traffic)",
        "keywords_zh": [
            "游戏", "玩家", "完播率", "留存", "景区", "文旅", "非遗", "演出",
            "票房", "剧情", "关卡", "帧率", "动画", "打卡", "客流", "满房率",
            "次留", "打击感", "二消", "关卡设计"
        ],
        "keywords_en": [
            "gameplay", "player", "retention", "frame rate", "ray tracing", "box office",
            "hospitality", "tourism", "occupancy", "storytelling", "episodic", "soundtrack",
            "visitor", "d1 retention", "level design", "rendering engine", "unreal engine",
            "unity", "occupancy rate", "ip licensing"
        ],
    },
}

# ============================================================================
# 2. 1:1 Chinese & English AI Buzzwords & Slop Patterns (中英对等黑话库)
# ============================================================================

AI_BUZZWORDS_ZH = [
    "赋能", "抓手", "闭环", "全链路", "多维度", "全方位", "深层次",
    "底层逻辑", "顶层设计", "范式转移", "生态体系", "协同共振", "组合拳",
    "颗粒度", "痛点剖析", "破局之道", "矩阵", "价值跃迁", "新生态",
    "战略支点", "多维感知", "深度融合", "全渠道", "靶向发力", "精准施策",
    "心智占领", "价值飞轮", "全域增长", "数智化底座", "颠覆性创新"
]

AI_BUZZWORDS_EN = [
    "delve", "delving", "testament to", "rich tapestry", "tapestry of",
    "paradigm shift", "paradigm-shifting", "synergy", "synergistic",
    "holistic", "holistically", "empower", "empowering", "empowerment",
    "game-changer", "game-changing", "cutting-edge", "next-gen", "next-generation",
    "seamless", "seamlessly", "leverage", "leveraging", "utilize", "utilizing",
    "unlock the full potential", "unleash", "unleashing", "foster", "fostering",
    "spearhead", "spearheading", "transformative", "revolutionize", "revolutionizing",
    "in today's fast-paced", "in the ever-evolving", "at the forefront of",
    "beacon of", "pivotal role", "underscore", "underscoring", "multifaceted"
]

# 英文卡片内同义反复凑数从句正则
REDUNDANT_SUBTEXT_EN_RE = re.compile(
    r"\b(by\s+(?:leveraging|utilizing|harnessing|integrating|combining)|"
    r"designed\s+to\s+(?:seamlessly|holistically|effectively)\s+(?:empower|facilitate|unlock|enhance)|"
    r"empowering\s+(?:organizations|enterprises|users|teams)\s+to\s+achieve|"
    r"driving\s+holistic\s+and\s+sustainable|"
    r"facilitating\s+end-to-end)\b",
    re.I,
)

# 中文卡片内同义反复凑数小字关键词
REDUNDANT_SUBTEXT_ZH_KEYS = [
    "通过", "实现", "助力", "构建", "赋能", "多维", "闭环", "有效", "体系", "全链路", "全方位"
]

# ============================================================================
# 3. Protected Real Domain Footnotes & Compliance Guard (真合规/真数据保护网)
# ============================================================================

# 拒绝将虚假演示占位符当作受保护声明
DISCLAIMER_FAKE_PATTERNS = re.compile(
    r"("
    r"仅供演示|演示参考|演示使用|排版展示|仅供排版展示|虚拟数据|虚构数据|占位数据|"
    r"for\s+(?:demonstration|illustrative|display|testing)\s+purposes?(?:\s+only)?|"
    r"(?:illustrative|sample|fictitious|mock|dummy|placeholder)\s+(?:layout|data|text|metrics|numbers?)|"
    r"(?:generated|created)\s+by\s+ai|ai-generated(?:\s+placeholder)?"
    r")",
    re.I,
)

PROTECTED_FOOTNOTE_PATTERNS = [
    # 医疗/临床/生物统计 (Clinical, Medical & Biotech)
    re.compile(
        r"(?<!\w)(p\s*(?:[<≤=]|&lt;)\s*0\.\d+|95%\s*CI|n\s*=\s*\d+|FDA\s*(?:510\(k\)|PMA|IND|NDA)|NMPA|CE\s*Mark|NCT\d{6,}|Phase\s*(?:I|II|III|IV|[1-4])|IC50|mPFS|For Investigational Use Only)(?!\w)",
        re.I | re.A,
    ),
    re.compile(
        r"(国械注准|国药准字|临床试验|多中心|伦理委员会|不良反应|双盲对照|受试者|适应症|敏感度|特异度)"
    ),

    # 金融/审计/法律/来源披露 (Financial, Audit & Regulatory)
    re.compile(
        r"(?<!\w)(Non-GAAP|GAAP|EBITDA|Unaudited|SEC\s*Form|10-K|10-Q|CAGR|YoY|QoQ|bps|Bloomberg|Wind|ROAS|Past performance is not indicative)(?!\w)",
        re.I | re.A,
    ),
    re.compile(
        r"(未经审计|经审计|会计准则|过往业绩不代表未来|风险提示|数据来源\s*[:：]|数据统计周期\s*[:：]|统计周期|统计口径\s*[:：]|统计口径)"
    ),

    # 工业/工程/双碳/标准规范 (Engineering, Standards & ESG)
    re.compile(
        r"(?<!\w)(ISO\s*\d{4,5}(?:-\d+)?|IEC\s*\d+|GB(?:/T)?\s*\d+(?:-\w+)?|ASTM\s*[A-Z0-9-]+|Scope\s*[123]|tCO2e|LCOE|IEEE|CVPR|NeurIPS|ICML|arXiv|PLC|S7-\d{3,4}|P99\s*latency|SLA\s*9\d|MTBF)(?!\w)",
        re.I | re.A,
    ),
    re.compile(
        r"(国家自然科学基金|公差等级|安全等级|一网通办|最多跑一次|P99\s*延迟|测试环境\s*[:：]|容积率|FAR\s*\d)"
    ),

    # 文娱/媒体版权与帧率 (Media, IP & Gaming)
    re.compile(
        r"(?<!\w)(UE5|4K@\d*fps|©\s*\d{4}|Copyright\s*(?:©|\(c\))?\s*\d{4})(?!\w)",
        re.I | re.A,
    ),
]


def is_protected_domain_footnote(text: str) -> bool:
    """判断一段小字是否属于严禁误删的真实行业合规声明、临床统计、审计口径或工程标准"""
    clean = text.strip()
    if not clean:
        return False
    # 若包含明显的 AI 演示免责假话，则不属于受保护真声明
    if DISCLAIMER_FAKE_PATTERNS.search(clean):
        return False
    for pat in PROTECTED_FOOTNOTE_PATTERNS:
        if pat.search(clean):
            return True
    return False


def detect_buzzwords_bilingual(text: str) -> List[str]:
    """同时检测中英文 AI 黑话"""
    hits = []
    for w in AI_BUZZWORDS_ZH:
        if w in text:
            hits.append(w)
    lower_t = text.lower()
    for w in AI_BUZZWORDS_EN:
        if re.search(r"\b" + re.escape(w) + r"\b", lower_t):
            hits.append(w)
    return list(dict.fromkeys(hits))


def is_redundant_subtext_bilingual(text: str) -> bool:
    """判断中英文小字是否属于同义反复的凑数解释"""
    if any(k in text for k in REDUNDANT_SUBTEXT_ZH_KEYS):
        return True
    if REDUNDANT_SUBTEXT_EN_RE.search(text):
        return True
    return False


def detect_industry_and_language(full_text: str) -> Dict:
    """
    根据全文内容自动识别主语言 (zh / en / bilingual) 与所属的 10 大行业 Profile。
    使用 (?<![a-zA-Z0-9]) 与 (?![a-zA-Z0-9]) 代替 \b，防止中英无空格混合时英文词被 CJK 吞没。
    """
    cjk_chars = len(re.findall(r"[\u4e00-\u9fa5]", full_text))
    en_words = len(re.findall(r"[A-Za-z]{2,}", full_text))

    if cjk_chars > 0 and en_words > 0:
        if cjk_chars >= en_words * 0.5:
            lang = "zh" if cjk_chars > en_words * 1.5 else "bilingual"
        else:
            lang = "en"
    elif cjk_chars > 0:
        lang = "zh"
    else:
        lang = "en"

    lower_text = full_text.lower()
    scores = []
    for ind_id, prof in INDUSTRY_PROFILES.items():
        matched_zh = [kw for kw in prof["keywords_zh"] if kw in full_text]
        matched_en = [
            kw for kw in prof["keywords_en"]
            if re.search(r"(?<![a-zA-Z0-9])" + re.escape(kw) + r"(?![a-zA-Z0-9])", lower_text)
        ]
        score = len(matched_zh) * 2 + len(matched_en) * 2
        scores.append((score, ind_id, matched_zh + matched_en))

    scores.sort(key=lambda x: x[0], reverse=True)
    best_score, best_id, matched_terms = scores[0]

    # 默认兜底为 tech_saas_ai
    if best_score == 0:
        best_id = "tech_saas_ai"
        matched_terms = []

    best_prof = INDUSTRY_PROFILES[best_id]
    return {
        "language": lang,
        "industry_id": best_id,
        "industry_name_zh": best_prof["name_zh"],
        "industry_name_en": best_prof["name_en"],
        "recommended_tone_zh": best_prof["tone_zh"],
        "recommended_tone_en": best_prof["tone_en"],
        "matched_domain_terms": matched_terms[:10],
        "confidence": "high" if best_score >= 6 else ("medium" if best_score >= 2 else "default"),
    }


# ============================================================================
# 4. Programmatic Domain Whitelist & Footnote Exposure APIs
# ============================================================================

def get_supported_industries() -> List[str]:
    """返回支持的 10 大行业 ID 列表"""
    return list(INDUSTRY_PROFILES.keys())


def get_industry_profile(industry_id: str) -> Dict:
    """获取指定行业的完整 Profile"""
    if industry_id not in INDUSTRY_PROFILES:
        raise KeyError(f"Unknown industry ID: {industry_id}. Supported: {list(INDUSTRY_PROFILES.keys())}")
    return INDUSTRY_PROFILES[industry_id]


def get_industry_whitelist(industry_id: str, lang: str = "all") -> List[str]:
    """获取指定行业的真实专业术语白名单 (zh / en / all)"""
    if industry_id not in INDUSTRY_PROFILES:
        return []
    prof = INDUSTRY_PROFILES[industry_id]
    if lang == "zh":
        return list(prof.get("keywords_zh", []))
    elif lang == "en":
        return list(prof.get("keywords_en", []))
    else:
        return list(prof.get("keywords_zh", [])) + list(prof.get("keywords_en", []))


def get_all_whitelists() -> Dict[str, Dict[str, List[str]]]:
    """获取全部 10 大行业中英文术语白名单映射"""
    return {
        ind_id: {
            "zh": list(prof.get("keywords_zh", [])),
            "en": list(prof.get("keywords_en", [])),
        }
        for ind_id, prof in INDUSTRY_PROFILES.items()
    }


def get_protected_footnote_patterns() -> List[re.Pattern]:
    """获取保护真实角标的正则表达式编译对象列表"""
    return list(PROTECTED_FOOTNOTE_PATTERNS)


def is_whitelisted_domain_term(term: str, industry_id: Optional[str] = None) -> bool:
    """判断一个词是否属于指定行业或任意行业的专业术语白名单，防止清洗器误改/误删"""
    clean_term = term.strip().lower()
    if not clean_term:
        return False
    target_industries = [industry_id] if industry_id and industry_id in INDUSTRY_PROFILES else list(INDUSTRY_PROFILES.keys())
    for i_id in target_industries:
        prof = INDUSTRY_PROFILES[i_id]
        if any(kw in clean_term for kw in prof.get("keywords_zh", [])):
            return True
        if any(
            kw.lower() == clean_term or re.search(r"(?<![a-zA-Z0-9])" + re.escape(kw.lower()) + r"(?![a-zA-Z0-9])", clean_term)
            for kw in prof.get("keywords_en", [])
        ):
            return True
    return False
