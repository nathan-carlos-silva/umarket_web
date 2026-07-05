-- =========================================================
-- 1. CRIAÇÃO DAS TABELAS (COM SUPORTE A AUTENTICAÇÃO E IMAGENS)
-- =========================================================

CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    data_nasc DATE,
    cpf NUMERIC(11) UNIQUE NOT NULL,
    senha_hash VARCHAR(255),
    is_admin BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE produtos (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(80) NOT NULL,
    classificacao VARCHAR(40),
    preco NUMERIC(10,2) NOT NULL,
    imagem_url VARCHAR(255)
);

CREATE TABLE pdv (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    cidade VARCHAR(50),
    estado CHAR(2),
    endereco TEXT
);

CREATE TABLE estoque (
    id_pdv INTEGER REFERENCES pdv(id),
    id_produto INTEGER REFERENCES produtos(id),
    qtd_atual INTEGER DEFAULT 0,
    capacity INTEGER, -- Mantido "capacity" conforme dump original
    PRIMARY KEY (id_pdv, id_produto)
);

CREATE TABLE vendas (
    id SERIAL PRIMARY KEY,
    data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    valor NUMERIC(10,2),
    forma_pagamento VARCHAR(20),
    id_pdv INTEGER REFERENCES pdv(id),
    id_usuario INTEGER REFERENCES usuarios(id)
);

CREATE TABLE vendas_produtos (
    id SERIAL PRIMARY KEY,
    id_venda INTEGER REFERENCES vendas(id) ON DELETE CASCADE,
    id_produto INTEGER REFERENCES produtos(id),
    qtd_produto INTEGER NOT NULL,
    valor_unitario NUMERIC(10,2) NOT NULL,
    valor_total NUMERIC(10,2) NOT NULL
);


-- =========================================================
-- 2. POPULAÇÃO DE DADOS (SEED DATA)
-- =========================================================

-- O hash abaixo corresponde à senha padrão "123456" gerada via pbkdf2 do Werkzeug
-- Nathan Carlos (ID: 1) já nasce configurado como Admin (is_admin = TRUE)
INSERT INTO usuarios (id, nome, email, data_nasc, cpf, senha_hash, is_admin) VALUES 
(1, 'Nathan Carlos', 'nathan@umarket.com', '2000-01-01', 12345678901, 'scrypt:32768:8:1$uH9Xm8XNUR778h9T$e208b049d567302488d57d5ee7d653fbb8dbb751b3ba7bd193efcf376cc6f5b9cb7b667bd4743c7b2a65a25b16eef2505be1748ce68d9f1092e9e6231d687440', TRUE),
(2, 'Ana Paula', 'ana@umarket.com', '1990-05-15', 98765432100, 'scrypt:32768:8:1$uH9Xm8XNUR778h9T$e208b049d567302488d57d5ee7d653fbb8dbb751b3ba7bd193efcf376cc6f5b9cb7b667bd4743c7b2a65a25b16eef2505be1748ce68d9f1092e9e6231d687440', FALSE),
(3, 'Marcos Silva', 'marcos@umarket.com', '1988-10-20', 11122233344, 'scrypt:32768:8:1$uH9Xm8XNUR778h9T$e208b049d567302488d57d5ee7d653fbb8dbb751b3ba7bd193efcf376cc6f5b9cb7b667bd4743c7b2a65a25b16eef2505be1748ce68d9f1092e9e6231d687440', FALSE),
(4, 'Rebeca Souza', 'rebeca@umarket.com', '1995-03-12', 55566677788, 'scrypt:32768:8:1$uH9Xm8XNUR778h9T$e208b049d567302488d57d5ee7d653fbb8dbb751b3ba7bd193efcf376cc6f5b9cb7b667bd4743c7b2a65a25b16eef2505be1748ce68d9f1092e9e6231d687440', FALSE),
(5, 'Arthur Joinville', 'arthur@umarket.com', '2001-07-25', 99988877766, 'scrypt:32768:8:1$uH9Xm8XNUR778h9T$e208b049d567302488d57d5ee7d653fbb8dbb751b3ba7bd193efcf376cc6f5b9cb7b667bd4743c7b2a65a25b16eef2505be1748ce68d9f1092e9e6231d687440', FALSE),
(6, 'Beatriz Santos', 'beatriz@umarket.com', '1992-12-30', 44433322211, 'scrypt:32768:8:1$uH9Xm8XNUR778h9T$e208b049d567302488d57d5ee7d653fbb8dbb751b3ba7bd193efcf376cc6f5b9cb7b667bd4743c7b2a65a25b16eef2505be1748ce68d9f1092e9e6231d687440', FALSE);

-- PRODUTOS (Com a coluna imagem_url nula por padrão no seed)
INSERT INTO produtos (id, nome, classificacao, preco, imagem_url) VALUES 
(1, 'Energético 250ml', 'Bebidas', 8.50, NULL),
(2, 'Barra de Cereal', 'Alimentos', 3.20, NULL),
(3, 'Café Expresso', 'Bebidas', 4.50, NULL),
(4, 'Sanduíche Natural', 'Alimentos', 12.00, NULL),
(5, 'Refrigerante Lata', 'Bebidas', 5.50, NULL),
(6, 'Chocolate Amargo', 'Alimentos', 6.00, NULL),
(7, 'Água Mineral', 'Bebidas', 3.00, NULL);

-- PDVs
INSERT INTO pdv (id, nome, cidade, estado, endereco) VALUES 
(1, 'Unidade CCT UDESC', 'Joinville', 'SC', 'Rua Paulo Malschitzki, 200'),
(2, 'Unidade Centro', 'Joinville', 'SC', 'Rua das Palmeiras, 10'),
(3, 'Unidade Shopping', 'Joinville', 'SC', 'Av. Rolf Wiest, 333'),
(4, 'Unidade Estação', 'Joinville', 'SC', 'Rua Leite Ribeiro, 50');

-- ESTOQUE
INSERT INTO estoque (id_pdv, id_produto, qtd_atual, capacity) VALUES 
(1, 1, 80, 100), (1, 2, 45, 50), (1, 3, 30, 40), (1, 4, 15, 20), (1, 5, 60, 60),
(2, 3, 20, 40), (2, 4, 10, 20), (2, 5, 30, 50), (2, 6, 25, 30), (2, 7, 50, 100),
(3, 1, 40, 50), (3, 2, 20, 30), (3, 6, 15, 20), (3, 7, 80, 100), (3, 4, 12, 15),
(4, 2, 10, 50), (4, 3, 40, 40), (4, 5, 25, 30), (4, 7, 90, 100), (4, 1, 30, 30);

-- VENDAS
INSERT INTO vendas (id, data, valor, forma_pagamento, id_pdv, id_usuario) VALUES 
(1, '2026-04-15 10:00:00', 8.50, 'PIX', 1, 1),
(2, '2026-04-20 14:00:00', 16.50, 'Crédito', 1, 1),
(3, '2026-04-19 11:30:00', 4.50, 'Débito', 2, 2),
(4, '2026-04-21 09:00:00', 17.50, 'PIX', 2, 2),
(5, '2026-04-23 08:00:00', 3.00, 'PIX', 3, 3),
(6, '2026-04-22 17:00:00', 14.50, 'Crédito', 3, 3),
(7, '2026-04-14 12:00:00', 12.00, 'Débito', 4, 4),
(8, '2026-04-15 15:00:00', 11.00, 'PIX', 4, 4),
(9, '2026-04-16 10:15:00', 5.50, 'Crédito', 1, 5),
(10, '2026-04-17 18:30:00', 12.50, 'Débito', 1, 5),
(11, '2026-04-20 09:45:00', 6.40, 'PIX', 2, 6),
(12, '2026-04-21 20:00:00', 7.50, 'Crédito', 2, 6);

-- ITENS DE VENDA
INSERT INTO vendas_produtos (id_venda, id_produto, qtd_produto, valor_unitario, valor_total) VALUES 
(1, 1, 1, 8.50, 8.50),
(2, 1, 1, 8.50, 8.50), (2, 6, 1, 8.00, 8.00),
(3, 3, 1, 4.50, 4.50),
(4, 3, 1, 4.50, 4.50), (4, 4, 1, 13.00, 13.00),
(5, 7, 1, 3.00, 3.00),
(6, 1, 1, 8.50, 8.50), (6, 6, 1, 6.00, 6.00),
(7, 4, 1, 12.00, 12.00),
(8, 5, 2, 5.50, 11.00),
(9, 5, 1, 5.50, 5.50),
(10, 1, 1, 8.50, 8.50), (10, 3, 1, 4.00, 4.00),
(11, 2, 2, 3.20, 6.40),
(12, 3, 1, 4.50, 4.50), (12, 7, 1, 3.00, 3.00);


-- =========================================================
-- 3. AJUSTE DE SEQUENCES (EVITA ERRO DE ID DUPLICADO EM NOVOS INSERTS)
-- =========================================================

SELECT setval('usuarios_id_seq', (SELECT COALESCE(MAX(id), 1) FROM usuarios));
SELECT setval('produtos_id_seq', (SELECT COALESCE(MAX(id), 1) FROM produtos));
SELECT setval('pdv_id_seq', (SELECT COALESCE(MAX(id), 1) FROM pdv));
SELECT setval('vendas_id_seq', (SELECT COALESCE(MAX(id), 1) FROM vendas));
SELECT setval('vendas_produtos_id_seq', (SELECT COALESCE(MAX(id), 1) FROM vendas_produtos));

-- RESET BANCO
/*
DROP TABLE vendas_produtos;
DROP TABLE vendas;
DROP TABLE estoque;
DROP TABLE usuarios;
DROP TABLE produtos;
DROP TABLE pdv;
*/