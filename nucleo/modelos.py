"""
Modelos de dados do sistema de energia solar
Versão adaptada para incluir funcionalidades do sistema legacy
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Any
from datetime import datetime
import json


class TipoLigacao(Enum):
    """Tipos de ligação elétrica"""
    MONOFASICA = "monofasica"
    BIFASICA = "bifasica"
    TRIFASICA = "trifasica"


class BandeiraTarifaria(Enum):
    """Bandeiras tarifárias"""
    VERDE = "verde"
    AMARELA = "amarela"
    VERMELHA_1 = "vermelha_1"
    VERMELHA_2 = "vermelha_2"
    ESCASSEZ = "escassez"


class TipoUnidade(Enum):
    """Tipos de unidade consumidora"""
    RESIDENCIAL = "residencial"
    COMERCIAL = "comercial"
    INDUSTRIAL = "industrial"
    RURAL = "rural"
    PODER_PUBLICO = "poder_publico"


@dataclass
class ConfiguracaoSistema:
    """Configurações gerais do sistema fotovoltaico"""
    # Configurações básicas
    potencia_instalada_kw: float = 100.0
    eficiencia_sistema: float = 0.85
    fator_capacidade: float = 0.15

    # Configurações tarifárias
    tarifa_energia_kwh: float = 0.75
    tarifa_tusd_kwh: float = 0.25
    tarifa_te_kwh: float = 0.50
    taxa_disponibilidade_mono: float = 30.0
    taxa_disponibilidade_bi: float = 50.0
    taxa_disponibilidade_tri: float = 100.0

    # Configurações de bandeira tarifária
    bandeira_atual: BandeiraTarifaria = BandeiraTarifaria.VERDE
    adicional_bandeira_amarela: float = 0.01874
    adicional_bandeira_vermelha_1: float = 0.03971
    adicional_bandeira_vermelha_2: float = 0.09492
    adicional_bandeira_escassez: float = 0.14200

    # Geração mensal esperada (kWh) - adaptado do sistema antigo
    geracao_mensal_kwh: List[float] = field(default_factory=lambda: [
        8500, 8200, 9100, 8800, 7900, 7200,
        7800, 8600, 8400, 8900, 9200, 8700
    ])

    # Configurações do sistema legacy
    perdas_sistema: float = 0.15
    fator_simultaneidade: float = 0.9
    vida_util_sistema: int = 25
    custo_investimento: float = 0.0

    # Configurações de créditos
    validade_creditos_meses: int = 60
    percentual_injecao_rede: float = 1.0


@dataclass
class UnidadeConsumidora:
    """Unidade consumidora de energia"""
    id: str
    nome: str
    tipo_ligacao: TipoLigacao
    tipo_unidade: TipoUnidade = TipoUnidade.RESIDENCIAL
    ativa: bool = True

    # Dados de localização
    endereco: str = ""
    cidade: str = ""
    estado: str = ""
    cep: str = ""

    # Dados técnicos
    demanda_contratada_kw: float = 0.0
    grupo_tarifario: str = "B1"  # B1, B2, B3, A4, etc.

    # Histórico de consumo (adaptado do sistema antigo)
    consumo_mensal_kwh: List[float] = field(default_factory=lambda: [0.0] * 12)

    # Configurações específicas
    percentual_energia_alocada: float = 0.0
    prioridade_distribuicao: int = 1

    def get_taxa_disponibilidade(self) -> float:
        """Retorna taxa de disponibilidade baseada no tipo de ligação"""
        taxas = {
            TipoLigacao.MONOFASICA: 30.0,
            TipoLigacao.BIFASICA: 50.0,
            TipoLigacao.TRIFASICA: 100.0
        }
        return taxas.get(self.tipo_ligacao, 30.0)

    def get_consumo_total_anual(self) -> float:
        """Retorna consumo total anual em kWh"""
        return sum(self.consumo_mensal_kwh)

    def get_consumo_medio_mensal(self) -> float:
        """Retorna consumo médio mensal em kWh"""
        consumos_validos = [c for c in self.consumo_mensal_kwh if c > 0]
        return sum(consumos_validos) / len(consumos_validos) if consumos_validos else 0.0


@dataclass
class ResultadoMensalEnergia:
    """Resultado energético mensal"""
    mes: int
    geracao_kwh: float
    consumo_total_kwh: float
    saldo_kwh: float
    creditos_gerados_kwh: float
    creditos_utilizados_kwh: float
    energia_injetada_kwh: float
    energia_consumida_rede_kwh: float

    # Dados adicionais do sistema legacy
    fator_capacidade_real: float = 0.0
    eficiencia_real: float = 0.0
    perdas_kwh: float = 0.0


@dataclass
class ResultadoMensalFinanceiro:
    """Resultado financeiro mensal"""
    mes: int
    custo_sem_solar: float
    custo_com_solar: float
    economia_mensal: float
    valor_energia_injetada: float
    valor_creditos_utilizados: float

    # Dados de bandeira tarifária
    bandeira_aplicada: BandeiraTarifaria
    valor_bandeira: float = 0.0

    # Dados do sistema legacy
    custo_disponibilidade: float = 0.0
    custo_demanda: float = 0.0
    impostos: float = 0.0


@dataclass
class ResultadoAnualEnergia:
    """Resultado energético anual"""
    ano: int
    geracao_total_kwh: float
    consumo_total_kwh: float
    saldo_anual_kwh: float
    creditos_acumulados_kwh: float
    autossuficiencia_percentual: float
    resultados_mensais: List[ResultadoMensalEnergia]

    # Métricas do sistema legacy
    fator_capacidade_medio: float = 0.0
    eficiencia_media: float = 0.0
    perdas_totais_kwh: float = 0.0


@dataclass
class ResultadoAnualFinanceiro:
    """Resultado financeiro anual"""
    ano: int
    economia_total: float
    custo_total_sem_solar: float
    custo_total_com_solar: float
    payback_simples_anos: float
    roi_percentual: float
    resultados_mensais: List[ResultadoMensalFinanceiro]

    # Dados do sistema legacy
    valor_investimento: float = 0.0
    economia_acumulada: float = 0.0
    tir_percentual: float = 0.0


@dataclass
class HistoricoCreditos:
    """Histórico de créditos de energia"""
    mes_geracao: int
    ano_geracao: int
    creditos_kwh: float
    creditos_utilizados_kwh: float
    creditos_restantes_kwh: float
    mes_vencimento: int
    ano_vencimento: int
    ativo: bool = True


@dataclass
class ConfiguracaoRelatorio:
    """Configurações para geração de relatórios"""
    incluir_graficos: bool = True
    incluir_detalhes_mensais: bool = True
    incluir_projecoes: bool = True
    formato_moeda: str = "R$ {:.2f}"
    formato_energia: str = "{:.1f} kWh"
    formato_percentual: str = "{:.1f}%"

    # Configurações do sistema legacy
    incluir_analise_bandeiras: bool = True
    incluir_comparativo_anos: bool = True
    incluir_metricas_tecnicas: bool = True


@dataclass
class SistemaEnergia:
    """Sistema completo de energia solar"""
    configuracao: ConfiguracaoSistema
    unidades: List[UnidadeConsumidora]
    historico_creditos: List[HistoricoCreditos] = field(default_factory=list)
    configuracao_relatorio: ConfiguracaoRelatorio = field(default_factory=ConfiguracaoRelatorio)

    # Metadados do sistema
    versao_sistema: str = "2.0"
    data_criacao: str = field(default_factory=lambda: datetime.now().isoformat())
    data_ultima_atualizacao: str = field(default_factory=lambda: datetime.now().isoformat())

    # Dados do sistema legacy
    dados_importacao: Dict[str, Any] = field(default_factory=dict)
    configuracoes_avancadas: Dict[str, Any] = field(default_factory=dict)

    def atualizar_timestamp(self):
        """Atualiza timestamp da última modificação"""
        self.data_ultima_atualizacao = datetime.now().isoformat()

    def get_unidade_por_id(self, id_unidade: str) -> Optional[UnidadeConsumidora]:
        """Busca unidade por ID"""
        for unidade in self.unidades:
            if unidade.id == id_unidade:
                return unidade
        return None

    def get_unidades_ativas(self) -> List[UnidadeConsumidora]:
        """Retorna apenas unidades ativas"""
        return [u for u in self.unidades if u.ativa]

    def get_consumo_total_sistema(self) -> float:
        """Retorna consumo total anual do sistema"""
        return sum(u.get_consumo_total_anual() for u in self.get_unidades_ativas())

    def validar_integridade(self) -> List[str]:
        """Valida integridade dos dados do sistema"""
        erros = []

        # Validar configuração
        if self.configuracao.potencia_instalada_kw <= 0:
            erros.append("Potência instalada deve ser maior que zero")

        if not (0 < self.configuracao.eficiencia_sistema <= 1):
            erros.append("Eficiência deve estar entre 0 e 1")

        # Validar unidades
        if not self.unidades:
            erros.append("Sistema deve ter pelo menos uma unidade consumidora")

        ids_unidades = [u.id for u in self.unidades]
        if len(ids_unidades) != len(set(ids_unidades)):
            erros.append("IDs de unidades devem ser únicos")

        # Validar geração mensal
        if len(self.configuracao.geracao_mensal_kwh) != 12:
            erros.append("Geração mensal deve ter 12 valores")

        return erros


# Funções auxiliares para compatibilidade com sistema legacy
def criar_sistema_exemplo_legacy() -> SistemaEnergia:
    """Cria sistema de exemplo baseado no formato legacy"""

    config = ConfiguracaoSistema(
        potencia_instalada_kw=150.0,
        eficiencia_sistema=0.82,
        tarifa_energia_kwh=0.78,
        geracao_mensal_kwh=[
            12500, 11800, 13200, 12600, 11400, 10200,
            11100, 12300, 12000, 12800, 13100, 12400
        ],
        custo_investimento=450000.0,
        perdas_sistema=0.18,
        fator_simultaneidade=0.85
    )

    unidades = [
        UnidadeConsumidora(
            id="001",
            nome="Unidade Residencial 1",
            tipo_ligacao=TipoLigacao.MONOFASICA,
            tipo_unidade=TipoUnidade.RESIDENCIAL,
            consumo_mensal_kwh=[450, 420, 480, 460, 440, 500, 520, 480, 450, 430, 440, 460],
            percentual_energia_alocada=30.0
        ),
        UnidadeConsumidora(
            id="002",
            nome="Unidade Comercial 1",
            tipo_ligacao=TipoLigacao.TRIFASICA,
            tipo_unidade=TipoUnidade.COMERCIAL,
            consumo_mensal_kwh=[1200, 1150, 1300, 1250, 1180, 1400, 1450, 1300, 1200, 1180, 1220, 1280],
            percentual_energia_alocada=70.0
        )
    ]

    return SistemaEnergia(
        configuracao=config,
        unidades=unidades,
        versao_sistema="2.0-Legacy"
    )


def converter_dados_legacy(dados_antigos: Dict[str, Any]) -> SistemaEnergia:
    """Converte dados do formato antigo para o novo"""

    # Extrair configuração
    config_antiga = dados_antigos.get('configuracao', {})
    config = ConfiguracaoSistema(
        potencia_instalada_kw=config_antiga.get('potencia_sistema', 100.0),
        eficiencia_sistema=config_antiga.get('eficiencia', 0.85),
        tarifa_energia_kwh=config_antiga.get('tarifa_energia', 0.75),
        geracao_mensal_kwh=config_antiga.get('geracao_mensal', [8000] * 12),
        custo_investimento=config_antiga.get('custo_investimento', 0.0),
        perdas_sistema=config_antiga.get('perdas_sistema', 0.15),
        fator_simultaneidade=config_antiga.get('fator_simultaneidade', 0.9)
    )

    # Extrair unidades
    unidades_antigas = dados_antigos.get('unidades', [])
    unidades = []

    for i, unidade_antiga in enumerate(unidades_antigas):
        tipo_ligacao = TipoLigacao.MONOFASICA
        if unidade_antiga.get('tipo_ligacao', '').lower() == 'trifasica':
            tipo_ligacao = TipoLigacao.TRIFASICA
        elif unidade_antiga.get('tipo_ligacao', '').lower() == 'bifasica':
            tipo_ligacao = TipoLigacao.BIFASICA

        unidade = UnidadeConsumidora(
            id=f"legacy_{i + 1:03d}",
            nome=unidade_antiga.get('nome', f'Unidade {i + 1}'),
            tipo_ligacao=tipo_ligacao,
            consumo_mensal_kwh=unidade_antiga.get('consumo_mensal', [0] * 12),
            percentual_energia_alocada=unidade_antiga.get('percentual_alocacao', 0.0)
        )
        unidades.append(unidade)

    sistema = SistemaEnergia(
        configuracao=config,
        unidades=unidades,
        versao_sistema="2.0-Legacy-Import"
    )

    # Armazenar dados originais para referência
    sistema.dados_importacao = dados_antigos

    return sistema