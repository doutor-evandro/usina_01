"""
Calculadora de Créditos de Energia - Versão 2.0
Implementa a lógica específica de distribuição de créditos
"""

from typing import Dict, List, Tuple
from nucleo.modelos import SistemaEnergia, TipoLigacao
from utilitarios.formatadores import formatar_moeda, formatar_energia


class CalculadoraCreditos:
    """Calculadora específica para distribuição de créditos entre unidades"""

    def __init__(self, sistema: SistemaEnergia):
        self.sistema = sistema

        # Mapeamento de tarifas mínimas
        self.tarifas_minimas = {
            TipoLigacao.MONOFASICA: 30,
            TipoLigacao.BIFASICA: 50,
            TipoLigacao.TRIFASICA: 100
        }

    def obter_geracao_mensal(self, mes: int) -> float:
        """Obtém geração mensal considerando eficiência"""
        try:
            # Se tem geração mensal personalizada, usar ela
            if hasattr(self.sistema.configuracao,
                       'geracao_mensal_kwh') and self.sistema.configuracao.geracao_mensal_kwh:
                if 1 <= mes <= 12:
                    geracao_nominal = self.sistema.configuracao.geracao_mensal_kwh[mes - 1]
                    return geracao_nominal * self.sistema.configuracao.eficiencia_sistema

            # Senão, calcular baseado na potência
            geracao_base = self.sistema.configuracao.potencia_instalada_kw * 30 * 4.5  # 4.5h média
            return geracao_base * self.sistema.configuracao.eficiencia_sistema

        except (IndexError, AttributeError):
            return 0.0

    def calcular_tarifas_minimas_total(self) -> float:
        """Calcula total de tarifas mínimas de todas as unidades ativas"""
        total = 0
        for unidade in self.sistema.get_unidades_ativas():
            total += self.tarifas_minimas.get(unidade.tipo_ligacao, 100)
        return total

    def calcular_creditos_mes(self, mes: int) -> Dict:
        """Calcula os créditos disponíveis para um mês específico"""
        # Geração real do mês
        geracao_real = self.obter_geracao_mensal(mes)

        # Consumo total do mês
        consumo_total = 0
        for unidade in self.sistema.get_unidades_ativas():
            if 1 <= mes <= 12:
                consumo_total += unidade.consumo_mensal_kwh[mes - 1]

        # Tarifas mínimas
        tarifas_minimas = self.calcular_tarifas_minimas_total()

        # Créditos disponíveis (geração - tarifas mínimas)
        creditos_disponiveis = max(0, geracao_real - tarifas_minimas)

        # Créditos utilizados (menor entre consumo e disponível)
        creditos_utilizados = min(consumo_total, creditos_disponiveis)

        # Créditos restantes
        creditos_restantes = creditos_disponiveis - creditos_utilizados

        return {
            'mes': mes,
            'geracao_real': geracao_real,
            'consumo_total': consumo_total,
            'tarifas_minimas': tarifas_minimas,
            'creditos_disponiveis': creditos_disponiveis,
            'creditos_utilizados': creditos_utilizados,
            'creditos_restantes': creditos_restantes,
            'eficiencia': self.sistema.configuracao.eficiencia_sistema * 100,
            'status': 'SOBRA' if creditos_restantes > 0 else 'EQUILIBRIO' if creditos_restantes == 0 else 'DEFICIT'
        }

    def distribuir_creditos_mes(self, mes: int, metodo: str = 'proporcional') -> Dict:
        """Distribui créditos entre as unidades para um mês"""
        resultado_mes = self.calcular_creditos_mes(mes)
        creditos_disponiveis = resultado_mes['creditos_disponiveis']

        distribuicao = {}

        if metodo == 'proporcional':
            # Calcular consumo total líquido (sem tarifas mínimas)
            consumo_total_liquido = 0
            consumos_unidades = {}

            for unidade in self.sistema.get_unidades_ativas():
                if 1 <= mes <= 12:
                    consumo_bruto = unidade.consumo_mensal_kwh[mes - 1]
                    tarifa_minima = self.tarifas_minimas.get(unidade.tipo_ligacao, 100)
                    consumo_liquido = max(0, consumo_bruto - tarifa_minima)

                    consumos_unidades[unidade.id] = {
                        'unidade': unidade,
                        'consumo_bruto': consumo_bruto,
                        'tarifa_minima': tarifa_minima,
                        'consumo_liquido': consumo_liquido
                    }
                    consumo_total_liquido += consumo_liquido

            # Distribuir proporcionalmente
            for unidade_id, dados_consumo in consumos_unidades.items():
                if consumo_total_liquido > 0:
                    proporcao = dados_consumo['consumo_liquido'] / consumo_total_liquido
                    creditos_recebidos = creditos_disponiveis * proporcao
                else:
                    creditos_recebidos = 0

                # Valor que sobra para pagar (consumo - créditos recebidos)
                valor_a_pagar = max(0, dados_consumo['consumo_liquido'] - creditos_recebidos)

                # Valor final (tarifa mínima + valor a pagar)
                valor_final = dados_consumo['tarifa_minima'] + valor_a_pagar

                distribuicao[unidade_id] = {
                    'nome': dados_consumo['unidade'].nome,
                    'tipo_ligacao': dados_consumo['unidade'].tipo_ligacao.value,
                    'consumo_bruto': dados_consumo['consumo_bruto'],
                    'tarifa_minima': dados_consumo['tarifa_minima'],
                    'consumo_liquido': dados_consumo['consumo_liquido'],
                    'creditos_recebidos': round(creditos_recebidos, 2),
                    'valor_a_pagar': round(valor_a_pagar, 2),
                    'valor_final': round(valor_final, 2),
                    'proporcao': round(proporcao * 100, 1) if consumo_total_liquido > 0 else 0
                }

        return {
            'mes': mes,
            'resumo': resultado_mes,
            'distribuicao': distribuicao,
            'metodo': metodo
        }

    def calcular_balanco_anual(self) -> Dict:
        """Calcula balanço energético anual"""
        # Geração anual
        geracao_anual = sum(self.obter_geracao_mensal(mes) for mes in range(1, 13))

        # Consumo anual
        consumo_anual = 0
        for unidade in self.sistema.get_unidades_ativas():
            consumo_anual += sum(unidade.consumo_mensal_kwh)

        # Tarifas anuais
        tarifas_anuais = self.calcular_tarifas_minimas_total() * 12

        # Saldo anual
        saldo_anual = geracao_anual - consumo_anual - tarifas_anuais

        return {
            'geracao_anual': geracao_anual,
            'consumo_anual': consumo_anual,
            'tarifas_anuais': tarifas_anuais,
            'saldo_anual': saldo_anual,
            'percentual_sobra': round((saldo_anual / geracao_anual) * 100, 1) if geracao_anual > 0 else 0,
            'status': 'SOBRA' if saldo_anual > 0 else 'DEFICIT'
        }

    def obter_relatorio_creditos_completo(self, ano: int = 2025) -> Dict:
        """Gera relatório completo de créditos para o ano"""
        relatorio = {
            'ano': ano,
            'resumo_anual': self.calcular_balanco_anual(),
            'detalhes_mensais': [],
            'distribuicao_anual': {},
            'unidades': []
        }

        # Calcular para cada mês
        for mes in range(1, 13):
            resultado_mensal = self.distribuir_creditos_mes(mes)
            relatorio['detalhes_mensais'].append(resultado_mensal)

        # Resumo por unidade
        for unidade in self.sistema.get_unidades_ativas():
            consumo_anual = sum(unidade.consumo_mensal_kwh)
            creditos_anuais = 0
            valor_final_anual = 0

            # Somar créditos de todos os meses
            for detalhe_mensal in relatorio['detalhes_mensais']:
                if unidade.id in detalhe_mensal['distribuicao']:
                    dist = detalhe_mensal['distribuicao'][unidade.id]
                    creditos_anuais += dist['creditos_recebidos']
                    valor_final_anual += dist['valor_final']

            relatorio['unidades'].append({
                'id': unidade.id,
                'nome': unidade.nome,
                'tipo_ligacao': unidade.tipo_ligacao.value,
                'consumo_anual': consumo_anual,
                'creditos_anuais': round(creditos_anuais, 2),
                'valor_final_anual': round(valor_final_anual, 2),
                'percentual_consumo': round((consumo_anual / relatorio['resumo_anual']['consumo_anual']) * 100, 1)
            })

        return relatorio

    def gerar_relatorio_texto_creditos(self, ano: int = 2025) -> str:
        """Gera relatório em texto dos créditos"""
        relatorio = self.obter_relatorio_creditos_completo(ano)

        texto = []
        texto.append("=" * 80)
        texto.append(f"RELATÓRIO DE DISTRIBUIÇÃO DE CRÉDITOS - {ano}")
        texto.append("=" * 80)
        texto.append("")

        # Resumo anual
        resumo = relatorio['resumo_anual']
        texto.append("RESUMO ANUAL:")
        texto.append(f"  Geração Total: {formatar_energia(resumo['geracao_anual'])}")
        texto.append(f"  Consumo Total: {formatar_energia(resumo['consumo_anual'])}")
        texto.append(f"  Tarifas Mínimas: {formatar_energia(resumo['tarifas_anuais'])}")
        texto.append(f"  Saldo: {formatar_energia(resumo['saldo_anual'])} ({resumo['status']})")
        texto.append("")

        # Detalhes por unidade
        texto.append("DISTRIBUIÇÃO POR UNIDADE:")
        texto.append("-" * 80)
        for unidade in relatorio['unidades']:
            texto.append(f"📍 {unidade['nome']} ({unidade['tipo_ligacao']})")
            texto.append(f"   Consumo Anual: {formatar_energia(unidade['consumo_anual'])}")
            texto.append(f"   Créditos Recebidos: {formatar_energia(unidade['creditos_anuais'])}")
            texto.append(f"   Valor Final: {formatar_moeda(unidade['valor_final_anual'])}")
            texto.append(f"   Participação: {unidade['percentual_consumo']}%")
            texto.append("")

        return "\n".join(texto)