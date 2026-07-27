---
slug: background
title: Project background
role: project background
updated: "2026-07-27T16:52:32"
---

# Project background

## 为什么

本项目把《缠中说禅教你炒股票》108 课、原作者答疑和可复现课件口径落实为 TradingView 上可复核的结构指标。项目强调结构身份、候选与确认边界、双时间戳及资源限制，避免把不同流派的同名规则混入同一结果。

## 当前目标

- 交付单文件 Pine Script v6 指标 `chanlun.pine`，以 `course-v2` 为唯一生产理论口径。
- 在 TradingView 免费计划的编译 token、执行时间、内存和绘图对象预算内，保留焦点周期 `T0-T3`、最多四个参考周期 `T0-T2`、结构证据与提醒。
- 让候选结构、确认结构、可靠区间、详细绘图窗口和资源裁剪可审计。

## 非目标

- 不提供 `strategy()`、自动下单、仓位、止盈止损、收益曲线、胜率或策略回测。
- 不把行情周期 `TF` 固定映射为走势级别 `Tn`。
- 不在 Heikin Ashi、Renko、Kagi 等合成图表上产生确认信号。
- 不保留旧理论算法或独立实验指标作为生产兼容模式。

## 项目状态

核心 course-v2 引擎、交易视图和源码契约已存在；历史 lifecycle ledger 已从当前生产源码移除以降低编译与运行成本。TradingView 官方编译、逐事件 Pine 夹具、Bar Replay、完整事件快照和跨市场矩阵仍是未完成的发布证据，不能由本地源码测试替代。

## 目标使用者

[低置信度] README 没有冻结具体用户画像。可确认的使用者是希望在 TradingView 标准 K 线图表上复核严格缠论结构，并可能消费 webhook 结构事件的人；交易风格与自动化程度仍需维护者确认。
