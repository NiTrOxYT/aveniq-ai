"""
Comprehensive Analytics Test Suite for AVENIQ Performance Analytics & Continuous Optimization Platform.
Tests MetricCollectors, AttributionGraph, KPIScorecards, BenchmarkEngine, OptimizationEngine, and Learning Integration.
"""

import unittest
from analytics.collectors.linkedin import LinkedInCollector, XCollector, WebsiteCollector
from analytics.attribution.attribution_graph import AttributionGraph
from analytics.kpi.scorecards import KPICalculator, KPIScorecardNormalizer
from analytics.optimization.scoring import CampaignScorer, BenchmarkEngine
from analytics.optimization.recommendation_engine import OptimizationEngine
from analytics.dashboard.models import ExecutiveDashboardBuilder

class TestAnalyticsPlatform(unittest.TestCase):
    def test_collectors(self):
        collector = LinkedInCollector()
        m = collector.collect("cmp_001", "pub_001")
        self.assertEqual(m.platform, "LinkedIn")
        self.assertGreater(m.reach.impressions, 0)
        self.assertGreater(m.business.leads, 0)

    def test_kpi_calculators(self):
        ctr = KPICalculator.calculate_ctr(240, 24500)
        self.assertEqual(ctr, 0.98)

        score = KPIScorecardNormalizer.normalize_to_score(85.0, 50.0, 100.0)
        self.assertEqual(score, 85.0)

    def test_attribution_graph(self):
        graph = AttributionGraph()
        c_node = graph.add_node("cmp_001", "Campaign", "Enterprise AI Series")
        r_node = graph.add_node("opt_rec_001", "Recommendation", "Technical Depth")
        graph.add_edge("cmp_001", "opt_rec_001", "INFORMS")

        origin = graph.trace_recommendation_origin("opt_rec_001")
        self.assertEqual(len(origin["originating_nodes"]), 1)
        self.assertEqual(origin["originating_nodes"][0]["id"], "cmp_001")

    def test_scoring_and_benchmarks(self):
        collector = LinkedInCollector()
        m = collector.collect("cmp_001", "pub_001")
        scores = CampaignScorer.calculate_scores(m)
        self.assertGreater(scores["overall_campaign_score"], 0.0)

        benchmark = BenchmarkEngine.benchmark_campaign(scores, m.business.leads)
        self.assertEqual(benchmark["benchmark_status"], "OUTPERFORMING")

    def test_optimization_and_learning_submission(self):
        collector = LinkedInCollector()
        m = collector.collect("cmp_001", "pub_001")
        scores = CampaignScorer.calculate_scores(m)
        benchmark = BenchmarkEngine.benchmark_campaign(scores, m.business.leads)
        
        recs = OptimizationEngine.generate_recommendations(scores, benchmark)
        self.assertGreater(len(recs), 0)

        submission = OptimizationEngine.submit_to_learning(recs)
        self.assertEqual(submission["status"], "Submitted")

    def test_executive_dashboard(self):
        dash = ExecutiveDashboardBuilder.build_dashboard("cmp_001")
        self.assertEqual(dash.overview.campaign_id, "cmp_001")
        self.assertEqual(len(dash.platform_comparison.platforms), 3)

if __name__ == "__main__":
    unittest.main()
