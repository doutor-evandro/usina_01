"""
Calculadora de energia solar - Versão adaptada com funcionalidades legacy
"""

from typing import List, Dict, Tuple
import math
from datetime import datetime, timedelta

from nucleo.modelos import (
    SistemaEnergia, ConfiguracaoSistema, UnidadeConsumidora,
    ResultadoMensalEnergia, ResultadoAnualEnergia, TipoLigacao
)
from nucleo.excecoes import ErroCalculoEnergia


class CalculadoraEnergia:
    """Calculadora principal para cálculos energéticos"""

    def __init__(self, sistema: SistemaEnergia):
        self.sistema = sistema
        self.config = sistema.configuracao

    def calcular_geracao_mensal_real(self, mes: int, ano: int = None) -> float:
        """
        Calcula geração real mensal considerando fatores do sistema legacy
        """
        try:
            if not (1 <= mes <= 12):
                raise ErroCalculoEnergia(f"Mês inválido: {mes}")

            # Geração base do mês (índice 0-11)
            geracao_base = self.config.geracao_mensal_kwh[mes - 1]

            # Aplicar eficiência do sistema
            geracao_com_eficiencia = geracao_base * self.config.eficiencia_sistema

            # Aplicar perdas do sistema (do sistema legacy)
            geracao_com_perdas = geracao_com_eficiencia * (1 - self.config.perdas_sistema)

            # Aplicar fator de simultaneidade (do sistema legacy)
            geracao_final = geracao_com_perdas * self.config.fator_simultaneidade

            return max(0.0, geracao_final)

        except Exception as e:
            raise ErroCalculoEnergia(f"Erro ao calcular geração mensal: {e}")

    def calcular_consumo_total_mensal(self, mes: int) -> float:
        """
        Calcula consumo total mensal de todas as unidades ativas
        """
        try:
            if not (1 <= mes <= 12):
                raise ErroCalculoEnergia(f"Mês inválido: {mes}")

            consumo_total = 0.0
            unidades_ativas = self.sistema.get_unidades_ativas()

            for unidade in unidades_ativas:
                # Consumo do mês (índice 0-11)
                consumo_unidade = unidade.consumo_mensal_kwh[mes - 1]
                consumo_total += consumo_unidade

            return consumo_total

        except Exception as e:
            raise ErroCalculoEnergia(f"Erro ao calcular consumo total: {e}")

    def calcular_consumo_minimo_mensal(self, mes: int) -> float:
        """
        Calcula consumo mínimo mensal (taxa de disponibilidade)
        Funcionalidade do sistema legacy
        """
        try:
            consumo_minimo_total = 0.0
            unidades_ativas = self.sistema.get_unidades_ativas()

            for unidade in unidades_ativas:
                taxa_disponibilidade = unidade.get_taxa_disponibilidade()
                consumo_minimo_total += taxa_disponibilidade

            return consumo_minimo_total

        except Exception as e:
            raise ErroCalculoEnergia(f"Erro ao calcular consumo mínimo: {e}")

    def calcular_saldo_energetico_mensal(self, mes: int, ano: int = None) -> Tuple[float, float, float]:
        """
        Calcula saldo energético mensal
        Retorna: (saldo_kwh, energia_injetada, energia_consumida_rede)
        """
        try:
            geracao = self.calcular_geracao_mensal_real(mes, ano)
            consumo = self.calcular_consumo_total_mensal(mes)
            consumo_minimo = self.calcular_consumo_minimo_mensal(mes)

            # Consumo efetivo (maior entre consumo real e mínimo)
            consumo_efetivo = max(consumo, consumo_minimo)

            # Saldo energético
            saldo = geracao - consumo_efetivo

            # Energia injetada na rede (quando há excesso)
            energia_injetada = max(0.0, saldo) * self.config.percentual_injecao_rede

            # Energia consumida da rede (quando há déficit)
            energia_consumida_rede = max(0.0, -saldo)

            return saldo, energia_injetada, energia_consumida_rede

        except Exception as e:
            raise ErroCalculoEnergia(f"Erro ao calcular saldo energético: {e}")

    def calcular_fator_capacidade_real(self, mes: int, ano: int = None) -> float:
        """
        Calcula fator de capacidade real do sistema
        Funcionalidade do sistema legacy
        """
        try:
            geracao_real = self.calcular_geracao_mensal_real(mes, ano)

            # Dias no mês
            if ano:
                import calendar
                dias_mes = calendar.monthrange(ano, mes)[1]
            else:
                dias_mes = 30  # Aproximação

            # Geração máxima teórica (24h por dia)
            geracao_maxima_teorica = (
                    self.config.potencia_instalada_kw * 24 * dias_mes
            )

            if geracao_maxima_teorica > 0:
                fator_capacidade = geracao_real / geracao_maxima_teorica
                return min(1.0, fator_capacidade)

            return 0.0

        except Exception as e:
            raise ErroCalculoEnergia(f"Erro ao calcular fator de capacidade: {e}")

    def calcular_eficiencia_real_sistema(self, mes: int, ano: int = None) -> float:
        """
        Calcula eficiência real do sistema considerando perdas
        Funcionalidade do sistema legacy
        """
        try:
            geracao_teorica = self.config.geracao_mensal_kwh[mes - 1]
            geracao_real = self.calcular_geracao_mensal_real(mes, ano)

            if geracao_teorica > 0:
                eficiencia_real = geracao_real / geracao_teorica
                return min(1.0, eficiencia_real)

            return 0.0

        except Exception as e:
            raise ErroCalculoEnergia(f"Erro ao calcular eficiência real: {e}")

    def calcular_perdas_sistema_kwh(self, mes: int, ano: int = None) -> float:
        """
        Calcula perdas do sistema em kWh
        Funcionalidade do sistema legacy
        """
        try:
            geracao_teorica = self.config.geracao_mensal_kwh[mes - 1]
            geracao_real = self.calcular_geracao_mensal_real(mes, ano)

            perdas_kwh = max(0.0, geracao_teorica - geracao_real)
            return perdas_kwh

        except Exception as e:
            raise ErroCalculoEnergia(f"Erro ao calcular perdas: {e}")

    def calcular_resultado_mensal_energia(self, mes: int, ano: int = None) -> ResultadoMensalEnergia:
        """
        Calcula resultado energético completo para um mês
        """
        try:
            geracao = self.calcular_geracao_mensal_real(mes, ano)
            consumo_total = self.calcular_consumo_total_mensal(mes)
            saldo, energia_injetada, energia_consumida_rede = self.calcular_saldo_energetico_mensal(mes, ano)

            # Cálculos adicionais do sistema legacy
            fator_capacidade_real = self.calcular_fator_capacidade_real(mes, ano)
            eficiencia_real = self.calcular_eficiencia_real_sistema(mes, ano)
            perdas_kwh = self.calcular_perdas_sistema_kwh(mes, ano)

            # Créditos (simplificado - será expandido na próxima fase)
            creditos_gerados = max(0.0, saldo)
            creditos_utilizados = 0.0  # Será calculado pelo gerenciador de distribuição

            return ResultadoMensalEnergia(
                mes=mes,
                geracao_kwh=geracao,
                consumo_total_kwh=consumo_total,
                saldo_kwh=saldo,
                creditos_gerados_kwh=creditos_gerados,
                creditos_utilizados_kwh=creditos_utilizados,
                energia_injetada_kwh=energia_injetada,
                energia_consumida_rede_kwh=energia_consumida_rede,
                fator_capacidade_real=fator_capacidade_real,
                eficiencia_real=eficiencia_real,
                perdas_kwh=perdas_kwh
            )

        except Exception as e:
            raise ErroCalculoEnergia(f"Erro ao calcular resultado mensal: {e}")

    def calcular_resultado_anual_energia(self, ano: int = None) -> ResultadoAnualEnergia:
        """
        Calcula resultado energético anual completo
        """
        try:
            if ano is None:
                ano = datetime.now().year

            resultados_mensais = []
            geracao_total = 0.0
            consumo_total = 0.0
            creditos_acumulados = 0.0
            perdas_totais = 0.0

            # Calcular para cada mês
            for mes in range(1, 13):
                resultado_mensal = self.calcular_resultado_mensal_energia(mes, ano)
                resultados_mensais.append(resultado_mensal)

                geracao_total += resultado_mensal.geracao_kwh
                consumo_total += resultado_mensal.consumo_total_kwh
                creditos_acumulados += resultado_mensal.creditos_gerados_kwh
                perdas_totais += resultado_mensal.perdas_kwh

            # Saldo anual
            saldo_anual = geracao_total - consumo_total

            # Autossuficiência percentual
            if consumo_total > 0:
                autossuficiencia = min(100.0, (geracao_total / consumo_total) * 100)
            else:
                autossuficiencia = 0.0

            # Métricas médias do sistema legacy
            fatores_capacidade = [r.fator_capacidade_real for r in resultados_mensais]
            fator_capacidade_medio = sum(fatores_capacidade) / len(fatores_capacidade)

            eficiencias = [r.eficiencia_real for r in resultados_mensais]
            eficiencia_media = sum(eficiencias) / len(eficiencias)

            return ResultadoAnualEnergia(
                ano=ano,
                geracao_total_kwh=geracao_total,
                consumo_total_kwh=consumo_total,
                saldo_anual_kwh=saldo_anual,
                creditos_acumulados_kwh=creditos_acumulados,
                autossuficiencia_percentual=autossuficiencia,
                resultados_mensais=resultados_mensais,
                fator_capacidade_medio=fator_capacidade_medio,
                eficiencia_media=eficiencia_media,
                perdas_totais_kwh=perdas_totais
            )

        except Exception as e:
            raise ErroCalculoEnergia(f"Erro ao calcular resultado anual: {e}")

    def calcular_projecao_multiplos_anos(self, anos: int = 5) -> List[ResultadoAnualEnergia]:
        """
        Calcula projeção para múltiplos anos
        Funcionalidade do sistema legacy
        """
        try:
            ano_inicial = datetime.now().year
            resultados = []

            for i in range(anos):
                ano = ano_inicial + i
                resultado_anual = self.calcular_resultado_anual_energia(ano)
                resultados.append(resultado_anual)

            return resultados

        except Exception as e:
            raise ErroCalculoEnergia(f"Erro ao calcular projeção: {e}")

    def calcular_metricas_performance(self) -> Dict[str, float]:
        """
        Calcula métricas de performance do sistema
        Funcionalidade do sistema legacy
        """
        try:
            resultado_anual = self.calcular_resultado_anual_energia()

            metricas = {
                'geracao_especifica_kwh_kw': (
                    resultado_anual.geracao_total_kwh / self.config.potencia_instalada_kw
                    if self.config.potencia_instalada_kw > 0 else 0.0
                ),
                'fator_capacidade_medio': resultado_anual.fator_capacidade_medio,
                'eficiencia_media': resultado_anual.eficiencia_media,
                'autossuficiencia_percentual': resultado_anual.autossuficiencia_percentual,
                'perdas_percentuais': (
                    (resultado_anual.perdas_totais_kwh / sum(self.config.geracao_mensal_kwh)) * 100
                    if sum(self.config.geracao_mensal_kwh) > 0 else 0.0
                ),
                'utilizacao_sistema_percentual': (
                    (resultado_anual.consumo_total_kwh / resultado_anual.geracao_total_kwh) * 100
                    if resultado_anual.geracao_total_kwh > 0 else 0.0
                )
            }

            return metricas

        except Exception as e:
            raise ErroCalculoEnergia(f"Erro ao calcular métricas: {e}")


class CalculadoraEnergiaSolar:
    """
    Calculadora específica para sistemas solares fotovoltaicos
    Funcionalidades avançadas do sistema legacy
    """

    def __init__(self, sistema: SistemaEnergia):
        self.sistema = sistema
        self.config = sistema.configuracao

    def calcular_irradiacao_mensal(self, mes: int, latitude: float = -15.0) -> float:
        """
        Calcula irradiação solar mensal estimada
        Funcionalidade do sistema legacy
        """
        try:
            # Irradiação base para o Brasil (kWh/m²/dia)
            irradiacao_base = [5.5, 5.8, 5.2, 4.8, 4.2, 3.8, 4.1, 4.6, 5.0, 5.4, 5.7, 5.6]

            # Ajuste por latitude (simplificado)
            fator_latitude = 1.0 + (latitude + 15.0) * 0.01

            irradiacao_diaria = irradiacao_base[mes - 1] * fator_latitude

            # Dias no mês (aproximação)
            dias_mes = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

            irradiacao_mensal = irradiacao_diaria * dias_mes[mes - 1]

            return max(0.0, irradiacao_mensal)

        except Exception as e:
            raise ErroCalculoEnergia(f"Erro ao calcular irradiação: {e}")

    def calcular_temperatura_celula(self, mes: int, temperatura_ambiente: float = 25.0) -> float:
        """
        Calcula temperatura da célula fotovoltaica
        Funcionalidade do sistema legacy
        """
        try:
            # Temperatura ambiente média mensal (°C)
            temp_ambiente_mensal = [26, 26, 25, 24, 22, 21, 21, 23, 25, 26, 26, 26]

            if temperatura_ambiente == 25.0:  # Usar dados padrão
                temp_ambiente = temp_ambiente_mensal[mes - 1]
            else:
                temp_ambiente = temperatura_ambiente

            # Temperatura da célula (NOCT - Normal Operating Cell Temperature)
            # Fórmula simplificada: Tc = Ta + (NOCT - 20) * (G / 800)
            noct = 45.0  # Temperatura nominal de operação da célula
            irradiancia_media = 600.0  # W/m² (aproximação)

            temp_celula = temp_ambiente + (noct - 20) * (irradiancia_media / 800)

            return temp_celula

        except Exception as e:
            raise ErroCalculoEnergia(f"Erro ao calcular temperatura da célula: {e}")

    def calcular_eficiencia_temperatura(self, mes: int) -> float:
        """
        Calcula redução de eficiência por temperatura
        Funcionalidade do sistema legacy
        """
        try:
            temp_celula = self.calcular_temperatura_celula(mes)
            temp_referencia = 25.0  # Temperatura de referência STC
            coef_temperatura = -0.004  # %/°C (típico para silício cristalino)

            reducao_eficiencia = (temp_celula - temp_referencia) * coef_temperatura
            fator_temperatura = 1.0 + reducao_eficiencia

            return max(0.5, fator_temperatura)  # Mínimo de 50% de eficiência

        except Exception as e:
            raise ErroCalculoEnergia(f"Erro ao calcular eficiência por temperatura: {e}")

    def calcular_degradacao_anual(self, ano: int) -> float:
        """
        Calcula degradação anual dos painéis
        Funcionalidade do sistema legacy
        """
        try:
            ano_instalacao = datetime.now().year  # Assumir instalação atual
            anos_operacao = max(0, ano - ano_instalacao)

            # Degradação típica: 0.5% ao ano após o primeiro ano
            if anos_operacao == 0:
                degradacao = 0.0
            elif anos_operacao == 1:
                degradacao = 0.025  # 2.5% no primeiro ano
            else:
                degradacao = 0.025 + (anos_operacao - 1) * 0.005

            fator_degradacao = 1.0 - degradacao

            return max(0.7, fator_degradacao)  # Mínimo de 70% após degradação

        except Exception as e:
            raise ErroCalculoEnergia(f"Erro ao calcular degradação: {e}")


# Funções auxiliares para compatibilidade
def calcular_energia_sistema_legacy(sistema: SistemaEnergia, mes: int = None) -> Dict[str, float]:
    """
    Função de compatibilidade com sistema legacy
    """
    calculadora = CalculadoraEnergia(sistema)

    if mes:
        resultado = calculadora.calcular_resultado_mensal_energia(mes)
        return {
            'geracao_kwh': resultado.geracao_kwh,
            'consumo_kwh': resultado.consumo_total_kwh,
            'saldo_kwh': resultado.saldo_kwh,
            'eficiencia_real': resultado.eficiencia_real,
            'perdas_kwh': resultado.perdas_kwh
        }
    else:
        resultado = calculadora.calcular_resultado_anual_energia()
        return {
            'geracao_total_kwh': resultado.geracao_total_kwh,
            'consumo_total_kwh': resultado.consumo_total_kwh,
            'saldo_anual_kwh': resultado.saldo_anual_kwh,
            'autossuficiencia_percentual': resultado.autossuficiencia_percentual,
            'perdas_totais_kwh': resultado.perdas_totais_kwh
        }