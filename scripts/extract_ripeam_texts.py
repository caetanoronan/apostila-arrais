"""
Extrai texto de todos os PDFs que comecem com 'RIPEAM' no diretório atual
Salva cada PDF como <basename>.txt em UTF-8.
Tenta usar PyMuPDF (fitz) e recai para PyPDF2 se necessário.
"""
import os
import sys

PDF_PREFIX = 'RIPEAM'

files = [f for f in os.listdir('.') if f.lower().endswith('.pdf') and f.startswith(PDF_PREFIX)]
if not files:
    print('Nenhum PDF RIPEAM encontrado no diretório atual.')
    sys.exit(0)

for pdf in files:
    txt_name = os.path.splitext(pdf)[0] + '.txt'
    print(f'Processando: {pdf} -> {txt_name}')
    try:
        import fitz
        doc = fitz.open(pdf)
        text_parts = []
        for page in doc:
            text_parts.append(page.get_text('text'))
        text = '\n\n'.join(text_parts)
    except Exception as e_fitz:
        print(f'PyMuPDF (fitz) não disponível ou falha ({e_fitz}), tentando PyPDF2...')
        try:
            import PyPDF2
            with open(pdf, 'rb') as fh:
                reader = PyPDF2.PdfReader(fh)
                text_parts = []
                for p in reader.pages:
                    try:
                        page_text = p.extract_text() or ''
                    except Exception:
                        page_text = ''
                    text_parts.append(page_text)
                text = '\n\n'.join(text_parts)
        except Exception as e_pdf2:
            print(f'PyPDF2 também não disponível ou falhou: {e_pdf2}')
            text = ''

    try:
        with open(txt_name, 'w', encoding='utf-8') as out:
            out.write(text)
        print(f'Arquivo salvo: {txt_name} (tamanho {os.path.getsize(txt_name)} bytes)')
    except Exception as e:
        print(f'Falha ao salvar {txt_name}: {e}')

print('Concluído.')
