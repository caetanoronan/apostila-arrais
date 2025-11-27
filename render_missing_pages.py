import fitz
import re
import os

# Build list of missing referenced images by scanning HTML files
root = os.path.dirname(__file__)
assets_dir = os.path.join(root, 'assets')

missing = set()
pattern = re.compile(r'assets/(page_(\d+)_img_\d+\.(?:png|jpeg|jpg))')
for fname in os.listdir(root):
    if fname.endswith('.html'):
        with open(os.path.join(root, fname), 'r', encoding='utf-8') as f:
            txt = f.read()
            for match in pattern.findall(txt):
                imgfile = match[0]
                assetpath = os.path.join(assets_dir, imgfile)
                if not os.path.exists(assetpath):
                    missing.add(imgfile)

if not missing:
    print('No missing assets found')
    exit(0)

print('Missing assets to render:')
for m in sorted(missing):
    print('-', m)

# Render the PDF pages for each missing asset
pdf_path = os.path.join(root, 'Apostila_2021.pdf')
if not os.path.exists(pdf_path):
    print('PDF not found:', pdf_path)
    exit(1)

print('Rendering pages from PDF: ', pdf_path)
doc = fitz.open(pdf_path)

for imgfile in missing:
    page_idx = int(re.search(r'page_(\d+)_img_', imgfile).group(1))
    if page_idx < 0 or page_idx >= len(doc):
        print(f"Page index out of range for {imgfile}, idx={page_idx}")
        continue

    page = doc.load_page(page_idx)
    mat = fitz.Matrix(2.0, 2.0)  # 2x zoom for better quality
    pix = page.get_pixmap(matrix=mat, alpha=False)
    outpath = os.path.join(assets_dir, imgfile)
    pix.save(outpath)
    print('Rendered', outpath)

print('Done.')
