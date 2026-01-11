# 🔧 Guia Técnico - Manutenção e Expansão

## Para Desenvolvedores

### Arquitetura do Sistema

```
┌─────────────────────────────────────────────┐
│     Apostila_Multilingue.html               │
│  ┌──────────────────────────────────────┐   │
│  │  <header>                            │   │
│  │    - Selector de Idioma              │   │
│  │    - Toggle Dark Mode                │   │
│  ├──────────────────────────────────────┤   │
│  │  <nav>                               │   │
│  │    - 8 Abas (Tabs)                   │   │
│  ├──────────────────────────────────────┤   │
│  │  <main>                              │   │
│  │    - 8 Divs com tab-panes            │   │
│  │    - IDs para popular via JS         │   │
│  └──────────────────────────────────────┘   │
│    ↓ referencia                             │
│    translations.js                          │
│  ┌──────────────────────────────────────┐   │
│  │  translationsData = {                │   │
│  │    pt: { 300+ keys },                │   │
│  │    es: { 300+ keys },                │   │
│  │    en: { 300+ keys }                 │   │
│  │  }                                   │   │
│  └──────────────────────────────────────┘   │
└─────────────────────────────────────────────┘
```

### Fluxo de Funcionamento

```javascript
Usuário clica idioma
        ↓
changeLanguage(lang)
        ↓
1. Salva em localStorage
2. Atualiza botão ativo
        ↓
updateContent()
        ↓
Para cada chave em translationsData[currentLanguage]:
  - Busca elemento com id=chave
  - Atualiza innerHTML
        ↓
Página atualiza em tempo real
```

---

## 📝 Como Adicionar Nova Tradução

### Passo 1: Localizar onde adicionar em `translations.js`

```javascript
en: {
    // ... outras traduções ...
    
    // NOVO CONTEÚDO
    'nova-chave': 'English text here',
    'outro-termo': 'More english text'
}
```

### Passo 2: Adicionar em todos os 3 idiomas

```javascript
pt: {
    'nova-chave': 'Texto em português aqui',
    'outro-termo': 'Mais texto português'
}

es: {
    'nova-chave': 'Texto en español aquí',
    'outro-termo': 'Más texto español'
}

en: {
    'nova-chave': 'English text here',
    'outro-termo': 'More english text'
}
```

### Passo 3: Adicionar elemento HTML em `Apostila_Multilingue.html`

```html
<div id="nova-chave"></div>
<div id="outro-termo"></div>
```

### Pronto! 🎉
Quando `updateContent()` for chamado, o HTML será preenchido automaticamente.

---

## 🌍 Como Adicionar Novo Idioma

### Exemplo: Adicionar Francês

### Passo 1: Adicionar chave `fr` em `translations.js`

```javascript
const translationsData = {
    pt: { /* ... */ },
    es: { /* ... */ },
    en: { /* ... */ },
    
    // NOVO IDIOMA
    fr: {
        'header-title': 'Manuel Théorique pour Cours de Skipper Amateur',
        'tab-sumario': '📋 Table des Matières',
        // ... copiar todas as 300+ chaves em francês ...
    }
}
```

### Passo 2: Adicionar botão em HTML

```html
<!-- Antes tinha: -->
<button class="lang-btn active" data-lang="pt" onclick="changeLanguage('pt')">
    🇧🇷 Português
</button>
<button class="lang-btn" data-lang="es" onclick="changeLanguage('es')">
    🇪🇸 Español
</button>
<button class="lang-btn" data-lang="en" onclick="changeLanguage('en')">
    🇺🇸 English
</button>

<!-- Agora adicione: -->
<button class="lang-btn" data-lang="fr" onclick="changeLanguage('fr')">
    🇫🇷 Français
</button>
```

### Pronto! Francês está ativo.

---

## 🐛 Debugging

### Problema: Tradução não aparece

**Solução 1: Verificar se chave existe**
```javascript
// No console do navegador (F12):
console.log(translationsData.pt['sua-chave'])
// Se retornar undefined, a chave não existe
```

**Solução 2: Verificar se ID existe no HTML**
```javascript
// No console:
document.getElementById('sua-chave')
// Se retornar null, o elemento não existe
```

**Solução 3: Verificar se updateContent foi chamado**
```javascript
// No console:
updateContent()
// Executa manualmente
```

### Problema: localStorage não funciona

```javascript
// Testar localStorage:
localStorage.setItem('teste', 'ok')
localStorage.getItem('teste')  // Deve retornar 'ok'
localStorage.removeItem('teste')

// Se der erro, localStorage pode estar desabilitado
```

### Problema: Idioma não persiste

```javascript
// Verificar se está salvando:
localStorage.getItem('apostila-lang')
// Deve retornar 'pt', 'es' ou 'en'

// Forçar reset:
localStorage.removeItem('apostila-lang')
location.reload()
```

---

## 📊 Validar Integridade

### Checklist de Tradução

```python
# Script para validar que todas as chaves existem em todos idiomas

def validar_traducoes(translations_file):
    import json
    
    with open(translations_file) as f:
        data = json.load(f)
    
    pt_keys = set(data['pt'].keys())
    es_keys = set(data['es'].keys())
    en_keys = set(data['en'].keys())
    
    print(f"PT: {len(pt_keys)} chaves")
    print(f"ES: {len(es_keys)} chaves")
    print(f"EN: {len(en_keys)} chaves")
    
    # Chaves faltantes
    faltam_es = pt_keys - es_keys
    faltam_en = pt_keys - en_keys
    
    if faltam_es:
        print(f"⚠️ Faltam em ES: {faltam_es}")
    if faltam_en:
        print(f"⚠️ Faltam em EN: {faltam_en}")
    
    if not faltam_es and not faltam_en:
        print("✓ Todas as traduções estão completas!")
```

---

## 🎨 Customização de Estilo

### Mudar cores do tema

```css
/* Adicione ou modifique em Apostila_Multilingue.html */
:root {
    --primary-color: #2c3e50;      /* Azul escuro */
    --secondary-color: #3498db;    /* Azul claro */
    --accent-color: #e74c3c;       /* Vermelho */
    --text-color: #333;             /* Texto escuro */
    --background-color: #f9f9f9;   /* Fundo claro */
}
```

### Adicionar Dark Mode mais agressivo

```css
body.high-contrast {
    --primary-color: #1a1a1a;
    --text-color: #e0e0e0;
    --background-color: #0d0d0d;
}
```

### Mudar fonte

```css
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    /* Mude para sua fonte favorita */
}
```

---

## ⚡ Performance

### Otimizações Aplicadas:
- ✓ Sem requisições AJAX (tudo local)
- ✓ Sem biblioteca externas (vanilla JS)
- ✓ CSS crítico inline
- ✓ localStorage em vez de servidor

### Possíveis Melhorias:
- [ ] Minificar HTML/CSS/JS em produção
- [ ] Gzip compressão no servidor
- [ ] Cache buster para translations.js
- [ ] Service Worker para offline

### Tamanhos Atuais:
- HTML: ~40 KB
- CSS: ~10 KB (integrado no HTML)
- JavaScript: ~3 KB (integrado no HTML)
- translations.js: ~50 KB

**Total: ~103 KB**

---

## 🚀 Deploy

### Opção 1: Arquivo Local
```bash
# Abrir localmente
file:///caminho/para/Apostila_Multilingue.html
```

### Opção 2: Servidor Python
```bash
cd /caminho/do/projeto
python -m http.server 8000
# Acessar: http://localhost:8000/Apostila_Multilingue.html
```

### Opção 3: Servidor Node.js
```bash
npm install -g serve
cd /caminho/do/projeto
serve
```

### Opção 4: Servidor Web (Nginx/Apache)
```bash
# Copiar arquivos para /var/www/html/apostila/
cp Apostila_Multilingue.html /var/www/html/apostila/
cp translations.js /var/www/html/apostila/
# Acessar: http://seu-dominio.com/apostila/
```

### Opção 5: GitHub Pages
```bash
# Fazer push para branch 'gh-pages'
# Acessar: https://seu-usuario.github.io/seu-repo/
```

---

## 🔐 Segurança

### Considerações:
- ✓ Sem dados sensíveis em localStorage
- ✓ Sem requisições externas (seguro)
- ✓ Sem execução de código dinâmico
- ✓ HTML escapado corretamente

### Para o Futuro:
- [ ] Validar entrada se adicionar formulários
- [ ] HTTPS recomendado para produção
- [ ] CORS headers se adicionar APIs
- [ ] Rate limiting se adicionar backend

---

## 📚 Referências Técnicas

### Tecnologias Usadas:
- HTML5
- CSS3 (Flexbox, CSS Variables, Media Queries)
- Vanilla JavaScript (ES6)
- localStorage API

### Navegadores Suportados:
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+
- Opera 76+

### Compatibilidade:
- Desktop: ✓ 100%
- Tablet: ✓ 100%
- Mobile: ✓ 100%
- IE 11: ✗ Não suportado (localStorage OK, CSS Variables não)

---

## 🤝 Contribuindo

### Para adicionar conteúdo:
1. Fork do projeto
2. Edite `translations.js`
3. Teste em todos os 3 idiomas
4. Faça commit com mensagem clara
5. Abra Pull Request

### Convenções:
- Nomes de chaves: `mod[n]-[topico]` em lowercase
- Sem caracteres especiais nas chaves
- Traducoes completas em 3 idiomas
- Testar sempre antes de commit

---

## 📞 Suporte Técnico

### Checklist de Resolução de Problemas:

1. **Página não carrega**
   - [ ] HTML existe?
   - [ ] translations.js na mesma pasta?
   - [ ] Arquivo não está corrompido?
   - [ ] Servidor web rodando?

2. **Tradução não aparece**
   - [ ] Chave existe em translations.js?
   - [ ] ID existe no HTML?
   - [ ] updateContent() foi chamado?
   - [ ] Console sem erros?

3. **localStorage não funciona**
   - [ ] Navegador suporta?
   - [ ] Modo privado/incógnito?
   - [ ] Limite de espaço?
   - [ ] Domínio diferente?

4. **Estilo quebrado**
   - [ ] CSS carregou?
   - [ ] Conflito com extensões?
   - [ ] Zoom do navegador normal?
   - [ ] Cache do navegador?

---

## 🎓 Recursos para Aprender Mais

- [MDN - HTML](https://developer.mozilla.org/en-US/docs/Web/HTML)
- [MDN - CSS](https://developer.mozilla.org/en-US/docs/Web/CSS)
- [MDN - JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
- [MDN - localStorage](https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage)

---

**Atualizado em**: Janeiro 2026  
**Versão**: 1.0  
**Mantido por**: Central de Aventuras
