# ChatGPT 结构化字段与数据

- 生成时间：2026-07-20T23:40:32.069085+00:00
- 输入文件：chatgpt-crawl.json
- 目标实体：豆包
- 实体类型：产品

本文件保存分析阶段从原始 ChatGPT JSON 中清洗出的结构化字段和对应数据，表结构与同目录 Excel 文件保持一致。

## 输出文件

本次分析产物清单。

- 行数：6

| file_type | path | description |
| --- | --- | --- |
| raw_json | ../chatgpt-crawl.json | 抓取阶段原始聚合 JSON 日志 |
| summary_json | report/summary.json | 分析阶段机器可读 summary JSON |
| structured_markdown | report/structured-data.md | 结构化字段与数据 Markdown |
| structured_excel | omitted-public-example/structured-data.xlsx | 结构化字段与数据 Excel |
| html_report | report/report.html | 正式可视化诊断分析报告 |
| semantic_review_cache | omitted-public-example/semantic-review-cache.json | 语义复核缓存 JSON |

## 概览字段

采样、实体、信源和报告级核心字段。

- 行数：26

| field | value | description |
| --- | --- | --- |
| generated_at | 2026-07-20T23:40:32.069085+00:00 | 分析生成时间 |
| input_file | chatgpt-crawl.json | 输入原始 JSON 文件名 |
| target_entity | 豆包 | 目标实体 |
| target_aliases | 豆包、Doubao、豆包大模型、豆包模型 | 目标实体别名 |
| entity_type | product | 目标实体类型 |
| entity_type_label | 产品 | 目标实体类型中文 |
| brand_source | target_entity | 实体来源口径 |
| semantic_review_mode | auto | 语义复核模式 |
| semantic_review_status | fallback | 语义复核状态 |
| semantic_review_source | heuristic | 语义复核来源 |
| semantic_confidence_threshold | 0.72 | AI 语义复核竞品准入阈值 |
| planned_samples | 15 | 计划采样次数 |
| completed_samples | 15 | 已完成采样次数 |
| valid_samples | 15 | 有效采样次数 |
| failed_samples | 0 | 失败采样次数 |
| pending_samples | 0 | 未完成采样次数 |
| valid_rate | 1.0 | 有效采样率 |
| completion_rate | 1.0 | 完成率 |
| question_count | 5 | 关键词/问题数量 |
| answer_chars | 50362 | 有效回答总字数 |
| reference_count | 196 | ChatGPT 引用信源总数 |
| unique_urls | 105 | 唯一 URL 数 |
| unique_domains | 79 | 唯一域名数 |
| competitor_count | 14 | 同类型竞品数量 |
| entity_candidate_count | 170 | 实体识别候选总数 |
| report_item_limit | 10 | HTML 报告默认明细上限 |

## 问题采集

每个关键词/问题的采集覆盖情况。

- 行数：5

| question_id | question | planned | completed | valid | failed | pending | valid_rate | reference_count | avg_references | answer_chars | avg_answer_chars |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| q01 | 国内目前最值得关注的大模型有哪些？ | 3 | 3 | 3 | 0 | 0 | 1.0 | 42 | 14.0 | 10220 | 3406.6666666666665 |
| q02 | 中国大模型排名前十的公司和产品分别是什么？ | 3 | 3 | 3 | 0 | 0 | 1.0 | 38 | 12.666666666666666 | 10297 | 3432.3333333333335 |
| q03 | 现在国产大模型里，哪些模型的推理和代码能力最强？ | 3 | 3 | 3 | 0 | 0 | 1.0 | 41 | 13.666666666666666 | 10586 | 3528.6666666666665 |
| q04 | 国产大模型主要可以分为哪些类型，各自适合什么场景？ | 3 | 3 | 3 | 0 | 0 | 1.0 | 36 | 12.0 | 9067 | 3022.3333333333335 |
| q05 | 如果企业要接入国产大模型，应该优先选择哪些模型？ | 3 | 3 | 3 | 0 | 0 | 1.0 | 39 | 13.0 | 10192 | 3397.3333333333335 |

## 目标实体指标

目标实体的核心诊断指标。

- 行数：1

| entity | role | entity_type | aliases | mentioned_samples | mention_rate | mention_total | avg_mentions_per_sample | avg_mentions_per_mentioned_sample | top1_samples | top1_rate | top3_samples | top3_rate | top5_samples | top5_rate | average_rank | dominant_sentiment | negative_rate | sentiment_total | sentiment_counts | reference_mentions | reference_domain_count | reference_url_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 豆包 | target | product | 豆包、Doubao、豆包大模型、豆包模型 | 11 | 0.7333333333333333 | 43 | 2.8666666666666667 | 3.909090909090909 | 0 | 0.0 | 4 | 0.26666666666666666 | 6 | 0.4 | 4.909090909090909 | positive | 0.0 | 11 | {"positive": 11} | 27 | 12 | 12 |

## 同类型实体对比

目标实体与同类型竞品的指标矩阵。

- 行数：10

| entity | role | entity_type | aliases | mentioned_samples | mention_rate | mention_total | avg_mentions_per_sample | top1_rate | top3_rate | top5_rate | average_rank | dominant_sentiment | negative_rate | reference_mentions | gap_vs_target_top3 | gap_vs_target_top5 | avg_mentions_per_mentioned_sample | top1_samples | top3_samples | top5_samples | sentiment_counts | sentiment_total | reference_domain_count | reference_url_count |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 豆包 | target | product | 豆包、Doubao、豆包大模型、豆包模型 | 11 | 0.7333333333333333 | 43 | 2.8666666666666667 | 0.0 | 0.26666666666666666 | 0.4 | 4.909090909090909 | positive | 0.0 | 27 | 0.0 | 0.0 | 3.909090909090909 | 0 | 4 | 6 | {"positive": 11} | 11 | 12 | 12 |
| 通义千问 | competitor | product | 通义千问、Qwen、千问、Qwen3、Qwen2.5 | 15 | 1.0 | 154 | 10.266666666666667 | 0.4666666666666667 | 0.9333333333333333 | 1.0 | 1.7333333333333334 | positive | 0.0 | 65 | 0.6666666666666667 | 0.6 | 10.266666666666667 | 7 | 14 | 15 | {"positive": 15} | 15 | 26 | 29 |
| DeepSeek | competitor | product | DeepSeek、DeepSeek-V3、DeepSeek-R1、深度求索 | 15 | 1.0 | 130 | 8.666666666666666 | 0.4666666666666667 | 0.6 | 0.9333333333333333 | 2.7333333333333334 | positive | 0.0 | 64 | 0.3333333333333333 | 0.5333333333333333 | 8.666666666666666 | 7 | 9 | 14 | {"neutral": 1, "positive": 14} | 15 | 26 | 30 |
| 文心一言 | competitor | product | 文心一言、ERNIE Bot、文心大模型、ERNIE、ERNIE 4.5 | 14 | 0.9333333333333333 | 35 | 2.3333333333333335 | 0.06666666666666667 | 0.4666666666666667 | 0.6666666666666666 | 3.7857142857142856 | positive | 0.07142857142857142 | 19 | 0.2 | 0.2666666666666666 | 2.5 | 1 | 7 | 10 | {"negative": 1, "neutral": 1, "positive": 12} | 14 | 6 | 6 |
| GLM | competitor | product | GLM、智谱GLM、ChatGLM、GLM-4、GLM-4.5、智谱清言 | 15 | 1.0 | 102 | 6.8 | 0.0 | 0.3333333333333333 | 0.6 | 4.666666666666667 | positive | 0.0 | 42 | 0.06666666666666665 | 0.19999999999999996 | 6.8 | 0 | 5 | 9 | {"neutral": 1, "positive": 14} | 15 | 18 | 19 |
| Kimi | competitor | product | Kimi、Kimi K2、Kimi大模型、Moonshot Kimi | 14 | 0.9333333333333333 | 63 | 4.2 | 0.0 | 0.26666666666666666 | 0.8 | 4.357142857142857 | positive | 0.0 | 58 | 0.0 | 0.4 | 4.5 | 0 | 4 | 12 | {"positive": 14} | 14 | 23 | 25 |
| 混元 | competitor | product | 混元、腾讯混元、Hunyuan | 10 | 0.6666666666666666 | 32 | 2.1333333333333333 | 0.0 | 0.13333333333333333 | 0.3333333333333333 | 5.5 | positive | 0.0 | 2 | -0.13333333333333333 | -0.06666666666666671 | 3.2 | 0 | 2 | 5 | {"positive": 10} | 10 | 1 | 1 |
| MiniMax | competitor | product | MiniMax、abab、海螺AI、海螺大模型 | 9 | 0.6 | 24 | 1.6 | 0.0 | 0.0 | 0.0 | 7.555555555555555 | positive | 0.0 | 13 | -0.26666666666666666 | -0.4 | 2.6666666666666665 | 0 | 0 | 0 | {"neutral": 3, "positive": 6} | 9 | 5 | 6 |
| 讯飞星火 | competitor | product | 讯飞星火、星火大模型、SparkDesk、iFlytek Spark | 3 | 0.2 | 5 | 0.3333333333333333 | 0.0 | 0.0 | 0.0 | 9.0 | positive | 0.0 | 0 | -0.26666666666666666 | -0.4 | 1.6666666666666667 | 0 | 0 | 0 | {"positive": 3} | 3 | 0 | 0 |
| 盘古大模型 | competitor | product | 盘古大模型、盘古、Pangu | 3 | 0.2 | 8 | 0.5333333333333333 | 0.0 | 0.0 | 0.06666666666666667 | 6.666666666666667 | positive | 0.0 | 0 | -0.26666666666666666 | -0.33333333333333337 | 2.6666666666666665 | 0 | 0 | 1 | {"positive": 3} | 3 | 0 | 0 |

## 问题实体明细

每个问题下各实体的表现。

- 行数：75

| question_id | question | entity | mentioned_samples | mention_rate | avg_mentions_per_sample | top1_rate | top3_rate | top5_rate | average_rank |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| q01 | 国内目前最值得关注的大模型有哪些？ | 豆包 | 3 | 1.0 | 3.0 | 0.0 | 0.3333333333333333 | 0.3333333333333333 | 6.0 |
| q01 | 国内目前最值得关注的大模型有哪些？ | 通义千问 | 3 | 1.0 | 9.0 | 0.6666666666666666 | 1.0 | 1.0 | 1.3333333333333333 |
| q01 | 国内目前最值得关注的大模型有哪些？ | 文心一言 | 3 | 1.0 | 3.6666666666666665 | 0.0 | 0.6666666666666666 | 1.0 | 3.0 |
| q01 | 国内目前最值得关注的大模型有哪些？ | DeepSeek | 3 | 1.0 | 7.333333333333333 | 0.3333333333333333 | 0.3333333333333333 | 1.0 | 3.0 |
| q01 | 国内目前最值得关注的大模型有哪些？ | Kimi | 3 | 1.0 | 4.333333333333333 | 0.0 | 0.3333333333333333 | 1.0 | 4.333333333333333 |
| q01 | 国内目前最值得关注的大模型有哪些？ | 讯飞星火 | 0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |  |
| q01 | 国内目前最值得关注的大模型有哪些？ | 混元 | 3 | 1.0 | 3.0 | 0.0 | 0.3333333333333333 | 0.3333333333333333 | 5.666666666666667 |
| q01 | 国内目前最值得关注的大模型有哪些？ | GLM | 3 | 1.0 | 7.0 | 0.0 | 0.0 | 0.3333333333333333 | 5.333333333333333 |
| q01 | 国内目前最值得关注的大模型有哪些？ | 商汤日日新 | 0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |  |
| q01 | 国内目前最值得关注的大模型有哪些？ | 百川智能 | 1 | 0.3333333333333333 | 0.6666666666666666 | 0.0 | 0.0 | 0.0 | 9.0 |
| q01 | 国内目前最值得关注的大模型有哪些？ | MiniMax | 3 | 1.0 | 2.6666666666666665 | 0.0 | 0.0 | 0.0 | 7.333333333333333 |
| q01 | 国内目前最值得关注的大模型有哪些？ | 阶跃星辰 | 0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |  |
| q01 | 国内目前最值得关注的大模型有哪些？ | 书生浦语 | 0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |  |
| q01 | 国内目前最值得关注的大模型有哪些？ | 盘古大模型 | 0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |  |
| q01 | 国内目前最值得关注的大模型有哪些？ | Yi | 1 | 0.3333333333333333 | 0.3333333333333333 | 0.0 | 0.0 | 0.0 | 10.0 |
| q02 | 中国大模型排名前十的公司和产品分别是什么？ | 豆包 | 3 | 1.0 | 3.3333333333333335 | 0.0 | 0.6666666666666666 | 1.0 | 3.0 |
| q02 | 中国大模型排名前十的公司和产品分别是什么？ | 通义千问 | 3 | 1.0 | 5.666666666666667 | 1.0 | 1.0 | 1.0 | 1.0 |
| q02 | 中国大模型排名前十的公司和产品分别是什么？ | 文心一言 | 3 | 1.0 | 2.0 | 0.0 | 0.6666666666666666 | 0.6666666666666666 | 3.6666666666666665 |
| q02 | 中国大模型排名前十的公司和产品分别是什么？ | DeepSeek | 3 | 1.0 | 4.666666666666667 | 0.0 | 0.3333333333333333 | 0.6666666666666666 | 4.666666666666667 |
| q02 | 中国大模型排名前十的公司和产品分别是什么？ | Kimi | 3 | 1.0 | 3.0 | 0.0 | 0.0 | 0.3333333333333333 | 5.666666666666667 |
| q02 | 中国大模型排名前十的公司和产品分别是什么？ | 讯飞星火 | 2 | 0.6666666666666666 | 1.0 | 0.0 | 0.0 | 0.0 | 10.0 |
| q02 | 中国大模型排名前十的公司和产品分别是什么？ | 混元 | 3 | 1.0 | 3.0 | 0.0 | 0.3333333333333333 | 0.6666666666666666 | 4.333333333333333 |
| q02 | 中国大模型排名前十的公司和产品分别是什么？ | GLM | 3 | 1.0 | 3.0 | 0.0 | 0.0 | 0.3333333333333333 | 6.666666666666667 |
| q02 | 中国大模型排名前十的公司和产品分别是什么？ | 商汤日日新 | 0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |  |
| q02 | 中国大模型排名前十的公司和产品分别是什么？ | 百川智能 | 1 | 0.3333333333333333 | 1.3333333333333333 | 0.0 | 0.0 | 0.0 | 9.0 |
| q02 | 中国大模型排名前十的公司和产品分别是什么？ | MiniMax | 3 | 1.0 | 2.3333333333333335 | 0.0 | 0.0 | 0.0 | 8.666666666666666 |
| q02 | 中国大模型排名前十的公司和产品分别是什么？ | 阶跃星辰 | 0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |  |
| q02 | 中国大模型排名前十的公司和产品分别是什么？ | 书生浦语 | 0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |  |
| q02 | 中国大模型排名前十的公司和产品分别是什么？ | 盘古大模型 | 2 | 0.6666666666666666 | 2.0 | 0.0 | 0.0 | 0.3333333333333333 | 6.5 |
| q02 | 中国大模型排名前十的公司和产品分别是什么？ | Yi | 0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |  |
| q03 | 现在国产大模型里，哪些模型的推理和代码能力最强？ | 豆包 | 1 | 0.3333333333333333 | 0.6666666666666666 | 0.0 | 0.0 | 0.0 | 6.0 |
| q03 | 现在国产大模型里，哪些模型的推理和代码能力最强？ | 通义千问 | 3 | 1.0 | 13.333333333333334 | 0.0 | 1.0 | 1.0 | 2.3333333333333335 |
| q03 | 现在国产大模型里，哪些模型的推理和代码能力最强？ | 文心一言 | 2 | 0.6666666666666666 | 1.3333333333333333 | 0.0 | 0.0 | 0.3333333333333333 | 5.5 |
| q03 | 现在国产大模型里，哪些模型的推理和代码能力最强？ | DeepSeek | 3 | 1.0 | 13.666666666666666 | 1.0 | 1.0 | 1.0 | 1.0 |
| q03 | 现在国产大模型里，哪些模型的推理和代码能力最强？ | Kimi | 3 | 1.0 | 4.333333333333333 | 0.0 | 0.6666666666666666 | 1.0 | 3.6666666666666665 |
| q03 | 现在国产大模型里，哪些模型的推理和代码能力最强？ | 讯飞星火 | 0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |  |
| q03 | 现在国产大模型里，哪些模型的推理和代码能力最强？ | 混元 | 2 | 0.6666666666666666 | 1.6666666666666667 | 0.0 | 0.0 | 0.3333333333333333 | 6.5 |
| q03 | 现在国产大模型里，哪些模型的推理和代码能力最强？ | GLM | 3 | 1.0 | 9.0 | 0.0 | 0.3333333333333333 | 0.6666666666666666 | 4.333333333333333 |
| q03 | 现在国产大模型里，哪些模型的推理和代码能力最强？ | 商汤日日新 | 0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |  |
| q03 | 现在国产大模型里，哪些模型的推理和代码能力最强？ | 百川智能 | 0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |  |
| q03 | 现在国产大模型里，哪些模型的推理和代码能力最强？ | MiniMax | 1 | 0.3333333333333333 | 1.0 | 0.0 | 0.0 | 0.0 | 6.0 |
| q03 | 现在国产大模型里，哪些模型的推理和代码能力最强？ | 阶跃星辰 | 1 | 0.3333333333333333 | 0.3333333333333333 | 0.0 | 0.0 | 0.3333333333333333 | 4.0 |
| q03 | 现在国产大模型里，哪些模型的推理和代码能力最强？ | 书生浦语 | 0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |  |
| q03 | 现在国产大模型里，哪些模型的推理和代码能力最强？ | 盘古大模型 | 0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |  |
| q03 | 现在国产大模型里，哪些模型的推理和代码能力最强？ | Yi | 0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |  |
| q04 | 国产大模型主要可以分为哪些类型，各自适合什么场景？ | 豆包 | 2 | 0.6666666666666666 | 3.0 | 0.0 | 0.0 | 0.0 | 6.5 |
| q04 | 国产大模型主要可以分为哪些类型，各自适合什么场景？ | 通义千问 | 3 | 1.0 | 9.666666666666666 | 0.6666666666666666 | 1.0 | 1.0 | 1.3333333333333333 |
| q04 | 国产大模型主要可以分为哪些类型，各自适合什么场景？ | 文心一言 | 3 | 1.0 | 1.6666666666666667 | 0.3333333333333333 | 1.0 | 1.0 | 1.6666666666666667 |
| q04 | 国产大模型主要可以分为哪些类型，各自适合什么场景？ | DeepSeek | 3 | 1.0 | 6.666666666666667 | 0.0 | 0.3333333333333333 | 1.0 | 4.0 |
| q04 | 国产大模型主要可以分为哪些类型，各自适合什么场景？ | Kimi | 2 | 0.6666666666666666 | 3.0 | 0.0 | 0.0 | 0.6666666666666666 | 4.5 |
| q04 | 国产大模型主要可以分为哪些类型，各自适合什么场景？ | 讯飞星火 | 1 | 0.3333333333333333 | 0.6666666666666666 | 0.0 | 0.0 | 0.0 | 7.0 |
| q04 | 国产大模型主要可以分为哪些类型，各自适合什么场景？ | 混元 | 0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |  |
| q04 | 国产大模型主要可以分为哪些类型，各自适合什么场景？ | GLM | 3 | 1.0 | 4.0 | 0.0 | 0.6666666666666666 | 1.0 | 3.3333333333333335 |
| q04 | 国产大模型主要可以分为哪些类型，各自适合什么场景？ | 商汤日日新 | 0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |  |
| q04 | 国产大模型主要可以分为哪些类型，各自适合什么场景？ | 百川智能 | 0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |  |
| q04 | 国产大模型主要可以分为哪些类型，各自适合什么场景？ | MiniMax | 2 | 0.6666666666666666 | 2.0 | 0.0 | 0.0 | 0.0 | 7.0 |
| q04 | 国产大模型主要可以分为哪些类型，各自适合什么场景？ | 阶跃星辰 | 0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |  |
| q04 | 国产大模型主要可以分为哪些类型，各自适合什么场景？ | 书生浦语 | 0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |  |
| q04 | 国产大模型主要可以分为哪些类型，各自适合什么场景？ | 盘古大模型 | 0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |  |
| q04 | 国产大模型主要可以分为哪些类型，各自适合什么场景？ | Yi | 0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |  |
| q05 | 如果企业要接入国产大模型，应该优先选择哪些模型？ | 豆包 | 2 | 0.6666666666666666 | 4.333333333333333 | 0.0 | 0.3333333333333333 | 0.6666666666666666 | 4.0 |
| q05 | 如果企业要接入国产大模型，应该优先选择哪些模型？ | 通义千问 | 3 | 1.0 | 13.666666666666666 | 0.0 | 0.6666666666666666 | 1.0 | 2.6666666666666665 |
| q05 | 如果企业要接入国产大模型，应该优先选择哪些模型？ | 文心一言 | 3 | 1.0 | 3.0 | 0.0 | 0.0 | 0.3333333333333333 | 5.666666666666667 |
| q05 | 如果企业要接入国产大模型，应该优先选择哪些模型？ | DeepSeek | 3 | 1.0 | 11.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| q05 | 如果企业要接入国产大模型，应该优先选择哪些模型？ | Kimi | 3 | 1.0 | 6.333333333333333 | 0.0 | 0.3333333333333333 | 1.0 | 3.6666666666666665 |
| q05 | 如果企业要接入国产大模型，应该优先选择哪些模型？ | 讯飞星火 | 0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |  |
| q05 | 如果企业要接入国产大模型，应该优先选择哪些模型？ | 混元 | 2 | 0.6666666666666666 | 3.0 | 0.0 | 0.0 | 0.3333333333333333 | 6.0 |
| q05 | 如果企业要接入国产大模型，应该优先选择哪些模型？ | GLM | 3 | 1.0 | 11.0 | 0.0 | 0.6666666666666666 | 0.6666666666666666 | 3.6666666666666665 |
| q05 | 如果企业要接入国产大模型，应该优先选择哪些模型？ | 商汤日日新 | 0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |  |
| q05 | 如果企业要接入国产大模型，应该优先选择哪些模型？ | 百川智能 | 0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |  |
| q05 | 如果企业要接入国产大模型，应该优先选择哪些模型？ | MiniMax | 0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |  |
| q05 | 如果企业要接入国产大模型，应该优先选择哪些模型？ | 阶跃星辰 | 0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |  |
| q05 | 如果企业要接入国产大模型，应该优先选择哪些模型？ | 书生浦语 | 0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |  |
| q05 | 如果企业要接入国产大模型，应该优先选择哪些模型？ | 盘古大模型 | 1 | 0.3333333333333333 | 0.6666666666666666 | 0.0 | 0.0 | 0.0 | 7.0 |
| q05 | 如果企业要接入国产大模型，应该优先选择哪些模型？ | Yi | 0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |  |

## 实体识别候选

实体识别、清洗、过滤、语义复核和分类候选。

- 行数：170

| name | kind | role | entity_type | is_target | entered_competitor_matrix | semantic_label | semantic_is_same_type | semantic_is_direct_competitor | semantic_confidence | semantic_source | semantic_recommended_action | semantic_reason | confidence | sample_count | raw_count | evidence_score | surface_score | surface_reasons | reasons | aliases | evidence | metric_mentioned_samples | metric_mention_rate | metric_mention_total | metric_avg_mentions_per_sample | metric_top1_rate | metric_top3_rate | metric_top5_rate | metric_average_rank | metric_dominant_sentiment | metric_negative_rate | metric_reference_mentions |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 通义千问 | product | competitor | product | TRUE | TRUE | direct_competitor | TRUE | TRUE | 0.9 | heuristic | include_competitor | 候选项来自人工实体别名表，并在正文回答中有明确命中。 | 0.95 | 15 | 18 | 12.0 | 3 | 产品品牌形态 | 用户提供或进入指标计算的实体、匹配目标类型：product | Qwen、千问、Qwen3、Qwen2.5 | {"answer_alias_match": 15, "person_alias": 3, "provided_or_metric_entity": 1} | 15 | 1.0 | 154 | 10.266666666666667 | 0.4666666666666667 | 0.9333333333333333 | 1.0 | 1.7333333333333334 | positive | 0.0 | 65 |
| DeepSeek | product | competitor | product | TRUE | TRUE | direct_competitor | TRUE | TRUE | 0.9 | heuristic | include_competitor | 候选项来自人工实体别名表，并在正文回答中有明确命中。 | 0.95 | 15 | 16 | 10.0 | 0 | 属性、泛称或噪声短语 | 用户提供或进入指标计算的实体、匹配目标类型：product | DeepSeek-V3、DeepSeek-R1、深度求索 | {"answer_alias_match": 15, "provided_or_metric_entity": 1} | 15 | 1.0 | 130 | 8.666666666666666 | 0.4666666666666667 | 0.6 | 0.9333333333333333 | 2.7333333333333334 | positive | 0.0 | 64 |
| 文心一言 | product | competitor | product | TRUE | TRUE | direct_competitor | TRUE | TRUE | 0.9 | heuristic | include_competitor | 候选项来自人工实体别名表，并在正文回答中有明确命中。 | 0.95 | 14 | 16 | 12.0 | 3 | 产品品牌形态 | 用户提供或进入指标计算的实体、匹配目标类型：product | ERNIE、ERNIE Bot、文心大模型、ERNIE 4.5 | {"answer_alias_match": 14, "person_alias": 2, "provided_or_metric_entity": 1} | 14 | 0.9333333333333333 | 35 | 2.3333333333333335 | 0.06666666666666667 | 0.4666666666666667 | 0.6666666666666666 | 3.7857142857142856 | positive | 0.07142857142857142 | 19 |
| GLM | product | competitor | product | TRUE | TRUE | direct_competitor | TRUE | TRUE | 0.9 | heuristic | include_competitor | 候选项来自人工实体别名表，并在正文回答中有明确命中。 | 0.95 | 15 | 16 | 10.0 | 3 | 产品品牌形态 | 用户提供或进入指标计算的实体、匹配目标类型：product | 智谱GLM、ChatGLM、GLM-4、GLM-4.5、智谱清言 | {"answer_alias_match": 15, "provided_or_metric_entity": 1} | 15 | 1.0 | 102 | 6.8 | 0.0 | 0.3333333333333333 | 0.6 | 4.666666666666667 | positive | 0.0 | 42 |
| Kimi | product | competitor | product | TRUE | TRUE | direct_competitor | TRUE | TRUE | 0.9 | heuristic | include_competitor | 候选项来自人工实体别名表，并在正文回答中有明确命中。 | 0.95 | 14 | 15 | 10.0 | 0 | 属性、泛称或噪声短语 | 用户提供或进入指标计算的实体、匹配目标类型：product | Kimi K2、Kimi大模型、Moonshot Kimi | {"answer_alias_match": 14, "provided_or_metric_entity": 1} | 14 | 0.9333333333333333 | 63 | 4.2 | 0.0 | 0.26666666666666666 | 0.8 | 4.357142857142857 | positive | 0.0 | 58 |
| 豆包 | product | target | product | TRUE | FALSE | target_alias | TRUE | FALSE | 0.96 | heuristic | merge_target_alias | 候选项与目标实体或目标别名匹配。 | 0.95 | 11 | 15 | 12.0 | 3 | 产品品牌形态 | 用户提供或进入指标计算的实体、匹配目标类型：product | Doubao、豆包大模型、豆包模型 | {"answer_alias_match": 11, "person_alias": 4, "provided_or_metric_entity": 1} | 11 | 0.7333333333333333 | 43 | 2.8666666666666667 | 0.0 | 0.26666666666666666 | 0.4 | 4.909090909090909 | positive | 0.0 | 27 |
| 混元 | product | competitor | product | TRUE | TRUE | direct_competitor | TRUE | TRUE | 0.9 | heuristic | include_competitor | 候选项来自人工实体别名表，并在正文回答中有明确命中。 | 0.95 | 10 | 12 | 12.0 | 3 | 产品品牌形态 | 用户提供或进入指标计算的实体、匹配目标类型：product | Tencent Hunyuan、Hunyuan、腾讯混元 | {"answer_alias_match": 10, "person_alias": 2, "provided_or_metric_entity": 1} | 10 | 0.6666666666666666 | 32 | 2.1333333333333333 | 0.0 | 0.13333333333333333 | 0.3333333333333333 | 5.5 | positive | 0.0 | 2 |
| 盘古大模型 | product | competitor | product | TRUE | TRUE | direct_competitor | TRUE | TRUE | 0.9 | heuristic | include_competitor | 候选项来自人工实体别名表，并在正文回答中有明确命中。 | 0.95 | 3 | 4 | 9.2 | 3 | 产品品牌形态 | 用户提供或进入指标计算的实体、匹配目标类型：product | 盘古、Pangu | {"answer_alias_match": 3, "provided_or_metric_entity": 1} | 3 | 0.2 | 8 | 0.5333333333333333 | 0.0 | 0.0 | 0.06666666666666667 | 6.666666666666667 | positive | 0.0 | 0 |
| 阶跃星辰 | product | competitor | product | TRUE | TRUE | direct_competitor | TRUE | TRUE | 0.9 | heuristic | include_competitor | 候选项来自人工实体别名表，并在正文回答中有明确命中。 | 0.95 | 1 | 2 | 8.4 | 3 | 产品品牌形态 | 用户提供或进入指标计算的实体、匹配目标类型：product | Step、Step-2、Step系列模型 | {"answer_alias_match": 1, "provided_or_metric_entity": 1} | 1 | 0.06666666666666667 | 1 | 0.06666666666666667 | 0.0 | 0.0 | 0.06666666666666667 | 4.0 | positive | 0.0 | 2 |
| MiniMax | product | competitor | product | TRUE | TRUE | direct_competitor | TRUE | TRUE | 0.9 | heuristic | include_competitor | 候选项来自人工实体别名表，并在正文回答中有明确命中。 | 0.95 | 9 | 10 | 10.0 | 3 | 产品品牌形态 | 用户提供或进入指标计算的实体、匹配目标类型：product | abab、海螺AI、海螺大模型 | {"answer_alias_match": 9, "provided_or_metric_entity": 1} | 9 | 0.6 | 24 | 1.6 | 0.0 | 0.0 | 0.0 | 7.555555555555555 | positive | 0.0 | 13 |
| 讯飞星火 | product | competitor | product | TRUE | TRUE | direct_competitor | TRUE | TRUE | 0.9 | heuristic | include_competitor | 候选项来自人工实体别名表，并在正文回答中有明确命中。 | 0.95 | 3 | 4 | 9.2 | 3 | 产品品牌形态 | 用户提供或进入指标计算的实体、匹配目标类型：product | 星火大模型、SparkDesk、iFlytek Spark | {"answer_alias_match": 3, "provided_or_metric_entity": 1} | 3 | 0.2 | 5 | 0.3333333333333333 | 0.0 | 0.0 | 0.0 | 9.0 | positive | 0.0 | 0 |
| 百川智能 | product | competitor | product | TRUE | TRUE | direct_competitor | TRUE | TRUE | 0.9 | heuristic | include_competitor | 候选项来自人工实体别名表，并在正文回答中有明确命中。 | 0.95 | 2 | 6 | 12.8 | 1 |  | 用户提供或进入指标计算的实体、匹配目标类型：product | Baichuan、Baichuan2 | {"answer_alias_match": 2, "org_suffix": 2, "person_alias": 2, "provided_or_metric_entity": 1} | 2 | 0.13333333333333333 | 6 | 0.4 | 0.0 | 0.0 | 0.0 | 9.0 | neutral | 0.0 | 0 |
| Yi | product | competitor | product | TRUE | TRUE | direct_competitor | TRUE | TRUE | 0.9 | heuristic | include_competitor | 候选项来自人工实体别名表，并在正文回答中有明确命中。 | 0.95 | 1 | 2 | 8.4 | 3 | 产品品牌形态 | 用户提供或进入指标计算的实体、匹配目标类型：product | 零一万物、Yi-Large、Yi系列模型 | {"answer_alias_match": 1, "provided_or_metric_entity": 1} | 1 | 0.06666666666666667 | 1 | 0.06666666666666667 | 0.0 | 0.0 | 0.0 | 10.0 | positive | 0.0 | 0 |
| 智谱AI | product | candidate | product | TRUE | FALSE | direct_competitor | TRUE | TRUE | 0.95 | heuristic | include_competitor | 候选项与目标实体类型一致，且有正文证据、实体形态和重复样本支撑。 | 0.95 | 5 | 5 | 4.0 | 4 | 产品类后缀、中英混合品牌形态 | 带产品/工具/平台类后缀、匹配目标类型：product |  | {"org_suffix": 5} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 商汤日日新 | product | competitor | product | TRUE | TRUE | direct_competitor | TRUE | TRUE | 0.95 | heuristic | include_competitor | 候选项与目标实体类型一致，且有正文证据、实体形态和重复样本支撑。 | 0.95 | 0 | 1 | 5.0 | 3 | 产品品牌形态 | 用户提供或进入指标计算的实体、匹配目标类型：product | 日日新、SenseNova | {"provided_or_metric_entity": 1} | 0 | 0.0 | 0 | 0.0 | 0.0 | 0.0 | 0.0 |  | neutral | 0.0 | 0 |
| 书生浦语 | product | competitor | product | TRUE | TRUE | direct_competitor | TRUE | TRUE | 0.95 | heuristic | include_competitor | 候选项与目标实体类型一致，且有正文证据、实体形态和重复样本支撑。 | 0.95 | 0 | 1 | 5.0 | 3 | 产品品牌形态 | 用户提供或进入指标计算的实体、匹配目标类型：product | InternLM | {"provided_or_metric_entity": 1} | 0 | 0.0 | 0 | 0.0 | 0.0 | 0.0 | 0.0 |  | neutral | 0.0 | 0 |
| Presenc AI | product | candidate | product | TRUE | FALSE | direct_competitor | TRUE | TRUE | 0.94 | heuristic | include_competitor | 候选项与目标实体类型一致，且有正文证据、实体形态和重复样本支撑。 | 0.94 | 6 | 10 | 4.0 | 3 | 产品类后缀 | 带产品/工具/平台类后缀、匹配目标类型：product |  | {"english_brand_like": 10} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| Moonshot AI | product | candidate | product | TRUE | FALSE | direct_competitor | TRUE | TRUE | 0.94 | heuristic | include_competitor | 候选项与目标实体类型一致，且有正文证据、实体形态和重复样本支撑。 | 0.94 | 5 | 5 | 4.0 | 3 | 产品类后缀 | 带产品/工具/平台类后缀、匹配目标类型：product |  | {"english_brand_like": 5} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| RadarAI | product | candidate | product | TRUE | FALSE | direct_competitor | TRUE | TRUE | 0.94 | heuristic | include_competitor | 候选项与目标实体类型一致，且有正文证据、实体形态和重复样本支撑。 | 0.94 | 3 | 5 | 3.7 | 3 | 产品品牌形态 | 带产品/工具/平台类后缀、匹配目标类型：product |  | {"english_brand_like": 1, "org_suffix": 1, "source_title_org": 3} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 百度 | product | candidate | product | TRUE | FALSE | direct_competitor | TRUE | TRUE | 0.86 | heuristic | include_competitor | 候选项与目标实体类型一致，且有正文证据、实体形态和重复样本支撑。 | 0.86 | 3 | 3 | 3.2 | 3 | 产品品牌形态 | 带产品/工具/平台类后缀、匹配目标类型：product | Baidu、ERNIE | {"person_alias": 3} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 深度求索 | product | candidate | product | TRUE | FALSE | direct_competitor | TRUE | TRUE | 0.86 | heuristic | include_competitor | 候选项与目标实体类型一致，且有正文证据、实体形态和重复样本支撑。 | 0.86 | 3 | 3 | 3.2 | 3 | 产品品牌形态 | 带产品/工具/平台类后缀、匹配目标类型：product | DeepSeek | {"person_alias": 3} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 月之暗面 | product | candidate | product | TRUE | FALSE | direct_competitor | TRUE | TRUE | 0.86 | heuristic | include_competitor | 候选项与目标实体类型一致，且有正文证据、实体形态和重复样本支撑。 | 0.86 | 3 | 3 | 3.2 | 3 | 产品品牌形态 | 带产品/工具/平台类后缀、匹配目标类型：product | Moonshot AI | {"person_alias": 3} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 阿里巴巴 | product | candidate | product | TRUE | FALSE | direct_competitor | TRUE | TRUE | 0.82 | heuristic | include_competitor | 候选项与目标实体类型一致，且有正文证据、实体形态和重复样本支撑。 | 0.82 | 2 | 2 | 2.8 | 3 | 产品品牌形态 | 带产品/工具/平台类后缀、匹配目标类型：product | Alibaba | {"person_alias": 2} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 腾讯 | product | candidate | product | TRUE | FALSE | direct_competitor | TRUE | TRUE | 0.82 | heuristic | include_competitor | 候选项与目标实体类型一致，且有正文证据、实体形态和重复样本支撑。 | 0.82 | 2 | 2 | 2.8 | 3 | 产品品牌形态 | 带产品/工具/平台类后缀、匹配目标类型：product | Tencent | {"person_alias": 2} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 字节跳动 | product | candidate | product | TRUE | FALSE | direct_competitor | TRUE | TRUE | 0.82 | heuristic | include_competitor | 候选项与目标实体类型一致，且有正文证据、实体形态和重复样本支撑。 | 0.82 | 2 | 2 | 2.8 | 3 | 产品品牌形态 | 带产品/工具/平台类后缀、匹配目标类型：product | ByteDance | {"person_alias": 2} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 混合 | product | candidate | product | TRUE | FALSE | direct_competitor | TRUE | TRUE | 0.82 | heuristic | include_competitor | 候选项与目标实体类型一致，且有正文证据、实体形态和重复样本支撑。 | 0.82 | 2 | 2 | 2.8 | 3 | 产品品牌形态 | 带产品/工具/平台类后缀、匹配目标类型：product |  | {"person_role_after": 2} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 模型 | product | candidate | product | TRUE | FALSE | target_alias | TRUE | FALSE | 0.96 | heuristic | merge_target_alias | 候选项与目标实体或目标别名匹配。 | 0.82 | 2 | 3 | 2.8 | 3 | 产品品牌形态 | 带产品/工具/平台类后缀、匹配目标类型：product | Mixture of Experts | {"person_alias": 1, "person_role_before": 2} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 你愿意 | product | candidate | product | TRUE | FALSE | direct_competitor | TRUE | TRUE | 0.82 | heuristic | include_competitor | 候选项与目标实体类型一致，且有正文证据、实体形态和重复样本支撑。 | 0.82 | 2 | 2 | 1.8 | 3 | 产品品牌形态 | 带产品/工具/平台类后缀、匹配目标类型：product |  | {"answer_heading": 2} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 国产AI | product | candidate | product | FALSE | FALSE | source_or_title | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项缺少正文回答证据，主要来自信源标题或来源信息。 | 0.95 | 5 | 5 | 2.5 | 4 | 产品类后缀、中英混合品牌形态 | 带产品/工具/平台类后缀 |  | {"source_title_org": 5} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 详细对比 | product | candidate | product | FALSE | FALSE | source_or_title | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项缺少正文回答证据，主要来自信源标题或来源信息。 | 0.95 | 4 | 4 | 2.1 | 3 | 产品品牌形态 | 带产品/工具/平台类后缀 |  | {"source_title_person": 4} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 人工智能6S服务平台 | product | candidate | product | FALSE | FALSE | source_or_title | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项缺少正文回答证据，主要来自信源标题或来源信息。 | 0.95 | 3 | 3 | 1.7 | 4 | 产品类后缀、中英混合品牌形态 | 带产品/工具/平台类后缀 |  | {"source_title_org": 3} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 2026年国产AI | product | candidate | product | FALSE | FALSE | source_or_title | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项缺少正文回答证据，主要来自信源标题或来源信息。 | 0.95 | 3 | 3 | 1.7 | 4 | 产品类后缀、中英混合品牌形态 | 带产品/工具/平台类后缀 |  | {"source_title_org": 3} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 太平洋科技 | company | candidate | company | FALSE | FALSE | source_or_title | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项缺少正文回答证据，主要来自信源标题或来源信息。 | 0.94 | 4 | 4 | 2.1 | 1 |  | 带机构/公司/平台类后缀 |  | {"source_title_org": 4} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 中国AI | product | candidate | product | FALSE | FALSE | source_or_title | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项缺少正文回答证据，主要来自信源标题或来源信息。 | 0.92 | 2 | 2 | 1.3 | 4 | 产品类后缀、中英混合品牌形态 | 带产品/工具/平台类后缀 |  | {"source_title_org": 2} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 2026年国内AI | product | candidate | product | FALSE | FALSE | source_or_title | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项缺少正文回答证据，主要来自信源标题或来源信息。 | 0.92 | 2 | 2 | 1.3 | 4 | 产品类后缀、中英混合品牌形态 | 带产品/工具/平台类后缀 |  | {"source_title_org": 2} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 横向评测 | product | candidate | product | FALSE | FALSE | source_or_title | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项缺少正文回答证据，主要来自信源标题或来源信息。 | 0.9 | 2 | 2 | 1.3 | 3 | 产品品牌形态 | 带产品/工具/平台类后缀 |  | {"source_title_person": 2} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| StarverseAI | product | candidate | product | FALSE | FALSE | source_or_title | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项缺少正文回答证据，主要来自信源标题或来源信息。 | 0.9 | 2 | 2 | 1.3 | 3 | 产品品牌形态 | 带产品/工具/平台类后缀 |  | {"source_title_org": 2} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 企业AI | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.88 | 3 | 3 | 3.2 | 4 | 产品类后缀、中英混合品牌形态 | 带产品/工具/平台类后缀 |  | {"org_suffix": 3} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 2026中国企业AI公司 | company | candidate | company | FALSE | FALSE | source_or_title | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项缺少正文回答证据，主要来自信源标题或来源信息。 | 0.88 | 2 | 2 | 1.3 | 2 | 中英混合品牌形态 | 带机构/公司/平台类后缀 |  | {"source_title_org": 2} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 2026国内AI | product | candidate | product | FALSE | FALSE | source_or_title | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项缺少正文回答证据，主要来自信源标题或来源信息。 | 0.88 | 1 | 1 | 0.9 | 4 | 产品类后缀、中英混合品牌形态 | 带产品/工具/平台类后缀 |  | {"source_title_org": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 国内外主流AI | product | candidate | product | FALSE | FALSE | source_or_title | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项缺少正文回答证据，主要来自信源标题或来源信息。 | 0.88 | 1 | 1 | 0.9 | 4 | 产品类后缀、中英混合品牌形态 | 带产品/工具/平台类后缀 |  | {"source_title_org": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 2026主流AI | product | candidate | product | FALSE | FALSE | source_or_title | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项缺少正文回答证据，主要来自信源标题或来源信息。 | 0.88 | 1 | 1 | 0.9 | 4 | 产品类后缀、中英混合品牌形态 | 带产品/工具/平台类后缀 |  | {"source_title_org": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 2024年中国AI | product | candidate | product | FALSE | FALSE | source_or_title | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项缺少正文回答证据，主要来自信源标题或来源信息。 | 0.88 | 1 | 1 | 0.9 | 4 | 产品类后缀、中英混合品牌形态 | 带产品/工具/平台类后缀 |  | {"source_title_org": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 北京朝阳AI | product | candidate | product | FALSE | FALSE | source_or_title | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项缺少正文回答证据，主要来自信源标题或来源信息。 | 0.88 | 1 | 1 | 0.9 | 4 | 产品类后缀、中英混合品牌形态 | 带产品/工具/平台类后缀 |  | {"source_title_org": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| Java开发者AI | product | candidate | product | FALSE | FALSE | source_or_title | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项缺少正文回答证据，主要来自信源标题或来源信息。 | 0.88 | 1 | 1 | 0.9 | 4 | 产品类后缀、中英混合品牌形态 | 带产品/工具/平台类后缀 |  | {"source_title_org": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 老达AI | product | candidate | product | FALSE | FALSE | source_or_title | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项缺少正文回答证据，主要来自信源标题或来源信息。 | 0.88 | 1 | 1 | 0.9 | 4 | 产品类后缀、中英混合品牌形态 | 带产品/工具/平台类后缀 |  | {"source_title_org": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| Zhipu AI | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.86 | 3 | 3 | 3.2 | 3 | 产品类后缀 | 带产品/工具/平台类后缀 |  | {"english_brand_like": 3} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 新浪科技 | company | candidate | company | FALSE | FALSE | source_or_title | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项缺少正文回答证据，主要来自信源标题或来源信息。 | 0.86 | 2 | 2 | 1.3 | 1 |  | 带机构/公司/平台类后缀 |  | {"source_title_org": 2} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 元大模型 | person | candidate | person | FALSE | FALSE | unrelated_entity | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项与目标实体类型不一致。 | 0.86 | 2 | 2 | 2.8 | 3 | 产品品牌形态 | 中文姓名且邻近专家职务或来源标题 | Hunyuan | {"person_alias": 2} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 简米科技 | company | candidate | company | FALSE | FALSE | source_or_title | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项缺少正文回答证据，主要来自信源标题或来源信息。 | 0.86 | 2 | 2 | 1.3 | 1 |  | 带机构/公司/平台类后缀 |  | {"source_title_org": 2} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 2026福布斯中国人工智能科技 | company | candidate | company | FALSE | FALSE | source_or_title | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项缺少正文回答证据，主要来自信源标题或来源信息。 | 0.86 | 2 | 2 | 1.3 | 1 |  | 带机构/公司/平台类后缀 |  | {"source_title_org": 2} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 能力排行 | product | candidate | product | FALSE | FALSE | source_or_title | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项缺少正文回答证据，主要来自信源标题或来源信息。 | 0.86 | 1 | 1 | 0.9 | 3 | 产品品牌形态 | 带产品/工具/平台类后缀 |  | {"source_title_person": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 市场格局 | product | candidate | product | FALSE | FALSE | source_or_title | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项缺少正文回答证据，主要来自信源标题或来源信息。 | 0.86 | 1 | 1 | 0.9 | 3 | 产品品牌形态 | 带产品/工具/平台类后缀 |  | {"source_title_person": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 产业发展 | product | candidate | product | FALSE | FALSE | source_or_title | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项缺少正文回答证据，主要来自信源标题或来源信息。 | 0.86 | 1 | 1 | 0.9 | 3 | 产品品牌形态 | 带产品/工具/平台类后缀 |  | {"source_title_person": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 模型分类 | product | candidate | product | FALSE | FALSE | source_or_title | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项缺少正文回答证据，主要来自信源标题或来源信息。 | 0.86 | 1 | 2 | 0.9 | 3 | 产品品牌形态 | 带产品/工具/平台类后缀 |  | {"source_title_person": 2} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 深度探索 | product | candidate | product | FALSE | FALSE | source_or_title | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项缺少正文回答证据，主要来自信源标题或来源信息。 | 0.86 | 1 | 1 | 0.9 | 3 | 产品品牌形态 | 带产品/工具/平台类后缀 |  | {"source_title_person": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| DataLearnerAI | product | candidate | product | FALSE | FALSE | source_or_title | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项缺少正文回答证据，主要来自信源标题或来源信息。 | 0.86 | 1 | 1 | 0.9 | 3 | 产品品牌形态 | 带产品/工具/平台类后缀 |  | {"source_title_org": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 模型选型 | product | candidate | product | FALSE | FALSE | source_or_title | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项缺少正文回答证据，主要来自信源标题或来源信息。 | 0.86 | 1 | 1 | 0.9 | 3 | 产品品牌形态 | 带产品/工具/平台类后缀 |  | {"source_title_person": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 大模型平台 | product | candidate | product | FALSE | FALSE | source_or_title | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项缺少正文回答证据，主要来自信源标题或来源信息。 | 0.86 | 1 | 1 | 0.9 | 3 | 产品类后缀 | 带产品/工具/平台类后缀 |  | {"source_title_org": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| Agent平台 | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.84 | 2 | 2 | 2.8 | 4 | 产品类后缀、中英混合品牌形态 | 带产品/工具/平台类后缀 |  | {"org_suffix": 2} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 端侧AI | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.84 | 2 | 2 | 2.8 | 4 | 产品类后缀、中英混合品牌形态 | 带产品/工具/平台类后缀 |  | {"org_suffix": 2} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 通用AI | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.84 | 2 | 2 | 2.8 | 4 | 产品类后缀、中英混合品牌形态 | 带产品/工具/平台类后缀 |  | {"org_suffix": 2} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| C端AI | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.84 | 2 | 2 | 2.8 | 4 | 产品类后缀、中英混合品牌形态 | 带产品/工具/平台类后缀 |  | {"org_suffix": 2} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| InfoQ研究中心 | company | candidate | company | FALSE | FALSE | source_or_title | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项缺少正文回答证据，主要来自信源标题或来源信息。 | 0.84 | 1 | 1 | 0.9 | 2 | 中英混合品牌形态 | 带机构/公司/平台类后缀 |  | {"source_title_org": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 20AI | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.82 | 2 | 3 | 2.8 | 3 | 产品类后缀 | 带产品/工具/平台类后缀 |  | {"org_suffix": 3} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| MagicEngine AI | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.82 | 2 | 3 | 2.8 | 3 | 产品类后缀 | 带产品/工具/平台类后缀 |  | {"english_brand_like": 3} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| Check.AI | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.82 | 2 | 3 | 2.8 | 3 | 产品类后缀 | 带产品/工具/平台类后缀 |  | {"english_brand_like": 3} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 国产大模型 | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.82 | 2 | 2 | 1.8 | 3 | 产品类后缀 | 带产品/工具/平台类后缀 |  | {"answer_heading": 2} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 企业平台 | product | candidate | product | FALSE | FALSE | generic_category | FALSE | FALSE | 0.82 | heuristic | exclude | 候选项是行业、品类或选择口径，不是具体实体名称。 | 0.82 | 2 | 2 | 2.8 | 3 | 产品类后缀 | 带产品/工具/平台类后缀 |  | {"org_suffix": 2} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 华为 | person | candidate | person | FALSE | FALSE | unrelated_entity | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项与目标实体类型不一致。 | 0.82 | 1 | 1 | 2.4 | 3 | 产品品牌形态 | 中文姓名且邻近专家职务或来源标题 | Huawei | {"person_alias": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 解型模型 | person | candidate | person | FALSE | FALSE | unrelated_entity | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项与目标实体类型不一致。 | 0.82 | 1 | 1 | 2.4 | 3 | 产品品牌形态 | 中文姓名且邻近专家职务或来源标题 | Long Context Models | {"person_alias": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 程序员 | person | candidate | person | FALSE | FALSE | unrelated_entity | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项与目标实体类型不一致。 | 0.82 | 1 | 1 | 2.4 | 3 | 产品品牌形态 | 中文姓名且邻近专家职务或来源标题 | Copilot | {"person_alias": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 云服务 | person | candidate | person | FALSE | FALSE | service_or_feature | FALSE | FALSE | 0.82 | heuristic | exclude | 候选项更像服务能力、产品功能或内容特征，不是独立竞品实体。 | 0.82 | 1 | 1 | 2.4 | 3 | 产品类后缀 | 中文姓名且邻近专家职务或来源标题 | API | {"person_alias": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 电商AI | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.8 | 1 | 1 | 2.4 | 4 | 产品类后缀、中英混合品牌形态 | 带产品/工具/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| B端AI | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.8 | 1 | 1 | 2.4 | 4 | 产品类后缀、中英混合品牌形态 | 带产品/工具/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| AI入口级平台 | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.8 | 1 | 1 | 2.4 | 4 | 产品类后缀、中英混合品牌形态 | 带产品/工具/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 产品驱动AI | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.8 | 1 | 1 | 2.4 | 4 | 产品类后缀、中英混合品牌形态 | 带产品/工具/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 平台型AI | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.8 | 1 | 1 | 2.4 | 4 | 产品类后缀、中英混合品牌形态 | 带产品/工具/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 最强内容生产型AI | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.8 | 1 | 1 | 2.4 | 4 | 产品类后缀、中英混合品牌形态 | 带产品/工具/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 多模态娱乐化AI | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.8 | 1 | 1 | 2.4 | 4 | 产品类后缀、中英混合品牌形态 | 带产品/工具/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 纳米AI | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.8 | 1 | 1 | 2.4 | 4 | 产品类后缀、中英混合品牌形态 | 带产品/工具/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 工业AI | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.8 | 1 | 1 | 2.4 | 4 | 产品类后缀、中英混合品牌形态 | 带产品/工具/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 语音AI | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.8 | 1 | 1 | 2.4 | 4 | 产品类后缀、中英混合品牌形态 | 带产品/工具/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| App内置AI | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.8 | 1 | 1 | 2.4 | 4 | 产品类后缀、中英混合品牌形态 | 带产品/工具/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 企业AI平台 | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.8 | 1 | 1 | 2.4 | 4 | 产品类后缀、中英混合品牌形态 | 带产品/工具/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 被大量企业用于API替换OpenAI | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.8 | 1 | 1 | 2.4 | 4 | 产品类后缀、中英混合品牌形态 | 带产品/工具/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 企业Agent平台 | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.8 | 1 | 1 | 2.4 | 4 | 产品类后缀、中英混合品牌形态 | 带产品/工具/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 产品化AI | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.8 | 1 | 1 | 2.4 | 4 | 产品类后缀、中英混合品牌形态 | 带产品/工具/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 做企业AI平台 | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.8 | 1 | 1 | 2.4 | 4 | 产品类后缀、中英混合品牌形态 | 带产品/工具/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 心大模型 | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.78 | 1 | 1 | 2.4 | 3 | 产品品牌形态 | 带产品/工具/平台类后缀 | ERNIE | {"person_alias": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 知识增强 | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.78 | 1 | 1 | 2.4 | 3 | 产品品牌形态 | 带产品/工具/平台类后缀 | RAG | {"person_alias": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 需要说明的是 | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.78 | 1 | 1 | 1.4 | 3 | 产品品牌形态 | 带产品/工具/平台类后缀 |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 古大模型 | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.78 | 1 | 1 | 2.4 | 3 | 产品品牌形态 | 带产品/工具/平台类后缀 | Pangu | {"person_alias": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 火大模型 | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.78 | 1 | 1 | 2.4 | 3 | 产品品牌形态 | 带产品/工具/平台类后缀 | Spark | {"person_alias": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 盘古 | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.78 | 1 | 1 | 2.4 | 3 | 产品品牌形态 | 带产品/工具/平台类后缀 | Pangu | {"person_alias": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 语音识别与教育 | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.78 | 1 | 1 | 2.4 | 3 | 产品品牌形态 | 带产品/工具/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 最强梯队 | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.78 | 1 | 1 | 2.4 | 3 | 产品品牌形态 | 带产品/工具/平台类后缀 | Reasoning | {"person_alias": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 全能平台 | product | candidate | product | FALSE | FALSE | generic_category | FALSE | FALSE | 0.82 | heuristic | exclude | 候选项是行业、品类或选择口径，不是具体实体名称。 | 0.78 | 1 | 1 | 2.4 | 3 | 产品类后缀 | 带产品/工具/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 基座模型 | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.78 | 1 | 1 | 2.4 | 3 | 产品品牌形态 | 带产品/工具/平台类后缀 | General LLM | {"person_alias": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 考型模型 | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.78 | 1 | 1 | 2.4 | 3 | 产品品牌形态 | 带产品/工具/平台类后缀 | Reasoning Models | {"person_alias": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 模态模型 | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.78 | 1 | 1 | 2.4 | 3 | 产品品牌形态 | 带产品/工具/平台类后缀 | Multimodal Models | {"person_alias": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 下文模型 | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.78 | 1 | 1 | 2.4 | 3 | 产品品牌形态 | 带产品/工具/平台类后缀 | Kimi | {"person_alias": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 长文本 | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.78 | 1 | 1 | 2.4 | 3 | 产品品牌形态 | 带产品/工具/平台类后缀 | Kimi | {"person_alias": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 内容平台 | product | candidate | product | FALSE | FALSE | generic_category | FALSE | FALSE | 0.82 | heuristic | exclude | 候选项是行业、品类或选择口径，不是具体实体名称。 | 0.78 | 1 | 1 | 2.4 | 3 | 产品类后缀 | 带产品/工具/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 结合近两年 | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.78 | 1 | 1 | 1.4 | 3 | 产品品牌形态 | 带产品/工具/平台类后缀 |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| ## 1）通用基础大模型 | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.78 | 1 | 1 | 1.4 | 3 | 产品类后缀 | 带产品/工具/平台类后缀 |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 用大模型 | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.78 | 1 | 1 | 2.4 | 3 | 产品品牌形态 | 带产品/工具/平台类后缀 | General-purpose LLM | {"person_alias": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 业大模型 | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.78 | 1 | 1 | 2.4 | 3 | 产品品牌形态 | 带产品/工具/平台类后缀 | Industry LLM | {"person_alias": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 写代码 | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.78 | 1 | 1 | 2.4 | 3 | 产品品牌形态 | 带产品/工具/平台类后缀 | Code LLM | {"person_alias": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 视觉模型 | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.78 | 1 | 1 | 2.4 | 3 | 产品品牌形态 | 带产品/工具/平台类后缀 | Qwen-VL | {"person_alias": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 文本模型 | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.78 | 1 | 1 | 2.4 | 3 | 产品品牌形态 | 带产品/工具/平台类后缀 | Text-only LLM | {"person_alias": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 态大模型 | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.78 | 1 | 1 | 2.4 | 3 | 产品品牌形态 | 带产品/工具/平台类后缀 | Multimodal LLM | {"person_alias": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 增强问答 | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.78 | 1 | 1 | 2.4 | 3 | 产品品牌形态 | 带产品/工具/平台类后缀 | RAG | {"person_alias": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 业知识库 | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.78 | 1 | 1 | 2.4 | 3 | 产品品牌形态 | 带产品/工具/平台类后缀 | RAG | {"person_alias": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 最完整的企业级大模型平台 | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.78 | 1 | 1 | 2.4 | 3 | 产品类后缀 | 带产品/工具/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 阿里云百炼平台 | product | candidate | product | FALSE | FALSE | generic_category | FALSE | FALSE | 0.82 | heuristic | exclude | 候选项是行业、品类或选择口径，不是具体实体名称。 | 0.78 | 1 | 1 | 2.4 | 3 | 产品类后缀 | 带产品/工具/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 腾讯混元 | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.78 | 1 | 1 | 2.4 | 3 | 产品品牌形态 | 带产品/工具/平台类后缀 | Hunyuan | {"person_alias": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 检索增强 | product | candidate | product | FALSE | FALSE | uncertain | FALSE | FALSE | 0.5 | heuristic | manual_review | 候选项证据不足，建议人工确认。 | 0.78 | 1 | 1 | 2.4 | 3 | 产品品牌形态 | 带产品/工具/平台类后缀 | RAG | {"person_alias": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 字节豆包 | product | candidate | product | FALSE | FALSE | target_alias | TRUE | FALSE | 0.96 | heuristic | merge_target_alias | 候选项与目标实体或目标别名匹配。 | 0.78 | 1 | 1 | 2.4 | 3 | 产品品牌形态 | 带产品/工具/平台类后缀 | Doubao | {"person_alias": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| AI基础设施公司 | company | candidate | company | FALSE | FALSE | unrelated_entity | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项与目标实体类型不一致。 | 0.76 | 1 | 1 | 2.4 | 2 | 中英混合品牌形态 | 带机构/公司/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 的国内模型公司 | company | candidate | company | FALSE | FALSE | generic_category | FALSE | FALSE | 0.82 | heuristic | exclude | 候选项是行业、品类或选择口径，不是具体实体名称。 | 0.74 | 1 | 1 | 2.4 | 1 |  | 带机构/公司/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 10中国大模型公司 | company | candidate | company | FALSE | FALSE | unrelated_entity | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项与目标实体类型不一致。 | 0.74 | 1 | 1 | 2.4 | 1 |  | 带机构/公司/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 互联网公司 | company | candidate | company | FALSE | FALSE | generic_category | FALSE | FALSE | 0.82 | heuristic | exclude | 候选项是行业、品类或选择口径，不是具体实体名称。 | 0.74 | 1 | 1 | 2.4 | 1 |  | 带机构/公司/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 科技公司 | company | candidate | company | FALSE | FALSE | generic_category | FALSE | FALSE | 0.82 | heuristic | exclude | 候选项是行业、品类或选择口径，不是具体实体名称。 | 0.74 | 1 | 1 | 2.4 | 1 |  | 带机构/公司/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 中台架构怎么设计 | company | candidate | company | FALSE | FALSE | unrelated_entity | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项与目标实体类型不一致。 | 0.74 | 1 | 1 | 2.4 | 1 |  | 带机构/公司/平台类后缀 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 人工智能 | concept | candidate | concept | FALSE | FALSE | source_or_title | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项缺少正文回答证据，主要来自信源标题或来源信息。 | 0.65 | 7 | 13 | 2.5 | 1 |  |  |  | {"source_title_org": 13} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| domain=https | concept | candidate | concept | FALSE | FALSE | unrelated_entity | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项与目标实体类型不一致。 | 0.59 | 14 | 100 | 3.0 | 2 | 中英混合品牌形态 |  |  | {"answer_heading": 100} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| utm_source=chatgpt.com | concept | candidate | concept | FALSE | FALSE | unrelated_entity | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项与目标实体类型不一致。 | 0.59 | 7 | 26 | 3.0 | 2 | 中英混合品牌形态 |  |  | {"answer_heading": 26} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 性能排行 | concept | candidate | concept | FALSE | FALSE | source_or_title | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项缺少正文回答证据，主要来自信源标题或来源信息。 | 0.53 | 2 | 2 | 1.3 | 1 |  |  |  | {"source_title_person": 2} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| # 一、第一梯队 | concept | candidate | concept | FALSE | FALSE | unrelated_entity | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项与目标实体类型不一致。 | 0.49 | 3 | 3 | 2.2 | 1 |  |  |  | {"answer_heading": 3} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 企业接入国产大模型时 | concept | candidate | concept | FALSE | FALSE | unrelated_entity | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项与目标实体类型不一致。 | 0.45 | 2 | 2 | 1.8 | 1 |  |  |  | {"answer_heading": 2} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| # 🇨🇳 中国大模型Top 10 | concept | candidate | concept | FALSE | FALSE | unrelated_entity | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项与目标实体类型不一致。 | 0.43 | 1 | 1 | 1.4 | 2 | 中英混合品牌形态 |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| # 🇨🇳 2026中国大模型Top 10 | concept | candidate | concept | FALSE | FALSE | unrelated_entity | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项与目标实体类型不一致。 | 0.43 | 1 | 1 | 1.4 | 2 | 中英混合品牌形态 |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| ## 1）MoE | concept | candidate | concept | FALSE | FALSE | unrelated_entity | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项与目标实体类型不一致。 | 0.43 | 1 | 1 | 1.4 | 2 | 中英混合品牌形态 |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 截至 2026 年 | concept | candidate | concept | FALSE | FALSE | unrelated_entity | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项与目标实体类型不一致。 | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 结合近期公开行业报告与技术新闻 | concept | candidate | concept | FALSE | FALSE | unrelated_entity | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项与目标实体类型不一致。 | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| # 🇨🇳 中国大模型前十 | concept | candidate | concept | FALSE | FALSE | unrelated_entity | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项与目标实体类型不一致。 | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| # 一、结论先说 | concept | candidate | concept | FALSE | FALSE | unrelated_entity | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项与目标实体类型不一致。 | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| ## 💻 代码能力最强梯队 | concept | candidate | concept | FALSE | FALSE | unrelated_entity | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项与目标实体类型不一致。 | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| # 一、结论先说清 | concept | candidate | concept | FALSE | FALSE | unrelated_entity | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项与目标实体类型不一致。 | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 结合近期公开评测与行业报告 | concept | candidate | concept | FALSE | FALSE | unrelated_entity | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项与目标实体类型不一致。 | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| # 一、按能力路线划分 | concept | candidate | concept | FALSE | FALSE | unrelated_entity | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项与目标实体类型不一致。 | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| ** * * * # 五、未来趋势 | concept | candidate | concept | FALSE | FALSE | unrelated_entity | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项与目标实体类型不一致。 | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 下面给你一个比较清晰的“行业通用分法 | concept | candidate | concept | FALSE | FALSE | unrelated_entity | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项与目标实体类型不一致。 | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| # 一、按技术架构分 | concept | candidate | concept | FALSE | FALSE | unrelated_entity | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项与目标实体类型不一致。 | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| ## 1）通用推理/代码型 | concept | candidate | concept | FALSE | FALSE | unrelated_entity | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项与目标实体类型不一致。 | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 最强智能 | concept | candidate | concept | FALSE | FALSE | unrelated_entity | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项与目标实体类型不一致。 | 0.41 | 1 | 1 | 2.4 | 1 |  |  |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 企业级智能 | concept | candidate | concept | FALSE | FALSE | unrelated_entity | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项与目标实体类型不一致。 | 0.41 | 1 | 1 | 2.4 | 1 |  |  |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 结合 2026 年公开评测与行业报告 | concept | candidate | concept | FALSE | FALSE | unrelated_entity | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项与目标实体类型不一致。 | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| # 一、优先级结论 | concept | candidate | concept | FALSE | FALSE | unrelated_entity | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项与目标实体类型不一致。 | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| # 一、结论先行 | concept | candidate | concept | FALSE | FALSE | unrelated_entity | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项与目标实体类型不一致。 | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 推理能力 | concept | candidate | concept | FALSE | FALSE | service_or_feature | FALSE | FALSE | 0.82 | heuristic | exclude | 候选项更像服务能力、产品功能或内容特征，不是独立竞品实体。 | 0.41 | 1 | 1 | 2.4 | 1 |  |  | Reasoning | {"person_alias": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 结合 2025–2026 年公开测评与行业实践 | concept | candidate | concept | FALSE | FALSE | unrelated_entity | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项与目标实体类型不一致。 | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 下面给你一个**企业可落地的优先选型清单 | concept | candidate | concept | FALSE | FALSE | unrelated_entity | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项与目标实体类型不一致。 | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| # 一、第一优先梯队 | concept | candidate | concept | FALSE | FALSE | unrelated_entity | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项与目标实体类型不一致。 | 0.41 | 1 | 1 | 1.4 | 1 |  |  |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| DeepSeek-Co | noise | candidate | noise | FALSE | FALSE | unrelated_entity | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项与目标实体类型不一致。 | 0.2 | 2 | 4 | 2.8 | 3 | 产品品牌形态 | 通用词/指标/缩写，非目标实体 |  | {"english_brand_like": 4} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| Qwen-Co | noise | candidate | noise | FALSE | FALSE | unrelated_entity | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项与目标实体类型不一致。 | 0.2 | 2 | 2 | 2.8 | 3 | 产品品牌形态 | 通用词/指标/缩写，非目标实体 |  | {"english_brand_like": 2} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 谁最适合做AI | noise | candidate | noise | FALSE | FALSE | unrelated_entity | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项与目标实体类型不一致。 | 0.2 | 1 | 1 | 2.4 | 4 | 产品类后缀、中英混合品牌形态 | 通用词/指标/缩写，非目标实体 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| Qwen3-Co | noise | candidate | noise | FALSE | FALSE | unrelated_entity | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项与目标实体类型不一致。 | 0.2 | 1 | 2 | 2.4 | 4 | 车型/型号形态 | 通用词/指标/缩写，非目标实体 |  | {"english_brand_like": 2} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 应用场景 | noise | candidate | noise | FALSE | FALSE | source_or_title | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项缺少正文回答证据，主要来自信源标题或来源信息。 | 0.2 | 1 | 1 | 0.9 | 3 | 产品品牌形态 | 通用词/指标/缩写，非目标实体 |  | {"source_title_person": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 企业标准化AI | noise | candidate | noise | FALSE | FALSE | unrelated_entity | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项与目标实体类型不一致。 | 0.2 | 1 | 1 | 2.4 | 4 | 产品类后缀、中英混合品牌形态 | 通用词/指标/缩写，非目标实体 |  | {"org_suffix": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 下面基于**2025–2026年公开信息 | noise | candidate | noise | FALSE | FALSE | unrelated_entity | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项与目标实体类型不一致。 | 0.16 | 1 | 1 | 1.4 | 1 |  | 通用词/指标/缩写，非目标实体 |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 下面基于**2026年上半年公开信息 | noise | candidate | noise | FALSE | FALSE | unrelated_entity | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项与目标实体类型不一致。 | 0.16 | 1 | 1 | 1.4 | 1 |  | 通用词/指标/缩写，非目标实体 |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| DeepSeek Co | noise | candidate | noise | FALSE | FALSE | unrelated_entity | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项与目标实体类型不一致。 | 0.16 | 1 | 2 | 2.4 | 1 |  | 通用词/指标/缩写，非目标实体 |  | {"english_brand_like": 2} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| Qwen3.5 - Qwen-Co | noise | candidate | noise | FALSE | FALSE | unrelated_entity | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项与目标实体类型不一致。 | 0.16 | 1 | 1 | 2.4 | 1 |  | 通用词/指标/缩写，非目标实体 |  | {"english_brand_like": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| Long Co | noise | candidate | noise | FALSE | FALSE | unrelated_entity | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项与目标实体类型不一致。 | 0.16 | 1 | 1 | 2.4 | 1 |  | 通用词/指标/缩写，非目标实体 |  | {"english_brand_like": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| Qwen Long Co | noise | candidate | noise | FALSE | FALSE | unrelated_entity | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项与目标实体类型不一致。 | 0.16 | 1 | 1 | 2.4 | 1 |  | 通用词/指标/缩写，非目标实体 |  | {"english_brand_like": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 📌来源 | noise | candidate | noise | FALSE | FALSE | unrelated_entity | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项与目标实体类型不一致。 | 0.16 | 1 | 1 | 1.4 | 1 |  | 通用词/指标/缩写，非目标实体 |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| 下面给你一个**企业可落地的优先级推荐框架** | noise | candidate | noise | FALSE | FALSE | unrelated_entity | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项与目标实体类型不一致。 | 0.16 | 1 | 1 | 1.4 | 1 |  | 通用词/指标/缩写，非目标实体 |  | {"answer_heading": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |
| Qwen Co | noise | candidate | noise | FALSE | FALSE | unrelated_entity | FALSE | FALSE | 0.74 | heuristic | exclude | 候选项与目标实体类型不一致。 | 0.16 | 1 | 1 | 2.4 | 1 |  | 通用词/指标/缩写，非目标实体 |  | {"english_brand_like": 1} | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  | neutral | 0 | 0 |

## 信源渠道分布

ChatGPT 引用信源的渠道结构。

- 行数：6

| bucket | raw_bucket | count | rate |
| --- | --- | --- | --- |
| 媒体 | media | 32 | 0.16326530612244897 |
| 社区 | community | 25 | 0.12755102040816327 |
| 其他 | other | 111 | 0.5663265306122449 |
| 学术 | academic | 9 | 0.04591836734693878 |
| 开发者 | developer | 18 | 0.09183673469387756 |
| 官方 | official | 1 | 0.00510204081632653 |

## 来源编号位置

ChatGPT 引用编号或链接位置分布。

- 行数：3

| bucket | raw_bucket | count | rate |
| --- | --- | --- | --- |
| 1-3 | 1-3 | 45 | 0.22959183673469388 |
| 4-6 | 4-6 | 45 | 0.22959183673469388 |
| 7+ | 7+ | 106 | 0.5408163265306123 |

## 高频域名

高频引用域名。

- 行数：10

| display_name | name | count | url |
| --- | --- | --- | --- |
| 技术栈 | jishuzhan.net | 8 | https://jishuzhan.net |
| Presenc AI | presenc.ai | 7 | https://presenc.ai |
| Reuters | reuters.com | 6 | https://reuters.com |
| sina.com.cn | finance.sina.com.cn | 6 | https://finance.sina.com.cn |
| Check.AI | checkaimodels.com | 6 | https://checkaimodels.com |
| 智数站 | zishuzhan.com | 6 | https://zishuzhan.com |
| sina.cn | k.sina.cn | 6 | https://k.sina.cn |
| ai-learn.cn | ai-learn.cn | 6 | https://ai-learn.cn |
| sina.com.cn | k.sina.com.cn | 5 | https://k.sina.com.cn |
| codingplan.fyi | codingplan.fyi | 5 | https://codingplan.fyi |

## 高频来源名

高频引用来源名称。

- 行数：10

| name | count |
| --- | --- |
| csdn.net | 11 |
| sina.com.cn | 10 |
| Reuters | 6 |
| Presenc AI | 6 |
| ai-learn.cn | 6 |
| zishuzhan.com | 5 |
| codingplan.fyi | 5 |
| jishuzhan.net | 4 |
| checkaimodels.com | 4 |
| sina.cn | 4 |

## 高频URL

高频引用 URL。

- 行数：10

| display_name | name | url | domain | source | count |
| --- | --- | --- | --- | --- | --- |
| 2026 国产 AI 大模型横评：DeepSeek、通义千问、Kimi、文心一言、星火、豆包谁更能打？ - 技术栈 | 2026 国产 AI 大模型横评：DeepSeek、通义千问、Kimi、文心一言、星火、豆包谁更能打？ - 技术栈 | https://jishuzhan.net/article/2065289201393954817?utm_source=chatgpt.com | jishuzhan.net | jishuzhan.net | 8 |
| 2026年国内大模型终极横评 - 智数站 | 2026年国内大模型终极横评 - 智数站 | https://zishuzhan.com/article-llm-comparison.html?utm_source=chatgpt.com | zishuzhan.com | zishuzhan.com | 6 |
| AI Learn \| 2026 国产前沿模型观察站 (Frontier AI Radar) | AI Learn \| 2026 国产前沿模型观察站 (Frontier AI Radar) | https://www.ai-learn.cn/?utm_source=chatgpt.com | ai-learn.cn | ai-learn.cn | 6 |
| 2026 国产 AI 模型哪个最强？DeepSeek/Qwen/Kimi/GLM/MiniMax 价格+跑分对比 \| Check.AI | 2026 国产 AI 模型哪个最强？DeepSeek/Qwen/Kimi/GLM/MiniMax 价格+跑分对比 \| Check.AI | https://checkaimodels.com/zh/articles/china-ai-models-landscape-2026/?utm_source=chatgpt.com | checkaimodels.com | Check.AI | 5 |
| 2026国产大模型Token成本对比：DeepSeek/GLM/Kimi/通义千问谁性价比最高？ | 2026国产大模型Token成本对比：DeepSeek/GLM/Kimi/通义千问谁性价比最高？ | https://www.bingotech.net/news/2026-Token-DeepSeek-GLM-Kimi.html?utm_source=chatgpt.com | bingotech.net | bingotech.net | 4 |
| 国产AI主流模型比较：DeepSeek、kimi、千问、豆包、元宝详细对比与排行榜-行业资讯-AI工具网 | 国产AI主流模型比较：DeepSeek、kimi、千问、豆包、元宝详细对比与排行榜-行业资讯-AI工具网 | https://www.aigjw.com.cn/news/2026/176874921620.html?utm_source=chatgpt.com | aigjw.com.cn | aigjw.com.cn | 4 |
| 2026 年中国 AI 大模型厂商行业报告\|市场份额\|文心\|应用场景\|阿里巴巴\|百度_新浪新闻 | 2026 年中国 AI 大模型厂商行业报告\|市场份额\|文心\|应用场景\|阿里巴巴\|百度_新浪新闻 | https://k.sina.cn/article_7879848900_1d5acf3c401902xa4a.html?utm_source=chatgpt.com | k.sina.cn | sina.cn | 4 |
| 2026年6月主流大模型Coding能力深度对比｜GPT-5.5、Claude Opus 4.8、国产多款跻身前十 | 2026年6月主流大模型Coding能力深度对比｜GPT-5.5、Claude Opus 4.8、国产多款跻身前十 | https://www.codingplan.fyi/articles/model_comparisons/20260604/?utm_source=chatgpt.com | codingplan.fyi | codingplan.fyi | 4 |
| 国产大模型横向对比：Kimi K2.6、GLM-5.1、Qwen3、MiniMax M2 四大模型选型指南 - 苏米客 | 国产大模型横向对比：Kimi K2.6、GLM-5.1、Qwen3、MiniMax M2 四大模型选型指南 - 苏米客 | https://www.xmsumi.com/detail/2984?utm_source=chatgpt.com | xmsumi.com | 苏米客 | 4 |
| Best Chinese LLMs in 2026: DeepSeek V4, Kimi K2.6, GLM-5, Qwen, and Every Model Ranked \| BenchLM.ai | Best Chinese LLMs in 2026: DeepSeek V4, Kimi K2.6, GLM-5, Qwen, and Every Model Ranked \| BenchLM.ai | https://benchlm.ai/blog/posts/best-chinese-llm?utm_source=chatgpt.com | benchlm.ai | benchlm.ai | 4 |

## 高频引用标题

被重复引用的标题。

- 行数：10

| name | url | source | domain | count |
| --- | --- | --- | --- | --- |
| 2026 国产 AI 大模型横评：DeepSeek、通义千问、Kimi、文心一言、星火、豆包谁更能打？ - 技术栈 | https://jishuzhan.net/article/2065289201393954817?utm_source=chatgpt.com | jishuzhan.net | jishuzhan.net | 8 |
| 2026年国内大模型终极横评 - 智数站 | https://zishuzhan.com/article-llm-comparison.html?utm_source=chatgpt.com | zishuzhan.com | zishuzhan.com | 6 |
| AI Learn \| 2026 国产前沿模型观察站 (Frontier AI Radar) | https://www.ai-learn.cn/?utm_source=chatgpt.com | ai-learn.cn | ai-learn.cn | 6 |
| 2026 年中国 AI 大模型厂商行业报告\|市场份额\|文心\|应用场景\|阿里巴巴\|百度_新浪新闻 | https://k.sina.cn/article_7879848900_1d5acf3c401902xa4a.html?utm_source=chatgpt.com | sina.cn | k.sina.cn | 5 |
| 2026 国产 AI 模型哪个最强？DeepSeek/Qwen/Kimi/GLM/MiniMax 价格+跑分对比 \| Check.AI | https://checkaimodels.com/zh/articles/china-ai-models-landscape-2026/?utm_source=chatgpt.com | checkaimodels.com | checkaimodels.com | 5 |
| 2026国产大模型Token成本对比：DeepSeek/GLM/Kimi/通义千问谁性价比最高？ | https://www.bingotech.net/news/2026-Token-DeepSeek-GLM-Kimi.html?utm_source=chatgpt.com | bingotech.net | bingotech.net | 4 |
| 国产AI主流模型比较：DeepSeek、kimi、千问、豆包、元宝详细对比与排行榜-行业资讯-AI工具网 | https://www.aigjw.com.cn/news/2026/176874921620.html?utm_source=chatgpt.com | aigjw.com.cn | aigjw.com.cn | 4 |
| 2026年6月主流大模型Coding能力深度对比｜GPT-5.5、Claude Opus 4.8、国产多款跻身前十 | https://www.codingplan.fyi/articles/model_comparisons/20260604/?utm_source=chatgpt.com | codingplan.fyi | codingplan.fyi | 4 |
| 国产大模型横向对比：Kimi K2.6、GLM-5.1、Qwen3、MiniMax M2 四大模型选型指南 - 苏米客 | https://www.xmsumi.com/detail/2984?utm_source=chatgpt.com | 苏米客 | xmsumi.com | 4 |
| Best Chinese LLMs in 2026: DeepSeek V4, Kimi K2.6, GLM-5, Qwen, and Every Model Ranked \| BenchLM.ai | https://benchlm.ai/blog/posts/best-chinese-llm?utm_source=chatgpt.com | benchlm.ai | benchlm.ai | 4 |

## 标题功能特征

引用标题的功能信号。

- 行数：5

| feature | count | rate |
| --- | --- | --- |
| has_number | 158 | 0.8061224489795918 |
| has_year | 130 | 0.6632653061224489 |
| contains_brand | 90 | 0.45918367346938777 |
| has_structure_punctuation | 96 | 0.4897959183673469 |
| has_question | 39 | 0.1989795918367347 |

## 标题长度

引用标题长度分布。

- 行数：4

| bucket | raw_bucket | count | rate |
| --- | --- | --- | --- |
| 25-40 | 25-40 | 39 | 0.1989795918367347 |
| 41+ | 41+ | 144 | 0.7346938775510204 |
| 13-24 | 13-24 | 11 | 0.05612244897959184 |
| 0-12 | 0-12 | 2 | 0.01020408163265306 |

## 时间新旧

引用标题或日期的新旧分布。

- 行数：4

| bucket | raw_bucket | count | rate |
| --- | --- | --- | --- |
| 本年 | current_year | 170 | 0.8673469387755102 |
| 未识别 | unknown | 15 | 0.07653061224489796 |
| 近一年 | last_year | 9 | 0.04591836734693878 |
| 更早 | older | 2 | 0.01020408163265306 |

## 标题意图

引用标题意图特征分布。

- 行数：8

| bucket | raw_bucket | count | rate |
| --- | --- | --- | --- |
| 趋势新闻 | 趋势新闻 | 136 | 0.4358974358974359 |
| 其他信息 | 其他信息 | 31 | 0.09935897435897435 |
| 榜单排名 | 榜单排名 | 40 | 0.1282051282051282 |
| 对比评测 | 对比评测 | 75 | 0.2403846153846154 |
| 避坑风险 | 避坑风险 | 3 | 0.009615384615384616 |
| 指南攻略 | 指南攻略 | 17 | 0.05448717948717949 |
| 推荐选择 | 推荐选择 | 6 | 0.019230769230769232 |
| 研究论文 | 研究论文 | 4 | 0.01282051282051282 |
