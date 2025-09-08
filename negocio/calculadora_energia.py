# usina_01/negocio/calculadora_energia.py

from typing import Dict, List, Tuple
from dataclasses import dataclass
from nucleo.modelos import SistemaEnergia, UnidadeConsumidora, ConfiguracaoSistema
from utilitarios.constantes import MESES_APENAS


@dataclass
class ResultadoEnergia:
    """Resultado dos cálculos de energia para um mês específico."""
    mes: str
    geracao_kwh: float
    consumo_total_kwh: float
    excesso_kwh: float
    deficit_kwh: float
    energia_injetada_kwh: float
    energia_consumida_rede_kwh: float
    saldo_energetico_kwh: float


@dataclass
class ResumoAnual:
    """Resumo anual dos cálculos de energia."""
    geracao_total_kwh: float
    consumo_total_kwh: float
    excesso_total_kwh: float
    deficit_total_kwh: float
    energia_injetada_total_kwh: float
    energia_consumida_rede_total_kwh: float
    saldo_energetico_total_kwh: float
    percentual_autossuficiencia: float


class CalculadoraEnergia:
    """
    Responsável por todos os cálculos relacionados à energia solar.
    """

    def __init__(self, sistema: SistemaEnergia):
        self.sistema = sistema

    def calcular_geracao_mensal(self, mes: str) -> float:
        """
        Calcula a geração de energia para um mês específico.

        Args:
            mes: Nome do mês (ex: "Janeiro")

        Returns:
            Geração em kWh para o mês
        """
        if mes not in self.sistema.configuracao.geracao_mensal:
            return 0.0

        geracao_bruta = self.sistema.configuracao.geracao_mensal[mes]
        eficiencia_decimal = self.sistema.configuracao.eficiencia / 100.0

        return geracao_bruta * eficiencia_decimal

    def calcular_consumo_total_mensal(self, mes: str) -> float:
        """
        Calcula o consumo total de todas as unidades para um mês específico.

        Args:
            mes: Nome do mês (ex: "Janeiro")

        Returns:
            Consumo total em kWh para o mês
        """
        consumo_total = 0.0

        for unidade in self.sistema.unidades:
            consumo_uc = self.sistema.consumos.get(unidade.codigo, {})
            consumo_mes = consumo_uc.get(mes, 0.0)
            consumo_total += consumo_mes

        return consumo_total

    def calcular_resultado_mensal(self, mes: str) -> ResultadoEnergia:
        """
        Calcula o resultado energético completo para um mês.

        Args:
            mes: Nome do mês (ex: "Janeiro")

        Returns:
            ResultadoEnergia com todos os cálculos do mês
        """
        geracao = self.calcular_geracao_mensal(mes)
        consumo_total = self.calcular_consumo_total_mensal(mes)

        # Calcula excesso e déficit
        if geracao >= consumo_total:
            excesso = geracao - consumo_total
            deficit = 0.0
        else:
            excesso = 0.0
            deficit = consumo_total - geracao

        # Energia injetada na rede (excesso que vai para a rede)
        energia_injetada = excesso

        # Energia consumida da rede (déficit que vem da rede)
        energia_consumida_rede = deficit

        # Saldo energético (positivo = excesso, negativo = déficit)
        saldo_energetico = geracao - consumo_total

        return ResultadoEnergia(
            mes=mes,
            geracao_kwh=geracao,
            consumo_total_kwh=consumo_total,
            excesso_kwh=excesso,
            deficit_kwh=deficit,
            energia_injetada_kwh=energia_injetada,
            energia_consumida_rede_kwh=energia_consumida_rede,
            saldo_energetico_kwh=saldo_energetico
        )

    def calcular_resultados_anuais(self) -> Tuple[List[ResultadoEnergia], ResumoAnual]:
        """
        Calcula os resultados energéticos para todos os meses do ano.

        Returns:
            Tupla contendo:
            - Lista de ResultadoEnergia para cada mês
            - ResumoAnual com totais e percentuais
        """
        resultados_mensais = []

        # Calcula resultado para cada mês
        for mes in MESES_APENAS:
            resultado_mes = self.calcular_resultado_mensal(mes)
            resultados_mensais.append(resultado_mes)

        # Calcula totais anuais
        geracao_total = sum(r.geracao_kwh for r in resultados_mensais)
        consumo_total = sum(r.consumo_total_kwh for r in resultados_mensais)
        excesso_total = sum(r.excesso_kwh for r in resultados_mensais)
        deficit_total = sum(r.deficit_kwh for r in resultados_mensais)
        energia_injetada_total = sum(r.energia_injetada_kwh for r in resultados_mensais)
        energia_consumida_rede_total = sum(r.energia_consumida_rede_kwh for r in resultados_mensais)
        saldo_energetico_total = sum(r.saldo_energetico_kwh for r in resultados_mensais)

        # Calcula percentual de autossuficiência
        if consumo_total > 0:
            energia_atendida_pelo_sistema = min(geracao_total, consumo_total)
            percentual_autossuficiencia = (energia_atendida_pelo_sistema / consumo_total) * 100
        else:
            percentual_autossuficiencia = 0.0

        resumo_anual = ResumoAnual(
            geracao_total_kwh=geracao_total,
            consumo_total_kwh=consumo_total,
            excesso_total_kwh=excesso_total,
            deficit_total_kwh=deficit_total,
            energia_injetada_total_kwh=energia_injetada_total,
            energia_consumida_rede_total_kwh=energia_consumida_rede_total,
            saldo_energetico_total_kwh=saldo_energetico_total,
            percentual_autossuficiencia=percentual_autossuficiencia
        )

        return resultados_mensais, resumo_anual

    def calcular_consumo_por_unidade(self, mes: str) -> Dict[str, float]:
        """
        Calcula o consumo individual de cada unidade para um mês.

        Args:
            mes: Nome do mês (ex: "Janeiro")

        Returns:
            Dicionário com código da UC como chave e consumo em kWh como valor
        """
        consumos_por_uc = {}

        for unidade in self.sistema.unidades:
            consumo_uc = self.sistema.consumos.get(unidade.codigo, {})
            consumo_mes = consumo_uc.get(mes, 0.0)
            consumos_por_uc[unidade.codigo] = consumo_mes

        return consumos_por_uc

    def obter_tarifa_minima_total(self) -> float:
        """
        Calcula a tarifa mínima total de todas as unidades.

        Returns:
            Soma das tarifas mínimas de todas as unidades em kWh
        """
        tarifa_total = 0.0

        for unidade in self.sistema.unidades:
            tarifa_total += unidade.tarifa_minima

        return tarifa_total


# --- Bloco de Teste ---
if __name__ == "__main__":
    print("--- Teste: negocio/calculadora_energia.py ---")

    # Importa dados de exemplo para teste
    from configuracao.definicoes import CONFIG_EXEMPLO, UNIDADES_EXEMPLO, CONSUMOS_EXEMPLO

    # Cria sistema de teste
    sistema_teste = SistemaEnergia(
        configuracao=CONFIG_EXEMPLO,
        unidades=UNIDADES_EXEMPLO,
        consumos=CONSUMOS_EXEMPLO
    )

    calculadora = CalculadoraEnergia(sistema_teste)

    print("\n--- Teste 1: Cálculo de geração mensal ---")
    geracao_jan = calculadora.calcular_geracao_mensal("Janeiro")
    print(f"Geração em Janeiro: {geracao_jan:.2f} kWh")
    print(f"Eficiência aplicada: {sistema_teste.configuracao.eficiencia}%")

    print("\n--- Teste 2: Cálculo de consumo total mensal ---")
    consumo_jan = calculadora.calcular_consumo_total_mensal("Janeiro")
    print(f"Consumo total em Janeiro: {consumo_jan:.2f} kWh")

    print("\n--- Teste 3: Resultado energético mensal ---")
    resultado_jan = calculadora.calcular_resultado_mensal("Janeiro")
    print(f"Mês: {resultado_jan.mes}")
    print(f"Geração: {resultado_jan.geracao_kwh:.2f} kWh")
    print(f"Consumo: {resultado_jan.consumo_total_kwh:.2f} kWh")
    print(f"Excesso: {resultado_jan.excesso_kwh:.2f} kWh")
    print(f"Déficit: {resultado_jan.deficit_kwh:.2f} kWh")
    print(f"Saldo energético: {resultado_jan.saldo_energetico_kwh:.2f} kWh")

    print("\n--- Teste 4: Consumo por unidade ---")
    consumos_jan = calculadora.calcular_consumo_por_unidade("Janeiro")
    for codigo, consumo in consumos_jan.items():
        nome_uc = next(u.nome for u in sistema_teste.unidades if u.codigo == codigo)
        print(f"{codigo} ({nome_uc}): {consumo:.2f} kWh")

    print("\n--- Teste 5: Tarifa mínima total ---")
    tarifa_total = calculadora.obter_tarifa_minima_total()
    print(f"Tarifa mínima total: {tarifa_total:.2f} kWh")

    print("\n--- Teste 6: Resultados anuais ---")
    resultados_mensais, resumo_anual = calculadora.calcular_resultados_anuais()

    print(f"Geração total anual: {resumo_anual.geracao_total_kwh:.2f} kWh")
    print(f"Consumo total anual: {resumo_anual.consumo_total_kwh:.2f} kWh")
    print(f"Excesso total anual: {resumo_anual.excesso_total_kwh:.2f} kWh")
    print(f"Déficit total anual: {resumo_anual.deficit_total_kwh:.2f} kWh")
    print(f"Percentual de autossuficiência: {resumo_anual.percentual_autossuficiencia:.1f}%")

    print(f"\nPrimeiros 3 meses detalhados:")
    for i, resultado in enumerate(resultados_mensais[:3]):
        print(f"{resultado.mes}: Geração={resultado.geracao_kwh:.1f} kWh, "
              f"Consumo={resultado.consumo_total_kwh:.1f} kWh, "
              f"Saldo={resultado.saldo_energetico_kwh:.1f} kWh")

    print("\nTeste de Calculadora de Energia concluído com sucesso!")