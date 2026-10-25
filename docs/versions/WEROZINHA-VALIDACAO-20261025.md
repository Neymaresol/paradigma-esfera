# Plano de validação e liberação — Werozinha
Data/hora do registro: 2026-10-25 16:46 BRT (referência do pedido).
Versão: WEROZINHA-IDLE-CAROUSEL-V1; branch: feat/werozinha-carousel-idle-20261025.

## Entregue na branch
- Protótipo HTML isolado com layout responsivo, gestos temporários em ciclo de 5 s, pausa e busca local demonstrativa.
- Testes de contrato estáticos em tests/test_werozinha_prototype.py.
- Histórico de decisões em docs/versions/WEROZINHA-IDLE-CAROUSEL-V1.md.

## Gates antes de produção
1. Executar pytest -q tests/test_werozinha_prototype.py e registrar resultado CI.
2. Validar manualmente Chrome Android: foco no campo de busca, teclado aberto, sugestões, toque, layout do painel, pausa, gesto a cada 5 s e acessibilidade.
3. Substituir emojis por imagens individuais oficiais da personagem, otimizadas para web; confirmar direitos de uso.
4. Integrar chat a backend de IA com limites, proteção de credenciais e observabilidade.
5. Integrar catálogo e links reais somente com autorização, sem inventar atribuição de afiliado.
6. Verificar staging no Render, health, logs, rollback e canário; não realizar deploy direto em produção.
7. Preparar criativos e mensagens de divulgação; publicar apenas em contas conectadas e autorizadas após revisão de políticas, privacidade e links.

## Estado
Sem confirmação de CI, browser E2E, integração de IA, catálogo, afiliados, deploy ou publicação de anúncios. Não registrar vendas simuladas como reais.
