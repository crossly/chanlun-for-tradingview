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

    def test_stroke_requires_both_distances_and_real_extreme(self) -> None:
        self.assertIn("math.abs(newFractal.kPosition - lastEndpoint.kPosition) >= 3", SOURCE)
        self.assertIn("math.abs(newFractal.structureIndex - lastEndpoint.structureIndex) >= 4", SOURCE)
        self.assertRegex(
            SOURCE,
            r"enoughSyntheticBars and enoughRawBars and f_is_real_extreme\(",
        )
        self.assertIn("float rawRangeHigh", SOURCE)
        self.assertIn("float rawRangeLow", SOURCE)
        self.assertIn("current.rawRangeHigh > startPoint.price", SOURCE)

    def test_segments_keep_full_child_range(self) -> None:
        self.assertIn("f_children_range_high(lowerUnits, startChild, endpointChild - 1)", SOURCE)
        self.assertIn("f_children_range_low(lowerUnits, startChild, endpointChild - 1)", SOURCE)
        self.assertIn("float rangeHigh", SOURCE)
        self.assertIn("float rangeLow", SOURCE)

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
        self.assertIn('"a=" + f_indexed_unit_structure_id(', SOURCE)
        self.assertIn('"|3p=" + f_indexed_unit_structure_id(', SOURCE)

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

    def test_lifecycle_history_is_append_only(self) -> None:
        self.assertIn('"replaced"', SOURCE)
        self.assertIn('"invalidated"', SOURCE)
        self.assertIn("var array<LifecycleEvent> lifecycleEvents", SOURCE)
        self.assertNotIn("array.clear(lifecycleEvents)", SOURCE)
        self.assertNotIn("array.shift(lifecycleEvents)", SOURCE)
        event_type = re.search(
            r"type LifecycleEvent(?P<body>.*?)type ReferenceState",
            SOURCE,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(event_type)
        self.assertNotIn("marketTimeframe", event_type.group("body"))
        self.assertNotIn("structureKind", event_type.group("body"))
        self.assertNotIn("int layer", event_type.group("body"))

    def test_lifecycle_history_replays_during_historical_execution(self) -> None:
        self.assertIn("bool focusStructuresDirty", SOURCE)
        self.assertIn("state.structuresDirty", SOURCE)
        self.assertIn("previousFocusStructureSnapshots", SOURCE)
        self.assertIn("previousReferenceStructureSnapshots4", SOURCE)
        self.assertNotIn("bool lifecycleReplayStep", SOURCE)
        replay_block = re.search(
            r"if focusReplayDirty(?P<body>.*?)if barstate\.islast",
            SOURCE,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(replay_block)
        self.assertIn(
            "f_reconcile_lifecycle(previousFocusStructureSnapshots",
            replay_block.group("body"),
        )
        self.assertIn(
            "f_reconcile_lifecycle(previousReferenceStructureSnapshots4",
            replay_block.group("body"),
        )

    def test_realtime_preview_does_not_mutate_confirmed_lifecycle_history(self) -> None:
        preview_block = SOURCE.split("if barstate.islast", maxsplit=1)[1]
        self.assertNotIn("f_reconcile_lifecycle", preview_block)

    def test_lifecycle_reconcile_indexes_snapshot_slots(self) -> None:
        self.assertIn("map<string, int> previousIndexBySlot", SOURCE)
        self.assertIn("map<string, int> currentIndexBySlot", SOURCE)
        self.assertIn("map.get(previousIndexBySlot, incoming.slotId)", SOURCE)
        self.assertIn("map.get(currentIndexBySlot, old.slotId)", SOURCE)
        self.assertNotIn("for candidateIndex = 0 to previousCount - 1", SOURCE)

    def test_lifecycle_phase_reason_is_part_of_event_identity(self) -> None:
        self.assertIn('"|reason=" + reason', SOURCE)
        self.assertIn('"|sequence=" + str.tostring(sequence)', SOURCE)
        self.assertNotIn("f_lifecycle_occurrence", SOURCE)
        self.assertIn("old.reason != incoming.reason", SOURCE)

    def test_lifecycle_sources_use_stable_structure_ids(self) -> None:
        self.assertIn("f_unit_structure_id", SOURCE)
        self.assertIn("f_center_structure_id", SOURCE)
        self.assertIn('"first=" + f_indexed_unit_structure_id(', SOURCE)
        self.assertNotIn('"children=" + str.tostring(', SOURCE)
        self.assertNotIn('"components=" + str.tostring(', SOURCE)
        self.assertNotIn('"divergence=" + str.tostring(', SOURCE)

    def test_point_lifecycle_sources_preserve_causal_structure_ids(self) -> None:
        self.assertIn("f_divergence_structure_id", SOURCE)
        self.assertIn('"|divergence=" + causalSourceId', SOURCE)
        self.assertIn('"|first_point=" + causalSourceId', SOURCE)
        self.assertIn('"|center=" + causalSourceId', SOURCE)
        self.assertNotIn(
            'str.tostring(current.structureTime) + "@" + str.tostring(current.structureIndex)',
            SOURCE,
        )


if __name__ == "__main__":
    unittest.main()
