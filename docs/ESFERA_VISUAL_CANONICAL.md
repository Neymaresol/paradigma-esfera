# ESFERA — Visual canônico e política de preservação
**Registro:** 2026-10-24 21:45 America/Sao_Paulo (aproximado; horário do commit é a referência técnica)
**Versão de referência:** PR #29, branch `fix/esfera-futuristic-home-search-20261024`, commit `4b6940010a4a158e4348dfd03268996b5d130e2c`.
**Arquivo visual canônico:** `esfera_prototipo.html`; endpoint principal `/` (também `/esfera`).
**Estado:** versão preservada no GitHub em branch; NÃO afirmar que já está em produção.

## Elementos obrigatórios
- Fundo azul-escuro, luzes neon azul e detalhes dourados.
- Núcleo central PARADIGMA / IA CENTRAL com coroa.
- Quatro frentes: EDUCAÇÃO, SERVIÇOS, COMÉRCIO, EXPANSÃO.
- Faixa inferior: MONITORAMENTO, BANCO DE DADOS, APRENDIZADO, SEGURANÇA, MULTIPLICAÇÃO.
- Pesquisa por interesses incorporada à página futurista, sem substituir a homepage por página minimalista.
- Layout responsivo, sem alterar bloqueios de publicação de ofertas não verificadas.

## Gates obrigatórios para qualquer mudança visual
1. Capturar screenshot da homepage em viewport móvel e desktop no staging.
2. Comparar com o layout canônico; rejeitar perda de núcleo central, quatro pilares, paleta e faixa de controles.
3. Validar links e busca, acessibilidade, ausência de erros JS, saúde e logs.
4. Submeter PR com screenshots, revisão e Double Check antes de produção.
5. Após deploy, confirmar health e regressão visual; manter rollback para commit anterior.

## Teste de regressão recomendado
Verificar `/` com conteúdo 'PARADIGMA', 'IA CENTRAL', 'EDUCAÇÃO', 'SERVIÇOS', 'COMÉRCIO', 'EXPANSÃO', 'MONITORAMENTO' e formulário com action `/descobrir`.

**Nota:** O registro é uma política de preservação e referência de rollback; não constitui teste executado nem proteção automática até a CI ser implementada.
