"""
Configurações e definições do sistema
Versão adaptada para compatibilidade com sistema legacy
"""

from nucleo.modelos import (
    ConfiguracaoSistema, UnidadeConsumidora, SistemaEnergia,
    TipoLigacao, TipoUnidade, BandeiraTarifaria
)

# Configurações do sistema
VERSAO_SISTEMA = "2.0-Legacy"
CAMINHO_ARQUIVO_DADOS = "dados_sistema.json"

# Configuração de exemplo adaptada para novos parâmetros
CONFIG_EXEMPLO = ConfiguracaoSistema(
    potencia_instalada_kw=100.0,  # Potência instalada em kW
    eficiencia_sistema=0.85,  # Eficiência do sistema
    fator_capacidade=0.15,  # Fator de capacidade

    # Tarifas
    tarifa_energia_kwh=0.6305,  # Tarifa de energia em R$/kWh
    tarifa_tusd_kwh=0.25,  # TUSD em R$/kWh
    tarifa_te_kwh=0.35,  # TE em R$/kWh

    # Taxas de disponibilidade
    taxa_disponibilidade_mono=30.0,  # Taxa monofásica
    taxa_disponibilidade_bi=50.0,  # Taxa bifásica
    taxa_disponibilidade_tri=100.0,  # Taxa trifásica

    # Bandeiras tarifárias
    bandeira_atual=BandeiraTarifaria.VERDE,
    adicional_bandeira_amarela=0.01874,
    adicional_bandeira_vermelha_1=0.03971,
    adicional_bandeira_vermelha_2=0.09492,
    adicional_bandeira_escassez=0.14200,

    # Geração mensal esperada (kWh)
    geracao_mensal_kwh=[
        8500, 8200, 9100, 8800, 7900, 7200,
        7800, 8600, 8400, 8900, 9200, 8700
    ],

    # Configurações do sistema legacy
    perdas_sistema=0.15,
    fator_simultaneidade=0.9,
    vida_util_sistema=25,
    custo_investimento=300000.0,

    # Configurações de créditos
    validade_creditos_meses=60,
    percentual_injecao_rede=1.0
)

# Unidades de exemplo adaptadas
UNIDADES_EXEMPLO = [
    UnidadeConsumidora(
        id="exemplo_001",
        nome="Residência Principal",
        tipo_ligacao=TipoLigacao.MONOFASICA,
        tipo_unidade=TipoUnidade.RESIDENCIAL,
        ativa=True,
        endereco="Rua das Flores, 123",
        cidade="São Paulo",
        estado="SP",
        cep="01234-567",
        demanda_contratada_kw=0.0,
        grupo_tarifario="B1",
        consumo_mensal_kwh=[
            450, 420, 480, 460, 440, 500,
            520, 480, 450, 430, 440, 460
        ],
        percentual_energia_alocada=30.0,
        prioridade_distribuicao=1
    ),
    UnidadeConsumidora(
        id="exemplo_002",
        nome="Comércio Local",
        tipo_ligacao=TipoLigacao.TRIFASICA,
        tipo_unidade=TipoUnidade.COMERCIAL,
        ativa=True,
        endereco="Av. Comercial, 456",
        cidade="São Paulo",
        estado="SP",
        cep="01234-890",
        demanda_contratada_kw=15.0,
        grupo_tarifario="B3",
        consumo_mensal_kwh=[
            1200, 1150, 1300, 1250, 1180, 1400,
            1450, 1300, 1200, 1180, 1220, 1280
        ],
        percentual_energia_alocada=70.0,
        prioridade_distribuicao=2
    )
]

# Dados de consumo de exemplo (compatibilidade legacy)
CONSUMOS_EXEMPLO = {
    "exemplo_001": [450, 420, 480, 460, 440, 500, 520, 480, 450, 430, 440, 460],
    "exemplo_002": [1200, 1150, 1300, 1250, 1180, 1400, 1450, 1300, 1200, 1180, 1220, 1280]
}

# Sistema de exemplo completo
SISTEMA_EXEMPLO = SistemaEnergia(
    configuracao=CONFIG_EXEMPLO,
    unidades=UNIDADES_EXEMPLO,
    versao_sistema=VERSAO_SISTEMA
)

# Configurações de interface
CONFIGURACOES_UI = {
    'tema_padrao': 'claro',
    'fonte_padrao': 'Arial',
    'tamanho_fonte': 10,
    'cores': {
        'primaria': '#2E86AB',
        'secundaria': '#A23B72',
        'sucesso': '#F18F01',
        'erro': '#C73E1D',
        'fundo': '#F5F5F5'
    },
    'dimensoes_janela': {
        'largura': 1200,
        'altura': 800,
        'largura_minima': 800,
        'altura_minima': 600
    }
}

# Configurações de relatórios
CONFIGURACOES_RELATORIO = {
    'formato_moeda': 'R$ {:.2f}',
    'formato_energia': '{:.1f} kWh',
    'formato_percentual': '{:.1f}%',
    'formato_potencia': '{:.1f} kW',
    'casas_decimais_energia': 1,
    'casas_decimais_financeiro': 2,
    'incluir_graficos_padrao': True,
    'incluir_detalhes_mensais': True,
    'incluir_projecoes': True
}

# Configurações de exportação
CONFIGURACOES_EXPORTACAO = {
    'formatos_suportados': ['PDF', 'Excel', 'CSV', 'JSON'],
    'diretorio_padrao': 'exports',
    'prefixo_arquivo': 'relatorio_energia',
    'incluir_timestamp': True,
    'compressao_excel': True
}

# Configurações de migração legacy
CONFIGURACOES_MIGRACAO = {
    'tipos_arquivo_suportados': ['.xlsx', '.xls', '.json', '.csv'],
    'diretorio_backup': 'backups',
    'validar_antes_migrar': True,
    'criar_backup_automatico': True,
    'manter_dados_originais': True
}

# Mapeamento de campos legacy para novos campos
MAPEAMENTO_CAMPOS_LEGACY = {
    'potencia_inversor': 'potencia_instalada_kw',
    'eficiencia_inversor': 'eficiencia_sistema',
    'valor_kwh': 'tarifa_energia_kwh',
    'custo_disponibilidade': 'taxa_disponibilidade_mono',
    'geracao_estimada': 'geracao_mensal_kwh',
    'tipo_conexao': 'tipo_ligacao',
    'consumo_historico': 'consumo_mensal_kwh'
}

# Valores padrão para migração
VALORES_PADRAO_MIGRACAO = {
    'potencia_instalada_kw': 100.0,
    'eficiencia_sistema': 0.85,
    'tarifa_energia_kwh': 0.75,
    'perdas_sistema': 0.15,
    'fator_simultaneidade': 0.9,
    'vida_util_sistema': 25,
    'validade_creditos_meses': 60
}

# Configurações de validação
LIMITES_VALIDACAO = {
    'potencia_minima_kw': 0.1,
    'potencia_maxima_kw': 10000.0,
    'eficiencia_minima': 0.1,
    'eficiencia_maxima': 1.0,
    'tarifa_minima': 0.01,
    'tarifa_maxima': 10.0,
    'consumo_minimo': 0.0,
    'consumo_maximo': 100000.0,
    'perdas_minimas': 0.0,
    'perdas_maximas': 0.5
}

# Mensagens do sistema
MENSAGENS_SISTEMA = {
    'migracao_sucesso': 'Migração realizada com sucesso!',
    'migracao_erro': 'Erro durante a migração: {}',
    'validacao_erro': 'Erro de validação: {}',
    'arquivo_nao_encontrado': 'Arquivo não encontrado: {}',
    'backup_criado': 'Backup criado em: {}',
    'sistema_salvo': 'Sistema salvo com sucesso!',
    'sistema_carregado': 'Sistema carregado com sucesso!'
}

# Configurações de logging
CONFIGURACOES_LOG = {
    'nivel_log': 'INFO',
    'arquivo_log': 'sistema_energia.log',
    'formato_log': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    'rotacao_log': True,
    'tamanho_maximo_mb': 10,
    'backup_count': 5
}

# Constantes do sistema
CONSTANTES = {
    'MESES_ANO': 12,
    'DIAS_ANO': 365,
    'HORAS_DIA': 24,
    'MINUTOS_HORA': 60,
    'SEGUNDOS_MINUTO': 60,
    'KW_PARA_W': 1000,
    'MW_PARA_KW': 1000,
    'PERCENTUAL_PARA_DECIMAL': 100
}

# Configurações específicas do Brasil
CONFIGURACOES_BRASIL = {
    'fuso_horario': 'America/Sao_Paulo',
    'moeda': 'BRL',
    'simbolo_moeda': 'R$',
    'separador_decimal': ',',
    'separador_milhares': '.',
    'formato_data': '%d/%m/%Y',
    'formato_hora': '%H:%M:%S'
}


# Função para obter configuração padrão
def obter_configuracao_padrao():
    """Retorna configuração padrão do sistema"""
    return CONFIG_EXEMPLO


def obter_unidades_padrao():
    """Retorna unidades padrão do sistema"""
    return UNIDADES_EXEMPLO


def obter_sistema_padrao():
    """Retorna sistema padrão completo"""
    return SISTEMA_EXEMPLO


def validar_configuracao(config):
    """Valida configuração do sistema"""
    erros = []

    if config.potencia_instalada_kw < LIMITES_VALIDACAO['potencia_minima_kw']:
        erros.append(f"Potência muito baixa: {config.potencia_instalada_kw}")

    if config.potencia_instalada_kw > LIMITES_VALIDACAO['potencia_maxima_kw']:
        erros.append(f"Potência muito alta: {config.potencia_instalada_kw}")

    if not (LIMITES_VALIDACAO['eficiencia_minima'] <= config.eficiencia_sistema <= LIMITES_VALIDACAO[
        'eficiencia_maxima']):
        erros.append(f"Eficiência inválida: {config.eficiencia_sistema}")

    return erros


# ===== ADIÇÃO INCREMENTAL - DADOS REAIS =====

def obter_sistema_com_dados_reais():
    """Obtém sistema com dados reais se disponível, senão usa padrão"""
    try:
        from utilitarios.importador_dados import importar_dados_reais_para_sistema

        sistema_real = importar_dados_reais_para_sistema()
        if sistema_real:
            print("✅ Sistema carregado com dados reais da usina")
            return sistema_real
        else:
            print("ℹ️ Usando dados padrão (dados reais não disponíveis)")
            return SISTEMA_EXEMPLO

    except Exception as e:
        print(f"⚠️ Erro ao carregar dados reais, usando padrão: {e}")
        return SISTEMA_EXEMPLO


def obter_sistema_padrao():
    """Retorna sistema padrão (agora verifica dados reais primeiro)"""
    return obter_sistema_com_dados_reais()


# ===== INTEGRAÇÃO COM DADOS LEGACY =====

def obter_sistema_com_dados_legacy():
    """Obtém sistema usando dados legacy se disponível"""
    try:
        from dados.gerenciador_dados_legacy import GerenciadorDadosLegacy

        gerenciador = GerenciadorDadosLegacy()
        dados_legacy = gerenciador.carregar_dados()
        sistema = gerenciador.converter_para_sistema_energia(dados_legacy)

        print("✅ Sistema carregado com dados legacy")
        return sistema

    except Exception as e:
        print(f"⚠️ Erro ao carregar dados legacy: {e}")
        return obter_sistema_com_dados_reais()


# Atualizar função principal
def obter_sistema_padrao():
    """Retorna sistema padrão (prioriza legacy, depois reais)"""
    return obter_sistema_com_dados_legacy()

# Arquivo de dados padrão
ARQUIVO_DADOS = CAMINHO_ARQUIVO_DADOS