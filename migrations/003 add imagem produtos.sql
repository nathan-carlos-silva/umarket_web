-- =========================================================
-- Migration 003: adiciona suporte a imagem de produto
-- =========================================================

ALTER TABLE produtos ADD COLUMN IF NOT EXISTS imagem_url VARCHAR(255);