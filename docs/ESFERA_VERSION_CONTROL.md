# PARADIGMA ESFERA — Controle de versão
Versão candidata: **v1.4.0-visual-rc1**
Registrada em: **2026-10-24 21:45 America/Sao_Paulo** (referência aproximada; timestamps GitHub são autoritativos)
Branch: `fix/esfera-futuristic-home-search-20261024`
PR: https://github.com/Neymaresol/paradigma-esfera/pull/29
Status: **candidata em revisão, não é versão de produção confirmada**

## Contrato visual
- Fonte canônica: `esfera_prototipo.html`
- Rotas: `/`, `/esfera`
- Visual obrigatório: neon azul e dourado, IA Central, coroa, Educação, Serviços, Comércio, Expansão, cinco indicadores de controle.
- A busca `/descobrir` deve ser integrada à homepage sem substituí-la.
- Arquivo de referência: `docs/ESFERA_VISUAL_CANONICAL.md`

## Proteção automática
- Workflow `.github/workflows/esfera-visual-regression.yml` roda em PRs para main e pushes na main.
- Testes `tests/test_esfera_visual_regression.py` validam os textos/estrutura essenciais e navegação.
- **Limitação:** são testes estruturais, não comparação automática de pixels. Exigir screenshots e revisão visual antes de produção.

## Gate de implantação
1. Testes verdes e PR revisado.
2. Merge na main; aguardar staging LIVE, health, logs e smoke tests.
3. Verificar homepage em desktop e celular e comparar com imagens de referência.
4. Liberar produção somente após aprovação e Double Check.
5. Registrar commit efetivo de produção, timestamp e health; guardar commit anterior para rollback.

## Histórico
- v1.3.1-dev: base anterior do serviço (não confundir com versão de deploy).
- v1.4.0-visual-rc1: homepage futurista com pesquisa integrada e contrato de regressão (PR #29).
