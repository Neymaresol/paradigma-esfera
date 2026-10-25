# BACKUP E RECUPERAÇÃO — PARADIGMA ESFERA
Data de registro: 2026-10-24 (horário exato: consultar commit GitHub).
Status: procedimento documentado; backup externo automatizado ainda não configurado.

## Fontes preservadas
- Visual canônico: `esfera_prototipo.html`
- Contrato visual: `docs/ESFERA_VISUAL_CANONICAL.md`
- Versão: `docs/ESFERA_VERSION_CONTROL.md`
- Links recuperados: `data/hotmart_affiliate_links_recovered.json` (4 links, publicação bloqueada)
- Aplicação: `app.py`, `esfera_discovery.py`
- Testes: `tests/test_esfera_visual_regression.py`
- CI: `.github/workflows/esfera-visual-regression.yml`

## Política obrigatória
1. Antes de mudar qualquer link, salvar snapshot imutável (commit/tag) com timestamp.
2. Nunca substituir a lista inteira de afiliados por apenas um link. Fazer merge por `id`/URL e verificar contagem.
3. Validar schema e URLs; não gravar tokens, segredos ou dados pessoais no repositório.
4. Revisar o diff e executar testes antes do deploy; exigir contagem de links >= snapshot anterior, salvo remoção explicitamente autorizada.
5. Registrar commit em produção e manter rollback para versão anterior.
6. Criar cópia independente do GitHub em armazenamento seguro; sem isso há apenas versionamento no mesmo provedor.
7. Confirmar afiliação, destino e autorização antes de publicar ofertas. Nenhum backup é prova de vendas.

## Restauração
`git show <commit>:data/hotmart_affiliate_links_recovered.json` recupera o arquivo no commit.
`git show <commit>:esfera_prototipo.html` recupera a página canônica.
Restaurar primeiro em branch e staging, comparar, só depois promover para produção.
