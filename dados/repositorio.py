# usina_01/dados/repositorio.py

import json
import os
from dataclasses import asdict
from typing import Dict, Any

from nucleo.modelos import SistemaEnergia, ConfiguracaoSistema, UnidadeConsumidora, TipoLigacao
from nucleo.excecoes import ErroCarregamentoDados, ErroSalvamentoDados
from configuracao.definicoes import ARQUIVO_DADOS, CONFIG_EXEMPLO, UNIDADES_EXEMPLO, CONSUMOS_EXEMPLO


class RepositorioDados:
    def __init__(self, arquivo_dados: str = ARQUIVO_DADOS):
        self.arquivo_dados = arquivo_dados

    def _converter_para_json_compativel(self, obj: Any) -> Any:
        """
        Converte objetos complexos (como Enums e dataclasses) para tipos compatíveis com JSON.
        """
        if isinstance(obj, TipoLigacao):
            return obj.value  # Converte Enum para seu valor de string
        if isinstance(obj, dict):
            return {k: self._converter_para_json_compativel(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self._converter_para_json_compativel(elem) for elem in obj]
        if isinstance(obj, (ConfiguracaoSistema, UnidadeConsumidora, SistemaEnergia)):
            # asdict converte a dataclass em um dicionário, e então recursivamente processamos seus valores
            return {k: self._converter_para_json_compativel(v) for k, v in asdict(obj).items()}
        return obj

    def _converter_de_json_para_modelo(self, data: Dict[str, Any]) -> SistemaEnergia:
        """
        Converte um dicionário (vindo do JSON) de volta para uma instância de SistemaEnergia.
        Usa uma abordagem direta e específica para este projeto.
        """
        # 1. Converte a configuração
        config_data = data.get('configuracao', {})
        configuracao = ConfiguracaoSistema(**config_data)

        # 2. Converte as unidades
        unidades_data = data.get('unidades', [])
        unidades = []
        for unidade_dict in unidades_data:
            # Converte o tipo_ligacao de string de volta para Enum
            tipo_ligacao_str = unidade_dict.get('tipo_ligacao', 'mono')
            unidade_dict_copy = unidade_dict.copy()
            unidade_dict_copy['tipo_ligacao'] = TipoLigacao(tipo_ligacao_str)
            unidades.append(UnidadeConsumidora(**unidade_dict_copy))

        # 3. Converte os consumos (já são dicionários simples, não precisam de conversão especial)
        consumos = data.get('consumos', {})

        return SistemaEnergia(
            configuracao=configuracao,
            unidades=unidades,
            consumos=consumos
        )

    def carregar_sistema(self) -> SistemaEnergia:
        """
        Carrega os dados do sistema de um arquivo JSON.
        Se o arquivo não existir ou estiver corrompido, inicializa com dados de exemplo.
        """
        if not os.path.exists(self.arquivo_dados):
            print(f"Arquivo '{self.arquivo_dados}' não encontrado. Inicializando com dados de exemplo.")
            sistema = self._inicializar_com_dados_exemplo()
            self.salvar_sistema(sistema)
            return sistema

        try:
            with open(self.arquivo_dados, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)

            # Converte o dicionário carregado de volta para a estrutura de dataclasses
            sistema = self._converter_de_json_para_modelo(raw_data)
            return sistema

        except json.JSONDecodeError as e:
            print(f"❌ Erro ao carregar dados: {e}")
            print(f"🔧 Arquivo JSON corrompido na linha {e.lineno}, coluna {e.colno}")
            print("📝 Criando backup e inicializando com dados de exemplo...")

            # Fazer backup do arquivo corrompido
            backup_path = f"{self.arquivo_dados}.backup"
            os.rename(self.arquivo_dados, backup_path)
            print(f"💾 Backup salvo em: {backup_path}")

            # Criar novo sistema
            sistema = self._inicializar_com_dados_exemplo()
            self.salvar_sistema(sistema)
            return sistema

        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
            print("📝 Inicializando com dados de exemplo...")
            sistema = self._inicializar_com_dados_exemplo()
            return sistema

    def salvar_sistema(self, sistema: SistemaEnergia):
        """
        Salva os dados do sistema em um arquivo JSON.
        """
        try:
            # Converte a dataclass SistemaEnergia e suas aninhadas para um dicionário compatível com JSON
            data_to_save = self._converter_para_json_compativel(sistema)

            with open(self.arquivo_dados, 'w', encoding='utf-8') as f:
                json.dump(data_to_save, f, indent=4, ensure_ascii=False)
        except Exception as e:
            raise ErroSalvamentoDados(f"Erro ao salvar dados no arquivo '{self.arquivo_dados}': {e}")

    def _inicializar_com_dados_exemplo(self) -> SistemaEnergia:
        """
        Cria uma instância de SistemaEnergia com os dados de exemplo definidos.
        """
        sistema = SistemaEnergia(
            configuracao=CONFIG_EXEMPLO,
            unidades=UNIDADES_EXEMPLO,
            consumos=CONSUMOS_EXEMPLO
        )
        return sistema


# --- Bloco de Teste ---
if __name__ == "__main__":
    print("--- Teste: dados/repositorio.py ---")

    # Define um arquivo de teste para não sobrescrever o arquivo de dados real durante os testes
    TEST_FILE = "test_dados_sistema.json"
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)  # Limpa o arquivo de teste anterior

    repo = RepositorioDados(TEST_FILE)

    print("\n--- Teste 1: Carregar sistema (deve inicializar com dados de exemplo) ---")
    sistema_inicial = repo.carregar_sistema()
    print(f"Sistema carregado. Configuração: Eficiência={sistema_inicial.configuracao.eficiencia}%")
    print(f"Unidades carregadas: {[u.nome for u in sistema_inicial.unidades]}")
    print(f"Consumo UC001 em Janeiro: {sistema_inicial.consumos['UC001']['Janeiro']} kWh")

    # Verifica se o arquivo foi criado
    assert os.path.exists(TEST_FILE)
    print(f"Arquivo '{TEST_FILE}' criado com sucesso.")

    print("\n--- Teste 2: Modificar o sistema e salvar ---")
    # Adiciona uma nova unidade
    nova_unidade = UnidadeConsumidora(codigo="UC004", nome="Escritório Central", tipo_ligacao=TipoLigacao.TRI,
                                      endereco="Av. Brasil, 1000")
    sistema_inicial.unidades.append(nova_unidade)
    # Altera um consumo
    sistema_inicial.consumos["UC001"]["Fevereiro"] = 250  # Altera o consumo de UC001 em Fevereiro
    # Adiciona consumos para a nova unidade
    sistema_inicial.consumos["UC004"] = {"Janeiro": 800, "Fevereiro": 820, "Março": 790}

    repo.salvar_sistema(sistema_inicial)
    print("Sistema modificado e salvo.")

    print("\n--- Teste 3: Carregar novamente e verificar as modificações ---")
    sistema_recarregado = repo.carregar_sistema()
    print(f"Unidades recarregadas: {[u.nome for u in sistema_recarregado.unidades]}")
    print(f"Consumo UC001 em Fevereiro (recarregado): {sistema_recarregado.consumos['UC001']['Fevereiro']} kWh")
    print(
        f"Consumo UC004 em Janeiro (nova unidade): {sistema_recarregado.consumos.get('UC004', {}).get('Janeiro', 'N/A')} kWh")

    assert any(u.codigo == "UC004" for u in sistema_recarregado.unidades)
    assert sistema_recarregado.consumos["UC001"]["Fevereiro"] == 250
    assert sistema_recarregado.consumos["UC004"]["Janeiro"] == 800
    print("Modificações persistidas e recarregadas com sucesso!")

    print("\n--- Teste 4: Verificar tipos após recarregamento ---")
    uc004 = next(u for u in sistema_recarregado.unidades if u.codigo == "UC004")
    print(f"Tipo de ligação da UC004: {uc004.tipo_ligacao} (tipo: {type(uc004.tipo_ligacao)})")
    assert isinstance(uc004.tipo_ligacao, TipoLigacao)
    print("Tipos verificados com sucesso!")

    print("\n--- Teste 5: Testar carregamento de arquivo corrompido (simulado) ---")
    with open(TEST_FILE, 'w', encoding='utf-8') as f:
        f.write("{invalid json")  # Escreve JSON inválido

    try:
        repo.carregar_sistema()
        assert False, "Deveria ter levantado uma exceção"
    except ErroCarregamentoDados as e:
        print(f"Erro de carregamento esperado capturado: {e}")

    # Limpa o arquivo de teste
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)
        print(f"Arquivo de teste '{TEST_FILE}' removido.")

    print("\nTeste de Repositório de Dados concluído com sucesso!")