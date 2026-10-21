"""Re-run the Groww review analysis. Usage: python3 analyze.py reviews.csv"""
import sys, warnings
import pandas as pd
warnings.filterwarnings("ignore")

THEMES = {
    "App stability & trading UX": r"\blag|slow|crash|hang|glitch|\bbug|not working|stuck|server|freez|buffer|not load|loading|update|navigation|back button|stop.?loss|trailing|scalper|chart",
    "Customer support": r"customer (care|support|service)|support|no response|not respond|no reply|ticket|helpline|complain|grievance|chat",
    "Charges & pricing clarity": r"charge|brokerage|\bfee|deduct|hidden|\bgst\b|haircut|\bamc\b|maintenance",
    "Money movement & account": r"withdraw|payout|payment|upi|refund|money (stuck|blocked)|kyc|blocked|suspend|account (open|clos|freez)|verification|settle",
    "Ease of use / UI praise": r"easy|user.?friendly|simple|smooth|best app|good app|beginner|interface|\bui\b|\bux\b",
}
FEE = {
    "Charges 'hidden' or unclear": r"hidden|not clearly|transparen|unclear|not easy to understand|misleading|no clarity|clarity",
    "Brokerage higher than advertised ₹20": r"(20|₹20|rs.? ?20).{0,50}(per order|every|each)|too much brokerage|more than.{0,20}brokerage|brokerage.{0,40}(high|more|too much|excess)",
    "Charges eat into profit": r"(eat|ate|left with|net gain|net profit|deduct|cut|reduce).{0,60}(profit|gain)|profit.{0,60}(brokerage|charges|deduct)",
    "GST, taxes and other charges": r"\bgst\b|\bstt\b|stamp|sebi (turnover|charge)|taxes|other charges|external charges|transaction charge|exchange charge",
    "MTF / haircut charges": r"\bmtf\b|haircut|interest charge|margin interest",
    "DP / sell-side charges": r"\bdp\b|dp charge|20 rs for every sell|every sell|selling stocks",
    "Auto square-off charges": r"square.?off charge|sqare.?off|auto.?square",
    "Exit load": r"exit load",
}
path = sys.argv[1] if len(sys.argv) > 1 else "reviews.csv"
df = pd.read_csv(path)
df["words"] = df["review"].str.split().str.len()
sub = df[df.words >= 8]
t = sub["review"].str.lower()
print(f"{len(df)} reviews, {len(sub)} with 8+ words, {df['date'].min()} to {df['date'].max()}")
print("\nThemes:")
for k, v in THEMES.items():
    m = t.str.contains(v, regex=True)
    print(f"  {k}: {m.sum()} mentions, avg {sub[m].rating.mean():.2f} stars, {(sub[m].rating <= 2).sum()} rated 1-2")
print("\nFee confusion:")
for k, v in FEE.items():
    print(f"  {k}: {t.str.contains(v, regex=True).sum()}")
