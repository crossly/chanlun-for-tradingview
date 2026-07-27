---
slug: flow
title: Key flows
role: key flows
updated: "2026-07-27T13:13:59"
---

# Key flows

## 典型分析路径

用户把 `chanlun.pine` 粘贴到 TradingView Pine Editor，并将指标添加到标准 OHLC 图表。指标按图表周期处理全部可用历史，构建焦点周期结构；参考周期只在自身收盘后提供确认结果。最后一根 K 线根据展示预设输出有限几何和状态面板；符合筛选条件的确认事件经单一 `alert()` 发送。

```mermaid
sequenceDiagram
  participant U as 使用者
  participant TV as TradingView 图表
  participant P as chanlun.pine
  participant R as 参考周期请求
  participant W as Webhook
  U->>TV: 添加 Pine v6 指标
  TV->>P: 提供标准 OHLC 与图表周期
  P->>P: 包含处理 -> 分型 -> 笔 -> 线段 -> T0-T3
  P->>R: 请求严格更高周期的已收盘数据
  R-->>P: 已确认参考结构 T0-T2
  P->>P: 建立证据、共振、区间套和候选情景
  P-->>TV: 绘制结构、标签和状态面板
  P->>W: 可筛选、去重的确认事件 JSON
```

## 关键时间规则

- 结构时间记录结构端点发生时间；确认时间记录实时首次可知时间。
- 候选结构可被替换或失效；确认结构冻结，不被未来 K 线回改。
- 非标准图表停止确认信号；参考周期的未收盘状态不得参与确认共振或默认提醒。
