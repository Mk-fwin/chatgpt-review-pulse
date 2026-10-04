"""Re-run the review analysis on a fresh Play Store CSV.
Usage: python3 analyze.py chatgpt_reviews_low.csv
Prints theme counts and fee-confusion counts. Quotes in data/insights.json are curated by hand.
"""
import sys
import warnings

import pandas as pd

warnings.filterwarnings("ignore")

THEMES = {
    "Usage limits, paywall & plan value": r"limit|\bcap\b|caps\b|ran out|out of messages|cooldown|cool down|upgrade|subscri|premium|\bplus\b|\bpro\b|\bgo plan|expensive|overpriced|price|pricing|afford|not worth|paywall|refund|charged|billing|₹|\$ ?\d",
    "Answer quality & instruction-following": r"wrong|incorrect|hallucin|inaccura|made up|nonsense|stupid|dumb|useless|garbage|doesn.?t (follow|listen|understand|remember)|ignor|forget|memory|worse|downgrad|degrad|gpt.?5|model|accura|not helpful|bad answer|poor answer",
    "App bugs, crashes & slowness": r"crash|\bbug|glitch|not working|doesn.?t work|stuck|freez|\blag|slow|loading|hang|error|something went wrong|network error|thinking|infinite|broken|keeps (closing|stopping)|won.?t (open|load)",
    "Login, account & support": r"login|log in|sign in|logged out|account|banned|suspend|locked out|otp|verification|verify|customer (service|support|care)|support|no response|no reply|helpline|ticket",
    "Image generation, ads & feature requests": r"image gen|generate (an )?image|image (limit|quality)|\bads?\b|advert|bring back|please add|add (a|an|the) (option|feature|toggle)|feature request|toggle|dark mode|folder|projects",
}
FEE = {
    "paid_but_still_limited": r"(i pay|paying|paid|plus|pro|premium).{0,60}(limit|cap|cooldown|still|same|no difference|worse|not worth)|(limit|cap).{0,50}(even|despite|though).{0,30}(pay|plus|pro|premium|subscri)",
    "price_too_high_or_not_worth": r"(too |very |so )?(expensive|overpriced)|not worth|ridiculous(ly)? (high )?pric|price.{0,25}(high|ridiculous|justif)|afford|\$ ?20|£ ?\d|₹ ?\d|rs\.? ?\d|\d+ ?(rs|rupees)",
    "unclear_what_you_pay_for": r"what you.{0,10}(are )?(buying|paying)|unclear|not clear|confus|no (clear )?(info|transparen)|transparen|misleading|hidden|fine print|without (telling|informing)",
    "refund_charge_cancel_issues": r"refund|charged|double charg|deducted|auto.?renew|unsubscrib|cancel.{0,25}(subscri|plan|plus)|(subscri|plan|plus).{0,25}cancel|billing",
    "paid_but_plan_not_activated": r"(payment|paid|purchase|bought|subscription|plus).{0,60}(not (applied|activated|showing|reflect|received|working)|didn.?t (get|receive|apply|activate)|still (show|free)|no subscription)|not getting.{0,20}(subscription|plus|premium)",
}
VOICE = r"\bvoice|speak(ing)?\b|speech|\bmic\b|microphone|dictat"

path = sys.argv[1] if len(sys.argv) > 1 else "chatgpt_reviews_low.csv"
df = pd.read_csv(path).drop_duplicates("review").reset_index(drop=True)
df["words"] = df["review"].str.split().str.len()
sub = df[df.words >= 8]
t = sub["review"].str.lower()
print(f"{len(df)} unique reviews, {len(sub)} with 8+ words, {df['date'].min()} to {df['date'].max()}")
print("\nThemes (share of long reviews):")
for name, pat in THEMES.items():
    m = t.str.contains(pat, regex=True)
    print(f"  {name}: {m.sum()} ({m.mean() * 100:.1f}%)")
print("\nFee confusion (all unique reviews):")
ta = df["review"].str.lower()
for name, pat in FEE.items():
    print(f"  {name}: {ta.str.contains(pat, regex=True).sum()}")
v = ta.str.contains(VOICE, regex=True)
print(f"\nVoice mentions: {v.sum()} ({v.mean() * 100:.1f}%), avg rating {df[v].rating.mean():.2f}")
