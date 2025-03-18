from db_connection import Database

class Pedido:
    def __init__(self):
        self.db = Database()

    def save(self, description, value, payment_method):
        query = "INSERT INTO pedido (description, value, payment_method) VALUES (%s, %s, %s)"
        params = (description, value, payment_method)

        if self.db.executar_query(query, params):
            return {"message": "Pedido cadastrado com sucesso!"}
        else:
            return {"message": "Erro ao cadastrar pedido."}

    def listar_tudo(self):
        if self.db.conexao:
            self.db.cursor.execute("SELECT codPedido, order_date, description, value, payment_method FROM pedido")
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

    def update(self, order_id, order_date, description, value, payment_method):
        order_id = int(order_id)

        query = "UPDATE pedido SET order_date = %s, description = %s, value = %s, payment_method = %s WHERE id = %s"
        params = (order_date, description, value, payment_method, order_id)

        if self.db.executar_query(query, params):
            print("Pedido atualizado com sucesso!")
            return True
        else:
            print("Erro ao atualizar pedido.")
            return False