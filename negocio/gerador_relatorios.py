# usina_01/negocio/gerador_relatorios.py

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
from nucleo.modelos import SistemaEnergia
from negocio.calculadora_energia import CalculadoraEnergia
from negocio.gerenciador_distribuicao import GerenciadorDistribuicao
from utilitarios.formatadores import FormatadorBrasileiro
from utilitarios.constantes import MESES_APENAS


@dataclass
class RelatorioCompleto:
    """Estrutura completa de um relatório do sistema."""
    titulo: str
    data_geracao: str
    resumo_sistema: str
    resumo_energetico: str
    resumo_financeiro: str
    detalhamento_mensal: str
    detalhamento_unidades: str
    analise_payback: str
    conclusoes: str


class GeradorRelatorios:
    """
    Responsável por gerar relatórios textuais completos do sistema de energia solar.
    """

    def __init__(self, sistema: SistemaEnergia):
        self.sistema = sistema
        self.calculadora_energia = CalculadoraEnergia(sistema)
        self.gerenciador_distribuicao = GerenciadorDistribuicao(sistema)
        self.formatador = FormatadorBrasileiro()

    def gerar_relatorio_completo(self, investimento_inicial: Optional[float] = None) -> RelatorioCompleto:
        """
        Gera um relatório completo do sistema.

        Args:
            investimento_inicial: Valor investido no sistema (opcional)

        Returns:
            RelatorioCompleto com todas as seções preenchidas
        """
        # Calcula todos os dados necessários
        resultados_mensais, resumo_anual = self.calculadora_energia.calcular_resultados_anuais()
        resultados_fin_mensais, resumo_fin_anual = self.gerenciador_distribuicao.calcular_resultados_financeiros_anuais()

        # Gera cada seção do relatório
        titulo = "RELATÓRIO DE ANÁLISE DO SISTEMA DE ENERGIA SOLAR"
        data_geracao = datetime.now().strftime("%d/%m/%Y às %H:%M")

        resumo_sistema = self._gerar_resumo_sistema()
        resumo_energetico = self._gerar_resumo_energetico(resumo_anual)
        resumo_financeiro = self._gerar_resumo_financeiro(resumo_fin_anual)
        detalhamento_mensal = self._gerar_detalhamento_mensal(resultados_mensais, resultados_fin_mensais)
        detalhamento_unidades = self._gerar_detalhamento_unidades()
        analise_payback = self._gerar_analise_payback(investimento_inicial, resumo_fin_anual)
        conclusoes = self._gerar_conclusoes(resumo_anual, resumo_fin_anual)

        return RelatorioCompleto(
            titulo=titulo,
            data_geracao=data_geracao,
            resumo_sistema=resumo_sistema,
            resumo_energetico=resumo_energetico,
            resumo_financeiro=resumo_financeiro,
            detalhamento_mensal=detalhamento_mensal,
            detalhamento_unidades=detalhamento_unidades,
            analise_payback=analise_payback,
            conclusoes=conclusoes
        )

    def _gerar_resumo_sistema(self) -> str:
        """Gera o resumo das configurações do sistema."""
        config = self.sistema.configuracao

        texto = "CONFIGURAÇÃO DO SISTEMA\n"
        texto += "=" * 50 + "\n\n"
        texto += f"Potência do Inversor: {self.formatador.formatar_numero(config.potencia_inversor)} W\n"
        texto += f"Potência dos Módulos: {self.formatador.formatar_numero(config.potencia_modulos)} W\n"
        texto += f"Eficiência do Sistema: {self.formatador.formatar_porcentagem(config.eficiencia)}\n"
        texto += f"Valor da Tarifa: R\$ {self.formatador.formatar_numero(config.valor_kwh)}/kWh\n"
        texto += f"Número de Unidades: {self.formatador.formatar_inteiro(len(self.sistema.unidades))}\n\n"

        texto += "UNIDADES CONSUMIDORAS:\n"
        for unidade in self.sistema.unidades:
            texto += f"• {unidade.codigo} - {unidade.nome}\n"
            texto += f"  Tipo: {unidade.tipo_ligacao.value.upper()}\n"
            texto += f"  Tarifa Mínima: {self.formatador.formatar_inteiro(int(unidade.tarifa_minima))} kWh\n"
            if unidade.endereco:
                texto += f"  Endereço: {unidade.endereco}\n"
            texto += "\n"

        return texto

    def _gerar_resumo_energetico(self, resumo_anual) -> str:
        """Gera o resumo energético anual."""
        texto = "RESUMO ENERGÉTICO ANUAL\n"
        texto += "=" * 50 + "\n\n"
        texto += f"Geração Total: {self.formatador.formatar_numero(resumo_anual.geracao_total_kwh)} kWh\n"
        texto += f"Consumo Total: {self.formatador.formatar_numero(resumo_anual.consumo_total_kwh)} kWh\n"
        texto += f"Excesso Total: {self.formatador.formatar_numero(resumo_anual.excesso_total_kwh)} kWh\n"
        texto += f"Déficit Total: {self.formatador.formatar_numero(resumo_anual.deficit_total_kwh)} kWh\n"
        texto += f"Energia Injetada na Rede: {self.formatador.formatar_numero(resumo_anual.energia_injetada_total_kwh)} kWh\n"
        texto += f"Energia Consumida da Rede: {self.formatador.formatar_numero(resumo_anual.energia_consumida_rede_total_kwh)} kWh\n"
        texto += f"Saldo Energético: {self.formatador.formatar_numero(resumo_anual.saldo_energetico_total_kwh)} kWh\n"
        texto += f"Autossuficiência: {self.formatador.formatar_porcentagem(resumo_anual.percentual_autossuficiencia)}\n\n"

        return texto

    def _gerar_resumo_financeiro(self, resumo_fin_anual) -> str:
        """Gera o resumo financeiro anual."""
        texto = "RESUMO FINANCEIRO ANUAL\n"
        texto += "=" * 50 + "\n\n"
        texto += f"Economia Total: R\$ {self.formatador.formatar_numero(resumo_fin_anual.economia_total_reais)}\n"
        texto += f"Custo sem Sistema: R\$ {self.formatador.formatar_numero(resumo_fin_anual.custo_total_sem_sistema_reais)}\n"
        texto += f"Custo com Sistema: R\$ {self.formatador.formatar_numero(resumo_fin_anual.custo_total_com_sistema_reais)}\n"
        texto += f"Percentual de Economia: {self.formatador.formatar_porcentagem(resumo_fin_anual.percentual_economia)}\n"
        texto += f"Economia Mensal Média: R\$ {self.formatador.formatar_numero(resumo_fin_anual.economia_total_reais / 12)}\n\n"

        return texto

    def _gerar_detalhamento_mensal(self, resultados_mensais, resultados_fin_mensais) -> str:
        """Gera o detalhamento mês a mês."""
        texto = "DETALHAMENTO MENSAL\n"
        texto += "=" * 50 + "\n\n"

        for i, mes in enumerate(MESES_APENAS):
            resultado_energia = resultados_mensais[i]
            resultado_financeiro = resultados_fin_mensais[i]

            texto += f"{mes.upper()}\n"
            texto += "-" * 20 + "\n"
            texto += f"Geração: {self.formatador.formatar_numero(resultado_energia.geracao_kwh)} kWh\n"
            texto += f"Consumo: {self.formatador.formatar_numero(resultado_energia.consumo_total_kwh)} kWh\n"
            texto += f"Saldo: {self.formatador.formatar_numero(resultado_energia.saldo_energetico_kwh)} kWh\n"
            texto += f"Economia: R\$ {self.formatador.formatar_numero(resultado_financeiro.economia_reais)}\n"
            texto += f"Custo Final: R\$ {self.formatador.formatar_numero(resultado_financeiro.custo_com_sistema_reais)}\n\n"

        return texto

    def _gerar_detalhamento_unidades(self) -> str:
        """Gera o detalhamento por unidade consumidora."""
        texto = "ANÁLISE POR UNIDADE CONSUMIDORA\n"
        texto += "=" * 50 + "\n\n"

        # Usa Janeiro como mês de referência para a análise
        distribuicoes = self.gerenciador_distribuicao.calcular_distribuicao_por_unidade("Janeiro")

        for dist in distribuicoes:
            texto += f"{dist.codigo} - {dist.nome}\n"
            texto += "-" * 30 + "\n"
            texto += f"Consumo Mensal (Jan): {self.formatador.formatar_numero(dist.consumo_kwh)} kWh\n"
            texto += f"Atendimento pelo Sistema: {self.formatador.formatar_porcentagem(dist.percentual_atendimento)}\n"
            texto += f"Energia da Rede: {self.formatador.formatar_numero(dist.energia_da_rede_kwh)} kWh\n"
            texto += f"Economia Mensal: R\$ {self.formatador.formatar_numero(dist.economia_reais)}\n"
            texto += f"Custo sem Sistema: R\$ {self.formatador.formatar_numero(dist.custo_sem_sistema_reais)}\n"
            texto += f"Custo com Sistema: R\$ {self.formatador.formatar_numero(dist.custo_com_sistema_reais)}\n\n"

        return texto

    def _gerar_analise_payback(self, investimento_inicial: Optional[float], resumo_fin_anual) -> str:
        """Gera a análise de payback do investimento."""
        texto = "ANÁLISE DE RETORNO DO INVESTIMENTO\n"
        texto += "=" * 50 + "\n\n"

        if investimento_inicial is not None:
            payback_anos, economia_mensal = self.gerenciador_distribuicao.calcular_payback_simples(investimento_inicial)

            texto += f"Investimento Inicial: R\$ {self.formatador.formatar_numero(investimento_inicial)}\n"
            texto += f"Economia Anual: R\$ {self.formatador.formatar_numero(resumo_fin_anual.economia_total_reais)}\n"
            texto += f"Economia Mensal Média: R\$ {self.formatador.formatar_numero(economia_mensal)}\n"

            if payback_anos != float('inf'):
                anos = int(payback_anos)
                meses = int((payback_anos - anos) * 12)
                texto += f"Payback Simples: {anos} anos e {meses} meses\n"
                texto += f"Payback em Anos: {self.formatador.formatar_numero(payback_anos)} anos\n\n"

                # Análise do payback
                if payback_anos <= 5:
                    texto += "ANÁLISE: Excelente retorno do investimento!\n"
                elif payback_anos <= 8:
                    texto += "ANÁLISE: Bom retorno do investimento.\n"
                elif payback_anos <= 12:
                    texto += "ANÁLISE: Retorno moderado do investimento.\n"
                else:
                    texto += "ANÁLISE: Retorno longo do investimento.\n"
            else:
                texto += "Payback: Não se paga (economia insuficiente)\n"
        else:
            texto += "Investimento inicial não informado.\n"
            texto += "Para calcular o payback, informe o valor do investimento.\n"

        texto += "\n"
        return texto

    def _gerar_conclusoes(self, resumo_anual, resumo_fin_anual) -> str:
        """Gera as conclusões e recomendações."""
        texto = "CONCLUSÕES E RECOMENDAÇÕES\n"
        texto += "=" * 50 + "\n\n"

        # Análise da autossuficiência
        autossuficiencia = resumo_anual.percentual_autossuficiencia
        if autossuficiencia >= 95:
            texto += "✓ AUTOSSUFICIÊNCIA: Excelente! O sistema atende quase toda a demanda.\n"
        elif autossuficiencia >= 80:
            texto += "✓ AUTOSSUFICIÊNCIA: Muito boa! O sistema atende a maior parte da demanda.\n"
        elif autossuficiencia >= 60:
            texto += "⚠ AUTOSSUFICIÊNCIA: Moderada. Considere expandir o sistema.\n"
        else:
            texto += "⚠ AUTOSSUFICIÊNCIA: Baixa. Sistema subdimensionado.\n"

        # Análise da economia
        economia_percentual = resumo_fin_anual.percentual_economia
        if economia_percentual >= 80:
            texto += "✓ ECONOMIA: Excelente economia na conta de energia!\n"
        elif economia_percentual >= 60:
            texto += "✓ ECONOMIA: Boa economia na conta de energia.\n"
        elif economia_percentual >= 40:
            texto += "⚠ ECONOMIA: Economia moderada.\n"
        else:
            texto += "⚠ ECONOMIA: Economia baixa.\n"

        # Recomendações
        texto += "\nRECOMENDAÇÕES:\n"

        if resumo_anual.deficit_total_kwh > resumo_anual.excesso_total_kwh:
            texto += "• Considere expandir o sistema para reduzir o déficit energético.\n"

        if resumo_anual.excesso_total_kwh > resumo_anual.deficit_total_kwh * 1.5:
            texto += "• Sistema com excesso significativo. Avalie adicionar mais unidades.\n"

        if economia_percentual < 70:
            texto += "• Revise a configuração do sistema para otimizar a economia.\n"

        texto += "• Monitore mensalmente o desempenho do sistema.\n"
        texto += "• Mantenha os módulos limpos para máxima eficiência.\n"

        return texto

    def gerar_relatorio_texto(self, investimento_inicial: Optional[float] = None) -> str:
        """
        Gera um relatório completo em formato de texto.

        Args:
            investimento_inicial: Valor investido no sistema (opcional)

        Returns:
            String com o relatório completo formatado
        """
        relatorio = self.gerar_relatorio_completo(investimento_inicial)

        texto_completo = f"{relatorio.titulo}\n"
        texto_completo += "=" * len(relatorio.titulo) + "\n"
        texto_completo += f"Gerado em: {relatorio.data_geracao}\n\n"

        texto_completo += relatorio.resumo_sistema + "\n"
        texto_completo += relatorio.resumo_energetico + "\n"
        texto_completo += relatorio.resumo_financeiro + "\n"
        texto_completo += relatorio.detalhamento_mensal + "\n"
        texto_completo += relatorio.detalhamento_unidades + "\n"
        texto_completo += relatorio.analise_payback + "\n"
        texto_completo += relatorio.conclusoes + "\n"

        return texto_completo


# --- Bloco de Teste ---
if __name__ == "__main__":
    print("--- Teste: negocio/gerador_relatorios.py ---")

    # Importa dados de exemplo para teste
    from configuracao.definicoes import CONFIG_EXEMPLO, UNIDADES_EXEMPLO, CONSUMOS_EXEMPLO

    # Cria sistema de teste
    sistema_teste = SistemaEnergia(
        configuracao=CONFIG_EXEMPLO,
        unidades=UNIDADES_EXEMPLO,
        consumos=CONSUMOS_EXEMPLO
    )

    gerador = GeradorRelatorios(sistema_teste)

    print("\n--- Teste 1: Geração de relatório completo ---")
    relatorio_completo = gerador.gerar_relatorio_completo(50000.0)

    print(f"Título: {relatorio_completo.titulo}")
    print(f"Data: {relatorio_completo.data_geracao}")
    print("✓ Relatório completo gerado com sucesso!")

    print("\n--- Teste 2: Visualização das primeiras seções ---")
    print("RESUMO DO SISTEMA:")
    print(relatorio_completo.resumo_sistema[:200] + "...")

    print("\nRESUMO ENERGÉTICO:")
    print(relatorio_completo.resumo_energetico[:200] + "...")

    print("\nRESUMO FINANCEIRO:")
    print(relatorio_completo.resumo_financeiro[:200] + "...")

    print("\n--- Teste 3: Geração de relatório em texto ---")
    relatorio_texto = gerador.gerar_relatorio_texto(50000.0)

    # Mostra apenas as primeiras linhas para não poluir o terminal
    linhas = relatorio_texto.split('\n')[:15]
    print("PRIMEIRAS LINHAS DO RELATÓRIO:")
    for linha in linhas:
        print(linha)
    print("...")

    print(f"\nRelatório completo gerado com {len(relatorio_texto)} caracteres.")
    print("✓ Todas as seções foram incluídas no relatório!")

    print("\nTeste de Gerador de Relatórios concluído com sucesso!")