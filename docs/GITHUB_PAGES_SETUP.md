# 📘 Como Configurar GitHub Pages

## Passo 1: Habilitar GitHub Pages

1. Vá até o repositório no GitHub: https://github.com/viniruggeri/humainze-java
2. Clique em **Settings** (Configurações)
3. Na sidebar esquerda, clique em **Pages**
4. Em **Source**, selecione:
   - Branch: `main`
   - Folder: `/docs`
5. Clique em **Save**

## Passo 2: Aguardar Deploy

O GitHub Pages levará ~1-2 minutos para fazer o deploy inicial.

Após o deploy, sua documentação estará disponível em:
```
https://viniruggeri.github.io/humainze-java/
```

## Passo 3: Verificar

Acesse a URL e verifique se a página inicial carrega corretamente.

## Estrutura de Arquivos

A pasta `docs/` contém:

```
docs/
├── index.html                   ← Página inicial (landing page)
├── _config.yml                  ← Configuração Jekyll
├── README.md                    ← Introdução da documentação
├── INDEX.md                     ← Índice completo
├── EXECUTIVE_SUMMARY.md         ← Sumário executivo
├── INTEGRATION_GUIDE_IA.md      ← Guia IA
├── INTEGRATION_GUIDE_IOT.md     ← Guia IoT
├── OTEL_INGESTION_ENDPOINTS.md  ← Endpoints OTLP
├── PAYLOAD_EXAMPLES.md          ← Exemplos de payloads
├── DASHBOARD_GUIDE.md             ← Dashboard Streamlit (porta 8501)
├── ALERTS_SYSTEM.md             ← Sistema de alertas
└── DEPLOY_AZURE.md              ← Deploy Azure VM
```

## Navegação

### URLs das Páginas

- **Home:** https://viniruggeri.github.io/humainze-java/
- **Introdução:** https://viniruggeri.github.io/humainze-java/README
- **Índice:** https://viniruggeri.github.io/humainze-java/INDEX
- **IA:** https://viniruggeri.github.io/humainze-java/INTEGRATION_GUIDE_IA
- **IoT:** https://viniruggeri.github.io/humainze-java/INTEGRATION_GUIDE_IOT
- **Alertas:** https://viniruggeri.github.io/humainze-java/ALERTS_SYSTEM
- **Deploy:** https://viniruggeri.github.io/humainze-java/DEPLOY_AZURE

## Atualizações

Para atualizar a documentação:

1. Edite os arquivos `.md` na pasta `docs/`
2. Commit e push:
   ```bash
   git add docs/
   git commit -m "docs: atualizar documentação"
   git push origin main
   ```
3. GitHub Pages redeployará automaticamente em ~1-2 minutos

## Temas Disponíveis

O tema atual é **Cayman** (definido em `_config.yml`).

Outros temas disponíveis:
- `jekyll-theme-minimal`
- `jekyll-theme-architect`
- `jekyll-theme-slate`
- `jekyll-theme-merlot`
- `jekyll-theme-time-machine`

Para trocar, edite `_config.yml`:
```yaml
theme: jekyll-theme-minimal
```

## Domínio Customizado (Opcional)

Se você tiver um domínio próprio:

1. No GitHub Pages settings, adicione seu domínio em **Custom domain**
2. Configure DNS do seu provedor:
   ```
   Type: CNAME
   Name: docs (ou @)
   Value: viniruggeri.github.io
   ```

## Troubleshooting

### Página 404

- Verifique se `/docs` está commitado e pushed
- Confirme que `index.html` ou `README.md` existe na raiz de `docs/`
- Aguarde 2-3 minutos após mudanças

### Markdown não renderiza

- Certifique-se que arquivos têm extensão `.md`
- Verifique sintaxe Markdown
- Adicione frontmatter se necessário:
  ```yaml
  ---
  layout: default
  title: Título da Página
  ---
  ```

### CSS não carrega

- Limpe cache do navegador (Ctrl+Shift+R)
- Verifique console do navegador por erros

## Links Úteis

- [Documentação GitHub Pages](https://docs.github.com/en/pages)
- [Jekyll Themes](https://pages.github.com/themes/)
- [Markdown Guide](https://www.markdownguide.org/)

---

**Status Atual:** ✅ Pronto para deployment  
**Última atualização:** 21/11/2025
