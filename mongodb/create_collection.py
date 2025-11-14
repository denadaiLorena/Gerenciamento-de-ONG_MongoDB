from pymongo import MongoClient

client = MongoClient("mongodb+srv://avnadmin:SistemaONG2025@bdong.thugnkf.mongodb.net/admin?retryWrites=true&w=majority&appName=bdong")

db = client["doacoesmongodb"]

collections = [
    "pessoas",
    "campanhas",
    "formas_pagamento",
    "doacoes",
    "recibos"
]

for col in collections:
    try:
        # cria collection (se já existir, ignora)
        db.create_collection(col)
        print(f"Collection criada: {col}")
    except:
        print(f"Collection já existe: {col}")

    # força a criação real (inserção inicial)
    db[col].insert_one({"__init__": True})

    # remove o documento de inicialização
    db[col].delete_one({"__init__": True})

# índices
db["pessoas"].create_index("cpf", unique=True)
db["pessoas"].create_index("email", unique=True)

print("\nTodas as collections criadas e visíveis!")
