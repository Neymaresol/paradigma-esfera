# PARADIGMA ESFERA — Empresa digital assistida por IAs

Versão do plano: 1.0 · 2026-10-24 (data de elaboração; horário de produção deve ser obtido no Render).

## Missão
Criar, apresentar e divulgar sites, cursos e serviços digitais, com uma operação escalável, auditável e internacional. O plano não representa robôs já implantados.

## Orquestração
- IA Central: prioriza demandas, delega tarefas e mantém fila de trabalho.
- IA Frontend: HTML, CSS, JavaScript, acessibilidade, performance e responsividade.
- IA Backend: APIs, catálogo, banco de dados, autenticação e integrações.
- IA Designer: componentes, imagens autorizadas, identidade e UX.
- IA Educação: curadoria e revisão de cursos, disponibilidade e termos de oferta.
- Werozinha: orienta visitantes; informa claramente quando respostas são predefinidas ou geradas por IA.
- IA Marketing: SEO, páginas úteis, campanhas e parceiros com autorização.
- IA Comercial: eventos de visita, clique, conversão e reconciliação com fontes oficiais.
- IA Internacional: tradução, revisão humana e adequação de ofertas por país.
- IA Segurança/QA: revisão de dependências, testes, CSP, autorização, rollback e Double Check.

## Fluxo de trabalho
1. Detectar demanda por fontes públicas ou solicitação expressa do cliente.
2. Criar briefing e proposta de página/campanha, sem coletar pesquisas privadas.
3. Gerar versão em branch de desenvolvimento; testar conteúdo, links, acessibilidade, performance e segurança.
4. Publicar em staging; conferir funcionamento no celular.
5. Exigir aprovação e evidência da autorização de afiliado e da oferta antes de publicar.
6. Implantar por canary e health checks, preservando rollback.
7. Monitorar dados verificados, produzir recomendações e abrir nova proposta de melhoria.

## Portões de segurança
- Nenhuma IA recebe acesso irrestrito a credenciais; usar secret manager/env do provedor.
- Sem autoenvio de mensagens em massa, scraping de dados pessoais, cliques artificiais ou publicação não autorizada.
- Sem anúncios pagos, compras de infraestrutura, alterações financeiras ou replicação autônoma sem orçamento e aprovação.
- Não anunciar disponibilidade de cursos sem verificar o fornecedor.
- Separar métricas operacionais de vendas/comissões confirmadas na plataforma.
- Não considerar deploy como comprovação de tráfego, venda ou faturamento.
- Lei Geral de Proteção de Dados, consentimento, descadastro e regras dos canais aplicáveis.

## MVP de entrega
1. Portal corporativo responsivo com Werozinha e catálogo.
2. Páginas de ofertas autorizadas com links patrocinados rastreáveis.
3. SEO técnico, sitemap, robots.txt e conteúdo editorial revisado.
4. Painel com versão LIVE, timestamp, health e eventos de cliques, sem inventar conversões.
5. Integração Hotmart para verificação de atribuição e comissões, quando autorizada.
6. Fluxo de geração de sites por briefing, com prévia, testes e publicação aprovada.

## Critérios de aceite
- Navegação mobile, testes automatizados e zero erros críticos.
- Link de afiliado e autorização comprovados antes de campanhas.
- Eventos de cliques auditáveis, sem manipulação.
- Receita somente com evidência do provedor.
- Deploy seguro, monitoramento e rollback testados.
