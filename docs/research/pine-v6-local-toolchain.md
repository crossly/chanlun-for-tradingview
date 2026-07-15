# Pine Script v6 本地编译与验证工具链调研

调研日期：2026-07-15

## 结论

TradingView **没有在公开文档中提供受支持的 Pine Script v6 本地编译器、CLI 或编译 API**。官方将 Pine 定义为云端语言，脚本运行在 TradingView 服务器；受支持的编译入口是网页 Pine Editor 的保存或“Add to chart”操作。因此，本项目不能诚实地交付一个与 TradingView 等价的本地 Pine v6 编译器。[TradingView: Welcome][tv-welcome] [TradingView: Script compilation][tv-compilation]

官方编译器把源码转换成 tokenized Intermediate Language（IL），但官方同时明确说明，用户无法查看脚本的编译形式，也无法查看其 IL token 数。没有公开的 IL/bytecode 格式、导出命令或可部署的本地 Pine runtime；TradingView 发布脚本时复制的仍是源码，而不是可下载的编译包。[TradingView: Compiled tokens][tv-il] [TradingView: Publishing scripts][tv-publishing]

本项目的现实方案应是：

1. 交付单文件 Pine v6 源码，作为唯一产品代码。
2. 自建轻量 TypeScript 预检，检查本项目约束和明显错误，但不冒充 Pine 类型检查器。
3. 可选采用 PineTS 做本地转译和确定性 OHLC 数据上的运行冒烟测试；其结果只作辅助证据。
4. 每次发布仍必须在 TradingView Pine Editor 中成功保存、编译并添加到图表，作为权威门禁。
5. 不调用 TradingView 未公开的内部端点，不尝试提取或复刻官方 IL。

PineTS 是目前最接近本项目需求、且仍活跃维护的社区实现，但它不能替代官方编译器：原生 Pine 输入仍被项目标为 experimental；完整 v6 兼容仍在路线图；没有完整 Pine 类型/qualifier 检查；部分语言特性和 API 尚未完成。[PineTS README][pinets-readme] [PineTS language coverage][pinets-language] [PineTS request coverage][pinets-request]

## 官方编译与运行边界

### 是否存在官方本地编译器、CLI 或 API

截至调研日期，TradingView 的公开 Pine 文档没有提供本地编译器、命令行工具或编译 API。这个结论应严谨地表述为“**官方公开、受支持的接口不存在**”，而不是声称 TradingView 内部没有编译服务。证据如下：

- Pine 官方欢迎页明确称 Pine 是 cloud-based，工具运行在 TradingView servers。[TradingView: Welcome][tv-welcome]
- 官方入门流程说明，Pine Editor 在保存图表中已加载脚本的新版本时自动完成 write/compile/run；脚本保存到 TradingView 的云服务器。[TradingView: First indicator][tv-first-indicator]
- 官方限制页明确规定，编译发生在从 Pine Editor 保存脚本或把脚本添加到图表时。[TradingView: Script compilation][tv-compilation]
- v5 到 v6 的官方转换器也位于 Pine Editor 中，并要求原 v5 脚本先成功编译。[TradingView: Migrating to v6][tv-migration]

TradingView Advanced Charts 和 Trading Platform 不能充当本地 Pine runtime。官方文档明确写明这些库不支持 Pine Script，自定义指标必须使用其 JavaScript API 重写。[TradingView: Custom indicators][tv-custom-studies]

### Pine 编译成什么

官方只公开了以下编译模型：

- 编译器把脚本转换为 tokenized IL。
- 每个指标、策略或库的编译形式最多 100,000 IL tokens；导入库后的总量最多 1,000,000 tokens。
- 用户无法查看编译形式或 IL token 数。
- 未使用的变量、函数和类型可以在最终 IL 中被删除。

这些事实来自官方“Compiled tokens”说明。[TradingView: Compiled tokens][tv-il]

因此，IL 只是 TradingView 平台内部的实现形式，不是公开的可部署 bytecode。不能从官方文档推导其 schema、序列化格式、虚拟机指令集或兼容性承诺，也不存在把 `.pine` 编译成可在免费版外部加载的公开 artifact 的受支持流程。

### 权威验证入口

权威语法、类型、重载、qualifier、资源限制及实际图表执行验证只能由 TradingView 编译器完成。发布门禁应要求：

- 文件以 `//@version=6` 编译器注解声明版本。
- Pine Editor 保存后无编译错误。
- “Add to chart”成功，指标在标准 OHLC 图表上运行。
- 关键周期和输入组合不会触发运行时错误或资源限制。

官方教程说明 `//@version=6` 是选择 v6 的编译器注解，也说明保存和 Add to chart 的完整流程。[TradingView: First indicator][tv-first-indicator]

不建议把浏览器自动化称为“编译 API”。它最多是对受支持网页流程的脆弱自动操作，依赖登录状态和 UI；不能成为无需 TradingView 的本地编译器，也不应调用抓包得到的未公开后端接口。

## 候选工具评估

| 工具 | 实现语言 | 许可证 | 最近活动/版本 | v6 语法与类型检查 | 运行覆盖 | 对本项目的结论 |
| --- | --- | --- | --- | --- | --- | --- |
| [PineTS][pinets-repo] | TypeScript | AGPL-3.0-only 或商业许可 | [`0.9.29`][pinets-registry]，npm 发布于 2026-07-13；同日源码提交 | 原生 v5/v6 输入为 experimental；使用统一的 `>=5` 解析路径；没有完整 Pine 类型检查 | 支持时间序列、常用绘图、数组/Map/Matrix、`request.security()`/`security_lower_tf()` 及策略子集，但 API 并不完整 | **推荐作可选非权威 smoke runtime**；不能判定 TradingView 一定可编译 |
| [OpenPineScript][openpine-repo] | TypeScript + ANTLR | GPL-3.0 | 最近提交 2026-06-07 | 当前明确是 Pine **v2 Beta**；v3 是下一里程碑，v4 仍在后续路线图；没有 v6 | v2 转 JS、CSV 回测和部分 TA/runtime | **不适用** v6 项目 |
| [Pynescript][pynescript-repo] | Python + ANTLR | LGPL-3.0-or-later | `0.3.0`，最近提交 2025-12-18，包标为 Pre-Alpha | grammar 覆盖 enum/type/method/import/while 等现代语法，但项目没有声明完整 v6 兼容或语义类型检查 | 只提供 parse/dump/unparse；文档明确说明转 Python 示例不会生成可运行程序 | 可作 AST 实验工具；不应作为默认工具链或 compiler/runtime |
| [tiny-pine-script-parser][tiny-repo] | C++ + ANTLR | Apache-2.0 | 最近提交 2023-08-16 | grammar 使用分号、花括号、`function`/`return` 等与当前 Pine v6 不一致的形式 | 示例级 parser/evaluator | **排除** |
| [tradesdontlie/pinescript-compiler][tdl-repo] | TypeScript | **未提供许可证** | 最近提交 2026-03-03；`package.json` 为 private `0.1.0` | 提交信息声称 100% v6 parity，但同一提交的主规格仍列出大量缺失/部分项；semantic analyzer 源码存在但 `compile()` 未调用它 | 有自建 runtime/renderer 和测试，但不是已发布包，也没有 TradingView 权威一致性证明 | **排除集成**：无许可证即无明确复用授权；自述覆盖相互矛盾 |

### PineTS 详细判断

PineTS 当前 npm 元数据为 `0.9.29`，源码为 TypeScript，依赖 Acorn/Astring，自称可在 Node.js 和浏览器中转译并运行 Pine；包和仓库在调研日前两天仍有发布/提交，维护活跃度明显优于其他候选。[PineTS npm metadata][pinets-registry] [PineTS package metadata][pinets-package] [PineTS latest commit][pinets-commit]

它对本指标有价值的覆盖包括：

- 时间序列和历史引用执行模型。
- 数组、Map、Matrix 的大量方法。
- `line`、`box`、`label`、`table` 的大部分创建/更新 API。
- `request.security()` 和 `request.security_lower_tf()`。
- UDT、enum 和部分 method/object 支持。
- 自定义 OHLCV 数据运行，适合用 TypeScript fixture 做确定性冒烟测试。

这些能力可在项目自己的覆盖表中核查。[PineTS language coverage][pinets-language] [PineTS API coverage][pinets-api] [PineTS request coverage][pinets-request] [PineTS drawing coverage][pinets-line]

但它不能被称为 Pine v6 兼容编译器，原因是：

- README 将 native Pine v5/v6 标为 experimental，路线图仍以“Pine Script v6 full compatibility”为目标。[PineTS README][pinets-readme]
- 当前 parser 对版本号只检查 `version >= 5` 后进入同一解析路径；它不是按 v6 官方版本规则隔离的 grammar，因此“本地接受”不等于“官方 v6 接受”。[PineTS version dispatch][pinets-version-dispatch]
- 覆盖表把类型系统描述为 native JS/TS；源码中的 `TypeInferencePass` 明确是只为 `int / int` 语义建立的最小 `int/notint` lattice，而不是 Pine 的完整 base type + qualifier + overload 语义检查。[PineTS language coverage][pinets-language] [PineTS type inference][pinets-type-inference]
- 语言覆盖表仍列出 switch needs testing、objects/methods in progress、imports planned。该表部分状态与近期 changelog 有滞后，因此应把它看作“至少这些区域没有稳定完整承诺”，而不是精确完成百分比。[PineTS language coverage][pinets-language] [PineTS changelog][pinets-changelog]
- `request.*` 只实现了 `security` 和 `security_lower_tf`；currency/dividends/earnings/economic/financial/seed/splits 等未实现。[PineTS request coverage][pinets-request]
- 个别绘图 API 仍有空缺，例如 label/table 的部分格式化函数。[PineTS label coverage][pinets-label] [PineTS table coverage][pinets-table]

本项目的核心用例主要是 indicator、数组/UDT、动态绘图和多周期 `request.security()`，因此 PineTS 足以成为“尽早发现解析失败、缺失内置函数和明显运行错误”的辅助工具；它不足以证明复杂递归结构、绘图对象生命周期、高周期确认语义和 TradingView 资源消耗完全一致。

### PineTS 许可证边界

PineTS `package.json` 声明 `AGPL-3.0-only`，仓库另提供商业许可证。项目自己的许可说明称，分发包含 PineTS 的应用或把它作为网络服务提供时需要遵守 AGPL 的源码义务，不能遵守时应取得商业许可。[PineTS package metadata][pinets-package] [PineTS dual license][pinets-license]

当前仓库没有项目许可证，因而现在不应直接 vendoring、修改或把 PineTS 打进可分发产品。推荐边界是：

- 先确定本仓库许可证是否与 AGPL-3.0 兼容，或取得 PineTS 商业许可。
- 未完成该决定前，把 PineTS 集成列为可选的开发工具实验，不提交其源码或构建产物。
- 即使只作开发依赖，也应保留版权/许可证文件并由项目负责人确认分发方式。
- 本报告只记录上游许可声明，不构成法律意见。

## 推荐工具链

### 1. 权威产品 artifact

仓库只把 `.pine` 文件视为可交付产品。不要生成或宣称存在“Pine bytecode”“本地 IL”或“可上传编译包”。

### 2. 本地源码预检

用仓库自有的 TypeScript 脚本做窄而可审计的检查：

- 必须且只能声明 `//@version=6`。
- 必须是 `indicator()`，而非 `strategy()` 或 `library()`。
- 禁止依赖外部 Pine library import，保证免费版单文件交付。
- 检查 `request.*` 调用、plot count、绘图对象上限等可静态估算预算。
- 检查本项目约定的确认/候选命名、报警 JSON 字段和禁止未来数据读取规则。
- 对无法准确判断的 Pine 类型和 overload 只报“需 TradingView 验证”，不伪造成功结论。

这些检查是项目 linter，不是 Pine compiler。

### 3. 本地语法解析与 subset execution

许可证问题解决后，固定 PineTS 精确版本，用 TypeScript 测试运行本指标的代表性子集：

- 包含关系、分型、笔、线段、中枢等纯算法路径使用合成 OHLC fixture。
- 至少覆盖数组/UDT/method、同柱多次更新、线/框/标签生命周期和 `request.security()`。
- PineTS 报错使本地 CI 失败；PineTS 成功只表示“社区 runtime smoke test 通过”，不授予官方编译通过状态。
- 对 PineTS 明确未实现或与 TradingView 不一致的路径标记 skip，并附上上游覆盖链接。

若许可证不合适，不建议从零重写整个 Pine v6 parser/runtime。可以只保留第 2 步的项目 linter，把执行测试放到指标内部的诊断 plot/table 以及 TradingView 手工验证中。

### 4. TradingView 权威发布门禁

每个候选发布版本执行：

1. 在标准 OHLC 图表的 Pine Editor 中载入完整 `.pine` 文件。
2. 保存，确认 v6 编译无错误。
3. Add to chart，检查默认配置和最重配置。
4. 在焦点周期及四个参考周期配置下检查运行时错误、超时、request 限额和绘图对象截断。
5. 记录验证日期、TradingView 显示的脚本版本、品种、周期和输入 preset。

这一步不能由 PineTS、Pynescript 或任何自建 parser 替代。

## 不推荐的方向

- **从零实现完整 Pine v6 编译器**：官方 grammar、完整类型/qualifier 规则、内置签名库、IL 格式和 runtime 都未公开；成本会远超指标本身，仍无法成为权威编译器。
- **调用未公开 TradingView 编译端点**：没有稳定性、兼容性或支持承诺，还会引入账户凭据和合规风险。
- **把 PineTS 成功等同于 TradingView 成功**：两者 parser、类型系统、runtime、市场数据和绘图实现不同。
- **采用 OpenPineScript**：活跃不代表版本适用；其当前目标仍是 Pine v2。
- **采用无许可证的 `tradesdontlie/pinescript-compiler`**：没有明确复用授权，且同一版本的“100% parity”提交信息与仓库规格相冲突。

## 最终建议

接受用户“不需要 Python 参考引擎”的要求：不建设 Python 行情参考实现。用 TypeScript 完成本地项目 linter 和测试 harness；在许可证允许时，以 PineTS 作为非权威 subset runtime；TradingView Pine Editor 始终是唯一权威编译器。

对交付措辞应统一为：**“提供 Pine v6 源文件、本地预检和社区 runtime 冒烟测试；最终兼容性由 TradingView 云端编译验证。”** 不应承诺本地生成 TradingView 可部署 IL 或实现 100% v6 编译等价。

## Sources

[tv-welcome]: https://www.tradingview.com/pine-script-docs/welcome/
[tv-first-indicator]: https://www.tradingview.com/pine-script-docs/primer/first-indicator/#the-pine-editor
[tv-compilation]: https://www.tradingview.com/pine-script-docs/writing/limitations/#script-compilation
[tv-il]: https://www.tradingview.com/pine-script-docs/writing/limitations/#compiled-tokens
[tv-publishing]: https://www.tradingview.com/pine-script-docs/writing/publishing/#source-code
[tv-migration]: https://www.tradingview.com/pine-script-docs/migration-guides/to-pine-version-6/#converting-v5-to-v6-using-the-pine-editor
[tv-custom-studies]: https://www.tradingview.com/charting-library-docs/latest/custom_studies/
[pinets-repo]: https://github.com/LuxAlgo/PineTS
[pinets-registry]: https://registry.npmjs.org/pinets/0.9.29
[pinets-readme]: https://github.com/LuxAlgo/PineTS/blob/9bc386f1105078c6bb2865c746b95ce729f4e97a/README.md
[pinets-package]: https://github.com/LuxAlgo/PineTS/blob/9bc386f1105078c6bb2865c746b95ce729f4e97a/package.json
[pinets-commit]: https://github.com/LuxAlgo/PineTS/commit/9bc386f1105078c6bb2865c746b95ce729f4e97a
[pinets-language]: https://github.com/LuxAlgo/PineTS/blob/9bc386f1105078c6bb2865c746b95ce729f4e97a/docs/lang-coverage.md
[pinets-api]: https://github.com/LuxAlgo/PineTS/blob/9bc386f1105078c6bb2865c746b95ce729f4e97a/docs/api-coverage.md
[pinets-request]: https://github.com/LuxAlgo/PineTS/blob/9bc386f1105078c6bb2865c746b95ce729f4e97a/docs/api-coverage/request.md
[pinets-line]: https://github.com/LuxAlgo/PineTS/blob/9bc386f1105078c6bb2865c746b95ce729f4e97a/docs/api-coverage/line.md
[pinets-label]: https://github.com/LuxAlgo/PineTS/blob/9bc386f1105078c6bb2865c746b95ce729f4e97a/docs/api-coverage/label.md
[pinets-table]: https://github.com/LuxAlgo/PineTS/blob/9bc386f1105078c6bb2865c746b95ce729f4e97a/docs/api-coverage/table.md
[pinets-version-dispatch]: https://github.com/LuxAlgo/PineTS/blob/9bc386f1105078c6bb2865c746b95ce729f4e97a/src/transpiler/pineToJS/pineToJS.index.ts
[pinets-type-inference]: https://github.com/LuxAlgo/PineTS/blob/9bc386f1105078c6bb2865c746b95ce729f4e97a/src/transpiler/analysis/TypeInferencePass.ts
[pinets-changelog]: https://github.com/LuxAlgo/PineTS/blob/9bc386f1105078c6bb2865c746b95ce729f4e97a/CHANGELOG.md
[pinets-license]: https://github.com/LuxAlgo/PineTS/blob/9bc386f1105078c6bb2865c746b95ce729f4e97a/LICENSE-COMMERCIAL.md
[openpine-repo]: https://github.com/be-thomas/OpenPineScript/tree/723f6d803df73010b75e5a55ced0bdb297f5850e
[pynescript-repo]: https://github.com/elbakramer/pynescript/tree/0b9b4d0b0cd40d7d98c939830ccd06527a90c4d5
[tiny-repo]: https://github.com/doublnt/tiny-pine-script-parser/tree/dafcb979ed53111792d16148a2a363b36640c585
[tdl-repo]: https://github.com/tradesdontlie/pinescript-compiler/tree/0e25e93c0606a5322db72458cd8386b815b26ea9
