# 持久化四状态结构生命周期事件

分型端点、笔、线段、走势、背驰和买卖点统一保存 `candidate`、`confirmed`、`replaced`、`invalidated`。已确认结构冻结；候选替换和证据失效产生不可变历史事件，不能通过清空当前数组后重新推导替代。焦点周期与参考周期都在历史确认柱推进时重建并 reconcile，脚本重载由同一顺序重放迁移；`reason` 进入事件身份，使 `forming`、`qualified`、`completion_candidate`、`completed` 的阶段变化不会被相同外层状态吞掉。事件保存结构时间、首次可知时间、来源结构 ID 和状态原因，并使用 `TF + Tn + structure_id + theory=course-v2` 身份。
