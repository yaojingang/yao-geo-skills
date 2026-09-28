#!/usr/bin/env python3
"""Check built-in industry scoring examples and custom-profile validation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from score_keywords import load_profile, score_keyword


ROOT = Path(__file__).resolve().parent.parent
CASES = ROOT / 'evals' / 'scoring_cases.json'


def main() -> int:
    argparse.ArgumentParser(description=__doc__).parse_args()
    cases = json.loads(CASES.read_text(encoding='utf-8'))
    for index, case in enumerate(cases, 1):
        profile = load_profile(case['industry'])
        actual, _ = score_keyword(case['term'], profile)
        if actual != case['score']:
            raise AssertionError(f"case {index}: {case['term']}: expected {case['score']}, got {actual}")

    custom = {
        'id': 'pet_grooming', 'industry': '宠物洗护',
        'conversion_goal': '预约到店宠物洗护',
        'rules': [
            {'pattern': '自己洗', 'score': 2, 'reason': '自助内容'},
            {'pattern': '预约', 'score': 10, 'reason': '预约服务'},
        ],
        'fallback': {'score': 4, 'reason': '一般信息查询'},
    }
    with TemporaryDirectory() as folder:
        path = Path(folder) / 'custom.json'
        path.write_text(json.dumps(custom, ensure_ascii=False), encoding='utf-8')
        profile = load_profile(profile_path=path)
        assert score_keyword('宠物洗护预约', profile)[0] == 10
        assert score_keyword('自己洗宠物教程', profile)[0] == 2
        assert score_keyword('宠物洗护知识', profile)[0] == 4

        legal_custom = {
            'id': 'legal', 'industry': '法律服务',
            'conversion_goal': '下载法律文书模板',
            'rules': [{'pattern': '模板', 'score': 10, 'reason': '下载意图'}],
            'fallback': {'score': 1, 'reason': '其他搜索'},
        }
        path.write_text(json.dumps(legal_custom, ensure_ascii=False), encoding='utf-8')
        profile = load_profile(industry='legal', profile_path=path)
        assert score_keyword('离婚协议模板', profile)[0] == 10
        assert score_keyword('离婚律师推荐', profile)[0] == 1

        legal_custom['_builtin_legal'] = True
        path.write_text(json.dumps(legal_custom, ensure_ascii=False), encoding='utf-8')
        try:
            load_profile(industry='legal', profile_path=path)
        except ValueError:
            pass
        else:
            raise AssertionError('自定义画像不能覆盖内置评分标记')

        legal_custom.pop('_builtin_legal')
        legal_custom['industry'] = '医疗服务'
        path.write_text(json.dumps(legal_custom, ensure_ascii=False), encoding='utf-8')
        try:
            load_profile(industry='legal', profile_path=path)
        except ValueError:
            pass
        else:
            raise AssertionError('自定义画像的行业不能与命令行选择冲突')

    try:
        load_profile()
    except ValueError:
        pass
    else:
        raise AssertionError('缺少行业时必须拒绝静默评分')
    print(f'通过 {len(cases)} 条内置画像样例及自定义画像检查')
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
