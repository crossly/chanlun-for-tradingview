---
id: course-new-stroke-and-true-ranges
title: "只使用课件新笔并保存线段真实区间"
category: decision
status: active
tags: [stroke, segment, course-v2]
created: "2026-07-27T13:14:27"
updated: "2026-07-27T13:14:28"
---

## compiled_truth

成笔必须同时满足：异型笔端分型中心至少相隔三个合成 K 线位置，且实际端点原始索引至少相差四。笔端由基础分型与同型更极端替换确定；不再扫描两端之间原始 K 线的全局高低，也不提供修订笔或严格笔模式。

线段保留完整特征序列规则，并保存所有子笔到达的真实高低区间；上层中枢以该真实区间为输入。候选线段只能派生候选上层结构。此规则替代旧的多笔模式，修改任何端点筛选或上层范围前必须保持两种距离条件与真实区间来源。

相关：[[course-v2-theory-authority]]、[[bounded-focus-and-reference-timeframes]]。


## timeline

- time: 2026-07-27T13:14:27
  kind: decision
  summary: "Created this page: 只使用课件新笔并保存线段真实区间"
  source: "README, CONTEXT.md, ADR, git log"
  affects: [course-new-stroke-and-true-ranges]

- time: 2026-07-27T13:14:28
  kind: decision
  summary: "从项目理论规范、ADR 与提交历史提炼持续约束"
  source: "README, CONTEXT.md, ADR, git log"
  affects: [course-new-stroke-and-true-ranges]
