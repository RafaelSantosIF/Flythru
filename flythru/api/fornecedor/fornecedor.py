from db_connection import Database

class Fornecedor:
    def __init__(self):
        self.db = Database()

    def save(self, nome, telefone, email, endereco):
        query = "INSERT INTO fornecedor (nome, telefone, email, endereco) VALUES (%s, %s, %s, %s)"
        params = (nome, telefone, email, endereco)

        if self.db.executar_query(query, params):
            return {"message": "Fornecedor cadastrado com sucesso!"}
        else:
            return {"message": "Erro ao cadastrar item do fornecedor."}

    def listar_tudo(self):
        if self.db.conexao:
            self.db.cursor.execute("SELECT * FROM fornecedor")
            return self.db.cursor.fetchall()
        return []

    def delete(self, codFornecedor):
        codFornecedor = int(codFornecedor)

        query = "DELETE FROM fornecedor WHERE codFornecedor = %s"
        params = (codFornecedor,)

        if self.db.executar_query(query, params):
            print("Fornecedor excluído com sucesso!")
            return True
        else:
            print("Erro ao excluir Fornecedor.")
            return False

    def update(self, codFornecedor, nome, telefone, email, endereco):
        codCardapio = int(codCardapio)

        query = "UPDATE fornecedor SET nome = %s, telefone = %s, email = %s, endereco = %s WHERE codFornecedor = %s"
        params = (nome, telefone, email, endereco, codFornecedor)

        if self.db.executar_query(query, params):
            print("Fornecedor atualizado com sucesso!")
            return True
        else:
            print("Erro ao atualizar Fornecedor.")
            return False