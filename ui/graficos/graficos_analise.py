"""
Gerador de gráficos de análise - Versão adaptada com gráficos do sistema legacy
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
import seaborn as sns
from pathlib import Path
import os

from nucleo.modelos import (
    SistemaEnergia, ResultadoMensalEnergia, ResultadoAnualEnergia,
    ResultadoMensalFinanceiro, ResultadoAnualFinanceiro
)
from nucleo.excecoes import ErroGrafico
from negocio.calculadora_energia import CalculadoraEnergia
from negocio.gerenciador_distribuicao import GerenciadorDistribuicao

# Configurar estilo dos gráficos
plt.style.use('default')
sns.set_palette("husl")


class GeradorGraficosAnalise:
    """Gerador de gráficos de análise do sistema"""

    def __init__(self, sistema: SistemaEnergia):
        self.sistema = sistema
        self.calculadora = CalculadoraEnergia(sistema)
        self.gerenciador = GerenciadorDistribuicao(sistema)

        # Configurações visuais
        self.cores = {
            'geracao': '#2E86AB',
            'consumo': '#A23B72',
            'economia': '#F18F01',
            'custo': '#C73E1D',
            'creditos': '#4CAF50',
            'saldo': '#FF9800',
            'eficiencia': '#9C27B0',
            'perdas': '#F44336'
        }

        self.figsize_padrao = (12, 8)
        self.dpi = 100

    def gerar_grafico_geracao_consumo_mensal(self, ano: int = None, salvar: bool = False,
                                             caminho: str = None) -> str:
        """
        Gera gráfico de geração vs consumo mensal
        Funcionalidade principal do sistema legacy
        """
        try:
            if ano is None:
                ano = datetime.now().year

            # Obter dados mensais
            meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
                     'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

            geracao_mensal = []
            consumo_mensal = []

            for mes in range(1, 13):
                # Usar método correto da calculadora
                resultado = self.calculadora.calcular_resultado_mensal_energia(mes, ano)
                geracao_mensal.append(resultado.geracao_kwh)
                consumo_mensal.append(resultado.consumo_total_kwh)

            # Criar gráfico
            fig, ax = plt.subplots(figsize=self.figsize_padrao, dpi=self.dpi)

            x = np.arange(len(meses))
            width = 0.35

            bars1 = ax.bar(x - width / 2, geracao_mensal, width,
                           label='Geração', color=self.cores['geracao'], alpha=0.8)
            bars2 = ax.bar(x + width / 2, consumo_mensal, width,
                           label='Consumo', color=self.cores['consumo'], alpha=0.8)

            # Configurações do gráfico
            ax.set_xlabel('Mês', fontsize=12)
            ax.set_ylabel('Energia (kWh)', fontsize=12)
            ax.set_title(f'Geração vs Consumo Mensal - {ano}', fontsize=14, fontweight='bold')
            ax.set_xticks(x)
            ax.set_xticklabels(meses)
            ax.legend()
            ax.grid(True, alpha=0.3)

            # Adicionar valores nas barras
            for bar in bars1:
                height = bar.get_height()
                if height > 0:
                    ax.text(bar.get_x() + bar.get_width() / 2., height + max(geracao_mensal) * 0.02,
                            f'{height:.0f}', ha='center', va='bottom', fontsize=9)

            for bar in bars2:
                height = bar.get_height()
                if height > 0:
                    ax.text(bar.get_x() + bar.get_width() / 2., height + max(consumo_mensal) * 0.02,
                            f'{height:.0f}', ha='center', va='bottom', fontsize=9)

            plt.tight_layout()

            # Salvar se solicitado
            if salvar:
                caminho_arquivo = self._salvar_grafico(fig, caminho, 'geracao_consumo_mensal')
                plt.close(fig)
                return caminho_arquivo

            plt.show()
            return "Gráfico exibido"

        except Exception as e:
            raise ErroGrafico(f"Erro ao gerar gráfico geração vs consumo: {e}")

    def gerar_grafico_economia_mensal(self, ano: int = None, salvar: bool = False,
                                      caminho: str = None) -> str:
        """
        Gera gráfico de economia mensal
        Funcionalidade do sistema legacy
        """
        try:
            if ano is None:
                ano = datetime.now().year

            # Obter dados financeiros mensais
            meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
                     'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

            economia_mensal = []
            custo_sem_solar = []
            custo_com_solar = []

            for mes in range(1, 13):
                # Usar método correto da calculadora
                resultado_energia = self.calculadora.calcular_resultado_mensal_energia(mes, ano)
                resultado_financeiro = self.gerenciador.calcular_resultado_financeiro_mensal(mes, ano)

                economia_mensal.append(resultado_financeiro.economia_mensal)
                custo_sem_solar.append(resultado_financeiro.custo_sem_solar)
                custo_com_solar.append(resultado_financeiro.custo_com_solar)

            # Criar gráfico
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), dpi=self.dpi)

            # Gráfico 1: Custos comparativos
            x = np.arange(len(meses))
            width = 0.35

            ax1.bar(x - width / 2, custo_sem_solar, width,
                    label='Sem Solar', color=self.cores['custo'], alpha=0.8)
            ax1.bar(x + width / 2, custo_com_solar, width,
                    label='Com Solar', color=self.cores['geracao'], alpha=0.8)

            ax1.set_xlabel('Mês', fontsize=12)
            ax1.set_ylabel('Custo (R$)', fontsize=12)
            ax1.set_title('Comparação de Custos Mensais', fontsize=14, fontweight='bold')
            ax1.set_xticks(x)
            ax1.set_xticklabels(meses)
            ax1.legend()
            ax1.grid(True, alpha=0.3)

            # Gráfico 2: Economia mensal
            ax2.bar(meses, economia_mensal, color=self.cores['economia'], alpha=0.8)
            ax2.set_xlabel('Mês', fontsize=12)
            ax2.set_ylabel('Economia (R$)', fontsize=12)
            ax2.set_title('Economia Mensal com Sistema Solar', fontsize=14, fontweight='bold')
            ax2.grid(True, alpha=0.3)

            # Adicionar valores nas barras
            if economia_mensal and max(economia_mensal) > 0:
                for i, valor in enumerate(economia_mensal):
                    ax2.text(i, valor + max(economia_mensal) * 0.01,
                             f'R$ {valor:.0f}', ha='center', va='bottom', fontsize=9)

            plt.tight_layout()

            # Salvar se solicitado
            if salvar:
                caminho_arquivo = self._salvar_grafico(fig, caminho, 'economia_mensal')
                plt.close(fig)
                return caminho_arquivo

            plt.show()
            return "Gráfico exibido"

        except Exception as e:
            raise ErroGrafico(f"Erro ao gerar gráfico de economia: {e}")

    def gerar_grafico_saldo_energetico(self, ano: int = None, salvar: bool = False,
                                       caminho: str = None) -> str:
        """
        Gera gráfico de saldo energético mensal
        Funcionalidade do sistema legacy
        """
        try:
            if ano is None:
                ano = datetime.now().year

            # Obter dados de saldo energético
            meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
                     'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

            saldo_mensal = []
            energia_injetada = []
            energia_consumida_rede = []

            for mes in range(1, 13):
                resultado = self.calculadora.calcular_resultado_mensal_energia(mes, ano)
                saldo_mensal.append(resultado.saldo_kwh)
                energia_injetada.append(resultado.energia_injetada_kwh)
                energia_consumida_rede.append(resultado.energia_consumida_rede_kwh)

            # Criar gráfico
            fig, ax = plt.subplots(figsize=self.figsize_padrao, dpi=self.dpi)

            # Gráfico de barras empilhadas
            x = np.arange(len(meses))

            # Separar valores positivos e negativos
            saldo_positivo = [max(0, s) for s in saldo_mensal]
            saldo_negativo = [min(0, s) for s in saldo_mensal]

            bars1 = ax.bar(x, saldo_positivo, label='Excesso (Créditos)',
                           color=self.cores['creditos'], alpha=0.8)
            bars2 = ax.bar(x, saldo_negativo, label='Déficit (Rede)',
                           color=self.cores['custo'], alpha=0.8)

            # Linha zero
            ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8)

            # Configurações do gráfico
            ax.set_xlabel('Mês', fontsize=12)
            ax.set_ylabel('Saldo Energético (kWh)', fontsize=12)
            ax.set_title(f'Saldo Energético Mensal - {ano}', fontsize=14, fontweight='bold')
            ax.set_xticks(x)
            ax.set_xticklabels(meses)
            ax.legend()
            ax.grid(True, alpha=0.3)

            # Adicionar valores nas barras
            for i, valor in enumerate(saldo_mensal):
                if valor > 0 and saldo_mensal:
                    max_positivo = max([s for s in saldo_mensal if s > 0]) if any(s > 0 for s in saldo_mensal) else 1
                    ax.text(i, valor + max_positivo * 0.02,
                            f'{valor:.0f}', ha='center', va='bottom', fontsize=9)
                elif valor < 0 and saldo_mensal:
                    min_negativo = min([s for s in saldo_mensal if s < 0]) if any(s < 0 for s in saldo_mensal) else -1
                    ax.text(i, valor + min_negativo * 0.02,
                            f'{valor:.0f}', ha='center', va='top', fontsize=9)

            plt.tight_layout()

            # Salvar se solicitado
            if salvar:
                caminho_arquivo = self._salvar_grafico(fig, caminho, 'saldo_energetico')
                plt.close(fig)
                return caminho_arquivo

            plt.show()
            return "Gráfico exibido"

        except Exception as e:
            raise ErroGrafico(f"Erro ao gerar gráfico de saldo energético: {e}")

    def gerar_grafico_distribuicao_consumo(self, salvar: bool = False,
                                           caminho: str = None) -> str:
        """
        Gera gráfico de distribuição de consumo por unidade
        Funcionalidade do sistema legacy
        """
        try:
            # Obter dados de consumo por unidade
            unidades_ativas = self.sistema.get_unidades_ativas()

            if not unidades_ativas:
                raise ErroGrafico("Nenhuma unidade ativa encontrada")

            nomes_unidades = []
            consumo_anual = []

            consumo_total_sistema = 0

            for unidade in unidades_ativas:
                consumo_unidade = sum(unidade.consumo_mensal_kwh)
                consumo_total_sistema += consumo_unidade

                nomes_unidades.append(unidade.nome)
                consumo_anual.append(consumo_unidade)

            # Criar gráfico
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6), dpi=self.dpi)

            # Gráfico 1: Pizza
            cores_pizza = plt.cm.Set3(np.linspace(0, 1, len(nomes_unidades)))
            wedges, texts, autotexts = ax1.pie(consumo_anual, labels=nomes_unidades,
                                               autopct='%1.1f%%', startangle=90,
                                               colors=cores_pizza)
            ax1.set_title('Distribuição do Consumo por Unidade', fontsize=14, fontweight='bold')

            # Gráfico 2: Barras
            bars = ax2.bar(nomes_unidades, consumo_anual, color=cores_pizza, alpha=0.8)
            ax2.set_xlabel('Unidades', fontsize=12)
            ax2.set_ylabel('Consumo Anual (kWh)', fontsize=12)
            ax2.set_title('Consumo Anual por Unidade', fontsize=14, fontweight='bold')
            ax2.grid(True, alpha=0.3)

            # Rotacionar labels se necessário
            if nomes_unidades and len(max(nomes_unidades, key=len)) > 10:
                ax2.tick_params(axis='x', rotation=45)

            # Adicionar valores nas barras
            if consumo_anual and max(consumo_anual) > 0:
                for bar, valor in zip(bars, consumo_anual):
                    height = bar.get_height()
                    ax2.text(bar.get_x() + bar.get_width() / 2., height + max(consumo_anual) * 0.01,
                             f'{valor:.0f}', ha='center', va='bottom', fontsize=9)

            plt.tight_layout()

            # Salvar se solicitado
            if salvar:
                caminho_arquivo = self._salvar_grafico(fig, caminho, 'distribuicao_consumo')
                plt.close(fig)
                return caminho_arquivo

            plt.show()
            return "Gráfico exibido"

        except Exception as e:
            raise ErroGrafico(f"Erro ao gerar gráfico de distribuição: {e}")

    def gerar_dashboard_completo(self, ano: int = None, salvar: bool = False,
                                 caminho: str = None) -> str:
        """
        Gera dashboard completo com múltiplos gráficos
        Funcionalidade principal do sistema legacy
        """
        try:
            if ano is None:
                ano = datetime.now().year

            # Criar figura com subplots
            fig = plt.figure(figsize=(20, 16), dpi=self.dpi)

            # Layout do dashboard: 3x2 grid
            gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)

            # Obter dados para todos os gráficos
            meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
                     'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

            geracao_mensal = []
            consumo_mensal = []
            economia_mensal = []
            saldo_mensal = []
            eficiencia_mensal = []

            for mes in range(1, 13):
                resultado_energia = self.calculadora.calcular_resultado_mensal_energia(mes, ano)
                resultado_financeiro = self.gerenciador.calcular_resultado_financeiro_mensal(mes, ano)

                geracao_mensal.append(resultado_energia.geracao_kwh)
                consumo_mensal.append(resultado_energia.consumo_total_kwh)
                economia_mensal.append(resultado_financeiro.economia_mensal)
                saldo_mensal.append(resultado_energia.saldo_kwh)
                eficiencia_mensal.append(resultado_energia.eficiencia_real * 100)

            # Gráfico 1: Geração vs Consumo
            ax1 = fig.add_subplot(gs[0, 0])
            x = np.arange(len(meses))
            width = 0.35
            ax1.bar(x - width / 2, geracao_mensal, width, label='Geração',
                    color=self.cores['geracao'], alpha=0.8)
            ax1.bar(x + width / 2, consumo_mensal, width, label='Consumo',
                    color=self.cores['consumo'], alpha=0.8)
            ax1.set_title('Geração vs Consumo Mensal', fontweight='bold')
            ax1.set_xticks(x)
            ax1.set_xticklabels(meses, rotation=45)
            ax1.legend()
            ax1.grid(True, alpha=0.3)

            # Gráfico 2: Economia Mensal
            ax2 = fig.add_subplot(gs[0, 1])
            ax2.bar(meses, economia_mensal, color=self.cores['economia'], alpha=0.8)
            ax2.set_title('Economia Mensal', fontweight='bold')
            ax2.tick_params(axis='x', rotation=45)
            ax2.grid(True, alpha=0.3)

            # Gráfico 3: Saldo Energético
            ax3 = fig.add_subplot(gs[1, 0])
            saldo_positivo = [max(0, s) for s in saldo_mensal]
            saldo_negativo = [min(0, s) for s in saldo_mensal]
            ax3.bar(x, saldo_positivo, label='Excesso', color=self.cores['creditos'], alpha=0.8)
            ax3.bar(x, saldo_negativo, label='Déficit', color=self.cores['custo'], alpha=0.8)
            ax3.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
            ax3.set_title('Saldo Energético Mensal', fontweight='bold')
            ax3.set_xticks(x)
            ax3.set_xticklabels(meses, rotation=45)
            ax3.legend()
            ax3.grid(True, alpha=0.3)

            # Gráfico 4: Eficiência do Sistema
            ax4 = fig.add_subplot(gs[1, 1])
            ax4.plot(meses, eficiencia_mensal, marker='o', linewidth=2,
                     color=self.cores['eficiencia'])
            ax4.set_title('Eficiência Real do Sistema', fontweight='bold')
            ax4.set_ylabel('Eficiência (%)')
            ax4.tick_params(axis='x', rotation=45)
            ax4.grid(True, alpha=0.3)
            ax4.set_ylim(0, 100)

            # Gráfico 5: Distribuição de Consumo (Pizza)
            ax5 = fig.add_subplot(gs[2, 0])
            unidades_ativas = self.sistema.get_unidades_ativas()
            nomes_unidades = [u.nome for u in unidades_ativas]
            consumo_unidades = [sum(u.consumo_mensal_kwh) for u in unidades_ativas]

            if consumo_unidades:
                cores_pizza = plt.cm.Set3(np.linspace(0, 1, len(nomes_unidades)))
                ax5.pie(consumo_unidades, labels=nomes_unidades, autopct='%1.1f%%',
                        startangle=90, colors=cores_pizza)
                ax5.set_title('Distribuição do Consumo', fontweight='bold')

            # Gráfico 6: Resumo Financeiro
            ax6 = fig.add_subplot(gs[2, 1])
            economia_anual = sum(economia_mensal) if economia_mensal else 0
            investimento = self.sistema.configuracao.custo_investimento
            roi_25_anos = (economia_anual * 25 / investimento) * 100 if investimento > 0 else 0

            categorias = ['Economia\nAnual', 'Investimento', 'ROI\n(25 anos)']
            valores = [economia_anual, investimento, roi_25_anos * 1000]  # Escalar ROI para visualização

            cores_resumo = [self.cores['economia'], self.cores['custo'], self.cores['creditos']]
            bars = ax6.bar(categorias, valores, color=cores_resumo, alpha=0.8)
            ax6.set_title('Resumo Financeiro', fontweight='bold')
            ax6.set_ylabel('Valor (R$)')

            # Adicionar valores nas barras
            if valores and max(valores) > 0:
                for bar, valor, categoria in zip(bars, valores, categorias):
                    height = bar.get_height()
                    if 'ROI' in categoria:
                        texto = f'{roi_25_anos:.1f}%'
                    else:
                        texto = f'R$ {valor:,.0f}'
                    ax6.text(bar.get_x() + bar.get_width() / 2., height + max(valores) * 0.01,
                             texto, ha='center', va='bottom', fontsize=9)

            # Título geral do dashboard
            fig.suptitle(f'Dashboard Energia Solar - {ano}', fontsize=20, fontweight='bold', y=0.98)

            # Adicionar informações resumo
            payback_anos = investimento / economia_anual if economia_anual > 0 else 0
            info_text = (f"Sistema: {self.sistema.configuracao.potencia_instalada_kw:.1f} kW | "
                         f"Payback: {payback_anos:.1f} anos | "
                         f"Economia Anual: R$ {economia_anual:,.0f}")

            fig.text(0.5, 0.02, info_text, ha='center', fontsize=12,
                     bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))

            # Salvar se solicitado
            if salvar:
                caminho_arquivo = self._salvar_grafico(fig, caminho, f'dashboard_completo_{ano}')
                plt.close(fig)
                return caminho_arquivo

            plt.show()
            return "Dashboard exibido"

        except Exception as e:
            raise ErroGrafico(f"Erro ao gerar dashboard: {e}")

    # Métodos auxiliares privados

    def _salvar_grafico(self, fig, caminho: str = None, nome_padrao: str = "grafico") -> str:
        """Salva gráfico em arquivo"""
        try:
            if caminho is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                caminho = f"{nome_padrao}_{timestamp}.png"

            # Garantir extensão .png
            if not caminho.lower().endswith('.png'):
                caminho += '.png'

            # Criar diretório se necessário
            diretorio = os.path.dirname(caminho)
            if diretorio and not os.path.exists(diretorio):
                os.makedirs(diretorio)

            fig.savefig(caminho, dpi=self.dpi, bbox_inches='tight',
                        facecolor='white', edgecolor='none')

            return caminho

        except Exception as e:
            raise ErroGrafico(f"Erro ao salvar gráfico: {e}")


# Funções de conveniência para compatibilidade legacy
def gerar_grafico_sistema_legacy(sistema: SistemaEnergia, tipo_grafico: str, **kwargs) -> str:
    """Função de conveniência para gerar gráficos do sistema legacy"""
    gerador = GeradorGraficosAnalise(sistema)

    graficos_disponiveis = {
        'geracao_consumo': gerador.gerar_grafico_geracao_consumo_mensal,
        'economia': gerador.gerar_grafico_economia_mensal,
        'saldo': gerador.gerar_grafico_saldo_energetico,
        'distribuicao': gerador.gerar_grafico_distribuicao_consumo,
        'dashboard': gerador.gerar_dashboard_completo
    }

    if tipo_grafico not in graficos_disponiveis:
        raise ErroGrafico(f"Tipo de gráfico não suportado: {tipo_grafico}")

    return graficos_disponiveis[tipo_grafico](**kwargs)