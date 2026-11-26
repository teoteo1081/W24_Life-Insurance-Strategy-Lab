/* W24 proposal engine — bản JS của các hàm Python sau, để trang HTML tính trực tiếp khi kéo thông số:
     proposal_k2_factor, calc_proposal_agent_12m (FYC/SYC đều nhau 12 tháng, đại lý có thâm niên),
     nhánh "W24_Proposed_Balanced" của calc_enterprise_hierarchy_cost,
     agent_income_3y (scripts/agent_income_multiyear.py) cho phương án đề xuất.
   Mọi thay đổi ở Python phải sửa tương ứng ở đây; tests/test_web_parity.py so JS với Python trên lưới golden. */
(function (root) {
  "use strict";
  var FYC_TO_FYP = 0.30, RENEWAL_COMM_Y2 = 0.20, RENEWAL_COMM_Y3 = 0.10, K3_RATIO = 0.92;
  var NUM_KEYS = ["k2_hard_floor_pct", "agent_q_consistency_3m", "agent_annual_mdrt_rate", "agent_ryc_bonus_rate",
    "mgr_direct_base_rate", "mgr_direct_max_rate", "mgr_indirect_l1_rate", "mgr_deferred_3y_rate",
    "rd_base_monthly", "rd_direct_fyc_rate", "rd_deferred_3y_share"];

  function num(x, name) {
    if (typeof x !== "number" || !isFinite(x)) throw new Error(name + " must be a finite number");
    return x;
  }

  function validate(p) {
    NUM_KEYS.forEach(function (k) { if (num(p[k], k) < 0) throw new Error(k + " must be >= 0"); });
    ["agent_m_tier_rates", "agent_m_tier_thresholds"].forEach(function (k) {
      if (!p[k] || p[k].length !== 5) throw new Error(k + " needs 5 values");
      p[k].forEach(function (v, i) { num(v, k + "[" + i + "]"); });
    });
    for (var i = 1; i < 5; i++) {
      if (!(p.agent_m_tier_thresholds[i] > p.agent_m_tier_thresholds[i - 1])) throw new Error("thresholds must be strictly increasing");
    }
  }

  function k2Factor(k2, floor) {
    num(k2, "k2");
    if (k2 >= 85) return 1.20;
    if (k2 >= 80) return 1.10;
    if (k2 >= 75) return 1.00;
    if (k2 >= 70) return 0.85;
    if (k2 >= floor) return 0.60;
    return 0.00;
  }

  /* Thưởng 12 tháng của một đại lý (triệu VND). fycM, sycM: FYC/SYC mỗi tháng. */
  function agentBonuses12m(fycM, sycM, k2, p) {
    num(fycM, "fyc"); num(sycM, "syc");
    var kf = k2Factor(k2, p.k2_hard_floor_pct), rate = 0;
    for (var i = 4; i >= 0; i--) {
      if (fycM >= p.agent_m_tier_thresholds[i]) { rate = p.agent_m_tier_rates[i]; break; }
    }
    var monthly = fycM * rate * kf * 12;
    var qCons = fycM >= 4.0 ? monthly * p.agent_q_consistency_3m : 0;
    var fycY = fycM * 12, sycY = sycM * 12;
    var mdrt = fycY >= 400 ? fycY * p.agent_annual_mdrt_rate * kf : 0;
    var ryc = k2 >= 75 ? sycY * p.agent_ryc_bonus_rate : 0;
    return { monthly: monthly, q_consistency: qCons, mdrt: mdrt, ryc: ryc, total: monthly + qCons + mdrt + ryc };
  }

  /* Hoa hồng tái tục mỗi tháng ở năm 1, 2, 3 — ASSUMPTION chung cho mọi hãng. */
  function renewalByYear(fycM, k2) {
    var fypYear = fycM * 12 / FYC_TO_FYP, k = k2 / 100;
    var y2 = fypYear * k * RENEWAL_COMM_Y2;
    var y3 = fypYear * k * RENEWAL_COMM_Y2 + fypYear * k * K3_RATIO * RENEWAL_COMM_Y3;
    return [0, y2 / 12, y3 / 12];
  }

  /* Thu nhập đại lý 3 năm theo phương án đề xuất (gồm FYC, tái tục, thưởng). */
  function agentIncome3y(fycM, k2, p) {
    validate(p);
    var syc = renewalByYear(fycM, k2), years = [];
    for (var y = 0; y < 3; y++) years.push(fycM * 12 + syc[y] * 12 + agentBonuses12m(fycM, syc[y], k2, p).total);
    return { y1: years[0], y2: years[1], y3: years[2], total_3y: years[0] + years[1] + years[2] };
  }

  /* Cây tổ chức chuẩn: 1 vùng 12.000tr FYP, 20 đại lý × 15tr FYC/tháng, 4 quản lý, 1 lãnh đạo vùng. */
  function enterprise(k2, p, opexPct) {
    validate(p);
    var annualFyp = 12000, annualFyc = annualFyp * FYC_TO_FYP;
    var ag = agentBonuses12m(15, 0, k2, p).total * 20;
    var kf = k2Factor(k2, p.k2_hard_floor_pct);
    var mgDirect = annualFyc * Math.min(p.mgr_direct_max_rate, p.mgr_direct_base_rate * kf);
    var mgIndirect = mgDirect * 0.5 * p.mgr_indirect_l1_rate;
    var mgDeferred = k2 >= 75 ? annualFyc * p.mgr_deferred_3y_rate : 0;
    var rdBase = p.rd_base_monthly * 12 * Math.min(1.40, 1.05 * 1.25);
    var rdVar = annualFyc * p.rd_direct_fyc_rate * kf;
    var rdDeferred = k2 >= 75 ? rdVar * p.rd_deferred_3y_share : 0;
    var rdCash = rdBase + rdVar;
    var total = annualFyc + ag + mgDirect + mgIndirect + mgDeferred + rdCash + rdDeferred;
    var deferred = mgDeferred + rdDeferred;
    var persisted = annualFyp * k2 / 100;
    var opex = (typeof opexPct === "number" ? opexPct : 0.20);
    return {
      earned_pct_fyp: total / annualFyp * 100,
      cash_y1_pct_fyp: (total - deferred) / annualFyp * 100,
      art52_bonus_pct_fyp: ag / annualFyp * 100,
      cost_per_persisted_y2_pct: persisted > 0 ? total / persisted * 100 : 0,
      breakeven_gross_margin_pct: (total / annualFyp + opex) * 100,
      total_earned: total,
      fixed_cost: rdBase,
      role_agent_earned: (annualFyc + ag) / 20,
      role_mgr_direct_earned: (mgDirect + mgDeferred) / 4,
      role_mgr_indirect_extra: mgIndirect / 2,
      role_leader_earned: rdCash + rdDeferred,
      deferred_share_pct: total > 0 ? deferred / total * 100 : 0,
      layers: {a_commission: annualFyc, b_agent_bonus: ag, c_mgr_direct: mgDirect, d_mgr_indirect: mgIndirect,
        e_mgr_deferred: mgDeferred, f_rd_base: rdBase, g_rd_variable: rdVar, h_rd_deferred: rdDeferred, k2_factor: kf}
    };
  }

  /* FYP phải tăng thêm bao nhiêu (%) để phương án `plan` có lợi nhuận bằng `base` ở FYP hiện tại.
     ASSUMPTION: FYP tăng nhờ thêm đại lý/quản lý cùng năng suất => mọi chi phí tăng tỷ lệ, trừ phí cơ bản lãnh đạo vùng (cố định).
     margin, opex: tỷ lệ trên FYP. Trả về null nếu phương án không thể hòa vốn ở biên này. */
  function requiredFypUplift(planEnt, baseEnt, margin, opex) {
    var F0 = 12000;
    var vPlan = planEnt.total_earned - planEnt.fixed_cost, vBase = baseEnt.total_earned - baseEnt.fixed_cost;
    var unit = (margin - opex) * F0 - vPlan;
    if (unit <= 0) return null;
    var target = (margin - opex) * F0 - vBase - baseEnt.fixed_cost + planEnt.fixed_cost;
    return (target / unit - 1) * 100;
  }

  var api = { k2Factor: k2Factor, agentBonuses12m: agentBonuses12m, agentIncome3y: agentIncome3y,
    enterprise: enterprise, requiredFypUplift: requiredFypUplift, validate: validate, renewalByYear: renewalByYear };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  else root.W24Engine = api;
})(typeof window !== "undefined" ? window : this);
