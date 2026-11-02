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
        transform = (
            'translate(265 331) scale(.455)'
            if mobile else
            'translate(632 108.93474283390933) scale(.8131734092295182)'
        )
        art = (
            f'{START}<g id="profile-art" aria-hidden="true" '
            f'transform="{transform}" fill="{color}" opacity=".88">'
            '<text font-family="Consolas,monospace" font-size="16" '
            f'xml:space="preserve" style="animation:none;white-space:pre">{lines}'
            f'</text></g>{END}'
        )
        svg = file.read_text(encoding='utf-8')
        svg = re.sub(re.escape(START) + r'.*?' + re.escape(END), '', svg, flags=re.S)
        file.write_text(svg.replace('</svg>', art + '</svg>'), encoding='utf-8')


if __name__ == '__main__':
    main()
