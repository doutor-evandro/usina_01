"""
Gerador de relatórios do sistema de energia solar - Versão Simplificada
"""

from datetime import datetime
from typing import Optional, List
from nucleo.modelos import SistemaEnergia
from negocio.calculadora_energia import CalculadoraEnergia
from negocio.gerenciador_distribuicao import GerenciadorDistribuicao
from utilitarios.formatadores import formatar_moeda, formatar_energia, formatar_percentual


class GeradorRelatorios:
    """Gerador de relatórios do sistema - Versão Simplificada"""

    def __init__(self, sistema: SistemaEnergia):
        self.sistema = sistema
        self.calculadora = CalculadoraEnergia(sistema)
        self.gerenciador = GerenciadorDistribuicao(sistema)

    def gerar_relatorio_completo(self, ano: Optional[int] = None) -> str:
        """
        Gera relatório completo do sistema - Versão Simplificada

        Args:
            ano: Ano para o relatório (padrão: ano atual)

        Returns:
            String com relatório completo
        """
        if ano is None:
            ano = datetime.now().year

        relatorio = []

        try:
            # Cabeçalho
            relatorio.append("=" * 80)
            relatorio.append(f"RELATÓRIO COMPLETO DO SISTEMA DE ENERGIA SOLAR - {ano}")
            relatorio.append("=" * 80)
            relatorio.append(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            relatorio.append(f"Versão do Sistema: {self.sistema.versao_sistema}")
            relatorio.append("")

            # Seção 1: Informações básicas do sistema
            relatorio.extend(self._gerar_secao_sistema_simples())

            # Seção 2: Resultados anuais
            relatorio.extend(self._gerar_secao_resultados_anuais_simples(ano))

            # Seção 3: Unidades (versão simplificada)
            relatorio.extend(self._gerar_secao_unidades_simples())

            # Rodapé
            relatorio.append("=" * 80)
            relatorio.append("Fim do Relatório")
            relatorio.append("=" * 80)

        except Exception as e:
            relatorio.append(f"ERRO na geração do relatório: {str(e)}")
            relatorio.append("")

        return "\n".join(relatorio)

    def _gerar_secao_sistema_simples(self) -> List[str]:
        """Gera seção com informações básicas do sistema"""
        secao = []

        try:
            config = self.sistema.configuracao

            secao.append("CONFIGURAÇÃO DO SISTEMA")
            secao.append("-" * 40)
            secao.append(f"Potência Instalada: {config.potencia_instalada_kw:.2f} kW")
            secao.append(f"Eficiência do Sistema: {config.eficiencia_sistema:.1%}")
            secao.append(f"Tarifa de Energia: {formatar_moeda(config.tarifa_energia_kwh)}/kWh")
            secao.append(f"Custo do Investimento: {formatar_moeda(config.custo_investimento)}")
            secao.append("")

        except Exception as e:
            secao.append("ERRO na seção do sistema:")
            secao.append(f"  {str(e)}")
            secao.append("")

        return secao

    def _gerar_secao_resultados_anuais_simples(self, ano: int) -> List[str]:
        """Gera seção com resultados anuais - Versão Simplificada"""
        secao = []

        try:
            # Calcular resultados
            resultado_energia = self.calculadora.calcular_resultado_anual_energia(ano)
            resultado_financeiro = self.gerenciador.calcular_resultado_financeiro_anual(ano)

            secao.append("RESULTADOS ANUAIS")
            secao.append("-" * 40)

            # Dados energéticos
            secao.append("ENERGIA:")
            secao.append(f"  Geração Total: {formatar_energia(resultado_energia.geracao_total_kwh)}")
            secao.append(f"  Consumo Total: {formatar_energia(resultado_energia.consumo_total_kwh)}")
            secao.append(f"  Saldo Anual: {formatar_energia(resultado_energia.saldo_anual_kwh)}")
            secao.append(f"  Eficiência Média: {formatar_percentual(resultado_energia.eficiencia_media)}")
            secao.append("")

            # Dados financeiros
            secao.append("FINANCEIRO:")
            secao.append(f"  Economia Total: {formatar_moeda(resultado_financeiro.economia_total)}")
            secao.append(f"  Payback Simples: {resultado_financeiro.payback_simples_anos:.1f} anos")
            secao.append(f"  ROI (25 anos): {formatar_percentual(resultado_financeiro.roi_percentual)}")
            secao.append(f"  Valor do Investimento: {formatar_moeda(resultado_financeiro.valor_investimento)}")
            secao.append("")

        except Exception as e:
            secao.append("ERRO ao calcular resultados anuais:")
            secao.append(f"  {str(e)}")
            secao.append("")

        return secao

    def _gerar_secao_unidades_simples(self) -> List[str]:
        """Gera seção com informações das unidades - Versão Simplificada"""
        secao = []

        try:
            secao.append("UNIDADES CONSUMIDORAS")
            secao.append("-" * 40)

            unidades_ativas = self.sistema.get_unidades_ativas()

            secao.append(f"Total de Unidades: {len(self.sistema.unidades)}")
            secao.append(f"Unidades Ativas: {len(unidades_ativas)}")
            secao.append("")

            if unidades_ativas:
                secao.append("UNIDADES ATIVAS:")

                for i, unidade in enumerate(unidades_ativas, 1):
                    try:
                        consumo_anual = sum(unidade.consumo_mensal_kwh)

                        # Usar apenas atributos básicos
                        secao.append(f"{i}. {unidade.nome}")
                        secao.append(f"   Consumo Anual: {formatar_energia(consumo_anual)}")

                        # Tentar obter tipo de ligação de forma segura
                        try:
                            if hasattr(unidade.tipo_ligacao, 'value'):
                                tipo = unidade.tipo_ligacao.value
                            else:
                                tipo = str(unidade.tipo_ligacao)
                            secao.append(f"   Tipo: {tipo}")
                        except:
                            secao.append(f"   Tipo: N/A")

                        secao.append("")

                    except Exception as e:
                        secao.append(f"{i}. ERRO na unidade {unidade.nome}: {str(e)}")
                        secao.append("")

        except Exception as e:
            secao.append("ERRO na seção de unidades:")
            secao.append(f"  {str(e)}")
            secao.append("")

        return secao

    def gerar_relatorio_resumido(self, ano: Optional[int] = None) -> str:
        """
        Gera relatório resumido - Versão mais simples ainda

        Args:
            ano: Ano para o relatório (padrão: ano atual)

        Returns:
            String com relatório resumido
        """
        if ano is None:
            ano = datetime.now().year

        relatorio = []

        try:
            # Cabeçalho
            relatorio.append("=" * 60)
            relatorio.append(f"RELATÓRIO RESUMIDO - {ano}")
            relatorio.append("=" * 60)
            relatorio.append(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            relatorio.append("")

            # Resultados básicos
            resultado_energia = self.calculadora.calcular_resultado_anual_energia(ano)
            resultado_financeiro = self.gerenciador.calcular_resultado_financeiro_anual(ano)

            relatorio.append("RESUMO ANUAL:")
            relatorio.append(f"Geração Total: {formatar_energia(resultado_energia.geracao_total_kwh)}")
            relatorio.append(f"Consumo Total: {formatar_energia(resultado_energia.consumo_total_kwh)}")
            relatorio.append(f"Economia Total: {formatar_moeda(resultado_financeiro.economia_total)}")
            relatorio.append(f"Payback: {resultado_financeiro.payback_simples_anos:.1f} anos")
            relatorio.append("")

            relatorio.append("=" * 60)
            relatorio.append("Fim do Relatório Resumido")
            relatorio.append("=" * 60)

        except Exception as e:
            relatorio.append(f"ERRO: {str(e)}")

        return "\n".join(relatorio)