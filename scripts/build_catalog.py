#!/usr/bin/env python3
"""Rebuild discovery-ordered lists, RSS and crawlable pages from finds.json.

finds.json records first-addition dates verified against Git. For a new find,
add its metadata (including addedAt) here as well as the normal relic registry.
Original publication dates are historical metadata, never the sorting key.
Run: python3 scripts/build_catalog.py
"""
import html
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://theforgottenweb.com'
ET.register_namespace('atom', 'http://www.w3.org/2005/Atom')


def registry(source):
    start = source.index('    const relics =')
    end = source.index('    const main =', start)
    # Evaluate only the data declarations, not application/browser code.
    code = source[start:end] + '; console.log(JSON.stringify({relics,randomKeys}));'
    return json.loads(subprocess.check_output(['node', '-e', code], text=True))


def rows_ordered(fragment, desired_keys, metadata, fallback=None):
    pattern = r'<div class="find">.*?</div><span class="badge[^>]*>.*?</span></div>'
    rows = list(re.finditer(pattern, fragment, re.S))
    assert rows, 'Missing finds container'
    existing = {re.search(r'data-open="([^"]+)"', row[0])[1]: row[0] for row in rows}
    new_rows = []
    for key in desired_keys:
        record = metadata[key]
        text = existing.get(key) or (fallback or {}).get(key)
        if text is None:
            year = str(datetime.strptime(record['originalPublicationDate'], '%a, %d %b %Y %H:%M:%S %z').year)
            archived = 'web.archive.org/' in record['source']
            status = 'archive copy' if archived else 'original online'
            css = 'status-archived' if archived else 'status-live'
            text = f'<div class="find"><span class="year">{year}</span><div><a href="#{key}" data-open="{key}">{html.escape(record["title"])}</a><p>{html.escape(record["description"])}</p></div><span class="badge {css}">{status}</span></div>'
        text = re.sub(r'<small class="added-date">.*?</small>', '', text, flags=re.S)
        date = record['addedDate']
        stamp = f'<small class="added-date">Added <time datetime="{date}">{date}</time></small>'
        text = text.replace('</a><p>', '</a>' + stamp + '<p>', 1)
        new_rows.append(text)
    return fragment[:rows[0].start()] + '\n      '.join(new_rows) + fragment[rows[-1].end():]


def page(title, description, canonical, body, structured=None):
    ld = '' if structured is None else '<script type="application/ld+json">' + json.dumps(structured, ensure_ascii=False).replace('</', '<\\/') + '</script>'
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} — The Forgotten Web</title><meta name="description" content="{html.escape(description, quote=True)}">
<link rel="canonical" href="{canonical}"><meta name="robots" content="index,follow">
<link rel="alternate" type="application/rss+xml" title="The Forgotten Web RSS" href="{BASE}/feed.xml">
<style>body{{margin:0;background:#ff00ff;color:#24152a;font:16px/1.6 Georgia,serif}}main{{max-width:820px;margin:32px auto;padding:24px;background:#fff9d8;border:3px solid #24152a;box-shadow:8px 8px #7e3f79}}h1,h2,nav,.sysline,small,dt{{font-family:Geneva,Tahoma,sans-serif}}nav{{display:flex;gap:18px;flex-wrap:wrap;margin-bottom:24px}}a{{color:#005bd8;overflow-wrap:anywhere}}li{{margin:0 0 22px}}small,.sysline{{display:block;font-size:13px}}.button-row{{display:flex;gap:16px;flex-wrap:wrap}}.meta-cell{{margin:8px 0}}.meta-cell b{{margin-right:8px}}blockquote{{border-left:4px solid #24152a;padding-left:16px}}@media(max-width:880px){{main{{margin:16px;padding:16px}}}}</style>{ld}</head><body><main>{body}</main></body></html>
'''


def main():
    source = (ROOT / 'index.html').read_text()
    data = registry(source)
    records = json.loads((ROOT / 'finds.json').read_text())
    # Stable ordering within the launch batch; addedAt is always authoritative.
    records.sort(key=lambda r: datetime.fromisoformat(r['addedAt']), reverse=True)
    keys = [r['key'] for r in records]
    registry_keys = {k for k, r in data['relics'].items() if r['title'].startswith('Find ')}
    assert set(keys) == registry_keys and len(keys) == len(set(keys))
    metadata = {r['key']: r for r in records}
    (ROOT / 'finds.json').write_text(json.dumps(records, ensure_ascii=False, indent=2) + '\n')
    for r in records:
        assert r['addedDate'] == datetime.fromisoformat(r['addedAt']).date().isoformat()
        assert r['source'] in re.findall(r'href="([^"]+)"', data['relics'][r['key']]['html']), r['key']
    latest_template = re.search(r'<template id="tpl-latest">(.*?)</template>', source, re.S)[1]
    row_pattern = r'<div class="find">.*?</div><span class="badge[^>]*>.*?</span></div>'
    fallback = {re.search(r'data-open="([^"]+)"', row)[1]:row for row in re.findall(row_pattern, latest_template, re.S)}
    for name in ('start', 'latest'):
        pattern = r'(<template id="tpl-' + name + r'">)(.*?)(</template>)'
        wanted = keys[:5] if name == 'start' else keys
        source = re.sub(pattern, lambda m: m[1] + rows_ordered(m[2], wanted, metadata, fallback) + m[3], source, flags=re.S)
    # Every find belongs to exactly one category, including future additions.
    categories = {'web':'web architecture', 'culture':'pre-platform culture', 'programming':'old programming blogs', 'markets':'markets that aged well', 'weird':'weird useful corners'}
    assert all(r['category'] in categories.values() for r in records)
    for key, r in data['relics'].items():
        if not key.startswith('collection-'):
            continue
        wanted = [rec['key'] for rec in records if rec['category'] == categories[key.removeprefix('collection-')]]
        r['html'] = rows_ordered(r['html'], wanted, metadata, fallback)
        for field in ('status', 'preview'):
            r[field] = re.sub(r'\d+ finds', f'{len(wanted)} finds', r[field])
        line = r'(?m)^      ' + re.escape("'"+key+"'") + r':.*$'
        source, count = re.subn(line, lambda _: "      '" + key + "':" + json.dumps(r, ensure_ascii=False) + ',', source)
        assert count == 1, key
    source = re.sub(r'    const randomKeys = .*?;', '    const randomKeys = ' + json.dumps(keys) + ';', source)
    source = source.replace('/latest-finds · newest finds first', '/latest-finds · newest additions first · original years shown separately')
    if '.added-date{' not in source:
        source = source.replace('  </style>', '    .added-date{display:block;margin-top:5px;font:11px/1.5 Geneva,Tahoma,sans-serif;color:var(--muted);}\n  </style>', 1)
    inline = '    const findDates = ' + json.dumps({r['key']:r['addedDate'] for r in records}) + ';'
    if '    const findDates = ' in source:
        source = re.sub(r'    const findDates = .*?;', lambda _: inline, source)
    else:
        source = source.replace('    const main =', inline + '\n    const main =', 1)
    if 'findDates[safeKey]' not in source:
        source = source.replace('      prepareInternalLinks();', '''      if(findDates[safeKey]){
        const date = findDates[safeKey];
        const stamp = document.createElement('div');
        stamp.className = 'sysline';
        stamp.innerHTML = `Added to The Forgotten Web: <time datetime="${date}">${date}</time> · original publication shown below`;
        main.prepend(stamp);
      }
      prepareInternalLinks();''', 1)
    # A normal HTML link makes every find discoverable even without executing JS.
    if 'href="/catalog.html"' not in source:
        source = source.replace('  <template id="tpl-start">', f'  <p style="text-align:center"><a href="/catalog.html">Complete archive index · all {len(records)} finds by date added</a></p>\n  <noscript><p>JavaScript is disabled. <a href="/catalog.html">Browse the full archive and original sources here.</a></p></noscript>\n\n  <template id="tpl-start">', 1)
    source = source.replace('mailto:winston.kilby@gmail.com', 'mailto:winstonkilby@gmail.com')
    source = re.sub(r'full archive has \d+', f'full archive has {len(records)}', source)
    source = re.sub(r'Complete archive index · all \d+ finds', f'Complete archive index · all {len(records)} finds', source)
    source = re.sub(r'\d+ world-class finds ready', f'{len(records)} world-class finds ready', source)
    source = re.sub(r'\d+ items / no infinite scroll', f'{len(records)} items / no infinite scroll', source)
    source = re.sub(r'Five collection folders, now with [^<]+', f'Five collection folders, now with {len(records)} carefully selected finds.', source)
    (ROOT / 'index.html').write_text(source)

    tree = ET.parse(ROOT / 'feed.xml')
    channel = tree.getroot().find('channel')
    items = channel.findall('item')
    previous_items = [ET.tostring(item, encoding='unicode') for item in items]
    by_link = {i.findtext('link'): i for i in items}
    for item in items:
        channel.remove(item)
    for r in records:
        item = by_link.get(r['source'])
        if item is None:
            item = ET.Element('item')
            for name, value in [('title',r['title']),('link',r['source']),('guid',BASE+'/finds/'+r['key']+'.html'),('pubDate',''),('description',''),('category',r['category'])]:
                ET.SubElement(item, name).text = value
            item.find('guid').set('isPermaLink','false')
        item.find('pubDate').text = format_datetime(datetime.fromisoformat(r['addedAt']))
        # Preserve original publication metadata and the existing GUID (no duplicates).
        description = r['description'] + ' Originally published: ' + r['originalPublicationDate'] + '. Added to The Forgotten Web: ' + r['addedDate'] + '.'
        item.find('description').text = description
        channel.append(item)
    if previous_items != [ET.tostring(item, encoding='unicode') for item in channel.findall('item')]:
        channel.find('lastBuildDate').text = format_datetime(datetime.now(timezone.utc))
    ET.indent(tree, space='  ')
    tree.write(ROOT / 'feed.xml', encoding='utf-8', xml_declaration=True)

    links = []
    for r in records:
        key = r['key']
        content = data['relics'][key]['html']
        content = re.sub(r'href="#([^"]+)"', lambda m: 'href="/#' + m[1] + '"', content)
        content = re.sub(r'<a([^>]*href="https?://[^>]*)(?<!/)>' , r'<a\1 target="_blank" rel="noopener noreferrer">', content)
        title = r['title']
        body = f'<nav><a href="/#'+key+'">Open in the retro OS</a><a href="/catalog.html">All finds</a><a href="/feed.xml">RSS</a></nav>'
        body += '<h1>' + html.escape(title) + '</h1><p>Added to The Forgotten Web: <time datetime="' + r['addedDate'] + '">' + r['addedDate'] + '</time>. Historical publication details follow.</p>'
        body += re.sub(r'<h2>.*?</h2>', '', content, count=1, flags=re.S)
        structured = {'@context':'https://schema.org','@type':'WebPage','name':title,'url':BASE+'/finds/'+key+'.html','description':r['description'],'dateCreated':r['addedAt'],'about':{'@type':'CreativeWork','name':title,'url':r['source']}}
        dest = ROOT / 'finds' / (key + '.html')
        dest.parent.mkdir(exist_ok=True)
        dest.write_text(page(title, r['description'], BASE+'/finds/'+key+'.html', body, structured))
        links.append('<li><a href="/finds/'+key+'.html">'+html.escape(title)+'</a><small>Added '+r['addedDate']+' · '+html.escape(r['category'])+'</small><p>'+html.escape(r['description'])+'</p></li>')
    structured = {'@context':'https://schema.org','@type':'CollectionPage','name':'The Forgotten Web — complete archive','url':BASE+'/catalog.html','mainEntity':{'@type':'ItemList','numberOfItems':len(records),'itemListElement':[{'@type':'ListItem','position':n,'url':BASE+'/finds/'+r['key']+'.html','name':r['title']} for n,r in enumerate(records,1)]}}
    body = '<nav><a href="/">Back to the retro OS</a><a href="/feed.xml">RSS</a></nav><h1>Complete archive index</h1><p>All '+str(len(records))+' finds, newest added first. Added dates refer to this archive, not the original work’s publication date. Dates were verified against the site’s Git history; launch-batch items share a date.</p><ol>'+''.join(links)+'</ol>'
    (ROOT / 'catalog.html').write_text(page('Complete archive index', f'All {len(records)} Forgotten Web finds in verified newest-added order, with original sources and publication context.', BASE+'/catalog.html', body, structured))
    urlset = ET.Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
    for path in ['/', '/catalog.html'] + ['/finds/'+k+'.html' for k in keys]:
        url = ET.SubElement(urlset, 'url')
        ET.SubElement(url, 'loc').text = BASE+path
    ET.indent(urlset, space='  ')
    ET.ElementTree(urlset).write(ROOT/'sitemap.xml', encoding='utf-8', xml_declaration=True)
    (ROOT/'robots.txt').write_text('User-agent: *\nAllow: /\n\nSitemap: '+BASE+'/sitemap.xml\n')
    print(f'Built {len(records)} finds, discovery-ordered lists and RSS, catalog, sitemap and robots.txt.')


if __name__ == '__main__':
    main()
