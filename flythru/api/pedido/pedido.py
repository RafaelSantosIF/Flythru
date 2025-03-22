from db_connection import Database
from api.cardapio.item_cardapio import Item_Cardapio
from api.estoque.estoque import Estoque

cardapio = Item_Cardapio()
estoque = Estoque()

class Pedido:
    def __init__(self):
        self.db = Database()

    def save(self, description,quantidade_description, value, payment_method):
        query = "INSERT INTO pedido (description,quantidade_description, value, payment_method) VALUES (%s, %s, %s, %s)"
        params = (description, quantidade_description, value, payment_method)

        if self.db.executar_query(query, params):
            self.dar_baixa_estoque(description,quantidade_description)
            return {"message": "Pedido cadastrado com sucesso!"}
        else:
            return {"message": "Erro ao cadastrar pedido."}

    def listar_tudo(self):
        if self.db.conexao:
            self.db.cursor.execute("SELECT codPedido, order_date, description,quantidade_description, value, payment_method FROM pedido")
            return self.db.cursor.fetchall()
        return []

    def delete(self, order_id):
        order_id = int(order_id)

        query = "DELETE FROM pedido WHERE id = %s"
        params = (order_id,)

        if self.db.executar_query(query, params):
            print("Pedido excluído com sucesso!")
            return True
        else:
            print("Erro ao excluir pedido.")
            return False

    def update(self, order_id, order_date, description,quantidade_description, value, payment_method):
        order_id = int(order_id)

        query = "UPDATE pedido SET order_date = %s, description = %s,quantidade_description = %s, value = %s, payment_method = %s WHERE id = %s"
        params = (order_date, description,quantidade_description, value, payment_method, order_id)

        if self.db.executar_query(query, params):
            print("Pedido atualizado com sucesso!")
            return True
        else:
            print("Erro ao atualizar pedido.")
            return False
        
    def dar_baixa_estoque(self, description, quantidade_description):
        array_strings = description.split('\n')
        array_strings = [s for s in array_strings if s]

        array_quantidade = quantidade_description.split('\n')
        array_quantidade = [s for s in array_quantidade if s]

        for index, item in enumerate(array_strings):
            item_selecionado = cardapio.listByName(item)
            print(item_selecionado)
            ingredientes_item = item_selecionado[0][3].strip("--").split("--")
            print(f'Pedido.py = {ingredientes_item}')

            numeros = item_selecionado[0][4].replace("--", " ").strip().split()
            quantidade_ingredientes = [int(float(num)) for num in numeros]
            print(f'Pedido.py = {quantidade_ingredientes}')

            for i in range(int(array_quantidade[index])):
                for index, ingrediente in enumerate(ingredientes_item):
                    estoque.subtrairQuantidade(ingrediente,quantidade_ingredientes[index])