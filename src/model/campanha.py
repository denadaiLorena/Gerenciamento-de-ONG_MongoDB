from datetime import date
from .pessoa import Pessoa

class Campanha:
    def __init__(self,
                 id_campanha: str = None,
                 pessoa: Pessoa = None,
                 nome: str = None,
                 descricao: str = None,
                 data_inicio: date = None,
                 data_fim: date = None,
                 forma_pagamento: str = None,
                ):
        self.id_campanha = id_campanha
        self.set_pessoa(pessoa)
        self.set_nome(nome)
        self.set_descricao(descricao)
        self.set_data_inicio(data_inicio)
        self.set_data_fim(data_fim)
        self.set_forma_pagamento(forma_pagamento)
        self.ativar()
       
    
    def set_pessoa(self, pessoa: Pessoa):
        self.pessoa = pessoa

    def set_nome(self, nome: str):
        self.nome = nome

    def set_descricao(self, descricao: str):
        self.descricao = descricao

    def set_data_inicio(self, data_inicio: date):
        self.data_inicio = data_inicio

    def set_data_fim(self, data_fim: date):
        self.data_fim = data_fim

    def set_forma_pagamento(self, forma_pagamento: str):
        self.forma_pagamento = forma_pagamento

    def ativar(self):
        self.status = True

    def desativar(self):
        self.status = False


    def get_id_campanha(self) -> str:
        return self.id_campanha

    def get_pessoa(self) -> Pessoa:
        return self.pessoa

    def get_nome(self) -> str:
        return self.nome

    def get_descricao(self) -> str:
        return self.descricao

    def get_data_inicio(self) -> date:
        return self.data_inicio

    def get_data_fim(self)  -> date:
        return self.data_fim

    def is_ativa(self) -> bool:
        return self.status

    def get_forma_pagamento(self) -> str:
        return self.forma_pagamento


    def toString(self) -> str:
        return (f"Campanha: {self.get_id_campanha()} | Pessoa Responsável: {self.pessoa.get_nome()} | Nome: {self.get_nome()} | Descrição: {self.get_descricao()} \nData de Início: {self.get_data_inicio()} | Data de Fim: {self.get_data_fim()} | Ativa: {self.is_ativa()} | Forma de Pagamento aceita: {self.get_forma_pagamento()}")