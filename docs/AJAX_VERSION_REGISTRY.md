# PARADIGMA ESFERA — Registro de Tema e Versão

- **ID permanente do tema:** AJAX
- **Nome:** ESFERA Mobile — AJAX Swipe Discovery
- **Versão de especificação:** AJAX-001
- **Data do registro:** 2026-10-25 (horário exato não aferido)
- **Status:** referência visual e requisitos aprovados; implementação completa e produção ainda não confirmadas.

## Conceito preservado
Interface mobile futurista azul-marinho e dourado, inspirada em padrões de descoberta de Netflix e Spotify, com identidade visual própria. Busca universal com autocomplete em todas as frentes (Educação, Serviços, Comércio e Expansão), cartões e vitrines horizontais navegáveis por gesto de dedo, rolagem vertical por categorias, AJAX/fetch para carregamento incremental sem refresh, telas Início → Resultados → Detalhe → link oficial de afiliado.

## Regras obrigatórias
1. Produtos e links reais somente de parceiros autorizados; jamais inventar cursos, preços, avaliações, vendas ou comissões.
2. Sincronização incremental de novos cursos a partir de fonte oficial autorizada, com validação de afiliação, atribuição, URL, categoria e deduplicação; bloquear publicação sem validação.
3. Adaptar a interface a celulares, acessibilidade e carregamento rápido; manter visual original e rollback.
4. Dashboard separa visitas/cliques de vendas e comissões confirmadas pela plataforma.
5. Mudanças passam por branch, testes, staging, Double Check e deploy controlado.

## Registro de versões
- AJAX-001 — 2026-10-25 — Especificação oficial do tema e template mobile aprovado pelo usuário. Sem deploy implícito.

Atualizar esta seção em cada nova versão com data, hora, commit, ambiente e resultado de testes.

## Regra arquitetural permanente — atualização de cursos sem deploy
- **Front estável:** tema visual aprovado, Werozinha oficial, busca textual, descoberta visual e trilhos de cartões AJAX permanecem desacoplados dos registros comerciais.
- **Fonte de verdade:** catálogo persistente de produtos afiliados no banco efetivo de produção, com ID de parceiro+produto, título, categoria, imagens autorizadas, idioma, URL oficial, autorização, verificação de atribuição, disponibilidade, timestamps e trilha de auditoria.
- **Ingestão:** worker agendado, webhook autenticado quando disponível ou importação autorizada; não presumir que a Hotmart ofereça endpoint de descoberta/afiliação com as permissões necessárias. Fazer paginação, retries com backoff, deduplicação, atualização e desativação de ofertas revogadas.
- **Publicação segura:** somente ofertas com evidência válida de autorização e atribuição; links não verificados ficam em quarentena e nunca são publicados. Revalidar expiração e revogação.
- **API de leitura:** /api/catalog/groups, /api/catalog/search?q= e /api/catalog/featured com paginação, ETag/cache curto e versão de dados; o front consome via fetch e atualiza cartões sem reload. Endpoints são contrato planejado, não presumir implementação.
- **Werozinha:** busca escrita e recomendações utilizam exatamente a mesma API de catálogo que as vitrines visuais; IA classifica intenção e não inventa produtos, preços, avaliações ou comissões.
- **Observabilidade:** registrar último sync, itens recebidos, aceitos, rejeitados, desativados, erros e saúde. Separar versão do código (AJAX-NNN) da revisão do catálogo (catalog_revision, sync_at).
- **Controle de mudança:** inserir/editar cursos autorizados não exige deploy; alterar schema, front, integração ou regras de negócio exige testes, staging, double check, canary e rollback.

## Evolução do registro
- AJAX-006 — 2026-10-25 — Código de busca visual e escrita unificado na branch, commit 3d26f054f457; testes e produção não confirmados.
- AJAX-007 — 2026-10-25 (horário exato não aferido) — Contrato arquitetural para catálogo dinâmico desacoplado de deploy; documentação somente, sem ativação do sincronizador.

## AJAX-008 — Release candidate e relatório de promoção
- **Data:** 2026-10-25; **horário de verificação:** não aferido com precisão.
- **Produção Render:** LIVE, commit 08328c7567e884a1c32617e9295d65dd1dd3d752 (PR #34); não contém necessariamente o AJAX-007.
- **Staging Render:** LIVE, commit 2980ef35221ca020eb07d27f448ef27e9f08a028 (PR #35); ainda não executa esta branch AJAX.
- **Branch de desenvolvimento:** feat/esfera-openai-intent-routing-20261024; AJAX-006 código commit 3d26f054f457, AJAX-007 especificação commit f243c13d3f22520475bdf9f8013d96fafdce83b9.
- **P0 security checks:** success no commit f243c13d3f22520475bdf9f8013d96fafdce83b9; não substitui testes HTTP, mobile, catálogo e integração.
- **Bloqueios GO LIVE comercial:** identidade oficial Werozinha ainda não integrada como mídia animada real; sync e banco de catálogo persistente não implementados; fonte autorizada Hotmart e atribuição não verificadas; fluxo comercial permanece fail-closed.
- **Gate de promoção:** resolver divergências de branch, testes de regressão e responsividade, deploy staging com health e testes reais; somente então promover main, canary/health e rollback.
- **Status:** documentação release candidate; NÃO implantado e NÃO liberado para vendas.
