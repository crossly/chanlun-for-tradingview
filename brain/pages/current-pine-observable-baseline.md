---
id: current-pine-observable-baseline
title: "当前 Pine 可观察行为是算法优化回归基线"
category: decision
status: active
tags: [algorithm, performance, regression]
created: "2026-07-27T17:15:29"
updated: "2026-07-27T20:15:06"
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

- time: 2026-07-27T19:12:03
  kind: evidence
  summary: "第一性审查发现：展示资源裁剪会改写执行状态；升级确认的一类点可能生成确认时间倒置的二类点；背驰冻结分支跳过后续失效扫描；失效状态迁移未进入提醒去重身份；参考周期主证据与焦点操作摘要可能错配。"
  source: "2026-07-27 chanlun.pine 第一性代码审查"
  affects: [current-pine-observable-baseline, resource-priorities-over-lifecycle-history]

- time: 2026-07-27T20:15:06
  kind: evidence
  summary: "第一性状态机修复已落地：展示裁剪不再门控执行真值；升级确认二类点使用不早于一类点的首次可知时间；反向证明只跳过证明单元而不终止背驰失效扫描；提醒身份覆盖失效候选与失效；自动操作摘要保留参考 market/TF/Tn；绘图仅在投影脏键变化时重建。源码契约 33/33，TradingView 官方 translate_light 编译无 errors。"
  source: "2026-07-27 chanlun.pine 实现、本地 unittest、TradingView 官方编译响应"
  affects: [current-pine-observable-baseline, resource-priorities-over-lifecycle-history]
