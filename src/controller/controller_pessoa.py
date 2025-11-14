from model.pessoa import Pessoa
from conexion.connection import MongoQueries, PostgresQueries
from model.doacao import Doacao
from model.pessoa import Pessoa
from conexion.connection import PostgresQueries
from model.doacao import Doacao
from model.recibo import Recibo
from typing import List
from utils import validation
from utils import logger
from bson.objectid import ObjectId


class Controller_Pessoa:
    def __init__(self):
        pass

    # insert
    def inserir_pessoa(self) -> Pessoa:
        postgres = None
        try:
            postgres = PostgresQueries(can_write=True)
            postgres.connect()

            cpf = input("CPF (Novo): ").strip()
            ok, msg = validation.require_field(cpf, "CPF")
            if not ok:
                print(msg)
                return None

            if not validation.is_valid_cpf(cpf):
                print("CPF inválido.")
                return None

            if self.verifica_existencia_pessoa(postgres, cpf):
                print(f"O CPF {cpf} já está cadastrado.")
                return None

            nome = input("Nome: ").strip()
            ok, msg = validation.require_field(nome, "Nome")
            if not ok:
                print(msg)
                return None

            email = input("Email: ").strip()
            senha = input("Senha: ").strip()
            ok, msg = validation.require_field(senha, "Senha")
            if not ok:
                print(msg)
                return None

            tipo_pessoa = input("Tipo (doador/usuario): ").strip().lower()
            if tipo_pessoa not in ("doador", "usuario"):
                print("Tipo inválido. Deve ser 'doador' ou 'usuario'.")
                return None

            # grava apenas números do CPF
            cpf_db = validation.normalize_numeric_field(cpf)

            sql = f"""
                INSERT INTO pessoa (nome, cpf, email, senha, tipo_pessoa)
                VALUES ('{nome}', '{cpf_db}', '{email}', '{senha}', '{tipo_pessoa}');
            """
            postgres.write(sql)

            df_pessoa = postgres.sqlToDataFrame(f"""
                SELECT id_pessoa, nome, cpf, email, senha, tipo_pessoa
                FROM pessoa
                WHERE cpf = '{cpf_db}';
            """)

            nova_pessoa = Pessoa(
                id_pessoa=df_pessoa.id_pessoa.values[0],
                nome=df_pessoa.nome.values[0],
                cpf=df_pessoa.cpf.values[0],
                email=df_pessoa.email.values[0],
                senha=df_pessoa.senha.values[0],
                tipo_pessoa=df_pessoa.tipo_pessoa.values[0]
            )

            print("\nPessoa cadastrada com sucesso!")
            print(nova_pessoa.to_string())
            return nova_pessoa

        except Exception as e:
            logger.log_exception(e, context='inserir_pessoa')
            print("Ocorreu um erro ao cadastrar a pessoa. Tente novamente mais tarde.")
            return None
        finally:
            if postgres:
                postgres.close()

    # update
    def atualizar_pessoa(self, id_pessoa_logado: int = None) -> Pessoa:
        postgres = None
        try:
            postgres = PostgresQueries(can_write=True)
            postgres.connect()

            # Se um id_pessoa_logado foi passado, permitimos que o usuário atualize apenas seu próprio registro
            if id_pessoa_logado is not None:
                df_self = postgres.sqlToDataFrame(f"SELECT cpf FROM pessoa WHERE id_pessoa = {id_pessoa_logado};")
                if df_self.empty:
                    print("Usuário logado não encontrado no sistema.")
                    return None
                cpf = df_self.cpf.values[0]
                print(f"Atualizando seu perfil (CPF: {cpf})")
            else:
                cpf = input("CPF da pessoa para atualizar: ").strip()
                ok, msg = validation.require_field(cpf, "CPF")
                if not ok:
                    print(msg)
                    return None

                cpf_db = validation.normalize_numeric_field(cpf)
                if not self.verifica_existencia_pessoa(postgres, cpf_db):
                    print(f"O CPF {cpf} não existe.")
                    return None

            print("\nQual dado deseja alterar?")
            print("1 - Nome")
            print("2 - Email")
            print("3 - Senha")
            print("4 - Tipo de pessoa (doador/usuario)")
            try:
                op = int(input("Opção: ").strip())
            except ValueError:
                print("Opção inválida.")
                return None

            campos = {
                1: "nome",
                2: "email",
                3: "senha",
                4: "tipo_pessoa"
            }

            if op not in campos:
                print("Opção inválida.")
                return None
            campo = campos[op]
            novo_valor = input(f"Novo valor para {campo}: ").strip()
            ok, msg = validation.require_field(novo_valor, campo)
            if not ok:
                print(msg)
                return None

            if campo == "tipo_pessoa" and novo_valor.lower() not in ("doador", "usuario"):
                print("Tipo inválido. Deve ser 'doador' ou 'usuario'.")
                return None

            sql = f"""
                UPDATE pessoa
                SET {campo} = '{novo_valor}'
                WHERE cpf = '{cpf_db if id_pessoa_logado is None else cpf}';
            """
            postgres.write(sql)
            df_pessoa = postgres.sqlToDataFrame(f"""
                SELECT id_pessoa, nome, cpf, email, senha, tipo_pessoa
                FROM pessoa
                WHERE cpf = '{cpf_db if id_pessoa_logado is None else cpf}';
            """)
            pessoa_atualizada = Pessoa(
                id_pessoa=df_pessoa.id_pessoa.values[0],
                nome=df_pessoa.nome.values[0],
                cpf=df_pessoa.cpf.values[0],
                email=df_pessoa.email.values[0],
                senha=df_pessoa.senha.values[0],
                tipo_pessoa=df_pessoa.tipo_pessoa.values[0]
            )
            print("\nPessoa atualizada com sucesso!")
            print(pessoa_atualizada.to_string())

            return pessoa_atualizada

        except Exception as e:
            logger.log_exception(e, context='atualizar_pessoa')
            print("Ocorreu um erro ao atualizar a pessoa. Tente novamente mais tarde.")
            return None
        finally:
            if postgres:
                postgres.close()

    # delete
    def excluir_pessoa(self):
        postgres = None
        try:
            postgres = PostgresQueries(can_write=True)
            postgres.connect()

            cpf = input("CPF da pessoa que deseja excluir(caso você seja doador, informe seu próprio CPF): ").strip()
            ok, msg = validation.require_field(cpf, "CPF")
            if not ok:
                print(msg)
                return None

            cpf_db = validation.normalize_numeric_field(cpf)
            if not self.verifica_existencia_pessoa(postgres, cpf_db):
                print(f"CPF {cpf} não existe.")
                return None

            # saber se esta em campanha
            df_campanha = postgres.sqlToDataFrame(f"""
                SELECT id_campanha FROM campanha
                WHERE id_pessoa = (SELECT id_pessoa FROM pessoa WHERE cpf = '{cpf_db}');
            """)
            if not df_campanha.empty:
                print("Essa pessoa está associada a uma ou mais campanhas e por isso não pode ser excluída.")
                return None

            df_pessoa = postgres.sqlToDataFrame(f"""
                SELECT id_pessoa, nome, cpf, email, senha, tipo_pessoa
                FROM pessoa
                WHERE cpf = '{cpf_db}';
            """)

            postgres.write(f"DELETE FROM pessoa WHERE cpf = '{cpf_db}';")

            pessoa_excluida = Pessoa(
                id_pessoa=df_pessoa.id_pessoa.values[0],
                nome=df_pessoa.nome.values[0],
                cpf=df_pessoa.cpf.values[0],
                email=df_pessoa.email.values[0],
                senha=df_pessoa.senha.values[0],
                tipo_pessoa=df_pessoa.tipo_pessoa.values[0]
            )

            print("\nPessoa foi removida")
            print(pessoa_excluida.to_string())

            return pessoa_excluida

        except Exception as e:
            logger.log_exception(e, context='excluir_pessoa')
            print("Ocorreu um erro ao excluir a pessoa. Tente novamente mais tarde.")
            return None
        finally:
            if postgres:
                postgres.close()

    def verifica_existencia_pessoa(self, postgres: PostgresQueries, cpf: str) -> bool:
        # assegura que a conexão/ cursor estejam inicializados antes de executar
        if postgres.cur is None:
            postgres.connect()

        df_pessoa = postgres.sqlToDataFrame(f"SELECT cpf FROM pessoa WHERE cpf = '{cpf}';")
        return not df_pessoa.empty


    #Já mexi nesse método, adicionei ele para diminuir a quantidade de chamadas no banco
    def verifica_existencia_pessoa_por_id(self, mongo: MongoQueries, id_mongo: ObjectId) -> bool:
        if mongo.cur is None:
            mongo.connect()

        doc_pessoa = mongo.db["pessoa"].find_one({"_id": id_mongo}, {"_id" : 1})
        return doc_pessoa is not None
    

    def validar_pessoa(self, postGree: PostgresQueries, cpf_pessoa: str = None) -> Pessoa:
        try:
            if cpf_pessoa is None:
                print("CPF é obrigatório para validar pessoa.")
                return None
            cpf_db = validation.normalize_numeric_field(cpf_pessoa)
            if not self.verifica_existencia_pessoa(postGree, cpf_db):
                print(f"A pessoa de CPF: {cpf_pessoa} informado não existe.")
                return None

            postGree.connect()
            df_pessoa = postGree.sqlToDataFrame(
                f"select id_pessoa, nome, cpf, email, senha, tipo_pessoa from Pessoa where cpf = '{cpf_db}'")

            if df_pessoa.empty:
                print("Erro interno: Pessoa não encontrada.")
                return None

            pessoa = Pessoa(df_pessoa.id_pessoa.values[0], df_pessoa.nome.values[0], cpf_db,
                            df_pessoa.email.values[0], df_pessoa.senha.values[0], df_pessoa.tipo_pessoa.values[0])

            return pessoa
        except Exception as e:
            logger.log_exception(e, context='validar_pessoa')
            print("Ocorreu um erro ao validar a pessoa. Tente novamente mais tarde.")
            return None
