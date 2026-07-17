# 验证 course-v2 生产指标

Type: task
Status: ready-for-agent
Blocked by: 04

## Goal

完成逐事件夹具、官方编译、Bar Replay、重载快照和跨市场发布矩阵。

## Acceptance

- 全部 spec validation seams 有可复现证据。
- 标准模式、四参考周期和 2,000 K 窗口稳定运行。
- 旧理论事件不会与 course-v2 事件去重冲突。
- 测试完成后移除所有临时指标。

## Comments

- 2026-07-16：本地 12 个源码契约测试通过；TradingView 官方编译通过，并在 `SKHYNIXUSDT.P / Bitget / 5m / 4 自动参考 / 2,000 K` 运行无错误。仍未完成逐事件 Pine 夹具、Premium Bar Replay、重载前后完整事件 ID 快照和 course-v2 跨市场矩阵，本 ticket 保持开放。
- 2026-07-16：最新本地源码契约为 13/13，通过原始覆盖极值、稳定来源 ID 与重复阶段迁移身份检查；这些审查后修复尚未经过 TradingView 官方重新编译，不能由前一版运行证据替代。
- 2026-07-16：本地源码契约增至 `17/17`；TradingView 官方接受 3,001 行最新源码。`SKHYNIXUSDT.P / Bitget / 5m / 4 自动参考 / 2,000 K` 首次运行等待约 23 秒、页面重载后再次等待约 25 秒，均无 `Runtime error` 或 `Memory limits exceeded`，面板恢复约 `4463` 个历史生命周期事件。证据为 `docs/test-evidence/2026-07-16-skhynix-5m-course-v2-memory-reload.png`，测试实例已移除。
- 2026-07-16：本 ticket 仍保持开放，剩余发布门禁是逐事件 morphology/走势/点位 Pine 夹具、Premium Bar Replay、重载前后完整事件 ID 逐项快照，以及 course-v2 完整跨市场矩阵；本地源码契约和单一 5m 烟雾/重载结果不能替代这些门禁。
- 2026-07-16：新增实际像素门禁复现“面板有结构计数但图上无笔/线段”。最小官方 Pine morphology 夹具确认最后笔停滞 1,657 根 K 线，最后笔端后 287 个满足双距离的反向分型被非课件的原始 K 全局极值门槛全部拒绝；生产修复已删除该门槛，待官方编译、实图像素、买卖点与重载复核后关闭本次回归项。
- 2026-07-17：本次绘图回归项已通过官方 Pine 编译、四参考周期、独立显示和页面重载复核。`SKHYNIXUSDT.P / Binance / 5m / 5D` 的蓝色线段像素从 `0` 恢复为重载后的 `30`，无 `Runtime error`；`BTCUSDT.P / Binance / 5m` 交易视图实际显示 `3类卖·T0·确认`。证据为 `docs/test-evidence/2026-07-17-course-v2-fixed-drawings-5d-reload-final.jpg` 与 `docs/test-evidence/2026-07-17-course-v2-btc-5m-trading-points-clear.jpg`。临时图表实例已移除，用户原指标已恢复。
