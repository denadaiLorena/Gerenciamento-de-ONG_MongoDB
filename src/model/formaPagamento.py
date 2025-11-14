from model.campanha import Campanha
from model.pessoa import Pessoa


class FormaPagamento:
    def __init__(self,
                id_forma: int = None,
                forma_de_pagamento: str = None,
                campanha: Campanha = None,
                pessoa: Pessoa = None):
        self.set_id_forma(id_forma)
        self.set_forma_de_pagamento(forma_de_pagamento)
        self.set_campanha(campanha)
        self.set_pessoa(pessoa)
        
    def set_id_forma(self, id_forma: int):
        self.id_forma = id_forma

    def set_campanha(self, campanha: Campanha):
        self.campanha = campanha

    def set_pessoa(self, pessoa: Pessoa):
        self.pessoa = pessoa

    def set_forma_de_pagamento(self, forma_de_pagamento: str):
        self.forma_de_pagamento = forma_de_pagamento



    def get_id_forma(self):
        return self.id_forma

    def get_campanha(self) -> Campanha:
        return self.campanha

    def get_pessoa(self) -> Pessoa:
        return self.pessoa

    def get_forma_de_pagamento(self):
        return self.forma_de_pagamento


    def toString(self) -> str:
        return (f"\nForma de Pagamento: {self.get_forma_de_pagamento()} | Campanha: {self.campanha.get_nome()} | Pessoa Responsável: {self.pessoa.get_nome()}")