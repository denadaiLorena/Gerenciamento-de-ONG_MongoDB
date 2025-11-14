from __future__ import annotations
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from model.doacao import Doacao


class Pessoa:
    def __init__(self,
                 id_pessoa: str = None,
                 nome: str = None,
                 cpf: str = None,
                 email: str = None,
                 senha: str = None,
                 tipo_pessoa: str = "doador",
                 doacoes: List['Doacao'] = None):
        self.set_id_pessoa(id_pessoa)
        self.set_nome(nome)
        self.set_cpf(cpf)
        self.set_email(email)
        self.set_senha(senha)
        self.set_tipo_pessoa(tipo_pessoa)
        self.doacoes = [] if doacoes is None else doacoes

    def set_id_pessoa(self, id_pessoa: str):
        self.id_pessoa = id_pessoa

    def set_nome(self, nome: str):
        self.nome = nome

    def set_cpf(self, cpf: str):
        self.cpf = cpf

    def set_email(self, email: str):
        self.email = email

    def set_senha(self, senha: str):
        self.senha = senha

    def set_tipo_pessoa(self, tipo_pessoa: str):
        if tipo_pessoa not in ("doador", "usuario"):
            raise ValueError("tipo_pessoa deve ser 'doador' ou 'usuario'")
        self.tipo_pessoa = tipo_pessoa

    def set_doacoes(self, doacoes: List['Doacao']):
        self.doacoes = doacoes

    def get_doacoes(self) -> List['Doacao']:
        return self.doacoes
    
    def add_doacao(self, doacao: 'Doacao'):
        self.doacoes.append(doacao)

    def get_id_pessoa(self) -> str:
        return self.id_pessoa

    def get_nome(self) -> str:
        return self.nome

    def get_cpf(self) -> str:
        return self.cpf

    def get_email(self) -> str:
        return self.email

    def get_senha(self) -> str:
        return self.senha

    def get_tipo_pessoa(self) -> str:
        return self.tipo_pessoa

    def to_string(self) -> str:
        return f"ID: {self.get_id_pessoa()} | Nome: {self.get_nome()} | Email: {self.get_email()} | Tipo: {self.get_tipo_pessoa()}"