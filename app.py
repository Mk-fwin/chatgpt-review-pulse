import json
import re
from datetime import date
from email.message import EmailMessage
from pathlib import Path

import pandas as pd
import streamlit as st

BASE = Path(__file__).parent
DATA = BASE / "data"
OUT = BASE / "output"
OUT.mkdir(exist_ok=True)

st.set_page_config(page_title="ChatGPT India: Review Pulse", page_icon="📝", layout="centered")

insights = json.loads((DATA / "insights.json").read_text(encoding="utf-8"))
pulse = (DATA / "weekly_pulse.md").read_text(encoding="utf-8")
explainer = (DATA / "fee_explainer.md").read_text(encoding="utf-8")

bullets = re.findall(r"^- (.+)$", explainer, re.M)
links = re.findall(r"https?://\S+", explainer)
last_checked = re.search(r"Last checked: (.+)", explainer).group(1).strip()
today = date.today().strftime("%d %b %Y")
top_themes = insights["top3"]
fee_issue = insights["fee_issue"]

entry = {
    "date": today,
    "top_themes": top_themes,
    "weekly_pulse": pulse,
    "identified_fee_issue": fee_issue,
    "explanation_bullets": bullets,
    "source_links": links,
}

subject = f"Weekly Product Pulse + Customer Clarification — {today}"
email_body = (
    "Hi team,\n\nWeekly product pulse\n" + "-" * 20 + "\n" + pulse
    + "\n\nSupport snippet: plan limits and billing\n" + "-" * 20 + "\n"
    + "\n".join(f"- {b}" for b in bullets)
    + "\n\nSources:\n" + "\n".join(links)
    + f"\nLast checked: {last_checked}\n"
)


def action_append_note():
    """MCP action 1 (simulated): append the entry to the notes doc."""
    md = (
        f"\n\n## Entry: {entry['date']}\n"
        f"**Top themes:** {', '.join(entry['top_themes'])}\n\n"
        f"**Identified fee issue:** {entry['identified_fee_issue']}\n\n"
        f"**Weekly pulse:**\n{entry['weekly_pulse']}\n\n"
        "**Explanation bullets:**\n"
        + "\n".join(f"- {b}" for b in entry["explanation_bullets"])
        + "\n\n**Source links:**\n"
        + "\n".join(f"- {u}" for u in entry["source_links"])
        + "\n"
    )
    with open(OUT / "notes_log.md", "a", encoding="utf-8") as f:
        f.write(md)
    with open(OUT / "notes_log.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return md


def action_create_draft():
    """MCP action 2 (simulated): create an email draft. Never sends."""
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["X-Unsent"] = "1"
    msg.set_content(email_body)
    (OUT / "email_draft.eml").write_bytes(bytes(msg))
    (OUT / "email_draft.txt").write_text(f"Subject: {subject}\n\n{email_body}", encoding="utf-8")
    return f"Subject: {subject}\n\n{email_body}"


CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.block-container { padding-top: 1.4rem; max-width: 1000px; }
.hero { background: linear-gradient(135deg,#0f2f2a 0%,#10a37f 100%); color:#fff; padding:28px 32px; border-radius:22px; margin-bottom:18px; }
.hero h1 { margin:0; font-size:1.9rem; font-weight:700; color:#fff; }
.hero p { margin:6px 0 0; opacity:.85; font-size:.92rem; }
.kpi { background:#fff; border:1px solid #e7e5df; border-radius:16px; padding:14px 16px; }
.kpi .n { font-size:1.6rem; font-weight:700; color:#0f2f2a; }
.kpi .l { font-size:.78rem; color:#6b6b66; }
.card { background:#fff; border:1px solid #e7e5df; border-radius:14px; padding:14px 16px; margin-bottom:10px; }
.bar { height:8px; background:#ece9e1; border-radius:99px; overflow:hidden; margin-top:8px; }
.bar > div { height:100%; background:#10a37f; border-radius:99px; }
.quote { border-left:4px solid #10a37f; background:#fff; padding:14px 18px; border-radius:0 14px 14px 0; margin-bottom:10px; }
.quote small { color:#6b6b66; }
.pill { display:inline-block; padding:2px 10px; border-radius:99px; font-size:.74rem; font-weight:600; background:#e6f6f1; color:#0b7a5e; }
.pill.warn { background:#fff1e0; color:#a15c00; }
.callout { background:#fff8ec; border:1px solid #f3dfb8; border-radius:16px; padding:16px 20px; margin-bottom:12px; }
.flow { display:flex; gap:8px; margin:6px 0 14px; font-size:.85rem; }
.flow span { padding:6px 14px; border-radius:99px; background:#f1efe8; color:#4a4a45; }
.flow span.on { background:#10a37f; color:#fff; font-weight:600; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

st.markdown(
    f"""<div class="hero"><h1>ChatGPT India: Review Pulse</h1>
    <p>Play Store reviews to a weekly product pulse and a support-ready plan explainer</p>
    <p>{insights['source']}</p></div>""",
    unsafe_allow_html=True,
)

LABELS = {
    "paid_but_still_limited": "Paid, still hit limits",
    "price_too_high_or_not_worth": "Price too high / not worth it",
    "unclear_what_you_pay_for": "Unclear what they pay for",
    "refund_charge_cancel_issues": "Refund / charge / cancel issues",
    "paid_but_plan_not_activated": "Paid, plan not activated",
}

tab1, tab2, tab3, tab4 = st.tabs(["Insights", "Weekly pulse", "Fee explainer", "Approval gate"])

with tab1:
    kpis = [
        (f"{insights['total_reviews']:,}", "reviews analysed (1-3 stars)"),
        (f"{insights['substantive_8plus_words']:,}", "long reviews (8+ words)"),
        (str(insights["fee_evidence"]["paid_but_still_limited"]), "paid and still hit limits"),
        (f"{insights['voice_mentions']['share_pct']}%", "mention voice"),
    ]
    cols = st.columns(4)
    for c, (n, l) in zip(cols, kpis):
        c.markdown(f'<div class="kpi"><div class="n">{n}</div><div class="l">{l}</div></div>', unsafe_allow_html=True)
    st.caption(insights["caveat"])

    st.markdown("#### Themes")
    mx = max(t["share_pct"] for t in insights["themes"])
    for t in sorted(insights["themes"], key=lambda x: -x["share_pct"]):
        top = '<span class="pill">Top 3</span>' if t["name"] in top_themes else ""
        st.markdown(
            f'<div class="card"><b>{t["name"]}</b> {top}'
            f'<span style="float:right;color:#6b6b66">{t["share_pct"]}% · {t["mentions"]:,} mentions</span>'
            f'<div class="bar"><div style="width:{t["share_pct"] / mx * 100:.0f}%"></div></div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("#### What users actually said")
    for q in insights["quotes"]:
        st.markdown(
            f'<div class="quote">“{q["text"]}”<br><small>{q["theme"]} · {q["rating"]}★ · {q["date"]}</small></div>',
            unsafe_allow_html=True,
        )

    st.markdown("#### Fee / charge confusion")
    st.markdown(f'<div class="callout"><b>{fee_issue}</b></div>', unsafe_allow_html=True)
    ev = insights["fee_evidence"]
    emx = max(ev.values())
    for k, v in ev.items():
        st.markdown(
            f'<div class="card" style="padding:10px 14px"><span>{LABELS.get(k, k)}</span>'
            f'<b style="float:right">{v}</b><div class="bar"><div style="width:{v / emx * 100:.0f}%;background:#e8913a"></div></div></div>',
            unsafe_allow_html=True,
        )
    with st.expander("Reviews CSV sample"):
        st.dataframe(pd.read_csv(DATA / "reviews_sample.csv"))

with tab2:
    with st.container(border=True):
        st.markdown(pulse)

with tab3:
    with st.container(border=True):
        st.markdown(explainer)

with tab4:
    st.markdown("#### Approval gate")
    st.markdown(
        '<div class="flow"><span>1 Review output</span><span class="on">2 Approve</span><span>3 Saved, never sent</span></div>',
        unsafe_allow_html=True,
    )
    st.caption("Nothing is written until you approve. The email is saved as a draft only.")
    c1, c2 = st.columns(2)
    with c1, st.container(border=True):
        st.markdown("**Action 1: Append to notes doc**")
        st.caption("output/notes_log.md")
        with st.expander("Preview entry"):
            st.json(entry)
        ok1 = st.checkbox("Approve action 1")
        st.markdown(f'<span class="pill{"" if ok1 else " warn"}">{"Approved" if ok1 else "Awaiting approval"}</span>', unsafe_allow_html=True)
    with c2, st.container(border=True):
        st.markdown("**Action 2: Create email draft**")
        st.caption("output/email_draft.eml, no auto-send")
        with st.expander("Preview subject"):
            st.text(subject)
        ok2 = st.checkbox("Approve action 2")
        st.markdown(f'<span class="pill{"" if ok2 else " warn"}">{"Approved" if ok2 else "Awaiting approval"}</span>', unsafe_allow_html=True)
    if st.button("Run approved actions", type="primary", disabled=not (ok1 or ok2)):
        if ok1:
            st.success("Appended to output/notes_log.md")
            st.markdown(action_append_note())
        if ok2:
            st.success("Draft saved to output/email_draft.eml (not sent)")
            st.text(action_create_draft())
    if not (ok1 or ok2):
        st.caption("Not approved: no files are written.")
