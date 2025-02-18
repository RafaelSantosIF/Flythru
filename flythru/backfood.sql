create database backfood;
use backfood;

CREATE TABLE fornecedor (
  codFornecedor INT PRIMARY KEY AUTO_INCREMENT,
  nome VARCHAR(255) NOT NULL,
  telefone VARCHAR(20),
  email VARCHAR(255),
  endereço VARCHAR(255)
);

CREATE TABLE produto (
  codProduto INT PRIMARY KEY AUTO_INCREMENT,
  nome VARCHAR(255) NOT NULL,
  quantidade int,
  categoria VARCHAR(255)
);

CREATE TABLE item_cardapio (
  codCardapio INT PRIMARY KEY AUTO_INCREMENT,
  nome varchar(255),
  preco float,
  codProduto INT,
  FOREIGN KEY (codProduto) REFERENCES produto (codProduto)
);


CREATE TABLE produto_cardapio (
  codProduto INT,
  codCardapio INT,
  PRIMARY KEY (codProduto, codCardapio),
  FOREIGN KEY (codProduto) REFERENCES produto (codProduto),
  FOREIGN KEY (codCardapio) REFERENCES item_cardapio (codCardapio)
);


INSERT INTO fornecedor (nome, telefone, email, endereço) VALUES
('Fornecedor A', '1234-5678', 'fornecedorA@email.com', 'Rua 1, Cidade A'),
('Fornecedor B', '9876-5432', 'fornecedorB@email.com', 'Rua 2, Cidade B');

-- Inserindo produtos
INSERT INTO produto (nome, quantidade, categoria) VALUES
('Pão de Hambúrguer', 100, 'Padaria'),
('Carne de Hambúrguer', 50, 'Carnes'),
('Queijo Cheddar', 80, 'Laticínios'),
('Alface', 30, 'Verduras');

-- Inserindo itens no cardápio
INSERT INTO item_cardapio (nome, preco, codProduto) VALUES
('Hambúrguer Simples', 15.99, 1),
('Cheeseburguer', 18.99, 2),
('X-Salada', 20.99, 3);

-- Relacionando produtos com itens do cardápio
INSERT INTO produto_cardapio (codProduto, codCardapio) VALUES
(1, 1), (2, 1), -- Hambúrguer Simples usa pão e carne
(1, 2), (2, 2), (3, 2), -- Cheeseburguer usa pão, carne e queijo
(1, 3), (2, 3), (3, 3), (4, 3); -- X-Salada usa pão, carne, queijo e alface


SELECT 
    ic.nome AS ItemCardapio, 
    GROUP_CONCAT(p.nome SEPARATOR ', ') AS Ingredientes,
    ic.preco AS Preco
FROM produto_cardapio pc
JOIN produto p ON pc.codProduto = p.codProduto
JOIN item_cardapio ic ON pc.codCardapio = ic.codCardapio
GROUP BY ic.codCardapio, ic.nome, ic.preco
ORDER BY ic.nome;
select * from produto;
DELETE FROM produto WHERE codProduto >= 7;