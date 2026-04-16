# Personalization Matrix

## Goal

同样是 GEO 后端归因，不同业务形态应该使用不同的承接动作、指标口径和优先级。

## 1. B2B Sales-Led

### Typical conversion

- 预约演示
- 售前咨询
- 留资
- 商机推进

### Priority design

- 专属顾问入口
- 专属热线或分机
- 表单隐藏字段
- CRM 线索来源映射
- 自报来源问卷

### Secondary metrics

- 品牌词检索量
- 官网 UV
- 落地页 UV
- 线索到商机率

## 2. PLG / SaaS

### Typical conversion

- 免费注册
- 免费试用
- 产品激活
- 付费升级

### Priority design

- GEO 专属注册页
- UTM / 页面 ID / 渠道码
- 注册表单来源字段
- 产品内首次来源问卷
- 激活率与升级率跟踪

### Secondary metrics

- 品牌词检索量
- 关键产品页 UV
- 注册转化率
- 激活率

## 3. Ecommerce / Standardized Consumer

### Typical conversion

- 下单
- 加购
- 领券
- 门店到访

### Priority design

- 优惠口令
- 专属活动页
- AI 专属权益包
- 页面来源参数
- 购买后来源问卷

### Secondary metrics

- 商品页 UV
- 加购率
- 领取优惠率
- 订单转化率

## 4. Appointment / Consultation Service

### Typical conversion

- 预约
- 拨打电话
- 添加客服
- 到店或到诊

### Priority design

- 专属电话
- 专属预约页
- 渠道二维码
- 顾问入口
- 预约后来源确认

### Secondary metrics

- 预约率
- 到店率
- 咨询到成交率

## Default Rule

如果业务类型混合：

- 先找最关键转化动作
- 用最关键动作来选主归因模型
- 其他动作只做辅助指标，不平均发力

如果市场类型混合：

- 先分别判断国内 GEO 和海外 GEO 的主承接方式
- 海外优先看官网结构、表单、升级链路
- 国内优先补口令、问卷、企微、电话和活动页
