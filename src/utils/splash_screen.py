from conexion.connection import PostgresQueries

class SplashScreen:

    def __init__(self):
        self.created_by = [
            "Hevellyn Monteiro Medeiros",
            "Lorena Moreira De Nadai",
            "Natalia Pianca Martins",
            "Wanessa Silva Guisso"
        ]
        self.professor = "Prof. M.Sc. Howard Roatti"
        self.disciplina = "Banco de Dados"
        self.semestre = "2025/2"

    def contar_registros(self, tabela: str) -> int:
        postGree = PostgresQueries()
        postGree.connect()
        try:
            query = f"SELECT COUNT(1) as total FROM {tabela}"
            df = postGree.sqlToDataFrame(query)
            total = df.total[0] if not df.empty else 0
            return total
        except Exception as e:
            print(f"Erro ao contar registros da tabela {tabela}: {e}")
            return 0

    def get_updated_screen(self):
        total_pessoas = self.contar_registros("pessoa")
        total_campanhas = self.contar_registros("campanha")

        largura_total = 56
        
        def criar_linha(texto_interno: str = "") -> str:
            if texto_interno == "":
                return "#" + " " * (largura_total - 2) + "#\n"
            
            texto_formatado = f"#  {texto_interno}"
            return texto_formatado.ljust(largura_total - 1) + "#\n"

        screen =  "#" * largura_total + "\n"
        screen += criar_linha()
        screen += criar_linha("SISTEMA DE DOAÇÕES PARA ONG")
        screen += criar_linha()
        screen += criar_linha("TOTAL DE REGISTROS:")
        
        linha_pessoas = f"    1 - PESSOAS:     {str(total_pessoas).rjust(5)}"
        screen += criar_linha(linha_pessoas)
        
        linha_campanhas = f"    2 - CAMPANHAS:   {str(total_campanhas).rjust(5)}"
        screen += criar_linha(linha_campanhas)
        
        screen += criar_linha()
        
        linha_criado_por = f"CRIADO POR: {self.created_by[0]}"
        screen += criar_linha(linha_criado_por)
        
        padding_nomes = " " * 12
        for nome in self.created_by[1:]:
            screen += criar_linha(f"{padding_nomes}{nome}")
            
        screen += criar_linha()
        screen += criar_linha(f"PROFESSOR:  {self.professor}")
        screen += criar_linha()
        screen += criar_linha(f"DISCPLINA: {self.disciplina}")
        screen += criar_linha(f"            {self.semestre}")
        screen += "#" * largura_total + "\n"
        
        return screen