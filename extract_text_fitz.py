import fitz

doc = fitz.open('Apostila_2021.pdf')

text = ''

for page in doc:
    text += page.get_text()

with open('full_text.txt', 'w', encoding='utf-8') as f:
    f.write(text)

print("Texto extraído e salvo em full_text.txt")