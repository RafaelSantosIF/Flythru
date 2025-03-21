from db_connection import Database

class Cardapio:
    def __init__(self):
        self.db = Database()

    def save(self, nome, preco, codProduto):
        query_check = "SELECT codProduto FROM produto WHERE codProduto = %s"
        self.db.cursor.execute(query_check, (codProduto,))
        produto = self.db.cursor.fetchone()

        if produto:
            query = "INSERT INTO item_cardapio (nome, preco, codProduto) VALUES (%s, %s, %s)"
            params = (nome, preco, codProduto)

            if self.db.executar_query(query, params):
                return {"message": "Item do cardápio cadastrado com sucesso!"}
            else:
                return {"message": "Erro ao cadastrar item do cardápio."}
        else:
            return {"message": "Produto não encontrado. Verifique o código do produto."}

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