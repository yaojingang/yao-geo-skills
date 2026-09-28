"""Industry-aware commercial-intent scoring for Baidu keyword expansions."""

from __future__ import annotations

import json
import re
from pathlib import Path

SCRIPT_INTERFACE = 'internal-module'
SCRIPT_INTERFACE_REASON = 'Imported by the workbook builder and scoring checks.'

def has(text: str, pattern: str) -> bool:
    return re.search(pattern, text) is not None


def score_legal_keyword(raw: str) -> tuple[int, str]:
    term = re.sub(r'\s+', '', raw)
    specific_cases = {
        '离婚抚养权在男方,女方一直带着孩子': (7, '具体抚养争议'),
        '离婚财产分割会查个人账户吗': (5, '财产调查准备'),
        '离婚协议书写了房子归属有效吗': (5, '具体协议效力'),
        '婚内出轨赔偿协议': (5, '具体协议需求'),
        '婚内出轨离婚赔偿': (5, '具体赔偿问题'),
        '父亲过世后房产由母亲继承吗': (5, '具体继承问题'),
        '拖欠抚养费的后果': (4, '抚养费规则查询'),
        '第二次起诉离婚能离掉吗': (7, '继续诉讼的结果判断'),
        '第二次起诉离婚会判离吗': (6, '继续诉讼的结果判断'),
        '第二次起诉离婚男方不同意会判离吗': (7, '具体诉讼争议'),
    }
    if term in specific_cases:
        return specific_cases[term]

    # 百度下拉框里存在与法律服务同名的影视、小说和资讯词。
    if has(term, r'电视剧|短剧|在线观看|免费观看|小说|养成手册|手机版免费观看'):
        return 1, '娱乐或下载'
    if has(term, r'新闻|有没有退还|北京见面礼一般给多少|出手终止家暴噩梦|为老人撑腰'):
        return 2, '资讯浏览'
    if has(term, r'独特的简介|团队介绍|pdf$'):
        return 3, '职业或资料查询'
    if has(term, r'^.*流程是什么$|^.*具体流程是什么$'):
        return 4, '流程查询'
    if has(term, r'诉讼时效'):
        return 4, '诉讼期限查询'
    if has(term, r'诉讼费|起诉费|法院怎么收费'):
        return 5, '诉讼成本查询'
    if has(term, r'冷静期') and has(term, r'起诉离婚|诉讼离婚'):
        return 4, '离婚程序规则'
    if has(term, r'婚前财产公证是什么意思'):
        return 2, '概念查询'
    if has(term, r'家暴法律咨询免费'):
        return 6, '免费法律咨询'
    if has(term, r'家暴法律求助'):
        return 7, '即时法律求助'
    if has(term, r'结婚需要什么手续'):
        return 3, '婚姻登记事务'
    if has(term, r'不给抚养费') and has(term, r'后果|三种情况|老了要管|犯法吗'):
        return 4, '抚养费规则查询'
    if has(term, r'不给抚养费起诉流程'):
        return 6, '诉讼流程查询'
    if has(term, r'不给抚养费起诉有效果'):
        return 7, '维权可行性查询'
    if has(term, r'父母告孩子不赡养一般怎么判'):
        return 6, '裁判结果查询'
    if has(term, r'父亲没了,母亲还在,怎么继承房产'):
        return 6, '具体继承问题'
    if has(term, r'最怕三个|三种情况|三大忌|6大忌|十大忌讳'):
        return 3, '泛知识浏览'

    # 找到可委托的律师、律所，或比较其报价，是最直接的商业意图。
    provider = has(term, r'律师|律所|法律服务')
    if provider:
        if has(term, r'最害怕三个问题|找律师三个忌讳'):
            return 2, '律师话题浏览'
        if has(term, r'代理权限|特别授权|由哪一方承担|谁来承担|律师费可以退|先收费还是先办事'):
            return 5, '委托规则查询'
        if has(term, r'调查令多少钱|查询网'):
            return 6, '律师工具查询'
        if has(term, r'需要找律师吗|要请律师吗|需要律师吗|自己写还是律师写|找律师代写还是自己写'):
            return 8, '考虑委托律师'
        if has(term, r'请律师') and has(term, r'费用|多少钱|希望有多大|会见一次'):
            return 9, '委托律师价格或效果查询'
        if has(term, r'代写律师'):
            return 10, '明确律师代写需求'
        if has(term, r'哪里找|找谁|怎么找|找靠谱|找律师|哪家|哪个比较好|最好|排名|附近|专打|专业|推荐|请律师'):
            value = 10
            reason = '主动寻找律师或律所'
        elif has(term, r'事务所|律所|预约|电话|热线|联系|咨询|在线解答|询问'):
            value = 9
            reason = '联系律师或律所'
        elif has(term, r'收费|费用|律师费|价目|多少钱|付费'):
            value = 9
            reason = '比较法律服务价格'
        elif has(term, r'要请律师|需要律师|找律师代写|律师代写|律师写'):
            value = 9
            reason = '考虑委托律师'
        elif has(term, r'律师网|律师能帮|律师可以查'):
            value = 7
            reason = '律师能力或渠道查询'
        else:
            value = 9
            reason = '明确律师服务需求'
        if has(term, r'免费|公益|法律援助'):
            value = min(value, 7)
            reason = '免费法律服务需求'
        if term in {'家暴律师李莹', '重婚罪律师臧梵清'}:
            value, reason = 7, '指定律师查询'
        return value, reason

    # 代写和公证是明确的服务购买意图，低于直接寻找律所。
    if '代写' in term:
        if has(term, r'模板|范文'):
            return 3, '代写模板查询'
        if has(term, r'有效吗|合法吗|可以吗|有什么要求|需要公证吗'):
            return 6, '代写可行性查询'
        if has(term, r'收费|费用|多少钱|价格|贵么|找谁'):
            return 9, '比较代写服务价格'
        return 8, '代写服务需求'
    if has(term, r'法律援助|法律求助|12348'):
        if has(term, r'案例|途径|条件|申请书|申请怎么写|可以申请|不给法律援助|拨打12348的后果'):
            return 4, '援助资格或流程查询'
        if has(term, r'如何寻求|怎么联系|热线|地址|中心|妇女'):
            return 6, '寻找免费法律援助'
        return 5, '免费法律援助需求'
    if '公证' in term:
        if has(term, r'是什么意思|区别|有必要吗|有效吗|法律效力|需要另一方知道|可以一个人办|需要双方到场|需要见证人|什么要求|忌'):
            return 4, '公证规则查询'
        if has(term, r'找谁|在哪里办理|费用|收费|多少钱'):
            return 8 if '找谁' in term else 7, '公证服务选择或报价'
        if has(term, r'怎么公证|怎么办理|流程|手续|公证遗嘱|遗嘱赠予公证'):
            return 6, '公证办理需求'
        return 5, '公证相关需求'

    # 结婚登记和户口手续通常可自行到行政部门办理。
    if has(term, r'结婚证|结婚手续|婚姻登记|初婚登记|三婚的怎么|网上预约登记结婚|婚迁'):
        return (2 if has(term, r'是什么|规定|证$') else 3), '婚姻登记事务'
    if has(term, r'户口|立户|原籍村委'):
        return (5 if has(term, r'不接收|弄出去|怎么迁出|无房') else 3), '户籍手续'

    # 定义、模板、法规、案例和资讯类查询优先低分。
    if has(term, r'模板|范文|范本|word|下载|电子版|协议书标准版|协议书范本|起诉状范文|答辩状范文'):
        return 3, '模板或范文'
    if has(term, r'研究|案例中|成功案例|公诉案例|胜诉案例|纠纷案例|法律问题研究'):
        return 3, '案例或研究'
    if has(term, r'是什么意思|什么叫|是怎么回事|是什么|区别|谁提出的|哪年开始|什么时候实施|第几继承人|顺序|的顺序人'):
        return 2, '概念或背景查询'
    if has(term, r'最新政策|最新规定|法律法规|法律规定|司法解释|民法典|新规|法规定|法律责任|原则|判定标准|认定标准|的条件|标准是什么|有效吗|有法律效力吗|合法吗'):
        return 4, '法律规则查询'

    # 已发生的争议、维权和诉讼更可能需要专业帮助。
    if has(term, r'官司怎么打|怎么打官司|打官司才能赢|怎么争取|争取自己最大利益|怎么让公安取证|拒还|不给|不赡养|不抚养|拖欠|被骗了怎么办|能离掉吗'):
        return 8, '争议处理需求'
    if has(term, r'纠纷|争夺|争议'):
        if has(term, r'怎么处理|如何处理|怎么解决|如何起诉|怎么起诉|官司|诉讼'):
            return 7, '具体纠纷求助'
        if has(term, r'证据|起诉|案件|处理'):
            return 6, '纠纷准备或处理'
        return 6, '纠纷意图'
    if has(term, r'诉讼|起诉|控告|立案|法庭|开庭|法院|自诉|公诉|告重婚|告孩子|告其中一方'):
        if has(term, r'怎么起诉|如何起诉|怎样起诉|怎么打|再起诉|起诉重新分割'):
            return 7, '启动或继续诉讼'
        if has(term, r'材料|流程|程序|多久|多少钱|费用|收费|诉状|判决|证据|管辖|到庭|出庭|间隔|几率|能不能|需要什么|判离|能离|冷静期|控告书|在哪'):
            return 5, '诉讼流程查询'
        return 7, '诉讼需求'
    if has(term, r'证据|取证|胜诉|净身出户'):
        return 6, '证据或胜诉准备'

    # 其余词按执行距离和自助程度评分。
    if has(term, r'协议书自己写还是|自己写还是|怎么写才有效|怎样写才有效|协议怎样写|协议怎么写|财产协议书怎样写'):
        return 6, '协议拟定需求'
    if has(term, r'怎么处理|怎么办|怎样要回|怎么要回|如何处理|如何解决|女方怎么|男方怎么|怎么分|怎么判|归谁|如何确定|如何分割|怎么分配'):
        return 6, '具体法律问题'
    if has(term, r'赔偿|抚养权|抚养费|继承|遗产|分家析产|彩礼|家暴|重婚罪|婚内出轨|债务|财产分割'):
        if has(term, r'需要多少钱|多少钱|费用|收费|要交税|税费|手续费|多长时间|多久|流程|材料|手续|申请|办理|过户'):
            return 5, '办事成本或流程'
        if has(term, r'怎么|如何|需要|可以|能不能|要不要|应该'):
            return 5, '具体法律问题'
        return 4, '法律主题查询'
    if has(term, r'费用|收费|多少钱|要交税|税费|手续费'):
        return 4, '行政或诉讼成本查询'
    if has(term, r'流程|手续|材料|办理|申请|怎么弄|去哪里|哪里办|多久|时间'):
        return 4, '自助办理查询'
    return 3, '一般信息查询'


PROFILE_FILE = Path(__file__).resolve().parent.parent / 'references' / 'industry-profiles.json'
ALIASES = {
    'legal': 'legal', '法律': 'legal', '法律服务': 'legal', '律师': 'legal',
    'medical': 'medical', '医疗': 'medical', '医疗服务': 'medical',
    'education': 'education', '教育': 'education', '教育培训': 'education',
    'study_abroad': 'study_abroad', '留学': 'study_abroad', '留学服务': 'study_abroad', '出国留学': 'study_abroad',
    'renovation': 'renovation', '家装': 'renovation', '装修': 'renovation',
    'ecommerce': 'ecommerce', '电商': 'ecommerce', '商品零售': 'ecommerce',
}


def validate_profile(raw: object, label: str) -> dict:
    if not isinstance(raw, dict):
        raise ValueError(f'{label} 必须是 JSON 对象')
    if '_builtin_legal' in raw:
        raise ValueError(f'{label} 不能包含内部评分标记')
    if 'id' in raw and (not isinstance(raw['id'], str) or not raw['id'].strip()):
        raise ValueError(f'{label}.id 必须是非空文本')
    for key in ('industry', 'conversion_goal'):
        if not isinstance(raw.get(key), str) or not raw[key].strip():
            raise ValueError(f'{label}.{key} 必须是非空文本')
    rules = raw.get('rules')
    if not isinstance(rules, list) or not 1 <= len(rules) <= 80:
        raise ValueError(f'{label}.rules 必须包含 1–80 条规则')
    for index, rule in enumerate(rules, 1):
        if not isinstance(rule, dict):
            raise ValueError(f'{label}.rules[{index}] 必须是对象')
        if type(rule.get('score')) is not int or not 1 <= rule['score'] <= 10:
            raise ValueError(f'{label}.rules[{index}].score 必须是 1–10 的整数')
        if not isinstance(rule.get('reason'), str) or not rule['reason'].strip():
            raise ValueError(f'{label}.rules[{index}].reason 必须是非空文本')
        pattern = rule.get('pattern')
        if not isinstance(pattern, str) or not 1 <= len(pattern) <= 200:
            raise ValueError(f'{label}.rules[{index}].pattern 长度必须是 1–200')
        try:
            re.compile(pattern)
        except re.error as exc:
            raise ValueError(f'{label}.rules[{index}].pattern 无效: {exc}') from exc
    fallback = raw.get('fallback')
    if not isinstance(fallback, dict) or type(fallback.get('score')) is not int or not 1 <= fallback['score'] <= 10:
        raise ValueError(f'{label}.fallback.score 必须是 1–10 的整数')
    if not isinstance(fallback.get('reason'), str) or not fallback['reason'].strip():
        raise ValueError(f'{label}.fallback.reason 必须是非空文本')
    return raw


def load_profile(industry: str | None = None, profile_path: Path | None = None) -> dict:
    if profile_path is not None:
        profile = validate_profile(json.loads(profile_path.read_text(encoding='utf-8')), str(profile_path))
        selected = ALIASES.get(industry, industry) if industry else None
        profile_industry = ALIASES.get(profile['industry'], profile['industry'])
        if selected in {'legal', 'medical', 'education', 'study_abroad', 'renovation', 'ecommerce'} and selected != profile_industry:
            raise ValueError('指定行业与自定义评分画像的行业不一致')
        if selected and selected not in {profile.get('id'), profile_industry}:
            raise ValueError('指定行业与自定义评分画像不一致')
        return profile
    key = ALIASES.get(industry or '', industry or '')
    if not key:
        raise ValueError('缺少行业：请使用 --industry 或提供 --profile 自定义评分画像')
    profiles = json.loads(PROFILE_FILE.read_text(encoding='utf-8'))['profiles']
    if key not in profiles:
        raise ValueError(f'未知行业 {industry!r}：使用 --profile 指定该行业的转化目标和评分规则')
    profile = profiles[key]
    if key == 'legal':
        if not isinstance(profile, dict) or not all(isinstance(profile.get(field), str) and profile[field].strip() for field in ('industry', 'conversion_goal')):
            raise ValueError('内置法律服务画像缺少行业或转化目标')
        profile = profile.copy()
        profile['_builtin_legal'] = True
        return profile
    return validate_profile(profile, f'内置行业 {key}').copy()


def score_keyword(term: str, profile: dict) -> tuple[int, str]:
    if profile.get('_builtin_legal'):
        return score_legal_keyword(term)
    normalized = ' '.join(term.split())
    for rule in profile['rules']:
        if re.search(rule['pattern'], normalized, re.IGNORECASE):
            return rule['score'], rule['reason']
    fallback = profile['fallback']
    return fallback['score'], fallback['reason']
