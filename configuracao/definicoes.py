# Versão do sistema
VERSAO_SISTEMA = "1.0.0"
# usina_01/configuracao/definicoes.py

import os
from nucleo.modelos import ConfiguracaoSistema, UnidadeConsumidora, TipoLigacao
from utilitarios.constantes import MESES_APENAS

# --- Caminho do Arquivo de Dados ---
# Define o nome do arquivo JSON onde os dados do sistema serão salvos.
# O arquivo será criado/lido no mesmo diretório de execução do script principal.
ARQUIVO_DADOS = "dados_sistema.json"

# --- Dados de Exemplo Iniciais ---
# Estes dados serão usados para popular o sistema caso o arquivo ARQUIVO_DADOS não exista.
# Eles seguem a estrutura dos modelos definidos em nucleo/modelos.py.

# Configuração da Usina de Exemplo
CONFIG_EXEMPLO = ConfiguracaoSistema(
    potencia_inversor=10000,  # Potência do inversor em W
    potencia_modulos=12000,   # Potência dos módulos em Wp
    geracao_mensal={          # Geração média mensal esperada em kWh
        "Janeiro": 1200, "Fevereiro": 1100, "Março": 1250, "Abril": 1150,
        "Maio": 1000, "Junho": 900, "Julho": 950, "Agosto": 1050,
        "Setembro": 1100, "Outubro": 1200, "Novembro": 1150, "Dezembro": 1280
    },
    eficiencia=78.0,          # Eficiência geral da usina em %
    valor_kwh=0.6305          # Valor de referência do kWh em R\$
)

# Unidades Consumidoras de Exemplo
UNIDADES_EXEMPLO = [
    UnidadeConsumidora(codigo="UC001", nome="Casa do João", tipo_ligacao=TipoLigacao.MONO, endereco="Rua das Flores, 100 - Centro"),
    UnidadeConsumidora(codigo="UC002", nome="Comércio da Maria", tipo_ligacao=TipoLigacao.TRI, endereco="Av. Principal, 500 - Bairro Novo"),
    UnidadeConsumidora(codigo="UC003", nome="Apartamento 301", tipo_ligacao=TipoLigacao.BI, endereco="Rua da Paz, 301 - Jardim"),
]

# Consumos de Exemplo para as Unidades
# Cada unidade terá um dicionário de consumos por mês.
CONSUMOS_EXEMPLO = {
    "UC001": {
        "Janeiro": 250, "Fevereiro": 230, "Março": 260, "Abril": 240,
        "Maio": 220, "Junho": 200, "Julho": 210, "Agosto": 230,
        "Setembro": 240, "Outubro": 260, "Novembro": 250, "Dezembro": 270
    },
    "UC002": {
        "Janeiro": 600, "Fevereiro": 580, "Março": 620, "Abril": 590,
        "Maio": 550, "Junho": 500, "Julho": 520, "Agosto": 560,
        "Setembro": 580, "Outubro": 610, "Novembro": 590, "Dezembro": 630
    },
    "UC003": {
        "Janeiro": 150, "Fevereiro": 140, "Março": 160, "Abril": 150,
        "Maio": 130, "Junho": 120, "Julho": 125, "Agosto": 135,
        "Setembro": 145, "Outubro": 155, "Novembro": 150, "Dezembro": 165
    },
}

# --- Bloco de Teste ---
if __name__ == "__main__":
    print("--- Teste: configuracao/definicoes.py ---")
    print(f"Caminho do arquivo de dados: {ARQUIVO_DADOS}")
    print(f"Configuração de exemplo (Eficiência): {CONFIG_EXEMPLO.eficiencia}%")
    print(f"Número de unidades de exemplo: {len(UNIDADES_EXEMPLO)}")
    print(f"Consumo de UC001 em Janeiro: {CONSUMOS_EXEMPLO['UC001']['Janeiro']} kWh")

    # Verifica se todos os meses estão preenchidos para cada unidade
    for codigo, consumos_mes in CONSUMOS_EXEMPLO.items():
        if len(consumos_mes) != len(MESES_APENAS):
            print(f"AVISO: Consumos da unidade {codigo} não cobrem todos os meses do ano.")