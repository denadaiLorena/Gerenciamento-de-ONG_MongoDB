from decimal import Decimal
from datetime import datetime
from conexion.connection import PostgresQueries
from model.doacao import Doacao
from model.recibo import Recibo
from controller.controller_recibo import Controller_Recibo
from controller.controller_pessoa import Controller_Pessoa
from controller.controller_campanha import Controller_Campanha
from utils import validation
from utils import logger


class Controller_Doacao:
    def __init__(self):
        self.control_pessoa = Controller_Pessoa()
        self.control_campanha = Controller_Campanha()

    # Inserir nova doação
    def inserir_doacao(self, id_pessoa_logado: int = None) -> Doacao:
        postGree = None
        try:
            postGree = PostgresQueries(can_write=True)
            postGree.connect()

            print("\n--- Nova Doação ---")
            # Se o id do doador já for conhecido (usuário logado), não pedir CPF
            if id_pessoa_logado is None:
                cpf_pessoa = input("Digite o CPF do doador: ").strip()
                ok, msg = validation.require_field(cpf_pessoa, "CPF")
                if not ok:
                    print(msg)
                    return None

                if not validation.is_valid_cpf(cpf_pessoa):
                    print("CPF inválido.")
                    return None

                pessoa = self.control_pessoa.validar_pessoa(postGree, cpf_pessoa)
                if pessoa is None:
                    print("Pessoa não encontrada.")
                    return None

                id_pessoa = pessoa.get_id_pessoa()
            else:
                id_pessoa = id_pessoa_logado

            id_campanha_input = input("Digite o ID da campanha: ").strip()
            ok, msg = validation.require_field(id_campanha_input, "ID da campanha")
            if not ok:
                print(msg)
                return None
            try:
                id_campanha = int(validation.strip_non_digits(id_campanha_input))
            except ValueError:
                print("ID da campanha inválido.")
                return None

            valor_input = input("Digite o valor da doação: ").strip()
            ok, msg = validation.require_field(valor_input, "Valor")
            if not ok:
                print(msg)
                return None
            try:
                valor = Decimal(valor_input)
            except Exception:
                print("Valor inválido. Digite um número válido.")
                return None

            data_doacao = datetime.now()

            # Gera o próximo ID
            cursor = postGree.conn.cursor()
            cursor.execute("SELECT nextval('doacao_id_doacao_seq') AS id;")
            id_doacao = cursor.fetchone()[0]

            sql_insert = f"""
                INSERT INTO doacao (id_doacao, id_pessoa, id_campanha, valor, data_doacao)
                VALUES ('{id_doacao}', '{id_pessoa}', '{id_campanha}', '{valor}', '{data_doacao}');
            """
            postGree.write(sql_insert)

            # Cria o recibo automaticamente (1:1). Passa id_pessoa para a criação do recibo
            control_recibo = Controller_Recibo()
            recibo = control_recibo.inserir_recibo(postGree, id_doacao, id_pessoa, id_campanha)

            nova_doacao = Doacao(
                id_doacao=id_doacao,
                id_pessoa=id_pessoa,
                id_campanha=id_campanha,
                valor=valor,
                data_doacao=data_doacao,
                recibo=recibo
            )

            print("\nDoação registrada com sucesso:")
            print(nova_doacao.to_string())
            return nova_doacao

        except Exception as e:
            logger.log_exception(e, context='inserir_doacao')
            print("Ocorreu um erro ao processar a doação. Tente novamente mais tarde.")
            return None
        finally:
            if postGree:
                postGree.close()

    # Atualizar
    def atualizar_doacao(self) -> Doacao:
        postGree = PostgresQueries(can_write=True)
        postGree.connect()

        id_doacao = int(input("Informe o ID da doação a atualizar: "))
        df = postGree.sqlToDataFrame(f"SELECT * FROM doacao WHERE id_doacao = {id_doacao};")
        if df.empty:
            print("Doação não encontrada.")
            return None

        valor = Decimal(input("Novo valor da doação: "))
        postGree.write(f"UPDATE doacao SET valor = '{valor}' WHERE id_doacao = '{id_doacao}';")

        print("Doação atualizada com sucesso.")
        return Doacao(
            id_doacao=id_doacao,
            id_pessoa=df.id_pessoa[0],
            id_campanha=df.id_campanha[0],
            valor=valor,
            data_doacao=df.data_doacao[0]
        )

    # Excluir
    def excluir_doacao(self):
        postGree = PostgresQueries(can_write=True)
        postGree.connect()

        id_doacao = int(input("Informe o ID da doação que deseja excluir: "))
        df = postGree.sqlToDataFrame(f"SELECT * FROM doacao WHERE id_doacao = {id_doacao};")
        if df.empty:
            print("Doação não encontrada.")
            return

        confirmar = input(f"Confirma a exclusão da doação {id_doacao}? (s/n): ").lower()
        if confirmar == 's':
            postGree.write(f"DELETE FROM recibo WHERE id_doacao = {id_doacao};")
            postGree.write(f"DELETE FROM doacao WHERE id_doacao = {id_doacao};")
            print("Doação e recibo excluídos com sucesso.")
        else:
            print("Exclusão cancelada.")

    # Listar
    def listar_doacoes(self, postGree=None, need_connect=False):
        if postGree is None:
            postGree = PostgresQueries()
        if need_connect:
            postGree.connect()

        query = """
            SELECT d.id_doacao, p.nome AS doador, c.nome AS campanha, 
                   d.valor, d.data_doacao, r.id_recibo
            FROM doacao d
            JOIN pessoa p ON d.id_pessoa = p.id_pessoa
            JOIN campanha c ON d.id_campanha = c.id_campanha
            LEFT JOIN recibo r ON d.id_doacao = r.id_doacao
            ORDER BY d.data_doacao DESC;
        """
        print(postGree.sqlToDataFrame(query))
