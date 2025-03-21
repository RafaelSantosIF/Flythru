from db_connection import Database

class Item_Cardapio:
    def __init__(self):
        self.db = Database()

    def save(self, nome, preco, listaProdutos, category):
        query = """
            INSERT INTO item_cardapio (nome, preco, listaProdutos, category)
            VALUES (%s, %s, %s, %s)
        """
        params = (nome, preco, listaProdutos, category)

        if self.db.executar_query(query, params):
            return {"message": "Item do cardápio cadastrado com sucesso!"}
        else:
            return {"message": "Erro ao cadastrar item do cardápio."}

    def listar_tudo(self):
        if self.db.conexao:
            self.db.cursor.execute("SELECT codCardapio, nome, preco, listaProdutos, category FROM item_cardapio")
            return self.db.cursor.fetchall()
        return []

    def delete(self, nome):
        nome = str(nome)

        query = "DELETE FROM item_cardapio WHERE nome = %s"
        params = (nome,)

        if self.db.executar_query(query, params):
            print("Item do Cardápio excluído com sucesso!")
            return True
        else:
            print("Erro ao excluir Item do Cardapio.")
            return False

    def update(self, codCardapio, nome, preco, listaProdutos, category):
        codCardapio = int(codCardapio)

        query = """
            UPDATE item_cardapio
            SET nome = %s, preco = %s, listaProdutos = %s, categoria = %s
            WHERE codCardapio = %s
        """
        params = (nome, preco, listaProdutos, category, codCardapio)

        if self.db.executar_query(query, params):
            print("Item Cardapio atualizado com sucesso!")
            return True
        else:
            print("Erro ao atualizar Item Cardapio.")
            return False