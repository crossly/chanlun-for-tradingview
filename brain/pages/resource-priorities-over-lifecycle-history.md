---
id: resource-priorities-over-lifecycle-history
title: "确认真值优先于详细绘图和历史生命周期账本"
category: decision
status: active
tags: [performance, rendering, lifecycle, free-plan]
created: "2026-07-27T13:14:28"
updated: "2026-07-27T13:20:22"
---

## compiled_truth

指标的 TradingView 编译 token 预算与运行时对象、时间、内存预算同样是发布约束。展示层 helper 不得保留未读取的参数或其调用表达式：这些表达式可能被 Pine 编译器计入 token 预算，即使不会改变可见结果。

指标增量处理可用历史，并在至少 200 根 K 线预热及首个来源完整结构后才产生可靠区间内的确认事件。完整几何只绘制最近详细窗口，确认买卖点以轻量序列保留；面板必须披露可靠起点、详细绘图范围和资源裁剪。

历史生命周期账本需要在结构边界重建递归层级、构造快照并保存只增不减的事件数组。它不改变确认结构、买卖点、证据、共振、区间套或提醒的真值，因此是显式输入且默认关闭；免费计划的时间和内存预算优先给确认计算。

相关：[[bounded-focus-and-reference-timeframes]]。


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
