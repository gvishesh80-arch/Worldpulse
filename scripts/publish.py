import os
import json
import urllib.request
import datetime

API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
if not API_KEY:
    print("ERROR: ANTHROPIC_API_KEY secret is not set in GitHub Secrets!")
    print("Go to: repo Settings > Secrets and variables > Actions > New secret")
    print("Name: ANTHROPIC_API_KEY")
    exit(1)

MODEL = "claude-sonnet-4-20250514"
today = datetime.datetime.now().strftime("%A, %B %d, %Y")
print(f"WorldPulse Auto-Publisher starting for {today}")

SYSTEM = f"""You are the chief editor of WorldPulse, a world-class global news blog.
Today is {today}.

Write today's complete blog edition as a single JSON object.
Return ONLY raw JSON. No markdown. No backticks. No explanation. Just the JSON.

Use this exact structure:
{{
  "date": "{today}",
  "breaking_ticker": [
    "First breaking headline today",
    "Second breaking headline today",
    "Third breaking headline today",
    "Fourth breaking headline today",
    "Fifth breaking headline today"
  ],
  "markets": [
    {{"label": "S&P 500", "value": "5,241", "change": "▲ +0.4%", "dir": "up"}},
    {{"label": "Crude Oil", "value": "$81.2", "change": "▼ -0.8%", "dir": "down"}},
    {{"label": "Gold", "value": "$2,398", "change": "▲ +0.3%", "dir": "up"}},
    {{"label": "EUR/USD", "value": "1.071", "change": "▼ -0.1%", "dir": "down"}},
    {{"label": "10Y Treasury", "value": "4.68%", "change": "▲ +2bps", "dir": "up"}}
  ],
  "articles": [
    {{
      "id": "story-one",
      "cat": "Geopolitics",
      "tag": "Breaking",
      "headline": "Full compelling headline for story one",
      "deck": "Two to three sentence summary of the story that makes readers want to click and read more immediately.",
      "author": "Marcus Osei",
      "role": "Senior Diplomatic Correspondent",
      "time": "Today, 8:30 AM",
      "read_time": "6 min read",
      "hero_icon": "🌍",
      "body_html": "<p>Opening paragraph with full context and background of the story. At least 100 words here establishing what happened.</p><h3>What Happened</h3><p>Second paragraph explaining the key events in detail with specific facts and figures. Name real people, places, organisations involved.</p><blockquote>Real direct quote from a key figure involved in this story.<cite>Name, Title, Organisation</cite></blockquote><p>Third paragraph with analysis of what this means and why it matters globally.</p><div class=\\"fact-box\\"><div class=\\"fact-box-title\\">Key Facts</div><ul><li><span>Key detail one</span><strong>Value one</strong></li><li><span>Key detail two</span><strong>Value two</strong></li><li><span>Key detail three</span><strong>Value three</strong></li><li><span>Key detail four</span><strong>Value four</strong></li></ul></div><h3>What Happens Next</h3><p>Fourth paragraph explaining the implications, what analysts say, and what to watch for in the coming days.</p><p>Fifth paragraph with broader global context and conclusion.</p>"
    }},
    {{
      "id": "story-two",
      "cat": "Economy",
      "tag": "Markets",
      "headline": "Full compelling headline for the biggest economic story today",
      "deck": "Two to three sentence summary of the economic story.",
      "author": "Amina Diallo",
      "role": "Economics Correspondent",
      "time": "Today, 7:00 AM",
      "read_time": "5 min read",
      "hero_icon": "📈",
      "body_html": "<p>Full economic story here minimum 400 words. Include real data, figures, expert quotes, market reactions, and analysis of what this means for ordinary people and businesses.</p><h3>Market Impact</h3><p>Detailed analysis of market reactions and economic implications with specific numbers and percentages.</p><blockquote>Quote from economist or official.<cite>Name, Title</cite></blockquote><p>Further analysis and conclusion.</p>"
    }},
    {{
      "id": "story-three",
      "cat": "Science",
      "tag": "Discovery",
      "headline": "Full compelling headline for a major science or health story today",
      "deck": "Two to three sentence summary of the science story.",
      "author": "Dr. Priya Menon",
      "role": "Science Correspondent",
      "time": "Today, 9:00 AM",
      "read_time": "5 min read",
      "hero_icon": "🔬",
      "body_html": "<p>Full science story minimum 400 words. Explain the discovery or development in accessible language, its significance, who conducted the research, and what it means for the future.</p><h3>Why This Matters</h3><p>Detailed explanation of significance and practical implications.</p><p>Further context and conclusion.</p>"
    }},
    {{
      "id": "story-four",
      "cat": "Europe",
      "tag": "Conflict",
      "headline": "Full compelling headline for a conflict or crisis story today",
      "deck": "Two to three sentence summary.",
      "author": "Anna Kovalenko",
      "role": "Eastern Europe Correspondent",
      "time": "Today, 6:00 AM",
      "read_time": "4 min read",
      "hero_icon": "⚡",
      "body_html": "<p>Full conflict or crisis story minimum 400 words with real facts, casualty figures if applicable, official statements, and humanitarian context.</p><h3>Background</h3><p>Historical context and analysis.</p><p>Current situation and what to expect next.</p>"
    }},
    {{
      "id": "story-five",
      "cat": "Asia",
      "tag": "Diplomacy",
      "headline": "Full compelling headline for a major Asia story today",
      "deck": "Two to three sentence summary.",
      "author": "Kenji Tanaka",
      "role": "Asia Pacific Correspondent",
      "time": "Today, 5:00 AM",
      "read_time": "4 min read",
      "hero_icon": "🌏",
      "body_html": "<p>Full Asia story minimum 400 words covering the key developments, regional implications, and international reactions.</p><p>Analysis and conclusion.</p>"
    }}
  ],
  "claude_ai_article": {{
    "id": "claude-ai-today",
    "cat": "Claude AI",
    "tag": "AI Column",
    "headline": "What Anthropic and Claude Are Building This Week — And What It Means For You",
    "deck": "Our weekly deep dive into the latest from Anthropic, what Claude can now do, and an honest look at both the extraordinary benefits and the genuine risks of AI becoming more powerful.",
    "author": "James Park",
    "role": "AI & Technology Correspondent",
    "time": "Today, 6:00 AM",
    "read_time": "8 min read",
    "hero_icon": "🧠",
    "body_html": "<p>Opening paragraph about the most important AI development this week. Be specific about what Anthropic released, announced, or what Claude can now do that it could not do before.</p><h3>What Anthropic Built This Week</h3><p>Detailed explanation of the specific capability, product, or research development. Explain it in plain English so anyone can understand it.</p><blockquote>Real or representative quote from Anthropic or AI researcher about this development.<cite>Name, Title, Anthropic or Organisation</cite></blockquote><h3>The Benefits For Humanity</h3><p>Specific, concrete ways this helps real people. Examples: doctors using AI to diagnose diseases faster, scientists using Claude to analyse climate data, students in developing countries getting access to world-class tutoring. Be specific and optimistic but honest.</p><h3>The Risks We Cannot Ignore</h3><p>Honest, balanced analysis of the genuine risks. Job displacement, concentration of power, AI systems making mistakes in high-stakes situations, privacy concerns, the risk of more capable systems being misused. Do not minimise these.</p><div class=\\"fact-box\\"><div class=\\"fact-box-title\\">Claude AI This Week</div><ul><li><span>Latest model</span><strong>Claude Opus 4.7</strong></li><li><span>Anthropic valuation</span><strong>$380 billion</strong></li><li><span>Key new capability</span><strong>Describe it here</strong></li><li><span>Available on</span><strong>Claude.ai, API, Bedrock, Vertex</strong></li></ul></div><h3>The Bottom Line</h3><p>Your honest assessment as a journalist covering AI. What does this week mean in the bigger picture of where AI is heading? What should ordinary people pay attention to? End with something that makes the reader think.</p>"
  }},
  "live_updates": [
    {{"tag": "war", "tag_label": "Conflict", "text": "<strong>Conflict update:</strong> Write a real live update about a conflict or military situation happening today."}},
    {{"tag": "diplo", "tag_label": "Diplomacy", "text": "<strong>Diplomacy:</strong> Write a real live update about diplomatic talks or international negotiations happening today."}},
    {{"tag": "econ", "tag_label": "Markets", "text": "<strong>Markets:</strong> Write a real live update about a market movement or economic development today."}},
    {{"tag": "ai", "tag_label": "Tech", "text": "<strong>Technology:</strong> Write a real live update about a technology or AI development today."}},
    {{"tag": "sci", "tag_label": "Science", "text": "<strong>Science:</strong> Write a real live update about a science or health development today."}}
  ]
}}

CRITICAL: Replace ALL placeholder text with REAL content about what is actually happening on {today}.
Every article body_html must be at least 400 words.
Return ONLY the JSON. Nothing before it. Nothing after it."""

USER = f"Today is {today}. Write the complete WorldPulse blog edition now. Cover the most important real world events happening today. Return only the JSON."

print("Calling Claude API...")
payload = json.dumps({
    "model": MODEL,
    "max_tokens": 8000,
    "system": SYSTEM,
    "messages": [{"role": "user", "content": USER}]
}).encode()

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
    with urllib.request.urlopen(req, timeout=120) as r:
        result = json.loads(r.read())
        raw = result["content"][0]["text"].strip()
        print(f"API response received ({len(raw)} chars)")
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print(f"API ERROR {e.code}: {body}")
    exit(1)
except Exception as e:
    print(f"REQUEST ERROR: {e}")
    exit(1)

# Clean JSON
if raw.startswith("```"):
    lines = raw.split("\n")
    raw = "\n".join(lines[1:])
if raw.endswith("```"):
    raw = raw.rsplit("```", 1)[0]
raw = raw.strip()

print("Parsing JSON...")
try:
    data = json.loads(raw)
except json.JSONDecodeError as e:
    print(f"JSON PARSE ERROR: {e}")
    print(f"First 500 chars of response: {raw[:500]}")
    exit(1)

print(f"Got {len(data.get('articles', []))} articles + Claude AI column")

# Build HTML
data_json = json.dumps(data, ensure_ascii=False)

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<meta name="description" content="WorldPulse — Global Intelligence Daily. Real world news published every day."/>
<meta property="og:title" content="WorldPulse — """ + data.get('date','Today') + """"/>
<meta property="og:description" content="WorldPulse: World-class global journalism published daily."/>
<title>WorldPulse — """ + data.get('date','Today') + """</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=Source+Serif+4:opsz,wght@8..60,300;8..60,400&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet"/>
<style>
:root{--ink:#0f0e0d;--paper:#f6f2ea;--cream:#faf7f2;--red:#c41e3a;--gold:#b8860b;--teal:#1a5f7a;--rule:#ddd6c8;--mist:#8a8680;--surf:#fff;--blue:#1a3a5c;--green:#1a4a2e;}
*{margin:0;padding:0;box-sizing:border-box;}
html{scroll-behavior:smooth;}
body{background:var(--paper);color:var(--ink);font-family:"Source Serif 4",Georgia,serif;font-size:17px;line-height:1.7;}
.ticker{background:var(--red);color:#fff;height:34px;display:flex;overflow:hidden;position:sticky;top:0;z-index:200;}
.ticker-tag{background:#000;color:#fff;padding:0 14px;font-family:"Space Mono",monospace;font-size:10px;letter-spacing:2px;display:flex;align-items:center;flex-shrink:0;text-transform:uppercase;}
.ticker-track{overflow:hidden;flex:1;display:flex;align-items:center;}
.ticker-inner{display:flex;white-space:nowrap;animation:tick 50s linear infinite;}
.ticker-inner span{font-size:11px;padding:0 36px;}
.ticker-inner span::after{content:"◆";margin-left:36px;opacity:.4;}
@keyframes tick{0%{transform:translateX(0)}100%{transform:translateX(-50%)}}
.masthead{background:var(--ink);padding:0 32px;border-bottom:3px solid var(--red);}
.mast-top{display:flex;align-items:center;justify-content:space-between;padding:18px 0 14px;border-bottom:1px solid rgba(255,255,255,.08);}
.mast-date{font-family:"Space Mono",monospace;font-size:10px;color:rgba(255,255,255,.45);letter-spacing:1px;text-transform:uppercase;}
.mast-logo{text-align:center;flex:1;}
.logo-name{font-family:"Playfair Display",serif;font-weight:900;font-size:clamp(2rem,5vw,3.8rem);color:#fff;letter-spacing:-1px;line-height:1;text-transform:uppercase;cursor:pointer;text-decoration:none;display:block;}
.logo-name span{color:var(--red);}
.logo-tag{font-family:"Space Mono",monospace;font-size:9px;color:rgba(255,255,255,.35);letter-spacing:4px;text-transform:uppercase;margin-top:3px;}
.btn-sub{background:var(--red);color:#fff;border:none;padding:7px 16px;font-family:"Space Mono",monospace;font-size:10px;letter-spacing:1px;text-transform:uppercase;cursor:pointer;}
.nav{display:flex;overflow-x:auto;scrollbar-width:none;}
.nav::-webkit-scrollbar{display:none;}
.nav-item{font-family:"Space Mono",monospace;font-size:10px;letter-spacing:1.5px;text-transform:uppercase;color:rgba(255,255,255,.5);padding:12px 18px;cursor:pointer;border-bottom:3px solid transparent;white-space:nowrap;text-decoration:none;transition:color .2s;}
.nav-item:hover,.nav-item.active{color:#fff;border-bottom-color:var(--red);}
.markets{display:flex;background:var(--cream);border-bottom:2px solid var(--rule);overflow-x:auto;padding:0 32px;}
.m-item{display:flex;align-items:center;gap:8px;padding:9px 20px 9px 0;border-right:1px solid var(--rule);white-space:nowrap;}
.m-item:last-child{border-right:none;}
.m-label{font-family:"Space Mono",monospace;font-size:9px;letter-spacing:1px;color:var(--mist);text-transform:uppercase;}
.m-val{font-family:"Space Mono",monospace;font-size:12px;font-weight:700;color:var(--ink);}
.m-chg{font-family:"Space Mono",monospace;font-size:10px;}
.up{color:#2a9e60;}.down{color:var(--red);}
.container{max-width:1220px;margin:0 auto;padding:0 32px;}
.sec-hd{display:flex;align-items:center;gap:14px;margin:40px 0 22px;}
.sec-title{font-family:"Playfair Display",serif;font-size:1.5rem;font-weight:900;text-transform:uppercase;color:var(--ink);}
.sec-rule{flex:1;height:2px;background:var(--rule);}
.sec-rule.red{background:var(--red);}
.hero-grid{display:grid;grid-template-columns:1.55fr 1fr;gap:2px;background:var(--rule);border:2px solid var(--rule);margin-top:32px;}
.hero-lead{background:var(--surf);padding:28px 32px;position:relative;}
.hero-lead::before{content:"";position:absolute;top:0;left:0;right:0;height:4px;background:var(--red);}
.hero-img{width:100%;height:260px;display:flex;align-items:center;justify-content:center;font-size:80px;margin-bottom:20px;cursor:pointer;background:linear-gradient(160deg,#0f1520,#1a3a58);}
.kicker{font-family:"Space Mono",monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase;color:var(--red);border-top:2px solid var(--red);padding-top:5px;display:inline-block;margin-bottom:10px;}
.kicker.teal{color:var(--teal);border-top-color:var(--teal);}
.kicker.gold{color:var(--gold);border-top-color:var(--gold);}
h1.hero-hl{font-family:"Playfair Display",serif;font-weight:900;font-size:clamp(1.6rem,2.6vw,2.3rem);line-height:1.15;color:var(--ink);margin-bottom:14px;cursor:pointer;}
h1.hero-hl:hover{color:var(--red);}
.deck{font-size:15px;color:#444;line-height:1.7;font-weight:300;margin-bottom:14px;}
.byline{font-family:"Space Mono",monospace;font-size:9px;color:var(--mist);letter-spacing:.8px;text-transform:uppercase;padding-top:12px;border-top:1px solid var(--rule);}
.byline strong{color:var(--ink);}
.read-btn{font-family:"Space Mono",monospace;font-size:10px;letter-spacing:1px;text-transform:uppercase;color:var(--red);cursor:pointer;display:inline-flex;align-items:center;gap:5px;margin-top:10px;text-decoration:none;}
.read-btn:hover{text-decoration:underline;}
.hero-side{background:var(--surf);padding:22px 26px;}
.hero-side+.hero-side{border-top:2px solid var(--rule);}
.side-img{width:100%;height:110px;margin-bottom:12px;display:flex;align-items:center;justify-content:center;font-size:38px;cursor:pointer;background:linear-gradient(160deg,#0f1520,#1a2a38);}
.hl2{font-family:"Playfair Display",serif;font-weight:700;font-size:1.05rem;line-height:1.3;color:var(--ink);cursor:pointer;margin-bottom:6px;}
.hl2:hover{color:var(--red);}
.deck2{font-size:13px;color:#555;line-height:1.6;font-weight:300;}
.card-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:2px;background:var(--rule);border:2px solid var(--rule);}
.card{background:var(--surf);padding:22px;cursor:pointer;transition:background .15s;}
.card:hover{background:#fffef9;}
.card-img{width:100%;height:140px;display:flex;align-items:center;justify-content:center;font-size:40px;margin-bottom:14px;background:linear-gradient(160deg,#0f1520,#1a2a38);}
.hl3{font-family:"Playfair Display",serif;font-weight:700;font-size:.98rem;line-height:1.3;color:var(--ink);margin-bottom:6px;}
.hl3:hover{color:var(--red);}
.deck3{font-size:12px;color:#555;line-height:1.6;font-weight:300;}
.dark-feat{background:var(--ink);padding:38px 44px;display:grid;grid-template-columns:1.3fr 1fr;gap:40px;align-items:center;cursor:pointer;margin:2px 0;}
.df-kicker{font-family:"Space Mono",monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase;color:rgba(232,160,160,.8);border-top:2px solid var(--red);padding-top:5px;display:inline-block;margin-bottom:12px;}
.df-hl{font-family:"Playfair Display",serif;font-weight:900;font-size:clamp(1.4rem,2.2vw,2rem);line-height:1.2;color:#fff;margin-bottom:12px;}
.df-deck{font-size:14px;color:rgba(255,255,255,.6);line-height:1.7;}
.df-read{font-family:"Space Mono",monospace;font-size:10px;color:rgba(232,160,160,.8);display:inline-block;margin-top:12px;text-decoration:none;}
.df-vis{font-size:100px;opacity:.14;text-align:center;}
.live-sec{background:var(--ink);padding:34px 0;margin:40px 0;}
.live-badge{display:inline-flex;align-items:center;gap:7px;background:var(--red);color:#fff;font-family:"Space Mono",monospace;font-size:10px;letter-spacing:2px;padding:5px 12px;text-transform:uppercase;margin-bottom:18px;}
.live-dot{width:7px;height:7px;background:#fff;border-radius:50%;animation:blink 1.4s ease infinite;}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.3}}
.live-title{font-family:"Playfair Display",serif;font-size:1.4rem;font-weight:900;color:#fff;margin-bottom:22px;}
.u-item{display:grid;grid-template-columns:90px 1fr;gap:16px;padding:14px 0;border-bottom:1px solid rgba(255,255,255,.07);}
.u-time{font-family:"Space Mono",monospace;font-size:11px;color:var(--red);}
.u-text{font-size:13px;color:rgba(255,255,255,.78);line-height:1.6;}
.u-text strong{color:#fff;}
.utag{display:inline-block;font-family:"Space Mono",monospace;font-size:8px;letter-spacing:1px;padding:2px 7px;margin-right:6px;text-transform:uppercase;border:1px solid;}
.utag.war{border-color:#ff7070;color:#ff7070;}
.utag.econ{border-color:#60c878;color:#60c878;}
.utag.ai{border-color:#a090f0;color:#a090f0;}
.utag.diplo{border-color:#f0c040;color:#f0c040;}
.utag.sci{border-color:#60aaf0;color:#60aaf0;}
.bot-grid{display:grid;grid-template-columns:2fr 300px;gap:2px;background:var(--rule);border:2px solid var(--rule);margin-bottom:40px;}
.most-read{background:var(--surf);padding:26px;}
.mr-item{display:grid;grid-template-columns:32px 1fr;gap:12px;padding:13px 0;border-bottom:1px solid var(--rule);curso
