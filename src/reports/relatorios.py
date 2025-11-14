from conexion.connection import PostgresQueries


class Relatorio:
    def __init__(self):
        with open("src/sql/relatorio_doacoes.sql") as f:
            self.query_relatorio_doacoes = f.read()

        with open("src/sql/relatorio_campanhas.sql") as f:
            self.query_relatorio_campanhas = f.read()

        with open("src/sql/relatorio_pessoas.sql") as f:
            self.query_relatorio_pessoas = f.read()

    def get_relatorio_campanhas(self):
        postgree = PostgresQueries()
        postgree.connect()

        print(postgree.sqlToDataFrame(self.query_relatorio_campanhas))
        input("Pressione Enter para Sair do Relatório de Campanhas \n")



    def get_relatorio_doacoes(self):
        postgree = PostgresQueries()
        postgree.connect()

        print(postgree.sqlToDataFrame(self.query_relatorio_doacoes))
        input("Pressione Enter para Sair do Relatório de Doações")


    def get_relatorio_pessoas(self):
        postgree = PostgresQueries()
        postgree.connect()

        print(postgree.sqlToDataFrame(self.query_relatorio_pessoas))
        input("Pressione Enter para Sair do Relatório de Pessoas")