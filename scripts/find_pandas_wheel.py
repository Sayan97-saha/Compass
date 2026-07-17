"""Find pandas wheel compatible with Python 3.14 on PyPI and print top candidate URL."""
import json
import sys
from urllib.request import urlopen

try:
    with urlopen('https://pypi.org/pypi/pandas/json') as r:
        data = json.load(r)
except Exception as e:
    print('ERROR: failed to fetch PyPI data:', e)
    sys.exit(2)

releases = data.get('releases', {})
candidates = []
for ver, files in releases.items():
    for f in files:
        fn = f.get('filename', '')
        packagetype = f.get('packagetype', '')
        url = f.get('url')
        if packagetype != 'bdist_wheel' or not url:
            continue
        # prefer Windows wheels for win_amd64
        if 'win_amd64' in fn and ('cp314' in fn or 'py3' in fn):
            candidates.append((ver, fn, url))

# fallback: manylinux wheels that may work via pip on Windows (rare), include macosx
if not candidates:
    for ver, files in releases.items():
        for f in files:
            fn = f.get('filename', '')
            packagetype = f.get('packagetype', '')
            url = f.get('url')
            if packagetype != 'bdist_wheel' or not url:
                continue
            if ('cp314' in fn or 'py3' in fn) and ('manylinux' in fn or 'macosx' in fn):
                candidates.append((ver, fn, url))

candidates.sort(reverse=True)
if not candidates:
    print('NO_CANDIDATES')
    sys.exit(1)

# print top 3
for ver, fn, url in candidates[:3]:
    print(f'{ver} | {fn} | {url}')

# print the best url on last line prefixed with URL:
print('URL:' + candidates[0][2])
sys.exit(0)
