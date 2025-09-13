"""
Gerenciador de distribuição e cálculos financeiros - Versão adaptada com funcionalidades legacy
"""

from typing import List, Dict, Tuple, Optional
from datetime import datetime, timedelta
import math

from nucleo.modelos import (
    SistemaEnergia, ConfiguracaoSistema, UnidadeConsumidora,
    ResultadoMensalFinanceiro, ResultadoAnualFinanceiro,
    HistoricoCreditos, BandeiraTarifaria, TipoLigacao
)
from nucleo.excecoes import ErroCalculoFinanceiro
from negocio.calculadora_energia import CalculadoraEnergia


class GerenciadorDistribuicao:
    """Gerenciador principal para cálculos financeiros e distribuição de energia"""

    def __init__(self, sistema: SistemaEnergia):
        self.sistema = sistema
        self.config = sistema.configuracao
        self.calculadora_energia = CalculadoraEnergia(sistema)

    def calcular_custo_energia_sem_solar(self, mes: int, consumo_kwh: float,
                                         bandeira: BandeiraTarifaria = None) -> Dict[str, float]:
        """
        Calcula custo da energia sem sistema solar
        Funcionalidade adaptada do sistema legacy
        """
        try:
            if bandeira is None:
                bandeira = self.config.bandeira_atual

            # Tarifa base
            tarifa_base = self.config.tarifa_energia_kwh

            # Adicional da bandeira tarifária
            adicional_bandeira = self._calcular_adicional_bandeira(bandeira)
            tarifa_total = tarifa_base + adicional_bandeira

            # Custo da energia consumida
            custo_energia = consumo_kwh * tarifa_total

            # Taxa de disponibilidade (custo mínimo)
            taxa_disponibilidade = self._calcular_taxa_disponibilidade_total()

            # Custo TUSD e TE (separados para compatibilidade legacy)
            custo_tusd = consumo_kwh * self.config.tarifa_tusd_kwh
            custo_te = consumo_kwh * self.config.tarifa_te_kwh

            # Impostos (PIS/COFINS/ICMS - aproximação)
            base_impostos = custo_energia + custo_tusd + custo_te
            impostos = base_impostos * 0.25  # Aproximação 25%

            # Custo total
            custo_total = max(custo_energia + custo_tusd + custo_te + impostos, taxa_disponibilidade)

            return {
                'custo_energia': custo_energia,
                'custo_tusd': custo_tusd,
                'custo_te': custo_te,
                'taxa_disponibilidade': taxa_disponibilidade,
                'impostos': impostos,
                'adicional_bandeira': consumo_kwh * adicional_bandeira,
                'custo_total': custo_total,
                'tarifa_efetiva': custo_total / consumo_kwh if consumo_kwh > 0 else 0
            }

        except Exception as e:
            raise ErroCalculoFinanceiro(f"Erro ao calcular custo sem solar: {e}")

    def calcular_custo_energia_com_solar(self, mes: int, ano: int = None) -> Dict[str, float]:
        """
        Calcula custo da energia com sistema solar
        Funcionalidade adaptada do sistema legacy
        """
        try:
            # Obter dados energéticos do mês
            resultado_energia = self.calculadora_energia.calcular_resultado_mensal_energia(mes, ano)

            # Consumo da rede (quando há déficit)
            consumo_rede = resultado_energia.energia_consumida_rede_kwh

            # Taxa de disponibilidade sempre cobrada
            taxa_disponibilidade = self._calcular_taxa_disponibilidade_total()

            if consumo_rede > 0:
                # Há consumo da rede - calcular custo
                custo_rede = self.calcular_custo_energia_sem_solar(mes, consumo_rede)

                # Custo total é o maior entre custo calculado e taxa mínima
                custo_total = max(custo_rede['custo_total'], taxa_disponibilidade)

                return {
                    'consumo_rede_kwh': consumo_rede,
                    'custo_energia_rede': custo_rede['custo_energia'],
                    'custo_tusd': custo_rede['custo_tusd'],
                    'custo_te': custo_rede['custo_te'],
                    'taxa_disponibilidade': taxa_disponibilidade,
                    'impostos': custo_rede['impostos'],
                    'adicional_bandeira': custo_rede['adicional_bandeira'],
                    'custo_total': custo_total,
                    'economia_vs_sem_solar': 0.0  # Será calculado externamente
                }
            else:
                # Não há consumo da rede - apenas taxa mínima
                return {
                    'consumo_rede_kwh': 0.0,
                    'custo_energia_rede': 0.0,
                    'custo_tusd': 0.0,
                    'custo_te': 0.0,
                    'taxa_disponibilidade': taxa_disponibilidade,
                    'impostos': 0.0,
                    'adicional_bandeira': 0.0,
                    'custo_total': taxa_disponibilidade,
                    'economia_vs_sem_solar': 0.0
                }

        except Exception as e:
            raise ErroCalculoFinanceiro(f"Erro ao calcular custo com solar: {e}")

    def calcular_valor_creditos_gerados(self, creditos_kwh: float, mes: int) -> float:
        """
        Calcula valor monetário dos créditos gerados
        Funcionalidade do sistema legacy
        """
        try:
            # Valor dos créditos baseado na tarifa sem impostos
            tarifa_credito = self.config.tarifa_tusd_kwh + self.config.tarifa_te_kwh

            # Adicional da bandeira (se aplicável)
            adicional_bandeira = self._calcular_adicional_bandeira(self.config.bandeira_atual)
            tarifa_credito += adicional_bandeira

            valor_creditos = creditos_kwh * tarifa_credito

            return valor_creditos

        except Exception as e:
            raise ErroCalculoFinanceiro(f"Erro ao calcular valor dos créditos: {e}")

    def gerenciar_creditos_energia(self, mes: int, ano: int = None) -> Dict[str, float]:
        """
        Gerencia créditos de energia (geração, utilização, vencimento)
        Funcionalidade do sistema legacy
        """
        try:
            if ano is None:
                ano = datetime.now().year

            # Obter dados energéticos
            resultado_energia = self.calculadora_energia.calcular_resultado_mensal_energia(mes, ano)

            # Créditos gerados no mês
            creditos_gerados = resultado_energia.creditos_gerados_kwh

            # Créditos utilizados (quando há déficit)
            creditos_utilizados = 0.0
            if resultado_energia.energia_consumida_rede_kwh > 0:
                # Tentar usar créditos disponíveis antes de consumir da rede
                creditos_disponiveis = self._obter_creditos_disponiveis(mes, ano)
                creditos_utilizados = min(creditos_disponiveis, resultado_energia.energia_consumida_rede_kwh)

            # Valor monetário
            valor_creditos_gerados = self.calcular_valor_creditos_gerados(creditos_gerados, mes)
            valor_creditos_utilizados = self.calcular_valor_creditos_gerados(creditos_utilizados, mes)

            # Atualizar histórico de créditos
            if creditos_gerados > 0:
                self._adicionar_credito_historico(mes, ano, creditos_gerados)

            if creditos_utilizados > 0:
                self._utilizar_creditos_historico(creditos_utilizados, mes, ano)

            return {
                'creditos_gerados_kwh': creditos_gerados,
                'creditos_utilizados_kwh': creditos_utilizados,
                'creditos_saldo_kwh': creditos_gerados - creditos_utilizados,
                'valor_creditos_gerados': valor_creditos_gerados,
                'valor_creditos_utilizados': valor_creditos_utilizados,
                'creditos_disponiveis_total': self._obter_creditos_disponiveis(mes, ano)
            }

        except Exception as e:
            raise ErroCalculoFinanceiro(f"Erro ao gerenciar créditos: {e}")

    def calcular_resultado_financeiro_mensal(self, mes: int, ano: int = None) -> ResultadoMensalFinanceiro:
        """
        Calcula resultado financeiro completo para um mês
        """
        try:
            if ano is None:
                ano = datetime.now().year

            # Consumo total do mês
            consumo_total = self.calculadora_energia.calcular_consumo_total_mensal(mes)

            # Custo sem sistema solar
            custo_sem_solar = self.calcular_custo_energia_sem_solar(mes, consumo_total)

            # Custo com sistema solar
            custo_com_solar = self.calcular_custo_energia_com_solar(mes, ano)

            # Gerenciamento de créditos
            creditos_info = self.gerenciar_creditos_energia(mes, ano)

            # Economia mensal
            economia_mensal = custo_sem_solar['custo_total'] - custo_com_solar['custo_total']
            economia_mensal += creditos_info['valor_creditos_utilizados']  # Valor dos créditos usados

            # Valor da energia injetada (créditos gerados)
            valor_energia_injetada = creditos_info['valor_creditos_gerados']

            return ResultadoMensalFinanceiro(
                mes=mes,
                custo_sem_solar=custo_sem_solar['custo_total'],
                custo_com_solar=custo_com_solar['custo_total'],
                economia_mensal=economia_mensal,
                valor_energia_injetada=valor_energia_injetada,
                valor_creditos_utilizados=creditos_info['valor_creditos_utilizados'],
                bandeira_aplicada=self.config.bandeira_atual,
                valor_bandeira=custo_sem_solar.get('adicional_bandeira', 0.0),
                custo_disponibilidade=custo_com_solar['taxa_disponibilidade'],
                custo_demanda=0.0,  # Para unidades do grupo A
                impostos=custo_sem_solar['impostos']
            )

        except Exception as e:
            raise ErroCalculoFinanceiro(f"Erro ao calcular resultado financeiro mensal: {e}")

    def calcular_payback_simples(self) -> float:
        """
        Calcula payback simples do investimento
        Funcionalidade do sistema legacy
        """
        try:
            if self.config.custo_investimento <= 0:
                return 0.0

            # Calcular economia anual
            economia_anual = 0.0
            for mes in range(1, 13):
                resultado_mensal = self.calcular_resultado_financeiro_mensal(mes)
                economia_anual += resultado_mensal.economia_mensal

            if economia_anual <= 0:
                return float('inf')  # Nunca se paga

            payback_anos = self.config.custo_investimento / economia_anual

            return payback_anos

        except Exception as e:
            raise ErroCalculoFinanceiro(f"Erro ao calcular payback: {e}")

    def calcular_roi_percentual(self, anos_analise: int = 25) -> float:
        """
        Calcula ROI (Return on Investment) percentual
        Funcionalidade do sistema legacy
        """
        try:
            if self.config.custo_investimento <= 0:
                return 0.0

            # Economia anual
            economia_anual = 0.0
            for mes in range(1, 13):
                resultado_mensal = self.calcular_resultado_financeiro_mensal(mes)
                economia_anual += resultado_mensal.economia_mensal

            # Economia total no período (considerando degradação)
            economia_total = 0.0
            for ano in range(anos_analise):
                # Degradação anual (0.5% ao ano após primeiro ano)
                if ano == 0:
                    fator_degradacao = 0.975  # 2.5% no primeiro ano
                else:
                    fator_degradacao = 0.975 - (ano * 0.005)

                fator_degradacao = max(0.7, fator_degradacao)  # Mínimo 70%
                economia_ano = economia_anual * fator_degradacao
                economia_total += economia_ano

            # ROI percentual
            roi = ((economia_total - self.config.custo_investimento) / self.config.custo_investimento) * 100

            return roi

        except Exception as e:
            raise ErroCalculoFinanceiro(f"Erro ao calcular ROI: {e}")

    def calcular_tir_percentual(self, anos_analise: int = 25) -> float:
        """
        Calcula TIR (Taxa Interna de Retorno) percentual
        Funcionalidade do sistema legacy
        """
        try:
            # Fluxo de caixa inicial (investimento negativo)
            fluxo_caixa = [-self.config.custo_investimento]

            # Economia anual para cada ano
            economia_anual = 0.0
            for mes in range(1, 13):
                resultado_mensal = self.calcular_resultado_financeiro_mensal(mes)
                economia_anual += resultado_mensal.economia_mensal

            # Adicionar fluxos anuais
            for ano in range(anos_analise):
                if ano == 0:
                    fator_degradacao = 0.975
                else:
                    fator_degradacao = 0.975 - (ano * 0.005)

                fator_degradacao = max(0.7, fator_degradacao)
                economia_ano = economia_anual * fator_degradacao
                fluxo_caixa.append(economia_ano)

            # Cálculo simplificado da TIR usando método iterativo
            tir = self._calcular_tir_iterativo(fluxo_caixa)

            return tir * 100  # Converter para percentual

        except Exception as e:
            raise ErroCalculoFinanceiro(f"Erro ao calcular TIR: {e}")

    def calcular_resultado_financeiro_anual(self, ano: int = None) -> ResultadoAnualFinanceiro:
        """
        Calcula resultado financeiro anual completo
        """
        try:
            if ano is None:
                ano = datetime.now().year

            resultados_mensais = []
            economia_total = 0.0
            custo_total_sem_solar = 0.0
            custo_total_com_solar = 0.0

            # Calcular para cada mês
            for mes in range(1, 13):
                resultado_mensal = self.calcular_resultado_financeiro_mensal(mes, ano)
                resultados_mensais.append(resultado_mensal)

                economia_total += resultado_mensal.economia_mensal
                custo_total_sem_solar += resultado_mensal.custo_sem_solar
                custo_total_com_solar += resultado_mensal.custo_com_solar

            # Cálculos financeiros
            payback_simples = self.calcular_payback_simples()
            roi_percentual = self.calcular_roi_percentual()
            tir_percentual = self.calcular_tir_percentual()

            # Economia acumulada (considerando anos anteriores)
            economia_acumulada = economia_total  # Simplificado para um ano

            return ResultadoAnualFinanceiro(
                ano=ano,
                economia_total=economia_total,
                custo_total_sem_solar=custo_total_sem_solar,
                custo_total_com_solar=custo_total_com_solar,
                payback_simples_anos=payback_simples,
                roi_percentual=roi_percentual,
                resultados_mensais=resultados_mensais,
                valor_investimento=self.config.custo_investimento,
                economia_acumulada=economia_acumulada,
                tir_percentual=tir_percentual
            )

        except Exception as e:
            raise ErroCalculoFinanceiro(f"Erro ao calcular resultado financeiro anual: {e}")

    # Métodos auxiliares privados

    def _calcular_adicional_bandeira(self, bandeira: BandeiraTarifaria) -> float:
        """Calcula adicional da bandeira tarifária"""
        adicionais = {
            BandeiraTarifaria.VERDE: 0.0,
            BandeiraTarifaria.AMARELA: self.config.adicional_bandeira_amarela,
            BandeiraTarifaria.VERMELHA_1: self.config.adicional_bandeira_vermelha_1,
            BandeiraTarifaria.VERMELHA_2: self.config.adicional_bandeira_vermelha_2,
            BandeiraTarifaria.ESCASSEZ: self.config.adicional_bandeira_escassez
        }
        return adicionais.get(bandeira, 0.0)

    def _calcular_taxa_disponibilidade_total(self) -> float:
        """Calcula taxa de disponibilidade total de todas as unidades"""
        taxa_total = 0.0
        for unidade in self.sistema.get_unidades_ativas():
            taxa_total += unidade.get_taxa_disponibilidade()
        return taxa_total

    def _obter_creditos_disponiveis(self, mes: int, ano: int) -> float:
        """Obtém créditos disponíveis considerando vencimento"""
        creditos_disponiveis = 0.0
        data_atual = datetime(ano, mes, 1)

        for credito in self.sistema.historico_creditos:
            if credito.ativo and credito.creditos_restantes_kwh > 0:
                data_vencimento = datetime(credito.ano_vencimento, credito.mes_vencimento, 1)
                if data_vencimento >= data_atual:
                    creditos_disponiveis += credito.creditos_restantes_kwh

        return creditos_disponiveis

    def _adicionar_credito_historico(self, mes: int, ano: int, creditos_kwh: float):
        """Adiciona crédito ao histórico"""
        # Calcular vencimento (60 meses)
        data_geracao = datetime(ano, mes, 1)
        data_vencimento = data_geracao + timedelta(days=60 * 30)  # Aproximação

        credito = HistoricoCreditos(
            mes_geracao=mes,
            ano_geracao=ano,
            creditos_kwh=creditos_kwh,
            creditos_utilizados_kwh=0.0,
            creditos_restantes_kwh=creditos_kwh,
            mes_vencimento=data_vencimento.month,
            ano_vencimento=data_vencimento.year,
            ativo=True
        )

        self.sistema.historico_creditos.append(credito)

    def _utilizar_creditos_historico(self, creditos_utilizados: float, mes: int, ano: int):
        """Utiliza créditos do histórico (FIFO - primeiro a vencer, primeiro a usar)"""
        creditos_restantes = creditos_utilizados

        # Ordenar por data de vencimento
        creditos_ordenados = sorted(
            [c for c in self.sistema.historico_creditos if c.ativo and c.creditos_restantes_kwh > 0],
            key=lambda x: (x.ano_vencimento, x.mes_vencimento)
        )

        for credito in creditos_ordenados:
            if creditos_restantes <= 0:
                break

            utilizacao = min(credito.creditos_restantes_kwh, creditos_restantes)
            credito.creditos_utilizados_kwh += utilizacao
            credito.creditos_restantes_kwh -= utilizacao
            creditos_restantes -= utilizacao

            if credito.creditos_restantes_kwh <= 0:
                credito.ativo = False

    def _calcular_tir_iterativo(self, fluxo_caixa: List[float], precisao: float = 0.0001) -> float:
        """Calcula TIR usando método iterativo (Newton-Raphson simplificado)"""
        try:
            # Estimativa inicial
            taxa = 0.1  # 10%

            for _ in range(100):  # Máximo 100 iterações
                vpl = sum(fluxo / ((1 + taxa) ** i) for i, fluxo in enumerate(fluxo_caixa))

                if abs(vpl) < precisao:
                    return taxa

                # Derivada do VPL
                dvpl = sum(-i * fluxo / ((1 + taxa) ** (i + 1)) for i, fluxo in enumerate(fluxo_caixa) if i > 0)

                if abs(dvpl) < precisao:
                    break

                # Nova estimativa
                taxa = taxa - vpl / dvpl

                # Limitar taxa entre -50% e 100%
                taxa = max(-0.5, min(1.0, taxa))

            return taxa

        except:
            return 0.0  # Retorna 0% se não conseguir calcular


# Funções auxiliares para compatibilidade
def calcular_economia_sistema_legacy(sistema: SistemaEnergia, mes: int = None) -> Dict[str, float]:
    """
    Função de compatibilidade com sistema legacy para cálculos financeiros
    """
    gerenciador = GerenciadorDistribuicao(sistema)

    if mes:
        resultado = gerenciador.calcular_resultado_financeiro_mensal(mes)
        return {
            'custo_sem_solar': resultado.custo_sem_solar,
            'custo_com_solar': resultado.custo_com_solar,
            'economia_mensal': resultado.economia_mensal,
            'valor_energia_injetada': resultado.valor_energia_injetada,
            'payback_anos': gerenciador.calcular_payback_simples()
        }
    else:
        resultado = gerenciador.calcular_resultado_financeiro_anual()
        return {
            'economia_anual': resultado.economia_total,
            'custo_total_sem_solar': resultado.custo_total_sem_solar,
            'custo_total_com_solar': resultado.custo_total_com_solar,
            'payback_anos': resultado.payback_simples_anos,
            'roi_percentual': resultado.roi_percentual,
            'tir_percentual': resultado.tir_percentual
        }