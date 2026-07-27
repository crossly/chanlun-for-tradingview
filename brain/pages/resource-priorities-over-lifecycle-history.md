---
id: resource-priorities-over-lifecycle-history
title: "确认真值优先于详细绘图和历史生命周期账本"
category: decision
status: active
tags: [performance, rendering, lifecycle, free-plan]
created: "2026-07-27T13:14:28"
updated: "2026-07-27T16:48:31"
---

## compiled_truth

TradingView 的编译 token、执行时间、内存和绘图对象预算都是发布约束。资源取舍顺序仍是：焦点周期确认真值、参考周期已收盘结构与共振、候选可见性、历史详细几何、情景与调试能力。

当前工作树已完全移除生产 `chanlun.pine` 的历史 lifecycle ledger、结构快照与逐边界 reconcile，而不只是默认关闭。这样保留了当前结构、买卖点、证据、共振、区间套、提醒和 tooltip，但不再交付 `candidate/confirmed/replaced/invalidated` 的完整历史迁移账本。该范围与 `.scratch/chanlun-theory-v2/spec.md`、ADR 0044 以及“默认关闭但仍可启用”的 ADR 0048 存在明确偏差；发布前必须通过新 ADR/规格更新确认取舍，或恢复实现。

2026-07-27 对当前 `chanlun.pine` 的静态审查确认三个风险：

1. 参考周期的同型更极端分型会更新末端候选笔，但 `f_update_strokes` 返回未变化，`ReferenceState.structuresDirty` 不会置位；已确认前缀不受影响，参考候选 `S/Tn`、候选证据与候选提醒可能延迟到下一次新笔边界才刷新。
2. 焦点周期在活动最后柱的每个 tick 复制完整 K、MACD 和笔数组，并从头重建 `S/T0-T3`、背驰、点位和证据；其中 DIF 极值、背驰/点位历史匹配及若干嵌套扫描仍可能形成超线性成本。
3. 展示层每个最后柱更新都会删除并新建全部可见 line、label、box，造成与可见对象数成正比的对象 churn。

这些结论来自源码结构，不是 TradingView profiler 结果。最新工作树仍需官方 Pine v6 编译、最重配置 profiler、Bar Replay 与重载验证。相关：[[bounded-focus-and-reference-timeframes]]、[[course-new-stroke-and-true-ranges]]。


## timeline

- time: 2026-07-27T13:14:28
  kind: decision
  summary: "Created this page: 确认真值优先于详细绘图和历史生命周期账本"
  source: "README, CONTEXT.md, ADR, git log"
  affects: [resource-priorities-over-lifecycle-history]

- time: 2026-07-27T13:14:28
  kind: decision
  summary: "从项目理论规范、ADR 与提交历史提炼持续约束"
  source: "README, CONTEXT.md, ADR, git log"
  affects: [resource-priorities-over-lifecycle-history]

- time: 2026-07-27T13:20:22
  kind: decision
  summary: "补充 TradingView 编译 token 预算与展示层死参数约束"
  source: "TradingView CE10117 编译错误与 chanlun.pine 审核"
  affects: [resource-priorities-over-lifecycle-history]

- time: 2026-07-27T13:29:53
  kind: decision
  summary: "CE10117 token 上限下移除非核心历史生命周期账本"
  source: "TradingView CE10117 与生产源码审计"
  affects: [resource-priorities-over-lifecycle-history]

- time: 2026-07-27T16:48:31
  kind: decision
  summary: "校准当前生产范围、ADR 偏差与 2026-07-27 性能审查结论"
  source: "chanlun.pine、README、docs/adr、.scratch 与 2026-07-27 静态审查"
  affects: [resource-priorities-over-lifecycle-history]
