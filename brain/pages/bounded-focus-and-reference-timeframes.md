---
id: bounded-focus-and-reference-timeframes
title: "焦点周期绑定图表，参考周期只使用已收盘结构"
category: decision
status: active
tags: [timeframe, confirmation, recursion]
created: "2026-07-27T13:14:28"
updated: "2026-07-27T13:14:28"
---

## compiled_truth

焦点周期始终是当前 TradingView 图表周期，完整历史结构只在焦点周期展示。最多四个参考周期必须唯一且严格高于图表周期；参考结果只在自身 K 线收盘后以无未来数据方式传入，未收盘参考状态不得参与确认共振或默认提醒。

焦点周期递归边界为 `T0-T3`，参考周期为 `T0-T2`。事件同时保留结构时间与焦点图首次可知的确认时间，防止从未完成高周期柱伪造低周期完整结构。

相关：[[course-v2-theory-authority]]、[[resource-priorities-over-lifecycle-history]]。


## timeline

- time: 2026-07-27T13:14:28
  kind: decision
  summary: "Created this page: 焦点周期绑定图表，参考周期只使用已收盘结构"
  source: "README, CONTEXT.md, ADR, git log"
  affects: [bounded-focus-and-reference-timeframes]

- time: 2026-07-27T13:14:28
  kind: decision
  summary: "从项目理论规范、ADR 与提交历史提炼持续约束"
  source: "README, CONTEXT.md, ADR, git log"
  affects: [bounded-focus-and-reference-timeframes]
