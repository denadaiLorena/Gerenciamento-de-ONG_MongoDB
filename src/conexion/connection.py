import pymongo
from pymongo.errors import ConnectionFailure

class MongoQueries:
    def __init__(self):
        self.host = "bdong-nhui.j.aivencloud.com"
        self.port = 27017
        self.service_name = "sistema_doacoes"
        self.mongo_client = None

        with open("src/conexion/passphrase/authentication.pg", "r") as f:
            self.user, self.passwd = f.read().split(',')

    def __del__(self):
        if hasattr(self, "mongo_client"):
            self.close() 

    def connect(self):
        if self.user is None or self.passwd is None:
            raise ConnectionFailure("Credenciais não carregadas.")
        
        self.sistema_doacoes = pymongo.MongoClient(f"mongodb://{self.user}:{self.passwd}@{self.host}:{self.port}/")
        self.db = self.mongo_client[self.service_name]

    def close(self):
        if  self.mongo_client:
            self.close()