from hashlib import sha256
from pathlib import Path
import re
import urllib.request

from calendar_art import blue_calendar

root = Path(__file__).resolve().parents[1]
request = urllib.request.Request('https://github.com/users/CatOtchi/contributions', headers={'User-Agent':'CatOtchi-profile-calendar'})
with urllib.request.urlopen(request, timeout=30) as response:
    source = response.read().decode('utf-8')
if source.count('data-date=') < 350:
    raise ValueError('GitHub did not return a full contribution calendar')
readme = root / 'README.md'
text = readme.read_text(encoding='utf-8')
for theme in ['dark', 'light']:
    for size in ['desktop', 'mobile']:
        filename = f'calendar-{theme}-{size}.svg'
        content = blue_calendar(source, mobile=size == 'mobile', light=theme == 'light').encode('utf-8')
        (root / 'assets' / filename).write_bytes(content)
        version = sha256(content).hexdigest()[:12]
        text = re.sub(
            rf'(\./assets/{re.escape(filename)})(?:\?v=[a-zA-Z0-9]+)?(?=")',
            rf'\g<1>?v={version}',
            text,
        )
total = re.search(r'(\d[\d,]*)\s+contributions\s+in the last year', source).group(1)
snapshot = re.search(r'data-to="(\d{4}-\d{2}-\d{2})', source).group(1)
text = re.sub(r'alt="[\d,]+ public contributions in the last year\. Contribution snapshot from [^"]+"', f'alt="{total} public contributions in the last year. Contribution snapshot from {snapshot}."', text)
readme.write_bytes(text.encode('utf-8'))
print(f'Updated public contribution calendar: {total} contributions, {snapshot}')
