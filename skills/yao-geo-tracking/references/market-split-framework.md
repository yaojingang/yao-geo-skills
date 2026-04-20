# Market Split Framework

## Goal

国内 GEO 和海外 GEO 的后端效果监测不能完全沿用同一套权重。分析前先判断市场和平台环境，再决定方案重点。

## 1. Overseas GEO

### Typical platforms

- ChatGPT
- Gemini
- Perplexity
- Claude

### Default characteristics

- 用户更容易通过网页访问官网、帮助中心、文档页和产品页
- 官网页矩阵、落地页、表单字段、Web analytics 更容易成为主归因骨架
- 页面结构、FAQ、schema、内容承接和转化页设计的重要性更高

### Priority actions

- GEO 专属落地页
- 表单来源字段
- 页面 ID 与主题映射
- CTA 事件跟踪
- 注册、激活、升级链路回传

## 2. China GEO

### Typical platforms

- DeepSeek
- 豆包
- 元宝
- Kimi

### Default characteristics

- 跨端访问、App 内跳转、来源丢失更常见
- 仅依赖官网来源字段通常不够
- 需要更多“来源补丁”来还原 GEO 带来的线索和咨询

### Priority actions

- 专属口令、权益码、活动页
- 专属企微、电话、顾问入口
- 预约后或成交后自报来源问卷
- GEO 专属承接页和表单字段
- 线索台账与人工回访补录

## 3. Hybrid Case

如果公司同时做国内和海外 GEO：

- 先分开设计两套主归因链路
- 再统一收口到一张 attribution dictionary
- 不要把国内和海外流量、线索、问卷口径混成一套

## 4. Output Requirement

最终方案必须明确回答：

- 当前主要是国内 GEO、海外 GEO，还是混合 GEO
- 哪些环节可以更多依赖官网
- 哪些环节必须用口令、问卷、电话、企微等补丁手段
- 为什么会这样设计
