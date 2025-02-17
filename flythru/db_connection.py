import mysql.connector

class Database:
    def __init__(self):
        try:
            self.conexao = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Alan3640.",
                database="backfood"
            )
            self.cursor = self.conexao.cursor()
            print("Conexão bem-sucedida!")
        except mysql.connector.Error as erro:
            print(f"Erro ao conectar ao MySQL: {erro}")
            self.conexao = None
            self.cursor = None
    
    def executar_query(self, query, params=None):
        try:
            if self.conexao and self.cursor:
                self.cursor.execute(query, params)
                self.conexao.commit()
                return True
        except mysql.connector.Error as erro:
            print(f"Erro ao executar query: {erro}")
            return False
