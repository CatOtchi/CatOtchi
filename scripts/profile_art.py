"""Place the supplied lying-cat text art in the profile bio assets."""

from html import escape
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
START = '<!-- profile-art:start -->'
END = '<!-- profile-art:end -->'


def main():
    rows = (ROOT / 'assets/lying-cat.txt').read_text(encoding='utf-8').splitlines()
    lines = ''.join(
        f'<tspan x="0" y="{i * 16}">{escape(row)}</tspan>'
        for i, row in enumerate(rows)
    )
    for file in (ROOT / 'assets').glob('bio-*.svg'):
        mobile = 'mobile' in file.name
        dark = 'dark' in file.name
        color = '#91bfff' if dark else '#0969da'
        delay = '3.4s' if mobile else '2.9s'
        distance = '12px' if mobile else '18px'
        transform = (
            'translate(252 323) scale(.50)'
            if mobile else
            'translate(615 109) scale(.90)'
        )
        art = (
            f'{START}<style>'
            f'.cat-arrival{{animation:cat-enter 1.55s cubic-bezier(.2,.7,.3,1) {delay} both}}'
            f'@keyframes cat-enter{{from{{opacity:0;transform:translateX({distance})}}'
            'to{opacity:1;transform:translateX(0)}}'
            '@supports (-moz-appearance:none){.cat-arrival{animation-name:cat-fade;transform:none}}'
            '@keyframes cat-fade{from{opacity:0}to{opacity:1}}'
            '@media(prefers-reduced-motion:reduce){.cat-arrival{animation:none;opacity:1;transform:none}}'
            '</style><g id="profile-art" aria-hidden="true" '
            f'transform="{transform}" fill="{color}" opacity=".88">'
            '<g class="cat-arrival">'
            '<text font-family="Consolas,monospace" font-size="16" '
            f'xml:space="preserve" style="animation:none;white-space:pre">{lines}'
            f'</text></g></g>{END}'
        )
        svg = file.read_text(encoding='utf-8')
        svg = re.sub(re.escape(START) + r'.*?' + re.escape(END), '', svg, flags=re.S)
        file.write_text(svg.replace('</svg>', art + '</svg>'), encoding='utf-8')


if __name__ == '__main__':
    main()
