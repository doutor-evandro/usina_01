# usina_01/negocio/gerenciador_distribuicao.py

from typing import Dict, List, Tuple
from dataclasses import dataclass
from nucleo.modelos import SistemaEnergia, UnidadeConsumidora
from negocio.calculadora_energia import CalculadoraEnergia, ResultadoEnergia, ResumoAnual
from utilitarios.constantes import MESES_APENAS


@dataclass
class ResultadoFinanceiro:
    """Resultado dos cálculos financeiros para um mês específico."""
    mes: str
    economia_kwh: float
    economia_reais: float
    custo_sem_sistema_reais: float
    custo_com_sistema_reais: float
    energia_compensada_kwh: float
    tarifa_minima_paga_reais: float


@dataclass
class ResumoFinanceiroAnual:
    """Resumo anual dos cálculos financeiros."""
    economia_total_reais: float
    custo_total_sem_sistema_reais: float
    custo_total_com_sistema_reais: float
    energia_compensada_total_kwh: float
    tarifa_minima_total_anual_reais: float
    percentual_economia: float


@dataclass
class DistribuicaoUnidade:
    """Distribuição de energia e custos para uma unidade específica."""
    codigo: str
    nome: str
    consumo_kwh: float
    energia_atendida_sistema_kwh: float
    energia_da_rede_kwh: float
    percentual_atendimento: float
    economia_reais: float
    custo_sem_sistema_reais: float
    custo_com_sistema_reais: float


class GerenciadorDistribuicao:
    """
    Responsável por calcular a distribuição de energia e custos entre as unidades,
    bem como análises financeiras do sistema.
    """

    def __init__(self, sistema: SistemaEnergia):
        self.sistema = sistema
        self.calculadora_energia = CalculadoraEnergia(sistema)

    def calcular_resultado_financeiro_mensal(self, mes: str) -> ResultadoFinanceiro:
        """
        Calcula o resultado financeiro para um mês específico.

        Args:
            mes: Nome do mês (ex: "Janeiro")

        Returns:
            ResultadoFinanceiro com todos os cálculos financeiros do mês
        """
        resultado_energia = self.calculadora_energia.calcular_resultado_mensal(mes)
        valor_kwh = self.sistema.configuracao.valor_kwh
        tarifa_minima_total = self.calculadora_energia.obter_tarifa_minima_total()

        # Energia compensada é a energia gerada que efetivamente reduz o consumo da rede
        energia_compensada = min(resultado_energia.geracao_kwh, resultado_energia.consumo_total_kwh)

        # Economia em kWh é a energia que deixou de ser comprada da rede
        economia_kwh = energia_compensada

        # Custo sem sistema (todo o consumo viria da rede)
        custo_sem_sistema = max(resultado_energia.consumo_total_kwh, tarifa_minima_total) * valor_kwh

        # Custo com sistema
        # Paga pela energia que ainda precisa vir da rede + tarifa mínima
        energia_rede_necessaria = resultado_energia.energia_consumida_rede_kwh
        custo_energia_rede = energia_rede_necessaria * valor_kwh
        tarifa_minima_paga = tarifa_minima_total * valor_kwh

        # O custo total é o maior entre o custo da energia da rede e a tarifa mínima
        custo_com_sistema = max(custo_energia_rede, tarifa_minima_paga)

        # Economia em reais
        economia_reais = custo_sem_sistema - custo_com_sistema

        return ResultadoFinanceiro(
            mes=mes,
            economia_kwh=economia_kwh,
            economia_reais=economia_reais,
            custo_sem_sistema_reais=custo_sem_sistema,
            custo_com_sistema_reais=custo_com_sistema,
            energia_compensada_kwh=energia_compensada,
            tarifa_minima_paga_reais=tarifa_minima_paga
        )

    def calcular_resultados_financeiros_anuais(self) -> Tuple[List[ResultadoFinanceiro], ResumoFinanceiroAnual]:
        """
        Calcula os resultados financeiros para todos os meses do ano.

        Returns:
            Tupla contendo:
            - Lista de ResultadoFinanceiro para cada mês
            - ResumoFinanceiroAnual com totais e percentuais
        """
        resultados_mensais = []

        # Calcula resultado financeiro para cada mês
        for mes in MESES_APENAS:
            resultado_mes = self.calcular_resultado_financeiro_mensal(mes)
            resultados_mensais.append(resultado_mes)

        # Calcula totais anuais
        economia_total = sum(r.economia_reais for r in resultados_mensais)
        custo_total_sem_sistema = sum(r.custo_sem_sistema_reais for r in resultados_mensais)
        custo_total_com_sistema = sum(r.custo_com_sistema_reais for r in resultados_mensais)
        energia_compensada_total = sum(r.energia_compensada_kwh for r in resultados_mensais)
        tarifa_minima_total_anual = sum(r.tarifa_minima_paga_reais for r in resultados_mensais)

        # Calcula percentual de economia
        if custo_total_sem_sistema > 0:
            percentual_economia = (economia_total / custo_total_sem_sistema) * 100
        else:
            percentual_economia = 0.0

        resumo_anual = ResumoFinanceiroAnual(
            economia_total_reais=economia_total,
            custo_total_sem_sistema_reais=custo_total_sem_sistema,
            custo_total_com_sistema_reais=custo_total_com_sistema,
            energia_compensada_total_kwh=energia_compensada_total,
            tarifa_minima_total_anual_reais=tarifa_minima_total_anual,
            percentual_economia=percentual_economia
        )

        return resultados_mensais, resumo_anual

    def calcular_distribuicao_por_unidade(self, mes: str) -> List[DistribuicaoUnidade]:
        """
        Calcula como a energia gerada é distribuída entre as unidades em um mês.

        Args:
            mes: Nome do mês (ex: "Janeiro")

        Returns:
            Lista de DistribuicaoUnidade com os cálculos para cada unidade
        """
        resultado_energia = self.calculadora_energia.calcular_resultado_mensal(mes)
        consumos_por_uc = self.calculadora_energia.calcular_consumo_por_unidade(mes)
        valor_kwh = self.sistema.configuracao.valor_kwh

        distribuicoes = []
        energia_disponivel = resultado_energia.geracao_kwh

        # Ordena unidades por consumo (menor para maior) para distribuição proporcional
        unidades_ordenadas = sorted(self.sistema.unidades, key=lambda u: consumos_por_uc.get(u.codigo, 0))

        for unidade in unidades_ordenadas:
            consumo_uc = consumos_por_uc.get(unidade.codigo, 0.0)

            # Calcula quanto da energia do sistema pode atender esta unidade
            if energia_disponivel > 0 and consumo_uc > 0:
                # Distribui proporcionalmente baseado no consumo total
                proporcao_consumo = consumo_uc / resultado_energia.consumo_total_kwh if resultado_energia.consumo_total_kwh > 0 else 0
                energia_atendida = min(consumo_uc, resultado_energia.geracao_kwh * proporcao_consumo)
            else:
                energia_atendida = 0.0

            energia_da_rede = consumo_uc - energia_atendida

            # Calcula percentual de atendimento
            percentual_atendimento = (energia_atendida / consumo_uc * 100) if consumo_uc > 0 else 0.0

            # Calcula custos
            custo_sem_sistema = max(consumo_uc, unidade.tarifa_minima) * valor_kwh
            custo_energia_rede = energia_da_rede * valor_kwh
            tarifa_minima_uc = unidade.tarifa_minima * valor_kwh
            custo_com_sistema = max(custo_energia_rede, tarifa_minima_uc)

            economia = custo_sem_sistema - custo_com_sistema

            distribuicao = DistribuicaoUnidade(
                codigo=unidade.codigo,
                nome=unidade.nome,
                consumo_kwh=consumo_uc,
                energia_atendida_sistema_kwh=energia_atendida,
                energia_da_rede_kwh=energia_da_rede,
                percentual_atendimento=percentual_atendimento,
                economia_reais=economia,
                custo_sem_sistema_reais=custo_sem_sistema,
                custo_com_sistema_reais=custo_com_sistema
            )

            distribuicoes.append(distribuicao)

        return distribuicoes

    def calcular_payback_simples(self, investimento_inicial: float) -> Tuple[float, float]:
        """
        Calcula o payback simples do investimento.

        Args:
            investimento_inicial: Valor investido no sistema em reais

        Returns:
            Tupla contendo:
            - Payback em anos
            - Economia mensal média em reais
        """
        _, resumo_anual = self.calcular_resultados_financeiros_anuais()
        economia_anual = resumo_anual.economia_total_reais

        if economia_anual <= 0:
            return float('inf'), 0.0  # Nunca se paga se não há economia

        payback_anos = investimento_inicial / economia_anual
        economia_mensal_media = economia_anual / 12

        return payback_anos, economia_mensal_media


# --- Bloco de Teste ---
if __name__ == "__main__":
    print("--- Teste: negocio/gerenciador_distribuicao.py ---")

    # Importa dados de exemplo para teste
    from configuracao.definicoes import CONFIG_EXEMPLO, UNIDADES_EXEMPLO, CONSUMOS_EXEMPLO

    # Cria sistema de teste
    sistema_teste = SistemaEnergia(
        configuracao=CONFIG_EXEMPLO,
        unidades=UNIDADES_EXEMPLO,
        consumos=CONSUMOS_EXEMPLO
    )

    gerenciador = GerenciadorDistribuicao(sistema_teste)

    print("\n--- Teste 1: Resultado financeiro mensal ---")
    resultado_fin_jan = gerenciador.calcular_resultado_financeiro_mensal("Janeiro")
    print(f"Mês: {resultado_fin_jan.mes}")
    print(f"Economia: {resultado_fin_jan.economia_kwh:.2f} kWh = R\$ {resultado_fin_jan.economia_reais:.2f}")
    print(f"Custo sem sistema: R\$ {resultado_fin_jan.custo_sem_sistema_reais:.2f}")
    print(f"Custo com sistema: R\$ {resultado_fin_jan.custo_com_sistema_reais:.2f}")
    print(f"Energia compensada: {resultado_fin_jan.energia_compensada_kwh:.2f} kWh")

    print("\n--- Teste 2: Distribuição por unidade ---")
    distribuicoes_jan = gerenciador.calcular_distribuicao_por_unidade("Janeiro")
    for dist in distribuicoes_jan:
        print(f"{dist.codigo} ({dist.nome}):")
        print(f"  Consumo: {dist.consumo_kwh:.2f} kWh")
        print(
            f"  Atendido pelo sistema: {dist.energia_atendida_sistema_kwh:.2f} kWh ({dist.percentual_atendimento:.1f}%)")
        print(f"  Da rede: {dist.energia_da_rede_kwh:.2f} kWh")
        print(f"  Economia: R\$ {dist.economia_reais:.2f}")

    print("\n--- Teste 3: Resultados financeiros anuais ---")
    resultados_fin_anuais, resumo_fin_anual = gerenciador.calcular_resultados_financeiros_anuais()

    print(f"Economia total anual: R\$ {resumo_fin_anual.economia_total_reais:.2f}")
    print(f"Custo total sem sistema: R\$ {resumo_fin_anual.custo_total_sem_sistema_reais:.2f}")
    print(f"Custo total com sistema: R\$ {resumo_fin_anual.custo_total_com_sistema_reais:.2f}")
    print(f"Percentual de economia: {resumo_fin_anual.percentual_economia:.1f}%")
    print(f"Energia compensada total: {resumo_fin_anual.energia_compensada_total_kwh:.2f} kWh")

    print("\n--- Teste 4: Cálculo de payback ---")
    investimento_exemplo = 50000.0  # R\$ 50.000
    payback_anos, economia_mensal = gerenciador.calcular_payback_simples(investimento_exemplo)

    print(f"Investimento inicial: R\$ {investimento_exemplo:.2f}")
    print(f"Economia mensal média: R\$ {economia_mensal:.2f}")
    print(f"Payback simples: {payback_anos:.1f} anos")

    print(f"\nPrimeiros 3 meses financeiros:")
    for i, resultado in enumerate(resultados_fin_anuais[:3]):
        print(f"{resultado.mes}: Economia=R\$ {resultado.economia_reais:.2f}, "
              f"Custo com sistema=R\$ {resultado.custo_com_sistema_reais:.2f}")

    print("\nTeste de Gerenciador de Distribuição concluído com sucesso!")