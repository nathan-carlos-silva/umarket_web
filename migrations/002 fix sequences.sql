-- =========================================================
-- Migration 002: corrige as SEQUENCES do PostgreSQL
--
-- Causa raiz do erro "duplicate key value violates unique
-- constraint vendas_pkey": o backup.sql insere IDs manuais
-- (1, 2, 3...) em usuarios, produtos, pdv e vendas. O
-- PostgreSQL nao atualiza a sequence (usada pelo SERIAL)
-- automaticamente quando um ID e inserido manualmente, entao
-- ela continua "achando" que o proximo ID livre e o 1.
--
-- Isso afeta qualquer INSERT feito pela aplicacao sem id
-- explicito: novo usuario (cadastro), novo produto, nova
-- venda etc.
-- =========================================================

SELECT setval('usuarios_id_seq', (SELECT COALESCE(MAX(id), 1) FROM usuarios));
SELECT setval('produtos_id_seq', (SELECT COALESCE(MAX(id), 1) FROM produtos));
SELECT setval('pdv_id_seq', (SELECT COALESCE(MAX(id), 1) FROM pdv));
SELECT setval('vendas_id_seq', (SELECT COALESCE(MAX(id), 1) FROM vendas));
SELECT setval('vendas_produtos_id_seq', (SELECT COALESCE(MAX(id), 1) FROM vendas_produtos));