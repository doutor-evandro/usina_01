"""
Funções auxiliares compatíveis com sistema legacy
Adaptação das funções originais para a nova estrutura
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import locale
from typing import Dict, List, Tuple, Any
from datetime import datetime

# Importações do sistema atual
from nucleo.modelos import SistemaEnergia, TipoLigacao
from dados.gerenciador_dados_legacy import GerenciadorDadosLegacy


# ========== CONFIGURAÇÃO DE LOCALIZAÇÃO ==========

def configurar_locale_brasileiro():
    """Configura o locale para formato brasileiro"""
    try:
        locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')
        except locale.Error:
            try:
                locale.setlocale(locale.LC_ALL, 'pt_BR')
            except locale.Error:
                print("⚠️ Locale brasileiro não disponível, usando formatação manual")


def formatar_numero_brasileiro(numero):
    """Formata número no padrão brasileiro (1.234.567,89)"""
    try:
        return locale.format_string("%.2f", numero, grouping=True).replace('.', 'TEMP').replace(',', '.').replace(
            'TEMP', ',')
    except:
        if isinstance(numero, (int, float)):
            numero_str = f"{numero:.2f}"
            if '.' in numero_str:
                parte_inteira, parte_decimal = numero_str.split('.')
            else:
                parte_inteira, parte_decimal = numero_str, "00"

            parte_inteira_formatada = ""
            for i, digito in enumerate(reversed(parte_inteira)):
                if i > 0 and i % 3 == 0:
                    parte_inteira_formatada = "." + parte_inteira_formatada
                parte_inteira_formatada = digito + parte_inteira_formatada

            return f"{parte_inteira_formatada},{parte_decimal}"
        else:
            return str(numero)


def formatar_numero_inteiro_brasileiro(numero):
    """Formata número inteiro no padrão brasileiro (1.234.567)"""
    try:
        return locale.format_string("%.0f", numero, grouping=True).replace(',', '.')
    except:
        numero_str = f"{int(numero)}"
        numero_formatado = ""
        for i, digito in enumerate(reversed(numero_str)):
            if i > 0 and i % 3 == 0:
                numero_formatado = "." + numero_formatado
            numero_formatado = digito + numero_formatado
        return numero_formatado


def formatar_porcentagem_brasileira(valor):
    """Formata porcentagem no padrão brasileiro (15,86%)"""
    return f"{valor:.2f}%".replace('.', ',')


# Configurar locale na inicialização
configurar_locale_brasileiro()


# ========== CLASSE PRINCIPAL DE FUNÇÕES LEGACY ==========

class FuncoesLegacy:
    """Classe que encapsula todas as funções legacy adaptadas"""

    def __init__(self, sistema: SistemaEnergia = None):
        self.sistema = sistema
        self.gerenciador = GerenciadorDadosLegacy()

        # Meses completos
        self.meses_completos = [
            "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
        ]

        # Tarifas mínimas
        self.tarifas_minimas = {
            "mono": 30,
            "bi": 50,
            "tri": 100
        }

    def converter_sistema_para_dados_legacy(self) -> Dict:
        """Converte sistema atual para formato legacy"""
        if not self.sistema:
            return {}

        return self.gerenciador.converter_de_sistema_energia(self.sistema)

    def obter_dados_legacy(self) -> Dict:
        """Obtém dados no formato legacy"""
        if self.sistema:
            return self.converter_sistema_para_dados_legacy()
        else:
            return self.gerenciador.carregar_dados()

    # ========== FUNÇÕES DE VALIDAÇÃO ==========

    def validar_consumo(self, consumo_str: str) -> Tuple[bool, Any]:
        """Valida entrada de consumo"""
        try:
            consumo = float(consumo_str)
            if consumo < 0:
                return False, "Consumo não pode ser negativo"
            return True, consumo
        except ValueError:
            return False, "Digite um valor numérico válido"

    def validar_dados_unidade(self, codigo: str, nome: str, tipo: str) -> Tuple[bool, str]:
        """Valida dados de uma unidade"""
        if not codigo.strip():
            return False, "Código é obrigatório"

        if not nome.strip():
            return False, "Nome é obrigatório"

        if tipo not in self.tarifas_minimas:
            return False, "Tipo de ligação inválido"

        return True, "Dados válidos"

    def validar_eficiencia(self, eficiencia_str: str) -> Tuple[bool, Any]:
        """Valida entrada de eficiência"""
        try:
            eficiencia = float(eficiencia_str)
            if eficiencia < 1 or eficiencia > 100:
                return False, "Eficiência deve estar entre 1% e 100%"
            return True, eficiencia
        except ValueError:
            return False, "Digite um valor numérico válido"

    # ========== FUNÇÕES DE CÁLCULO ==========

    def obter_eficiencia_usina_porcentagem(self, dados_sistema: Dict = None) -> float:
        """Obtém a eficiência da usina em porcentagem (1-100)"""
        if dados_sistema is None:
            dados_sistema = self.obter_dados_legacy()

        eficiencia = dados_sistema.get("sistema", {}).get("eficiencia_usina", 100)

        # Se estiver em decimal (0.78), converter para porcentagem
        if eficiencia <= 1:
            eficiencia = eficiencia * 100

        return eficiencia

    def obter_geracao_mensal(self, dados_sistema: Dict, mes: str) -> float:
        """Obtém a geração de um mês específico"""
        sistema = dados_sistema.get("sistema", {})

        if mes == "Resultado Anual":
            return self.calcular_geracao_anual_total(dados_sistema)

        # Verificar se existe estrutura nova (mensal)
        if "geracao_mensal" in sistema and isinstance(sistema["geracao_mensal"], dict):
            return float(sistema["geracao_mensal"].get(mes, 0))
        else:
            return float(sistema.get("geracao_mensal", 0))

    def calcular_geracao_anual_total(self, dados_sistema: Dict) -> float:
        """Calcula a geração total anual"""
        sistema = dados_sistema.get("sistema", {})

        if "geracao_mensal" in sistema and isinstance(sistema["geracao_mensal"], dict):
            total = 0
            for valor in sistema["geracao_mensal"].values():
                total += float(valor)
            return total
        else:
            return float(sistema.get("geracao_mensal", 0)) * 12

    def calcular_geracao_real_mensal_variavel(self, dados_sistema: Dict, mes: str) -> float:
        """Calcula a geração real considerando eficiência e mês específico"""
        geracao_nominal = self.obter_geracao_mensal(dados_sistema, mes)
        eficiencia_pct = self.obter_eficiencia_usina_porcentagem(dados_sistema)
        return float(geracao_nominal) * (float(eficiencia_pct) / 100)

    def calcular_consumo_anual_unidade(self, dados_sistema: Dict, codigo_unidade: str) -> float:
        """Calcula o consumo anual de uma unidade específica"""
        if codigo_unidade not in dados_sistema.get('consumos', {}):
            return 0

        consumos = dados_sistema['consumos'][codigo_unidade]
        consumos_validos = {k: v for k, v in consumos.items() if k in self.meses_completos}
        return sum(consumos_validos.values())

    def calcular_consumo_total_anual(self, dados_sistema: Dict) -> float:
        """Calcula o consumo total anual de todas as unidades"""
        total = 0
        for codigo in dados_sistema.get('consumos', {}):
            total += self.calcular_consumo_anual_unidade(dados_sistema, codigo)
        return total

    def calcular_tarifas_minimas_anuais(self, dados_sistema: Dict) -> float:
        """Calcula o total de tarifas mínimas anuais"""
        total_mensal = 0

        for unidade in dados_sistema.get('unidades', []):
            tipo = unidade['tipo']
            tarifa_minima = self.tarifas_minimas.get(tipo, 100)
            total_mensal += tarifa_minima

        return total_mensal * 12

    def calcular_saldo_mensal_com_eficiencia(self, dados_sistema: Dict, mes: str) -> Dict:
        """Calcula saldo mensal considerando eficiência da usina"""
        if mes == "Resultado Anual":
            return self.calcular_saldo_anual_com_eficiencia(dados_sistema)

        geracao_nominal = self.obter_geracao_mensal(dados_sistema, mes)
        geracao_real = self.calcular_geracao_real_mensal_variavel(dados_sistema, mes)
        eficiencia = self.obter_eficiencia_usina_porcentagem(dados_sistema)

        # Calcular consumo total do mês
        consumo_total = 0
        for unidade in dados_sistema.get("unidades", []):
            codigo = unidade["codigo"]
            if codigo in dados_sistema.get("consumos", {}):
                consumo_total += float(dados_sistema["consumos"][codigo].get(mes, 0))

        # Calcular tarifas mínimas
        tarifas_total = 0
        for unidade in dados_sistema.get("unidades", []):
            tipo = unidade["tipo"]
            tarifas_total += self.tarifas_minimas.get(tipo, 100)

        # Calcular saldo
        saldo = float(geracao_real) - float(consumo_total) - float(tarifas_total)

        return {
            "mes": mes,
            "geracao_nominal": float(geracao_nominal),
            "geracao_real": float(geracao_real),
            "consumo_total": float(consumo_total),
            "tarifas_total": float(tarifas_total),
            "saldo": float(saldo),
            "eficiencia": float(eficiencia),
            "status": "SOBRA" if saldo > 0 else "DÉFICIT" if saldo < 0 else "EQUILIBRADO"
        }

    def calcular_saldo_anual_com_eficiencia(self, dados_sistema: Dict) -> Dict:
        """Calcula saldo anual considerando eficiência da usina"""
        geracao_nominal_anual = self.calcular_geracao_anual_total(dados_sistema)
        eficiencia = self.obter_eficiencia_usina_porcentagem(dados_sistema)
        geracao_real_anual = float(geracao_nominal_anual) * (float(eficiencia) / 100)

        consumo_anual = self.calcular_consumo_total_anual(dados_sistema)
        tarifas_anuais = self.calcular_tarifas_minimas_anuais(dados_sistema)

        saldo_anual = float(geracao_real_anual) - float(consumo_anual) - float(tarifas_anuais)

        return {
            "mes": "Resultado Anual",
            "geracao_nominal": float(geracao_nominal_anual),
            "geracao_real": float(geracao_real_anual),
            "consumo_total": float(consumo_anual),
            "tarifas_total": float(tarifas_anuais),
            "saldo": float(saldo_anual),
            "eficiencia": float(eficiencia),
            "status": "SOBRA" if saldo_anual > 0 else "DÉFICIT" if saldo_anual < 0 else "EQUILIBRADO"
        }

    def calcular_porcentagens_em_relacao_usina(self, dados_sistema: Dict, mes: str) -> Dict:
        """Calcula percentuais de cada unidade EM RELAÇÃO À USINA"""
        if mes == "Resultado Anual":
            return self.calcular_porcentagens_anuais_em_relacao_usina(dados_sistema)

        geracao_real = self.calcular_geracao_real_mensal_variavel(dados_sistema, mes)

        if geracao_real == 0:
            return {}

        porcentagens = {}
        total_consumo = 0

        # Calcular porcentagem de cada unidade em relação à usina
        for unidade in dados_sistema.get("unidades", []):
            codigo = unidade["codigo"]
            nome = unidade["nome"]

            if codigo in dados_sistema.get("consumos", {}):
                consumo = dados_sistema["consumos"][codigo].get(mes, 0)
                if consumo > 0:
                    porcentagem = (float(consumo) / float(geracao_real)) * 100
                    porcentagens[nome] = porcentagem
                    total_consumo += float(consumo)

        # Calcular tarifas mínimas
        tarifas_total = 0
        for unidade in dados_sistema.get("unidades", []):
            tipo = unidade["tipo"]
            tarifas_total += self.tarifas_minimas.get(tipo, 100)

        # Porcentagem das tarifas mínimas
        if tarifas_total > 0:
            porcentagem_tarifas = (float(tarifas_total) / float(geracao_real)) * 100
            porcentagens["Tarifas Mínimas"] = porcentagem_tarifas

        # Calcular sobra/déficit
        total_usado = total_consumo + tarifas_total
        sobra_deficit = float(geracao_real) - float(total_usado)
        porcentagem_sobra = (float(sobra_deficit) / float(geracao_real)) * 100

        if sobra_deficit > 0:
            porcentagens["SOBRA DA USINA"] = porcentagem_sobra
        else:
            porcentagens["DÉFICIT DA USINA"] = abs(porcentagem_sobra)

        return porcentagens

    def calcular_porcentagens_anuais_em_relacao_usina(self, dados_sistema: Dict) -> Dict:
        """Calcula percentuais anuais de cada unidade EM RELAÇÃO À USINA"""
        geracao_real_anual = self.calcular_geracao_anual_total(dados_sistema)
        eficiencia_pct = self.obter_eficiencia_usina_porcentagem(dados_sistema)
        geracao_real_anual_com_eficiencia = float(geracao_real_anual) * (float(eficiencia_pct) / 100)

        if geracao_real_anual_com_eficiencia == 0:
            return {}

        porcentagens = {}
        total_consumo_anual = 0

        # Calcular porcentagem de cada unidade em relação à usina
        for unidade in dados_sistema.get("unidades", []):
            codigo = unidade["codigo"]
            nome = unidade["nome"]

            consumo_anual = self.calcular_consumo_anual_unidade(dados_sistema, codigo)
            if consumo_anual > 0:
                porcentagem = (float(consumo_anual) / float(geracao_real_anual_com_eficiencia)) * 100
                porcentagens[nome] = porcentagem
                total_consumo_anual += float(consumo_anual)

        # Calcular tarifas mínimas anuais
        tarifas_anuais = self.calcular_tarifas_minimas_anuais(dados_sistema)

        # Porcentagem das tarifas mínimas
        if tarifas_anuais > 0:
            porcentagem_tarifas = (float(tarifas_anuais) / float(geracao_real_anual_com_eficiencia)) * 100
            porcentagens["Tarifas Mínimas"] = porcentagem_tarifas

        # Calcular sobra/déficit anual
        total_usado_anual = total_consumo_anual + tarifas_anuais
        sobra_deficit_anual = float(geracao_real_anual_com_eficiencia) - float(total_usado_anual)
        porcentagem_sobra_anual = (float(sobra_deficit_anual) / float(geracao_real_anual_com_eficiencia)) * 100

        if sobra_deficit_anual > 0:
            porcentagens["SOBRA DA USINA"] = porcentagem_sobra_anual
        else:
            porcentagens["DÉFICIT DA USINA"] = abs(porcentagem_sobra_anual)

        return porcentagens

    # ========== FUNÇÕES DE RELATÓRIOS ==========

    def gerar_texto_resumo_com_eficiencia(self, saldo_info: Dict, dados_sistema: Dict) -> str:
        """Gera texto do resumo considerando eficiência - FORMATO BRASILEIRO"""
        if saldo_info["mes"] == "Resultado Anual":
            periodo = "ANUAL"
            multiplicador = ""
        else:
            periodo = saldo_info["mes"].upper()
            multiplicador = " (x12 meses)"

        # Calcular porcentagens em relação à usina
        porcentagem_consumo = (saldo_info['consumo_total'] / saldo_info['geracao_real']) * 100 if saldo_info[
                                                                                                      'geracao_real'] > 0 else 0
        porcentagem_tarifas = (saldo_info['tarifas_total'] / saldo_info['geracao_real']) * 100 if saldo_info[
                                                                                                      'geracao_real'] > 0 else 0
        porcentagem_saldo = (saldo_info['saldo'] / saldo_info['geracao_real']) * 100 if saldo_info[
                                                                                            'geracao_real'] > 0 else 0

        # Formatação brasileira dos números
        geracao_nominal_fmt = formatar_numero_inteiro_brasileiro(saldo_info['geracao_nominal'])
        geracao_real_fmt = formatar_numero_inteiro_brasileiro(saldo_info['geracao_real'])
        consumo_total_fmt = formatar_numero_inteiro_brasileiro(saldo_info['consumo_total'])
        tarifas_total_fmt = formatar_numero_inteiro_brasileiro(saldo_info['tarifas_total'])
        total_usado_fmt = formatar_numero_inteiro_brasileiro(saldo_info['consumo_total'] + saldo_info['tarifas_total'])
        saldo_fmt = formatar_numero_inteiro_brasileiro(abs(saldo_info['saldo']))

        texto = f"""=== RESUMO {periodo} ===

🔋 GERAÇÃO:
• Nominal: {geracao_nominal_fmt} kWh{multiplicador}
• Real ({saldo_info['eficiencia']:.0f}%): {geracao_real_fmt} kWh{multiplicador}

📊 DISTRIBUIÇÃO EM RELAÇÃO À USINA:
• Consumo das Unidades: {consumo_total_fmt} kWh ({porcentagem_consumo:.1f}% da usina)
• Tarifas Mínimas: {tarifas_total_fmt} kWh ({porcentagem_tarifas:.1f}% da usina)
• Total Usado: {total_usado_fmt} kWh ({porcentagem_consumo + porcentagem_tarifas:.1f}% da usina)

⚖️ SALDO DA USINA: {saldo_fmt} kWh ({porcentagem_saldo:+.1f}% da usina)

🏠 UNIDADES ({len(dados_sistema.get('unidades', []))}):
"""

        if saldo_info["mes"] != "Resultado Anual":
            # Mostrar detalhes por unidade para mês específico
            for unidade in dados_sistema.get("unidades", []):
                codigo = unidade["codigo"]
                nome = unidade["nome"]
                tipo = unidade["tipo"]
                tarifa = self.tarifas_minimas.get(tipo, 100)

                if codigo in dados_sistema.get("consumos", {}):
                    consumo = dados_sistema["consumos"][codigo].get(saldo_info["mes"], 0)
                else:
                    consumo = 0

                # Porcentagem em relação à usina
                porcentagem_unidade = (consumo / saldo_info['geracao_real']) * 100 if saldo_info[
                                                                                          'geracao_real'] > 0 else 0
                consumo_fmt = formatar_numero_inteiro_brasileiro(consumo)

                texto += f"\n• {codigo} - {nome}"
                texto += f"\n  Tipo: {tipo}"
                texto += f"\n  Consumo: {consumo_fmt} kWh ({porcentagem_unidade:.1f}% da usina)"
                texto += f"\n  Tarifa Mín.: {tarifa} kWh"
        else:
            # Mostrar resumo anual por unidade
            relatorio = self.calcular_relatorio_completo(dados_sistema)
            for i, unidade in enumerate(relatorio['unidades'][:5], 1):
                consumo_anual = unidade['consumo_anual']
                porcentagem_usina = (consumo_anual / saldo_info['geracao_real']) * 100 if saldo_info[
                                                                                              'geracao_real'] > 0 else 0
                consumo_anual_fmt = formatar_numero_inteiro_brasileiro(consumo_anual)
                texto += f"\n{i}. {unidade['nome']}: {consumo_anual_fmt} kWh/ano ({porcentagem_usina:.1f}% da usina)"

        # Status final
        if saldo_info["saldo"] > 0:
            texto += f"\n\n✅ SOBRA de {saldo_fmt} kWh{multiplicador} ({abs(porcentagem_saldo):.1f}% da usina)"
        elif saldo_info["saldo"] < 0:
            texto += f"\n\n❌ DÉFICIT de {saldo_fmt} kWh{multiplicador} ({abs(porcentagem_saldo):.1f}% da usina)"
        else:
            texto += f"\n\n⚖️ EQUILIBRADO{multiplicador}"

        # Validação: soma deve dar aproximadamente 100%
        soma_total = porcentagem_consumo + porcentagem_tarifas + abs(porcentagem_saldo)
        texto += f"\n\n📊 TOTAL: {soma_total:.1f}% da usina"

        return texto

    def calcular_relatorio_completo(self, dados_sistema: Dict) -> Dict:
        """Gera relatório completo com todas as análises"""
        relatorio = {
            'unidades': [],
            'resumo_geral': {},
            'balanco_energetico': {}
        }

        # Dados por unidade
        for unidade in dados_sistema.get('unidades', []):
            codigo = unidade['codigo']
            consumo_anual = self.calcular_consumo_anual_unidade(dados_sistema, codigo)

            dados_unidade = {
                'codigo': codigo,
                'nome': unidade['nome'],
                'tipo': unidade['tipo'],
                'endereco': unidade.get('endereco', ''),
                'consumo_anual': consumo_anual,
                'media_mensal': round(consumo_anual / 12, 2),
                'percentual': self.calcular_percentual_unidade(dados_sistema, codigo)
            }

            relatorio['unidades'].append(dados_unidade)

        # Ordenar por consumo (maior para menor)
        relatorio['unidades'].sort(key=lambda x: x['consumo_anual'], reverse=True)

        # Resumo geral
        total_anual = self.calcular_consumo_total_anual(dados_sistema)
        relatorio['resumo_geral'] = {
            'total_anual': total_anual,
            'media_mensal_total': round(total_anual / 12, 2),
            'maior_consumidor': relatorio['unidades'][0] if relatorio['unidades'] else None,
            'menor_consumidor': relatorio['unidades'][-1] if relatorio['unidades'] else None,
            'total_unidades': len(dados_sistema.get('unidades', []))
        }

        # Balanço energético
        relatorio['balanco_energetico'] = self.calcular_balanco_energetico(dados_sistema)

        return relatorio

    def calcular_percentual_unidade(self, dados_sistema: Dict, codigo_unidade: str) -> float:
        """Calcula o percentual de consumo de uma unidade em relação ao total"""
        consumo_unidade = self.calcular_consumo_anual_unidade(dados_sistema, codigo_unidade)
        consumo_total = self.calcular_consumo_total_anual(dados_sistema)

        if consumo_total == 0:
            return 0

        return round((consumo_unidade / consumo_total) * 100, 1)

    def calcular_balanco_energetico(self, dados_sistema: Dict) -> Dict:
        """Calcula o balanço energético completo"""
        geracao_nominal_anual = self.calcular_geracao_anual_total(dados_sistema)
        eficiencia = self.obter_eficiencia_usina_porcentagem(dados_sistema)
        geracao_real_anual = float(geracao_nominal_anual) * (float(eficiencia) / 100)

        consumo_anual = self.calcular_consumo_total_anual(dados_sistema)
        tarifas_anuais = self.calcular_tarifas_minimas_anuais(dados_sistema)

        saldo_anual = geracao_real_anual - consumo_anual - tarifas_anuais
        saldo_mensal = saldo_anual / 12

        return {
            'geracao_anual_nominal': float(geracao_nominal_anual),
            'geracao_anual_real': float(geracao_real_anual),
            'geracao_mensal_nominal': float(geracao_nominal_anual / 12),
            'geracao_mensal_real': float(geracao_real_anual / 12),
            'eficiencia': float(eficiencia),
            'consumo_anual': float(consumo_anual),
            'consumo_mensal': round(consumo_anual / 12, 2),
            'tarifas_anuais': float(tarifas_anuais),
            'tarifas_mensais': float(tarifas_anuais / 12),
            'saldo_anual': float(saldo_anual),
            'saldo_mensal': round(saldo_mensal, 2),
            'percentual_sobra': round((saldo_anual / geracao_real_anual) * 100, 1) if geracao_real_anual > 0 else 0,
            'status': 'SOBRA' if saldo_anual > 0 else 'DÉFICIT'
        }


# ========== FUNÇÕES DE COMPATIBILIDADE ==========

# Instância global para compatibilidade
_funcoes_legacy = None


def obter_funcoes_legacy(sistema: SistemaEnergia = None) -> FuncoesLegacy:
    """Obtém instância das funções legacy"""
    global _funcoes_legacy
    if _funcoes_legacy is None or sistema is not None:
        _funcoes_legacy = FuncoesLegacy(sistema)
    return _funcoes_legacy


# Funções de compatibilidade direta
def formatar_numero_brasileiro_compat(numero):
    return formatar_numero_brasileiro(numero)


def formatar_numero_inteiro_brasileiro_compat(numero):
    return formatar_numero_inteiro_brasileiro(numero)


def calcular_saldo_mensal_com_eficiencia_compat(dados_sistema, mes):
    funcoes = obter_funcoes_legacy()
    return funcoes.calcular_saldo_mensal_com_eficiencia(dados_sistema, mes)


def gerar_texto_resumo_com_eficiencia_compat(saldo_info, dados_sistema):
    funcoes = obter_funcoes_legacy()
    return funcoes.gerar_texto_resumo_com_eficiencia(saldo_info, dados_sistema)


def calcular_porcentagens_em_relacao_usina_compat(dados_sistema, mes):
    funcoes = obter_funcoes_legacy()
    return funcoes.calcular_porcentagens_em_relacao_usina(dados_sistema, mes)