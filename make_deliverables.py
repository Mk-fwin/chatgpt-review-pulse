"""Rebuilds the doc snippet and email draft files into deliverables/ from data/."""
import json, re
from datetime import date
from pathlib import Path

D, O = Path("data"), Path("deliverables")
O.mkdir(exist_ok=True)
ins = json.loads((D / "insights.json").read_text(encoding="utf-8"))
pulse = (D / "weekly_pulse.md").read_text(encoding="utf-8")
exp = (D / "fee_explainer.md").read_text(encoding="utf-8")
bullets = re.findall(r"^- (.+)$", exp, re.M)
links = re.findall(r"https?://\S+", exp)
last = re.search(r"Last checked: (.+)", exp).group(1).strip()
today = date.today().strftime("%d %b %Y")
note = (
    f"## Entry: {today}\n**Top themes:** {', '.join(ins['top3'])}\n\n"
    f"**Identified fee issue:** {ins['fee_issue']}\n\n**Weekly pulse:**\n{pulse}\n\n"
    "**Explanation bullets:**\n" + "\n".join(f"- {b}" for b in bullets)
    + "\n\n**Source links:**\n" + "\n".join(f"- {u}" for u in links) + "\n"
)
(O / "appended_entry_snippet.md").write_text(note, encoding="utf-8")
subject = f"Weekly Product Pulse + Customer Clarification — {today}"
body = (
    "Hi team,\n\nWeekly product pulse\n" + "-" * 20 + "\n" + pulse
    + "\n\nSupport snippet: Groww charges\n" + "-" * 20 + "\n"
    + "\n".join(f"- {b}" for b in bullets)
    + "\n\nSources:\n" + "\n".join(links) + f"\nLast checked: {last}\n"
)
(O / "email_draft.txt").write_text(f"Subject: {subject}\n\n{body}", encoding="utf-8")
print("done")
