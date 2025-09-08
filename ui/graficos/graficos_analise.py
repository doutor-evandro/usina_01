# usina_01/ui/graficos/graficos_analise.py

import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Tuple

from nucleo.modelos import SistemaEnergia
from negocio.calculadora_energia import CalculadoraEnergia
from negocio.gerenciador_distribuicao import GerenciadorDistribuicao
from utilitarios.constantes import MESES_APENAS


class GraficosAnalise:
    """
    Classe responsável por criar os diferentes tipos de gráficos de análise
    do sistema de energia solar.
    """

    def __init__(self, sistema: SistemaEnergia):
        self.sistema = sistema
        self.calculadora = CalculadoraEnergia(sistema)
        self.gerenciador = GerenciadorDistribuicao(sistema)

        # Cores padrão para os gráficos
        self.cores = {
            'geracao': '#FFA500',  # Laranja para geração solar
            'consumo': '#4169E1',  # Azul para consumo
            'economia': '#32CD32',  # Verde para economia
            'deficit': '#FF6347',  # Vermelho para déficit
            'excesso': '#32CD32',  # Verde para excesso
            'custo_sem': '#FF6347',  # Vermelho para custo sem solar
            'custo_com': '#32CD32',  # Verde para custo com solar
            'eficiencia': '#4169E1'  # Azul para eficiência
        }

    def obter_dados_mensais(self) -> Tuple[Dict, Dict]:
        """
        Obtém os dados mensais calculados do sistema.

        Returns:
            Tuple com resultados energéticos e financeiros mensais
        """
        resultados_energeticos, _ = self.calculadora.calcular_resultados_anuais()
        resultados_financeiros, _ = self.gerenciador.calcular_resultados_financeiros_anuais()

        return resultados_energeticos, resultados_financeiros

    def criar_grafico_geracao_consumo(self, ax):
        """
        Cria gráfico de barras comparando geração solar vs consumo total.

        Args:
            ax: Eixo do matplotlib onde desenhar o gráfico
        """
        resultados_energeticos, _ = self.obter_dados_mensais()

        # Prepara dados
        meses = MESES_APENAS
        meses_abrev = [mes[:3] for mes in meses]
        geracao = [resultados_energeticos.resultados_por_mes[mes].geracao_kwh for mes in meses]
        consumo = [resultados_energeticos.resultados_por_mes[mes].consumo_total_kwh for mes in meses]

        # Cria o gráfico
        x = np.arange(len(meses))
        width = 0.35

        bars1 = ax.bar(x - width / 2, geracao, width, label='Geração Solar',
                       color=self.cores['geracao'], alpha=0.8)
        bars2 = ax.bar(x + width / 2, consumo, width, label='Consumo Total',
                       color=self.cores['consumo'], alpha=0.8)

        # Configurações
        ax.set_xlabel('Meses', fontweight='bold')
        ax.set_ylabel('Energia (kWh)', fontweight='bold')
        ax.set_title('Geração Solar vs Consumo Total - Análise Mensal',
                     fontsize=14, fontweight='bold', pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels(meses_abrev, rotation=45)
        ax.legend(loc='upper right')
        ax.grid(True, alpha=0.3)

        # Adiciona valores nas barras
        for bar in bars1:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height + max(geracao) * 0.01,
                    f'{height:.0f}', ha='center', va='bottom', fontsize=8, fontweight='bold')

        for bar in bars2:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height + max(consumo) * 0.01,
                    f'{height:.0f}', ha='center', va='bottom', fontsize=8, fontweight='bold')

        # Adiciona linha de média
        media_geracao = sum(geracao) / len(geracao)
        media_consumo = sum(consumo) / len(consumo)

        ax.axhline(y=media_geracao, color=self.cores['geracao'], linestyle='--', alpha=0.7,
                   label=f'Média Geração: {media_geracao:.0f} kWh')
        ax.axhline(y=media_consumo, color=self.cores['consumo'], linestyle='--', alpha=0.7,
                   label=f'Média Consumo: {media_consumo:.0f} kWh')

    def criar_grafico_economia_mensal(self, ax):
        """
        Cria gráfico de barras da economia mensal.

        Args:
            ax: Eixo do matplotlib onde desenhar o gráfico
        """
        _, resultados_financeiros = self.obter_dados_mensais()

        # Prepara dados
        meses = MESES_APENAS
        meses_abrev = [mes[:3] for mes in meses]
        economia = [resultados_financeiros.resultados_por_mes[mes].economia_reais for mes in meses]

        # Cria o gráfico
        bars = ax.bar(meses_abrev, economia, color=self.cores['economia'], alpha=0.8)

        # Configurações
        ax.set_xlabel('Meses', fontweight='bold')
        ax.set_ylabel('Economia (R$)', fontweight='bold')
        ax.set_title('Economia Mensal com Energia Solar', fontsize=14, fontweight='bold', pad=20)
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True, alpha=0.3)

        # Adiciona valores nas barras
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height + max(economia) * 0.01,
                    f'R$ {height:.0f}', ha='center', va='bottom', fontsize=9, fontweight='bold')

        # Linha de média
        media_economia = sum(economia) / len(economia)
        ax.axhline(y=media_economia, color='red', linestyle='--', alpha=0.7,
                   label=f'Média Mensal: R$ {media_economia:.0f}')
        ax.legend()

        # Adiciona total anual no gráfico
        total_anual = sum(economia)
        ax.text(0.02, 0.98,
                f'Economia Total Anual: R$ {total_anual:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'),
                transform=ax.transAxes, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8),
                fontsize=10, fontweight='bold')

    def criar_grafico_saldo_energetico(self, ax):
        """
        Cria gráfico de saldo energético (geração - consumo).

        Args:
            ax: Eixo do matplotlib onde desenhar o gráfico
        """
        resultados_energeticos, _ = self.obter_dados_mensais()

        # Prepara dados
        meses = MESES_APENAS
        meses_abrev = [mes[:3] for mes in meses]
        saldos = []

        for mes in meses:
            resultado_mes = resultados_energeticos.resultados_por_mes[mes]
            saldo = resultado_mes.geracao_kwh - resultado_mes.consumo_total_kwh
            saldos.append(saldo)

        # Cores baseadas no saldo
        cores = [self.cores['excesso'] if saldo >= 0 else self.cores['deficit'] for saldo in saldos]

        # Cria o gráfico
        bars = ax.bar(meses_abrev, saldos, color=cores, alpha=0.8)

        # Configurações
        ax.set_xlabel('Meses', fontweight='bold')
        ax.set_ylabel('Saldo Energético (kWh)', fontweight='bold')
        ax.set_title('Saldo Energético Mensal (Geração - Consumo)',
                     fontsize=14, fontweight='bold', pad=20)
        ax.tick_params(axis='x', rotation=45)
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.8, linewidth=2)

        # Adiciona valores nas barras
        for bar, saldo in zip(bars, saldos):
            height = bar.get_height()
            y_pos = height + (max(saldos) * 0.02) if height >= 0 else height - (abs(min(saldos)) * 0.02)
            va = 'bottom' if height >= 0 else 'top'

            ax.text(bar.get_x() + bar.get_width() / 2., y_pos,
                    f'{saldo:.0f}', ha='center', va=va, fontsize=8, fontweight='bold')

        # Legenda explicativa
        ax.text(0.02, 0.98,
                'Verde: Excesso de geração (créditos)\nVermelho: Déficit energético (compra da rede)',
                transform=ax.transAxes, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.9),
                fontsize=9)

    def criar_grafico_distribuicao_unidades(self, ax):
        """
        Cria gráfico de pizza com distribuição de consumo por unidade.

        Args:
            ax: Eixo do matplotlib onde desenhar o gráfico
        """
        # Calcula consumo total por unidade
        consumos_unidades = {}
        for unidade in self.sistema.unidades:
            consumo_anual = sum(self.sistema.consumos.get(unidade.codigo, {}).values())
            if consumo_anual > 0:
                label = f"{unidade.codigo}\n{unidade.nome}"
                consumos_unidades[label] = consumo_anual

        if not consumos_unidades:
            ax.text(0.5, 0.5, 'Nenhum dado de consumo encontrado',
                    ha='center', va='center', transform=ax.transAxes, fontsize=14)
            return

        # Prepara dados
        labels = list(consumos_unidades.keys())
        sizes = list(consumos_unidades.values())

        # Cores automáticas
        colors = plt.cm.Set3(np.linspace(0, 1, len(labels)))

        # Cria o gráfico
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%',
                                          colors=colors, startangle=90,
                                          textprops={'fontsize': 9})

        # Configurações
        ax.set_title('Distribuição de Consumo por Unidade Consumidora',
                     fontsize=14, fontweight='bold', pad=20)

        # Melhora a legibilidade dos percentuais
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)

        # Adiciona informações no centro
        total_consumo = sum(sizes)
        ax.text(0, 0, f'Total Anual\n{total_consumo:,.0f} kWh'.replace(',', '.'),
                ha='center', va='center', fontsize=11, fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))

    def criar_grafico_analise_financeira(self, ax1, ax2):
        """
        Cria gráfico de análise financeira com economia mensal e acumulada.

        Args:
            ax1: Eixo principal (economia mensal)
            ax2: Eixo secundário (economia acumulada)
        """
        _, resultados_financeiros = self.obter_dados_mensais()

        # Prepara dados
        meses = MESES_APENAS
        meses_abrev = [mes[:3] for mes in meses]
        economia_mensal = [resultados_financeiros.resultados_por_mes[mes].economia_reais for mes in meses]
        economia_acumulada = np.cumsum(economia_mensal)

        # Gráfico de barras para economia mensal
        bars = ax1.bar(meses_abrev, economia_mensal, alpha=0.7, color=self.cores['economia'],
                       label='Economia Mensal')

        # Linha para economia acumulada
        line = ax2.plot(meses_abrev, economia_acumulada, color=self.cores['deficit'],
                        marker='o', linewidth=3, markersize=6, label='Economia Acumulada')

        # Configurações dos eixos
        ax1.set_xlabel('Meses', fontweight='bold')
        ax1.set_ylabel('Economia Mensal (R$)', color=self.cores['economia'], fontweight='bold')
        ax2.set_ylabel('Economia Acumulada (R$)', color=self.cores['deficit'], fontweight='bold')
        ax1.tick_params(axis='x', rotation=45)
        ax1.tick_params(axis='y', labelcolor=self.cores['economia'])
        ax2.tick_params(axis='y', labelcolor=self.cores['deficit'])
        ax1.grid(True, alpha=0.3)

        # Título
        ax1.set_title('Análise Financeira - Economia com Energia Solar',
                      fontsize=14, fontweight='bold', pad=20)

        # Legendas combinadas
        lines1, labels1 = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

        # Adiciona valores na linha (apenas alguns para não poluir)
        for i, (mes, valor) in enumerate(zip(meses_abrev, economia_acumulada)):
            if i % 3 == 0 or i == len(meses_abrev) - 1:  # Mostra a cada 3 meses e o último
                ax2.annotate(f'R$ {valor:.0f}',
                             (i, valor), textcoords="offset points",
                             xytext=(0, 15), ha='center', fontsize=8, fontweight='bold')

    def criar_grafico_comparativo_anual(self, ax):
        """
        Cria gráfico comparativo de custos com e sem energia solar.

        Args:
            ax: Eixo do matplotlib onde desenhar o gráfico
        """
        _, resultados_financeiros = self.obter_dados_mensais()

        # Prepara dados
        meses = MESES_APENAS
        meses_abrev = [mes[:3] for mes in meses]
        custo_sem_solar = []
        custo_com_solar = []

        for mes in meses:
            resultado_mes = resultados_financeiros.resultados_por_mes[mes]
            custo_sem_solar.append(resultado_mes.custo_sem_solar_reais)
            custo_com_solar.append(resultado_mes.custo_com_solar_reais)

        # Cria o gráfico
        x = np.arange(len(meses))
        width = 0.35

        bars1 = ax.bar(x - width / 2, custo_sem_solar, width,
                       label='Sem Energia Solar', color=self.cores['custo_sem'], alpha=0.8)
        bars2 = ax.bar(x + width / 2, custo_com_solar, width,
                       label='Com Energia Solar', color=self.cores['custo_com'], alpha=0.8)

        # Configurações
        ax.set_xlabel('Meses', fontweight='bold')
        ax.set_ylabel('Custo da Energia (R$)', fontweight='bold')
        ax.set_title('Comparativo de Custos: Com vs Sem Energia Solar',
                     fontsize=14, fontweight='bold', pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels(meses_abrev, rotation=45)
        ax.legend()
        ax.grid(True, alpha=0.3)

        # Adiciona economia no topo das barras
        for i, (sem, com) in enumerate(zip(custo_sem_solar, custo_com_solar)):
            economia = sem - com
            y_pos = max(sem, com) + max(custo_sem_solar) * 0.02
            ax.text(i, y_pos, f'-R$ {economia:.0f}',
                    ha='center', va='bottom', fontsize=8, color='green', fontweight='bold')

        # Adiciona totais anuais
        total_sem = sum(custo_sem_solar)
        total_com = sum(custo_com_solar)
        economia_total = total_sem - total_com

        ax.text(0.02, 0.98,
                f'Total Anual:\nSem Solar: R$ {total_sem:,.2f}\nCom Solar: R$ {total_com:,.2f}\nEconomia: R$ {economia_total:,.2f}'.replace(
                    ',', 'X').replace('.', ',').replace('X', '.'),
                transform=ax.transAxes, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8),
                fontsize=9, fontweight='bold')

    def criar_grafico_eficiencia_sistema(self, ax):
        """
        Cria gráfico de eficiência/autossuficiência do sistema.

        Args:
            ax: Eixo do matplotlib onde desenhar o gráfico
        """
        resultados_energeticos, _ = self.obter_dados_mensais()

        # Prepara dados
        meses = MESES_APENAS
        meses_abrev = [mes[:3] for mes in meses]
        percentual_autossuficiencia = []

        for mes in meses:
            resultado_mes = resultados_energeticos.resultados_por_mes[mes]
            if resultado_mes.consumo_total_kwh > 0:
                percentual = min(100, (resultado_mes.geracao_kwh / resultado_mes.consumo_total_kwh) * 100)
            else:
                percentual = 0
            percentual_autossuficiencia.append(percentual)

        # Cria o gráfico
        line = ax.plot(meses_abrev, percentual_autossuficiencia, marker='o', linewidth=3,
                       markersize=8, color=self.cores['eficiencia'], label='Autossuficiência Mensal')

        # Área preenchida
        ax.fill_between(meses_abrev, percentual_autossuficiencia, alpha=0.3,
                        color=self.cores['eficiencia'])

        # Linhas de referência
        ax.axhline(y=100, color='green', linestyle='--', alpha=0.7,
                   label='100% Autossuficiência')

        media = sum(percentual_autossuficiencia) / len(percentual_autossuficiencia)
        ax.axhline(y=media, color='red', linestyle='--', alpha=0.7,
                   label=f'Média: {media:.1f}%')

        # Configurações
        ax.set_xlabel('Meses', fontweight='bold')
        ax.set_ylabel('Autossuficiência (%)', fontweight='bold')
        ax.set_title('Eficiência do Sistema - Percentual de Autossuficiência',
                     fontsize=14, fontweight='bold', pad=20)
        ax.tick_params(axis='x', rotation=45)
        ax.set_ylim(0, max(110, max(percentual_autossuficiencia) + 10))
        ax.grid(True, alpha=0.3)
        ax.legend()

        # Adiciona valores nos pontos (apenas alguns)
        for i, (mes, valor) in enumerate(zip(meses_abrev, percentual_autossuficiencia)):
            if i % 2 == 0:  # Mostra apenas alguns valores
                ax.annotate(f'{valor:.1f}%',
                            (i, valor), textcoords="offset points",
                            xytext=(0, 15), ha='center', fontsize=8, fontweight='bold')

        # Adiciona informações de eficiência
        meses_100_porcento = sum(1 for p in percentual_autossuficiencia if p >= 100)
        ax.text(0.02, 0.02,
                f'Meses com 100% autossuficiência: {meses_100_porcento}/12\nEficiência média anual: {media:.1f}%',
                transform=ax.transAxes, verticalalignment='bottom',
                bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8),
                fontsize=9, fontweight='bold')


# --- Bloco de Teste ---
if __name__ == "__main__":
    print("--- Teste: ui/graficos/graficos_analise.py ---")

    # Importa dados de exemplo para teste
    from configuracao.definicoes import CONFIG_EXEMPLO, UNIDADES_EXEMPLO, CONSUMOS_EXEMPLO

    # Cria sistema de teste
    sistema_teste = SistemaEnergia(
        configuracao=CONFIG_EXEMPLO,
        unidades=UNIDADES_EXEMPLO,
        consumos=CONSUMOS_EXEMPLO
    )

    # Testa a criação da classe
    print("Criando instância de GraficosAnalise...")
    graficos = GraficosAnalise(sistema_teste)
    print("✓ GraficosAnalise criado com sucesso!")

    # Testa obtenção de dados
    print("Testando obtenção de dados...")
    resultados_energeticos, resultados_financeiros = graficos.obter_dados_mensais()
    print("✓ Dados mensais obtidos com sucesso!")

    # Testa criação de um gráfico simples
    print("Testando criação de gráfico...")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(10, 6))
    graficos.criar_grafico_geracao_consumo(ax)
    plt.title("Teste - Gráfico de Geração vs Consumo")
    plt.tight_layout()

    # Salva o gráfico de teste
    plt.savefig("teste_grafico.png", dpi=150, bbox_inches='tight')
    print("✓ Gráfico de teste criado e salvo como 'teste_grafico.png'!")

    plt.close()  # Fecha a figura para liberar memória

    print("Teste de GraficosAnalise concluído com sucesso!")