"""Generates every page of the CommonCrayon site (design 5, Midnight)."""
import pathlib, html

root = pathlib.Path(__file__).resolve().parent.parent
STEAM_IMG = "https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/2862670/header.jpg"
STEAM_URL = "https://store.steampowered.com/app/2862670/Playback_Loop/"
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '  <link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=Inter:wght@400;500;700&display=swap" rel="stylesheet">')
FALLBACK = "this.parentElement.classList.add('is-fallback');this.remove()"

GAMES = [dict(
    pn="MP-001", slug="playback-loop", name="Playback Loop",
    img=STEAM_IMG, fit=False, alt="Playback Loop key art",
    desc="First-person puzzle game by MapPack. Record your moves and replay them as ghosts.",
    spec=[("Price", "Free"), ("Platform", "Steam"), ("Released", "2024-07-22"), ("Studio", "MapPack")],
    steam=True)]
SOFTWARE = [
    dict(pn="CC-001", slug="crayon-all-portals", name="CrayonAllPortals",
         img="assets/img/allportals-app.jpg", fit=False,
         alt="CrayonAllPortals with eight stronghold rings and four colour-coded player paths",
         desc="Plans an All Portals route from one stronghold per ring and splits it evenly between players.",
         repo="CommonCrayon/CrayonAllPortals", ext=".exe", platform="Windows 10/11"),
    dict(pn="CC-002", slug="crayon-nav-assist", name="CrayonNavAssist",
         img="assets/img/nav-assist.png", fit=True,
         alt="CrayonNavAssist window showing stronghold 4 of 8 with distance and angle",
         desc="Overlay that shows the distance and turn angle to your next stronghold each time you press F3+C.",
         repo="CommonCrayon/CrayonAllPortalsJava", ext=".jar", platform="Java 17+"),
]
DL_ICON = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 4v12M6 11l6 6 6-6M5 20h14"/></svg>'


def shell(p, current, title, desc, body):
    def nav(key, href, label, count=None):
        cur = ' aria-current="page"' if key == current else ''
        c = f'<small>{count}</small>' if count is not None else ''
        return f'<a href="{href}"{cur}>{label}{c}</a>'
    full_title = "CommonCrayon" if title is None else f"{title} | CommonCrayon"
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{full_title}</title>
  <meta name="description" content="{html.escape(desc)}">
  <meta name="theme-color" content="#0c1428">
  <meta property="og:title" content="{title or 'CommonCrayon'}">
  <meta property="og:description" content="{html.escape(desc)}">
  <link rel="icon" type="image/png" href="{p}assets/img/favicon.png">
  <link rel="apple-touch-icon" href="{p}assets/img/apple-touch-icon.png">
  {FONTS}
  <link rel="stylesheet" href="{p}assets/css/site.css">
</head>
<body>
  <a class="skip" href="#content">Skip to content</a>
  <div class="lay">
    <aside class="side">
      <a class="brand" href="{p}"><img src="{p}assets/img/logo.jpg" alt="" width="30" height="30">CommonCrayon</a>
      <nav aria-label="Main">
        {nav("all", p or "./", "All", len(GAMES) + len(SOFTWARE))}
        {nav("games", p + "#games", "Games", len(GAMES))}
        {nav("software", p + "#software", "Software", len(SOFTWARE))}
        {nav("privacy", p + "privacy/", "Privacy")}
      </nav>
      <div class="meta">CATALOGUE<br>REV 2026.10<br>© 2026 CommonCrayon<br>Ads keep this site free.</div>
    </aside>
    <main id="content">
{body}
    </main>
  </div>
  <script src="{p}assets/js/releases.js" defer></script>
  <script src="{p}assets/js/ads.js" defer></script>
</body>
</html>
'''


def fig(e, p):
    src = e["img"] if e["img"].startswith("http") else p + e["img"]
    cls = "fit" if e["fit"] else "cover"
    onerr = f' onerror="{FALLBACK}"' if e["img"].startswith("http") else ''
    style = ' style="object-position:center"' if e.get("steam") else ''
    return f'<div class="fig"><img class="{cls}" src="{src}" alt="{e["alt"]}" loading="lazy"{style}{onerr}></div>'


def game_spec(e):
    return '<table class="spec">' + ''.join(f'<tr><td>{k}</td><td>{v}</td></tr>' for k, v in e["spec"]) + '</table>'


def soft_spec(e):
    return (f'<table class="spec">'
            f'<tr><td>Version</td><td data-field="version">Latest</td></tr>'
            f'<tr><td>Platform</td><td>{e["platform"]}</td></tr>'
            f'<tr><td>File</td><td>{e["ext"]}<span data-hide-empty hidden>, <span data-field="size"></span></span></td></tr>'
            f'</table>')


def dl_button(cls=""):
    return f'<a class="btn{cls}" data-download aria-disabled="true">{DL_ICON}<span data-label>Download</span></a>'


# ---------------- Home ----------------
def home():
    p = ""
    games = ''.join(
        f'''        <li class="row">
          {fig(e, p)}
          <div><div class="pn">{e["pn"]}</div><h3><a href="projects/{e["slug"]}/">{e["name"]}</a></h3><p>{e["desc"]}</p></div>
          {game_spec(e)}
          <div class="acts"><a class="btn" href="{STEAM_URL}">Play free on Steam</a><a class="btn line" href="projects/{e["slug"]}/">Details</a></div>
        </li>
''' for e in GAMES)
    soft = ''.join(
        f'''        <li class="row" data-repo="{e["repo"]}" data-asset="{e["ext"]}">
          {fig(e, p)}
          <div><div class="pn">{e["pn"]}</div><h3><a href="projects/{e["slug"]}/">{e["name"]}</a></h3><p>{e["desc"]}</p></div>
          {soft_spec(e)}
          <div class="acts">{dl_button()}<a class="btn line" href="projects/{e["slug"]}/">Details</a></div>
        </li>
''' for e in SOFTWARE)
    n = lambda k: f'{k} ITEM' if k == 1 else f'{k} ITEMS'
    body = f'''      <h1>Free games and software.</h1>
      <p class="sub">Games from MapPack and tools for Minecraft All Portals speedruns. Everything here is free.</p>

      <div class="sec" id="games"><h2>Games</h2><span>{n(len(GAMES))}</span></div>
      <ul class="list">
{games}      </ul>

      <div class="sec" id="software"><h2>Software</h2><span>{n(len(SOFTWARE))}</span></div>
      <ul class="list">
{soft}      </ul>
      <p class="later">CC-{len(SOFTWARE) + 1:03d} … in progress</p>

      <div class="ad-row"><div class="ad-slot"></div></div>'''
    (root / 'index.html').write_text(shell(p, "all", None, "Free games and software by CommonCrayon: games from MapPack and tools for Minecraft All Portals speedruns.", body))


# ---------------- Project pages ----------------
def project(e, current, aside, content):
    p = "../../"
    body = f'''      <p class="crumb"><a href="{p}">All</a> / <a href="{p}#{current}">{current.capitalize()}</a> / {e["name"]}</p>
      <div class="head">
        <div><div class="pn">{e["pn"]}</div><h1>{e["name"]}</h1><p>{e["desc"]}</p></div>
      </div>
      <div class="page">
        <div class="prose">
{content}
        </div>
        <aside class="aside">
{aside}
          <div class="ad-slot"></div>
        </aside>
      </div>'''
    out = root / 'projects' / e["slug"]
    out.mkdir(parents=True, exist_ok=True)
    (out / 'index.html').write_text(shell(p, current, e["name"], e["desc"], body))


def soft_panel(e, needs, kind):
    return f'''          <div class="panel" data-repo="{e["repo"]}" data-asset="{e["ext"]}">
            <h2>DOWNLOAD</h2>
            {dl_button()}
            <table class="spec">
              <tr><td>Version</td><td data-field="version">Latest</td></tr>
              <tr><td>File</td><td>{kind}</td></tr>
              <tr data-hide-empty hidden><td>Size</td><td data-field="size"></td></tr>
              <tr data-hide-empty hidden><td>Released</td><td data-field="date"></td></tr>
              <tr data-hide-empty hidden><td>Downloads</td><td data-field="downloads"></td></tr>
              <tr><td>Needs</td><td>{needs}</td></tr>
            </table>
          </div>'''


AP, NA = SOFTWARE
project(AP, "software", soft_panel(AP, "Windows 10/11", ".exe") + '''
          <div class="panel"><h2>WORKS WITH</h2><p class="note"><a href="../crayon-nav-assist/">CrayonNavAssist</a> (CC-002) follows the route in game and tells each player where to go next.</p></div>''',
'''          <figure class="figure">
            <img src="../../assets/img/allportals-app.jpg" alt="CrayonAllPortals with eight stronghold rings entered and four colour-coded player paths on the map" width="1000" height="1010">
            <figcaption>FIG. 1  Eight rings entered, four paths generated. Each path's colour matches its player.</figcaption>
          </figure>

          <h2>What it does</h2>
          <p>An All Portals run means lighting every End portal in the game. Enter one stronghold per ring and CrayonAllPortals predicts the rest of the ring, shows the ideal blind distance for each ring in the overworld and the nether, and works out the best route through all of them.</p>
          <p>In co-op, players pair up on paths. The solver balances the paths so they all finish around the same time, and you can give faster players more work by raising their weight.</p>

          <h2>How to use it</h2>
          <ol class="steps">
            <li><span>Download <code>CrayonAllPortals.exe</code> and run it. There's nothing to install.</span></li>
            <li><span>Enter the X and Z of one stronghold in each ring, or paste an F3+C command, then press Set. <a href="../crayon-nav-assist/">CrayonNavAssist</a> helps you measure these.</span></li>
            <li><span>Set the number of players and how long the solver should search. More time gives better routes.</span></li>
            <li><span>Click Generate Paths. The map draws the best routes found so far while it works.</span></li>
            <li><span>Edit any path's stronghold list to change it. The map updates as you type.</span></li>
            <li><span>Click Copy for NavAssist and paste each player's path into their CrayonNavAssist.</span></li>
          </ol>

          <h2>What gets copied</h2>
          <p>The copied text lists each path as <code>[id, x, z]</code> lines, ready for CrayonNavAssist:</p>
<pre><code>All Portals Paths

Path 1 - Player 1 &amp; Player 2
[5,941,5033]
[12,118,8191]
[23,2565,10968]

Path 2 - Player 3 &amp; Player 4
[2,-1246,1625]
[6,-3888,3331]
[13,-4719,6696]</code></pre>
          <p>Everything you enter is saved automatically and comes back the next time you open the app.</p>''')

project(NA, "software", soft_panel(NA, "Java 17+", ".jar") + '''
          <div class="panel"><h2>WORKS WITH</h2><p class="note"><a href="../crayon-all-portals/">CrayonAllPortals</a> (CC-001) plans the route you paste in here.</p></div>''',
'''          <div class="figs">
            <figure class="figure pad">
              <img src="../../assets/img/config-page.png" alt="CrayonNavAssist config page with a pasted route, launch button and settings" width="421" height="600">
              <figcaption>FIG. 1  Config page</figcaption>
            </figure>
            <figure class="figure pad">
              <img src="../../assets/img/nav-assist.png" alt="Nav window showing stronghold 4 of 8, target coordinates, distance and turning angle" width="522" height="180">
              <figcaption>FIG. 2  Nav window. Green means you're facing the right way.</figcaption>
            </figure>
          </div>

          <h2>How to use it</h2>
          <ol class="steps">
            <li><span>Download the latest <code>.jar</code> and open it. You need Java 17 or newer.</span></li>
            <li><span>Find a stronghold in each ring using the eight default coordinates.</span></li>
            <li><span>Put your results into <a href="../crayon-all-portals/">CrayonAllPortals</a> to get your route.</span></li>
            <li><span>Paste the route in and click Launch.</span></li>
            <li><span>Press F3+C in game whenever you want the distance and angle updated.</span></li>
          </ol>

          <h2>The nav window</h2>
          <ul>
            <li><strong>ID</strong> is the stronghold number.</li>
            <li><strong>Target</strong> is where to go. It switches to nether coordinates while you're in the nether.</li>
            <li><strong>Distance</strong> is how many blocks are left.</li>
            <li><strong>Angle</strong> is the F3 facing to aim for, then how far to turn.</li>
            <li>Use the arrow buttons or Ctrl + Left / Right to move between strongholds. Right-click the window to jump back to the first.</li>
          </ul>

          <h2>Settings</h2>
          <ul>
            <li><strong>Paste list</strong> takes one <code>[id, x, z]</code> per line and ignores other lines. Add <code>"a note"</code> after a line to show it under the target.</li>
            <li><strong>Target as Chunks</strong> shows chunk coordinates instead of block coordinates.</li>
            <li><strong>Compact Overlay</strong> hides the title bar and lets you set the opacity. Drag to move it, right-click to close it.</li>
            <li><strong>Rebind Controls</strong> lets you set any key combo. Press Esc to cancel.</li>
          </ul>
          <p>Settings save automatically to <code>%APPDATA%\\CrayonNavAssist</code>. Relaunching picks up at the same stronghold.</p>''')

PL = GAMES[0]
project(PL, "games", f'''          <div class="panel">
            <h2>PLAY</h2>
            <a class="btn" href="{STEAM_URL}">Play free on Steam</a>
            <table class="spec">
              <tr><td>Price</td><td>Free</td></tr>
              <tr><td>Released</td><td>2024-07-22</td></tr>
              <tr><td>Players</td><td>1</td></tr>
              <tr><td>Studio</td><td>MapPack</td></tr>
            </table>
          </div>''',
f'''          <figure class="figure">
            <img src="{STEAM_IMG}" alt="Playback Loop key art" width="460" height="215" onerror="this.closest('figure').remove()">
          </figure>

          <h2>About the game</h2>
          <p>Playback Loop is a puzzle platformer built around time. Record what you do, then replay it as a ghost and work alongside your past selves, or against them. Most puzzles have more than one solution, so planning a few moves ahead pays off.</p>
          <ul>
            <li>Record and replay your own actions to solve puzzles</li>
            <li>Flexible mechanics that allow several solutions</li>
            <li>Steam achievements, stats and leaderboards</li>
            <li>Full audio and subtitles in English</li>
          </ul>

          <h2>Get it on Steam</h2>
          <iframe class="steam-embed" src="https://store.steampowered.com/widget/2862670/" title="Playback Loop on Steam" loading="lazy"></iframe>

          <h2>About MapPack</h2>
          <p>MapPack is the indie studio behind Playback Loop. Follow along at <a href="https://www.mappack.net/">mappack.net</a>.</p>''')

# ---------------- Privacy ----------------
def privacy():
    p = "../"
    body = '''      <h1>Privacy</h1>
      <p class="sub">What this site collects, who it shares it with, and how to opt out. Last updated 29 October 2026.</p>
      <div class="prose">
          <h2>Ads</h2>
          <p>This site uses Google AdSense to show ads. Google and its partners use cookies to show ads based on your visits to this site and other sites on the internet.</p>
          <p>You can turn off personalised ads in <a href="https://adssettings.google.com/">Google's ad settings</a>, or opt out of personalised ads from many companies at <a href="https://www.aboutads.info/choices/">aboutads.info</a>. To learn more, read <a href="https://policies.google.com/technologies/partner-sites">how Google uses information from sites that use its services</a>.</p>
          <p>Visitors in the EEA, UK and Switzerland are asked for consent before personalised ads are shown.</p>

          <h2>Downloads and release info</h2>
          <p>Download buttons get the latest version numbers from GitHub, which also hosts the files, so your browser connects to GitHub's servers when you open a page or download something. See <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">GitHub's privacy statement</a>.</p>

          <h2>Hosting</h2>
          <p>The site is hosted on GitHub Pages, which may log your IP address for security. This site has no accounts or sign-up forms, and doesn't run its own analytics.</p>
      </div>'''
    (root / 'privacy').mkdir(exist_ok=True)
    (root / 'privacy' / 'index.html').write_text(shell(p, "privacy", "Privacy", "How the CommonCrayon website uses cookies, ads and third-party services.", body))


def notfound():
    # Served from any path, so it uses root-absolute links.
    page = shell("/", None, "Page not found", "This page doesn't exist.",
                 '''      <h1>This page doesn't exist.</h1>
      <p class="sub">The link may be old, or the page may have moved. Everything you can download is on the main list.</p>
      <p><a class="btn" style="display:inline-flex" href="/">Go to the list</a></p>''')
    page = page.replace('<script src="/assets/js/releases.js" defer></script>\n', '')
    (root / '404.html').write_text(page)


home(); privacy(); notfound()
print("ok")
