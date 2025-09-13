"""
Módulo de Gráficos Legacy - Sistema de Créditos de Energia
Adaptação dos gráficos originais para a nova estrutura
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from typing import Dict, List, Optional
import numpy as np

# Importações do sistema atual
from utilitarios.funcoes_legacy import FuncoesLegacy, formatar_numero_inteiro_brasileiro
from utilitarios.formatadores import formatar_energia, formatar_moeda

# Configuração de cores (compatível com programa antigo)
CORES_GRAFICO = [
    '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7',
    '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9',
    '#F8C471', '#82E0AA', '#F1948A', '#85C1E9', '#F4D03F'
]


class GraficosLegacy:
    """Classe para gráficos compatíveis com sistema legacy"""

    def __init__(self, funcoes_legacy: FuncoesLegacy):
        self.funcoes = funcoes_legacy
        self.meses_completos = [
            "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
        ]

    def criar_grafico_base(self, parent, titulo: str = "Distribuição de Energia") -> tuple:
        """Cria o gráfico base e retorna figura e canvas"""
        try:
            # Criar figura
            fig = Figure(figsize=(10, 8), dpi=100)
            ax = fig.add_subplot(111)

            # Configuração inicial
            ax.set_title(titulo, fontsize=14, fontweight='bold')
            ax.text(0.5, 0.5, 'Carregando dados...',
                    horizontalalignment='center', verticalalignment='center',
                    transform=ax.transAxes, fontsize=12)

            # Criar canvas
            canvas = FigureCanvasTkAgg(fig, parent)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)

            return fig, canvas

        except Exception as e:
            print(f"❌ Erro ao criar gráfico: {e}")
            # Fallback: criar label simples
            label = ttk.Label(parent, text="Gráfico não disponível", font=('Arial', 12))
            label.pack(expand=True)
            return None, None

    def atualizar_grafico_pizza(self, figura, canvas, dados: Dict, titulo: str = "Distribuição de Energia"):
        """Atualiza o gráfico com dados em formato pizza"""
        if not figura or not canvas:
            return

        try:
            # Limpar gráfico anterior
            figura.clear()
            ax = figura.add_subplot(111)

            if not dados:
                ax.text(0.5, 0.5, 'Nenhum dado disponível',
                        horizontalalignment='center', verticalalignment='center',
                        transform=ax.transAxes, fontsize=12)
            else:
                # Preparar dados
                labels = list(dados.keys())
                sizes = list(dados.values())
                colors = CORES_GRAFICO[:len(labels)]

                # Filtrar valores muito pequenos
                dados_filtrados = []
                labels_filtrados = []
                colors_filtrados = []
                outros_valor = 0

                for i, (label, size) in enumerate(zip(labels, sizes)):
                    if size >= 1.0:  # Só mostrar se >= 1%
                        dados_filtrados.append(size)
                        labels_filtrados.append(label)
                        colors_filtrados.append(colors[i] if i < len(colors) else '#CCCCCC')
                    else:
                        outros_valor += size

                # Adicionar "Outros" se necessário
                if outros_valor > 0:
                    dados_filtrados.append(outros_valor)
                    labels_filtrados.append('Outros')
                    colors_filtrados.append('#CCCCCC')

                # Criar gráfico de pizza
                wedges, texts, autotexts = ax.pie(
                    dados_filtrados,
                    labels=labels_filtrados,
                    autopct='%1.1f%%',
                    colors=colors_filtrados,
                    startangle=90,
                    textprops={'fontsize': 10}
                )

                # Melhorar legibilidade
                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontweight('bold')
                    autotext.set_fontsize(9)

                # Ajustar labels para não sobrepor
                for text in texts:
                    text.set_fontsize(9)

            ax.set_title(titulo, fontsize=14, fontweight='bold', pad=20)
            figura.tight_layout()
            canvas.draw()

        except Exception as e:
            print(f"❌ Erro ao atualizar gráfico: {e}")
            # Mostrar erro no gráfico
            figura.clear()
            ax = figura.add_subplot(111)
            ax.text(0.5, 0.5, f'Erro: {str(e)}',
                    horizontalalignment='center', verticalalignment='center',
                    transform=ax.transAxes, fontsize=12, color='red')
            canvas.draw()

    def mostrar_grafico_distribuicao(self, parent, mes: str):
        """Mostra gráfico de distribuição de créditos para um mês"""
        janela = tk.Toplevel(parent)
        janela.title(f"📊 Distribuição de Créditos - {mes}")
        janela.geometry("1000x700")
        janela.transient(parent)

        # Frame principal
        main_frame = ttk.Frame(janela, padding="10")
        main_frame.pack(fill="both", expand=True)

        # Título
        ttk.Label(main_frame, text=f"Distribuição de Créditos - {mes}",
                  font=('Arial', 16, 'bold')).pack(pady=(0, 20))

        # Obter dados legacy
        dados_sistema = self.funcoes.obter_dados_legacy()

        # Frame para informações
        info_frame = ttk.LabelFrame(main_frame, text="Informações do Sistema", padding=10)
        info_frame.pack(fill='x', pady=(0, 10))

        # Calcular saldo com eficiência
        saldo_info = self.funcoes.calcular_saldo_mensal_com_eficiencia(dados_sistema, mes)

        # Formatação brasileira
        geracao_nominal_fmt = formatar_numero_inteiro_brasileiro(saldo_info['geracao_nominal'])
        geracao_real_fmt = formatar_numero_inteiro_brasileiro(saldo_info['geracao_real'])
        consumo_total_fmt = formatar_numero_inteiro_brasileiro(saldo_info['consumo_total'])
        tarifas_total_fmt = formatar_numero_inteiro_brasileiro(saldo_info['tarifas_total'])
        saldo_fmt = formatar_numero_inteiro_brasileiro(abs(saldo_info['saldo']))

        info_text = f"""Geração Nominal: {geracao_nominal_fmt} kWh
Geração Real ({saldo_info['eficiencia']:.0f}%): {geracao_real_fmt} kWh
Consumo Total: {consumo_total_fmt} kWh
Tarifas Mínimas: {tarifas_total_fmt} kWh
Saldo: {saldo_fmt} kWh ({saldo_info['status']})"""

        ttk.Label(info_frame, text=info_text, font=('Courier', 11)).pack()

        # Frame para o gráfico
        grafico_frame = ttk.Frame(main_frame)
        grafico_frame.pack(fill='both', expand=True)

        try:
            # Calcular percentuais em relação à usina
            percentuais = self.funcoes.calcular_porcentagens_em_relacao_usina(dados_sistema, mes)

            if percentuais:
                # Criar gráfico
                fig, canvas = self.criar_grafico_base(grafico_frame, f'Distribuição de Créditos - {mes}')
                if fig and canvas:
                    self.atualizar_grafico_pizza(fig, canvas, percentuais, f'Distribuição de Créditos - {mes}')
            else:
                ttk.Label(grafico_frame, text="Nenhum dado de consumo disponível",
                          font=('Arial', 12)).pack(expand=True)

        except Exception as e:
            ttk.Label(grafico_frame, text=f"Erro ao gerar gráfico: {e}",
                      font=('Arial', 12)).pack(expand=True)

        # Botão para fechar
        ttk.Button(main_frame, text="Fechar", command=janela.destroy).pack(pady=10)

    def criar_janela_graficos_analises(self, parent):
        """Cria janela com gráficos de análises"""
        janela = tk.Toplevel(parent)
        janela.title("📈 Gráficos de Análises")
        janela.geometry("1200x800")
        janela.transient(parent)

        # Notebook para diferentes tipos de gráficos
        notebook = ttk.Notebook(janela)
        notebook.pack(fill='both', expand=True, padx=10, pady=10)

        # Obter dados
        dados_sistema = self.funcoes.obter_dados_legacy()
        relatorio = self.funcoes.calcular_relatorio_completo(dados_sistema)

        # Aba 1: Consumo Anual
        self.criar_aba_grafico_consumo_anual(notebook, relatorio)

        # Aba 2: Percentuais
        self.criar_aba_grafico_percentuais(notebook, relatorio)

        # Aba 3: Balanço Energético
        self.criar_aba_grafico_balanco(notebook, relatorio, dados_sistema)

        # Aba 4: Análise Mensal
        self.criar_aba_analise_mensal(notebook, dados_sistema)

    def criar_aba_grafico_consumo_anual(self, notebook, relatorio: Dict):
        """Cria aba com gráfico de consumo anual"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="📊 Consumo Anual")

        # Frame para controles
        frame_controles = ttk.Frame(frame)
        frame_controles.pack(fill='x', padx=10, pady=5)

        ttk.Label(frame_controles, text="Gráfico de Consumo Anual por Unidade",
                  font=('Arial', 12, 'bold')).pack(side='left')

        # Frame para o gráfico
        frame_grafico = ttk.Frame(frame)
        frame_grafico.pack(fill='both', expand=True, padx=10, pady=10)

        try:
            fig = Figure(figsize=(12, 8), dpi=100)
            ax = fig.add_subplot(111)

            nomes = [u['nome'][:15] + '...' if len(u['nome']) > 15 else u['nome'] for u in relatorio['unidades']]
            consumos = [u['consumo_anual'] for u in relatorio['unidades']]

            # Usar cores do config
            cores = CORES_GRAFICO[:len(nomes)]

            bars = ax.bar(nomes, consumos, color=cores, alpha=0.8)
            ax.set_title('Consumo Anual por Unidade', fontsize=16, fontweight='bold', pad=20)
            ax.set_ylabel('Consumo (kWh)', fontsize=12)
            ax.set_xlabel('Unidades', fontsize=12)

            # Rotacionar labels
            plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

            # Adicionar valores nas barras
            for bar, consumo in zip(bars, consumos):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2., height + height * 0.01,
                        f'{consumo:,.0f}'.replace(',', '.'),
                        ha='center', va='bottom', fontsize=9, fontweight='bold')

            # Melhorar layout
            fig.tight_layout()

            canvas = FigureCanvasTkAgg(fig, frame_grafico)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)

        except Exception as e:
            ttk.Label(frame_grafico, text=f"Erro ao criar gráfico: {e}",
                      font=('Arial', 12)).pack(expand=True)

    def criar_aba_grafico_percentuais(self, notebook, relatorio: Dict):
        """Cria aba com gráfico de percentuais"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="🥧 Percentuais")

        # Frame para controles
        frame_controles = ttk.Frame(frame)
        frame_controles.pack(fill='x', padx=10, pady=5)

        ttk.Label(frame_controles, text="Distribuição Percentual do Consumo",
                  font=('Arial', 12, 'bold')).pack(side='left')

        # Frame para o gráfico
        frame_grafico = ttk.Frame(frame)
        frame_grafico.pack(fill='both', expand=True, padx=10, pady=10)

        try:
            fig = Figure(figsize=(10, 8), dpi=100)
            ax = fig.add_subplot(111)

            # Preparar dados
            nomes = []
            percentuais = []

            for unidade in relatorio['unidades']:
                if unidade['consumo_anual'] > 0:
                    nome = unidade['nome'][:20] + '...' if len(unidade['nome']) > 20 else unidade['nome']
                    nomes.append(nome)
                    percentuais.append(unidade['percentual'])

            # Usar cores do config
            cores = CORES_GRAFICO[:len(nomes)]

            wedges, texts, autotexts = ax.pie(
                percentuais,
                labels=nomes,
                autopct='%1.1f%%',
                colors=cores,
                startangle=90,
                textprops={'fontsize': 10}
            )

            ax.set_title('Distribuição Percentual do Consumo', fontsize=16, fontweight='bold')

            # Melhorar legibilidade
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')
                autotext.set_fontsize(9)

            fig.tight_layout()

            canvas = FigureCanvasTkAgg(fig, frame_grafico)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)

        except Exception as e:
            ttk.Label(frame_grafico, text=f"Erro ao criar gráfico: {e}",
                      font=('Arial', 12)).pack(expand=True)

    def criar_aba_grafico_balanco(self, notebook, relatorio: Dict, dados_sistema: Dict):
        """Cria aba com gráfico de balanço energético"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="⚖️ Balanço")

        # Frame para controles
        frame_controles = ttk.Frame(frame)
        frame_controles.pack(fill='x', padx=10, pady=5)

        eficiencia = self.funcoes.obter_eficiencia_usina_porcentagem(dados_sistema)
        ttk.Label(frame_controles, text=f"Balanço Energético Anual (Eficiência: {eficiencia:.0f}%)",
                  font=('Arial', 12, 'bold')).pack(side='left')

        # Frame para o gráfico
        frame_grafico = ttk.Frame(frame)
        frame_grafico.pack(fill='both', expand=True, padx=10, pady=10)

        try:
            balanco = relatorio['balanco_energetico']

            fig = Figure(figsize=(12, 8), dpi=100)
            ax = fig.add_subplot(111)

            categorias = ['Geração\nNominal', 'Geração\nReal', 'Consumo\nUnidades', 'Tarifas\nMínimas', 'Saldo\nFinal']
            valores = [
                balanco['geracao_anual_nominal'],
                balanco['geracao_anual_real'],
                -balanco['consumo_anual'],  # Negativo para mostrar como saída
                -balanco['tarifas_anuais'],  # Negativo para mostrar como saída
                balanco['saldo_anual']
            ]

            cores = ['lightgreen', 'green', 'red', 'orange', 'green' if valores[-1] > 0 else 'red']

            bars = ax.bar(categorias, valores, color=cores, alpha=0.7, edgecolor='black', linewidth=1)
            ax.set_title(f'Balanço Energético Anual (Eficiência: {eficiencia:.0f}%)',
                         fontsize=16, fontweight='bold', pad=20)
            ax.set_ylabel('Energia (kWh)', fontsize=12)
            ax.axhline(y=0, color='black', linestyle='-', linewidth=1)

            # Adicionar valores nas barras
            for bar, valor in zip(bars, valores):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2.,
                        height + (abs(height) * 0.02 if height > 0 else -abs(height) * 0.02),
                        f'{valor:,.0f}'.replace(',', '.'),
                        ha='center',
                        va='bottom' if height > 0 else 'top',
                        fontsize=11, fontweight='bold')

            fig.tight_layout()

            canvas = FigureCanvasTkAgg(fig, frame_grafico)
            canvas.draw()
            canvas.get_tk_widget().pack(fill='both', expand=True)

        except Exception as e:
            ttk.Label(frame_grafico, text=f"Erro ao criar gráfico: {e}",
                      font=('Arial', 12)).pack(expand=True)

    def criar_aba_analise_mensal(self, notebook, dados_sistema: Dict):
        """Cria aba com análise mensal interativa"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="📅 Análise Mensal")

        # Frame para controles
        frame_controles = ttk.LabelFrame(frame, text="Controles", padding=10)
        frame_controles.pack(fill='x', padx=10, pady=5)

        # Seleção de mês
        ttk.Label(frame_controles, text="Selecionar Mês:").grid(row=0, column=0, sticky='w', padx=5)

        mes_var = tk.StringVar(value="Janeiro")
        combo_mes = ttk.Combobox(frame_controles, textvariable=mes_var,
                                 values=self.meses_completos + ["Resultado Anual"],
                                 state="readonly", width=15)
        combo_mes.grid(row=0, column=1, padx=10)

        # Frame para o gráfico
        frame_grafico = ttk.Frame(frame)
        frame_grafico.pack(fill='both', expand=True, padx=10, pady=10)

        # Função para atualizar gráfico
        def atualizar_grafico_mensal():
            # Limpar frame
            for widget in frame_grafico.winfo_children():
                widget.destroy()

            mes_selecionado = mes_var.get()

            try:
                # Calcular percentuais
                percentuais = self.funcoes.calcular_porcentagens_em_relacao_usina(dados_sistema, mes_selecionado)

                if percentuais:
                    fig, canvas = self.criar_grafico_base(frame_grafico, f'Distribuição - {mes_selecionado}')
                    if fig and canvas:
                        self.atualizar_grafico_pizza(fig, canvas, percentuais, f'Distribuição - {mes_selecionado}')
                else:
                    ttk.Label(frame_grafico, text="Nenhum dado disponível para este mês",
                              font=('Arial', 12)).pack(expand=True)

            except Exception as e:
                ttk.Label(frame_grafico, text=f"Erro: {e}",
                          font=('Arial', 12)).pack(expand=True)

        # Botão para atualizar
        ttk.Button(frame_controles, text="📊 Atualizar Gráfico",
                   command=atualizar_grafico_mensal).grid(row=0, column=2, padx=10)

        # Carregar gráfico inicial
        atualizar_grafico_mensal()

        # Bind para atualizar automaticamente
        combo_mes.bind('<<ComboboxSelected>>', lambda e: atualizar_grafico_mensal())


# ========== FUNÇÕES DE COMPATIBILIDADE ==========

def criar_grafico_compativel(parent):
    """Função de compatibilidade para criar gráfico"""
    try:
        from utilitarios.funcoes_legacy import obter_funcoes_legacy
        funcoes = obter_funcoes_legacy()
        graficos = GraficosLegacy(funcoes)
        return graficos.criar_grafico_base(parent)
    except Exception as e:
        print(f"❌ Erro ao criar gráfico compatível: {e}")
        return None, None


def mostrar_grafico_distribuicao_compativel(parent, dados_sistema, calculadora, mes_index):
    """Função de compatibilidade para mostrar gráfico de distribuição"""
    try:
        from utilitarios.funcoes_legacy import obter_funcoes_legacy
        funcoes = obter_funcoes_legacy()
        graficos = GraficosLegacy(funcoes)

        # Converter índice para nome do mês
        meses = [
            "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro",
            "Resultado Anual"
        ]

        mes_nome = meses[mes_index] if mes_index < len(meses) else "Janeiro"
        graficos.mostrar_grafico_distribuicao(parent, mes_nome)

    except Exception as e:
        print(f"❌ Erro ao mostrar gráfico: {e}")


def criar_janela_graficos_analises_compativel(parent, dados_sistema):
    """Função de compatibilidade para criar janela de análises"""
    try:
        from utilitarios.funcoes_legacy import obter_funcoes_legacy
        funcoes = obter_funcoes_legacy()
        graficos = GraficosLegacy(funcoes)
        graficos.criar_janela_graficos_analises(parent)

    except Exception as e:
        print(f"❌ Erro ao criar janela de análises: {e}")