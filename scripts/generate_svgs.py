import json
import os
import urllib.request

THEMES = {
    "dark": {
        "bg": "#161618",
        "surface": "#1e1e21",
        "border": "#2e2e33",
        "text": "#ececec",
        "muted": "#8c8c92",
        "faint": "#3a3a40",
        "accent": "#e86c42",
        "accent_soft": "rgba(232, 108, 66, 0.16)",
        "line": "#ececec",
        "area_top": "rgba(236, 236, 236, 0.14)",
        "area_bot": "rgba(236, 236, 236, 0.0)",
    },
    "light": {
        "bg": "#fafafa",
        "surface": "#ffffff",
        "border": "#e5e5e5",
        "text": "#0a0a0a",
        "muted": "#737373",
        "faint": "#d4d4d4",
        "accent": "#c85a32",
        "accent_soft": "rgba(200, 90, 50, 0.12)",
        "line": "#111215",
        "area_top": "rgba(17, 18, 21, 0.10)",
        "area_bot": "rgba(17, 18, 21, 0.0)",
    },
}

OUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "graphics")
os.makedirs(OUT_DIR, exist_ok=True)


def fetch_github_data():
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        query = """
        {
          user(login: "isntle") {
            repositories(first: 100, ownerAffiliations: OWNER, isFork: false) {
              totalCount
              nodes {
                stargazerCount
                languages(first: 5, orderBy: {field: SIZE, direction: DESC}) {
                  edges {
                    size
                    node { name color }
                  }
                }
              }
            }
            contributionsCollection {
              totalCommitContributions
              totalPullRequestContributions
              contributionCalendar {
                totalContributions
                weeks {
                  contributionDays {
                    contributionCount
                    date
                  }
                }
              }
            }
          }
        }
        """
        req = urllib.request.Request(
            "https://api.github.com/graphql",
            data=json.dumps({"query": query}).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
                "User-Agent": "isntle-readme-generator",
            },
        )
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))["data"]["user"]
    with open("/tmp/gh_stats.json") as f:
        return json.load(f)["data"]["user"]


def gen_hero(theme_name, t):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 168" width="100%" role="img" aria-label="Luis Mérida — AI Engineer, Systems Programmer &amp; Founder">
  <style>
    .mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 10.5px; letter-spacing: 0.14em; fill: {t["muted"]}; }}
    .serif {{ font-family: Georgia, "Times New Roman", serif; font-size: 46px; font-weight: 400; fill: {t["text"]}; letter-spacing: -0.02em; }}
    .serif-it {{ font-style: italic; }}
    .sub {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 14px; font-weight: 400; fill: {t["muted"]}; }}
    @keyframes pulse {{
      0%, 100% {{ opacity: 1; transform: scale(1); }}
      50% {{ opacity: 0.35; transform: scale(1.45); }}
    }}
    @keyframes sweep {{
      0% {{ stroke-dashoffset: 840; }}
      100% {{ stroke-dashoffset: 0; }}
    }}
    @keyframes scan {{
      0% {{ transform: translateX(-120px); opacity: 0; }}
      15% {{ opacity: 1; }}
      85% {{ opacity: 1; }}
      100% {{ transform: translateX(840px); opacity: 0; }}
    }}
    .dot-pulse {{ transform-box: fill-box; transform-origin: center; animation: pulse 2.4s ease-in-out infinite; }}
    .wave-line {{ stroke-dasharray: 840; animation: sweep 2.2s cubic-bezier(0.16, 1, 0.3, 1) forwards; }}
    .scanner {{ animation: scan 5.5s linear infinite; }}
  </style>
  <defs>
    <linearGradient id="scanGrad-{theme_name}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{t["accent"]}" stop-opacity="0"/>
      <stop offset="50%" stop-color="{t["accent"]}" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="{t["accent"]}" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <rect x="0.5" y="0.5" width="839" height="167" rx="14" fill="{t["bg"]}" stroke="{t["border"]}"/>

  <!-- Top metadata bar -->
  <text x="32" y="34" class="mono">ENGINEER ID · LM-2026 · CDMX</text>
  <circle cx="624" cy="30" r="5" fill="{t["accent_soft"]}" class="dot-pulse"/>
  <circle cx="624" cy="30" r="2.5" fill="{t["accent"]}"/>
  <text x="636" y="34" class="mono">BUILDING RELAY &amp; FYTIC</text>

  <!-- Main editorial title -->
  <text x="32" y="92" class="serif">Luis <tspan class="serif-it">Mérida</tspan></text>
  <text x="32" y="122" class="sub">AI Engineer · Systems Programmer · Founder — building things that actually work in production.</text>

  <!-- Bottom animated signal track -->
  <line x1="32" y1="146" x2="808" y2="146" stroke="{t["border"]}" stroke-width="1"/>
  <path class="wave-line" d="M 32 146 L 280 146 L 292 146 L 298 139 L 304 152 L 310 143 L 316 146 L 808 146" fill="none" stroke="{t["muted"]}" stroke-width="1.2" opacity="0.7"/>
  <rect class="scanner" x="0" y="144.8" width="90" height="2.4" rx="1.2" fill="url(#scanGrad-{theme_name})"/>
</svg>'''
    with open(os.path.join(OUT_DIR, f"hero-{theme_name}.svg"), "w") as f:
        f.write(svg)


def gen_architecture(theme_name, t):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 200" width="100%" role="img" aria-label="Engineering Architecture Loop">
  <style>
    .mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 9.5px; letter-spacing: 0.12em; fill: {t["muted"]}; }}
    .title {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 14px; font-weight: 600; fill: {t["text"]}; }}
    .desc {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 11.5px; fill: {t["muted"]}; }}
    .tag {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 10px; fill: {t["accent"]}; }}
    @keyframes flow {{
      0% {{ stroke-dashoffset: 24; }}
      100% {{ stroke-dashoffset: 0; }}
    }}
    @keyframes breathe {{
      0%, 100% {{ opacity: 0.45; }}
      50% {{ opacity: 1; }}
    }}
    .stream {{ stroke-dasharray: 4 4; animation: flow 1.1s linear infinite; }}
    .n1 {{ animation: breathe 3.2s ease-in-out infinite 0s; }}
    .n2 {{ animation: breathe 3.2s ease-in-out infinite 1s; }}
    .n3 {{ animation: breathe 3.2s ease-in-out infinite 2s; }}
  </style>

  <rect x="0.5" y="0.5" width="839" height="199" rx="14" fill="{t["bg"]}" stroke="{t["border"]}"/>
  <text x="28" y="30" class="mono">HOW I ARCHITECT SYSTEMS · HYBRID EDGE + AGENTIC RUNTIME + HARDENED INFRA</text>

  <!-- Node 1: On-Device / Edge -->
  <rect x="28" y="48" width="234" height="124" rx="10" fill="{t["surface"]}" stroke="{t["border"]}"/>
  <circle cx="46" cy="68" r="3" fill="{t["accent"]}" class="n1"/>
  <text x="56" y="71" class="mono">01 · EDGE &amp; ON-DEVICE</text>
  <text x="44" y="96" class="title">Zero-Cost Determinism</text>
  <text x="44" y="116" class="desc">Local inference, normalization</text>
  <text x="44" y="132" class="desc">&amp; offline persistence.</text>
  <text x="44" y="156" class="tag">Sentinel · Hincha · ONE</text>

  <!-- Connector 1 -> 2 -->
  <line x1="262" y1="110" x2="303" y2="110" stroke="{t["accent"]}" stroke-width="1.5" class="stream"/>
  <polygon points="299,106 306,110 299,114" fill="{t["accent"]}"/>

  <!-- Node 2: Agentic Runtime -->
  <rect x="303" y="48" width="234" height="124" rx="10" fill="{t["surface"]}" stroke="{t["border"]}"/>
  <circle cx="321" cy="68" r="3" fill="{t["accent"]}" class="n2"/>
  <text x="331" y="71" class="mono">02 · AGENTIC RUNTIME</text>
  <text x="319" y="96" class="title">Bounded Autonomy</text>
  <text x="319" y="116" class="desc">Code-checked mandates, voice</text>
  <text x="319" y="132" class="desc">agents &amp; human handoff.</text>
  <text x="319" y="156" class="tag">Relay · FyTic · Ghost Shopper</text>

  <!-- Connector 2 -> 3 -->
  <line x1="537" y1="110" x2="578" y2="110" stroke="{t["accent"]}" stroke-width="1.5" class="stream"/>
  <polygon points="574,106 581,110 574,114" fill="{t["accent"]}"/>

  <!-- Node 3: Hardened Infra -->
  <rect x="578" y="48" width="234" height="124" rx="10" fill="{t["surface"]}" stroke="{t["border"]}"/>
  <circle cx="596" cy="68" r="3" fill="{t["accent"]}" class="n3"/>
  <text x="606" y="71" class="mono">03 · HARDENED SYSTEMS</text>
  <text x="594" y="96" class="title">Production &amp; POSIX</text>
  <text x="594" y="116" class="desc">Multi-tenant RLS, local LLMs</text>
  <text x="594" y="132" class="desc">&amp; low-level C systems.</text>
  <text x="594" y="156" class="tag">CleanOps · Ronald's · Minishell</text>
</svg>'''
    with open(os.path.join(OUT_DIR, f"architecture-{theme_name}.svg"), "w") as f:
        f.write(svg)


def gen_stats_and_activity(data):
    repos = data["repositories"]["totalCount"]
    commits = data["contributionsCollection"]["totalCommitContributions"]
    total_cal = data["contributionsCollection"]["contributionCalendar"]["totalContributions"]

    langs = {}
    for r in data["repositories"]["nodes"]:
        for e in r["languages"]["edges"]:
            name = e["node"]["name"]
            color = e["node"]["color"] or "#888888"
            langs[name] = (langs.get(name, (0, color))[0] + e["size"], color)
    total_sz = sum(v[0] for v in langs.values()) or 1
    top_langs = sorted(langs.items(), key=lambda x: x[1][0], reverse=True)[:5]

    weeks = data["contributionsCollection"]["contributionCalendar"]["weeks"]
    weekly = [sum(d["contributionCount"] for d in w["contributionDays"]) for w in weeks]
    max_w = max(weekly) or 1

    for theme_name, t in THEMES.items():
        # 1. Stats + Languages SVG
        bar_x = 340
        bar_w = 468
        bar_segments = []
        legend_items = []
        curr_x = bar_x
        for i, (lname, (sz, col)) in enumerate(top_langs):
            pct = sz / total_sz
            seg_w = max(4, round(pct * bar_w, 1))
            if i == len(top_langs) - 1:
                seg_w = max(4, round(bar_x + bar_w - curr_x, 1))
            bar_segments.append(
                f'<rect x="{curr_x}" y="68" width="{seg_w}" height="8" rx="2" fill="{col}"/>'
            )
            curr_x += seg_w
            lx = bar_x + (i % 3) * 158
            ly = 104 + (i // 3) * 24
            legend_items.append(
                f'<circle cx="{lx + 4}" cy="{ly - 4}" r="3.5" fill="{col}"/>'
                f'<text x="{lx + 14}" y="{ly}" class="leg">{lname} <tspan fill="{t["muted"]}">{pct*100:.1f}%</tspan></text>'
            )

        stats_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 156" width="100%" role="img" aria-label="GitHub Telemetry and Language Stack">
  <style>
    .mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 9.5px; letter-spacing: 0.12em; fill: {t["muted"]}; }}
    .num {{ font-family: Georgia, "Times New Roman", serif; font-size: 34px; font-weight: 400; fill: {t["text"]}; }}
    .lbl {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 11px; fill: {t["muted"]}; }}
    .leg {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 11.5px; font-weight: 500; fill: {t["text"]}; }}
    @keyframes reveal {{
      0% {{ transform: scaleX(0); }}
      100% {{ transform: scaleX(1); }}
    }}
    .bar-wrap {{ transform-origin: 340px 72px; animation: reveal 1.2s cubic-bezier(0.16, 1, 0.3, 1) forwards; }}
  </style>
  <rect x="0.5" y="0.5" width="839" height="155" rx="14" fill="{t["bg"]}" stroke="{t["border"]}"/>

  <!-- Left: Metrics -->
  <text x="32" y="34" class="mono">GITHUB TELEMETRY · @ISNTLE</text>
  <text x="32" y="92" class="num">{total_cal}</text>
  <text x="32" y="114" class="lbl">Contributions (52w)</text>

  <text x="148" y="92" class="num">{commits}</text>
  <text x="148" y="114" class="lbl">Commits</text>

  <text x="242" y="92" class="num">{repos}</text>
  <text x="242" y="114" class="lbl">Repos</text>

  <line x1="312" y1="28" x2="312" y2="128" stroke="{t["border"]}"/>

  <!-- Right: Languages -->
  <text x="340" y="34" class="mono">TOP LANGUAGES BY VOLUME</text>
  <g class="bar-wrap">
    {"".join(bar_segments)}
  </g>
  {"".join(legend_items)}
</svg>'''
        with open(os.path.join(OUT_DIR, f"stats-{theme_name}.svg"), "w") as f:
            f.write(stats_svg)

        # 2. Activity Pulse Graph SVG
        gx, gy, gw, gh = 32, 46, 776, 86
        pts = []
        n = len(weekly)
        for i, val in enumerate(weekly):
            px = gx + (i / max(1, n - 1)) * gw
            py = gy + gh - (val / max_w) * (gh - 8)
            pts.append((px, py))

        line_d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)
        area_d = line_d + f" L {pts[-1][0]:.1f} {gy + gh} L {pts[0][0]:.1f} {gy + gh} Z"
        last_x, last_y = pts[-1]

        activity_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 162" width="100%" role="img" aria-label="52-Week Contribution Activity">
  <style>
    .mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 9.5px; letter-spacing: 0.12em; fill: {t["muted"]}; }}
    @keyframes draw {{
      0% {{ stroke-dashoffset: 1600; }}
      100% {{ stroke-dashoffset: 0; }}
    }}
    @keyframes ping {{
      0%, 100% {{ transform: scale(1); opacity: 0.9; }}
      50% {{ transform: scale(2.1); opacity: 0; }}
    }}
    .pulse-line {{ stroke-dasharray: 1600; animation: draw 2.2s cubic-bezier(0.16, 1, 0.3, 1) forwards; }}
    .ping-ring {{ transform-box: fill-box; transform-origin: center; animation: ping 2.2s ease-out infinite; }}
  </style>
  <defs>
    <linearGradient id="areaGrad-{theme_name}" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{t["line"]}" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="{t["line"]}" stop-opacity="0.0"/>
    </linearGradient>
  </defs>

  <rect x="0.5" y="0.5" width="839" height="161" rx="14" fill="{t["bg"]}" stroke="{t["border"]}"/>

  <text x="32" y="30" class="mono">CONTRIBUTION PULSE · 52 WEEKS</text>
  <text x="640" y="30" class="mono">PEAK: {max_w}/WK · TOTAL: {total_cal}</text>

  <!-- Subtle gridlines -->
  <line x1="{gx}" y1="{gy + gh * 0.25:.1f}" x2="{gx + gw}" y2="{gy + gh * 0.25:.1f}" stroke="{t["border"]}" stroke-dasharray="2 4"/>
  <line x1="{gx}" y1="{gy + gh * 0.65:.1f}" x2="{gx + gw}" y2="{gy + gh * 0.65:.1f}" stroke="{t["border"]}" stroke-dasharray="2 4"/>
  <line x1="{gx}" y1="{gy + gh}" x2="{gx + gw}" y2="{gy + gh}" stroke="{t["border"]}"/>

  <path d="{area_d}" fill="url(#areaGrad-{theme_name})"/>
  <path class="pulse-line" d="{line_d}" fill="none" stroke="{t["line"]}" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round"/>

  <!-- Live endpoint -->
  <circle cx="{last_x:.1f}" cy="{last_y:.1f}" r="5" fill="{t["accent"]}" class="ping-ring"/>
  <circle cx="{last_x:.1f}" cy="{last_y:.1f}" r="3" fill="{t["accent"]}"/>
</svg>'''
        with open(os.path.join(OUT_DIR, f"activity-{theme_name}.svg"), "w") as f:
            f.write(activity_svg)


def main():
    data = fetch_github_data()
    for theme_name, t in THEMES.items():
        gen_hero(theme_name, t)
        gen_architecture(theme_name, t)
    gen_stats_and_activity(data)
    print("Generated all SVGs successfully!")


if __name__ == "__main__":
    main()
