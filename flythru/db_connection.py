# Modifique a classe Database
import mysql.connector

class Database:
    def __init__(self):
        self.conectar()
    
    def conectar(self):
        try:
            self.conexao = mysql.connector.connect(
                host="localhost",
                user="root",
                password="aluno123",               
                database="backfood"
            )
            self.cursor = self.conexao.cursor(buffered=True)  # Cursor com buffer
            print("Conexão bem-sucedida!")
        except mysql.connector.Error as erro:
            print(f"Erro ao conectar ao MySQL: {erro}")
            self.conexao = None
            self.cursor = None
    
    def executar_query(self, query, params=None):
        try:
            if not self.conexao or not self.conexao.is_connected():
                self.conectar()
                
            if self.conexao and self.cursor:
                # Fecha e recria o cursor para cada consulta
                self.cursor.close()
                self.cursor = self.conexao.cursor(buffered=True)
                
                self.cursor.execute(query, params)
                self.conexao.commit()
                return True
        except mysql.connector.Error as erro:
            print(f"Erro ao executar query: {erro}")
            return False
    
    def limpar_resultados_pendentes(self):
        if hasattr(self, 'cursor') and self.cursor:
            try:
                self.cursor.fetchall()
            except:
                pass
            
            try:
                while self.cursor.nextset():
                    pass
            except:
                pass
    
    def __del__(self):
        # Destrutor para garantir que a conexão seja fechada
        if hasattr(self, 'cursor') and self.cursor:
            try:
                self.cursor.close()
            except:
                pass
                
        if hasattr(self, 'conexao') and self.conexao:
            try:
                self.conexao.close()
            except:
                pass