# ChatGPT India: Review Pulse (Milestone workflow)

Turns Play Store reviews of the ChatGPT mobile app into (1) an internal weekly product pulse and (2) a support-ready fee explainer, then saves both after human approval.

## Fee issue identified from the reviews
**What the Free, Go, Plus and Pro plans actually include (usage limits, voice limits, billing).** ChatGPT has no hidden fee; the confusion is about value for money. Counts across 14,946 unique 1 to 3 star reviews (9 Aug to 3 Oct 2026):
- 228 say they paid and still hit limits
- 217 say the price is too high or not worth it
- 132 say it is unclear what they are paying for
- 118 mention refund, charge or cancellation problems
- 16 paid but the plan did not activate

Link to the voice case (Milestone 1): 328 reviews mention voice (2.2%, average 1.84 stars). OpenAI's Go help page says Go voice has Free-tier limits, while its Voice page (newer) lists 3 hours per 24 hours for Go.

## How to run (Mac)
1. Open Terminal and go to this folder: `cd path/to/chatgpt-pulse-app`
2. Install: `pip3 install -r requirements.txt`
3. Start: `python3 -m streamlit run app.py`
4. A browser tab opens. Go through the four tabs.

Optional: re-run the review analysis on your own CSV: `python3 analyze.py chatgpt_reviews_low.csv`

## Where the MCP approval happens
Tab **4. Approval gate**. The app shows exactly what will be written, and the **Run approved actions** button stays disabled until you tick an approval checkbox. Nothing is written before that.
- Action 1, append to notes: `output/notes_log.md` (and `notes_log.jsonl`) with date, top_themes, weekly_pulse, identified_fee_issue, explanation_bullets, source_links
- Action 2, create email draft: `output/email_draft.eml` and `.txt`, subject "Weekly Product Pulse + Customer Clarification — <date>". The draft is never sent.

The MCP actions are **simulated** with local files (the brief allows a simple approval step). To use real tools, replace `action_append_note()` and `action_create_draft()` in `app.py` with a Zapier/Make webhook, or Google Docs and Gmail API calls. The approval gate stays the same.

## Method and limits
- Reviews: Google Play, India, 1 to 3 stars only (Play's paging cap stopped an all-ratings pull at about 2.5 weeks), so sentiment skews negative.
- Themes come from keyword rules (`analyze.py`), and one review can count in several themes. Quotes were picked by hand and checked word for word against the CSV.
- INR prices are not in the explainer because no official OpenAI page I opened showed them; it links to the pricing page instead.

## Files
`app.py` app | `analyze.py` analysis | `data/` insights, pulse, explainer, sources, 178-row review sample | `output/` created when you approve
