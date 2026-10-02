"""Live GitHub stats card in the Agency theme. Runs daily from .github/workflows/profile.yml (needs `gh` + GH_TOKEN)."""
import json, subprocess
from collections import Counter
from lib import *

LOGIN = 'TheAgencyMGE'
QUERY = """
query($login:String!){ user(login:$login){
  followers{totalCount}
  repositories(ownerAffiliations:OWNER, isFork:false, privacy:PUBLIC, first:100){
    totalCount
    nodes{ stargazerCount languages(first:10, orderBy:{field:SIZE, direction:DESC}){ edges{ size node{ name } } } }
  }
  contributionsCollection{ totalCommitContributions totalPullRequestContributions contributionCalendar{ totalContributions } }
}}"""


def fetch():
    out = subprocess.run(['gh', 'api', 'graphql', '-f', f'query={QUERY}', '-F', f'login={LOGIN}'],
                         capture_output=True, text=True, check=True).stdout
    u = json.loads(out)['data']['user']
    repos = u['repositories']['nodes']
    langs = Counter()
    for r in repos:
        for e in r['languages']['edges']:
            langs[e['node']['name']] += e['size']
    cc = u['contributionsCollection']
    return dict(
        stars=sum(r['stargazerCount'] for r in repos),
        repos=u['repositories']['totalCount'],
        followers=u['followers']['totalCount'],
        commits=cc['totalCommitContributions'],
        prs=cc['totalPullRequestContributions'],
        contribs=cc['contributionCalendar']['totalContributions'],
        langs=langs.most_common(6),
        lang_total=sum(langs.values()),
    )


def render(s):
    W, H = 1000, 380
    d = Doc(W, H, f"Ryan Panda's GitHub stats: {s['stars']} stars, {s['contribs']} contributions in the last year")
    d.add(panel_bg(d, W, H))
    d.css.append('@keyframes slide{from{transform:translateX(-1100px)}}')
    d.css.append('@keyframes fillx{from{transform:scaleX(0)}}')
    d.css.append('@keyframes popn{0%{transform:scale(1.8) rotate(-10deg)}100%{transform:none}}')

    # ---- left: player stats
    d.add(f'<g transform="translate(40,34)">' + skewbox(0, 0, 230, 36, -12, RED) + d.text(115, 27, 'PLAYER STATS', 'Anton', 22, '#fff', 'middle', .16) + '</g>')
    rows = [('STARS EARNED', s['stars']), ('CONTRIBUTIONS · 1Y', s['contribs']), ('COMMITS · 1Y', s['commits']),
            ('PULL REQUESTS · 1Y', s['prs']), ('FOLLOWERS', s['followers'])]
    for i, (lab, val) in enumerate(rows):
        y = 92 + i * 46
        sh = RED if i % 2 == 0 else GOLD
        d.add(f'<g transform="translate(40,{y})"><g style="animation:slide .35s cubic-bezier(.2,1.6,.4,1) {.1 + i * .08:.2f}s both">'
              + skewbox(0, 0, 420, 36, -10, INK, '#fff', 3, sh, 6, 6)
              + f'<g transform="translate(20,18)"><g style="animation:spin {3 + i}s linear infinite">{star(0, 0, 20, sh)}</g></g>'
              + d.text(40, 26, lab, 'Anton', 19, '#fff', 'start', .06)
              + f'<g class="c" style="animation:popn .4s cubic-bezier(.2,1.8,.4,1) {.5 + i * .08:.2f}s both">'
              + d.text(402, 28, f'{val:,}', 'Anton', 26, GOLD, 'end') + '</g></g></g>')

    # ---- right: top languages
    x0 = 520
    d.add(f'<g transform="translate({x0},34)">' + skewbox(0, 0, 250, 36, -12, GOLD) + d.text(125, 27, 'TOP LANGUAGES', 'Anton', 22, INK, 'middle', .16) + '</g>')
    BW = 440
    for i, (name, size) in enumerate(s['langs']):
        pct = size / s['lang_total'] if s['lang_total'] else 0
        y = 92 + i * 46
        col = [RED, GOLD, '#fff'][i % 3]
        d.add(f'<g transform="translate({x0},{y})">'
              + d.text(0, 18, name.upper(), 'Anton', 17, '#fff', 'start', .06) + d.text(BW, 18, f'{pct * 100:.1f}%', 'Mono', 14, GOLD, 'end')
              + f'<g transform="translate(0,26) skewX(-14)"><rect width="{BW}" height="12" fill="{INK}" stroke="#fff" stroke-width="2"/>'
              f'<rect class="bl" x="1" y="1" width="{max(2, (BW - 2) * pct / (s["langs"][0][1] / s["lang_total"])):.1f}" height="10" fill="{col}" '
              f'style="animation:fillx .7s cubic-bezier(.2,1.2,.4,1) {.4 + i * .1:.2f}s both"/></g></g>')
    d.add(crt(d, W, H))
    d.save('stats.svg')


if __name__ == '__main__':
    render(fetch())
