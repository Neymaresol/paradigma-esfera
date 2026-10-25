# ESFERA — Registro de versão WEROZINHA-IDLE-CAROUSEL-V1

Data: 25/10/2026, 14:47 (America/Sao_Paulo; horário de referência da solicitação).
Estado: especificação aprovada, implementação pendente; NÃO implantado em produção.

## Histórico preservado
- WEROZINHA-OFICIAL-V1: personagem baseada na foto fornecida, headset, coroa W, preto/rosa neon.
- ESFERA-AJAX-BUSCA-V1: autocomplete sob o campo, seleção de sugestões e catálogo autorizado.
- ESFERA-WEROZINHA-MVP-V1.1/V1.2: protótipos HTML, ainda sem validação de integração real.
- WEROZINHA-IA-INTERATIVA-V1: clicar na personagem abre conversa no próprio site.
- WEROZINHA-IDLE-CAROUSEL-V1: layout aprovado; personagem grande na área central, SEM miniaturas de gestos abaixo e SEM avatar circular flutuante no canto.

## Comportamento a desenvolver
1. Após 5 segundos de inatividade, alternar a imagem central entre poses oficiais (dança, cabelo, piscar, biquinho, beijo, gestos), com transição suave e temporizador reiniciado em interações.
2. Nunca trocar a imagem durante digitação ou leitura ativa; respeitar prefers-reduced-motion e fornecer pausa manual.
3. Toque na imagem abre IA Werozinha dentro do painel, mantendo o contexto da pesquisa.
4. Busca AJAX apresenta sugestões abaixo do campo, com teclado e toque; produtos só exibem CTA de compra quando o link de afiliado for autorizado e validado.
5. Não inventar vendas, comissões, catálogo, autorização ou status online.

## Critérios de aceite / Double Check
- Testar Chrome Android, desktop, acessibilidade e responsividade.
- Confirmar 5s de inatividade, pausa durante interação, retomada, troca de imagens, clique e foco no chat.
- Validar busca, estados vazio/erro, redirecionamento e rastreabilidade de afiliados sem cliques artificiais.
- Testar staging, health, logs, rollback e só então planejar deploy canário.

## Próxima etapa
Implementar imagens individuais licenciadas/fornecidas, carousel de verdade (não apenas imagem estática), IA e API de catálogo em branch de desenvolvimento. Produção permanece inalterada.
