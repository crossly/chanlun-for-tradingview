from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "chanlun.pine").read_text(encoding="utf-8")


class CourseV2ContractTest(unittest.TestCase):
    def test_only_course_new_stroke_is_exposed(self) -> None:
        self.assertIn('string THEORY_VERSION = "course-v2"', SOURCE)
        self.assertNotIn("strokeMode", SOURCE)
        self.assertNotIn('"stroke_mode"', SOURCE)
        self.assertNotIn('"修订笔"', SOURCE)
        self.assertNotIn('"严格笔"', SOURCE)

    def test_stroke_requires_both_distances_without_extra_raw_extreme_gate(self) -> None:
        self.assertIn("math.abs(newFractal.kPosition - lastEndpoint.kPosition) >= 3", SOURCE)
        self.assertIn("math.abs(newFractal.structureIndex - lastEndpoint.structureIndex) >= 4", SOURCE)
        self.assertIn("if enoughSyntheticBars and enoughRawBars", SOURCE)
        self.assertNotIn(
            "if enoughSyntheticBars and enoughRawBars and allowConfirmation",
            SOURCE,
        )
        self.assertNotIn("f_is_real_extreme", SOURCE)
        self.assertNotIn("rawRangeHigh", SOURCE)
        self.assertNotIn("rawRangeLow", SOURCE)

    def test_intrabar_opposite_fractal_creates_candidate_without_freezing_prefix(self) -> None:
        stroke_builder = re.search(
            r"f_update_strokes\(.*?\) =>(?P<body>.*?)\n\nf_extend_terminal_candidate",
            SOURCE,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(stroke_builder)
        body = stroke_builder.group("body")
        self.assertIn("if strokeCount > 0 and allowConfirmation", body)
        self.assertRegex(
            body,
            r"if enoughSyntheticBars and enoughRawBars[\s\S]*?"
            r"if strokeCount > 0 and allowConfirmation[\s\S]*?"
            r"array\.push\(strokes, nextStroke\)",
        )

    def test_segments_keep_full_child_range(self) -> None:
        self.assertIn(
            "[segmentHigh, segmentLow, segmentDifHigh, segmentDifLow] = "
            "f_children_stats(lowerUnits, startChild, endpointChild - 1)",
            SOURCE,
        )
        self.assertNotIn("f_children_range_high", SOURCE)
        self.assertNotIn("f_children_range_low", SOURCE)
        self.assertIn("float rangeHigh", SOURCE)
        self.assertIn("float rangeLow", SOURCE)

    def test_dif_extremes_are_scanned_once_then_composed(self) -> None:
        self.assertIn("float difHigh", SOURCE)
        self.assertIn("float difLow", SOURCE)
        self.assertIn("f_dif_bounds", SOURCE)
        self.assertIn("f_apply_raw_strength", SOURCE)
        self.assertIn("f_extend_stroke_strength", SOURCE)
        self.assertIn("f_apply_composite_strength", SOURCE)
        self.assertNotIn("f_unit_dif_extreme", SOURCE)

        composite_builder = re.search(
            r"f_apply_composite_strength\(.*?\) =>(?P<body>.*?)"
            r"\n\nf_update_strokes",
            SOURCE,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(composite_builder)
        self.assertNotIn("array<float> difValues", composite_builder.group("body"))
        self.assertIn(
            "candidateUnit := "
            "f_apply_raw_strength(candidateUnit, posAreaCums, negAreaCums, difValues)",
            SOURCE,
        )

    def test_center_relation_and_expansion_use_course_v2_ranges(self) -> None:
        self.assertIn("current.dd > previous.gg ? 1 : current.gg < previous.dd ? -1 : 0", SOURCE)
        self.assertIn("not coreOverlap and not coreTouches and volatilityOverlap", SOURCE)
        self.assertIn("lowerComponentCount >= 9", SOURCE)

    def test_trend_divergence_is_traceable_and_binds_third_point(self) -> None:
        for field in (
            "comparisonCenter",
            "firstEnteringUnit",
            "enteringUnit",
            "leavingUnit",
            "thirdPointUnit",
        ):
            self.assertRegex(SOURCE, rf"\b{field}\b")
        self.assertIn("confirmedThirdPoint and not na(leavingIndex)", SOURCE)
        self.assertIn("array.get(centers, comparisonCenter).startChild", SOURCE)

    def test_points_support_weak_and_cross_level_second_class(self) -> None:
        self.assertIn("int sourceLayer", SOURCE)
        self.assertIn("int relativePosition", SOURCE)
        self.assertIn("array<BuySellPoint> lowerPoints", SOURCE)
        self.assertNotIn("holdsExtreme", SOURCE)
        self.assertIn("pointConfirmed = currentCenter.leaveState == 2 and retest.confirmed", SOURCE)
        self.assertIn("possibleAdvance.startTime >= lowerFirst.structureTime", SOURCE)

    def test_second_class_invalidation_requires_completed_opposing_movement(self) -> None:
        self.assertIn("array<Unit> completedMovements", SOURCE)
        self.assertIn("bool completedOpposingMovement", SOURCE)
        self.assertIn("breakMovement.startTime >= currentPoint.structureTime", SOURCE)
        self.assertNotIn("bool confirmedPostPointAdvance", SOURCE)
        self.assertNotIn(
            "currentPoint.pointClass == 2 and not na(currentPoint.invalidationPrice)",
            SOURCE,
        )

    def test_focus_and_reference_recursion_are_bounded(self) -> None:
        focus_builder = re.search(
            r"f_build_focus_hierarchy\(.*?\) =>(?P<body>.*?)// -----------------------------------------------------------------------------",
            SOURCE,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(focus_builder)
        focus_levels = re.findall(
            r"f_build_centers\((?:segments|movements[0-2]), centers([0-3]), ([0-3])\)",
            focus_builder.group("body"),
        )
        self.assertEqual(focus_levels, [("0", "0"), ("1", "1"), ("2", "2"), ("3", "3")])
        self.assertIn("engine.centersT2", SOURCE)
        self.assertNotIn("engine.centersT3", SOURCE)

    def test_reference_requests_keep_only_confirmed_structure_state(self) -> None:
        reference_source = re.search(
            r"f_reference_source\(\) =>(?P<body>.*?)\n\nf_contains",
            SOURCE,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(reference_source)
        self.assertIn("time[1]", reference_source.group("body"))
        self.assertNotIn("referencePreview", SOURCE)
        self.assertNotIn("f_copy_reference_engine", SOURCE)

    def test_completion_requires_a_qualified_reverse_component(self) -> None:
        self.assertIn("f_is_qualified_reverse_component", SOURCE)
        self.assertIn("proof.layer == expectedLayer", SOURCE)
        self.assertIn("proof.lastChild - proof.firstChild + 1 >= 3", SOURCE)
        self.assertIn("bool endpointFrozenByReverse", SOURCE)
        self.assertIn("if current.confirmed and not endpointFrozenByReverse", SOURCE)

    def test_level_promotion_completes_state_without_bootstrapping_components(self) -> None:
        self.assertIn("int promotionConfirmationTime", SOURCE)
        self.assertIn("int completionProof", SOURCE)
        self.assertIn("sourceCenter.expansionConfirmed", SOURCE)
        self.assertIn("MOVEMENT_COMPLETED_BY_PROMOTION", SOURCE)
        self.assertNotIn("expansionConfirmed or hasReverseProof", SOURCE)
        self.assertIn("promotion_does_not_bootstrap_parent_components", SOURCE)

    def test_level_promotion_links_contained_trend_centers_independently(self) -> None:
        promotion_builder = re.search(
            r"f_link_center_promotions\(.*?\) =>(?P<body>.*?)\n\nf_is_qualified_reverse_component",
            SOURCE,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(promotion_builder)
        body = promotion_builder.group("body")
        self.assertIn("for lowerIndex = 0 to lowerCount - 1", body)
        self.assertIn(
            "parent.startTime <= current.startTime and parent.endTime >= current.endTime",
            body,
        )
        self.assertNotIn("if current.expansionCandidate", body)

    def test_divergence_must_match_movement_kind_and_direction(self) -> None:
        divergence_builder = re.search(
            r"f_build_divergences\(.*?\) =>(?P<body>.*?)\n\nf_build_completed_movements",
            SOURCE,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(divergence_builder)
        divergence_body = divergence_builder.group("body")
        self.assertIn("int trendDirection = 0", divergence_body)
        self.assertIn(
            "bool departureMatchesStructure = trendCenterCount == 1 or trendDirection == departureDirection",
            divergence_body,
        )
        self.assertIn(
            "if departureMatchesStructure and not na(enteringIndex)",
            divergence_body,
        )

        trend_builder = re.search(
            r"f_get_trend_state\(.*?\) =>(?P<body>.*?)\n\nf_unit_confirmation_time",
            SOURCE,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(trend_builder)
        trend_body = trend_builder.group("body")
        self.assertIn(
            "bool divergenceMatchesMovement = latest.kind == kind and latest.direction == direction",
            trend_body,
        )
        self.assertIn(
            "direction := current.leaveDirection != 0 ? current.leaveDirection : current.failedDeparture ? current.failedLeaveDirection : 0",
            trend_body,
        )
        self.assertIn(
            "latest.centerIndex == lastCenter and latest.valid and divergenceMatchesMovement",
            trend_body,
        )


    def test_departure_detection_is_direction_aware(self) -> None:
        # Leaving units start inside the core, so whole-unit separation
        # misidentifies the reverse retest as the departure.
        self.assertIn("f_unit_cross_side", SOURCE)
        self.assertIn("f_retest_holds_outside", SOURCE)
        self.assertNotIn("f_unit_center_side", SOURCE)
        self.assertIn(
            "unit.direction == 1 and f_unit_high(unit) > zg ? 1 : unit.direction == -1 and f_unit_low(unit) < zd ? -1 : 0",
            SOURCE,
        )
        # a failed retest that crosses the opposite boundary immediately
        # becomes the new departure candidate
        self.assertIn("int reverseSide = f_unit_cross_side(current, newCenter.zd, newCenter.zg)", SOURCE)

    def test_macd_area_uses_prefix_sums(self) -> None:
        self.assertIn("f_push_macd_cums", SOURCE)
        self.assertIn("posAreaCums", SOURCE)
        self.assertIn("negAreaCums", SOURCE)
        self.assertNotIn("array<float> histValues", SOURCE)

    def test_evidence_identity_includes_structure_time(self) -> None:
        self.assertIn(
            "current.confirmed == incoming.confirmed and current.structureTime == incoming.structureTime",
            SOURCE,
        )

    def test_candidate_extension_refreshes_reference_hierarchy(self) -> None:
        stroke_builder = re.search(
            r"f_update_strokes\(.*?\) =>(?P<body>.*?)\n\nf_extend_terminal_candidate",
            SOURCE,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(stroke_builder)
        body = stroke_builder.group("body")
        self.assertEqual(body.count("changed := true"), 3)
        more_extreme_branch = re.search(
            r"if moreExtreme or equalAndLater(?P<branch>.*?)\n        else\n",
            body,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(more_extreme_branch)
        self.assertIn("changed := true", more_extreme_branch.group("branch"))
        self.assertIn(
            "state.structuresDirty := state.structuresDirty or structuresChanged",
            SOURCE,
        )

    def test_reliable_start_uses_first_center_confirmation_time(self) -> None:
        reliable_builder = re.search(
            r"f_reliable_confirmed_center_time\(.*?\) =>(?P<body>.*?)"
            r"\n\nf_center_relation",
            SOURCE,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(reliable_builder)
        self.assertIn(
            "reliableTime := na(third.confirmationTime) ? "
            "third.endTime : third.confirmationTime",
            reliable_builder.group("body"),
        )
        self.assertIn(
            "reliableStartTime := "
            "f_reliable_confirmed_center_time(segmentsS, MACD_WARMUP_BARS)",
            SOURCE,
        )
        self.assertNotIn("reliableStartTime := time", SOURCE)

    def test_seed_direction_updates_incrementally_without_preview_copies(self) -> None:
        seed_builder = re.search(
            r"f_seed_direction_step\(.*?\) =>(?P<body>.*?)\n\nf_ingest_kbar",
            SOURCE,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(seed_builder)
        self.assertNotIn("for ", seed_builder.group("body"))
        self.assertIn("float seedClusterHigh", SOURCE)
        self.assertIn("float seedClusterLow", SOURCE)
        self.assertNotIn("previewPendingHighs", SOURCE)
        self.assertNotIn("previewPendingLows", SOURCE)

    def test_execution_policy_derives_state_without_changing_structure_truth(self) -> None:
        for constant in (
            "EXECUTION_DATA_INSUFFICIENT",
            "EXECUTION_OBSERVE",
            "EXECUTION_WAIT_CONFIRMATION",
            "EXECUTION_READY",
            "EXECUTION_CONFLICT",
        ):
            self.assertIn(f"int {constant}", SOURCE)

        builder = re.search(
            r"f_build_execution_state\(.*?\) =>(?P<body>.*?)\n\nf_execution_status_summary",
            SOURCE,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(builder)
        body = builder.group("body")
        self.assertIn("if reliable and not resourceClipped", body)
        self.assertIn("primary.confirmed and primary.kind >= 11 and not primary.invalidationCandidate", body)
        self.assertIn("candidate.marketTimeframe == primary.marketTimeframe and candidate.layer == primary.layer", body)
        self.assertIn("candidate.confirmed and candidate.direction == -primary.direction", body)
        self.assertIn("math.abs(primary.confirmationPrice - primary.invalidationPrice)", body)
        self.assertNotIn("f_build_points(", body)
        self.assertNotIn("f_build_divergences(", body)

    def test_trading_dashboard_discloses_execution_state_and_risk_boundary(self) -> None:
        self.assertIn("ExecutionState executionState = f_build_execution_state(activeEvidence, executionReliable, resourceClipped)", SOURCE)
        self.assertIn('"结构状态"', SOURCE)
        self.assertIn('"主要证据"', SOURCE)
        self.assertIn('"同 TF 同 Tn 冲突"', SOURCE)
        self.assertIn('"失效 / 风险距离"', SOURCE)
        self.assertIn("风险距离仅为确认价与结构失效边界的价格距离；不表示仓位或收益。", SOURCE)

    def test_trading_dashboard_discloses_confirmed_cross_timeframe_opposition(self) -> None:
        self.assertIn("bool crossTimeframeOpposition = false", SOURCE)
        self.assertIn("resonance.scope == 2 and resonance.confirmed and resonance.direction == -executionState.direction", SOURCE)
        self.assertIn('" · 跨周期反向确认"', SOURCE)
        self.assertIn("它不改写当前结构身份", SOURCE)

    def test_trading_panel_is_movable_and_uses_readable_text(self) -> None:
        self.assertIn('string tradingPanelPosition = input.string("左中", "交易面板位置"', SOURCE)
        self.assertIn('"左上", "左中", "左下", "右上", "右中", "右下"', SOURCE)
        self.assertIn("table.set_position(statusPanel, panelPosition)", SOURCE)
        self.assertIn("table.cell_set_text_size(statusPanel, 0, panelRow, size.small)", SOURCE)
        self.assertIn("table.cell_set_text_size(statusPanel, 1, panelRow, size.small)", SOURCE)

    def test_structural_explanations_preserve_theory_and_expose_point_causes(self) -> None:
        self.assertNotIn("float departureExtreme", SOURCE)
        self.assertIn('state.kind == 2 ? "趋势资格" : "盘整资格"', SOURCE)
        self.assertIn('state.status == MOVEMENT_QUALIFIED ? "未完成"', SOURCE)
        self.assertIn('"趋背#" + str.tostring(current.sourceDivergence)', SOURCE)
        self.assertIn('"1点#" + str.tostring(current.linkedFirstPoint)', SOURCE)
        self.assertIn('"·首回试"', SOURCE)
        self.assertIn('"\\n因果: " + causeText', SOURCE)

    def test_divergence_tooltip_distinguishes_trend_completion_from_consolidation_weakness(self) -> None:
        self.assertIn('current.kind == 2 ? "趋势完成候选，等待反向确认" : "单中枢减弱，不直接确认一类点"', SOURCE)
        self.assertIn('"\\n解释: " + usageText', SOURCE)
        self.assertIn("string divergenceStyle = current.direction == 1 ? label.style_label_down : label.style_label_up", SOURCE)

    def test_divergence_draws_the_actual_strength_comparison_units(self) -> None:
        divergence_drawer = re.search(
            r"f_draw_divergences\(.*?\) =>(?P<body>.*?)\n\nf_draw_points",
            SOURCE,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(divergence_drawer)
        body = divergence_drawer.group("body")
        self.assertIn("Unit entering = array.get(units, current.enteringUnit)", body)
        self.assertIn("Unit leaving = array.get(units, current.leavingUnit)", body)
        self.assertIn(
            "chart.point.from_time(entering.endTime, entering.endPrice)",
            body,
        )
        self.assertIn(
            "chart.point.from_time(leaving.endTime, leaving.endPrice)",
            body,
        )
        self.assertIn("polyline.new(comparisonPoints", body)
        self.assertNotIn("current.firstEnteringUnit", body)

        for call in (
            "f_draw_divergences(segmentsS, divergencesT0",
            "f_draw_divergences(movementsT0, divergencesT1",
            "f_draw_divergences(movementsT1, divergencesT2",
            "f_draw_divergences(movementsT2, divergencesT3",
        ):
            self.assertIn(call, SOURCE)

    def test_divergence_visual_state_distinguishes_invalid_history(self) -> None:
        self.assertIn(
            "bool invalid = current.confirmed and not current.valid",
            SOURCE,
        )
        self.assertIn(
            'string stateText = invalid ? "失" : '
            'current.invalidationCandidate ? "失候" : '
            'current.confirmed ? "确" : "候"',
            SOURCE,
        )
        self.assertIn(
            "string connectorStyle = invalid ? line.style_dotted",
            SOURCE,
        )
        self.assertIn("polyline.delete(array.get(divergenceConnectors, i))", SOURCE)
        self.assertIn("int MAX_DIVERGENCE_CONNECTORS = 48", SOURCE)
        self.assertIn(
            "array.size(connectors) < MAX_DIVERGENCE_CONNECTORS",
            SOURCE,
        )

    def test_center_tooltip_exposes_departure_and_retest_context(self) -> None:
        self.assertIn('current.leaveState == 2 ? "\\n离开确认: "', SOURCE)
        self.assertIn('"·回试#" + str.tostring(current.retestChild)', SOURCE)
        self.assertIn('"\\n离开候选: "', SOURCE)
        self.assertIn('"\\n离开失败: "', SOURCE)
        self.assertIn("+ departureText + promotionText", SOURCE)

    def test_operation_level_view_selects_one_structural_layer(self) -> None:
        self.assertIn('string operationLevel = input.string("自动", "操作级别"', SOURCE)
        self.assertIn('"自动", "T0", "T1", "T2", "T3"', SOURCE)
        self.assertIn("int operationLayer = operationLevel == \"自动\" ? automaticOperationLayer", SOURCE)
        self.assertIn('"操作结构"', SOURCE)
        self.assertIn('"操作点位"', SOURCE)
        self.assertIn("operationLabel + \"·\" + operationTrend + \" | \" + operationDivergence", SOURCE)



if __name__ == "__main__":
    unittest.main()
