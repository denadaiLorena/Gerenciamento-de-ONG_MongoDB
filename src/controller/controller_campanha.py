from datetime import date, datetime
from bson.objectid import ObjectId
import pandas as pd
from controller.controller_pessoa import Controller_Pessoa
from model.campanha import Campanha
from conexion.connection import MongoQueries

class Controller_Campanha:
    def __init__(self):
        self.control_pessoa = Controller_Pessoa()
        self.mongo = MongoQueries()
        self.colecao = "campanha"

    def inserir_campanha(self) -> Campanha:
        from controller.controller_formaPagamento import Controller_FormaPagamento
       
        cpf_pessoa = str(input("Digite o CPF da Pessoa: "))
        pessoa = self.control_pessoa.validar_pessoa(self.mongo, cpf_pessoa)
        if pessoa is None:
            return None

        id_pessoa_mongo = ObjectId(pessoa.get_id_pessoa())

        nome = str(input("Informe o nome da Campanha: "))
        descricao = str(input("Descrição da Campanha: "))

        data_i = input("Data de início(dd/mm/aaaa): ")
        data_inicio = datetime.strptime(data_i, "%d/%m/%Y").date()

        data_f = input("Data de término(dd/mm/aaaa): ")
        data_fim = datetime.strptime(data_f, "%d/%m/%Y").date()

        forma_de_pagamento = str(
            input("Informa a forma de Pagamento(obs* Apenas uma): "))

       
        self.mongo.connect()
        resultado = self.mongo.db["campanha"].insert_one({"id_pessoa": id_pessoa_mongo,
                                        "nome": nome,
                                        "descricao": descricao,
                                        "data_inicio": data_inicio,
                                        "data_fim": data_fim,
                                        "formaPagamento": forma_de_pagamento})
        
        novo_id = resultado.inserted_id
        nova_campanha = Campanha(novo_id, pessoa, nome, descricao, data_inicio, data_fim, forma_de_pagamento)

        # criar forma de pagamento vinculada
        control_formaPagamento = Controller_FormaPagamento()
        formaPagamento_obj = control_formaPagamento.inserir_formaPagamento(nova_campanha)

        if formaPagamento_obj is None:
            print("Erro ao adicionar a forma de pagamento")
            self.mongo.close()
            return None

        print("\nCampanha criada com sucesso!")
        print(nova_campanha.toString())

        self.mongo.close()
        return nova_campanha


    def atualizar_campanha(self) -> Campanha:
        self.mongo.connect()
        from controller.controller_formaPagamento import Controller_FormaPagamento

        id_campanha = input("Informe o ID da Campanha que irá alterar: ")
        id_campanha_mongo = ObjectId(id_campanha)

        if not self.verifica_existencia_campanha(id_campanha_mongo):
            print(f"A campanha de ID {id_campanha} não existe.")
            return None

        cpf_pessoa = str(input("Digite o CPF da Pessoa Responsável: "))
        pessoa = self.control_pessoa.validar_pessoa( self.mongo, cpf_pessoa)
        if pessoa == None:
            return None

        id_pessoa_respon = ObjectId(pessoa.get_id_pessoa())


        doc_campanha= self.mongo.db["campanha"].find_one({"_id":id_campanha_mongo},
                                                                       {"nome": 1,
                                                                        "descricao": 1,
                                                                        "data_inicio": 1,
                                                                        "data_fim": 1,
                                                                        "formaPagamento": 1,
                                                                        "_id" : 0})
        nome = doc_campanha.get("nome")
        descricao = doc_campanha.get("descricao")
        data_inicio = doc_campanha.get("data_inicio")
        data_fim = doc_campanha.get("data_fim")
        formaPagamento = doc_campanha.get("formaPagamento")

        if (input("Você quer alterar o nome da Campanha?(s/n) ").lower() == "s"):
            nome = str(input("Informe o nome da Campanha: "))

        if (input("Você quer alterar a descrção da Campanha?(s/n) ").lower() == "s"):
            descricao = str(input("Descrição da Campanha: "))

        if (input("Você quer alterar a data de início da Campanha?(s/n) ").lower() == "s"):
            data_i = input("Data de início(dd/mm/aaaa): ")
            data_inicio = datetime.strptime(data_i, "%d/%m/%Y").date()

        if (input("Você quer alterar a data de término da Campanha?(s/n) ").lower() == "s"):
            data_f = input("Data de término(dd/mm/aaaa): ")
            data_fim = datetime.strptime(data_f, "%d/%m/%Y").date()

        if (input("Você quer alterar a forma de pagamento da Campanha?(s/n) ").lower() == "s"):
            formaPagamento = str(
                input("Informe a Forma de Pagamento(obs* Apenas uma): "))
            control_formaPagamento = Controller_FormaPagamento()
            formaPagamento_obj = control_formaPagamento.atualizar_formaPagamento(
                id_campanha_mongo, id_pessoa_respon, formaPagamento)

            if formaPagamento_obj is None:
                print("Erro ao adicionar a forma de pagamento")
                return None


        self.mongo.db["campanha"].update_one({"_id": id_campanha_mongo}, {"$set": {"id_pessoa": id_pessoa_respon,
                                    "nome": nome,
                                    "descricao": descricao,
                                    "data_inicio": data_inicio,
                                    "data_fim": data_fim,
                                    "formaPagamento": formaPagamento}})


        campanha_atualizada = Campanha(id_campanha, pessoa, nome, descricao, data_inicio, data_fim, formaPagamento)
        print(campanha_atualizada.toString())

        return campanha_atualizada
      

    def desativar_campanha(self):
            self.mongo.connect()

            id_campanha = input("Informe o ID da Campanha que irá desativar: ")
            id_campanha_mongo = ObjectId(id_campanha)

            if not self.verifica_existencia_campanha(id_campanha_mongo):
                print(f"A campanha de ID {id_campanha} não existe.")
                return None

            doc_campanha = self.mongo.db["campanha"].find_one({"_id":id_campanha_mongo},
                                                                            {"id_pessoa": 1,
                                                                             "nome": 1,
                                                                            "descricao": 1,
                                                                            "data_inicio": 1,
                                                                            "data_fim": 1,
                                                                            "formaPagamento": 1,
                                                                            "_id": 0})
                

            if doc_campanha is None:
                print("Campanha não encontrada, apesar da verificação de existência.")
                return None
            
            id_pessoa = doc_campanha.get("id_pessoa")
            id_pessoa_mongo = ObjectId(id_pessoa)

            if not self.control_pessoa.verifica_existencia_pessoa_por_id(id_pessoa_mongo):
                print("Pessoa responsável não encontrada.")
                return None
            
            nome_campanha = doc_campanha.get("nome")
            opcao_desativar = input(f"Tem certeza que deseja desativar a campanha {nome_campanha} [S ou N]? ")
            if opcao_desativar.lower() == "s":
                self.mongo.db["campanha"].update_one({"_id" : id_campanha_mongo}, {"$set": {"status" : False}})
                   
                print("Campanha desativada com Sucesso!")


    def verifica_existencia_campanha(self, id_campanha_mongo: ObjectId = None) -> bool:
        doc_campanha = self.mongo.db["campanha"].find_one({"_id" : id_campanha_mongo, "status" : True}, {"_id" : 1})
        return doc_campanha is not None


    def buscar_campanhas_com_doacoes(self, need_connect: bool = True):
        pipeline = [
            {
                '$lookup': {
                    'from': 'doacao',            # Coleção alvo (tabela d)
                    'localField': 'id_campanha', # Campo na coleção 'campanha' (c.id_campanha)
                    'foreignField': 'id_campanha', # Campo na coleção 'doacao' (d.id_campanha)
                    'as': 'doacoes'              # Nome do array que conterá as doações
                }
            },
            {
                '$unwind': '$doacoes'
            },
            {
                '$lookup': {
                    'from': 'pessoa',          # Coleção alvo (tabela p)
                    'localField': 'doacoes.id_pessoa', # Campo na doacao (d.id_pessoa)
                    'foreignField': '_id',     # Campo na pessoa (p.id_pessoa ou _id, assumindo que id_pessoa referencia _id)
                    'as': 'doador'             # Nome do array que conterá a pessoa
                }
            },
            {
                '$unwind': '$doador'
            },
            {
                '$project': {
                    '_id': 0, # Oculta o _id da campanha
                    'id_campanha': '$id_campanha',
                    'nome_campanha': '$nome', # c.nome AS nome_campanha
                    'descricao': '$descricao',
                    'data_inicio': '$data_inicio',
                    'data_fim': '$data_fim',
                    'status': '$status',
                    'forma_pagamento_campanha': '$formaPagamento', # c.formapagamento AS forma_pagamento_campanha
                    
                    # Campos da Doação
                    'id_doacao': '$doacoes._id', # d.id_doacao (assumindo que o ID da doação é '_id')
                    'valor_doacao': '$doacoes.valor', # d.valor AS valor_doacao
                    
                    # Campos da Pessoa (Doador)
                    'nome_doador': '$doador.nome' # p.nome AS nome_doador
                }
            },
            {
                '$sort': {
                    'data_inicio': -1,     # c.data_inicio DESC
                    'nome_campanha': 1,    # nome_campanha ASC
                    'doacoes.data_doacao': 1 # d.data_doacao ASC (necessário referenciar o campo original)
                }
            }
        ]
        if need_connect:
            self.mongo.connect()
        print(list(self.mongo.db["campanha"].aggregate(pipeline)))
