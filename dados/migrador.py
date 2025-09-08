# usina_01/dados/migrador.py

from typing import Dict, Any
from nucleo.excecoes import ErroCarregamentoDados


class MigradorDados:
    """
    Responsável por migrar dados de versões antigas para a estrutura atual.
    Permite evolução da estrutura de dados sem perder compatibilidade.
    """

    # Versão atual da estrutura de dados
    VERSAO_ATUAL = "1.0"

    def __init__(self):
        # Dicionário que mapeia versões para suas respectivas funções de migração
        self.migracoes = {
            "0.9": self._migrar_de_0_9_para_1_0,
            # Futuras migrações podem ser adicionadas aqui
            # "1.0": self._migrar_de_1_0_para_1_1,
        }

    def migrar_se_necessario(self, dados: Dict[str, Any]) -> Dict[str, Any]:
        """
        Verifica se os dados precisam ser migrados e aplica as migrações necessárias.

        Args:
            dados: Dicionário com os dados carregados do JSON

        Returns:
            Dicionário com os dados migrados para a versão atual
        """
        versao_dados = dados.get('versao', '0.9')  # Assume versão 0.9 se não especificada

        if versao_dados == self.VERSAO_ATUAL:
            return dados  # Não precisa migrar

        print(f"Migrando dados da versão {versao_dados} para {self.VERSAO_ATUAL}...")

        # Aplica migrações sequenciais até chegar na versão atual
        dados_migrados = dados.copy()
        versao_atual = versao_dados

        while versao_atual != self.VERSAO_ATUAL:
            if versao_atual not in self.migracoes:
                raise ErroCarregamentoDados(
                    f"Não foi possível migrar dados da versão {versao_atual}. "
                    f"Migração não implementada."
                )

            dados_migrados = self.migracoes[versao_atual](dados_migrados)
            versao_atual = dados_migrados.get('versao', self.VERSAO_ATUAL)

        print(f"Migração concluída para a versão {self.VERSAO_ATUAL}.")
        return dados_migrados

    def _migrar_de_0_9_para_1_0(self, dados: Dict[str, Any]) -> Dict[str, Any]:
        """
        Migra dados da versão 0.9 para 1.0.

        Mudanças na versão 1.0:
        - Adiciona campo 'versao' aos dados
        - Garante que todos os campos obrigatórios estejam presentes
        - Normaliza nomes de meses para formato completo
        """
        dados_migrados = dados.copy()

        # 1. Adiciona versão aos dados
        dados_migrados['versao'] = '1.0'

        # 2. Garante que a estrutura básica existe
        if 'configuracao' not in dados_migrados:
            dados_migrados['configuracao'] = {
                'potencia_inversor': 0.0,
                'potencia_modulos': 0.0,
                'geracao_mensal': {},
                'eficiencia': 100.0,
                'valor_kwh': 0.6305
            }

        if 'unidades' not in dados_migrados:
            dados_migrados['unidades'] = []

        if 'consumos' not in dados_migrados:
            dados_migrados['consumos'] = {}

        # 3. Normaliza nomes de meses (caso existam abreviações)
        meses_mapping = {
            'Jan': 'Janeiro', 'Fev': 'Fevereiro', 'Mar': 'Março', 'Abr': 'Abril',
            'Mai': 'Maio', 'Jun': 'Junho', 'Jul': 'Julho', 'Ago': 'Agosto',
            'Set': 'Setembro', 'Out': 'Outubro', 'Nov': 'Novembro', 'Dez': 'Dezembro'
        }

        # Normaliza meses na geração mensal
        if 'geracao_mensal' in dados_migrados['configuracao']:
            geracao_normalizada = {}
            for mes, valor in dados_migrados['configuracao']['geracao_mensal'].items():
                mes_normalizado = meses_mapping.get(mes, mes)
                geracao_normalizada[mes_normalizado] = valor
            dados_migrados['configuracao']['geracao_mensal'] = geracao_normalizada

        # Normaliza meses nos consumos
        for codigo_uc, consumos_uc in dados_migrados['consumos'].items():
            consumos_normalizados = {}
            for mes, valor in consumos_uc.items():
                mes_normalizado = meses_mapping.get(mes, mes)
                consumos_normalizados[mes_normalizado] = valor
            dados_migrados['consumos'][codigo_uc] = consumos_normalizados

        # 4. Garante que todas as unidades têm os campos obrigatórios
        for unidade in dados_migrados['unidades']:
            if 'endereco' not in unidade:
                unidade['endereco'] = ""
            if 'tipo_ligacao' not in unidade:
                unidade['tipo_ligacao'] = 'mono'  # Valor padrão

        return dados_migrados

    def adicionar_versao_aos_dados(self, dados: Dict[str, Any]) -> Dict[str, Any]:
        """
        Adiciona a versão atual aos dados antes de salvá-los.
        Deve ser chamado pelo RepositorioDados antes de salvar.
        """
        dados_com_versao = dados.copy()
        dados_com_versao['versao'] = self.VERSAO_ATUAL
        return dados_com_versao


# --- Bloco de Teste ---
if __name__ == "__main__":
    print("--- Teste: dados/migrador.py ---")

    migrador = MigradorDados()

    print("\n--- Teste 1: Dados já na versão atual (não precisa migrar) ---")
    dados_atuais = {
        'versao': '1.0',
        'configuracao': {'eficiencia': 80.0},
        'unidades': [],
        'consumos': {}
    }
    resultado = migrador.migrar_se_necessario(dados_atuais)
    assert resultado['versao'] == '1.0'
    print("✅ Dados já atuais - nenhuma migração necessária.")

    print("\n--- Teste 2: Migração da versão 0.9 para 1.0 ---")
    dados_antigos = {
        'configuracao': {
            'potencia_inversor': 5000,
            'geracao_mensal': {'Jan': 800, 'Fev': 750}  # Meses abreviados
        },
        'unidades': [
            {'codigo': 'UC001', 'nome': 'Casa Teste', 'tipo_ligacao': 'mono'}
        ],
        'consumos': {
            'UC001': {'Jan': 200, 'Fev': 180}  # Meses abreviados
        }
    }

    resultado_migrado = migrador.migrar_se_necessario(dados_antigos)

    # Verifica se a versão foi adicionada
    assert resultado_migrado['versao'] == '1.0'

    # Verifica se os meses foram normalizados
    assert 'Janeiro' in resultado_migrado['configuracao']['geracao_mensal']
    assert 'Fevereiro' in resultado_migrado['configuracao']['geracao_mensal']
    assert 'Janeiro' in resultado_migrado['consumos']['UC001']
    assert 'Fevereiro' in resultado_migrado['consumos']['UC001']

    # Verifica se campos padrão foram adicionados
    assert 'endereco' in resultado_migrado['unidades'][0]
    assert resultado_migrado['unidades'][0]['endereco'] == ""

    print("✅ Migração 0.9 → 1.0 realizada com sucesso.")
    print(f"   Meses normalizados: {list(resultado_migrado['configuracao']['geracao_mensal'].keys())}")

    print("\n--- Teste 3: Adicionar versão aos dados ---")
    dados_sem_versao = {'configuracao': {}, 'unidades': [], 'consumos': {}}
    dados_com_versao = migrador.adicionar_versao_aos_dados(dados_sem_versao)
    assert dados_com_versao['versao'] == '1.0'
    print("✅ Versão adicionada aos dados com sucesso.")

    print("\n--- Teste 4: Erro ao tentar migrar versão não suportada ---")
    dados_versao_inexistente = {'versao': '2.0'}
    try:
        migrador.migrar_se_necessario(dados_versao_inexistente)
        assert False, "Deveria ter levantado uma exceção"
    except ErroCarregamentoDados as e:
        print(f"✅ Erro esperado capturado: {e}")

    print("\nTeste de Migrador de Dados concluído com sucesso!")