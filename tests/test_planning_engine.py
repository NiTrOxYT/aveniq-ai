"""
Unit tests for Planning Engine, Planners, Dependencies, and Quality Gate.
"""

import unittest
from planning.engine.planning_engine import PlanningEngine
from planning.dependencies.graph_builder import DependencyGraphBuilder
from planning.utils.quality_gate import QualityGateVerifier

class TestPlanningEngineAndPlanners(unittest.TestCase):
    def test_planning_engine(self):
        engine = PlanningEngine()
        pkg = engine.generate_planning_package("AI Agents in Enterprise Operations")
        self.assertIsNotNone(pkg)
        self.assertEqual(pkg.topic, "AI Agents in Enterprise Operations")
        self.assertGreater(len(pkg.deliverables), 0)
        self.assertTrue(pkg.quality_gate.passed)

    def test_dependency_graph(self):
        graph = DependencyGraphBuilder.build_graph()
        self.assertGreater(len(graph.nodes), 0)
        self.assertEqual(graph.max_dependency_depth, 6)
        self.assertIn("Master Planning Package", graph.critical_path)

if __name__ == "__main__":
    unittest.main()
