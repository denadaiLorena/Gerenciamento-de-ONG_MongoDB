from conexion.connection import MongoQueries


class Relatorio:
    def __init__(self):
        pass
        self.mongo = MongoQueries()

    def get_relatorio_campanhas(self):
        self.mongo.connect()

        pipeline = [
            {
                "$match": {"status": True}
            },


            {
                "$lookup": {
                    "from": "pessoas",
                    "localField": "id_pessoa",
                    "foreignField": "id_pessoa",
                    "as": "pessoa_responsavel"
                }
            },
            {
                "$unwind": {
                    "path": "$pessoa_responsavel",
                    "preserveNullAndEmptyArrays": True
                }
            },


            {
                "$lookup": {
                    "from": "doacoes",
                    "localField": "id_campanha",
                    "foreignField": "id_campanha",
                    "as": "doacoes"
                }
            },


            {
                "$addFields": {
                    "total_de_doacoes": {"$size": "$doacoes"},
                    "valor_total_arrecadado": {"$sum": "$doacoes.valor"}
                }
            },


            {
                "$project": {
                    "_id": 0,
                    "id_campanha": 1,
                    "nome_campanha": "$nome",
                    "descricao": 1,
                    "pessoa_responsavel": "$pessoa_responsavel.nome",
                    "data_inicio": 1,
                    "data_fim": 1,
                    "status": 1,
                    "total_de_doacoes": 1,
                    "valor_total_arrecadado": 1
                }
            },


            {
                "$sort": {
                    "valor_total_arrecadado": -1,
                    "nome_campanha": 1
                }
            }
        ]

        resultado = list(self.mongo.db["campanhas"].aggregate(pipeline))

        print(resultado)
        input("Pressione Enter para Sair do Relatório de Campanhas\n")

    def get_relatorio_doacoes(self):
        self.mongo.connect()

        pipeline = [

            {
                "$lookup": {
                    "from": "pessoas",
                    "localField": "id_pessoa",
                    "foreignField": "id_pessoa",
                    "as": "doador"
                }
            },
            {"$unwind": "$doador"},


            {
                "$lookup": {
                    "from": "campanhas",
                    "localField": "id_campanha",
                    "foreignField": "id_campanha",
                    "as": "campanha"
                }
            },
            {"$unwind": "$campanha"},


            {
                "$project": {
                    "_id": 0,
                    "id_doacao": 1,
                    "nome_doador": "$doador.nome",
                    "cpf": "$doador.cpf",
                    "id_campanha": "$campanha.id_campanha",
                    "nome_campanha": "$campanha.nome",
                    "valor_doacao": "$valor",
                    "data_doacao": 1
                }
            },


            {
                "$sort": {
                    "data_doacao": -1,
                    "nome_doador": 1
                }
            }
        ]

        resultado = list(self.mongo.db["doacoes"].aggregate(pipeline))
        print(resultado)
        input("Pressione Enter para Sair do Relatório de Doações\n")

    def get_relatorio_pessoas(self):
        self.mongo.connect()

        pipeline = [
            {
                "$project": {
                    "_id": 0,
                    "id_pessoa": 1,
                    "nome": 1,
                    "cpf": 1,
                    "tipo_pessoa": 1
                }
            },
            {
                "$sort": {"nome": 1}
            }
        ]

        resultado = list(self.mongo.db["pessoas"].aggregate(pipeline))
        print(resultado)
        input("Pressione Enter para Sair do Relatório de Pessoas")
