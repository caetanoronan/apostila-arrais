import fitz

doc = fitz.open('Apostila_2021.pdf')

for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    images = page.get_images(full=True)
    for img_index, img in enumerate(images):
        xref = img[0]
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]
        with open(f"page_{page_num}_img_{img_index}.{image_ext}", "wb") as img_file:
            img_file.write(image_bytes)

print("Imagens extraídas.")