from controller.controller_pessoa import Controller_Pessoa
from model.formaPagamento import FormaPagamento
from conexion.connection import PostgresQueries
from model.pessoa import Pessoa
from model.campanha import Campanha

class Controller_FormaPagamento:
    def __init__(self):
        self.control_pessoa = Controller_Pessoa()
        # Controller_Campanha pode causar import circular se importado no topo;
        # importe localmente quando necessário.


    def inserir_formaPagamento(self, postGree: PostgresQueries, campanha: Campanha) -> FormaPagamento:
        id_campanha = int(campanha.get_id_campanha())

        pessoa = campanha.get_pessoa()
        id_pessoa = int(pessoa.get_id_pessoa())

        cpf_pessoa = pessoa.get_cpf()

        pessoa = self.validar_pessoa(postGree, cpf_pessoa)
        if pessoa is None:
            print("Pessoa responsável inválida.")
            return None
        
        descricao = campanha.get_forma_pagamento()

        params = dict(id_campanha=id_campanha, id_pessoa=id_pessoa, descricao=descricao)

        # use cursor existente ou conecte se necessário
        if postGree.cur is None:
            cursor = postGree.connect()
        else:
            cursor = postGree.cur

        try:
            cursor.execute(
                """
                INSERT INTO formapagamento (id_campanha, id_pessoa, descricao)
                VALUES (%(id_campanha)s, %(id_pessoa)s, %(descricao)s)
                RETURNING id_forma_pagamento;
                """,
                params,
            )

            id_forma = cursor.fetchone()[0]
            postGree.conn.commit()

            forma_de_pagamento = FormaPagamento(id_forma, descricao, campanha, pessoa)

            print("\nForma de pagamento cadastrada com sucesso!")
            print(forma_de_pagamento.toString())
            return forma_de_pagamento
        except Exception as e:
            print(f"Erro ao inserir forma de Pagamento: {e}.")
            return None

    
    def atualizar_formaPagamento(self, id_campanha: int, id_pessoa_respon: int, nome_forma: str) -> bool:
        postGree = PostgresQueries(can_write=True)
        postGree.connect()
        
        try:
            postGree.write(f"update formapagamento set descricao = '{nome_forma}' where id_campanha = {id_campanha} and id_pessoa = {id_pessoa_respon};")
            return True
        except Exception as e:
            print(f"Erro ao salvar a forma de Pagamento: {e}")
            return False


    def executar_atualizar_formaPagamento(self, postGree)-> bool:
        try:
            id_campanha_alvo = int(input("Informe o ID da Campanha: "))
            cpf_pessoa_respon = str(input("Informe o CPF da Pessoa Responsável (para identificação):"))

            pessoa = self.validar_pessoa(postGree, cpf_pessoa_respon)
            if pessoa is None:
                print("Pessoa Responsável não encontrada.")
                return False
            
            id_pessoa_respon = pessoa.get_id_pessoa()

            novo_nome_forma = str(input("Informe a nova Forma de Pagamento: "))
            sucesso = self.atualizar_formaPagamento(id_campanha_alvo, id_pessoa_respon, novo_nome_forma)

            if sucesso:
                print(f"A Forma de Pagamento da Campanha {id_campanha_alvo} foi atualizada para {novo_nome_forma}!")
                return True
            
            print(f"Falha na atualização da Forma de Pagamento no Banco de dados.")
            return False
        except ValueError:
            print("Entrada inválida.Certifique-se de usar números para os IDs.")
            return False


    def listar_campanhas_formaPag(self, postGree: PostgresQueries, need_connect:bool=False):
            query = """
                    select fp.id_forma_pagamento,
                    fp.descricao AS forma_de_pagamento,
                    fp.id_campanha,
                    c.nome AS nome_campanha,
                    c.data_inicio,
                    c.status,
                    fp.id_pessoa
                    from formapagamento fp
                    inner join Campanha c ON fp.id_campanha = c.id_campanha
                    order by c.nome, fp.descricao;
                    """
            if need_connect:
                postGree.connect()
            print(postGree.sqlToDataFrame(query))
    

    def validar_pessoa(self, postGree: PostgresQueries, cpf_pessoa: str=None) -> Pessoa:
        if not self.control_pessoa.verifica_existencia_pessoa(postGree, cpf_pessoa):
            print(f"A pessoa de CPF: {cpf_pessoa} informado não existe.")
            return None
        else:
            postGree.connect()
            df_pessoa = postGree.sqlToDataFrame(f"select id_pessoa, nome, cpf, email, senha, tipo_pessoa from Pessoa where cpf = '{cpf_pessoa}'")

            if df_pessoa.empty:
                print(f"Erro ao recuperar dados da Pessoa {cpf_pessoa}.")
                return None
            
            pessoa = Pessoa(df_pessoa.id_pessoa.values[0], df_pessoa.nome.values[0], df_pessoa.cpf.values[0], df_pessoa.email.values[0], df_pessoa.senha.values[0], df_pessoa.tipo_pessoa.values[0])
            return pessoa
        

    def validar_campanha(self, postGree: PostgresQueries, id_campanha: int) -> Campanha:
        postGree.connect()
        query_campanha = f"""
            SELECT c.id_campanha, c.nome, c.descricao, c.data_inicio, c.data_fim, c.formapagamento AS formaPagamento, p.cpf
            FROM campanha c
            JOIN pessoa p ON c.id_pessoa = p.id_pessoa
            WHERE c.id_campanha = {id_campanha}
        """

        df_campanha = postGree.sqlToDataFrame(query_campanha)

        if df_campanha.empty:
            print("Campanha não encontrada com o ID informado.")
            return None

        cpf_pessoa = df_campanha.cpf.values[0]

        pessoa = self.validar_pessoa(postGree, cpf_pessoa)
        if pessoa is None:
            print("A Pessoa informada não é válida.")
            return None

        dados = df_campanha.iloc[0]
        campanha = Campanha(dados.id_campanha, pessoa, dados.nome, dados.descricao, dados.data_inicio, dados.data_fim, dados.formaPagamento)
        return campanha
    

    def verificar_existencia_formaPagamento(self, postGree: PostgresQueries, id_forma: int) -> bool:
        # coluna primária é id_forma_pagamento segundo create_tables_ong.sql
        df_formaPagamento = postGree.sqlToDataFrame(f"select id_forma_pagamento from formapagamento where id_forma_pagamento = {id_forma}")
        return not df_formaPagamento.empty