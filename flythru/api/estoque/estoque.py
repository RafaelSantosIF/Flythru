from db_connection import Database

class Estoque:
    def __init__(self):
        self.db = Database()

    def save(self, produto, quantidade, categoria):
        query = "INSERT INTO produto ( nome, quantidade, categoria) VALUES (%s, %s, %s)"
        params = ( produto, quantidade, categoria)
        if self.db.executar_query(query, params):
            print("Produto cadastrado com sucesso!")
        else:
            print("Erro ao cadastrar produto.")

    def listar_tudo(self):
        if self.db.conexao:
            self.db.cursor.execute("SELECT codProduto, nome, quantidade, categoria FROM produto")
            return self.db.cursor.fetchall()
        return []

    def delete(self, id_produto):
        try:
            id_produto = int(id_produto)  # Converte para inteiro *aqui*

            query = "DELETE FROM produto WHERE codProduto = %s"
            params = (id_produto,)

            if self.db.executar_query(query, params):
                print("Produto excluído com sucesso!")
                return True # Retorna True em caso de sucesso
            else:
                print("Erro ao excluir produto.")
                return False # Retorna False em caso de falha

        except ValueError:
            print("ID do produto inválido. Deve ser um número inteiro.")
            return False # Retorna False se o ID não for um inteiro válido
        except Exception as e:
            print(f"Erro ao excluir produto: {e}")
            return False # Retorna False em caso de outro erro

    def update(self, id_produto, produto, quantidade, categoria):
            try:
                id_produto = int(id_produto)  # Converte o ID para inteiro

                query = "UPDATE produto SET nome = %s, quantidade = %s, categoria = %s WHERE codProduto = %s"
                params = (produto, quantidade, categoria, id_produto)

                if self.db.executar_query(query, params):
                    print("Produto atualizado com sucesso!")
                    return True
                else:
                    print("Erro ao atualizar produto.")
                    return False

            except ValueError:
                print("ID do produto inválido. Deve ser um número inteiro.")
                return False
            except Exception as e:
                print(f"Erro ao atualizar produto: {e}")
                return False

    def baixoEstoque(self):
        if self.db.conexao:
            self.db.cursor.execute("SELECT codProduto, nome, quantidade, categoria FROM produto")
            produtos = self.db.cursor.fetchall()

            produtos_baixo_estoque = []
            for produto in produtos:
                codProduto, nome, quantidade, categoria = produto
                limite_baixo_estoque = 10  # Valor padrão para unidades

                if categoria == "Bebidas":
                    limite_baixo_estoque = 1000  # 1000 ml = 1 litro
                elif categoria in ["Carnes", "Laticíneos", "Verduras", "Laticínios"]:
                    limite_baixo_estoque = 1000  # 1000 g = 1 kg

                if quantidade < limite_baixo_estoque:
                    produtos_baixo_estoque.append(produto)

            return produtos_baixo_estoque
        return []

    def buscar(self, nome_produto):
        if self.db.conexao:
            query = "SELECT codProduto, nome, quantidade, categoria FROM produto WHERE nome LIKE %s"
            params = (f"%{nome_produto}%",)  # Adiciona '%' para pesquisa parcial
            self.db.cursor.execute(query, params)
            return self.db.cursor.fetchall()
        return []
    
    def update_quantity(self, id_ingrediente, nova_quantidade):
        """Atualiza a quantidade de um ingrediente no estoque"""
        try:
            nova_quantidade = max(0, nova_quantidade)  # Garantir que não fique negativo
            self.cursor.execute(
                "UPDATE ingrediente SET quantidade = ? WHERE id = ?",
                (nova_quantidade, id_ingrediente)
            )
            self.conexao.commit()
            return True
        except Exception as e:
            print(f"Erro ao atualizar quantidade: {e}")
            return False