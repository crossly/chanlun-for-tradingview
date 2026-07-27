---
id: current-pine-observable-baseline
title: "当前 Pine 可观察行为是算法优化回归基线"
category: decision
status: active
tags: [algorithm, performance, regression]
created: "2026-07-27T17:15:29"
updated: "2026-07-27T17:15:29"
---

## compiled_truth

算法与性能优化以当前生产 `chanlun.pine` 的可观察输出、状态迁移和确认边界作为唯一回归基线。`.scratch/` spec、`docs/adr/`、历史课件归纳和旧文档只提供背景，不得阻塞修复，也不得覆盖当前代码已经交付的行为。

“保持行为”不等于保留已识别错误。参考周期候选尾部变化未触发刷新、`reliableStartTime` 在重载后错误指向末根 K 等问题，应从当前状态模型的一致性出发修复，并用源码契约与相同 OHLC 输入的结构输出对照锁定新行为。性能优化必须保持已确认结构冻结、结构时间与确认时间分离、参考周期只消费已收盘柱、候选不进入默认提醒这些当前代码不变量。

实施顺序：先修复可观察正确性，再降低初始化、区间统计和 DIF 聚合成本，最后才考虑不可变确认前缀加可变尾部的增量层级引擎。TradingView profiler、Bar Replay、重载结果和源码契约是验证证据；spec/ADR 一致性不再是门禁。

相关：[[resource-priorities-over-lifecycle-history]]、[[bounded-focus-and-reference-timeframes]]、[[course-new-stroke-and-true-ranges]]。


## timeline

- time: 2026-07-27T17:15:29
  kind: decision
  summary: "Created this page: 当前 Pine 可观察行为是算法优化回归基线"
  source: "2026-07-27 用户决定与当前 chanlun.pine"
  affects: [current-pine-observable-baseline]

- time: 2026-07-27T17:15:29
  kind: decision
  summary: "确立当前生产 Pine 行为作为算法与性能优化的唯一回归基线"
  source: "2026-07-27 用户决定与当前 chanlun.pine"
  affects: [current-pine-observable-baseline]
