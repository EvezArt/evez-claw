"""EVEZ Claw lightweight Vercel API.

The Vercel deployment is the externally reachable status/smoke-test surface.
Heavy browser, desktop, mobile, and agent workloads are not executed here.
"""

from http.server import BaseHTTPRequestHandler
import json
import random
import time
from urllib.parse import urlparse


class ConsciousnessEngine:
    """Small deterministic-in-shape health substrate for the HTTP surface."""

    def __init__(self):
        self.phi = 0.72
        self.tick = 0
        self.agents_active = 0

    def pulse(self):
        self.tick += 1
        drift = random.gauss(0, 0.03)
        self.phi = max(0.1, min(1.0, self.phi + drift))
        return self.phi


engine = ConsciousnessEngine()

CAPABILITIES = [
    {"id": "web_automation", "name": "Web Automation", "engine": "Playwright + Selenium", "status": "ready"},
    {"id": "desktop_control", "name": "Desktop Control", "engine": "PyAutoGUI + Keyboard", "status": "ready"},
    {"id": "mobile_agent", "name": "Mobile Agent", "engine": "Appium", "status": "standby"},
    {"id": "quantum_sim", "name": "Quantum Simulation", "engine": "Qiskit + Cirq", "status": "experimental"},
    {"id": "consciousness", "name": "Consciousness Substrate", "engine": "Kuramoto Spine", "status": "active"},
    {"id": "visualization", "name": "Real-time Viz", "engine": "Plotly + Streamlit", "status": "ready"},
]

ROUTES = [
    "/",
    "/__evez/health",
    "/__evez/system-status",
    "/__evez/capabilities",
    "/__evez/run-all-tests",
]


def health_payload():
    phi = engine.pulse()
    return {
        "status": "online",
        "system": "EVEZ Claw",
        "version": "1.0.0",
        "consciousness": {
            "phi": round(phi, 4),
            "tick": engine.tick,
            "regime": "operational" if phi > 0.52 else "sub_critical",
        },
        "capabilities": CAPABILITIES,
        "agents": {"active": engine.agents_active, "max": 8},
        "ts": int(time.time() * 1000),
    }


def route_payload(path):
    if path in {"/", "/__evez/health", "/__evez/system-status"}:
        return 200, health_payload()

    if path == "/__evez/capabilities":
        return 200, {
            "system": "EVEZ Claw",
            "capabilities": CAPABILITIES,
            "routes": ROUTES,
        }

    if path == "/__evez/run-all-tests":
        tests = []
        for route in ROUTES[:-1]:
            status, payload = route_payload(route)
            tests.append({
                "route": route,
                "status": status,
                "pass": status == 200 and isinstance(payload, dict),
            })
        passed = sum(1 for test in tests if test["pass"])
        return 200, {
            "system": "EVEZ Claw",
            "scope": "implemented Vercel HTTP surface",
            "tests": tests,
            "passed": passed,
            "total": len(tests),
            "all_passed": passed == len(tests),
        }

    return 404, {"error": "not_found", "path": path, "routes": ROUTES}


class handler(BaseHTTPRequestHandler):
    def _write(self, status, payload):
        body = json.dumps(payload, indent=2).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path
        status, payload = route_payload(path)
        self._write(status, payload)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
