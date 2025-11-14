from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime
from uuid import UUID, uuid4

if TYPE_CHECKING:
    from .doacao import Doacao


class Recibo:
    def __init__(self,
                 id_recibo: int = None,
                 data_emissao: datetime = None,
                 codigo_validacao: UUID = None,
                 doacao: 'Doacao' = None):
        self.set_id_recibo(id_recibo)
        self.set_data_emissao(data_emissao)
        self.set_codigo_validacao(codigo_validacao)
        self.set_doacao(doacao)

    def set_id_recibo(self, id_recibo: int):
        self._id_recibo = id_recibo

    def set_data_emissao(self, data_emissao: datetime):
        self._data_emissao = data_emissao if data_emissao is not None else datetime.now()

    def set_codigo_validacao(self, codigo_validacao: UUID):
        self._codigo_validacao = codigo_validacao if codigo_validacao is not None else uuid4()

    def set_doacao(self, doacao: 'Doacao'):
        self._doacao = doacao

    def get_doacao(self) -> 'Doacao':
        return self._doacao

    def get_id_recibo(self) -> int:
        return self._id_recibo

    def get_data_emissao(self) -> datetime:
        return self._data_emissao

    def get_codigo_validacao(self) -> UUID:
        return self._codigo_validacao

    def to_string(self) -> str:
        data_formatada = self.get_data_emissao().strftime('%d/%m/%Y %H:%M:%S')
        id_doacao = self.get_doacao().get_id_doacao() if self.get_doacao() else "N/A"
        
        return (f"ID: {self.get_id_recibo()} | "
                f"Data de Emissão: {data_formatada} | "
                f"Código: {self.get_codigo_validacao()} | "
                f"ID Doação: {id_doacao}")