---
id: divergence-comparison-visualization
title: "背驰比较线必须对应实际强度比较段"
category: decision
status: active
tags: [divergence, rendering, performance]
created: "2026-07-27T17:44:12"
updated: "2026-07-27T17:44:12"
---

## compiled_truth

当前背驰算法只保留两类事件：`kind == 1` 是单中枢进入段与离开段减弱（盘背），`kind == 2` 是多中枢趋势背驰。绘图不得创造第三种算法身份，也不得改变背驰、买卖点、证据或提醒状态。

背驰比较线必须连接算法实际参与 MACD 强度比较的 `enteringUnit.endTime/endPrice` 与 `leavingUnit.endTime/endPrice`。趋势背驰的 `firstEnteringUnit` 用于完整走势追踪，不是强度比较段，不能作为比较线起点。层级数据源固定为：T0 使用 `segmentsS`，T1 使用 `movementsT0`，T2 使用 `movementsT1`，T3 使用 `movementsT2`。

视觉状态必须区分候选、已确认有效、失效候选和已失效历史。候选使用橙色虚线，确认有效使用层级色实线，失效候选使用 warning 色虚线，已失效历史使用弱化点线并只在非交易视图保留。标签和 tooltip 必须披露比较单元索引、中枢来源、MACD 面积比、DIF 附加证据以及有效性状态。

背驰比较线使用独立 `polyline` 配额，最多显示焦点四层各 12 条，总数不超过 48，不占用笔、线段、买卖点失效边界和情景使用的 `line` 配额。该配额隔离只解决背驰连接线的对象竞争；全局 line/label/box 每 tick 删除重建仍是后续性能工作。

相关：[[current-pine-observable-baseline]]、[[resource-priorities-over-lifecycle-history]]。


## timeline

- time: 2026-07-27T17:44:12
  kind: decision
  summary: "Created this page: 背驰比较线必须对应实际强度比较段"
  source: "2026-07-27 chanlun.pine 绘图审查与修复"
  affects: [divergence-comparison-visualization]

- time: 2026-07-27T17:44:12
  kind: decision
  summary: "确立背驰比较端点、状态样式和独立 polyline 预算"
  source: "2026-07-27 chanlun.pine 绘图审查与修复"
  affects: [divergence-comparison-visualization]
