from bson import ObjectId
from controller.controller_pessoa import Controller_Pessoa
from model.formaPagamento import FormaPagamento
from conexion.connection import MongoQueries
from model.pessoa import Pessoa
from model.campanha import Campanha

class Controller_FormaPagamento:
    def __init__(self):
        self.control_pessoa = Controller_Pessoa()
        self.colecao = "formapagamento"
        self.mongo = MongoQueries()


    def inserir_formaPagamento(self, campanha: Campanha) -> FormaPagamento:
        id_campanha = int(campanha.get_id_campanha())

        pessoa = campanha.get_pessoa()
        id_pessoa = pessoa.get_id_pessoa()

        cpf_pessoa = pessoa.get_cpf()

        pessoa = self.control_pessoa.validar_pessoa( self.mongo, cpf_pessoa)
        if pessoa is None:
            print("Pessoa responsável inválida.")
            return None
        
        descricao = campanha.get_forma_pagamento()

        doc_formapagamento = {
            "id_campanha" : id_campanha,
            "id_pessoa" : id_pessoa,
            "formapagamento": descricao
        }

        try:
            self.mongo.connect()
            resultado =  self.mongo.db[self.colecao].insert_one(doc_formapagamento)
            id_forma = str(resultado.inserted_id)

            forma_de_pagamento = FormaPagamento(id_forma, descricao, campanha, pessoa)

            print("\nForma de pagamento cadastrada com sucesso!")
            print(forma_de_pagamento.toString())
            return forma_de_pagamento
        except Exception as e:
            print(f"Erro ao inserir forma de Pagamento: {e}.")
            return None

    
    def atualizar_formaPagamento(self, id_campanha: ObjectId, id_pessoa_respon: ObjectId, nome_forma: str) -> bool:

        try:
            self.mongo.connect()
            self.mongo.db[self.colecao].update_one({"_id": id_campanha, "id_pessoa": id_pessoa_respon}, {"$set": {
                                        "descricao": nome_forma}})
            return True
        except Exception as e:
            print(f"Erro ao salvar a forma de Pagamento: {e}")
            return False


    def executar_atualizar_formaPagamento(self)-> bool:
        try:
            id_campanha_alvo = ObjectId(input("Informe o ID da Campanha: "))
            cpf_pessoa_respon = str(input("Informe o CPF da Pessoa Responsável (para identificação):"))

            pessoa = self.control_pessoa.validar_pessoa(self.mongo, cpf_pessoa_respon)
            if pessoa is None:
                print("Pessoa Responsável não encontrada.")
                return False
            
            id_pessoa_respon = ObjectId(pessoa.get_id_pessoa())

            novo_nome_forma = str(input("Informe a nova Forma de Pagamento: "))
            sucesso = self.atualizar_formaPagamento(self.mongo, id_campanha_alvo, id_pessoa_respon, novo_nome_forma)

            if sucesso:
                print(f"A Forma de Pagamento da Campanha {id_campanha_alvo} foi atualizada para {novo_nome_forma}!")
                return True
            
            print(f"Falha na atualização da Forma de Pagamento no Banco de dados.")
            return False
        except ValueError:
            print("Entrada inválida.Certifique-se de usar números para os IDs.")
            return False


    def listar_campanhas_formaPag(self, need_connect:bool=False):
        pipeline = [
          
            {
                '$lookup': {
                    'from': 'campanha',         # Coleção de destino do JOIN
                    'localField': 'id_campanha',  # Campo em 'formapagamento' (fp.id_campanha)
                    'foreignField': 'id_campanha', # Campo em 'campanha' (c.id_campanha)
                    'as': 'dados_campanha'      # Nome do array resultante (temporário)
                }
            },
          
            {
                '$unwind': '$dados_campanha'
            },
           
            {
                '$project': {
                    '_id': 0, # Exclui o _id da forma de pagamento, se desejar
                    'id_forma_pagamento': '$_id', # Renomeia o _id do documento para id_forma_pagamento
                    'forma_de_pagamento': '$descricao',
                    'id_campanha': '$id_campanha',
                    'id_pessoa': '$id_pessoa',
                    'nome_campanha': '$dados_campanha.nome',
                    'data_inicio': '$dados_campanha.data_inicio',
                    'status': '$dados_campanha.status',
                }
            },
         
            {
                '$sort': {
                    'nome_campanha': 1, # 1 para ordem ascendente (A-Z)
                    'forma_de_pagamento': 1
                }
            }
        ]

        try:
            if need_connect:
                self.mongo.connect()
                
            resultados = list(self.mongo.db[self.colecao].aggregate(pipeline))
            print("\n--- Formas de Pagamento e Campanhas (MongoDB) ---")
           
            for doc in resultados:
                print(doc)
                
        except Exception as e:
            print(f"Erro ao listar Formas de Pagamento: {e}")
    
        
    def validar_campanha(self, id_campanha: ObjectId) -> Campanha:
        self.mongo.connect()
        doc_campanha = self.mongo.db["campanha"].find_one({"_id" : id_campanha}, {
                                                    "_id": 1,
                                                    "id_pessoa": 1,
                                                    "nome": 1,
                                                    "descricao": 1,
                                                    "data_inicio": 1,
                                                    "data_fim": 1,
                                                    "formapagamento": 1,
        })

       

        if doc_campanha is None:
            print("Campanha não encontrada com o ID informado.")
            return None

        id_pessoa = ObjectId(doc_campanha.get("id_pessoa"))

        pessoa = self.control_pessoa.validar_pessoa_por_id(id_pessoa)
        if pessoa is None:
            print("A Pessoa informada não é válida.")
            return None

        campanha = Campanha(doc_campanha.get("_id"), pessoa, doc_campanha.get("nome"), doc_campanha.get("descricao"), doc_campanha.get("data_inicio"), doc_campanha.get("data_fim"), doc_campanha.get("formaPagamento"))
        return campanha
    

    def verificar_existencia_formaPagamento(self, id_forma: ObjectId) -> bool:
        doc_formapagamento = self.mongo.db[self.colecao].find_one({"_id" : id_forma}, {"_id" : 1})
        return doc_formapagamento is not None