from db_connection import Database

class Item_Cardapio:
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
            self.db.cursor.execute("SELECT codCardapio, nome, preco, codProduto FROM item_cardapio")
            return self.db.cursor.fetchall()
        return []

    def delete(self, codCardapio):
        codCardapio = int(codCardapio)

        query = "DELETE FROM item_cardapio WHERE codCardapio = %s"
        params = (codCardapio,)

        if self.db.executar_query(query, params):
            print("Item do Cardápio excluído com sucesso!")
            return True
        else:
            print("Erro ao excluir Item do Cardapio.")
            return False

    def update(self, codCardapio, nome, preco, codProduto):
        codCardapio = int(codCardapio)

        query = "UPDATE item_cardapio SET nome = %s, preco = %s, codProduto = %s WHERE codCardapio = %s"
        params = (nome, preco, codProduto, codCardapio)

        if self.db.executar_query(query, params):
            print("Item Cardapio atualizado com sucesso!")
            return True
        else:
            print("Erro ao atualizar Item Cardapio.")
            return False