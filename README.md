# Semana Especial Vida que Eleva · IASD Tingui

Quarta 11 a sábado 14/11/2026 · 20h (sábado a partir das 9h15) · Pr. Gilmar
Igreja Adventista do Tingui · Rua Guilherme Ihlenfeldt, 778, Curitiba

## Site
- `index.html` (inscrição), `obrigado.html` (dispara o evento Lead do Pixel), `privacidade.html`
- Publicação: GitHub Pages em https://guilherme-filipak-galtgrowthmkt.github.io/vida-que-eleva-tingui/
- Pixel da Meta: 1290472262966621 (o mesmo da conta CA01 - IASD Tingui)
- `obrigado.html`: preencher `WHATSAPP_GROUP_URL` com o link do grupo; vazio, a página só confirma a inscrição.

## Planilha
- [Inscrições · Vida que Eleva · IASD Tingui](https://docs.google.com/spreadsheets/d/1Ob0YqRD0EqWkAyL7hh9lnHl3JKC85n-BTHKAwwFyyv4/edit)
- O formulário usa o mesmo Web App do Apps Script do Encontro de Casais (`../Casais/apps-script/Code.gs`).
  O campo `evento=vida-que-eleva` faz o script gravar nesta planilha.

## Campanha na Meta
- Script: `meta/criar_campanha.py` (cria tudo pausado; IDs em `meta/ids.json`)
- Campanha `[LEADS] Vida que Eleva Tingui | 07-11/11`, CBO R$ 66,67/dia, sem data de término
  (R$ 300 ÷ 4,5 dias, de sáb 07/11 00h até qua 11/11 12h). Pausar na quarta ao meio-dia.
- Conjunto Adv+ aberto (2 km da igreja, 18-65): vídeos v1, v2, v4
- Conjunto Remarketing `[SITE] [TODOS] - 30D` (2 km): vídeo v3
- Transcrições dos vídeos em `criativos/v*.txt`. Os .MOV e o banner em PDF ficam fora do Git.
