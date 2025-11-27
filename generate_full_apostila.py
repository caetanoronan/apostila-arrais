import fitz
import os
import html

PDF = 'Apostila_2021.pdf'
OUT = 'apostila_completa.html'
IMAGE_PREFIX = 'page_'

doc = fitz.open(PDF)
N = doc.page_count
print(f'PDF opened: {PDF}, pages={N}')

# find module start pages by searching for "1º MÓDULO", etc.
module_starts = {}
for i in range(N):
    page = doc.load_page(i)
    txt = page.get_text()
    lower = txt.lower()
    # check for module headings
    for m in range(1,6):
        key = f'{m}º módulo'
        if key in lower and m not in module_starts:
            module_starts[m] = i

# If detection failed for some module, try alternative pattern 'módulo –' with number
if len(module_starts) < 5:
    for i in range(N):
        page = doc.load_page(i)
        txt = page.get_text()
        lower = txt.lower()
        for m in range(1,6):
            key = f'{m}º m'
            if f'{m}º' in lower and 'módulo' in lower and m not in module_starts:
                module_starts[m] = i

# Ensure we have at least the modules; if not, approximate ranges
starts = [module_starts.get(i, None) for i in range(1,6)]
# sort by module number
for i, s in enumerate(starts, start=1):
    print(f'Module {i} start page: {s}')

# Create map of ranges
ranges = {}
sorted_items = sorted([(m, p) for m,p in module_starts.items()], key=lambda x: x[0])
for idx, (m,p) in enumerate(sorted_items):
    start = p
    end = doc.page_count-1
    if idx+1 < len(sorted_items):
        end = sorted_items[idx+1][1]-1
    ranges[m] = (start, end)

# If some modules missing, assign heuristically by splitting doc
if len(ranges) < 5:
    # fallback: split into 5 equal parts
    per = max(1, N // 5)
    ranges = {}
    for m in range(1,6):
        s = (m-1)*per
        e = (m*per -1) if m<5 else N-1
        ranges[m] = (s,e)

print('Ranges:', ranges)

# list of image files in cwd for quick lookup
all_images = [f for f in os.listdir('.') if f.startswith(IMAGE_PREFIX) and ('_img_' in f)]
images_by_page = {}
for img in all_images:
    parts = img.split('_')
    # expected format page_{page}_img_{index}.{ext}
    if len(parts) >= 3 and parts[1].isdigit():
        p = int(parts[1])
        images_by_page.setdefault(p, []).append(img)

# build improved, responsive HTML with TOC and collapsible sections
html_lines = []
html_lines.append('<!doctype html>')
html_lines.append('<html lang="pt-BR">')
html_lines.append('<head>')
html_lines.append('<meta charset="utf-8">')
html_lines.append('<meta name="viewport" content="width=device-width,initial-scale=1">')
html_lines.append('<title>Apostila Completa — Estruturada</title>')
html_lines.append('<style>')
html_lines.append('  :root{--maxw:1100px;--accent:#0b6efd;--muted:#556;}')
html_lines.append('  body{font-family:Arial,Helvetica,sans-serif;margin:0;padding:0;background:#f3f6fb;color:#111;}')
html_lines.append('  header{background:linear-gradient(90deg,#fff,#f7fbff);padding:1rem 1rem;border-bottom:1px solid #e6ecff} ') 
html_lines.append('  .wrap{max-width:var(--maxw);margin:1rem auto;padding:0 1rem;}')
html_lines.append('  h1{margin:.2rem 0;font-size:1.4rem} .lead{color:var(--muted)}')
html_lines.append('  .layout{display:grid;grid-template-columns:260px 1fr;gap:1rem}')
html_lines.append('  nav.toc{background:#fff;padding:1rem;border-radius:8px;box-shadow:0 1px 3px rgba(0,0,0,.06)}')
html_lines.append('  nav.toc ul{list-style:none;padding-left:0;margin:0} nav.toc a{display:block;padding:.35rem .4rem;border-radius:6px;color:var(--accent);text-decoration:none} nav.toc a:hover{background:#f1f7ff} ') 
html_lines.append('  main.content{min-height:60vh} section.module{background:#fff;padding:1rem;border-radius:8px;box-shadow:0 1px 4px rgba(0,0,0,.06);margin-bottom:1rem} ') 
html_lines.append('  .page{border-top:1px dashed #eee;padding-top:.6rem;margin-top:.6rem} .page h4{margin:.2rem 0} pre{white-space:pre-wrap;background:#f8f9fc;padding:.6rem;border-radius:6px;overflow:auto} img{max-width:100%;height:auto;border-radius:4px} ') 
html_lines.append('  .coll{cursor:pointer;background:#f7fbff;border:1px solid #eef6ff;padding:.4rem .6rem;border-radius:6px;margin-bottom:.6rem} .meta{font-size:.9rem;color:#666} ') 
html_lines.append('  @media(max-width:880px){.layout{grid-template-columns:1fr} nav.toc{position:sticky;top:0}}')
html_lines.append('</style>')
html_lines.append('</head><body>')
html_lines.append('<header><div class="wrap"><h1>Apostila Completa — Estruturada</h1><div class="lead">Versão organizada automatically. Use o sumário para navegar por módulos e páginas.</div></div></header>')
html_lines.append('<div class="wrap layout">')
html_lines.append('<nav class="toc" aria-label="Sumário da apostila">')
html_lines.append('<h3 style="margin-top:0">Sumário</h3>')
html_lines.append('<ul>')
for m in range(1,6):
    s,e = ranges[m]
    # guard against invalid ranges
    if s > e:
        html_lines.append(f'<li><a href="#module{m}">{m}º MÓDULO</a> <span class="meta">(páginas: - )</span></li>')
    else:
        html_lines.append(f'<li><a href="#module{m}">{m}º MÓDULO</a> <span class="meta">(páginas: {s+1}–{e+1})</span></li>')
html_lines.append('</ul>')
html_lines.append('<hr /><p style="font-size:.95rem;color:#444;margin:0">Links rápidos</p><ul><li><a href="material_acessivel.html">Tela resumida e acessível</a></li><li><a href="apostila_completa.html">Versão completa por páginas</a></li></ul>')
html_lines.append('</nav>')

html_lines.append('<main class="content">')
for m in range(1,6):
    s,e = ranges[m]
    html_lines.append(f'<section class="module" id="module{m}">')
    html_lines.append(f'<h2>{m}º MÓDULO</h2>')
    if s>e:
        html_lines.append('<p class="meta">Faixa de páginas não detectada automaticamente.</p>')
    else:
        html_lines.append(f'<p class="meta">Páginas {s+1} a {e+1}</p>')
        # collapse per page
        for p in range(s, e+1):
            page = doc.load_page(p)
            text = page.get_text()
            text = html.escape(text).strip()
            html_lines.append(f'<div class="page" id="p{p}">')
            html_lines.append(f'<h4>Pagina {p+1}</h4>')
            imgs = images_by_page.get(p, [])
            if imgs:
                for im in sorted(imgs):
                    html_lines.append(f'<figure><img src="{im}" alt="Imagem da página {p+1}"/><figcaption style="font-size:.9rem;color:#666">{im}</figcaption></figure>')
            if text:
                # provide a short excerpt and a collapsible full text
                excerpt = text[:800]
                safe_excerpt = excerpt.replace('\n','\n')
                html_lines.append(f'<div class="coll" onclick="this.nextElementSibling.style.display=(this.nextElementSibling.style.display==\'none\'? \'block\' : \'none\')">Mostrar texto (alternar)</div>')
                html_lines.append('<div style="display:none">')
                html_lines.append(f'<pre>{text}</pre>')
                html_lines.append('</div>')
            else:
                html_lines.append('<p><em>(sem texto extraído desta página)</em></p>')
            html_lines.append('</div>')
    html_lines.append('</section>')

html_lines.append('</main></div>')
html_lines.append('<script>')
html_lines.append('  // small helper to expand module from hash on load')
html_lines.append('  (function(){if(location.hash){var el=document.querySelector(location.hash); if(el) el.scrollIntoView();}})();')
html_lines.append('</script>')
html_lines.append('</body></html>')

with open(OUT, 'w', encoding='utf-8') as f:
    f.write('\n'.join(html_lines))

print(f'HTML gerado (organizado): {OUT}')
