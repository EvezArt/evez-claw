"""Dependency-free contract tests for the EVEZ-Claw HTTP surface."""

import unittest

from api.index import ROUTES, route_payload


class ApiContractTests(unittest.TestCase):
    def test_declared_routes_are_reachable(self):
        for route in ROUTES:
            with self.subTest(route=route):
                status, payload = route_payload(route)
                self.assertEqual(status, 200)
                self.assertIsInstance(payload, dict)

    def test_unknown_routes_are_rejected(self):
        status, payload = route_payload("/__evez/not-a-real-route")
        self.assertEqual(status, 404)
        self.assertEqual(payload["error"], "not_found")
        self.assertIn("/__evez/health", payload["routes"])

    def test_run_all_tests_is_truthful(self):
        status, payload = route_payload("/__evez/run-all-tests")
        self.assertEqual(status, 200)
        self.assertTrue(payload["all_passed"])
        self.assertEqual(payload["passed"], payload["total"])


if __name__ == "__main__":
    unittest.main()
