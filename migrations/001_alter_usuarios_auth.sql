-- =========================================================
-- Migration: adiciona suporte a autenticacao na tabela usuarios
-- O dump original (backup.sql) nao possui campos de senha nem
-- flag de administrador, entao precisamos incluir:
--   - senha_hash: armazena o hash da senha (nunca a senha em texto puro)
--   - is_admin:   diferencia cliente (false) de administrador (true)
-- =========================================================

ALTER TABLE usuarios
    ADD COLUMN IF NOT EXISTS senha_hash VARCHAR(255),
    ADD COLUMN IF NOT EXISTS is_admin BOOLEAN NOT NULL DEFAULT FALSE;

-- Define uma senha padrao "123456" (ja em hash) para os usuarios
-- de seed existentes, apenas para fins de teste/desenvolvimento.
-- O hash abaixo foi gerado com werkzeug.security.generate_password_hash("123456")
-- Rode o script scripts/seed_senhas.py depois de aplicar esta migration
-- para gerar hashes reais no seu ambiente (o hash muda a cada execucao
-- por causa do salt aleatorio do werkzeug).

-- Marca o usuario Nathan Carlos (id=1) como administrador de teste
UPDATE usuarios SET is_admin = TRUE WHERE id = 1;
