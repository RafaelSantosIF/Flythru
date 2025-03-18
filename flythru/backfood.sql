create database backfood;
use backfood;

CREATE TABLE fornecedor (
  codFornecedor INT PRIMARY KEY AUTO_INCREMENT,
  nome VARCHAR(255) NOT NULL,
  telefone VARCHAR(20),
  email VARCHAR(255),
  cnpj varchar(15)
);

CREATE TABLE produto (
  codProduto INT PRIMARY KEY AUTO_INCREMENT,
  nome VARCHAR(255) NOT NULL,
  quantidade int,
  categoria VARCHAR(255)
);

CREATE TABLE pedido (
  codPedido INT PRIMARY KEY AUTO_INCREMENT, -- Código único do pedido (auto incremento)
  order_date DATETIME DEFAULT CURRENT_TIMESTAMP, -- Data e hora do pedido (valor padrão é o momento da inserção)
  description VARCHAR(255), -- Descrição do pedido (opcional)
  value DECIMAL(10, 2) NOT NULL, -- Valor total a ser pago (não pode ser nulo)
  payment_method VARCHAR(100) NOT NULL -- Método de pagamento (não pode ser nulo)
);

CREATE TABLE item_cardapio (
  codCardapio INT PRIMARY KEY AUTO_INCREMENT,
  nome varchar(255),
  preco float,
  codProduto INT,
  FOREIGN KEY (codProduto) REFERENCES produto (codProduto) on delete set null on update cascade
);


CREATE TABLE produto_cardapio (
  codProduto INT,
  codCardapio INT,
  PRIMARY KEY (codProduto, codCardapio),
  FOREIGN KEY (codProduto) REFERENCES produto (codProduto) on delete cascade,
  FOREIGN KEY (codCardapio) REFERENCES item_cardapio (codCardapio) on delete cascade
);


INSERT INTO fornecedor (nome, telefone, email, cnpj) VALUES
('Fornecedor A', '1234-5678', 'fornecedorA@email.com', '12345678910235'),
('Fornecedor B', '9876-5432', 'fornecedorB@email.com', '14345678910235');

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

drop database backfood;