# 重建新笔与线段形态层

Type: task
Status: ready-for-agent
Blocked by:

## Goal

实现唯一课件新笔、候选生命周期、完整特征序列线段和线段真实价格区间。

## Acceptance

- 同时校验合成 K 线距离和原始 K 线距离。
- 删除旧笔模式输入及事件身份。
- 线段保留端点及全部子笔真实 `high/low`。
- 候选线段不能确认任何上层结构。
- 临时 Pine 夹具覆盖 spec 中 morphology seam。

## Comments

- 2026-07-16：唯一课件新笔双距离、真实极值、候选替换、完整特征序列线段及子笔真实区间已进入 `chanlun.pine`；本地契约测试通过。发布级临时 Pine morphology 夹具仍属于 ticket 05 的未过门禁。
- 2026-07-16：真实极值校验改为读取包含合并前完整原始 K 线覆盖区间的 `rawRangeHigh/rawRangeLow`，不再只依赖合成 K 线高低；最新源码仍待 ticket 05 官方重新编译。
- 2026-07-16：上述最新源码已由 TradingView 官方 Pine v6 编译并在 `SKHYNIXUSDT.P / 5m / 4 自动参考 / 2,000 K` 首次运行及重载通过；逐事件 morphology 合成夹具仍由 ticket 05 保持开放。
