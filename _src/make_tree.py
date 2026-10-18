"""Build assets/tree.json from the master spreadsheet.

Privacy rule: anyone whose status is Living / Possibly living / unconfirmed is
shown publicly only as "Living relative (private)" with no name or dates —
except people who have chosen to be public (PUBLIC_LIVING).
"""
import json, re, sys, openpyxl

SRC = sys.argv[1] if len(sys.argv) > 1 else '/home/claude/tree/Kiefer_Family_Tree_updated.xlsx'
OUT = sys.argv[2] if len(sys.argv) > 2 else '../assets/tree.json'
PUBLIC_LIVING = {84: 'James Joseph (Jim) Blackburn', 83: 'James Herman Blackburn'}
ROOT = 20  # Dr. Herman Kiefer

wb = openpyxl.load_workbook(SRC, data_only=True)
ft = wb['Family Tree']
hdr = [c.value for c in ft[4]]
ix = {h: i for i, h in enumerate(hdr)}
rows = []
for r in ft.iter_rows(min_row=5, values_only=True):
    if r[0] is None: continue
    rows.append({h: r[i] for h, i in ix.items()})

def g(p, k): return p.get(k) or ''
people = {p['ID']: p for p in rows}
byname = {}
for p in rows: byname.setdefault(str(p['Full Name']).strip(), p['ID'])

def private(p):
    st = str(g(p, 'Status')).lower()
    return (st.startswith('living') or st.startswith('possibly')) and p['ID'] not in PUBLIC_LIVING

def parents_of(p):
    out = []
    for part in str(g(p, 'Parents')).split('&'):
        part = re.sub(r'\s*\(.*?\)\s*$', '', part.strip()) if part.strip().endswith(')') and part.strip() not in byname else part.strip()
        if part in byname: out.append(byname[part])
    return out

children = {}
for p in rows:
    for par in parents_of(p):
        children.setdefault(par, [])
        if p['ID'] not in children[par]: children[par].append(p['ID'])

def years(p):
    b, d = g(p, 'Birth Year'), g(p, 'Death Year')
    if b and d: return f"{b}–{d}"
    if b: return f"b. {b}"
    if d: return f"d. {d}"
    return ''

def spouses(p):
    out = []
    for nm in re.split(r';\s*', str(g(p, 'Spouse(s)'))):
        nm = nm.strip()
        if not nm: continue
        sid = byname.get(nm)
        sp = people.get(sid)
        if sp and private(sp): continue
        out.append(nm)
    return out

seen = set()
def node(pid):
    p = people[pid]; seen.add(pid)
    kids = sorted(children.get(pid, []), key=lambda k: (people[k].get('Birth Year') or 9999, k))
    kids = [k for k in kids if people[k].get('Role') in ('Descendant', 'You') and k not in seen]
    if private(p):
        n = {'id': pid, 'private': True, 'name': 'Living relative (private)', 'branch': g(p, 'Branch (Dr. Herman\'s child)')}
    else:
        n = {'id': pid, 'name': PUBLIC_LIVING.get(pid, p['Full Name']), 'years': years(p) if pid not in PUBLIC_LIVING else '',
             'spouse': spouses(p), 'branch': g(p, 'Branch (Dr. Herman\'s child)'),
             'place': g(p, 'Birth Place'), 'death_place': g(p, 'Death Place'),
             'mine': pid in (20, 60, 76, 78, 83, 84)}
    n['children'] = [node(k) for k in kids]
    return n

tree = node(ROOT)
ancestors = ['Dr. Conrad Kiefer (1798–1878) & Christine Friederika Schweykert (1800–1874)',
             'Dr. Ludwig Kiefer (1780–1843)', 'Joseph Kiefer (1747–1797)',
             'John Jacob Kiefer Jr. (1708–1788)', 'John Jacob Kiefer (1675–1744)',
             'Nicholas van Nidda, "von Kiefer zu Grötzingen" (c. 1650)']
def count(n): return 1 + sum(count(c) for c in n['children'])
json.dump({'root': tree, 'ancestors': ancestors, 'count': count(tree)}, open(OUT, 'w'), ensure_ascii=False)
print('people in tree:', count(tree))
