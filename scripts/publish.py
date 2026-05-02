import os
import json
import urllib.request
import urllib.error
import datetime

API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
if not API_KEY:
    print("FATAL: ANTHROPIC_API_KEY secret is missing")
    raise SystemExit(1)

print("API key found: ..."+API_KEY[-6:])
MODEL = "claude-haiku-4-5-20251001"
today = datetime.datetime.now().strftime("%A, %B %d, %Y")
print("Generating blog for: "+today)

SYSTEM = (
    "You are the editor of WorldPulse, a global news blog. Today is "+today+".\n"
    "Return a single valid JSON object. No markdown. No backticks. Just raw JSON.\n"
    "Use this structure:\n"
    "{\n"
    '  "date": "'+today+'",\n'
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
    '      "body_html": "<p>Write full article minimum 400 words about the biggest geopolitical story happening today '+today+'. Include real facts, figures, official quotes, context and analysis.</p><h3>Background</h3><p>Historical context and why this matters globally.</p><h3>What Happens Next</h3><p>Analysis and outlook.</p>"\n'
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
    "CRITICAL: Replace ALL placeholder text with REAL content about "+today+"\n"
    "Return ONLY the JSON. Nothing before it. Nothing after it."
)

USER = "Today is "+today+". Generate the complete WorldPulse blog. Return only JSON."

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
        print("API response: "+str(len(raw))+" chars")
except urllib.error.HTTPError as e:
    print("API HTTP ERROR "+str(e.code)+": "+e.read().decode("utf-8"))
    raise SystemExit(1)
except Exception as e:
    print("API ERROR: "+str(e))
    raise SystemExit(1)

print("Parsing JSON...")
clean = raw
if clean.startswith("```"):
    clean = "\n".join(clean.split("\n")[1:])
if clean.endswith("```"):
    clean = clean.rsplit("```",1)[0]
clean = clean.strip()

try:
    data = json.loads(clean)
except json.JSONDecodeError as e:
    print("JSON ERROR: "+str(e))
    print("Response start: "+clean[:300])
    raise SystemExit(1)

print("Got "+str(len(data.get("articles",[])))+" articles")

print("Building HTML...")
dj = json.dumps(data, ensure_ascii=False)
date_str = data.get("date", today)

html_parts = []
html_parts.append('<!DOCTYPE html>')
html_parts.append('<html lang="en">')
html_parts.append('<head>')
html_parts.append('<meta charset="UTF-8"/>')
html_parts.append('<meta name="viewport" content="width=device-width,initial-scale=1.0"/>')
html_parts.append('<meta name="description" content="WorldPulse - Global Intelligence Daily"/>')
html_parts.append('<title>WorldPulse - '+date_str+'</title>')
html_parts.append('<link rel="preconnect" href="https://fonts.googleapis.com"/>')
html_parts.append('<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=Source+Serif+4:opsz,wght@8..60,300;8..60,400&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet"/>')
html_parts.append('<style>')
html_parts.append(':root{--ink:#0f0e0d;--paper:#f6f2ea;--cream:#faf7f2;--red:#c41e3a;--gold:#b8860b;--teal:#1a5f7a;--rule:#ddd6c8;--mist:#8a8680;--surf:#fff;--blue:#1a3a5c;}')
html_parts.append('*{margin:0;padding:0;box-sizing:border-box;}')
html_parts.append('html{scroll-behavior:smooth;}')
html_parts.append('body{background:var(--paper);color:var(--ink);font-family:"Source Serif 4",Georgia,serif;font-size:17px;line-height:1.7;}')
html_parts.append('.ticker{background:var(--red);color:#fff;height:34px;display:flex;overflow:hidden;position:sticky;top:0;z-index:200;}')
html_parts.append('.ticker-tag{background:#000;color:#fff;padding:0 14px;font-family:"Space Mono",monospace;font-size:10px;letter-spacing:2px;display:flex;align-items:center;flex-shrink:0;text-transform:uppercase;}')
html_parts.append('.ticker-track{overflow:hidden;flex:1;display:flex;align-items:center;}')
html_parts.append('.ticker-inner{display:flex;white-space:nowrap;animation:tick 50s linear infinite;}')
html_parts.append('.ticker-inner span{font-size:11px;padding:0 36px;}')
html_parts.append('.ticker-inner span::after{content:"◆";margin-left:36px;opacity:.4;}')
html_parts.append('@keyframes tick{0%{transform:translateX(0)}100%{transform:translateX(-50%)}}')
html_parts.append('.masthead{background:var(--ink);padding:0 24px;border-bottom:3px solid var(--red);}')
html_parts.append('.mast-top{display:flex;align-items:center;justify-content:space-between;padding:16px 0 12px;border-bottom:1px solid rgba(255,255,255,.08);}')
html_parts.append('.mast-date{font-family:"Space Mono",monospace;font-size:9px;color:rgba(255,255,255,.4);letter-spacing:1px;text-transform:uppercase;}')
html_parts.append('.mast-logo{text-align:center;flex:1;}')
html_parts.append('.logo-name{font-family:"Playfair Display",serif;font-weight:900;font-size:clamp(1.8rem,5vw,3.5rem);color:#fff;letter-spacing:-1px;line-height:1;text-transform:uppercase;cursor:pointer;text-decoration:none;display:block;}')
html_parts.append('.logo-name span{color:var(--red);}')
html_parts.append('.logo-tag{font-family:"Space Mono",monospace;font-size:8px;color:rgba(255,255,255,.3);letter-spacing:4px;text-transform:uppercase;margin-top:3px;}')
html_parts.append('.btn-sub{background:var(--red);color:#fff;border:none;padding:6px 14px;font-family:"Space Mono",monospace;font-size:9px;letter-spacing:1px;text-transform:uppercase;cursor:pointer;}')
html_parts.append('.nav{display:flex;overflow-x:auto;scrollbar-width:none;}')
html_parts.append('.nav::-webkit-scrollbar{display:none;}')
html_parts.append('.nav-item{font-family:"Space Mono",monospace;font-size:9px;letter-spacing:1.5px;text-transform:uppercase;color:rgba(255,255,255,.5);padding:11px 16px;cursor:pointer;border-bottom:3px solid transparent;white-space:nowrap;text-decoration:none;transition:color .2s;}')
html_parts.append('.nav-item:hover,.nav-item.active{color:#fff;border-bottom-color:var(--red);}')
html_parts.append('.markets{display:flex;background:var(--cream);border-bottom:2px solid var(--rule);overflow-x:auto;padding:0 24px;}')
html_parts.append('.m-item{display:flex;align-items:center;gap:7px;padding:8px 18px 8px 0;border-right:1px solid var(--rule);white-space:nowrap;}')
html_parts.append('.m-item:last-child{border-right:none;}')
html_parts.append('.m-label{font-family:"Space Mono",monospace;font-size:8px;letter-spacing:1px;color:var(--mist);text-transform:uppercase;}')
html_parts.append('.m-val{font-family:"Space Mono",monospace;font-size:11px;font-weight:700;color:var(--ink);}')
html_parts.append('.m-chg{font-family:"Space Mono",monospace;font-size:9px;}')
html_parts.append('.up{color:#2a9e60;}.down{color:var(--red);}')
html_parts.append('.container{max-width:1200px;margin:0 auto;padding:0 24px;}')
html_parts.append('.sec-hd{display:flex;align-items:center;gap:12px;margin:36px 0 20px;}')
html_parts.append('.sec-title{font-family:"Playfair Display",serif;font-size:1.4rem;font-weight:900;text-transform:uppercase;color:var(--ink);}')
html_parts.append('.sec-rule{flex:1;height:2px;background:var(--rule);}')
html_parts.append('.sec-rule.red{background:var(--red);}')
html_parts.append('.hero-grid{display:grid;grid-template-columns:1.5fr 1fr;gap:2px;background:var(--rule);border:2px solid var(--rule);margin-top:28px;}')
html_parts.append('.hero-lead{background:var(--surf);padding:24px 28px;position:relative;}')
html_parts.append('.hero-lead::before{content:"";position:absolute;top:0;left:0;right:0;height:4px;background:var(--red);}')
html_parts.append('.hero-img{width:100%;height:240px;display:flex;align-items:center;justify-content:center;font-size:70px;margin-bottom:18px;cursor:pointer;background:linear-gradient(160deg,#0f1520,#1a3a58);}')
html_parts.append('.kicker{font-family:"Space Mono",monospace;font-size:8px;letter-spacing:2px;text-transform:uppercase;color:var(--red);border-top:2px solid var(--red);padding-top:4px;display:inline-block;margin-bottom:9px;}')
html_parts.append('.kicker.teal{color:var(--teal);border-top-color:var(--teal);}')
html_parts.append('.kicker.gold{color:var(--gold);border-top-color:var(--gold);}')
html_parts.append('h1.hero-hl{font-family:"Playfair Display",serif;font-weight:900;font-size:clamp(1.5rem,2.4vw,2.1rem);line-height:1.15;color:var(--ink);margin-bottom:12px;cursor:pointer;}')
html_parts.append('h1.hero-hl:hover{color:var(--red);}')
html_parts.append('.deck{font-size:14px;color:#444;line-height:1.7;font-weight:300;margin-bottom:12px;}')
html_parts.append('.byline{font-family:"Space Mono",monospace;font-size:8px;color:var(--mist);letter-spacing:.8px;text-transform:uppercase;padding-top:11px;border-top:1px solid var(--rule);}')
html_parts.append('.byline strong{color:var(--ink);}')
html_parts.append('.read-btn{font-family:"Space Mono",monospace;font-size:9px;letter-spacing:1px;text-transform:uppercase;color:var(--red);cursor:pointer;display:inline-flex;align-items:center;gap:4px;margin-top:9px;text-decoration:none;}')
html_parts.append('.read-btn:hover{text-decoration:underline;}')
html_parts.append('.hero-side{background:var(--surf);padding:20px 24px;}')
html_parts.append('.hero-side+.hero-side{border-top:2px solid var(--rule);}')
html_parts.append('.side-img{width:100%;height:100px;margin-bottom:11px;display:flex;align-items:center;justify-content:center;font-size:34px;cursor:pointer;background:linear-gradient(160deg,#0f1520,#1a2a38);}')
html_parts.append('.hl2{font-family:"Playfair Display",serif;font-weight:700;font-size:1rem;line-height:1.3;color:var(--ink);cursor:pointer;margin-bottom:5px;}')
html_parts.append('.hl2:hover{color:var(--red);}')
html_parts.append('.deck2{font-size:12px;color:#555;line-height:1.6;font-weight:300;}')
html_parts.append('.card-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:2px;background:var(--rule);border:2px solid var(--rule);}')
html_parts.append('.card{background:var(--surf);padding:20px;cursor:pointer;transition:background .15s;}')
html_parts.append('.card:hover{background:#fffef9;}')
html_parts.append('.card-img{width:100%;height:130px;display:flex;align-items:center;justify-content:center;font-size:36px;margin-bottom:12px;background:linear-gradient(160deg,#0f1520,#1a2a38);}')
html_parts.append('.hl3{font-family:"Playfair Display",serif;font-weight:700;font-size:.95rem;line-height:1.3;color:var(--ink);margin-bottom:5px;}')
html_parts.append('.hl3:hover{color:var(--red);}')
html_parts.append('.deck3{font-size:11px;color:#555;line-height:1.6;font-weight:300;}')
html_parts.append('.dark-feat{background:var(--ink);padding:34px 40px;display:grid;grid-template-columns:1.3fr 1fr;gap:36px;align-items:center;cursor:pointer;margin:2px 0;}')
html_parts.append('.df-kicker{font-family:"Space Mono",monospace;font-size:8px;letter-spacing:2px;text-transform:uppercase;color:rgba(232,160,160,.8);border-top:2px solid var(--red);padding-top:4px;display:inline-block;margin-bottom:10px;}')
html_parts.append('.df-hl{font-family:"Playfair Display",serif;font-weight:900;font-size:clamp(1.3rem,2vw,1.8rem);line-height:1.2;color:#fff;margin-bottom:10px;}')
html_parts.append('.df-deck{font-size:13px;color:rgba(255,255,255,.6);line-height:1.7;}')
html_parts.append('.df-read{font-family:"Space Mono",monospace;font-size:9px;color:rgba(232,160,160,.8);display:inline-block;margin-top:10px;text-decoration:none;}')
html_parts.append('.df-vis{font-size:90px;opacity:.14;text-align:center;}')
html_parts.append('.live-sec{background:var(--ink);padding:30px 0;margin:36px 0;}')
html_parts.append('.live-badge{display:inline-flex;align-items:center;gap:6px;background:var(--red);color:#fff;font-family:"Space Mono",monospace;font-size:9px;letter-spacing:2px;padding:4px 11px;text-transform:uppercase;margin-bottom:16px;}')
html_parts.append('.live-dot{width:6px;height:6px;background:#fff;border-radius:50%;animation:blink 1.4s ease infinite;}')
html_parts.append('@keyframes blink{0%,100%{opacity:1}50%{opacity:.3}}')
html_parts.append('.live-title{font-family:"Playfair Display",serif;font-size:1.3rem;font-weight:900;color:#fff;margin-bottom:18px;}')
html_parts.append('.u-item{display:grid;grid-template-columns:80px 1fr;gap:14px;padding:12px 0;border-bottom:1px solid rgba(255,255,255,.07);}')
html_parts.append('.u-time{font-family:"Space Mono",monospace;font-size:10px;color:var(--red);}')
html_parts.append('.u-text{font-size:12px;color:rgba(255,255,255,.78);line-height:1.6;}')
html_parts.append('.u-text strong{color:#fff;}')
html_parts.append('.utag{display:inline-block;font-family:"Space Mono",monospace;font-size:7px;letter-spacing:1px;padding:2px 6px;margin-right:5px;text-transform:uppercase;border:1px solid;}')
html_parts.append('.utag.war{border-color:#ff7070;color:#ff7070;}')
html_parts.append('.utag.econ{border-color:#60c878;color:#60c878;}')
html_parts.append('.utag.ai{border-color:#a090f0;color:#a090f0;}')
html_parts.append('.utag.diplo{border-color:#f0c040;color:#f0c040;}')
html_parts.append('.utag.sci{border-color:#60aaf0;color:#60aaf0;}')
html_parts.append('.bot-grid{display:grid;grid-template-columns:2fr 280px;gap:2px;background:var(--rule);border:2px solid var(--rule);margin-bottom:36px;}')
html_parts.append('.most-read{background:var(--surf);padding:22px;}')
html_parts.append('.mr-item{display:grid;grid-template-columns:28px 1fr;gap:11px;padding:11px 0;border-bottom:1px solid var(--rule);cursor:pointer;}')
html_parts.append('.mr-item:last-child{border-bottom:none;}')
html_parts.append('.mr-item:hover .mr-title{color:var(--red);}')
html_parts.append('.mr-num{font-family:"Playfair Display",serif;font-size:1.5rem;font-weight:900;color:var(--rule);line-height:1;}')
html_parts.append('.mr-title{font-family:"Playfair Display",serif;font-size:.85rem;font-weight:700;color:var(--ink);line-height:1.3;margin-bottom:2px;}')
html_parts.append('.mr-meta{font-size:10px;color:var(--mist);}')
html_parts.append('.sidebar{background:var(--surf);padding:18px;}')
html_parts.append('.sb-title{font-family:"Space Mono",monospace;font-size:8px;letter-spacing:2px;text-transform:uppercase;color:var(--mist);margin-bottom:11px;padding-bottom:5px;border-bottom:2px solid var(--rule);}')
html_parts.append('.nl-w p{font-size:11px;color:#555;margin-bottom:9px;line-height:1.5;}')
html_parts.append('.nl-w input{width:100%;border:1px solid var(--rule);padding:7px 9px;font-size:12px;background:var(--cream);margin-bottom:6px;outline:none;}')
html_parts.append('.nl-w button{width:100%;background:var(--ink);color:#fff;border:none;padding:8px;font-family:"Space Mono",monospace;font-size:9px;letter-spacing:2px;cursor:pointer;}')
html_parts.append('footer{background:var(--ink);color:rgba(255,255,255,.4);padding:30px 24px;margin-top:50px;}')
html_parts.append('.ft-inner{max-width:1200px;margin:0 auto;display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:30px;padding-bottom:22px;border-bottom:1px solid rgba(255,255,255,.08);}')
html_parts.append('.ft-logo{font-family:"Playfair Display",serif;font-weight:900;font-size:1.5rem;color:#fff;text-decoration:none;display:block;cursor:pointer;}')
html_parts.append('.ft-logo span{color:var(--red);}')
html_parts.append('.ft-brand p{margin-top:8px;font-size:11px;line-height:1.7;}')
html_parts.append('.ft-col h4{font-family:"Space Mono",monospace;font-size:8px;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,.6);margin-bottom:10px;}')
html_parts.append('.ft-col a{display:block;font-size:11px;color:rgba(255,255,255,.35);text-decoration:none;margin-bottom:5px;cursor:pointer;}')
html_parts.append('.ft-col a:hover{color:#fff;}')
html_parts.append('.ft-bot{max-width:1200px;margin:18px auto 0;display:flex;justify-content:space-between;font-family:"Space Mono",monospace;font-size:8px;}')
html_parts.append('.art-page{max-width:740px;margin:0 auto;padding:40px 24px 70px;}')
html_parts.append('.art-bc{font-family:"Space Mono",monospace;font-size:8px;letter-spacing:1px;text-transform:uppercase;color:var(--mist);margin-bottom:16px;}')
html_parts.append('.art-bc a{color:var(--red);text-decoration:none;cursor:pointer;}')
html_parts.append('.art-hl{font-family:"Playfair Display",serif;font-weight:900;font-size:clamp(1.7rem,4vw,2.6rem);line-height:1.13;color:var(--ink);margin-bottom:14px;}')
html_parts.append('.art-deck{font-size:1.05rem;font-weight:300;color:#444;line-height:1.65;margin-bottom:18px;border-left:4px solid var(--red);padding-left:14px;font-style:italic;}')
html_parts.append('.art-by{display:flex;align-items:center;gap:10px;padding:11px 0;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);margin-bottom:28px;flex-wrap:wrap;}')
html_parts.append('.art-av{width:34px;height:34px;border-radius:50%;background:var(--blue);display:flex;align-items:center;justify-content:center;color:#fff;font-family:"Playfair Display",serif;font-weight:700;font-size:13px;flex-shrink:0;}')
html_parts.append('.art-by-name{font-family:"Space Mono",monospace;font-size:9px;font-weight:700;color:var(--ink);letter-spacing:.5px;text-transform:uppercase;}')
html_parts.append('.art-by-meta{font-family:"Space Mono",monospace;font-size:8px;color:var(--mist);}')
html_parts.append('.art-hero{width:100%;height:280px;margin-bottom:22px;display:flex;align-items:center;justify-content:center;font-size:70px;background:linear-gradient(160deg,#0f1520,#1a3a58);border-radius:2px;}')
html_parts.append('.art-body p{margin-bottom:18px;font-size:.98rem;line-height:1.85;color:#1a1a1a;}')
html_parts.append('.art-body h3{font-family:"Playfair Display",serif;font-size:1.28rem;font-weight:700;color:var(--ink);margin:32px 0 11px;padding-top:24px;border-top:2px solid var(--rule);}')
html_parts.append('.art-body blockquote{margin:28px 0;padding:18px 22px;background:var(--cream);border-left:5px solid var(--gold);font-style:italic;font-size:1.05rem;color:#333;line-height:1.7;}')
html_parts.append('.art-body blockquote cite{display:block;margin-top:8px;font-family:"Space Mono",monospace;font-size:8px;font-style:normal;color:var(--mist);letter-spacing:1px;text-transform:uppercase;}')
html_parts.append('.fact-box{background:var(--blue);color:#fff;padding:22px;margin:28px 0;}')
html_parts.append('.fact-box-title{font-family:"Space Mono",monospace;font-size:8px;letter-spacing:2px;text-transform:uppercase;color:var(--gold);margin-bottom:11px;}')
html_parts.append('.fact-box ul{list-style:none;}')
html_parts.append('.fact-box ul li{font-size:12px;padding:5px 0;border-bottom:1px solid rgba(255,255,255,.1);display:flex;justify-content:space-between;color:rgba(255,255,255,.82);}')
html_parts.append('.fact-box ul li:last-child{border-bottom:none;}')
html_parts.append('.fact-box ul li strong{color:#fff;font-family:"Space Mono",monospace;font-size:11px;}')
html_parts.append('.art-tags{margin-top:36px;padding-top:18px;border-top:2px solid var(--rule);display:flex;flex-wrap:wrap;gap:5px;}')
html_parts.append('.atag{font-family:"Space Mono",monospace;font-size:8px;letter-spacing:1px;text-transform:uppercase;border:1px solid var(--rule);padding:3px 9px;color:var(--mist);cursor:pointer;}')
html_parts.append('.art-nav{display:grid;grid-template-columns:1fr 1fr;gap:2px;background:var(--rule);border:2px solid var(--rule);margin-top:36px;}')
html_parts.append('.art-nav-item{background:var(--surf);padding:16px;cursor:pointer;}')
html_parts.append('.art-nav-item:hover{background:var(--cream);}')
html_parts.append('.art-nav-item.next{text-align:right;}')
html_parts.append('.art-nav-dir{font-family:"Space Mono",monospace;font-size:8px;letter-spacing:1px;text-transform:uppercase;color:var(--mist);margin-bottom:4px;}')
html_parts.append('.art-nav-hl{font-family:"Playfair Display",serif;font-weight:700;font-size:.88rem;color:var(--ink);line-height:1.3;}')
html_parts.append('.art-nav-item:hover .art-nav-hl{color:var(--red);}')
html_parts.append('.back-btn{font-family:"Space Mono",monospace;font-size:9px;letter-spacing:1px;text-transform:uppercase;color:var(--red);cursor:pointer;display:inline-flex;align-items:center;gap:4px;margin-top:22px;padding-top:22px;border-top:1px solid var(--rule);text-decoration:none;}')
html_parts.append('.cat-page{max-width:1050px;margin:0 auto;padding:32px 24px 70px;}')
html_parts.append('.cat-hd{text-align:center;padding:22px 0 26px;border-bottom:3px double var(--rule);margin-bottom:28px;}')
html_parts.append('.cat-name{font-family:"Playfair Display",serif;font-size:2rem;font-weight:900;color:var(--ink);}')
html_parts.append('.cat-desc{font-size:12px;color:var(--mist);margin-top:5px;}')
html_parts.append('.cat-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:2px;background:var(--rule);border:2px solid var(--rule);}')
html_parts.append('#app>*{animation:fi .3s ease;}')
html_parts.append('@keyframes fi{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:translateY(0)}}')
html_parts.append('@media(max-width:860px){')
html_parts.append('.container,.art-page,.cat-page{padding:0 14px;}')
html_parts.append('.masthead,.markets{padding-left:14px;padding-right:14px;}')
html_parts.append('.hero-grid,.bot-grid{grid-template-columns:1fr;}')
html_parts.append('.card-grid,.cat-grid{grid-template-columns:1fr 1fr;}')
html_parts.append('.dark-feat{grid-template-columns:1fr;}')
html_parts.append('.df-vis{display:none;}')
html_parts.append('.ft-inner{grid-template-columns:1fr 1fr;}')
html_parts.append('.sidebar{display:none;}')
html_parts.append('.art-nav{grid-template-columns:1fr;}')
html_parts.append('}')
html_parts.append('@media(max-width:500px){')
html_parts.append('.card-grid,.cat-grid{grid-template-columns:1fr;}')
html_parts.append('.ft-inner{grid-template-columns:1fr;}')
html_parts.append('}')
html_parts.append('</style>')
html_parts.append('</head>')
html_parts.append('<body>')
html_parts.append('<div id="app"></div>')
html_parts.append('<script>')
html_parts.append('var DATA='+dj+';')
html_parts.append('var S={page:"home",aid:null,cat:"All",nav:"All"};')
html_parts.append('var CATS=["All","Geopolitics","Middle East","Claude AI","Europe","Asia","Economy","Science","Opinion"];')
html_parts.append('function go(p,x){S.page=p;if(p==="article")S.aid=x;if(p==="category"){S.cat=x;S.nav=x;}if(p==="home")S.nav="All";window.scrollTo(0,0);draw();}')
html_parts.append('function all(){return DATA.articles.concat([DATA.claude_ai_article]);}')
html_parts.append('function getA(id){return all().find(function(a){return a.id===id;});}')
html_parts.append('function byCat(c){var a=all();return c==="All"?a:a.filter(function(x){return x.cat===c;});}')
html_parts.append('function ticker(){var t=DATA.breaking_ticker;var d=t.concat(t);return\'<div class="ticker"><div class="ticker-tag">Breaking</div><div class="ticker-track"><div class="ticker-inner">\'+d.map(function(x){return\'<span>\'+x+\'</span>\';}).join(\'\')+\'</div></div></div>\';}')
html_parts.append('function mast(){return\'<header class="masthead"><div class="mast-top"><div class="mast-date">\'+DATA.date+\'</div><div class="mast-logo"><a class="logo-name" onclick="go(\\\'home\\\')" href="#">WORLD<span>PULSE</span></a><div class="logo-tag">Global Intelligence Daily</div></div><div><button class="btn-sub">Subscribe</button></div></div><nav class="nav">\'+CATS.map(function(c){return\'<a class="nav-item\'+(S.nav===c?\' active\':\'\')+\'" onclick="go(\\\'category\\\',\\\'\'+c+\'\\\')" href="#">\'+c+\'</a>\';}).join(\'\')+\'</nav></header>\';}')
html_parts.append('function mkts(){return\'<div class="markets">\'+DATA.markets.map(function(m){return\'<div class="m-item"><span class="m-label">\'+m.label+\'</span><span class="m-val">\'+m.value+\'</span><span class="m-chg \'+m.dir+\'">\'+m.change+\'</span></div>\';}).join(\'\')+\'</div>\';}')
html_parts.append('function hero(){var a=all();var ld=a[0];var s1=a[1];var s2=DATA.claude_ai_article;return\'<div class="hero-grid"><div class="hero-lead"><div class="hero-img" onclick="go(\\\'article\\\',\\\'\'+ld.id+\'\\\')">\'+ld.hero_icon+\'</div><div class="kicker">\'+ld.tag+\'</div><h1 class="hero-hl" onclick="go(\\\'article\\\',\\\'\'+ld.id+\'\\\')">\'+ld.headline+\'</h1><div class="deck">\'+ld.deck+\'</div><a class="read-btn" onclick="go(\\\'article\\\',\\\'\'+ld.id+\'\\\')" href="#">Continue Reading</a><div class="byline"><strong>\'+ld.author+\'</strong> \'+ld.role+\' \'+ld.time+\'</div></div><div>\'+[s1,s2].map(function(a,i){var k=i===1?\'teal\':\'gold\';return\'<div class="hero-side"><div class="side-img" onclick="go(\\\'article\\\',\\\'\'+a.id+\'\\\')">\'+a.hero_icon+\'</div><div class="kicker \'+k+\'">\'+a.tag+\'</div><div class="hl2" onclick="go(\\\'article\\\',\\\'\'+a.id+\'\\\')">\'+a.headline+\'</div><div class="deck2">\'+a.deck.substring(0,150)+\'</div><a class="read-btn" onclick="go(\\\'article\\\',\\\'\'+a.id+\'\\\')" href="#" style="color:var(--\'+k+\')">Read More</a></div>\';}).join(\'\')+\'</div></div>\';}')
html_parts.append('function cards(){return\'<div class="card-grid">\'+DATA.articles.slice(2,5).map(function(a){return\'<div class="card" onclick="go(\\\'article\\\',\\\'\'+a.id+\'\\\')">\'+\'<div class="card-img">\'+a.hero_icon+\'</div>\'+\'<div class="kicker">\'+a.tag+\'</div>\'+\'<div class="hl3">\'+a.headline+\'</div>\'+\'<div class="deck3">\'+a.deck.substring(0,110)+\'</div>\'+\'<div class="byline" style="margin-top:8px"><strong>\'+a.author+\'</strong> \'+a.time+\'</div></div>\';}).join(\'\')+\'</div>\';}')
html_parts.append('function dark(){var a=DATA.claude_ai_article;return\'<div class="dark-feat" onclick="go(\\\'article\\\',\\\'\'+a.id+\'\\\')">\'+\'<div><div class="df-kicker">Claude AI Column</div><div class="df-hl">\'+a.headline+\'</div><div class="df-deck">\'+a.deck+\'</div><a class="df-read" href="#">Read Full Column</a></div>\'+\'<div class="df-vis">\'+a.hero_icon+\'</div></div>\';}')
html_parts.append('function live(){var now=new Date();function t(m){var x=new Date(now-m*60000);return(x.getHours()<10?"0":"")+x.getHours()+":"+(x.getMinutes()<10?"0":"")+x.getMinutes()+" GMT";}return\'<div class="live-sec"><div class="container"><div class="live-badge"><div class="live-dot"></div>Live Updates</div><div class="live-title">Global Situation Room\'+DATA.date+\'</div>\'+DATA.live_updates.map(function(u,i){return\'<div class="u-item"><div class="u-time">\'+t(i*22+8)+\'</div><div class="u-text"><span class="utag \'+u.tag+\'">\'+u.tag_label+\'</span>\'+u.text+\'</div></div>\';}).join(\'\')+\'</div></div>\';}')
html_parts.append('function bot(){var a=all();return\'<div class="bot-grid"><div class="most-read"><div class="sec-hd" style="margin:0 0 12px"><div class="sec-title" style="font-size:1rem">Most Read</div><div class="sec-rule"></div></div>\'+a.slice(0,5).map(function(x,i){return\'<div class="mr-item" onclick="go(\\\'article\\\',\\\'\'+x.id+\'\\\')">\'+\'<div class="mr-num">0\'+(i+1)+\'</div>\'+\'<div><div class="mr-title">\'+x.headline+\'</div><div class="mr-meta">\'+x.cat+\'</div></div></div>\';}).join(\'\')+\'</div><div class="sidebar"><div class="sb-title">Newsletter</div><div class="nl-w"><p>Daily news at 6 AM free.</p><input type="email" placeholder="your@email.com"/><button>Subscribe</button></div></div></div>\';}')
html_parts.append('function foot(){return\'<footer><div class="ft-inner"><div class="ft-brand"><a class="ft-logo" onclick="go(\\\'home\\\')" href="#">WORLD<span>PULSE</span></a><p>Independent global journalism. Published daily.</p></div><div class="ft-col"><h4>Sections</h4>\'+[\'Geopolitics\',\'Middle East\',\'Claude AI\',\'Economy\',\'Europe\'].map(function(c){return\'<a onclick="go(\\\'category\\\',\\\'\'+c+\'\\\')" href="#">\'+c+\'</a>\';}).join(\'\')+\'</div><div class="ft-col"><h4>Company</h4>\'+[\'About\',\'Contact\',\'Press\'].map(function(p){return\'<a href="#">\'+p+\'</a>\';}).join(\'\')+\'</div><div class="ft-col"><h4>Subscribe</h4>\'+[\'Daily Brief\',\'AI Column\',\'Podcast\'].map(function(p){return\'<a href="#">\'+p+\'</a>\';}).join(\'\')+\'</div></div><div class="ft-bot"><span>2026 WorldPulse</span><span>Privacy Terms</span></div></footer>\';}')
html_parts.append('function home(){return\'<div>\'+ticker()+mast()+mkts()+\'<div class="container">\'+hero()+\'<div class="sec-hd"><div class="sec-title">Todays Coverage</div><div class="sec-rule red"></div></div>\'+cards()+dark()+\'</div>\'+live()+\'<div class="container">\'+bot()+\'</div>\'+foot()+\'</div>\';}')
html_parts.append('function article(id){var a=getA(id);if(!a)return\'<div class="container" style="padding:50px 0"><h2>Not found</h2><a class="back-btn" onclick="go(\\\'home\\\')" href="#">Back</a></div>\';var ar=all();var i=ar.findIndex(function(x){return x.id===id;});var pv=ar[i-1];var nx=ar[i+1];return\'<div>\'+ticker()+mast()+\'<div class="art-page"><div class="art-bc"><a onclick="go(\\\'home\\\')" href="#">WorldPulse</a> \'+a.cat+\'</div><div class="kicker">\'+a.tag+\'</div><h1 class="art-hl">\'+a.headline+\'</h1><div class="art-deck">\'+a.deck+\'</div><div class="art-by"><div class="art-av">\'+a.author.charAt(0)+\'</div><div><div class="art-by-name">\'+a.author+\'</div><div class="art-by-meta">\'+a.role+\' \'+a.time+\' \'+a.read_time+\'</div></div></div><div class="art-hero">\'+a.hero_icon+\'</div><div class="art-body">\'+a.body_html+\'</div><div class="art-tags"><span class="atag">\'+a.cat+\'</span><span class="atag">WorldPulse</span></div><div class="art-nav">\'+(pv?\'<div class="art-nav-item" onclick="go(\\\'article\\\',\\\'\'+pv.id+\'\\\')">\'+\'<div class="art-nav-dir">Previous</div><div class="art-nav-hl">\'+pv.headline+\'</div></div>\':\'<div></div>\')+(nx?\'<div class="art-nav-item next" onclick="go(\\\'article\\\',\\\'\'+nx.id+\'\\\')">\'+\'<div class="art-nav-dir">Next</div><div class="art-nav-hl">\'+nx.headline+\'</div></div>\':\'<div></div>\')+\'</div><a class="back-btn" onclick="go(\\\'home\\\')" href="#">Back to WorldPulse</a></div>\'+foot()+\'</div>\';}')
html_parts.append('function catpage(c){var a=byCat(c);return\'<div>\'+ticker()+mast()+\'<div class="cat-page"><div class="cat-hd"><div class="cat-name">\'+(c==="All"?"All Stories":c)+\'</div><div class="cat-desc">\'+a.length+\' articles \'+DATA.date+\'</div></div><div class="cat-grid">\'+a.map(function(x){return\'<div class="card" onclick="go(\\\'article\\\',\\\'\'+x.id+\'\\\')">\'+\'<div class="card-img">\'+x.hero_icon+\'</div>\'+\'<div class="kicker">\'+x.tag+\'</div>\'+\'<div class="hl3">\'+x.headline+\'</div>\'+\'<div class="deck3">\'+x.deck.substring(0,120)+\'</div>\'+\'<div class="byline" style="margin-top:7px"><strong>\'+x.author+\'</strong> \'+x.time+\'</div></div>\';}).join(\'\')+\'</div><a class="back-btn" onclick="go(\\\'home\\\')" href="#">Back</a></div>\'+foot()+\'</div>\';}')
html_parts.append('function draw(){var r=document.getElementById(\'app\');if(S.page===\'home\')r.innerHTML=home();else if(S.page===\'article\')r.innerHTML=article(S.aid);else if(S.page===\'category\')r.innerHTML=catpage(S.cat);}')
html_parts.append('draw();')
html_parts.append('<\/script>')
html_parts.append('</body>')
html_parts.append('</html>')

final_html = '\n'.join(html_parts)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(final_html)

size = os.path.getsize('index.html')
print('SUCCESS: index.html written ('+str(size)+' bytes)')
print('Lead: '+data['articles'][0]['headline'][:70])
print('AI: '+data['claude_ai_article']['headline'][:70])
