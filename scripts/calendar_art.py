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
    total = re.search(r'(\d[\d,]*)\s+contributions\s+in the last year', source).group(1)
    snapshot = re.search(r'data-to="(\d{4}-\d{2}-\d{2})', source).group(1)
    width, height = (420, 130) if mobile else (900, 190)
    colors = ['#ebedf0', '#b8d4fb', '#79b2f8', '#438de6', '#0969da'] if light else ['#161b22', '#142b4b', '#22538b', '#397ccc', '#91bfff']
    ink = '#59636e' if light else '#9ba9bb'
    step = width/53
    tile = step-2 if mobile else step-3
    top = 46 if mobile else 52
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title"><title id="title">{total} public contributions in the last year. {snapshot} snapshot.</title><style>.active{{animation:breathe ease-in-out infinite}}@keyframes breathe{{0%,100%{{opacity:.62}}50%{{opacity:1}}}}@media(prefers-reduced-motion:reduce){{.active{{animation:none;opacity:1}}}}</style><text x="4" y="23" font-family="monospace" font-size="{16 if mobile else 17}" fill="{ink}">{total} contributions</text><text x="{width-4}" y="23" text-anchor="end" font-family="monospace" font-size="{14 if mobile else 15}" fill="{ink}">past year</text>']
    parts.append(f'<style>.drift{{animation:scroll 60s linear infinite}}.column{{animation:column-in 1.1s cubic-bezier(.2,.7,.3,1) both}}@keyframes scroll{{from{{transform:translateX(0)}}to{{transform:translateX(-{width}px)}}}}@keyframes column-in{{from{{opacity:0;transform:translateX(36px)}}to{{opacity:1;transform:translateX(0)}}}}@media(prefers-reduced-motion:reduce){{.column,.drift{{animation:none;opacity:1;transform:none}}}}</style><g class="drift"><g id="tile-grid">')
    for index, (day, level) in enumerate(days):
        phase = crc32(day.encode())
        animation = f'class="active" style="animation-duration:{6+(phase % 301)/100:.2f}s;animation-delay:-{(phase % 9000)/1000:.3f}s"' if level else ''
        parts.append(f'<g class="column" style="animation-delay:{.35+(index//7)*.014:.3f}s"><rect x="{(index//7)*step:.2f}" y="{top+(index%7)*step:.2f}" width="{tile:.2f}" height="{tile:.2f}" rx="1.5" fill="{colors[level]}" {animation}><title>{day}</title></rect></g>')
    return ''.join(parts) + f'</g><use href="#tile-grid" x="{width}" aria-hidden="true"/></g></svg>'
