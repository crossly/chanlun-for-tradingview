---
id: performance-baseline-indicator
title: "单周期 course-v2 性能基线指标"
category: project
status: archived
tags: [performance, pine, course-v2]
created: "2026-07-27T14:18:51"
updated: "2026-07-27T16:52:32"
---

## compiled_truth

该独立实验指标及其专用契约测试已删除，不再是当前代码、测试、文档或路线图的一部分。生产性能结论已重新基于 `chanlun.pine` 静态审查校准到 [[resource-priorities-over-lifecycle-history]]；本页仅作为 Brain append-only 历史的归档墓碑保留。


## timeline

- time: 2026-07-27T14:18:51
  kind: decision
  summary: "Created this page: 单周期 course-v2 性能基线指标"
  source: "当前 chanlun.pine 审核与性能基线实现"
  affects: [performance-baseline-indicator]

- time: 2026-07-27T14:18:52
  kind: decision
  summary: "记录独立性能基线的范围与非等价边界"
  source: chanlun-performance-baseline.pine
  affects: [performance-baseline-indicator]

- time: 2026-07-27T14:29:40
  kind: decision
  summary: "记录新笔边界重建的累计次数与最近 bar"
  source: chanlun-performance-baseline.pine
  affects: [performance-baseline-indicator]

- time: 2026-07-27T14:40:10
  kind: decision
  summary: "固定对象池替代删除后重建，保持实时候选可见"
  source: chanlun-performance-baseline.pine
  affects: [performance-baseline-indicator]

- time: 2026-07-27T14:58:16
  kind: decision
  summary: "线段真实区间高低值合并为单次子笔扫描"
  source: chanlun-performance-baseline.pine
  affects: [performance-baseline-indicator]

- time: 2026-07-27T15:01:57
  kind: decision
  summary: "保留已确认线段前缀，只重建末尾候选线段"
  source: chanlun-performance-baseline.pine
  affects: [performance-baseline-indicator]

- time: 2026-07-27T15:05:19
  kind: decision
  summary: "面板显示线段可变尾部重建笔数，不混入 T0 扫描"
  source: chanlun-performance-baseline.pine
  affects: [performance-baseline-indicator]

- time: 2026-07-27T15:13:55
  kind: decision
  summary: "中枢重叠与离开扫描复用局部真实高低值"
  source: chanlun-performance-baseline.pine
  affects: [performance-baseline-indicator]

- time: 2026-07-27T16:21:45
  kind: decision
  summary: "记录生产指标实时全量重建与对象 churn 的审查结论"
  source: "2026-07-27 chanlun.pine 算法与性能审查"
  affects: [performance-baseline-indicator]

- time: 2026-07-27T16:48:31
  kind: reversal
  summary: "独立性能基线指标及其契约测试已按要求移除；该页不再属于当前项目知识"
  source: brain archive-page
  affects: [performance-baseline-indicator]

- time: 2026-07-27T16:52:32
  kind: decision
  summary: "移除归档页中的实验实现细节，仅保留删除事实"
  source: "2026-07-27 用户删除要求"
  affects: [performance-baseline-indicator]
