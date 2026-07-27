---
id: resource-priorities-over-lifecycle-history
title: "确认真值优先于详细绘图和历史生命周期账本"
category: decision
status: active
tags: [performance, rendering, lifecycle, free-plan]
created: "2026-07-27T13:14:28"
updated: "2026-07-27T20:40:13"
---

## compiled_truth

TradingView 的编译 token、历史执行时间、实时 tick 时间、内存和绘图对象预算是彼此独立的发布约束。优化的算法真值来自当前 `chanlun.pine` 的可观察行为，而不是 `.scratch/` spec 或 `docs/adr/`。资源取舍顺序是：焦点周期确认真值、参考周期已收盘结构与共振、候选可见性、历史详细几何、情景与调试能力。

当前生产源码已经移除历史 lifecycle ledger、结构快照与逐边界 reconcile。该裁剪是现行交付边界，不再因旧 spec/ADR 的描述而阻塞优化。必须保持的当前代码不变量是：已确认结构冻结、结构/确认双时间戳、参考周期只读已收盘柱、候选不进入默认提醒。

首批修复已经落地：

1. 参考周期同型更极端分型移动末端候选笔时会设置 `structuresDirty`，候选 `S/Tn`、证据和候选提醒不再延迟到下一条新笔。
2. `reliableStartTime` 取最早可靠三构件中第三构件的实际确认时间，脚本重载后不再错误指向末根 K。
3. 初始方向发现使用增量包含簇状态；历史 pending K 只在方向首次确定时回放一次，活动柱预览也不再复制四个 pending 数组，初始化总成本由最坏平方降为线性。
4. `Unit` 保存可组合的 DIF 上下界。已确认线段与走势把 high/low 和 DIF 合并为一次子结构扫描；末端笔只扫描新增原始区间。高层候选的价格极值可能早于最后子结构，因此候选必须继续按自身真实 `startIndex..endIndex` 扫描 DIF，不能聚合结束点之后的子结构数据。

尚未处理的最大热点是最后柱每 tick 复制焦点数组并全量重建 `S/T0-T3`、背驰、点位和证据，以及展示层删除重建全部对象。后续方向是不可变已确认前缀加小型可变尾部，再配合绘图对象池；这些改造必须以相同 OHLC 输入下的结构身份、方向、价格、结构时间、确认时间和确认状态对照为约束。

相关：[[current-pine-observable-baseline]]、[[bounded-focus-and-reference-timeframes]]、[[course-new-stroke-and-true-ranges]]。


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

- time: 2026-07-27T17:10:14
  kind: decision
  summary: "补充第一性性能模型、可靠起点错误与稳定前缀优化方向"
  source: "2026-07-27 chanlun.pine 第一性算法与性能审查"
  affects: [resource-priorities-over-lifecycle-history]

- time: 2026-07-27T17:15:29
  kind: reversal
  summary: "撤销 spec/ADR 偏差阻塞后续性能优化的结论"
  source: "2026-07-27 用户决定"
  affects: [current-pine-observable-baseline]

- time: 2026-07-27T17:15:29
  kind: decision
  summary: "按当前 Pine 行为基线重排正确性与性能修复优先级"
  source: "2026-07-27 用户决定与 chanlun.pine 静态审查"
  affects: [resource-priorities-over-lifecycle-history]

- time: 2026-07-27T17:24:01
  kind: decision
  summary: "记录候选精确区间边界与首批正确性性能修复已落地"
  source: "2026-07-27 chanlun.pine 实现与源码契约"
  affects: [resource-priorities-over-lifecycle-history]

- time: 2026-07-27T17:28:07
  kind: evidence
  summary: "优化提交 958b1d1 已通过 TradingView 官方 Pine 编译"
  source: "2026-07-27 用户实测"
  affects: [current-pine-observable-baseline]

- time: 2026-07-27T20:15:21
  kind: evidence
  summary: "展示层新增投影脏键：同一根 K 内仅当焦点结构尾部、强度或层级投影变化时删除重建 line/label/box/polyline；买卖点标签同时受 detailBars 限制。焦点数组复制和 T0-T3 全量重建仍是下一阶段热点。"
  source: "2026-07-27 chanlun.pine 绘图优化与官方编译"
  affects: [resource-priorities-over-lifecycle-history]

- time: 2026-07-27T20:26:43
  kind: reversal
  summary: "撤回跨 tick 绘图投影脏键。Pine 在实时柱每次重算前 rollback 临时绘图对象，而 varip previousDrawingStateKey 逃逸 rollback，导致下一 tick 跳过重画并让线条一闪即逝。恢复每次 barstate.islast 执行重画；后续性能优化必须使用可持续对象池并在每 tick 重放 setter，不能用 varip 跳过绘图。"
  source: "2026-07-27 用户图表运行报告与 TradingView Pine 官方执行模型"
  affects: [resource-priorities-over-lifecycle-history, current-pine-observable-baseline]

- time: 2026-07-27T20:40:13
  kind: evidence
  summary: "新增默认快速、可选完整的绘图密度。快速标准预设把理论对象上界由约 480 line/388 label/43 box/40 polyline 降至 255/177/28/24，约减少 49% 对象创建；只裁剪旧几何，不改变计算、结构、证据、提醒和事件身份。官方 Pine 编译无 errors，实际图表加载耗时待用户复验。"
  source: "2026-07-27 绘图预算模型、本地 34 项契约与 TradingView 官方编译"
  affects: [resource-priorities-over-lifecycle-history, current-pine-observable-baseline]
