import os
from time import sleep

MENU_PRINCIPAL = """
================== MENU PRINCIPAL ==================
1 - Relatórios
2 - Inserir Registros
3 - Atualizar Registros
4 - Excluir Registros
5 - Sair
===================================================="""

MENU_RELATORIOS = """
-- Menu de Relatórios --
1 - Relatório de Campanhas - total arrecadado e o número de doações para cada campanha ativa
2 - Relatório de Doações - doadores que contribuíram para quais campanhas, e qual foi o valor doado por eles em cada transação
"""

MENU_ENTIDADES = """
-- Escolha uma entidade --
1 - Pessoa
2 - Campanha
"""

MENU_ATUALIZAR_ENTIDADES = """
-- Escolha uma entidade --
1 - Pessoa
2 - Campanha
3 - Doação
4 - Forma de Pagamento
"""


QUERY_COUNT = 'SELECT COUNT(1) AS total_{tabela} FROM {tabela}'

def clear_console(wait_time:int=1):
    sleep(wait_time)
    os.system('cls' if os.name == 'nt' else 'clear')