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
- 2026-07-16：严格实图复核发现“覆盖区间全部原始 K 线全局极值”是课件未规定的额外门槛；`SKHYNIXUSDT.P / 5m` 最后笔端后共有 573 个基础分型，287 个反向分型全部满足双距离，却全部被该门槛否决，导致笔停滞 1,657 根 K 线并连锁清空线段、走势与点位的当前绘图。现改回课件步骤：同型分型保留更极端者，异型分型只校验合成与原始双距离。
- 2026-07-17：修复版在 `SKHYNIXUSDT.P / Binance / 5m / 5D` 独立显示并重载后恢复约 `3906` 根合成 K、`471` 笔和 `55` 条线段；目标蓝色线段像素由修复前 `0` 恢复为 `30`。实图证据为 `docs/test-evidence/2026-07-16-course-v2-missing-drawings-5d-repro.jpg` 与 `docs/test-evidence/2026-07-17-course-v2-fixed-drawings-5d-reload-final.jpg`。
