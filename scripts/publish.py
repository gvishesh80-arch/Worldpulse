import os
import json
import urllib.request
import urllib.error
import datetime

# ── CONFIG ──────────────────────────────────────────────────────────────────
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
if not API_KEY:
    print("FATAL: ANTHROPIC_API_KEY secret is missing")
    raise SystemExit(1)

print("API key found: ..." + API_KEY[-6:])
MODEL = "claude-haiku-4-5-20251001"
today = datetime.datetime.now().strftime("%A, %B %d, %Y")
print("Generating blog for: " + today)

# ── PROMPT ──────────────────────────────────────────────────────────────────
SYSTEM = (
    "You are the editor of WorldPulse, a global news blog. Today is " + today + ".\n"
    "Return a single valid JSON object. No markdown. No backticks. Just raw JSON.\n"
    "Use this structure:\n"
    "{\n"
    '  "date": "' + today + '",\n'
    '  "breaking_ticker": ["headline 1","headline 2","headline 3","headline 4","headline 5"],\n'
    '  "markets": [\n'
    '    {"label":"S&P 500","value":"5241","change":"UP +0.4%","dir":"up"},\n'
    '    {"label":"Crude Oil","value":"$81","change":"DOWN -0.8%","dir":"down"},\n'
    '    {"label":"Gold","value":"$2398","change":"UP +0.3%","dir":"up"},\n'
    '    {"label":"EUR/USD","value":"1.071","change":"DOWN -0.1%","dir":"down"},\n'
    '    {"label":"10Y Treasury","value":"4.68%","change":"UP +2bps","dir":"up"}\n'
    '  ],\n'
    '  "articles": [\n'
    '    {\n'
    '      "id": "story-one",\n'
    '      "cat": "Geopolitics",\n'
    '      "tag": "Breaking",\n'
    '      "headline": "Write real headline for biggest world story today",\n'
    '      "deck": "Write 2-3 sentences summarising this story.",\n'
    '      "author": "Marcus Osei",\n'
    '      "role": "Senior Correspondent",\n'
    '      "time": "Today, 8:00 AM",\n'
    '      "read_time": "5 min read",\n'
    '      "hero_icon": "globe",\n'
    '      "body_html": "<p>Write full article minimum 400 words about the biggest geopolitical story happening today ' + today + '. Include real facts, figures, official quotes, context and analysis.</p><h3>Background</h3><p>Historical context and why this matters globally.</p><h3>What Happens Next</h3><p>Analysis and outlook.</p>"\n'
    '    },\n'
    '    {\n'
    '      "id": "story-two",\n'
    '      "cat": "Economy",\n'
    '      "tag": "Markets",\n'
    '      "headline": "Write real headline for biggest economic story today",\n'
    '      "deck": "Write 2-3 sentences about this economic story.",\n'
    '      "author": "Amina Diallo",\n'
    '      "role": "Economics Correspondent",\n'
    '      "time": "Today, 7:00 AM",\n'
    '      "read_time": "4 min read",\n'
    '      "hero_icon": "chart",\n'
    '      "body_html": "<p>Write full economic article minimum 350 words. Include real market data, expert opinions and implications for ordinary people.</p><h3>Market Reaction</h3><p>How markets responded and what analysts say.</p>"\n'
    '    },\n'
    '    {\n'
    '      "id": "story-three",\n'
    '      "cat": "Science",\n'
    '      "tag": "Discovery",\n'
    '      "headline": "Write real headline for important science or health story today",\n'
    '      "deck": "Write 2-3 sentences about this science story.",\n'
    '      "author": "Dr. Priya Menon",\n'
    '      "role": "Science Correspondent",\n'
    '      "time": "Today, 9:00 AM",\n'
    '      "read_time": "4 min read",\n'
    '      "hero_icon": "microscope",\n'
    '      "body_html": "<p>Write full science article minimum 350 words. Explain the discovery in plain English, who did the research, and why it matters for humanity.</p>"\n'
    '    },\n'
    '    {\n'
    '      "id": "story-four",\n'
    '      "cat": "Europe",\n'
    '      "tag": "Conflict",\n'
    '      "headline": "Write real headline for a conflict or crisis story today",\n'
    '      "deck": "Write 2-3 sentences about this conflict.",\n'
    '      "author": "Anna Kovalenko",\n'
    '      "role": "Europe Correspondent",\n'
    '      "time": "Today, 6:00 AM",\n'
    '      "read_time": "4 min read",\n'
    '      "hero_icon": "alert",\n'
    '      "body_html": "<p>Write full conflict article minimum 350 words with real facts and official statements.</p>"\n'
    '    },\n'
    '    {\n'
    '      "id": "story-five",\n'
    '      "cat": "Asia",\n'
    '      "tag": "Diplomacy",\n'
    '      "headline": "Write real headline for a major Asia story today",\n'
    '      "deck": "Write 2-3 sentences about this Asia story.",\n'
    '      "author": "Kenji Tanaka",\n'
    '      "role": "Asia Correspondent",\n'
    '      "time": "Today, 5:00 AM",\n'
    '      "read_time": "4 min read",\n'
    '      "hero_icon": "world",\n'
    '      "body_html": "<p>Write full Asia article minimum 350 words covering key developments and regional implications.</p>"\n'
    '    }\n'
    '  ],\n'
    '  "claude_ai_article": {\n'
    '    "id": "claude-ai-today",\n'
    '    "cat": "Claude AI",\n'
    '    "tag": "AI Column",\n'
    '    "headline": "Write compelling headline about what Anthropic and Claude AI are doing this week",\n'
    '    "deck": "Write 2-3 sentences about the most important AI development this week.",\n'
    '    "author": "James Park",\n'
    '    "role": "AI Correspondent",\n'
    '    "time": "Today, 6:00 AM",\n'
    '    "read_time": "7 min read",\n'
    '    "hero_icon": "brain",\n'
    '    "body_html": "<p>Write full AI column minimum 500 words. Cover what Anthropic released this week, what Claude can now do, genuine benefits for humanity in healthcare education science, and real risks including job displacement concentration of power and misuse. Be honest and balanced.</p><h3>What Anthropic Built</h3><p>Specific details about latest Claude capabilities.</p><h3>Benefits For Humanity</h3><p>Concrete real world benefits with specific examples.</p><h3>The Risks</h3><p>Honest assessment of genuine risks and concerns.</p><h3>The Bottom Line</h3><p>Your honest journalistic conclusion about where AI is heading.</p>"\n'
    '  },\n'
    '  "live_updates": [\n'
    '    {"tag":"war","tag_label":"Conflict","text":"<strong>Conflict:</strong> Write real live update about military situation today."},\n'
    '    {"tag":"diplo","tag_label":"Diplomacy","text":"<strong>Diplomacy:</strong> Write real live update about international talks today."},\n'
    '    {"tag":"econ","tag_label":"Markets","text":"<strong>Markets:</strong> Write real live update about economic development today."},\n'
    '    {"tag":"ai","tag_label":"Tech","text":"<strong>Technology:</strong> Write real live update about technology development today."},\n'
    '    {"tag":"sci","tag_label":"Science","text":"<strong>Science:</strong> Write real live update about science development today."}\n'
    '  ]\n'
    "}\n"
    "CRITICAL: Replace ALL placeholder text with REAL content about " + today + "\n"
    "Return ONLY the JSON. Nothing before it. Nothing after it."
)

USER = "Today is " + today + ". Generate the complete WorldPulse blog. Return only JSON."

# ── CALL API ─────────────────────────────────────────────────────────────────
print("Calling Claude API...")
payload = json.dumps({
    "model": MODEL,
    "max_tokens": 7000,
    "system": SYSTEM,
    "messages": [{"role": "user", "content": USER}]
}).encode("utf-8")

req = urllib.request.Request(
    "https://api.anthropic.com/v1/messages",
    data=payload,
    headers={
        "Content-Type": "application/json",
        "x-api-key": API_KEY,
        "anthropic-version": "2023-06-01"
    },
    method="POST"
)

try:
    with urllib.request.urlopen(req, timeout=120) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        raw = result["content"][0]["text"].strip()
        print("API response: " + str(len(raw)) + " chars")
except urllib.error.HTTPError as e:
    print("API HTTP ERROR " + str(e.code) + ": " + e.read().decode("utf-8"))
    raise SystemExit(1)
except Exception as e:
    print("API ERROR: " + str(e))
    raise SystemExit(1)

# ── PARSE JSON ───────────────────────────────────────────────────────────────
print("Parsing JSON...")
clean = raw
if clean.startswith("```"):
    clean = "\n".join(clean.split("\n")[1:])
if clean.endswith("```"):
    clean = clean.rsplit("```", 1)[0]
clean = clean.strip()

try:
    data = json.loads(clean)
except json.JSONDecodeError as e:
    print("JSON ERROR: " + str(e))
    print("Response start: " + clean[:300])
    raise SystemExit(1)

print("Got " + str(len(data.get("articles", []))) + " articles")

# ── HELPERS ──────────────────────────────────────────────────────────────────
ICONS = {
    "globe": "🌍", "chart": "📈", "microscope": "🔬",
    "alert": "⚠️", "world": "🌏", "brain": "🧠",
    "shield": "🛡️", "dollar": "💵"
}

def icon(key):
    return ICONS.get(key, "📰")

def kicker_html(cat, tag, cls=""):
    return f'<div class="kicker {cls}">{cat} · {tag}</div>'

def article_card_html(a, onclick_id):
    return f'''
    <div class="card" onclick="openModal('{onclick_id}')">
      <div class="card-img">{icon(a.get("hero_icon",""))}</div>
      {kicker_html(a.get("cat",""), a.get("tag",""), "gold")}
      <div class="hl3">{a.get("headline","")}</div>
      <div class="deck3">{a.get("deck","")}</div>
      <div class="byline" style="margin-top:10px;"><strong>{a.get("author","")}</strong> · {a.get("time","")}</div>
    </div>'''

# ── BUILD HTML ───────────────────────────────────────────────────────────────
print("Building HTML...")

articles = data.get("articles", [])
lead = articles[0] if articles else {}
sides = articles[1:3]
cards = articles[3:]
ai_art = data.get("claude_ai_article", {})
ticker_items = data.get("breaking_ticker", [])
markets = data.get("markets", [])
live_updates = data.get("live_updates", [])
date_str = data.get("date", today)

# Ticker HTML
ticker_doubled = ticker_items * 2
ticker_spans = "".join(f"<span>{h}</span>" for h in ticker_doubled)

# Markets HTML
markets_html = "".join(f'''
  <div class="m-item">
    <div>
      <div class="m-label">{m.get("label","")}</div>
      <div class="m-val">{m.get("value","")}</div>
    </div>
    <div class="m-chg {m.get("dir","")}">{m.get("change","")}</div>
  </div>''' for m in markets)

# Hero HTML
lead_html = f'''
<div class="hero-lead">
  <div class="hero-img" onclick="openModal('{lead.get("id","")}')">{icon(lead.get("hero_icon",""))}</div>
  {kicker_html(lead.get("cat",""), lead.get("tag",""))}
  <h1 class="hero-hl" onclick="openModal('{lead.get("id","")}')">{lead.get("headline","")}</h1>
  <p class="deck">{lead.get("deck","")}</p>
  <div class="byline"><strong>{lead.get("author","")}</strong> · {lead.get("role","")}&nbsp;·&nbsp;{lead.get("time","")}&nbsp;·&nbsp;{lead.get("read_time","")}</div>
  <button class="read-btn" onclick="openModal('{lead.get("id","")}')" >Read full story →</button>
</div>
<div class="hero-side">
  {"".join(f'''
  <div class="hero-side-item">
    <div class="side-img" onclick="openModal(\'{s.get("id","")}\')"\>{icon(s.get("hero_icon",""))}</div>
    {kicker_html(s.get("cat",""), s.get("tag",""), "teal")}
    <div class="hl2" onclick="openModal(\'{s.get("id","")}\')\">{s.get("headline","")}</div>
    <div class="deck2">{s.get("deck","")}</div>
    <div class="byline" style="margin-top:8px;"><strong>{s.get("author","")}</strong> · {s.get("time","")}</div>
    <button class="read-btn" onclick="openModal(\'{s.get("id","")}\')">Read →</button>
  </div>''' for s in sides)}
</div>''' if lead else ""

# Cards HTML
cards_html = "".join(article_card_html(a, a.get("id","")) for a in cards)

# AI dark section
ai_html = f'''
<div class="dark-feat" onclick="openModal('{ai_art.get("id","")}')" >
  <div>
    <div class="df-kicker">{ai_art.get("cat","")} · {ai_art.get("tag","")}</div>
    <div class="df-hl">{ai_art.get("headline","")}</div>
    <div class="df-deck">{ai_art.get("deck","")}</div>
    <div class="df-read">Read the full column →</div>
  </div>
  <div class="df-vis">{icon(ai_art.get("hero_icon","brain"))}</div>
</div>''' if ai_art else ""

# Live updates HTML
update_times = ["Breaking", "Just now", "2 min ago", "5 min ago", "8 min ago"]
live_html = "".join(f'''
<div class="u-item">
  <div class="u-time"><span class="utag {u.get("tag","")}">{u.get("tag_label","")}</span><br>{update_times[i] if i < len(update_times) else ""}</div>
  <div class="u-text">{u.get("text","")}</div>
</div>''' for i, u in enumerate(live_updates))

# Most read HTML
all_arts = articles + ([ai_art] if ai_art else [])
most_read_html = "".join(f'''
<div class="mr-item" onclick="openModal('{a.get("id","")}')" >
  <div class="mr-num">{i+1}</div>
  <div>
    <div class="mr-title">{a.get("headline","")}</div>
    <div class="mr-meta">{a.get("cat","")} · {a.get("read_time","4 min read")}</div>
  </div>
</div>''' for i, a in enumerate(all_arts[:5]))

# Sidebar stats
sidebar_stats_html = "".join(f'''
<div class="sb-stat">
  <span class="sb-stat-label">{label}</span>
  <span class="sb-stat-val">{val}</span>
</div>''' for label, val in [
    ("Stories today", len(all_arts)),
    ("Regions covered", "6"),
    ("Live updates", len(live_updates)),
    ("Last updated", "Now")
])

# All articles JSON for modal
all_arts_json = json.dumps(all_arts, ensure_ascii=False)
ai_art_json = json.dumps(ai_art, ensure_ascii=False)

# ── FULL HTML ─────────────────────────────────────────────────────────────────
html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<meta name="description" content="WorldPulse - Global Intelligence Daily - {date_str}"/>
<title>WorldPulse — {date_str}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=Source+Serif+4:opsz,wght@8..60,300;8..60,400;8..60,600&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet"/>
<style>
:root{{
  --ink:#0f0e0d;--paper:#f6f2ea;--cream:#faf7f2;--red:#c41e3a;--gold:#b8860b;
  --teal:#1a5f7a;--rule:#ddd6c8;--mist:#8a8680;--surf:#fff;--blue:#1a3a5c;
}}
*{{margin:0;padding:0;box-sizing:border-box;}}
html{{scroll-behavior:smooth;}}
body{{background:var(--paper);color:var(--ink);font-family:"Source Serif 4",Georgia,serif;font-size:17px;line-height:1.7;}}
.ticker{{background:var(--red);color:#fff;height:34px;display:flex;overflow:hidden;position:sticky;top:0;z-index:200;}}
.ticker-tag{{background:#000;color:#fff;padding:0 14px;font-family:"Space Mono",monospace;font-size:10px;letter-spacing:2px;display:flex;align-items:center;flex-shrink:0;text-transform:uppercase;}}
.ticker-track{{overflow:hidden;flex:1;display:flex;align-items:center;}}
.ticker-inner{{display:flex;white-space:nowrap;animation:tick 60s linear infinite;}}
.ticker-inner span{{font-size:11px;padding:0 36px;}}
.ticker-inner span::after{{content:"◆";margin-left:36px;opacity:.4;}}
@keyframes tick{{0%{{transform:translateX(0)}}100%{{transform:translateX(-50%)}}}}
.masthead{{background:var(--ink);padding:0 24px;border-bottom:3px solid var(--red);}}
.mast-top{{display:flex;align-items:center;justify-content:space-between;padding:16px 0 12px;border-bottom:1px solid rgba(255,255,255,.08);}}
.mast-date{{font-family:"Space Mono",monospace;font-size:9px;color:rgba(255,255,255,.4);letter-spacing:1px;text-transform:uppercase;}}
.mast-logo{{text-align:center;flex:1;}}
.logo-name{{font-family:"Playfair Display",serif;font-weight:900;font-size:clamp(1.8rem,5vw,3.5rem);color:#fff;letter-spacing:-1px;line-height:1;text-transform:uppercase;cursor:pointer;text-decoration:none;display:block;}}
.logo-name span{{color:var(--red);}}
.logo-tag{{font-family:"Space Mono",monospace;font-size:8px;color:rgba(255,255,255,.3);letter-spacing:4px;text-transform:uppercase;margin-top:3px;}}
.btn-sub{{background:var(--red);color:#fff;border:none;padding:8px 16px;font-family:"Space Mono",monospace;font-size:9px;letter-spacing:1px;text-transform:uppercase;cursor:pointer;}}
.nav{{display:flex;overflow-x:auto;scrollbar-width:none;}}
.nav::-webkit-scrollbar{{display:none;}}
.nav-item{{font-family:"Space Mono",monospace;font-size:9px;letter-spacing:1.5px;text-transform:uppercase;color:rgba(255,255,255,.5);padding:11px 16px;cursor:pointer;border-bottom:3px solid transparent;white-space:nowrap;text-decoration:none;transition:color .2s;}}
.nav-item:hover,.nav-item.active{{color:#fff;border-bottom-color:var(--red);}}
.markets{{display:flex;background:var(--cream);border-bottom:2px solid var(--rule);overflow-x:auto;padding:0 24px;}}
.m-item{{display:flex;align-items:center;gap:7px;padding:8px 18px 8px 0;border-right:1px solid var(--rule);white-space:nowrap;}}
.m-item:last-child{{border-right:none;}}
.m-label{{font-family:"Space Mono",monospace;font-size:8px;letter-spacing:1px;color:var(--mist);text-transform:uppercase;}}
.m-val{{font-family:"Space Mono",monospace;font-size:11px;font-weight:700;color:var(--ink);}}
.m-chg{{font-family:"Space Mono",monospace;font-size:9px;}}
.up{{color:#2a9e60;}}.down{{color:var(--red);}}
.container{{max-width:1200px;margin:0 auto;padding:0 24px;}}
.sec-hd{{display:flex;align-items:center;gap:12px;margin:36px 0 20px;}}
.sec-title{{font-family:"Playfair Display",serif;font-size:1.4rem;font-weight:900;text-transform:uppercase;color:var(--ink);}}
.sec-rule{{flex:1;height:2px;background:var(--rule);}}
.sec-rule.red{{background:var(--red);}}
.hero-grid{{display:grid;grid-template-columns:1.5fr 1fr;gap:2px;background:var(--rule);border:2px solid var(--rule);margin-top:28px;}}
.hero-lead{{background:var(--surf);padding:24px 28px;position:relative;}}
.hero-lead::before{{content:"";position:absolute;top:0;left:0;right:0;height:4px;background:var(--red);}}
.hero-img{{width:100%;height:240px;display:flex;align-items:center;justify-content:center;font-size:70px;margin-bottom:18px;cursor:pointer;background:linear-gradient(160deg,#0f1520,#1a3a58);border-radius:2px;}}
.kicker{{font-family:"Space Mono",monospace;font-size:8px;letter-spacing:2px;text-transform:uppercase;color:var(--red);border-top:2px solid var(--red);padding-top:4px;display:inline-block;margin-bottom:9px;}}
.kicker.teal{{color:var(--teal);border-top-color:var(--teal);}}
.kicker.gold{{color:var(--gold);border-top-color:var(--gold);}}
h1.hero-hl{{font-family:"Playfair Display",serif;font-weight:900;font-size:clamp(1.4rem,2.4vw,2.1rem);line-height:1.15;color:var(--ink);margin-bottom:12px;cursor:pointer;transition:color .2s;}}
h1.hero-hl:hover{{color:var(--red);}}
.deck{{font-size:14px;color:#444;line-height:1.7;font-weight:300;margin-bottom:12px;}}
.byline{{font-family:"Space Mono",monospace;font-size:8px;color:var(--mist);letter-spacing:.8px;text-transform:uppercase;padding-top:11px;border-top:1px solid var(--rule);}}
.byline strong{{color:var(--ink);}}
.read-btn{{font-family:"Space Mono",monospace;font-size:9px;letter-spacing:1px;text-transform:uppercase;color:var(--red);cursor:pointer;display:inline-flex;align-items:center;gap:4px;margin-top:9px;background:none;border:none;text-decoration:none;}}
.read-btn:hover{{text-decoration:underline;}}
.hero-side{{background:var(--surf);display:flex;flex-direction:column;}}
.hero-side-item{{padding:20px 24px;flex:1;}}
.hero-side-item+.hero-side-item{{border-top:2px solid var(--rule);}}
.side-img{{width:100%;height:100px;margin-bottom:11px;display:flex;align-items:center;justify-content:center;font-size:34px;cursor:pointer;background:linear-gradient(160deg,#0f1520,#1a2a38);border-radius:2px;}}
.hl2{{font-family:"Playfair Display",serif;font-weight:700;font-size:1rem;line-height:1.3;color:var(--ink);cursor:pointer;margin-bottom:5px;transition:color .2s;}}
.hl2:hover{{color:var(--red);}}
.deck2{{font-size:12px;color:#555;line-height:1.6;font-weight:300;}}
.card-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:2px;background:var(--rule);border:2px solid var(--rule);}}
.card{{background:var(--surf);padding:20px;cursor:pointer;transition:background .15s;}}
.card:hover{{background:#fffef9;}}
card-img{{width:100%;height:130px;display:flex;align-items:center;justify-content:center;font-size:36px;margin-bottom:12px;background:linear-gradient(160deg,#0f1520,#1a2a38);border-radius:2px;}}
.hl3{{font-family:"Playfair Display",serif;font-weight:700;font-size:.95rem;line-height:1.3;color:var(--ink);margin-bottom:5px;transition:color .2s;}}
.hl3:hover{{color:var(--red);}}
.deck3{{font-size:11px;color:#555;line-height:1.6;font-weight:300;}}
.dark-feat{{background:var(--ink);padding:34px 40px;display:grid;grid-template-columns:1.3fr 1fr;gap:36px;align-items:center;cursor:pointer;margin:2px 0;transition:background .2s;}}
.dark-feat:hover{{background:#1a1917;}}
.df-kicker{{font-family:"Space Mono",monospace;font-size:8px;letter-spacing:2px;text-transform:uppercase;color:rgba(232,160,160,.8);border-top:2px solid var(--red);padding-top:4px;display:inline-block;margin-bottom:10px;}}
.df-hl{{font-family:"Playfair Display",serif;font-weight:900;font-size:clamp(1.3rem,2vw,1.8rem);line-height:1.2;color:#fff;margin-bottom:10px;}}
.df-deck{{font-size:13px;color:rgba(255,255,255,.6);line-height:1.7;}}
.df-read{{font-family:"Space Mono",monospace;font-size:9px;color:rgba(232,160,160,.8);display:inline-block;margin-top:10px;}}
.df-vis{{font-size:90px;opacity:.14;text-align:center;}}
.live-sec{{background:var(--ink);padding:30px 0;margin:36px 0;}}
.live-badge{{display:inline-flex;align-items:center;gap:6px;background:var(--red);color:#fff;font-family:"Space Mono",monospace;font-size:9px;letter-spacing:2px;padding:4px 11px;text-transform:uppercase;margin-bottom:16px;}}
.live-dot{{width:6px;height:6px;background:#fff;border-radius:50%;animation:blink 1.4s ease infinite;}}
@keyframes blink{{0%,100%{{opacity:1}}50%{{opacity:.3}}}}
.live-title{{font-family:"Playfair Display",serif;font-size:1.3rem;font-weight:900;color:#fff;margin-bottom:18px;}}
.u-item{{display:grid;grid-template-columns:80px 1fr;gap:14px;padding:12px 0;border-bottom:1px solid rgba(255,255,255,.07);}}
.u-time{{font-family:"Space Mono",monospace;font-size:10px;color:var(--red);}}
.u-text{{font-size:12px;color:rgba(255,255,255,.78);line-height:1.6;}}
.u-text strong{{color:#fff;}}
.utag{{display:inline-block;font-family:"Space Mono",monospace;font-size:7px;letter-spacing:1px;padding:2px 6px;margin-right:5px;text-transform:uppercase;border:1px solid;}}
.utag.war{{border-color:#ff7070;color:#ff7070;}}.utag.econ{{border-color:#60c878;color:#60c878;}}
.utag.ai{{border-color:#a090f0;color:#a090f0;}}.utag.diplo{{border-color:#f0c040;color:#f0c040;}}
.utag.sci{{border-color:#60aaf0;color:#60aaf0;}}
.bot-grid{{display:grid;grid-template-columns:2fr 280px;gap:2px;background:var(--rule);border:2px solid var(--rule);margin-bottom:36px;}}
.most-read{{background:var(--surf);padding:22px;}}
.mr-item{{display:grid;grid-template-columns:28px 1fr;gap:11px;padding:11px 0;border-bottom:1px solid var(--rule);cursor:pointer;}}
.mr-item:last-child{{border-bottom:none;}}
.mr-item:hover .mr-title{{color:var(--red);}}
.mr-num{{font-family:"Playfair Display",serif;font-size:1.5rem;font-weight:900;color:var(--rule);line-height:1;}}
.mr-title{{font-family:"Playfair Display",serif;font-size:.85rem;font-weight:700;color:var(--ink);line-height:1.3;margin-bottom:2px;transition:color .2s;}}
.mr-meta{{font-size:10px;color:var(--mist);}}
.sidebar{{background:var(--surf);padding:18px;}}
.sb-title{{font-family:"Space Mono",monospace;font-size:8px;letter-spacing:2px;text-transform:uppercase;color:var(--mist);border-bottom:1px solid var(--rule);padding-bottom:10px;margin-bottom:14px;}}
.sb-tag-cloud{{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:18px;}}
.sb-tag{{font-family:"Space Mono",monospace;font-size:8px;letter-spacing:1px;padding:4px 8px;border:1px solid var(--rule);color:var(--mist);cursor:pointer;text-transform:uppercase;transition:all .2s;}}
.sb-tag:hover{{border-color:var(--red);color:var(--red);}}
.sb-stat{{display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid var(--rule);}}
.sb-stat-label{{font-size:11px;color:#555;}}
.sb-stat-val{{font-family:"Space Mono",monospace;font-size:10px;font-weight:700;color:var(--ink);}}
footer{{background:var(--ink);color:rgba(255,255,255,.4);padding:40px 24px 24px;}}
.footer-grid{{max-width:1200px;margin:0 auto;display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:36px;border-bottom:1px solid rgba(255,255,255,.08);padding-bottom:30px;margin-bottom:24px;}}
.footer-brand{{font-family:"Playfair Display",serif;font-weight:900;font-size:1.8rem;color:#fff;text-transform:uppercase;letter-spacing:-1px;margin-bottom:8px;}}
.footer-brand span{{color:var(--red);}}
.footer-desc{{font-size:12px;line-height:1.7;}}
.footer-col-title{{font-family:"Space Mono",monospace;font-size:8px;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,.2);margin-bottom:12px;}}
.footer-link{{display:block;font-size:11px;color:rgba(255,255,255,.5);text-decoration:none;margin-bottom:7px;transition:color .2s;}}
.footer-link:hover{{color:#fff;}}
.footer-bottom{{max-width:1200px;margin:0 auto;display:flex;justify-content:space-between;align-items:center;font-family:"Space Mono",monospace;font-size:8px;letter-spacing:1px;text-transform:uppercase;}}
.modal-overlay{{position:fixed;inset:0;background:rgba(0,0,0,.85);z-index:1000;display:flex;align-items:center;justify-content:center;padding:20px;opacity:0;pointer-events:none;transition:opacity .3s;}}
.modal-overlay.open{{opacity:1;pointer-events:all;}}
.modal{{background:var(--surf);max-width:780px;width:100%;max-height:88vh;overflow-y:auto;position:relative;border-top:4px solid var(--red);}}
.modal-close{{position:sticky;top:0;display:flex;justify-content:flex-end;padding:12px 16px 0;background:var(--surf);z-index:1;}}
.modal-close-btn{{background:none;border:none;font-size:22px;cursor:pointer;color:var(--mist);line-height:1;}}
.modal-close-btn:hover{{color:var(--red);}}
.modal-body{{padding:32px 40px 40px;}}
.modal-kicker{{font-family:"Space Mono",monospace;font-size:8px;letter-spacing:2px;text-transform:uppercase;color:var(--red);border-top:2px solid var(--red);padding-top:4px;display:inline-block;margin-bottom:12px;}}
.modal-hl{{font-family:"Playfair Display",serif;font-weight:900;font-size:clamp(1.5rem,3vw,2.2rem);line-height:1.15;color:var(--ink);margin-bottom:16px;}}
.modal-meta{{font-family:"Space Mono",monospace;font-size:8px;color:var(--mist);letter-spacing:.8px;text-transform:uppercase;padding:12px 0;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);margin-bottom:22px;}}
.modal-content{{font-size:15px;line-height:1.85;color:#333;}}
.modal-content h3{{font-family:"Playfair Display",serif;font-size:1.1rem;font-weight:700;color:var(--ink);margin:24px 0 10px;border-left:3px solid var(--red);padding-left:12px;}}
.modal-content p{{margin-bottom:16px;}}
@media(max-width:768px){{
  .hero-grid{{grid-template-columns:1fr;}}.card-grid{{grid-template-columns:1fr;}}
  .dark-feat{{grid-template-columns:1fr;padding:24px;}}.df-vis{{display:none;}}
  .bot-grid{{grid-template-columns:1fr;}}.footer-grid{{grid-template-columns:1fr 1fr;}}
  .mast-date,.btn-sub{{display:none;}}.modal-body{{padding:20px;}}
}}
@media(max-width:480px){{.footer-grid{{grid-template-columns:1fr;}}}}
</style>
</head>
<body>
<div class="ticker">
  <div class="ticker-tag">◉ Live</div>
  <div class="ticker-track">
    <div class="ticker-inner">{ticker_spans}</div>
  </div>
</div>

<header class="masthead">
  <div class="mast-top">
    <div class="mast-date">{date_str}</div>
    <div class="mast-logo">
      <a class="logo-name" href="#">World<span>Pulse</span></a>
      <div class="logo-tag">Global Intelligence Daily</div>
    </div>
    <button class="btn-sub">Subscribe</button>
  </div>
  <nav class="nav">
    <a class="nav-item active" href="#">Top Stories</a>
    <a class="nav-item" href="#">Geopolitics</a>
    <a class="nav-item" href="#">Economy</a>
    <a class="nav-item" href="#">Europe</a>
    <a class="nav-item" href="#">Asia</a>
    <a class="nav-item" href="#">Science</a>
    <a class="nav-item" href="#">Technology</a>
    <a class="nav-item" href="#">Climate</a>
    <a class="nav-item" href="#">Opinion</a>
  </nav>
</header>

<div class="markets">{markets_html}</div>

<main>
  <div class="container">
    <div class="sec-hd">
      <div class="sec-title">Top Stories</div>
      <div class="sec-rule red"></div>
    </div>
    <div class="hero-grid">{lead_html}</div>
  </div>

  <div class="live-sec">
    <div class="container">
      <div class="live-badge"><span class="live-dot"></span> Live Updates</div>
      <div class="live-title">Breaking: Follow Live</div>
      {live_html}
    </div>
  </div>

  <div class="container">
    <div class="sec-hd">
      <div class="sec-title">More Stories</div>
      <div class="sec-rule"></div>
    </div>
    <div class="card-grid">{cards_html}</div>
  </div>

  <div class="container" style="margin-top:2px;">
    {ai_html}
  </div>

  <div class="container" style="margin-top:36px;">
    <div class="bot-grid">
      <div class="most-read">
        <div class="sec-hd" style="margin-top:0;margin-bottom:16px;">
          <div class="sec-title" style="font-size:1rem;">Most Read</div>
          <div class="sec-rule"></div>
        </div>
        {most_read_html}
      </div>
      <div class="sidebar">
        <div class="sb-title">Topics</div>
        <div class="sb-tag-cloud">
          <div class="sb-tag">Geopolitics</div><div class="sb-tag">Economy</div>
          <div class="sb-tag">Ukraine</div><div class="sb-tag">China</div>
          <div class="sb-tag">AI</div><div class="sb-tag">Climate</div>
          <div class="sb-tag">Middle East</div><div class="sb-tag">Markets</div>
          <div class="sb-tag">Science</div><div class="sb-tag">Health</div>
        </div>
        <div class="sb-title" style="margin-top:18px;">At a Glance</div>
        {sidebar_stats_html}
      </div>
    </div>
  </div>
</main>

<div class="modal-overlay" id="modalOverlay" onclick="closeModal(event)">
  <div class="modal" id="modalBox">
    <div class="modal-close"><button class="modal-close-btn" onclick="closeModalDirect()">✕</button></div>
    <div class="modal-body">
      <div class="modal-kicker" id="mKicker"></div>
      <div class="modal-hl" id="mHl"></div>
      <div class="modal-meta" id="mMeta"></div>
      <div class="modal-content" id="mContent"></div>
    </div>
  </div>
</div>

<footer>
  <div class="footer-grid">
    <div>
      <div class="footer-brand">World<span>Pulse</span></div>
      <p class="footer-desc">Global Intelligence Daily — independent, rigorous reporting from correspondents across six continents. Powered by Claude AI. Updated daily.</p>
    </div>
    <div>
      <div class="footer-col-title">Sections</div>
      <a class="footer-link" href="#">Geopolitics</a>
      <a class="footer-link" href="#">Economy</a>
      <a class="footer-link" href="#">Science</a>
      <a class="footer-link" href="#">Technology</a>
    </div>
    <div>
      <div class="footer-col-title">Regions</div>
      <a class="footer-link" href="#">Europe</a>
      <a class="footer-link" href="#">Asia</a>
      <a class="footer-link" href="#">Americas</a>
      <a class="footer-link" href="#">Middle East</a>
    </div>
    <div>
      <div class="footer-col-title">Company</div>
      <a class="footer-link" href="#">About</a>
      <a class="footer-link" href="#">Contact</a>
      <a class="footer-link" href="#">Privacy</a>
    </div>
  </div>
  <div class="footer-bottom">
    <span>© 2026 WorldPulse. Powered by Claude AI.</span>
    <span>{date_str}</span>
  </div>
</footer>

<script>
const ALL_ARTICLES = {all_arts_json};

function openModal(id) {{
  const art = ALL_ARTICLES.find(a => a.id === id);
  if(!art) return;
  document.getElementById('mKicker').textContent = art.cat + ' · ' + art.tag;
  document.getElementById('mHl').textContent = art.headline;
  document.getElementById('mMeta').innerHTML = '<strong>' + art.author + '</strong> · ' + art.role + ' · ' + art.time + ' · ' + art.read_time;
  document.getElementById('mContent').innerHTML = art.body_html;
  document.getElementById('modalOverlay').classList.add('open');
  document.body.style.overflow = 'hidden';
}}
function closeModal(e) {{
  if(e.target === document.getElementById('modalOverlay')) closeModalDirect();
}}
function closeModalDirect() {{
  document.getElementById('modalOverlay').classList.remove('open');
  document.body.style.overflow = '';
}}
document.addEventListener('keydown', e => {{ if(e.key === 'Escape') closeModalDirect(); }});
</script>
</body>
</html>'''

# ── WRITE OUTPUT ──────────────────────────────────────────────────────────────
os.makedirs("docs", exist_ok=True)
out_path = os.path.join("docs", "index.html")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(html)

print("Written: " + out_path)
print("Done! WorldPulse is ready.")
