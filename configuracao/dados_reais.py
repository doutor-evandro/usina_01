"""
Dados Reais do Sistema de Energia Solar
Configurações específicas da sua usina - INCREMENTAL
"""

from nucleo.modelos import TipoLigacao, TipoUnidade, BandeiraTarifaria

# Configurações da Usina Real (seus dados)
CONFIGURACAO_USINA_REAL = {
    "potencia_instalada_kw": 92.0,  # Potência dos módulos
    "potencia_inversor_kw": 75.0,  # Potência do inversor
    "eficiencia_sistema": 1.0,  # 100% de eficiência
    "tarifa_energia_kwh": 0.65,  # Tarifa média
    "custo_investimento": 450000.0,  # Custo estimado
    "versao_sistema": "2.0-Real"
}

# Geração Mensal Real da Usina (kWh) - SEUS DADOS
GERACAO_MENSAL_REAL = [
    15162,  # Janeiro
    12453,  # Fevereiro
    12500,  # Março
    10423,  # Abril
    9002.4,  # Maio
    6675,  # Junho
    8197,  # Julho
    9954,  # Agosto
    11561,  # Setembro
    13234,  # Outubro
    14000,  # Novembro
    14606  # Dezembro
]

# Unidades Consumidoras Reais - SEUS DADOS
UNIDADES_REAIS = [
    {
        "id": "112761577",
        "codigo": "112761577",
        "nome": "Lanchonet",
        "tipo_ligacao": TipoLigacao.TRIFASICA,
        "tipo_unidade": TipoUnidade.COMERCIAL,
        "endereco": "Av. Pres Getulio Vargas 1890",
        "ativa": True,
        "consumo_mensal": [1739, 1739, 1739, 1739, 1739, 1739, 1739, 1739, 1739, 1739, 1739, 1739],
        "percentual_energia_alocada": 19.9,
        "prioridade_distribuicao": 1
    },
    {
        "id": "114789592",
        "codigo": "114789592",
        "nome": "My Beach",
        "tipo_ligacao": TipoLigacao.TRIFASICA,
        "tipo_unidade": TipoUnidade.COMERCIAL,
        "endereco": "Av. Pres Getulio Vargas 1890 - Mybeach",
        "ativa": True,
        "consumo_mensal": [500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500],
        "percentual_energia_alocada": 5.7,
        "prioridade_distribuicao": 2
    },
    {
        "id": "104775009",
        "codigo": "104775009",
        "nome": "Loja",
        "tipo_ligacao": TipoLigacao.TRIFASICA,
        "tipo_unidade": TipoUnidade.COMERCIAL,
        "endereco": "R. Guilherme Casteletto 34 - loja",
        "ativa": True,
        "consumo_mensal": [1454, 2346, 2486, 1955, 1682, 1220, 1341, 1208, 1849, 1845, 2181, 2282],
        "percentual_energia_alocada": 20.8,
        "prioridade_distribuicao": 3
    },
    {
        "id": "94926239",
        "codigo": "94926239",
        "nome": "Sobreloja",
        "tipo_ligacao": TipoLigacao.TRIFASICA,
        "tipo_unidade": TipoUnidade.COMERCIAL,
        "endereco": "R. Guilherme Casteletto 34 - sobreloja1",
        "ativa": True,
        "consumo_mensal": [701, 1944, 2184, 1824, 1646, 1115, 1186, 1014, 1504, 1572, 1635, 1697],
        "percentual_energia_alocada": 17.0,
        "prioridade_distribuicao": 4
    },
    {
        "id": "101839405",
        "codigo": "101839405",
        "nome": "Casa Adriano",
        "tipo_ligacao": TipoLigacao.BIFASICA,
        "tipo_unidade": TipoUnidade.RESIDENCIAL,
        "endereco": "R Luiz Roncalha, 198",
        "ativa": True,
        "consumo_mensal": [663, 731, 847, 705, 542, 352, 384, 376, 539, 540, 452, 750],
        "percentual_energia_alocada": 6.8,
        "prioridade_distribuicao": 5
    },
    {
        "id": "95268278",
        "codigo": "95268278",
        "nome": "Depósito",
        "tipo_ligacao": TipoLigacao.TRIFASICA,
        "tipo_unidade": TipoUnidade.INDUSTRIAL,
        "endereco": "R. Apucarana 125",
        "ativa": True,
        "consumo_mensal": [176, 202, 387, 286, 269, 213, 216, 173, 185, 251, 245, 277],
        "percentual_energia_alocada": 2.9,
        "prioridade_distribuicao": 6
    },
    {
        "id": "70796270",
        "codigo": "70796270",
        "nome": "Fernando Lomas",
        "tipo_ligacao": TipoLigacao.TRIFASICA,
        "tipo_unidade": TipoUnidade.COMERCIAL,
        "endereco": "R. Sertanopolis 465",
        "ativa": True,
        "consumo_mensal": [650, 1239, 1307, 1082, 795, 803, 519, 844, 924, 971, 1018, 1016],
        "percentual_energia_alocada": 11.2,
        "prioridade_distribuicao": 7
    },
    {
        "id": "81788541",
        "codigo": "81788541",
        "nome": "Mário 1",
        "tipo_ligacao": TipoLigacao.TRIFASICA,
        "tipo_unidade": TipoUnidade.COMERCIAL,
        "endereco": "R. Santa Fé 218 - Sala 02",
        "ativa": True,
        "consumo_mensal": [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000],
        "percentual_energia_alocada": 13.7,
        "prioridade_distribuicao": 8
    },
    {
        "id": "76103684",
        "codigo": "76103684",
        "nome": "Mário 2",
        "tipo_ligacao": TipoLigacao.BIFASICA,
        "tipo_unidade": TipoUnidade.COMERCIAL,
        "endereco": "R. Santa Fé 218 - Sala 01",
        "ativa": True,
        "consumo_mensal": [500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500, 500],
        "percentual_energia_alocada": 6.8,
        "prioridade_distribuicao": 9
    }
]


# Função para obter resumo dos dados reais
def obter_resumo_dados_reais():
    """Retorna resumo dos dados reais"""
    total_unidades = len(UNIDADES_REAIS)
    geracao_anual = sum(GERACAO_MENSAL_REAL)
    consumo_total_anual = sum(sum(u["consumo_mensal"]) for u in UNIDADES_REAIS)

    return {
        "total_unidades": total_unidades,
        "geracao_anual_kwh": geracao_anual,
        "consumo_total_anual_kwh": consumo_total_anual,
        "saldo_anual_kwh": geracao_anual - consumo_total_anual,
        "potencia_instalada_kw": CONFIGURACAO_USINA_REAL["potencia_instalada_kw"],
        "potencia_inversor_kw": CONFIGURACAO_USINA_REAL["potencia_inversor_kw"]
    }


# Função para verificar se deve usar dados reais
def usar_dados_reais():
    """Verifica se deve usar dados reais em vez dos dados exemplo"""
    return True  # Mude para False se quiser voltar aos dados exemplo