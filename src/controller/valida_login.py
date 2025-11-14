from conexion.connection import PostgresQueries


class ValidaLogin:
    def fazer_login(self):
        print("\n=== LOGIN ===")
        nome = input("Nome: ")
        senha = input("Senha: ")

        sql = f"""
            SELECT id_pessoa, nome, tipo_pessoa
            FROM pessoa
            WHERE nome = '{nome}' AND senha = '{senha}';
        """

        # garante que a conexão existe
        if not hasattr(self, "postgres") or self.postgres is None:
            self.postgres = PostgresQueries(can_write=False)
            self.postgres.connect()

        df_usuario = self.postgres.sqlToDataFrame(sql)

        if df_usuario.empty:
            print("\n Nome ou senha incorretos. Tente novamente.")
            return self.iniciar_programa()

        tipo = df_usuario.tipo_pessoa.values[0]
        nome = df_usuario.nome.values[0]
        id_pessoa = int(df_usuario.id_pessoa.values[0])
        print(f"\n\u2705 Login realizado com sucesso! Bem-vindo(a), {nome}.")

        # Retorna tipo, nome e id_pessoa para que o programa possa utilizar o usuário logado
        return tipo, nome, id_pessoa

    def menu_doador(self, nome):
        print(f"""
        === MENU DOADOR ===
        Olá, {nome}! Você pode:
        1. Visualizar relatórios
        2. Atualizar seu perfil
        3. Fazer doação
        0. Deslogar
        """)

    def menu_usuario(self, nome):
        print(f"""
        === MENU ADMINISTRADOR ===
        Olá, {nome}! Você pode:
        1. Criar campanhas
        2. Ver relatórios
        3. Fazer doações
        4. Atualizar seu perfil
        5. Gerenciar CRUD de doadores
        0. Deslogar
        """)

    def iniciar_programa(self):
        print("""
        === SISTEMA DE DOAÇÕES ===
        1. Cadastrar-se
        2. Fazer login
        """)
        opcao = input("Escolha uma opção (1 ou 2): ")

        if opcao == "1":
            from controller.controller_pessoa import Controller_Pessoa
            controller = Controller_Pessoa()
            controller.inserir_pessoa()
            return self.iniciar_programa()  # volta para login após cadastro
        elif opcao == "2":
            return self.fazer_login()  # retorna tipo, nome e id_pessoa
        else:
            print("Opção inválida.")
            return self.iniciar_programa()
