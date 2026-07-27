---
slug: flow
title: Key flows
role: key flows
updated: "2026-07-27T16:48:31"
---

# Key flows

## 已收盘与活动状态

```mermaid
sequenceDiagram
  participant TV as TradingView
  participant F as 焦点引擎
  participant R as 参考周期引擎
  participant H as 结构层级
  participant O as 展示与提醒
  TV->>F: 已收盘焦点 OHLC
  F->>F: 合成 K -> 分型 -> 笔
  TV->>R: 已收盘参考柱 [1]
  R->>R: 各周期独立摄入
  TV->>F: 活动焦点 OHLC
  F->>F: 复制已确认尾部并形成隔离候选
  F->>H: 重建 S 与 T0-T3
  R->>H: dirty 时重建各自 T0-T2
  H->>O: 证据 共振 区间套 情景
  O-->>TV: 有界几何和状态面板
  O-->>TV: 经筛选的去重 alert JSON
```

## 时间与确认规则

- `structureTime` 是理论结构端点时间；`confirmationTime` 是全部确认条件首次可知时间。
- 已确认结构应冻结；候选结构可以移动、被替换或失效。
- 默认提醒只发送确认事件；候选提醒必须显式开启。
- 参考周期只使用其自身已收盘柱，不构造未收盘参考预览。
- 非标准图表停止焦点确认和参考周期分析。

## 当前实现代价

活动焦点 K 每个 tick 都执行历史数组复制、完整层级重建、证据组合及可见对象重建。该路径保证候选即时可见，但尚未有 TradingView profiler 证据证明它在最重配置下满足预算。
