"""Bản tóm tắt 2 trang A4 (PDF) — cửa chính để gửi người giao bài; HTML tương tác chỉ để "xem thêm".

Mọi con số đọc từ web/data/snapshot.json (cùng nguồn với trang tương tác và Gói A); không gõ tay số.
Sinh:
  outputs/interview/W24_Tom_Tat_2_Trang.html   (nguồn in)
  outputs/interview/W24_Tom_Tat_2_Trang.pdf    (in bằng Chrome/Edge headless nếu có trên máy)
Chạy:  python scripts/build_onepager.py [--no-pdf]
"""
from __future__ import annotations

import argparse
import html
import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "scripts"))

import build_exec_summary as ES  # noqa: E402

SNAPSHOT = REPO / "web" / "data" / "snapshot.json"
OUT_HTML = REPO / "outputs" / "interview" / "W24_Tom_Tat_2_Trang.html"
OUT_PDF = OUT_HTML.with_suffix(".pdf")
LIVE = "https://teoteo1081.github.io/W24_Life-Insurance-Strategy-Lab/outputs/interactive/W24_Strategy_Lab.html"
NAME = {"AIA": "AIA Alpha", "Chubb": "Chubb Life", "Manulife": "Manulife", "Hybrid": "Đề xuất 2026"}
COMPS = ("AIA", "Chubb", "Manulife")
BROWSERS = (r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            "google-chrome", "chromium", "msedge")


def vn(x, d=1) -> str:
    return f"{ES.fin(x):,.{d}f}".replace(",", "_").replace(".", ",").replace("_", ".")


def render(tables: dict) -> str:
    R = tables["roi_analysis"]
    e = html.escape

    def v(s, m, k=85):
        r = next((r for r in R if r["scheme"] == s and r["metric"] == m and int(r["k2"]) == k), None)
        return None if r is None else ES.fin(r["value"])

    def be(metric, comp, basis="mix4"):
        r = next((r for r in R if r["id"] == f"Hybrid|{metric}|{comp}|{basis}"), None)
        return None if r is None else ES.fin(r["value"])

    pct = lambda x, d=1: "—" if x is None else f"{vn(x, d)}%"
    drop = lambda s: v(s, "payout_drop_k2_85_to_65", 0)
    es = ES.build(tables)
    ag = {(r["milestone_id"], r["scheme"]): r for r in es["agent"]}
    tiers = []
    for r in es["agent"]:
        if (r["milestone_id"], r["tier"]) not in tiers:
            tiers.append((r["milestone_id"], r["tier"]))
    comps = [s for s in COMPS if v(s, "cost_pct_fyp") is not None]
    need = [s for s in comps if (be("breakeven_fyp_more_agents_pct", s) or 0) > 0]
    ahead = [s for s in comps if s not in need and be("breakeven_fyp_more_agents_pct", s) is not None]
    top_drop = max(comps, key=lambda s: drop(s) or -1)
    cap_gap = 75 - v("Hybrid", "cost_pct_fyp_worst_case")
    lead = ag[("M4", "Hybrid")]["month"]
    lead_lo = min(ag[("M4", s)]["month"] for s in comps if ("M4", s) in ag)
    be_lo = min((be("breakeven_fyp_productivity_pct", s) for s in need), default=None)
    be_hi = max((be("breakeven_fyp_more_agents_pct", s) for s in need), default=None)
    ex = lambda s: be("breakeven_extra_cost_bn_year", s)

    inc_rows = "".join(
        f"<tr><th>{e(t)}</th>" + "".join(
            (f"<td{' class=hl' if s == 'Hybrid' else ''}><span class=t>{e(ag[(mid, s)]['title'])}</span> <b>{vn(ag[(mid, s)]['month'])}</b></td>"
             if (mid, s) in ag else "<td>—</td>") for s in (*comps, "Hybrid")) + "</tr>"
        for mid, t in tiers)
    cost_rows = "".join(
        f"<tr{' class=hl' if s == 'Hybrid' else ''}><th>{NAME[s]}</th><td>{pct(v(s, 'cost_pct_fyp'))}</td><td>{pct(v(s, 'cost_pct_fyp_mix4'))}</td>"
        f"<td>{pct(v(s, 'cost_pct_fyp_worst_case'))}</td><td>{pct(v(s, 'cost_pct_fyp_worst_fyc40'))}</td><td>−{pct(drop(s))}</td><td>{pct(v(s, 'deferred_share'))}</td></tr>"
        for s in (*comps, "Hybrid"))
    be_rows = "".join(
        f"<tr><th>{NAME[s]}</th><td>{'chi thêm ' + vn(ex(s), 2) + ' tỷ' if ex(s) >= 0 else 'tiết kiệm ' + vn(-ex(s), 2) + ' tỷ'}</td>"
        + ("<td colspan=2>rẻ hơn ngay ở cùng FYP</td>" if s in ahead else
           f"<td><b>+{vn(be('breakeven_fyp_more_agents_pct', s))}%</b></td><td><b>{'+' + vn(be('breakeven_fyp_productivity_pct', s)) + '%' if be('breakeven_fyp_productivity_pct', s) is not None else 'chưa hòa vốn'}</b></td>")
        + "</tr>" for s in comps if be("breakeven_fyp_more_agents_pct", s) is not None)

    css = """
@page{size:A4;margin:11mm 12mm 10mm}
*{box-sizing:border-box}
body{font-family:"Segoe UI",Arial,sans-serif;font-size:8.6pt;line-height:1.36;color:#1b2430;margin:0}
h1{font-size:14.5pt;margin:0 0 1mm;color:#0f3d5e;letter-spacing:-.2px}
h2{font-size:10pt;margin:3.2mm 0 1.4mm;color:#0f3d5e;border-bottom:1.2px solid #c9d6e2;padding-bottom:.6mm}
.sub{color:#5b6b7b;font-size:7.8pt;margin-bottom:2mm}
.req{background:#f2f6fa;border-left:3px solid #0f3d5e;padding:1.6mm 2.6mm;font-style:italic;margin-bottom:2mm}
.rec{background:#eaf5ee;border:1px solid #b9dcc5;border-radius:2mm;padding:2mm 3mm;margin-bottom:2.2mm}
.rec b.k{color:#17623a}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:2mm;margin:0 0 1mm}
.kpis div{border:1px solid #d5dee7;border-radius:2mm;padding:1.6mm 2mm}
.kpis b{display:block;font-size:13pt;color:#0f3d5e;line-height:1.1}
.kpis span{font-size:7.4pt;color:#4a5866}
table{width:100%;border-collapse:collapse;margin:.6mm 0 1mm}
th,td{border-bottom:1px solid #e1e7ee;padding:1mm 1.4mm;text-align:left;vertical-align:top}
thead th{background:#0f3d5e;color:#fff;font-weight:600;font-size:7.8pt}
td{font-variant-numeric:tabular-nums}
.num td{text-align:right}.num td:first-child,.num th{text-align:left}
tr.hl td,tr.hl th,td.hl{background:#fff6e0}
.t{color:#6a7886;font-size:7.3pt}
.ans th{width:19%;color:#0f3d5e}
ul{margin:.4mm 0 1mm;padding-left:4.2mm}li{margin:.5mm 0}
.note{font-size:7.3pt;color:#5b6b7b}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:4mm}
.pb{break-before:page}
.lrn{display:grid;grid-template-columns:repeat(3,1fr);gap:2.4mm}
.lrn>div{border:1px solid #d5dee7;border-radius:2mm;padding:1.4mm 2mm}
.lrn ul{padding-left:3.6mm}.ok{color:#17623a}.mid{color:#8a5a00}.no{color:#a3261b}
footer{margin-top:2mm;font-size:7.2pt;color:#5b6b7b;border-top:1px solid #d5dee7;padding-top:1.2mm}
a{color:#0f5e9c}
"""
    p1 = f"""
<h1>Chính sách thu nhập đại lý BHNT tại Việt Nam 2026 — Tóm tắt khuyến nghị</h1>
<div class=sub>So sánh AIA (kênh Alpha), Chubb Life, Manulife trên 9 văn bản chính sách 2026 · mô hình khu vực 45 đại lý, 1,2 tỷ FYP/tháng, K2 85% · bản đầy đủ: <a href="{LIVE}">trang tương tác</a></div>
<div class=req><b>Đề bài:</b> “Phân tích các chính sách thu nhập giữa các công ty, và đề xuất chính sách phù hợp tại thị trường VN, nhằm thúc đẩy gia tăng doanh số, chất lượng kinh doanh và hiệu quả về mặt chi phí (ROI).”</div>
<div class=rec><b class=k>Khuyến nghị:</b> thí điểm <b>Chính sách Đề xuất 2026</b> trong 6–12 tháng ở 2 văn phòng (Vùng I và Vùng III), mỗi nơi ghép với 1 văn phòng đối chứng giữ chính sách cũ. Thu nhập đại lý và quản lý ngang thị trường; mọi khoản thưởng lớn gắn tỷ lệ duy trì hợp đồng năm 2 (K2); {pct(v('Hybrid', 'deferred_share'))} chi trả giữ lại trả chậm; tổng chi trả kênh đại lý có trần 75% FYP; chỉ tiêu và trợ cấp nhân hệ số theo 4 vùng lương tối thiểu. Chưa ban hành toàn quốc khi chưa có K2 và biên lợi nhuận thật.</div>
<div class=kpis>
 <div><b>{pct(v('Hybrid', 'cost_pct_fyp'))}</b><span>tổng chi / FYP khi đại lý bán đều · {pct(v('Hybrid', 'cost_pct_fyp_mix4'))} khi bán lệch 4 nhóm</span></div>
 <div><b>−{pct(drop('Hybrid'))}</b><span>chi trả tự giảm khi K2 từ 85% xuống 65% — mạnh nhất (hãng cao nhất: {NAME[top_drop]} −{pct(drop(top_drop))})</span></div>
 <div><b>{pct(v('Hybrid', 'cost_pct_fyp_worst_case'))}</b><span>kịch bản chi phí xấu nhất — vẫn dưới trần 75% (dư {vn(cap_gap)} điểm %)</span></div>
 <div><b>+{vn(be_lo or 0, 0)}–{vn(be_hi or 0, 0)}%</b><span>FYP phải bán thêm để hòa vốn so với {', '.join(NAME[s] for s in need) or '—'}</span></div>
</div>
<h2>Trả lời đề bài</h2>
<table class=ans>
<tr><th>Các công ty trả thế nào</th><td>Ở đại lý cá nhân các hãng trả gần ngang nhau; khác biệt nằm ở tầng quản lý và ở việc chi trả có co lại khi chất lượng xấu đi hay không. Tổng chi / FYP: {' · '.join(NAME[s] + ' ' + pct(v(s, 'cost_pct_fyp')) for s in comps)}. Chubb trả quản lý rất cao, gần như không trả chậm; Manulife rẻ nhất; AIA trả gần hết bằng tiền mặt năm đầu.</td></tr>
<tr><th>Doanh số</th><td>Đề xuất trả cao hơn {', '.join(NAME[s] for s in need) or '—'}{', rẻ hơn ' + ', '.join(NAME[s] for s in ahead) if ahead else ''}. Muốn hòa vốn phần phí còn lại sau chi trả kênh đại lý, khu vực phải bán thêm: {'; '.join(f"so với {NAME[s]} <b>+{vn(be('breakeven_fyp_productivity_pct', s))}%</b> nếu tăng năng suất hoặc <b>+{vn(be('breakeven_fyp_more_agents_pct', s))}%</b> nếu tuyển thêm" for s in need if be('breakeven_fyp_productivity_pct', s) is not None)}. Đây là mức tối thiểu thí điểm phải vượt; mức tăng thật chỉ đo được bằng thí điểm.</td></tr>
<tr><th>Chất lượng</th><td>Trợ cấp Full-time chỉ trả khi K2 ≥ 80%; phí quản lý nhân hệ số K2; phần trả chậm nhận đủ khi K2 ≥ 80%, một nửa khi 75–80%, mất khi dưới 75%. Kết quả: khi K2 sụt từ 85% xuống 65%, chi trả của đề xuất giảm {pct(drop('Hybrid'))}, nhiều hơn mọi hãng.</td></tr>
<tr><th>Chi phí / ROI</th><td>Không rẻ nhất khi chất lượng tốt nhưng an toàn nhất khi xấu: mọi kịch bản căng (năng suất −50%, bán nghiêng bảo vệ thuần, đạt quota hàng loạt) đều không vượt trần 75% FYP. “ROI” ở đây là chi phí / FYP mô phỏng, chưa phải lợi nhuận — cần biên VNB thật của công ty.</td></tr>
</table>
<h2>Thu nhập mỗi tháng theo 4 mốc quy mô (triệu đồng, gồm thưởng, chia đều 12 tháng)</h2>
<table class=num><thead><tr><th>Mốc</th>{''.join(f'<th>{NAME[s]}</th>' for s in (*comps, 'Hybrid'))}</tr></thead><tbody>{inc_rows}</tbody></table>
<div class=note>Mốc 2–4: phí quản lý thuần, không gồm tiền tự bán của người quản lý. Lãnh đạo khu vực của đề xuất nhận {vn(lead)} triệu/tháng ({'không thấp hơn' if lead >= lead_lo else 'thấp hơn'} mức thấp nhất của 3 hãng, {vn(lead_lo)}), trong đó 70% override trả chậm 3 năm theo K2.</div>
<h2>Học gì từ 3 hãng</h2>
<div class=lrn>
<div><b class=ok>Áp dụng</b><ul>
<li>Trả chậm 3 năm gắn K2, phí cơ bản lãnh đạo có sàn/trần theo % đạt chỉ tiêu (Manulife).</li>
<li>Khóa override gián tiếp khi nhóm trực tiếp dưới 15 triệu FYC/tháng (Chubb Life).</li>
<li>Thưởng cao cho phí tái tục năm 2 để giữ hợp đồng (AIA, Chubb Life).</li></ul></div>
<div><b class=mid>Cải tiến</b><ul>
<li>Cổng K2: không mềm như Chubb (dưới 50% vẫn trả 25%), không sốc như AIA 2027 (dưới 70% về 0) — đề xuất có bậc đệm 75–80%.</li>
<li>Kỷ luật hành vi bán hàng của Chubb: chỉ áp cho nhánh Full-time.</li>
<li>Trần tập trung 70% doanh số vào 1 người cho mọi bậc quản lý.</li></ul></div>
<div><b class=no>Tránh</b><ul>
<li>Phí cố định cao + gián tiếp nhiều tầng không trần (AIA PAF+).</li>
<li>Override trực tiếp vượt 100% FYC, đẩy tổng chi lên 89–100% FYP (Chubb Life).</li>
<li>Thưởng tăng trưởng theo quý — dễ dồn số giữa các quý (Chubb RD); tính phí đóng thêm vào chỉ tiêu (Manulife).</li></ul></div>
</div>
"""
    p2 = f"""
<h2 class=pb>Chính sách Đề xuất 2026 — kiến trúc</h2>
<table class=ans>
<tr><th>Đại lý — 2 đường ray</th><td><b>Full-time:</b> thưởng tháng 5 bậc + trợ cấp 3 triệu/tháng × hệ số vùng khi đạt quota vùng, ≥ 2 hợp đồng/tháng và K2 ≥ 80%. <b>Part-time:</b> thưởng 70%, không trợ cấp.</td></tr>
<tr><th>Quản lý nhóm / ban</th><td>Override trực tiếp × hệ số K2; gián tiếp tối đa 2 đời, khóa nếu nhóm trực tiếp chưa đạt 15 triệu FYC × hệ số vùng; một phần trả chậm 3 năm.</td></tr>
<tr><th>Lãnh đạo khu vực</th><td>Phí cơ bản theo % đạt chỉ tiêu (sàn 30%, trần 140%) thay vì phí cố định; override 11,5% FYC khu vực × hệ số K2, 70% trả chậm 3 năm.</td></tr>
<tr><th>Cơ sở tính & trần</th><td>Thưởng và phí quản lý tính trên FYC chuẩn hóa = FYP × 30% (không phụ thuộc hoa hồng từng sản phẩm); tổng chi trả kênh đại lý ≤ 75% FYP — vượt thì quỹ thưởng co theo cùng tỷ lệ.</td></tr>
<tr><th>4 vùng</th><td>Hệ số theo lương tối thiểu vùng (Nghị định 293/2025): 100% / 89% / 78% / 70% cho chỉ tiêu và trợ cấp; giữ nguyên số hợp đồng tối thiểu và K2.</td></tr>
</table>
<h2>Chi phí và độ an toàn (% FYP năm đầu)</h2>
<table class=num><thead><tr><th>Phương án</th><th>Bán đều</th><th>Bán lệch 4 nhóm</th><th>Xấu nhất</th><th>Hoa hồng 40%, xấu nhất</th><th>Khi K2 85→65%</th><th>Trả chậm</th></tr></thead><tbody>{cost_rows}</tbody></table>
<div class=note>Bán lệch 4 nhóm (giả định): 7 đại lý không hoạt động, 13 × 10 tr, 15 × 20 tr, 10 × 77 tr FYP/tháng — cùng tổng 1,2 tỷ. “Khi K2 85→65%”: chi trả giảm bao nhiêu — càng lớn càng tự bảo vệ công ty khi chất lượng xấu.</div>
<div class=cols>
<div><h2>Doanh số phải đạt để hòa vốn</h2>
<table class=num><thead><tr><th>So với</th><th>Chênh chi / năm</th><th>Tuyển thêm</th><th>Tăng năng suất</th></tr></thead><tbody>{be_rows}</tbody></table>
<div class=note>Hòa vốn = phần FYP còn lại sau chi trả kênh đại lý bằng mức của cơ chế so sánh; chưa trừ văn phòng, marketing — không phải lợi nhuận.</div></div>
<div><h2>Đánh đổi & rủi ro (công bố)</h2><ul>
<li>Đắt hơn {', '.join(NAME[s] for s in need) or '—'} ở cùng doanh số — phải được bù bằng doanh số và K2 cao hơn.</li>
<li>Kịch bản xấu nhất chỉ còn dư {vn(cap_gap)} điểm % so với trần 75%; trần tự co quỹ thưởng là chốt chặn cuối.</li>
<li>“Vách đá” thu nhập ở K2 80% và quota 30 triệu — có thể làm mượt khi thí điểm.</li>
<li>Lách vùng: cần xác định vùng theo địa bàn hoạt động thật.</li>
<li>Pháp lý (Điều 52 TT 67/2023, TT 96/2026) cần Pháp chế đối chiếu toàn văn.</li></ul></div>
</div>
<h2>Lộ trình</h2>
<ol style="margin:.4mm 0 1mm;padding-left:4.6mm">
<li><b>Tháng 1 — ghép số thật:</b> cơ cấu sản phẩm, biên VNB, chi phí vận hành → thay chi phí / FYP bằng ROI thật.</li>
<li><b>Tháng 1–12 — thí điểm có đối chứng:</b> đo hằng tháng số đại lý có hợp đồng, FYP / đại lý hoạt động, tỷ lệ đạt quota, tỷ lệ hủy 21 ngày, tỷ lệ đóng phí kỳ 2, tổng chi / FYP.</li>
<li><b>Tháng 13–15 — quyết định:</b> ban hành toàn quốc khi FYP vượt mức hòa vốn, K2 không thấp hơn đối chứng và chi phí vẫn ≤ 75% FYP ở kịch bản xấu nhất.</li></ol>
<footer>W24 Strategy Lab · Dữ liệu chuẩn hóa 2026 · số liệu sinh tự động từ cùng nguồn với trang tương tác. Số của 3 hãng là kết quả mô phỏng theo văn bản chính sách; số của đề xuất là đề xuất chưa ban hành; các giả định quy mô, năng suất, K2 ghi rõ trên trang tương tác (mục “Trả lời đề bài”). Trích dẫn từng điều khoản kèm số trang PDF: <a href="{LIVE}">{LIVE}</a></footer>
"""
    return f"<!doctype html><html lang=vi><head><meta charset=utf-8><title>W24 — Tóm tắt khuyến nghị 2 trang</title><style>{css}</style></head><body>{p1}{p2}</body></html>"


def browser() -> str | None:
    for b in BROWSERS:
        if Path(b).exists() or shutil.which(b):
            return b
    return None


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-pdf", action="store_true")
    a = ap.parse_args(argv)
    tables = json.loads(SNAPSHOT.read_text(encoding="utf-8"))["tables"]
    OUT_HTML.write_text(render(tables), encoding="utf-8")
    print(f"wrote {OUT_HTML.relative_to(REPO)}")
    if a.no_pdf:
        return 0
    b = browser()
    if not b:
        print("no Chrome/Edge found — PDF skipped")
        return 0
    subprocess.run([b, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={OUT_PDF}", OUT_HTML.as_uri()],
                   check=True, capture_output=True, timeout=120)
    print(f"wrote {OUT_PDF.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
