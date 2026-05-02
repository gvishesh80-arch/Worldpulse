import os
import json
import urllib.request
import urllib.error
import datetime

# ── CONFIG ─────────────────────────────────────────
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
if not API_KEY:
    print("FATAL: ANTHROPIC_API_KEY missing")
    raise SystemExit(1)

MODEL = "claude-3-haiku-20240307"
today = datetime.datetime.now().strftime("%A, %B %d, %Y")

print("Running for:", today)

# ── PROMPT ─────────────────────────────────────────
SYSTEM = f"""
You are the editor of WorldPulse. Today is {today}.
Return ONLY valid JSON. No markdown.

Structure:
{{
  "date": "{today}",
  "breaking_ticker": ["headline 1","headline 2","headline 3","headline 4","headline 5"],
  "articles": [
    {{
      "id": "story-one",
      "cat": "World",
      "tag": "Breaking",
      "headline": "Real world headline",
      "deck": "2-3 sentence summary.",
      "author": "Editor",
      "role": "Correspondent",
      "time": "Today",
      "read_time": "5 min",
      "hero_icon": "globe",
      "body_html": "<p>Minimum 400 words article.</p>"
    }}
  ]
}}

Replace everything with REAL content.
"""

payload = json.dumps({
    "model": MODEL,
    "max_tokens": 4000,
    "system": SYSTEM,
    "messages": [{"role": "user", "content": "Generate full news JSON"}]
}).encode("utf-8")

req = urllib.request.Request(
    "https://api.anthropic.com/v1/messages",
    data=payload,
    headers={
        "Content-Type": "application/json",
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01"
    }
)

# ── CALL API ───────────────────────────────────────
try:
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        raw = result["content"][0]["text"].strip()
except urllib.error.HTTPError as e:
    print("API ERROR:", e.code)
    print(e.read().decode())
    raise SystemExit(1)

# ── PARSE JSON ─────────────────────────────────────
try:
    data = json.loads(raw)
except:
    print("JSON FAILED")
    print(raw[:500])
    raise SystemExit(1)

articles = data.get("articles", [])

# ── BUILD HTML ─────────────────────────────────────
html_articles = ""
for a in articles:
    html_articles += f"""
    <div class="card">
        <h2>{a.get("headline")}</h2>
        <p>{a.get("deck")}</p>
        <div>{a.get("body_html")}</div>
    </div>
    """

html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>WorldPulse</title>
<style>
body {{ font-family: Arial; background:#111; color:#eee; padding:20px; }}
.card {{ background:#1e1e1e; padding:20px; margin:20px 0; border-radius:10px; }}
h2 {{ color:#ff4d4d; }}
</style>
</head>
<body>

<h1>WorldPulse — {today}</h1>

{html_articles}

</body>
</html>
"""

# ── SAVE FILE ──────────────────────────────────────
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ Website generated: index.html")
