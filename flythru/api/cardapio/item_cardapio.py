from db_connection import Database

class Item_Cardapio:
    def __init__(self):
        self.db = Database()

    def save(self, nome, preco, listaProdutos, quantidadeProdutos, category):
        query = """
            INSERT INTO item_cardapio (nome, preco, listaProdutos, quantidadeProdutos, category)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (nome, preco, listaProdutos, quantidadeProdutos, category)

        if self.db.executar_query(query, params):
            return {"message": "Item do cardápio cadastrado com sucesso!"}
        else:
            return {"message": "Erro ao cadastrar item do cardápio."}

    def listar_tudo(self):
        if self.db.conexao:
            self.db.cursor.execute("SELECT codCardapio, nome, preco, listaProdutos, quantidadeProdutos, category FROM item_cardapio")
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

    def update(self, codCardapio, nome, preco, listaProdutos, quantidadeProdutos, category):
        codCardapio = int(codCardapio)

        query = """
            UPDATE item_cardapio
            SET nome = %s, preco = %s, listaProdutos = %s, quantidadeProdutos = %s categoria = %s
            WHERE codCardapio = %s
        """
        params = (nome, preco, listaProdutos, category, quantidadeProdutos, codCardapio)

        if self.db.executar_query(query, params):
            print("Item Cardapio atualizado com sucesso!")
            return True
        else:
            print("Erro ao atualizar Item Cardapio.")
            return False
        
    def listByName(self, nome):
        query = """SELECT * FROM item_cardapio WHERE nome = %s"""
        params = (nome,)
        
        try:
            # Criar uma nova conexão e cursor exclusivamente para esta consulta
            temp_db = Database()
            
            if temp_db.executar_query(query, params):
                resultados = temp_db.cursor.fetchall()
                print("Item Cardapio selecionado com sucesso!")
                return resultados
            else:
                print("Erro ao selecionar Item Cardapio.")
                return False
        except Exception as e:
            print(f"Erro ao executar a consulta: {e}")
            return False
        finally:
            # Garantir que a conexão temporária seja fechada
            if 'temp_db' in locals() and hasattr(temp_db, 'conexao') and temp_db.conexao:
                temp_db.conexao.close()