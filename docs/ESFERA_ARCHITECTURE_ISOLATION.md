# Contrato de isolamento — PARADIGMA ESFERA

Data da revisão: 2026-10-24. Horário da revisão: não aferido.

## Decisão arquitetural obrigatória

PARADIGMA ESFERA é uma arquitetura autônoma de multiplicação. **Wero1Mercados é outro robô, independente, e NÃO é módulo, dependência, banco, fonte de produtos, mecanismo de publicação ou instância filha da ESFERA.**

## Regras

1. Código, banco, credenciais, jobs, endpoints, campanhas e catálogo da ESFERA são próprios.
2. Não importar código, ofertas, tabelas, configurações ou credenciais do Wero1Mercados para a ESFERA.
3. A recuperação histórica de informações do Wero1Mercados feita em auditoria anterior não autoriza integração nem compartilhamento de dados.
4. Multiplicação da ESFERA: descobrir oportunidades em fontes autorizadas, validar afiliação e rastreamento, deduplicar, registrar produtos no catálogo próprio, criar campanhas permitidas, medir conversões confirmadas e propor novas versões/instâncias com validação e rollback.
5. Qualquer nova integração externa deve ter contrato, autorização, testes, segregação de dados e flags de ativação independentes.
6. Manter homepage futurista atual e produção existente até Double Check e promoção controlada.
7. Não declarar vendas, comissões, publicações ou sincronização em produção sem evidência autenticada.

## Estado em 2026-10-24

O módulo `hotmart_catalog_sync.py` em branch de desenvolvimento é código nativo da ESFERA, sem dependência do Wero1Mercados; não possui ainda conector real, persistência ou agendamento. Os quatro HotLinks conhecidos são registro histórico, não prova de autorização atual. Produção permanece sem mudanças nesta revisão.
