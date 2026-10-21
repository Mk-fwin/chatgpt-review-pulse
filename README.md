# Groww: Review Pulse (AI workflow with approval-gated actions)

Turns Play Store reviews of the Groww app into (1) an internal weekly product pulse and (2) a support-ready fee explainer, then saves both after human approval.

## Fee issue identified from the reviews
**Total charges deducted on a trade vs the advertised ₹20 per order brokerage.** Of 1,596 long reviews (7 Aug to 3 Oct 2026), 195 mention charges or fees and 119 of those are rated 1 or 2 stars:
- 29 call charges hidden or unclear
- 22 say brokerage is higher than the advertised ₹20
- 20 say charges eat into their profit
- 16 mention GST, taxes or other charges
- 11 mention MTF or haircut charges, 7 DP charges, 5 auto square-off charges

Exit load appears in **0** reviews, so it was not chosen. Only 17 reviews mention a mutual fund and a fee together.

## How to run (Mac)
1. `cd` into this folder
2. `pip3 install -r requirements.txt`
3. `python3 -m streamlit run app.py`

Optional: `python3 analyze.py reviews.csv` re-runs the theme and fee counts on a Groww reviews CSV. `python3 make_deliverables.py` rebuilds `deliverables/` (doc snippet and email draft text).

## Where the MCP approval happens
Tab **Approval gate**. The app shows what will be written, and **Run approved actions** stays disabled until you tick an approval box. Nothing is written before that.
- Action 1, append to notes: `output/notes_log.md` (and `.jsonl`) with date, top_themes, weekly_pulse, identified_fee_issue, explanation_bullets, source_links
- Action 2, create email draft: `output/email_draft.eml` and `.txt`, subject "Weekly Product Pulse + Customer Clarification — <date>". Never sent.

The MCP actions are **simulated** with local files. To use real tools, replace `action_append_note()` and `action_create_draft()` in `app.py` with a Zapier/Make webhook or Google Docs and Gmail API calls; the approval gate stays the same.

## Method and limits
- Reviews: Google Play, India, latest 9,000 reviews (7 Aug to 3 Oct 2026), all ratings.
- Themes use keyword rules (`analyze.py`); one review can count in several themes. Quotes were picked by hand and checked against the CSV.
- Charges in the explainer come from Groww's official pricing and help pages; they can change, so check "Last checked".

## Files
`app.py` | `analyze.py` | `make_deliverables.py` | `data/` insights, pulse, explainer, sources, 200-row review sample | `deliverables/` doc snippet and email draft
