#!/usr/bin/env python3
"""Offline consistency and syntax checks. Run after build_catalog.py."""
import json
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from collections import Counter
from email.utils import parsedate_to_datetime
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
import build_catalog
from build_catalog import registry

ROOT = Path(__file__).resolve().parents[1]


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids = []
        self.hrefs = []
        self.scripts = []
        self.current = None
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a:
            self.ids.append(a['id'])
        if 'href' in a:
            self.hrefs.append(a['href'])
        if tag == 'script':
            self.current = [a.get('type', 'text/javascript'), '']

    def handle_data(self, data):
        if self.current is not None:
            self.current[1] += data

    def handle_endtag(self, tag):
        if tag == 'script' and self.current is not None:
            self.scripts.append(self.current)
            self.current = None


def main():
    source = (ROOT/'index.html').read_text()
    data = registry(source)
    records = json.loads((ROOT/'finds.json').read_text())
    keys = [r['key'] for r in records]
    assert len(keys) == len(set(keys)) and keys
    assert data['randomKeys'] == keys
    dates = [datetime.fromisoformat(r['addedAt']) for r in records]
    assert dates == sorted(dates, reverse=True)
    for r in records:
        assert r['addedDate'] == datetime.fromisoformat(r['addedAt']).date().isoformat()
        assert r['source'] in re.findall(r'href="([^"]+)"', data['relics'][r['key']]['html'])
        assert '/rants/99/0126.html' not in data['relics'][r['key']]['html'], 'Known broken CamWorld path'
    all_routes = set(data['relics']) | {'random'}
    assert 'oracle' not in source.lower(), 'Removed feature must not return'
    assert set(re.findall(r'data-open="([^"]+)"', source)) <= all_routes
    for name, r in data['relics'].items():
        assert not r.get('tpl') or f'id="{r["tpl"]}"' in source, name
        assert set(re.findall(r'data-open="([^"]+)"', r.get('html',''))) <= all_routes
    for name in ('start', 'latest'):
        content = re.search(r'<template id="tpl-'+name+r'">(.*?)</template>', source, re.S)[1]
        actual = re.findall(r'data-open="([^"]+)"', content)
        actual = [k for k in actual if k in keys]
        assert actual == (keys[:5] if name == 'start' else keys), (name, actual)
        assert len(re.findall(r'class="added-date"',content)) == len(actual)
    collection_keys = []
    for name, r in data['relics'].items():
        if name.startswith('collection-'):
            members = re.findall(r'data-open="([^"]+)"', r['html'])
            assert members == sorted(members, key=keys.index), name
            collection_keys.extend(members)
    assert Counter(collection_keys) == Counter(keys), 'Each find must belong to exactly one collection'
    rss = ET.parse(ROOT/'feed.xml').getroot().find('channel')
    items = rss.findall('item')
    assert [i.findtext('link') for i in items] == [r['source'] for r in records]
    assert [parsedate_to_datetime(i.findtext('pubDate')) for i in items] == dates
    guids = [i.findtext('guid') for i in items]
    assert len(set(guids)) == len(keys)
    sitemap = ET.parse(ROOT/'sitemap.xml').getroot()
    assert len(sitemap) == len(keys) + 2
    for url in sitemap:
        loc = url[0].text
        path = loc.replace('https://theforgottenweb.com','')
        assert (ROOT/(path.strip('/') or 'index.html')).is_file(), loc
    count = 0
    for path in [ROOT/'index.html', ROOT/'catalog.html', *sorted((ROOT/'finds').glob('*.html'))]:
        p = Page(path.read_text())
        assert len(p.ids) == len(set(p.ids)), (path, 'duplicate IDs')
        for href in p.hrefs:
            if href.startswith('/') and not href.startswith('//'):
                target = href.split('#')[0].split('?')[0].strip('/') or 'index.html'
                assert (ROOT/target).is_file(), (path, href)
        for kind, text in p.scripts:
            if kind == 'application/ld+json':
                json.loads(text)
            else:
                with tempfile.NamedTemporaryFile(suffix='.js', mode='w') as f:
                    f.write(text)
                    f.flush()
                    subprocess.run(['node','--check',f.name],check=True,capture_output=True)
                count += 1
    print(f'PASS: {len(keys)} finds, 5 collections, {len(keys)+2} HTML pages, {len(keys)+2} sitemap URLs, RSS dates/order/GUIDs, all internal links and {count} JavaScript blocks.')


def future_addition_regression():
    """A synthetic fixture lives ONLY in a temporary directory, never the site."""
    import contextlib
    import copy
    import io
    original_root = build_catalog.ROOT
    with tempfile.TemporaryDirectory(prefix='forgotten-web-test-') as tmp:
        sandbox = Path(tmp)
        source = (ROOT/'index.html').read_text()
        data = registry(source)
        records = json.loads((ROOT/'finds.json').read_text())
        fixture = copy.deepcopy(records[0])
        fixture.update(key='test-fixture', title='Temporary regression fixture', addedAt='2099-01-01T12:00:00+00:00', addedDate='2099-01-01', addedCommit=None, source='https://example.invalid/test-fixture')
        relic = copy.deepcopy(data['relics'][records[0]['key']])
        relic['title'] = 'Find 9999 / regression.fixture'
        relic['html'] = relic['html'].replace(records[0]['source'], fixture['source'])
        source = source.replace('    const relics = {', '    const relics = {\n      "test-fixture":'+json.dumps(relic)+',',1)
        (sandbox/'index.html').write_text(source)
        (sandbox/'finds.json').write_text(json.dumps(records+[fixture]))
        (sandbox/'feed.xml').write_bytes((ROOT/'feed.xml').read_bytes())
        try:
            build_catalog.ROOT = sandbox
            with contextlib.redirect_stdout(io.StringIO()):
                build_catalog.main()
            result = (sandbox/'index.html').read_text()
            rebuilt = registry(result)
            assert rebuilt['randomKeys'][0] == 'test-fixture'
            for name in ('start','latest'):
                section = re.search(r'<template id="tpl-'+name+r'">(.*?)</template>',result,re.S)[1]
                actual = re.findall(r'<a href="#[^"]+" data-open="([^"]+)"',section)
                assert actual[0] == 'test-fixture', (name, actual)
                assert len(actual) == (5 if name == 'start' else len(records)+1)
            assert 'data-open="test-fixture"' in rebuilt['relics']['collection-web']['html']
            rss = ET.parse(sandbox/'feed.xml').getroot().find('channel').findall('item')
            assert len(rss) == len(records)+1 and rss[0].findtext('link') == fixture['source']
            assert (sandbox/'finds/test-fixture.html').is_file()
            before = {str(p):p.read_bytes() for p in sandbox.rglob('*') if p.is_file()}
            with contextlib.redirect_stdout(io.StringIO()):
                build_catalog.main()
            after = {str(p):p.read_bytes() for p in sandbox.rglob('*') if p.is_file()}
            assert before == after, 'Build must be reproducible'
        finally:
            build_catalog.ROOT = original_root
    print('PASS: future addition appears on every surface automatically; repeated build is byte-identical (temporary fixture only).')


if __name__ == '__main__':
    main()
    future_addition_regression()
