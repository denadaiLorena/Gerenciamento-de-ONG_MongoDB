from datetime import datetime
from uuid import uuid4
from conexion.connection import PostgresQueries
from model.recibo import Recibo


class Controller_Recibo:
    def __init__(self):
        pass

    def inserir_recibo(self, postGree=None, id_doacao=None, id_pessoa=None, id_campanha=None) -> Recibo:
        if postGree is None:
            postGree = PostgresQueries(can_write=True)
            postGree.connect()

        data_emissao = datetime.now()
        codigo = uuid4()

        cursor = postGree.conn.cursor()
        cursor.execute("SELECT nextval('recibo_id_recibo_seq') AS id;")
        id_recibo = cursor.fetchone()[0]

        # id_doacao, id_pessoa e id_campanha são obrigatórios na tabela Recibo
        # Garantir que temos os valores necessários; preferimos falhar cedo com mensagem clara
        if id_pessoa is None or id_campanha is None:
            raise ValueError("id_pessoa e id_campanha são necessários para gerar um recibo.")

        sql_insert = f"""
            INSERT INTO recibo (id_recibo, data_emissao, codigo_validacao, id_doacao, id_pessoa, id_campanha)
            VALUES ('{id_recibo}', '{data_emissao}', '{codigo}', '{id_doacao}', '{id_pessoa}', '{id_campanha}');
        """
        postGree.write(sql_insert)

        novo_recibo = Recibo(
            id_recibo=id_recibo,
            data_emissao=data_emissao,
            codigo_validacao=codigo
        )

        print("\nRecibo gerado:")
        print(novo_recibo.to_string())
        return novo_recibo

    def listar_recibos(self, postGree=None, need_connect=False):
        if postGree is None:
            postGree = PostgresQueries()
        if need_connect:
            postGree.connect()

        query = """
            SELECT r.id_recibo, r.data_emissao, r.codigo_validacao,
                   d.id_doacao, p.nome AS doador, d.valor
            FROM recibo r
            JOIN doacao d ON r.id_doacao = d.id_doacao
            JOIN pessoa p ON d.id_pessoa = p.id_pessoa
            ORDER BY r.data_emissao DESC;
        """
        print(postGree.sqlToDataFrame(query))
