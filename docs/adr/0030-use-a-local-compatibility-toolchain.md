---
status: superseded by ADR-0032
---

# 交付 Pine v6 源码与本地兼容工具链

最终产品只使用单文件 Pine v6 指标，不建设 Python 参考引擎。仓库提供 TypeScript `pinec` CLI 执行项目静态规则、资源预算、未来数据约束、提醒契约及确定性 OHLC 冒烟运行，并在许可允许时固定 PineTS 作为实验性的本地解析/转译基础；本地成功不冒充官方兼容，发布仍须通过 TradingView Pine Editor 编译和 Add to chart。项目不调用未公开接口，也不尝试生成不可见的官方 IL。
