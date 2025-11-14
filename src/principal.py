from utils import config
from utils.splash_screen import SplashScreen
from reports.relatorios import Relatorio
from controller.controller_pessoa import Controller_Pessoa
from controller.controller_campanha import Controller_Campanha
from controller.valida_login import ValidaLogin
from controller.controller_doacao import Controller_Doacao
from controller.controller_formaPagamento import Controller_FormaPagamento
from conexion.connection import PostgresQueries

# melhoria de UI: cores
from colorama import init as colorama_init, Fore, Style
colorama_init(autoreset=True)


# Instâncias de controllers e utilitários
tela_inicial = SplashScreen()
relatorio = Relatorio()
ctrl_pessoa = Controller_Pessoa()
ctrl_campanha = Controller_Campanha()
ctrl_doacao = Controller_Doacao()
ctrl_formaPagamento = Controller_FormaPagamento()
login = ValidaLogin()
from utils import logger


def admin_menu_loop(nome_usuario: str, id_pessoa_logado: int):
    """Loop de menu para usuários do tipo 'usuario' (administrador)."""
    while True:
        login.menu_usuario(nome_usuario)
        opc = input("Escolha uma opção: ").strip()

        if opc == '1':
            # Criar campanha
            ctrl_campanha.inserir_campanha()

        elif opc == '2':
            # Ver relatórios (submenu simples)
            print("\n1 - Relatório de campanhas\n2 - Relatório de doações\n3 - Relatório de pessoas")
            sub = input("Escolha: ").strip()
            if sub == '1':
                relatorio.get_relatorio_campanhas()
            elif sub == '2':
                relatorio.get_relatorio_doacoes()
            elif sub == '3':
                relatorio.get_relatorio_pessoas()
            else:
                print("Opção inválida.")

        elif opc == '3':
            # Fazer doação (admin pode doar como ele mesmo)
            # Exibir relatório de campanhas antes da doação
            relatorio.get_relatorio_campanhas()
            ctrl_doacao.inserir_doacao(id_pessoa_logado=id_pessoa_logado)

        elif opc == '4':
            # Atualizar próprio perfil
            ctrl_pessoa.atualizar_pessoa(id_pessoa_logado=id_pessoa_logado)

        elif opc == '5':
            # Gerenciar CRUD de pessoas (admin tem acesso completo)
            # Exibir relatório de pessoas antes do CRUD
            relatorio.get_relatorio_pessoas()
            print("\n1 - Inserir pessoa\n2 - Listar pessoas\n3 - Atualizar pessoa\n4 - Excluir pessoa")
            s = input("Escolha: ").strip()
            if s == '1':
                ctrl_pessoa.inserir_pessoa()
            elif s == '2':
                relatorio.get_relatorio_pessoas()
            elif s == '3':
                # admin escolhe CPF para atualizar
                ctrl_pessoa.atualizar_pessoa()
            elif s == '4':
                ctrl_pessoa.excluir_pessoa()
            else:
                print("Opção inválida.")

        elif opc == '0':
            # Sair (logout)
            print("Saindo da conta...")
            # Indica que o usuário fez logout
            return True
        else:
            print("Opção inválida. Tente novamente.")
    # Se por alguma razão o loop terminar, não foi logout
    return False


def donor_menu_loop(nome_usuario: str, id_pessoa_logado: int):
    """Loop de menu para doadores."""
    while True:
        login.menu_doador(nome_usuario)
        opc = input("Escolha uma opção: ").strip()

        if opc == '1':
            # Visualizar relatórios (campanhas e doações)
            print("\n1 - Relatório de campanhas\n2 - Relatório de doações")
            sub = input("Escolha: ").strip()
            if sub == '1':
                relatorio.get_relatorio_campanhas()
            elif sub == '2':
                relatorio.get_relatorio_doacoes()
            else:
                print("Opção inválida.")

        elif opc == '2':
            # Atualizar apenas o próprio cadastro
            ctrl_pessoa.atualizar_pessoa(id_pessoa_logado=id_pessoa_logado)

        elif opc == '3':
            # Fazer doação usando o perfil logado
            # Exibir relatório de campanhas antes da doação
            relatorio.get_relatorio_campanhas()
            ctrl_doacao.inserir_doacao(id_pessoa_logado=id_pessoa_logado)

        elif opc == '0':
            print("Saindo da conta...")
            return True
        else:
            print("Opção inválida. Tente novamente.")
    return False


def main():
    splash_shown = False

    while True:
        # Mostrar splash screen apenas na primeira vez que o programa é iniciado
        if not splash_shown:
            print(tela_inicial.get_updated_screen())
            input("\nPressione Enter para continuar...")
            config.clear_console()
            splash_shown = True

        # Tela inicial de login/cadastro
        try:
            resultado = login.iniciar_programa()
        except Exception as e:
            logger.log_exception(e, context='iniciar_programa')
            print("Ocorreu um erro inesperado. Você será redirecionado para a tela inicial.")
            config.clear_console()
            continue
        # iniciar_programa retorna (tipo, nome, id_pessoa)
        if not resultado:
            # Em caso de retorno inesperado, reinicia a tela inicial
            continue
        tipo_usuario, nome_usuario, id_pessoa_logado = resultado

        # Fluxo por tipo de usuário
        logged_out = False
        if tipo_usuario == 'usuario':
            logged_out = admin_menu_loop(nome_usuario, id_pessoa_logado)
        elif tipo_usuario == 'doador':
            logged_out = donor_menu_loop(nome_usuario, id_pessoa_logado)
        else:
            print(f"Tipo de usuário desconhecido: {tipo_usuario}. Voltando à tela inicial.")

        # Ao sair do menu do usuário (logout), retorna para a tela de login
        # Se o usuário deslogou, queremos que o splash apareça novamente
        if logged_out:
            splash_shown = False
        config.clear_console()


if __name__ == '__main__':
    main()
