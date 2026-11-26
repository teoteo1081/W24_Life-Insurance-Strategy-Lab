"""Kiểm khớp engine JS (web/engine.js) với engine Python trên lưới golden (web/golden.json).
Lưới gồm 5 bộ tham số × 8 mức K2 × (chi phí toàn hệ thống + thu nhập đại lý 3 năm ở 5 mức FYC).
Cần Node.js; nếu máy không có Node thì test báo SKIP rõ ràng, không tính là PASS."""
from __future__ import annotations

import json
import math
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

NODE_RUNNER = r"""
const eng = require(process.argv[1]);
const g = JSON.parse(require('fs').readFileSync(process.argv[2], 'utf8'));
const out = g.cases.map(c => {
  const p = JSON.parse(JSON.stringify(g.params[c.plan]));
  return c.kind === 'enterprise' ? eng.enterprise(c.k2, p) : eng.agentIncome3y(c.fyc, c.k2, p);
});
process.stdout.write(JSON.stringify(out));
"""


@unittest.skipIf(shutil.which("node") is None, "Node.js not installed: JS parity NOT verified")
class TestWebParity(unittest.TestCase):
    def test_js_matches_python_on_golden_grid(self) -> None:
        import build_html
        plans = build_html.plan_params()
        g = build_html.golden(plans)
        gpath = REPO / "web/golden.json"
        gpath.write_text(json.dumps(g), encoding="utf-8")
        res = subprocess.run(["node", "-e", NODE_RUNNER, str(REPO / "web/engine.js"), str(gpath)],
                             capture_output=True, text=True, encoding="utf-8", check=True)
        got = json.loads(res.stdout)
        self.assertEqual(len(got), len(g["cases"]))
        self.assertEqual(len(got), 240)  # 5 bộ tham số × 8 K2 × (1 enterprise + 5 mức FYC)
        for case, js in zip(g["cases"], got):
            for k, v in case["expect"].items():
                with self.subTest(plan=case["plan"], kind=case["kind"], k2=case["k2"], fyc=case.get("fyc"), key=k):
                    self.assertTrue(math.isfinite(js[k]))
                    self.assertAlmostEqual(js[k], v, delta=0.02)  # Python làm tròn từng năm rồi cộng

    def test_js_rejects_nan_and_bad_thresholds(self) -> None:
        script = r"""
const eng = require(process.argv[1]);
const base = {k2_hard_floor_pct:60,agent_q_consistency_3m:0.12,agent_annual_mdrt_rate:0.1,agent_ryc_bonus_rate:0.25,
 mgr_direct_base_rate:0.3,mgr_direct_max_rate:0.36,mgr_indirect_l1_rate:0.35,mgr_deferred_3y_rate:0.12,
 rd_base_monthly:35,rd_direct_fyc_rate:0.07,rd_deferred_3y_share:0.6,
 agent_m_tier_rates:[0.08,0.16,0.24,0.32,0.38],agent_m_tier_thresholds:[5,12,22,35,55]};
const bad = [Object.assign({}, base, {agent_ryc_bonus_rate: NaN}),
             Object.assign({}, base, {rd_base_monthly: Infinity}),
             Object.assign({}, base, {agent_m_tier_thresholds:[5,22,12,35,55]})];
let rejected = 0;
for (const p of bad) { try { eng.enterprise(82, p); } catch (e) { rejected++; } }
try { eng.agentIncome3y(NaN, 82, base); } catch (e) { rejected++; }
process.stdout.write(String(rejected));
"""
        res = subprocess.run(["node", "-e", script, str(REPO / "web/engine.js")],
                             capture_output=True, text=True, check=True)
        self.assertEqual(res.stdout.strip(), "4")


if __name__ == "__main__":
    unittest.main()
