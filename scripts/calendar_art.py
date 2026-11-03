from html.parser import HTMLParser
import re
from zlib import crc32


class ContributionParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.days = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == 'td' and 'data-date' in values:
            self.days.append((values['data-date'], int(values['data-level'])))


def contribution_markup(source):
    parser = ContributionParser()
    parser.feed(source)
    total = re.search(r'(\d[\d,]*)\s+contributions\s+in the last year', source).group(1)
    days = sorted(parser.days)
    cells = ''.join(f'<span class="day level-{level}" data-tooltip="{day}" aria-hidden="true"></span>' for day, level in days)
    cells += '<span aria-hidden="true"></span>' * ((7-len(days) % 7) % 7)
    return total, cells


def blue_calendar(source, mobile=False, light=False):
    parser = ContributionParser()
    parser.feed(source)
    days = sorted(parser.days)
    days += [('', 0)] * (-len(days) % 7)
    total = re.search(r'(\d[\d,]*)\s+contributions\s+in the last year', source).group(1)
    snapshot = re.search(r'data-to="(\d{4}-\d{2}-\d{2})', source).group(1)
    width, height = (420, 130) if mobile else (900, 190)
    colors = ['#ebedf0', '#b8d4fb', '#79b2f8', '#438de6', '#0969da'] if light else ['#161b22', '#142b4b', '#22538b', '#397ccc', '#91bfff']
    ink = '#59636e' if light else '#9ba9bb'
    step = width / (len(days) // 7)
    tile = step - (2 if mobile else 3)
    top = 46 if mobile else 52
    parts = [f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title">
<title id="title">{total} public contributions in the last year. {snapshot} snapshot.</title>
<style>
.active{{animation:breathe ease-in-out infinite}}
.caption{{animation:caption-fade 1.55s ease-out 1.5s both}}
.entrance{{animation:enter 2.5s cubic-bezier(.2,.7,.3,1) 2.7s both}}
.drift{{animation:scroll 60s linear 2s infinite}}
@keyframes breathe{{0%,100%{{opacity:.85}}50%{{opacity:1}}}}
@keyframes caption-fade{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes enter{{from{{opacity:0;transform:translateX(36px)}}to{{opacity:1;transform:translateX(0)}}}}
@keyframes scroll{{from{{transform:translateX(0)}}to{{transform:translateX(-{width}px)}}}}
@supports (-moz-appearance:none){{
  .entrance,.drift{{animation:none;opacity:1;transform:none}}
  .track-copy{{display:none}}
}}
@media(prefers-reduced-motion:reduce){{.active,.entrance,.drift,.caption{{animation:none;opacity:1;transform:none}}}}
</style>
<g class="caption">
<text x="4" y="23" font-family="monospace" font-size="{16 if mobile else 17}" fill="{ink}">{total} contributions</text>
<text x="{width-4}" y="23" text-anchor="end" font-family="monospace" font-size="{14 if mobile else 15}" fill="{ink}">past year</text>
</g>
<g class="entrance"><g class="drift"><g id="tile-grid">''']
    for index, (day, level) in enumerate(days):
        phase = crc32(day.encode())
        animation = f'class="active" style="animation-duration:{9+(phase % 501)/100:.2f}s;animation-delay:-{(phase % 14000)/1000:.3f}s"' if level else ''
        parts.append(f'<rect x="{(index//7)*step:.2f}" y="{top+(index%7)*step:.2f}" width="{tile:.2f}" height="{tile:.2f}" rx="1.5" fill="{colors[level]}" {animation}><title>{day or "Unused day"}</title></rect>')
    return ''.join(parts) + f'</g><use class="track-copy" href="#tile-grid" x="{width}" aria-hidden="true"/></g></g></svg>'
