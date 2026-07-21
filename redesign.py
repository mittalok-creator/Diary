import io, os, re

f = 'app/index.html'
s = open(f, encoding='utf-8').read()

# ============ 1. FONTS ============
old_link = '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">'
assert old_link in s, 'font link'
s = s.replace(old_link, '<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,600;12..96,700;12..96,800&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">')

# body rule -> body font var (anchor: font-size:15px)
old_body = "font-family:'Inter',system-ui,sans-serif; font-size:15px;"
assert old_body in s, 'body font rule'
s = s.replace(old_body, "font-family:var(--font-b); font-size:15px;", 1)

# all remaining Inter refs (quoted CSS + unquoted JS-inline) -> display font var
n1 = s.count("font-family:'Inter',system-ui,sans-serif")
s = s.replace("font-family:'Inter',system-ui,sans-serif", "font-family:var(--font-d)")
n2 = s.count("font-family:Inter,system-ui,sans-serif")
s = s.replace("font-family:Inter,system-ui,sans-serif", "font-family:var(--font-d)")
print('display-font refs converted:', n1, '+', n2)
assert 'Inter' not in s, 'Inter leftover: ' + repr(s[s.find("Inter")-60:s.find("Inter")+60])

# ============ 2. ROOT TOKENS (dark default -> VELVET IRIS) ============
old_root = """:root{
  color-scheme:dark;
  --ink0:#0B0E13; --ink1:#12161E; --ink2:#1A2029; --hair:#262F3C;
  --gold:#D9A85C; --goldb:#F0C27B; --plat:#C9B896;
  --hi:#F3EFE6; --lo:#8A93A3;
  --good:#5FBF8A; --warn:#E0A448; --risk:#D96C6C;"""
assert old_root in s, 'root tokens'
new_root = """:root{
  color-scheme:dark;
  --font-d:'Bricolage Grotesque',system-ui,sans-serif;
  --font-b:'Plus Jakarta Sans',system-ui,sans-serif;
  --ink0:#0C0B16; --ink1:#14131F; --ink2:#1C1A2C; --hair:#2D2B42;
  --gold:#8E93FF; --goldb:#B9BDFF; --plat:#A9ACD6;
  --hi:#F1F2FB; --lo:#8D93AC;
  --good:#53D392; --warn:#EFB454; --risk:#F27D7D;"""
s = s.replace(old_root, new_root)

# ambient aurora: iris top glow + faint cyan lower-right
old_amb = """  --amb:radial-gradient(900px 620px at 50% -14%,color-mix(in srgb,var(--gold) 9%,var(--ink0)) 0%,transparent 60%),
        radial-gradient(760px 520px at 108% 104%,color-mix(in srgb,var(--gold) 6%,var(--ink0)) 0%,transparent 58%);"""
assert old_amb in s, 'dark amb'
new_amb = """  --amb:radial-gradient(940px 640px at 50% -14%,color-mix(in srgb,var(--gold) 11%,var(--ink0)) 0%,transparent 60%),
        radial-gradient(780px 540px at 108% 104%,color-mix(in srgb,#4ED0E0 7%,var(--ink0)) 0%,transparent 58%);"""
s = s.replace(old_amb, new_amb)

old_glass = "--glass:rgba(11,14,19,.74);"
assert old_glass in s, 'glass'
s = s.replace(old_glass, "--glass:rgba(12,11,22,.72);")

# ============ 3. LIGHT THEME ============
old_light = """html[data-theme="light"]{
  color-scheme:light;
  --ink0:#F6F3EC; --ink1:#FFFFFF; --ink2:#F1ECE1; --hair:#E4DCCC;
  --gold:#946420; --goldb:#B98A44; --plat:#7E6B42;
  --hi:#171C24; --lo:#5C636F;
  --good:#2F855A; --warn:#B7791F; --risk:#C0392B;"""
assert old_light in s, 'light tokens'
new_light = """html[data-theme="light"]{
  color-scheme:light;
  --ink0:#F4F4FA; --ink1:#FFFFFF; --ink2:#ECECF6; --hair:#DFE0EE;
  --gold:#575CE5; --goldb:#7C81F2; --plat:#6E71A6;
  --hi:#15162B; --lo:#5D6178;
  --good:#1F9E6A; --warn:#B07A1F; --risk:#CC4444;"""
s = s.replace(old_light, new_light)

old_lglass = "--glass:rgba(246,243,236,.78);"
assert old_lglass in s, 'light glass'
s = s.replace(old_lglass, "--glass:rgba(244,244,250,.8);")

old_lfocus = "--focus:rgba(169,118,47,.14);"
if old_lfocus in s:
    s = s.replace(old_lfocus, "--focus:rgba(87,92,229,.14);")

# initial meta theme-color
s = s.replace('<meta name="theme-color" content="#0B0E13">', '<meta name="theme-color" content="#0C0B16">')

# ============ 4. ACCENT WARDROBE REFRESH (same keys, new hues) ============
acc_dark = [
 ('html[data-accent="emerald"]{--gold:#43A97E;--goldb:#74D0A8;--plat:#8FBFA8}',
  'html[data-accent="emerald"]{--gold:#3ECF9A;--goldb:#7FE7C0;--plat:#8FCDB4}'),
 ('html[data-accent="blue"]{--gold:#5B8DEF;--goldb:#93B8FF;--plat:#93A8C9}',
  'html[data-accent="blue"]{--gold:#4D9DF7;--goldb:#8CC3FF;--plat:#93AECF}'),
 ('html[data-accent="rose"]{--gold:#E0708F;--goldb:#F2A3B9;--plat:#C79AA8}',
  'html[data-accent="rose"]{--gold:#F0719A;--goldb:#FFA3C0;--plat:#CF9CAE}'),
 ('html[data-accent="violet"]{--gold:#9A7BE0;--goldb:#C0A6F2;--plat:#A79AC9}',
  'html[data-accent="violet"]{--gold:#A374F5;--goldb:#C6A6FF;--plat:#AC9CD6}'),
 ('html[data-accent="teal"]{--gold:#3BB3AC;--goldb:#7FD8D2;--plat:#8FBFBB}',
  'html[data-accent="teal"]{--gold:#2FC4C4;--goldb:#7FE3E0;--plat:#8FC7C4}'),
 ('html[data-accent="copper"]{--gold:#C97B4A;--goldb:#E5A57A;--plat:#BF9A85}',
  'html[data-accent="copper"]{--gold:#F08A4B;--goldb:#FFB283;--plat:#CFA189}'),
]
acc_light = [
 ('html[data-theme="light"][data-accent="emerald"]{--gold:#2E8A61;--goldb:#43A97E;--plat:#5E8A75}',
  'html[data-theme="light"][data-accent="emerald"]{--gold:#1F9E6A;--goldb:#3ECF9A;--plat:#4E8A72}'),
 ('html[data-theme="light"][data-accent="blue"]{--gold:#3B6BD1;--goldb:#5B8DEF;--plat:#5E729A}',
  'html[data-theme="light"][data-accent="blue"]{--gold:#2B7CE0;--goldb:#4D9DF7;--plat:#54719A}'),
 ('html[data-theme="light"][data-accent="rose"]{--gold:#C05174;--goldb:#E0708F;--plat:#9A6B7A}',
  'html[data-theme="light"][data-accent="rose"]{--gold:#D14E7E;--goldb:#F0719A;--plat:#9A6579}'),
 ('html[data-theme="light"][data-accent="violet"]{--gold:#7455C4;--goldb:#9A7BE0;--plat:#7A6B9A}',
  'html[data-theme="light"][data-accent="violet"]{--gold:#8250E8;--goldb:#A374F5;--plat:#75629E}'),
 ('html[data-theme="light"][data-accent="teal"]{--gold:#1F837C;--goldb:#3BB3AC;--plat:#5E8A87}',
  'html[data-theme="light"][data-accent="teal"]{--gold:#189A98;--goldb:#2FC4C4;--plat:#548987}'),
 ('html[data-theme="light"][data-accent="copper"]{--gold:#9E5426;--goldb:#C97B4A;--plat:#8A6B5E}',
  'html[data-theme="light"][data-accent="copper"]{--gold:#D96A2A;--goldb:#F08A4B;--plat:#8F6A54}'),
]
for old, new in acc_dark + acc_light:
    assert old in s, 'accent line: ' + old[:60]
    s = s.replace(old, new)

# settings swatch dots
dots = [
 ('linear-gradient(135deg,#D9A85C,#F0C27B)', 'linear-gradient(135deg,#8E93FF,#B9BDFF)'),
 ('linear-gradient(135deg,#43A97E,#74D0A8)', 'linear-gradient(135deg,#3ECF9A,#7FE7C0)'),
 ('linear-gradient(135deg,#5B8DEF,#93B8FF)', 'linear-gradient(135deg,#4D9DF7,#8CC3FF)'),
 ('linear-gradient(135deg,#E0708F,#F2A3B9)', 'linear-gradient(135deg,#F0719A,#FFA3C0)'),
 ('linear-gradient(135deg,#9A7BE0,#C0A6F2)', 'linear-gradient(135deg,#A374F5,#C6A6FF)'),
 ('linear-gradient(135deg,#3BB3AC,#7FD8D2)', 'linear-gradient(135deg,#2FC4C4,#7FE3E0)'),
 ('linear-gradient(135deg,#C97B4A,#E5A57A)', 'linear-gradient(135deg,#F08A4B,#FFB283)'),
]
for old, new in dots:
    assert old in s, 'dot: ' + old
    s = s.replace(old, new)

# accent display names
old_names = "const ACC_NAMES={gold:'Gold',emerald:'Emerald',blue:'Royal Blue',rose:'Rose',violet:'Violet',teal:'Teal',copper:'Copper'};"
assert old_names in s, 'ACC_NAMES'
s = s.replace(old_names, "const ACC_NAMES={gold:'Iris',emerald:'Jade',blue:'Azure',rose:'Ros\\u00e9',violet:'Amethyst',teal:'Lagoon',copper:'Ember'};")
n = s.count("||'Gold'")
s = s.replace("||'Gold'", "||'Iris'")
print("||'Gold' fallbacks updated:", n)
s = s.replace('id="accSub">Gold<', 'id="accSub">Iris<')

# ============ 5. COMPONENT POLISH (appended, deliberate final-cascade overrides) ============
POLISH = """/* ===== VELVET IRIS polish ===== */
nav button{position:relative;padding:7px 15px 6px;border-radius:15px;transition:color .18s,background .18s}
nav button.on{background:color-mix(in srgb,var(--gold) 13%,transparent)}
.btn{transition:transform .12s ease,box-shadow .2s ease,filter .2s ease}
.btn:active{transform:scale(.97)}
.btn-gold{box-shadow:0 8px 22px color-mix(in srgb,var(--gold) 26%,transparent),inset 0 1px 0 color-mix(in srgb,#fff 32%,transparent);color:#111126}
html[data-theme="light"] .btn-gold{color:#fff;box-shadow:0 8px 20px color-mix(in srgb,var(--gold) 30%,transparent)}
#toast{border-color:var(--hair);box-shadow:0 14px 36px rgba(0,0,0,.4),inset 0 1px 0 color-mix(in srgb,var(--gold) 14%,transparent)}
.eyebrow{letter-spacing:.17em}
"""
s = s.replace('</style>', POLISH + '</style>', 1)

# ============ 6. VERSION -> 12.0.0 (also un-freezes the stale 11.2.0 label) ============
old_ver = "const APP_VER='11.2.0';"
assert old_ver in s, 'APP_VER anchor (expected frozen 11.2.0)'
s = s.replace(old_ver, "const APP_VER='12.0.0';")

# structural checks
assert s.count('<div') == s.count('</div>'), 'div balance'
assert s.count('<button') == s.count('</button>'), 'button balance'
assert re.findall(r'\.nt th\{[^}]*position:sticky', s), 'sticky header intact'
assert 'Fraunces' not in s and 'Space Grotesk' not in s

tmp = f + '.tmp'
with io.open(tmp, 'w', encoding='utf-8') as fh:
    fh.write(s)
os.replace(tmp, f)
print('patched', f, len(s))
