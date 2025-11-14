from __future__ import annotations
from typing import TYPE_CHECKING
from decimal import Decimal
from datetime import datetime

if TYPE_CHECKING:
    from .recibo import Recibo


class Doacao:
    def __init__(self,
                 id_doacao: int = None,
                 id_pessoa: int = None,
                 id_campanha: int = None,
                 valor: Decimal = None,
                 data_doacao: datetime = None,
                 recibo: 'Recibo' = None):

        self.set_id_doacao(id_doacao)
        self.set_id_pessoa(id_pessoa)
        self.set_id_campanha(id_campanha)
        self.set_valor(valor)
        self.set_data_doacao(data_doacao)
        self.set_recibo(recibo)

    def set_id_doacao(self, id_doacao: int):
        self._id_doacao = id_doacao

    def set_id_pessoa(self, id_pessoa: int):
        self._id_pessoa = id_pessoa

    def set_id_campanha(self, id_campanha: int):
        self._id_campanha = id_campanha

    def set_valor(self, valor: Decimal):
        self._valor = Decimal(valor) if valor is not None else None

    def set_data_doacao(self, data_doacao: datetime):
        self._data_doacao = data_doacao if data_doacao is not None else datetime.now()
        
    def set_recibo(self, recibo: 'Recibo'):
        self._recibo = recibo

    def get_id_doacao(self) -> int:
        return self._id_doacao

    def get_id_pessoa(self) -> int:
        return self._id_pessoa

    def get_id_campanha(self) -> int:
        return self._id_campanha

    def get_valor(self) -> Decimal:
        return self._valor

    def get_data_doacao(self) -> datetime:
        return self._data_doacao

    def get_recibo(self) -> 'Recibo':
        return self._recibo

    def to_string(self) -> str:
        data_formatada = self.get_data_doacao().strftime('%d/%m/%Y %H:%M:%S')
        valor_formatado = f"R$ {self.get_valor()}" if self.get_valor() is not None else "N/A"

        return (f"ID: {self.get_id_doacao()} | "
                f"ID Pessoa: {self.get_id_pessoa()} | "
                f"ID Campanha: {self.get_id_campanha()} | "
                f"Valor: {valor_formatado} | "
                f"Data: {data_formatada}")