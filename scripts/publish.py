import os
import json
import urllib.request
import urllib.error
import datetime

BLOG_TITLE = "WorldPulse"
BLOG_TAGLINE = "Global Intelligence Daily"
OUTPUT_FILE = "index.html"
API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
MODEL = "claude-sonnet-4-20250514"
MAX_TOKENS = 8000

SYSTEM_PROMPT = """You are the chief editor of WorldPulse, a world-class global news blog.
Today is: {today}

Produce a complete JSON blog edition. Return ONLY valid JSON, no markdown, no backticks.

Required JSON structure:
{{
  "date": "Wednesday, April 23, 2026",
  "breaking_ticker": ["headline 1", "headline 2", "headline 3", "headline 4", "headline 5"],
  "markets": [
    {{"label": "S&P 500", "value": "5,241", "change": "▲ +0.4%", "dir": "up"}},
    {{"label": "Crude Oil", "value": "$81.2", "change": "▼ -0.8%", "dir": "down"}},
    {{"label": "Gold", "value": "$2,398", "change": "▲ +0.3%", "dir": "up"}},
    {{"label": "EUR/USD", "value": "1.071", "change": "▼ -0.1%", "dir": "down"}},
    {{"label": "10Y Treasury", "value": "4.68%", "change": "▲ +2bps", "dir": "up"}}
  ],
  "articles": [
    {{
      "id": "unique-slug-here",
      "cat": "Geopolitics",
      "tag": "Breaking",
      "headline": "Full headline here",
      "deck": "2-3 sentence summary that makes reader want to read more",
      "author": "Author Name",
      "role": "Senior Correspondent",
      "time": "Today, 8:30 AM",
      "read_time": "6 min read",
      "hero_icon": "🌍",
      "body_html": "<p>Full article here minimum 500 words with real facts. Include h3 subheadings. Include blockquotes with real attributed quotes. Include a fact-box like this: <div class='fact-box'><div class='fact-box-title'>Key Facts</div><ul><li><span>Label</span><strong>Value</strong></li></ul></div></p>"
    }}
  ],
  "claude_ai_article": {{
    "id": "claude-ai-today",
    "cat": "Claude AI",
    "tag": "AI Column",
    "headline": "What Claude and Anthropic Are Doing This Week",
    "deck": "Weekly analysis of AI developments and what they mean for humanity",
    "author": "James Park",
    "role": "AI Correspondent",
    "time": "Today, 6:00 AM",
    "read_time": "8 min read",
    "hero_icon": "🧠",
    "body_html": "<p>Full Claude AI article 600+ words covering what Anthropic is building, benefits for humanity, risks and concerns. Include real recent AI news.</p>"
  }},
  "live_updates": [
    {{"tag": "war", "tag_label": "Conflict", "text": "<strong>Story name:</strong> Update text here"}},
    {{"tag": "econ", "tag_label": "Markets", "text": "<strong>Story name:</strong> Update text here"}},
    {{"tag": "ai", "tag_label": "Tech", "text": "<strong>Story name:</strong> Update text here"}},
    {{"tag": "diplo", "tag_label": "Diplomacy", "text": "<strong>Story name:</strong> Update text here"}},
    {{"tag": "sci", "tag_label": "Science", "text": "<strong>Story name:</strong> Update text here"}}
  ]
}}

CRITICAL RULES:
- Write about REAL news happening TODAY: {today}
- Include minimum 5 articles plus the Claude AI article
- Every article body minimum 500 words with real facts and quotes
- Markets should reflect real approximate values
- Return ONLY the JSON object, nothing else"""

USER_PROMPT = """Today is {today}.

Write the complete WorldPulse daily blog. Cover:
1. The biggest geopolitical story today
2. The most important economic or financial news
3. A major science or health breakthrough
4. A conflict or humanitarian crisis update
5. The Claude AI column - what Anthropic and the AI industry did this week, benefits and risks for humanity
6. Any other major story happening today

Make every article feel like a real newspaper - specific facts, real quotes, proper analysis.
Return only the JSON."""

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>WorldPulse - {date}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=Source+Serif+4:opsz,wght@8..60,300;8..60,400&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet"/>
<style>
:root{{--ink:#0f0e0d;--paper:#f6f2ea;--cream:#faf7f2;--red:#c41e3a;--gold:#b8860b;--teal:#1a5f7a;--rule:#ddd6c8;--mist:#8a8680;--surf:#fff;--blue:#1a3a5c;--green:#1a4a2e;}}
*{{margin:0;padding:0;box-sizing:border-box;}}
html{{scroll-behavior:smooth;}}
body{{background:var(--paper);color:var(--ink);font-family:"Source Serif 4",Georgia,serif;font-size:17px;line-height:1.7;}}
.ticker{{background:var(--red);color:#fff;height:34px;display:flex;overflow:hidden;position:sticky;top:0;z-index:200;}}
.ticker-tag{{background:#000;color:#fff;padding:0 14px;font-family:"Space Mono",monospace;font-size:10px;letter-spacing:2px;display:flex;align-items:center;flex-shrink:0;text-transform:uppercase;}}
.ticker-track{{overflow:hidden;flex:1;display:flex;align-items:center;}}
.ticker-inner{{display:flex;white-space:nowrap;animation:tick 50s linear infinite;}}
.ticker-inner span{{font-size:11px;padding:0 36px;}}
.ticker-inner span::after{{content:"◆";margin-left:36px;opacity:.4;}}
@keyframes tick{{0%{{transform:translateX(0)}}100%{{transform:translateX(-50%)}}}}
.masthead{{background:var(--ink);padding:0 32px;border-bottom:3px solid var(--red);}}
.mast-top{{display:flex;align-items:center;justify-content:space-between;padding:18px 0 14px;border-bottom:1px solid rgba(255,255,255,.08);}}
.mast-date{{font-family:"Space Mono",monospace;font-size:10px;color:rgba(255,255,255,.45);letter-spacing:1px;text-transform:uppercase;}}
.mast-logo{{text-align:center;flex:1;}}
.logo-name{{font-family:"Playfair Display",serif;font-weight:900;font-size:clamp(2rem,5vw,3.8rem);color:#fff;letter-spacing:-1px;line-height:1;text-transform:uppercase;cursor:pointer;text-decoration:none;display:block;}}
.logo-name span{{color:var(--red);}}
.logo-tag{{font-family:"Space Mono",monospace;font-size:9px;color:rgba(255,255,255,.35);letter-spacing:4px;text-transform:uppercase;margin-top:3px;}}
.btn-sub{{background:var(--red);color:#fff;border:none;padding:7px 16px;font-family:"Space Mono",monospace;font-size:10px;letter-spacing:1px;text-transform:uppercase;cursor:pointer;}}
.nav{{display:flex;overflow-x:auto;scrollbar-width:none;}}
.nav::-webkit-scrollbar{{display:none;}}
.nav-item{{font-family:"Space Mono",monospace;font-size:10px;letter-spacing:1.5px;text-transform:uppercase;color:rgba(255,255,255,.5);padding:12px 18px;cursor:pointer;border-bottom:3px solid transparent;white-space:nowrap;text-decoration:none;transition:color .2s;}}
.nav-item:hover,.nav-item.active{{color:#fff;border-bottom-color:var(--red);}}
.markets{{display:flex;background:var(--cream);border-bottom:2px solid var(--rule);overflow-x:auto;padding:0 32px;}}
.m-item{{display:flex;align-items:center;gap:8px;padding:9px 20px 9px 0;border-right:1px solid var(--rule);white-space:nowrap;}}
.m-item:last-child{{border-right:none;}}
.m-label{{font-family:"Space Mono",monospace;font-size:9px;letter-spacing:1px;color:var(--mist);text-transform:uppercase;}}
.m-val{{font-family:"Space Mono",monospace;font-size:12px;font-weight:700;color:var(--ink);}}
.m-chg{{font-family:"Space Mono",monospace;font-size:10px;}}
.up{{color:#2a9e60;}}.down{{color:var(--red);}}
.container{{max-width:1220px;margin:0 auto;padding:0 32px;}}
.sec-hd{{display:flex;align-items:center;gap:14px;margin:40px 0 22px;}}
.sec-title{{font-family:"Playfair Display",serif;font-size:1.5rem;font-weight:900;text-transform:uppercase;color:var(--ink);}}
.sec-rule{{flex:1;height:2px;background:var(--rule);}}
.sec-rule.red{{background:var(--red);}}
.hero-grid{{display:grid;grid-template-columns:1.55fr 1fr;gap:2px;background:var(--rule);border:2px solid var(--rule);margin-top:32px;}}
.hero-lead{{background:var(--surf);padding:28px 32px;position:relative;}}
.hero-lead::before{{content:"";position:absolute;top:0;left:0;right:0;height:4px;background:var(--red);}}
.hero-img{{width:100%;height:260px;display:flex;align-items:center;justify-content:center;font-size:80px;margin-bottom:20px;cursor:pointer;background:linear-gradient(160deg,#0f1520,#1a3a58);}}
.kicker{{font-family:"Space Mono",monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase;color:var(--red);border-top:2px solid var(--red);padding-top:5px;display:inline-block;margin-bottom:10px;}}
.kicker.teal{{color:var(--teal);border-top-color:var(--teal);}}
.kicker.gold{{color:var(--gold);border-top-color:var(--gold);}}
h1.hero-hl{{font-family:"Playfair Display",serif;font-weight:900;font-size:clamp(1.6rem,2.6vw,2.3rem);line-height:1.15;color:var(--ink);margin-bottom:14px;cursor:pointer;}}
h1.hero-hl:hover{{color:var(--red);}}
.deck{{font-size:15px;color:#444;line-height:1.7;font-weight:300;margin-bottom:14px;}}
.byline{{font-family:"Space Mono",monospace;font-size:9px;color:var(--mist);letter-spacing:.8px;text-transform:uppercase;padding-top:12px;border-top:1px solid var(--rule);}}
.byline strong{{color:var(--ink);}}
.read-btn{{font-family:"Space Mono",monospace;font-size:10px;letter-spacing:1px;text-transform:uppercase;color:var(--red);cursor:pointer;display:inline-flex;align-items:center;gap:5px;margin-top:10px;text-decoration:none;}}
.read-btn:hover{{text-decoration:underline;}}
.hero-side{{background:var(--surf);padding:22px 26px;}}
.hero-side+.hero-side{{border-top:2px solid var(--rule);}}
.side-img{{width:100%;height:110px;margin-bottom:12px;display:flex;align-items:center;justify-content:center;font-size:38px;cursor:pointer;background:linear-gradient(160deg,#0f1520,#1a2a38);}}
.hl2{{font-family:"Playfair Display",serif;font-weight:700;font-size:1.05rem;line-height:1.3;color:var(--ink);cursor:pointer;margin-bottom:6px;}}
.hl2:hover{{color:var(--red);}}
.deck2{{font-size:13px;color:#555;line-height:1.6;font-weight:300;}}
.card-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:2px;background:var(--rule);border:2px solid var(--rule);}}
.card{{background:var(--surf);padding:22px;cursor:pointer;transition:background .15s;}}
.card:hover{{background:#fffef9;}}
.card-img{{width:100%;height:140px;display:flex;align-items:center;justify-content:center;font-size:40px;margin-bottom:14px;background:linear-gradient(160deg,#0f1520,#1a2a38);}}
.hl3{{font-family:"Playfair Display",serif;font-weight:700;font-size:.98rem;line-height:1.3;color:var(--ink);margin-bottom:6px;}}
.hl3:hover{{color:var(--red);}}
.deck3{{font-size:12px;color:#555;line-height:1.6;font-weight:300;}}
.dark-feat{{background:var(--ink);padding:38px 44px;display:grid;grid-template-columns:1.3fr 1fr;gap:40px;align-items:center;cursor:pointer;margin:2px 0;}}
.df-kicker{{font-family:"Space Mono",monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase;color:rgba(232,160,160,.8);border-top:2px solid var(--red);padding-top:5px;display:inline-block;margin-bottom:12px;}}
.df-hl{{font-family:"Playfair Display",serif;font-weight:900;font-size:clamp(1.4rem,2.2vw,2rem);line-height:1.2;color:#fff;margin-bottom:12px;}}
.df-deck{{font-size:14px;color:rgba(255,255,255,.6);line-height:1.7;}}
.df-read{{font-family:"Space Mono",monospace;font-size:10px;color:rgba(232,160,160,.8);display:inline-block;margin-top:12px;text-decoration:none;}}
.df-vis{{font-size:100px;opacity:.14;text-align:center;}}
.live-sec{{background:var(--ink);padding:34px 0;margin:40px 0;}}
.live-badge{{display:inline-flex;align-items:center;gap:7px;background:var(--red);color:#fff;font-family:"Space Mono",monospace;font-size:10px;letter-spacing:2px;padding:5px 12px;text-transform:uppercase;margin-bottom:18px;}}
.live-dot{{width:7px;height:7px;background:#fff;border-radius:50%;animation:blink 1.4s ease infinite;}}
@keyframes blink{{0%,100%{{opacity:1}}50%{{opacity:.3}}}}
.live-title{{font-family:"Playfair Display",serif;font-size:1.4rem;font-weight:900;color:#fff;margin-bottom:22px;}}
.u-item{{display:grid;grid-template-columns:90px 1fr;gap:16px;padding:14px 0;border-bottom:1px solid rgba(255,255,255,.07);}}
.u-time{{font-family:"Space Mono",monospace;font-size:11px;color:var(--red);}}
.u-text{{font-size:13px;color:rgba(255,255,255,.78);line-height:1.6;}}
.u-text strong{{color:#fff;}}
.utag{{display:inline-block;font-family:"Space Mono",monospace;font-size:8px;letter-spacing:1px;padding:2px 7px;margin-right:6px;text-transform:uppercase;border:1px solid;}}
.utag.war{{border-color:#ff7070;color:#ff7070;}}
.utag.econ{{border-color:#60c878;color:#60c878;}}
.utag.ai{{border-color:#a090f0;color:#a090f0;}}
.utag.diplo{{border-color:#f0c040;color:#f0c040;}}
.utag.sci{{border-color:#60aaf0;color:#60aaf0;}}
.bot-grid{{display:grid;grid-template-columns:2fr 300px;gap:2px;background:var(--rule);border:2px solid var(--rule);margin-bottom:40px;}}
.most-read{{background:var(--surf);padding:26px;}}
.mr-item{{display:grid;grid-template-columns:32px 1fr;gap:12px;padding:13px 0;border-bottom:1px solid var(--rule);cursor:pointer;}}
.mr-item:last-child{{border-bottom:none;}}
.mr-item:hover .mr-title{{color:var(--red);}}
.mr-num{{font-family:"Playfair Display",serif;font-size:1.7rem;font-weight:900;color:var(--rule);line-height:1;}}
.mr-title{{font-family:"Playfair Display",serif;font-size:.88rem;font-weight:700;color:var(--ink);line-height:1.3;margin-bottom:2px;}}
.mr-meta{{font-size:11px;color:var(--mist);}}
.sidebar{{background:var(--surf);padding:20px;}}
.sb-title{{font-family:"Space Mono",monospace;font-size:8px;letter-spacing:2px;text-transform:uppercase;color:var(--mist);margin-bottom:12px;padding-bottom:6px;border-bottom:2px solid var(--rule);}}
.nl-w p{{font-size:12px;color:#555;margin-bottom:10px;line-height:1.5;}}
.nl-w input{{width:100%;border:1px solid var(--rule);padding:8px 10px;font-size:13px;background:var(--cream);margin-bottom:7px;outline:none;}}
.nl-w button{{width:100%;background:var(--ink);color:#fff;border:none;padding:9px;font-family:"Space Mono",monospace;font-size:10px;letter-spacing:2px;cursor:pointer;}}
footer{{background:var(--ink);color:rgba(255,255,255,.4);padding:34px 32px;margin-top:56px;}}
.ft-inner{{max-width:1220px;margin:0 auto;display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:34px;padding-bottom:26px;border-bottom:1px solid rgba(255,255,255,.08);}}
.ft-logo{{font-family:"Playfair Display",serif;font-weight:900;font-size:1.6rem;color:#fff;text-decoration:none;display:block;cursor:pointer;}}
.ft-logo span{{color:var(--red);}}
.ft-brand p{{margin-top:9px;font-size:12px;line-height:1.7;}}
.ft-col h4{{font-family:"Space Mono",monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,.6);margin-bottom:11px;}}
.ft-col a{{display:block;font-size:12px;color:rgba(255,255,255,.35);text-decoration:none;margin-bottom:6px;cursor:pointer;}}
.ft-col a:hover{{color:#fff;}}
.ft-bot{{max-width:1220px;margin:20px auto 0;display:flex;justify-content:space-between;font-family:"Space Mono",monospace;font-size:9px;}}
.art-page{{max-width:780px;margin:0 auto;padding:44px 32px 80px;}}
.art-bc{{font-family:"Space Mono",monospace;font-size:9px;letter-spacing:1px;text-transform:uppercase;color:var(--mist);margin-bottom:18px;}}
.art-bc a{{color:var(--red);text-decoration:none;cursor:pointer;}}
.art-hl{{font-family:"Playfair Display",serif;font-weight:900;font-size:clamp(1.8rem,4vw,2.8rem);line-height:1.13;color:var(--ink);margin-bottom:16px;}}
.art-deck{{font-size:1.1rem;font-weight:300;color:#444;line-height:1.65;margin-bottom:20px;border-left:4px solid var(--red);padding-left:16px;font-style:italic;}}
.art-by{{display:flex;align-items:center;gap:11px;padding:13px 0;border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);margin-bottom:32px;flex-wrap:wrap;}}
.art-av{{width:36px;height:36px;border-radius:50%;background:var(--blue);display:flex;align-items:center;justify-content:center;color:#fff;font-family:"Playfair Display",serif;font-weight:700;font-size:14px;flex-shrink:0;}}
.art-by-name{{font-family:"Space Mono",monospace;font-size:10px;font-weight:700;color:var(--ink);letter-spacing:.5px;text-transform:uppercase;}}
.art-by-meta{{font-family:"Space Mono",monospace;font-size:9px;color:var(--mist);}}
.art-hero{{width:100%;height:300px;margin-bottom:26px;display:flex;align-items:center;justify-content:center;font-size:80px;background:linear-gradient(160deg,#0f1520,#1a3a58);border-radius:2px;}}
.art-body p{{margin-bottom:20px;font-size:1rem;line-height:1.85;color:#1a1a1a;}}
.art-body h3{{font-family:"Playfair Display",serif;font-size:1.35rem;font-weight:700;color:var(--ink);margin:36px 0 13px;padding-top:28px;border-top:2px solid var(--rule);}}
.art-body blockquote{{margin:32px 0;padding:20px 24px;background:var(--cream);border-left:5px solid var(--gold);font-style:italic;font-size:1.08rem;color:#333;line-height:1.7;}}
.art-body blockquote cite{{display:block;margin-top:9px;font-family:"Space Mono",monospace;font-size:9px;font-style:normal;color:var(--mist);letter-spacing:1px;text-transform:uppercase;}}
.pull-quote{{font-family:"Playfair Display",serif;font-size:1.4rem;font-weight:700;font-style:italic;color:var(--red);text-align:center;padding:28px 0;border-top:3px solid var(--red);border-bottom:3px solid var(--red);margin:36px 0;}}
.fact-box{{background:var(--blue);color:#fff;padding:24px;margin:32px 0;}}
.fact-box-title{{font-family:"Space Mono",monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase;color:var(--gold);margin-bottom:12px;}}
.fact-box ul{{list-style:none;}}
.fact-box ul li{{font-size:13px;padding:6px 0;border-bottom:1px solid rgba(255,255,255,.1);display:flex;justify-content:space-between;color:rgba(255,255,255,.82);}}
.fact-box ul li:last-child{{border-bottom:none;}}
.fact-box ul li strong{{color:#fff;font-family:"Space Mono",monospace;font-size:12px;}}
.art-tags{{margin-top:40px;padding-top:20px;border-top:2px solid var(--rule);display:flex;flex-wrap:wrap;gap:6px;}}
.atag{{font-family:"Space Mono",monospace;font-size:9px;letter-spacing:1px;text-transform:uppercase;border:1px solid var(--rule);padding:4px 10px;color:var(--mist);cursor:pointer;}}
.art-nav{{display:grid;grid-template-columns:1fr 1fr;gap:2px;background:var(--rule);border:2px solid var(--rule);margin-top:40px;}}
.art-nav-item{{background:var(--surf);padding:18px;cursor:pointer;}}
.art-nav-item:hover{{background:var(--cream);}}
.art-nav-item.next{{text-align:right;}}
.art-nav-dir{{font-family:"Space Mono",monospace;font-size:9px;letter-spacing:1px;text-transform:uppercase;color:var(--mist);margin-bottom:5px;}}
.art-nav-hl{{font-family:"Playfair Display",serif;font-weight:700;font-size:.92rem;color:var(--ink);line-height:1.3;}}
.art-nav-item:hover .art-nav-hl{{color:var(--red);}}
.back-btn{{font-family:"Space Mono",monospace;font-size:10px;letter-spacing:1px;text-transform:uppercase;color:var(--red);cursor:pointer;display:inline-flex;align-items:center;gap:5px;margin-top:26px;padding-top:26px;border-top:1px solid var(--rule);text-decoration:none;}}
.cat-page{{max-width:1100px;margin:0 auto;padding:36px 32px 80px;}}
.cat-hd{{text-align:center;padding:26px 0 30px;border-bottom:3px double var(--rule);margin-bottom:32px;}}
.cat-name{{font-family:"Playfair Display",serif;font-size:2.2rem;font-weight:900;color:var(--ink);}}
.cat-desc{{font-size:13px;color:var(--mist);margin-top:6px;}}
.cat-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:2px;background:var(--rule);border:2px solid var(--rule);}}
#app>*{{animation:fi .3s ease;}}
@keyframes fi{{from{{opacity:0;transform:translateY(5px)}}to{{opacity:1;transform:translateY(0)}}}}
@media(max-width:900px){{
.container,.art-page,.cat-page{{padding:0 16px;}}
.masthead{{padding:0 16px;}}
.markets{{padding:0 16px;}}
.hero-grid,.bot-grid{{grid-template-columns:1fr;}}
.card-grid,.cat-grid{{grid-template-columns:1fr 1fr;}}
.dark-feat{{grid-template-columns:1fr;}}
.df-vis{{display:none;}}
.ft-inner{{grid-template-columns:1fr 1fr;}}
.sidebar{{display:none;}}
.art-nav{{grid-template-columns:1fr;}}
}}
@media(max-width:540px){{
.card-grid,.cat-grid{{grid-template-columns:1fr;}}
.ft-inner{{grid-template-columns
