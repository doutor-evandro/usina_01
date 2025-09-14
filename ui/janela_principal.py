"""
Janela Principal - Dashboard e Configurações
Sistema de Energia Solar v2.0
"""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import os
import sys

# Adicionar path do projeto
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import SistemaEnergiaSolar
from utilitarios.formatadores import formatar_moeda, formatar_energia, formatar_percentual


class InterfacePrincipal:
    """Interface principal com dashboard e configurações"""

    def __init__(self):
        print("🖼️ Iniciando Dashboard...")

        # Inicializar variáveis
        self.root = tk.Tk()
        self.sistema = None
        self.canvas_grafico = None
        self.figura_atual = None

        # Configurar janela principal
        self.configurar_janela()

        # Criar sistema
        if not self.inicializar_sistema():
            return

        # Criar interface
        self.criar_interface()

        # Atualizar dados iniciais
        self.atualizar_dados()

        print("✅ Dashboard criado com sucesso!")

    def configurar_janela(self):
        """Configura a janela principal"""
        self.root.title("Sistema de Energia Solar - Dashboard v2.0")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 600)

        # Cores personalizadas
        self.cores = {
            'primaria': '#2E86AB',
            'secundaria': '#A23B72',
            'sucesso': '#F18F01',
            'fundo': '#F5F5F5',
            'texto': '#2C3E50'
        }

    def inicializar_sistema(self):
        """Inicializa o sistema de energia solar"""
        try:
            self.sistema = SistemaEnergiaSolar()
            print("✅ Sistema inicializado com sucesso!")
            return True

        except Exception as e:
            print(f"❌ Erro ao inicializar sistema: {e}")
            messagebox.showerror("Erro", f"Erro ao inicializar sistema: {e}")
            self.root.destroy()
            return False

    def criar_interface(self):
        """Cria toda a interface gráfica"""
        # Frame principal
        self.frame_principal = ttk.Frame(self.root)
        self.frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Criar notebook (abas)
        self.notebook = ttk.Notebook(self.frame_principal)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # ⭐ NOVA ORDEM DOS MENUS CONFORME SOLICITADO:
        # 📊 Dashboard | 💰 Faturamento | 💳 Créditos | 🏠 Unidades | 📋 Relatórios | ⚙️ Config
        self.criar_aba_dashboard()      # 1º - 📊 Dashboard
        self.criar_aba_faturamento()    # 2º - 💰 Faturamento (NOVO)
        self.criar_aba_creditos()       # 3º - 💳 Créditos (NOVO)
        self.criar_aba_unidades()       # 4º - 🏠 Unidades (NOVO)
        self.criar_aba_relatorios()     # 5º - 📋 Relatórios
        self.criar_aba_configuracoes()  # 6º - ⚙️ Config (renomeado)

        # Menu superior
        self.criar_menu()

        # Barra de status
        self.criar_barra_status()

    def criar_menu(self):
        """Cria o menu superior"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Menu Arquivo
        menu_arquivo = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=menu_arquivo)
        menu_arquivo.add_command(label="Atualizar Dados", command=self.atualizar_dados)
        menu_arquivo.add_separator()
        menu_arquivo.add_command(label="Sair", command=self.root.quit)

        # Menu Análises
        menu_analises = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Análises", menu=menu_analises)
        menu_analises.add_command(label="🔬 Abrir Análises Avançadas", command=self.abrir_janela_analises)

        # Menu Ajuda
        menu_ajuda = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ajuda", menu=menu_ajuda)
        menu_ajuda.add_command(label="Sobre", command=self.mostrar_sobre)

    def criar_aba_dashboard(self):
        """Cria a aba do dashboard principal"""
        frame_dashboard = ttk.Frame(self.notebook)
        self.notebook.add(frame_dashboard, text="📊 Dashboard")

        # Frame superior - Indicadores
        frame_indicadores = ttk.LabelFrame(frame_dashboard, text="Indicadores Principais", padding=10)
        frame_indicadores.pack(fill=tk.X, padx=5, pady=5)

        self.criar_indicadores(frame_indicadores)

        # Frame central - Gráfico principal
        frame_grafico = ttk.LabelFrame(frame_dashboard, text="Análise Mensal", padding=10)
        frame_grafico.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.criar_grafico_principal(frame_grafico)

        # Frame inferior - Resumo rápido
        frame_resumo = ttk.LabelFrame(frame_dashboard, text="Resumo do Sistema", padding=10)
        frame_resumo.pack(fill=tk.X, padx=5, pady=5)

        self.criar_resumo_rapido(frame_resumo)

    def criar_aba_faturamento(self):
        """Cria a aba de faturamento (NOVA)"""
        frame_faturamento = ttk.Frame(self.notebook)
        self.notebook.add(frame_faturamento, text="💰 Faturamento")

        # Frame principal do faturamento
        frame_principal_fat = ttk.LabelFrame(frame_faturamento, text="Gestão de Faturamento", padding=20)
        frame_principal_fat.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Título da seção
        ttk.Label(frame_principal_fat, text="💰 MÓDULO DE FATURAMENTO",
                 font=('Arial', 16, 'bold')).pack(pady=20)

        # Frame para resumo financeiro
        frame_resumo_fat = ttk.LabelFrame(frame_principal_fat, text="Resumo Financeiro Mensal", padding=10)
        frame_resumo_fat.pack(fill=tk.X, pady=10)

        # Cards de faturamento
        frame_cards_fat = ttk.Frame(frame_resumo_fat)
        frame_cards_fat.pack(fill=tk.X)

        for i in range(4):
            frame_cards_fat.columnconfigure(i, weight=1)

        # Cards financeiros
        self.card_receita = self.criar_card(frame_cards_fat, "Receita Mensal", "R$ 0,00", self.cores['sucesso'], 0, 0)
        self.card_economia_fat = self.criar_card(frame_cards_fat, "Economia Gerada", "R$ 0,00", self.cores['primaria'], 0, 1)
        self.card_creditos_fat = self.criar_card(frame_cards_fat, "Créditos Ativos", "0 kWh", self.cores['secundaria'], 0, 2)
        self.card_faturamento_anual = self.criar_card(frame_cards_fat, "Faturamento Anual", "R$ 0,00", "#28A745", 0, 3)

        # Área de controles de faturamento
        frame_controles_fat = ttk.LabelFrame(frame_principal_fat, text="Controles de Faturamento", padding=10)
        frame_controles_fat.pack(fill=tk.X, pady=10)

        ttk.Button(frame_controles_fat, text="📊 Gerar Fatura Mensal",
                  command=self.gerar_fatura_mensal).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_controles_fat, text="📋 Relatório Financeiro",
                  command=self.relatorio_financeiro).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_controles_fat, text="💾 Exportar Dados",
                  command=self.exportar_faturamento).pack(side=tk.LEFT, padx=5)

        # Área de informações detalhadas
        frame_detalhes_fat = ttk.LabelFrame(frame_principal_fat, text="Detalhes Financeiros", padding=10)
        frame_detalhes_fat.pack(fill=tk.BOTH, expand=True, pady=10)

        # Text widget para mostrar detalhes
        self.text_faturamento = tk.Text(frame_detalhes_fat, wrap=tk.WORD, font=('Courier', 10), height=8)
        scroll_fat = ttk.Scrollbar(frame_detalhes_fat, orient=tk.VERTICAL, command=self.text_faturamento.yview)
        self.text_faturamento.configure(yscrollcommand=scroll_fat.set)

        self.text_faturamento.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_fat.pack(side=tk.RIGHT, fill=tk.Y)

        # Carregar dados iniciais do faturamento
        self.carregar_dados_faturamento()

    def criar_aba_creditos(self):
        """Cria a aba de créditos (NOVA)"""
        frame_creditos = ttk.Frame(self.notebook)
        self.notebook.add(frame_creditos, text="💳 Créditos")

        # Frame principal dos créditos
        frame_principal_cred = ttk.LabelFrame(frame_creditos, text="Gestão de Créditos Energéticos", padding=20)
        frame_principal_cred.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Título
        ttk.Label(frame_principal_cred, text="💳 SISTEMA DE CRÉDITOS ENERGÉTICOS",
                 font=('Arial', 16, 'bold')).pack(pady=20)

        # Frame para saldo de créditos
        frame_saldo_cred = ttk.LabelFrame(frame_principal_cred, text="Saldo de Créditos", padding=10)
        frame_saldo_cred.pack(fill=tk.X, pady=10)

        # Cards de créditos
        frame_cards_cred = ttk.Frame(frame_saldo_cred)
        frame_cards_cred.pack(fill=tk.X)

        for i in range(4):
            frame_cards_cred.columnconfigure(i, weight=1)

        # Cards de créditos
        self.card_creditos_total = self.criar_card(frame_cards_cred, "Créditos Totais", "0 kWh", self.cores['primaria'], 0, 0)
        self.card_creditos_mes = self.criar_card(frame_cards_cred, "Créditos do Mês", "0 kWh", self.cores['sucesso'], 0, 1)
        self.card_creditos_utilizados = self.criar_card(frame_cards_cred, "Créditos Utilizados", "0 kWh", self.cores['secundaria'], 0, 2)
        self.card_validade_creditos = self.criar_card(frame_cards_cred, "Próximo Vencimento", "-- meses", "#6F42C1", 0, 3)

        # Controles de créditos
        frame_controles_cred = ttk.LabelFrame(frame_principal_cred, text="Controles de Créditos", padding=10)
        frame_controles_cred.pack(fill=tk.X, pady=10)

        ttk.Button(frame_controles_cred, text="📊 Histórico de Créditos",
                  command=self.historico_creditos).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_controles_cred, text="⚡ Simular Consumo",
                  command=self.simular_consumo_creditos).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_controles_cred, text="📋 Relatório de Créditos",
                  command=self.relatorio_creditos).pack(side=tk.LEFT, padx=5)

        # Área de detalhes dos créditos
        frame_detalhes_cred = ttk.LabelFrame(frame_principal_cred, text="Detalhes dos Créditos", padding=10)
        frame_detalhes_cred.pack(fill=tk.BOTH, expand=True, pady=10)

        # Text widget para mostrar detalhes
        self.text_creditos = tk.Text(frame_detalhes_cred, wrap=tk.WORD, font=('Courier', 10), height=8)
        scroll_cred = ttk.Scrollbar(frame_detalhes_cred, orient=tk.VERTICAL, command=self.text_creditos.yview)
        self.text_creditos.configure(yscrollcommand=scroll_cred.set)

        self.text_creditos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_cred.pack(side=tk.RIGHT, fill=tk.Y)

        # Carregar dados iniciais dos créditos
        self.carregar_dados_creditos()

    def criar_aba_unidades(self):
        """Cria a aba de unidades (NOVA)"""
        frame_unidades = ttk.Frame(self.notebook)
        self.notebook.add(frame_unidades, text="🏠 Unidades")

        # Frame principal das unidades
        frame_principal_uni = ttk.LabelFrame(frame_unidades, text="Gestão de Unidades Consumidoras", padding=20)
        frame_principal_uni.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Título
        ttk.Label(frame_principal_uni, text="🏠 UNIDADES CONSUMIDORAS",
                 font=('Arial', 16, 'bold')).pack(pady=20)

        # Frame para resumo das unidades
        frame_resumo_uni = ttk.LabelFrame(frame_principal_uni, text="Resumo das Unidades", padding=10)
        frame_resumo_uni.pack(fill=tk.X, pady=10)

        # Cards de unidades
        frame_cards_uni = ttk.Frame(frame_resumo_uni)
        frame_cards_uni.pack(fill=tk.X)

        for i in range(4):
            frame_cards_uni.columnconfigure(i, weight=1)

        # Cards das unidades
        self.card_unidades_ativas = self.criar_card(frame_cards_uni, "Unidades Ativas", "0", self.cores['sucesso'], 0, 0)
        self.card_unidades_total = self.criar_card(frame_cards_uni, "Total de Unidades", "0", self.cores['primaria'], 0, 1)
        self.card_consumo_medio = self.criar_card(frame_cards_uni, "Consumo Médio", "0 kWh", self.cores['secundaria'], 0, 2)
        self.card_maior_consumidor = self.criar_card(frame_cards_uni, "Maior Consumidor", "-- kWh", "#28A745", 0, 3)

        # Controles das unidades
        frame_controles_uni = ttk.LabelFrame(frame_principal_uni, text="Controles das Unidades", padding=10)
        frame_controles_uni.pack(fill=tk.X, pady=10)

        ttk.Button(frame_controles_uni, text="➕ Adicionar Unidade",
                  command=self.adicionar_unidade).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_controles_uni, text="✏️ Editar Unidade",
                  command=self.editar_unidade).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_controles_uni, text="📊 Análise Detalhada",
                  command=self.analise_unidades).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_controles_uni, text="📋 Lista Completa",
                  command=self.listar_unidades).pack(side=tk.LEFT, padx=5)

        # Lista de unidades
        frame_lista_uni = ttk.LabelFrame(frame_principal_uni, text="Lista de Unidades", padding=10)
        frame_lista_uni.pack(fill=tk.BOTH, expand=True, pady=10)

        # Treeview para listar unidades
        columns = ('Código', 'Nome', 'Tipo', 'Status', 'Consumo Mensal')
        self.tree_unidades = ttk.Treeview(frame_lista_uni, columns=columns, show='headings', height=8)

        for col in columns:
            self.tree_unidades.heading(col, text=col)
            self.tree_unidades.column(col, width=120)

        # Scrollbar para a lista
        scroll_uni = ttk.Scrollbar(frame_lista_uni, orient=tk.VERTICAL, command=self.tree_unidades.yview)
        self.tree_unidades.configure(yscrollcommand=scroll_uni.set)

        self.tree_unidades.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_uni.pack(side=tk.RIGHT, fill=tk.Y)

        # Carregar dados iniciais das unidades
        self.carregar_dados_unidades()

    def criar_aba_relatorios(self):
        """Cria a aba de relatórios"""
        frame_relatorios = ttk.Frame(self.notebook)
        self.notebook.add(frame_relatorios, text="📋 Relatórios")

        # Frame superior - Opções de relatório
        frame_opcoes = ttk.LabelFrame(frame_relatorios, text="Gerar Relatórios", padding=10)
        frame_opcoes.pack(fill=tk.X, padx=10, pady=5)

        # Seleção de ano
        ttk.Label(frame_opcoes, text="Ano:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.var_ano_relatorio = tk.IntVar(value=datetime.now().year)
        self.spin_ano = ttk.Spinbox(frame_opcoes, from_=2020, to=2030, textvariable=self.var_ano_relatorio, width=10)
        self.spin_ano.grid(row=0, column=1, padx=10, pady=5)

        # Botões de relatório
        frame_botoes_rel = ttk.Frame(frame_opcoes)
        frame_botoes_rel.grid(row=1, column=0, columnspan=2, pady=10)

        ttk.Button(frame_botoes_rel, text="📊 Relatório Completo",
                   command=self.gerar_relatorio_completo).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botoes_rel, text="📋 Relatório Resumido",
                   command=self.gerar_relatorio_resumido).pack(side=tk.LEFT, padx=5)

        # Frame central - Visualização do relatório
        frame_visualizacao = ttk.LabelFrame(frame_relatorios, text="Visualização", padding=10)
        frame_visualizacao.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Text widget com scroll
        self.text_relatorio = tk.Text(frame_visualizacao, wrap=tk.WORD, font=('Courier', 10))
        scroll_relatorio = ttk.Scrollbar(frame_visualizacao, orient=tk.VERTICAL, command=self.text_relatorio.yview)
        self.text_relatorio.configure(yscrollcommand=scroll_relatorio.set)

        self.text_relatorio.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_relatorio.pack(side=tk.RIGHT, fill=tk.Y)

    def criar_aba_configuracoes(self):
        """Cria a aba de configurações (RENOMEADA para Config)"""
        frame_config = ttk.Frame(self.notebook)
        self.notebook.add(frame_config, text="⚙️ Config")  # ⭐ RENOMEADO

        # Configurações do Sistema
        frame_sistema = ttk.LabelFrame(frame_config, text="Configurações do Sistema", padding=20)
        frame_sistema.pack(fill=tk.X, padx=20, pady=20)

        # Potência
        ttk.Label(frame_sistema, text="Potência Instalada (kW):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.var_potencia = tk.DoubleVar()
        self.entry_potencia = ttk.Entry(frame_sistema, textvariable=self.var_potencia, width=15)
        self.entry_potencia.grid(row=0, column=1, padx=10, pady=5)

        # Eficiência
        ttk.Label(frame_sistema, text="Eficiência do Sistema (%):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.var_eficiencia = tk.DoubleVar()
        self.entry_eficiencia = ttk.Entry(frame_sistema, textvariable=self.var_eficiencia, width=15)
        self.entry_eficiencia.grid(row=1, column=1, padx=10, pady=5)

        # Tarifa
        ttk.Label(frame_sistema, text="Tarifa de Energia (R$/kWh):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.var_tarifa = tk.DoubleVar()
        self.entry_tarifa = ttk.Entry(frame_sistema, textvariable=self.var_tarifa, width=15)
        self.entry_tarifa.grid(row=2, column=1, padx=10, pady=5)

        # Investimento
        ttk.Label(frame_sistema, text="Custo do Investimento (R$):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.var_investimento = tk.DoubleVar()
        self.entry_investimento = ttk.Entry(frame_sistema, textvariable=self.var_investimento, width=15)
        self.entry_investimento.grid(row=3, column=1, padx=10, pady=5)

        # Botões
        frame_botoes_config = ttk.Frame(frame_sistema)
        frame_botoes_config.grid(row=4, column=0, columnspan=2, pady=10)

        ttk.Button(frame_botoes_config, text="💾 Salvar Configurações",
                   command=self.salvar_configuracoes).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botoes_config, text="🔄 Restaurar Padrão",
                   command=self.restaurar_configuracoes).pack(side=tk.LEFT, padx=5)

    # ========== MÉTODOS AUXILIARES (mantidos iguais) ==========

    def criar_indicadores(self, parent):
        """Cria os indicadores principais"""
        # Frame para os cards
        frame_cards = ttk.Frame(parent)
        frame_cards.pack(fill=tk.X)

        # Configurar grid
        for i in range(5):
            frame_cards.columnconfigure(i, weight=1)

        # Cards
        self.card_geracao = self.criar_card(frame_cards, "Geração Anual", "0 kWh", self.cores['primaria'], 0, 0)
        self.card_consumo = self.criar_card(frame_cards, "Consumo Anual", "0 kWh", self.cores['secundaria'], 0, 1)
        self.card_economia = self.criar_card(frame_cards, "Economia Anual", "R$ 0,00", self.cores['sucesso'], 0, 2)
        self.card_payback = self.criar_card(frame_cards, "Payback", "0 anos", "#28A745", 0, 3)
        self.card_roi = self.criar_card(frame_cards, "ROI (25 anos)", "0%", "#6F42C1", 0, 4)

    def criar_card(self, parent, titulo, valor, cor, row, col):
        """Cria um card de indicador"""
        frame_card = ttk.Frame(parent, relief=tk.RAISED, borderwidth=1)
        frame_card.grid(row=row, column=col, padx=5, pady=5, sticky="ew")

        # Título
        label_titulo = ttk.Label(frame_card, text=titulo, font=('Arial', 10, 'bold'))
        label_titulo.pack(pady=(10, 5))

        # Valor
        label_valor = ttk.Label(frame_card, text=valor, font=('Arial', 14, 'bold'), foreground=cor)
        label_valor.pack(pady=(0, 10))

        return label_valor

    def criar_grafico_principal(self, parent):
        """Cria o gráfico principal do dashboard"""
        # Frame para controles
        frame_controles = ttk.Frame(parent)
        frame_controles.pack(fill=tk.X, pady=(0, 10))

        # Combobox para tipo de gráfico
        ttk.Label(frame_controles, text="Tipo de Gráfico:").pack(side=tk.LEFT, padx=(0, 5))

        self.combo_grafico = ttk.Combobox(frame_controles, values=[
            "Geração vs Consumo",
            "Economia Mensal",
            "Saldo Energético"
        ], state="readonly", width=20)
        self.combo_grafico.pack(side=tk.LEFT, padx=(0, 10))
        self.combo_grafico.set("Geração vs Consumo")
        self.combo_grafico.bind('<<ComboboxSelected>>', self.atualizar_grafico)

        # Botão atualizar
        ttk.Button(frame_controles, text="🔄 Atualizar", command=self.atualizar_grafico).pack(side=tk.LEFT)

        # Frame para o gráfico
        self.frame_grafico = ttk.Frame(parent)
        self.frame_grafico.pack(fill=tk.BOTH, expand=True)

        # Criar gráfico inicial
        self.criar_grafico_inicial()

    def criar_grafico_inicial(self):
        """Cria o gráfico inicial"""
        try:
            # Criar figura
            self.figura_atual = plt.Figure(figsize=(10, 5), dpi=100)
            ax = self.figura_atual.add_subplot(111)

            # Dados de exemplo
            meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
                     'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

            tipo = self.combo_grafico.get()

            if tipo == "Geração vs Consumo":
                geracao_mensal = [15162, 12453, 12500, 10423, 9002, 6675, 8197, 9954, 11561, 13234, 14000, 14606]
                consumo_mensal = [8800] * 12

                ax.bar([i - 0.2 for i in range(len(meses))], geracao_mensal, 0.4,
                       label='Geração', color=self.cores['primaria'], alpha=0.8)
                ax.bar([i + 0.2 for i in range(len(meses))], consumo_mensal, 0.4,
                       label='Consumo', color=self.cores['secundaria'], alpha=0.8)

                ax.set_ylabel('Energia (kWh)')
                ax.set_title('Geração vs Consumo Mensal')
                ax.legend()

            elif tipo == "Economia Mensal":
                economia = [4000, 3200, 3250, 2800, 2400, 1800, 2200, 2650, 3100, 3550, 3750, 3900]

                ax.plot(meses, economia, marker='o', linewidth=2,
                        color=self.cores['sucesso'], markersize=8)
                ax.fill_between(meses, economia, alpha=0.3, color=self.cores['sucesso'])

                ax.set_ylabel('Economia (R$)')
                ax.set_title('Economia Mensal Estimada')

            else:  # Saldo Energético
                saldo = [6362, 3653, 3700, 1623, 202, -2125, -603, 1154, 2761, 4434, 5200, 5806]

                cores_saldo = ['green' if s >= 0 else 'red' for s in saldo]
                ax.bar(meses, saldo, color=cores_saldo, alpha=0.7)

                ax.set_ylabel('Saldo (kWh)')
                ax.set_title('Saldo Energético Mensal')
                ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)

            ax.set_xlabel('Meses')
            ax.set_xticks(range(len(meses)))
            ax.set_xticklabels(meses)
            ax.grid(True, alpha=0.3)

            # Limpar canvas anterior
            if self.canvas_grafico:
                self.canvas_grafico.get_tk_widget().destroy()
                self.canvas_grafico = None

            # Adicionar novo canvas
            self.canvas_grafico = FigureCanvasTkAgg(self.figura_atual, self.frame_grafico)
            self.canvas_grafico.draw()
            self.canvas_grafico.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        except Exception as e:
            print(f"Erro ao criar gráfico: {e}")

    def criar_resumo_rapido(self, parent):
        """Cria resumo rápido do sistema"""
        # Frame com informações básicas
        frame_info = ttk.Frame(parent)
        frame_info.pack(fill=tk.X)

        # Informações em colunas
        ttk.Label(frame_info, text="🔋 Potência:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, padx=5)
        self.label_potencia = ttk.Label(frame_info, text="92.0 kW")
        self.label_potencia.grid(row=0, column=1, sticky=tk.W, padx=5)

        ttk.Label(frame_info, text="🏠 Unidades Ativas:", font=('Arial', 10, 'bold')).grid(row=0, column=2, sticky=tk.W,
                                                                                          padx=20)
        self.label_unidades = ttk.Label(frame_info, text="9 unidades")
        self.label_unidades.grid(row=0, column=3, sticky=tk.W, padx=5)

        ttk.Label(frame_info, text="💰 Investimento:", font=('Arial', 10, 'bold')).grid(row=0, column=4, sticky=tk.W,
                                                                                       padx=20)
        self.label_investimento = ttk.Label(frame_info, text="R$ 450.000,00")
        self.label_investimento.grid(row=0, column=5, sticky=tk.W, padx=5)

    def criar_barra_status(self):
        """Cria a barra de status"""
        self.barra_status = ttk.Frame(self.root)
        self.barra_status.pack(fill=tk.X, side=tk.BOTTOM)

        # Labels de status
        self.label_status = ttk.Label(self.barra_status, text="Sistema carregado", relief=tk.SUNKEN)
        self.label_status.pack(side=tk.LEFT, padx=5, pady=2)

        self.label_data = ttk.Label(self.barra_status, text=f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
                                    relief=tk.SUNKEN)
        self.label_data.pack(side=tk.RIGHT, padx=5, pady=2)

    # ========== NOVOS MÉTODOS PARA AS NOVAS ABAS ==========

    def carregar_dados_faturamento(self):
        """Carrega dados iniciais do faturamento"""
        try:
            # Dados simulados para demonstração
            dados_faturamento = """RESUMO FINANCEIRO MENSAL
=============================

💰 RECEITAS:
- Economia gerada: R$ 8.500,00
- Créditos utilizados: R$ 2.300,00
- Total mensal: R$ 10.800,00

📊 ANÁLISE:
- Economia vs mês anterior: +12%
- Projeção anual: R$ 129.600,00
- ROI acumulado: 18.5%

📋 PRÓXIMAS AÇÕES:
- Revisão tarifária: 15/12/2024
- Análise de créditos: Mensal
- Relatório anual: Janeiro/2025
"""
            self.text_faturamento.delete(1.0, tk.END)
            self.text_faturamento.insert(1.0, dados_faturamento)

            # Atualizar cards
            self.card_receita.config(text="R$ 10.800,00")
            self.card_economia_fat.config(text="R$ 8.500,00")
            self.card_creditos_fat.config(text="2.300 kWh")
            self.card_faturamento_anual.config(text="R$ 129.600,00")

        except Exception as e:
            print(f"Erro ao carregar dados de faturamento: {e}")

    def carregar_dados_creditos(self):
        """Carrega dados iniciais dos créditos"""
        try:
            # Dados simulados para demonstração
            dados_creditos = """SISTEMA DE CRÉDITOS ENERGÉTICOS
=================================

💳 SALDO ATUAL:
- Créditos disponíveis: 15.420 kWh
- Créditos gerados este mês: 3.200 kWh
- Créditos utilizados: 1.850 kWh
- Saldo líquido: +1.350 kWh

⏰ VALIDADE:
- Próximo vencimento: 8 meses
- Créditos a vencer: 2.100 kWh
- Recomendação: Utilizar prioritariamente

�� HISTÓRICO:
- Janeiro: +2.800 kWh
- Fevereiro: +3.100 kWh
- Março: +3.200 kWh (atual)
"""
            self.text_creditos.delete(1.0, tk.END)
            self.text_creditos.insert(1.0, dados_creditos)

            # Atualizar cards
            self.card_creditos_total.config(text="15.420 kWh")
            self.card_creditos_mes.config(text="3.200 kWh")
            self.card_creditos_utilizados.config(text="1.850 kWh")
            self.card_validade_creditos.config(text="8 meses")

        except Exception as e:
            print(f"Erro ao carregar dados de créditos: {e}")

    def carregar_dados_unidades(self):
        """Carrega dados iniciais das unidades"""
        try:
            # Limpar lista atual
            for item in self.tree_unidades.get_children():
                self.tree_unidades.delete(item)

            # Dados simulados das unidades
            unidades_exemplo = [
                ('112761577', 'Lanchonet', 'Trifásico', '✅ Ativa', '1.739 kWh'),
                ('114789592', 'My Beach', 'Trifásico', '✅ Ativa', '500 kWh'),
                ('104567890', 'Loja Centro', 'Trifásico', '✅ Ativa', '1.454 kWh'),
                ('105123456', 'Sobreloja', 'Monofásico', '✅ Ativa', '850 kWh'),
                ('106789012', 'Escritório', 'Bifásico', '❌ Inativa', '0 kWh')
            ]

            for unidade in unidades_exemplo:
                self.tree_unidades.insert('', tk.END, values=unidade)

            # Atualizar cards
            unidades_ativas = len([u for u in unidades_exemplo if '✅' in u[3]])
            total_unidades = len(unidades_exemplo)
            consumo_medio = sum([int(u[4].split()[0].replace('.', '')) for u in unidades_exemplo if '✅' in u[3]]) / unidades_ativas

            self.card_unidades_ativas.config(text=str(unidades_ativas))
            self.card_unidades_total.config(text=str(total_unidades))
            self.card_consumo_medio.config(text=f"{consumo_medio:.0f} kWh")
            self.card_maior_consumidor.config(text="1.739 kWh")

        except Exception as e:
            print(f"Erro ao carregar dados de unidades: {e}")

    # ========== MÉTODOS DE AÇÃO DAS NOVAS ABAS ==========

    def gerar_fatura_mensal(self):
        """Gera fatura mensal"""
        messagebox.showinfo("Faturamento", "Funcionalidade de fatura mensal em desenvolvimento...")

    def relatorio_financeiro(self):
        """Gera relatório financeiro"""
        messagebox.showinfo("Faturamento", "Relatório financeiro em desenvolvimento...")

    def exportar_faturamento(self):
        """Exporta dados de faturamento"""
        messagebox.showinfo("Faturamento", "Exportação de faturamento em desenvolvimento...")

    def historico_creditos(self):
        """Mostra histórico de créditos"""
        messagebox.showinfo("Créditos", "Histórico de créditos em desenvolvimento...")

    def simular_consumo_creditos(self):
        """Simula consumo de créditos"""
        messagebox.showinfo("Créditos", "Simulação de consumo em desenvolvimento...")

    def relatorio_creditos(self):
        """Gera relatório de créditos"""
        messagebox.showinfo("Créditos", "Relatório de créditos em desenvolvimento...")

    def adicionar_unidade(self):
        """Adiciona nova unidade"""
        messagebox.showinfo("Unidades", "Adição de unidade em desenvolvimento...")

    def editar_unidade(self):
        """Edita unidade existente"""
        messagebox.showinfo("Unidades", "Edição de unidade em desenvolvimento...")

    def analise_unidades(self):
        """Análise detalhada das unidades"""
        messagebox.showinfo("Unidades", "Análise detalhada em desenvolvimento...")

    def listar_unidades(self):
        """Lista todas as unidades"""
        messagebox.showinfo("Unidades", "Listagem completa em desenvolvimento...")

    # ========== MÉTODOS EXISTENTES (mantidos iguais) ==========

    def atualizar_dados(self):
        """Atualiza todos os dados da interface"""
        try:
            # Carregar configurações atuais
            config = self.sistema.sistema.configuracao

            self.var_potencia.set(config.potencia_instalada_kw)
            self.var_eficiencia.set(config.eficiencia_sistema * 100)
            self.var_tarifa.set(config.tarifa_energia_kwh)
            self.var_investimento.set(config.custo_investimento)

            # Atualizar indicadores
            self.atualizar_indicadores()

            # Atualizar resumo
            self.atualizar_resumo()

            # Atualizar dados das novas abas
            self.carregar_dados_faturamento()
            self.carregar_dados_creditos()
            self.carregar_dados_unidades()

            # Atualizar status
            self.label_status.config(text="Dados atualizados com sucesso")

        except Exception as e:
            print(f"Erro ao atualizar dados: {e}")

    def atualizar_indicadores(self):
        """Atualiza os indicadores do dashboard"""
        try:
            resultados = self.sistema.calcular_resultados_anuais(2024)

            if resultados:
                energia = resultados['energia']
                financeiro = resultados['financeiro']

                self.card_geracao.config(text=formatar_energia(energia['geracao_total']))
                self.card_consumo.config(text=formatar_energia(energia['consumo_total']))
                self.card_economia.config(text=formatar_moeda(financeiro['economia_total']))
                self.card_payback.config(text=f"{financeiro['payback_anos']:.1f} anos")
                self.card_roi.config(text=formatar_percentual(financeiro['roi_percentual']))

        except Exception as e:
            print(f"Erro ao atualizar indicadores: {e}")

    def atualizar_resumo(self):
        """Atualiza o resumo rápido"""
        try:
            config = self.sistema.sistema.configuracao
            unidades_ativas = len(self.sistema.sistema.get_unidades_ativas())

            self.label_potencia.config(text=f"{config.potencia_instalada_kw:.1f} kW")
            self.label_unidades.config(text=f"{unidades_ativas} unidades")
            self.label_investimento.config(text=formatar_moeda(config.custo_investimento))

        except Exception as e:
            print(f"Erro ao atualizar resumo: {e}")

    def atualizar_grafico(self, event=None):
        """Atualiza o gráfico principal"""
        self.criar_grafico_inicial()

    def salvar_configuracoes(self):
        """Salva as configurações do sistema"""
        try:
            config = self.sistema.sistema.configuracao

            config.potencia_instalada_kw = self.var_potencia.get()
            config.eficiencia_sistema = self.var_eficiencia.get() / 100
            config.tarifa_energia_kwh = self.var_tarifa.get()
            config.custo_investimento = self.var_investimento.get()

            self.atualizar_dados()
            messagebox.showinfo("Sucesso", "Configurações salvas com sucesso!")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar configurações: {e}")

    def restaurar_configuracoes(self):
        """Restaura as configurações padrão"""
        try:
            if messagebox.askyesno("Confirmar", "Deseja restaurar as configurações padrão?"):
                self.var_potencia.set(92.0)
                self.var_eficiencia.set(100.0)
                self.var_tarifa.set(0.65)
                self.var_investimento.set(450000.0)
                messagebox.showinfo("Sucesso", "Configurações restauradas!")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao restaurar configurações: {e}")

        def gerar_relatorio_completo(self):
            """Gera relatório completo"""
            try:
                ano = self.var_ano_relatorio.get()

                relatorio = f"""RELATÓRIO COMPLETO DO SISTEMA - {ano}
    =====================================

    CONFIGURAÇÕES:
    - Potência: {self.var_potencia.get():.1f} kW
    - Eficiência: {self.var_eficiencia.get():.1f}%
    - Tarifa: R\$ {self.var_tarifa.get():.2f}/kWh
    - Investimento: R\$ {self.var_investimento.get():,.2f}

    UNIDADES ATIVAS:
    """

                for unidade in self.sistema.sistema.get_unidades_ativas():
                    consumo_anual = sum(unidade.consumo_mensal_kwh)
                    relatorio += f"- {unidade.nome}: {consumo_anual:,.0f} kWh/ano\n"

                # Adicionar resultados se disponíveis
                try:
                    resultados = self.sistema.calcular_resultados_anuais(ano)
                    if resultados:
                        energia = resultados['energia']
                        financeiro = resultados['financeiro']

                        relatorio += f"""
    RESULTADOS ANUAIS:
    - Geração Total: {energia['geracao_total']:,.0f} kWh
    - Consumo Total: {energia['consumo_total']:,.0f} kWh
    - Saldo Anual: {energia['saldo_anual']:,.0f} kWh
    - Economia Total: R\$ {financeiro['economia_total']:,.2f}
    - Payback: {financeiro['payback_anos']:.1f} anos
    - ROI (25 anos): {financeiro['roi_percentual']:.1f}%
    """
                except:
                    relatorio += "\nERRO: Não foi possível calcular resultados anuais"

                relatorio += f"""
    =====================================
    Relatório gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}
    Sistema de Energia Solar v2.0
    """

                self.text_relatorio.delete(1.0, tk.END)
                self.text_relatorio.insert(1.0, relatorio)

                messagebox.showinfo("Sucesso", "Relatório completo gerado!")

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao gerar relatório: {e}")

        def gerar_relatorio_resumido(self):
            """Gera relatório resumido"""
            try:
                ano = self.var_ano_relatorio.get()

                relatorio = f"""RELATÓRIO RESUMIDO - {ano}
    ==========================

    SISTEMA:
    - Potência: {self.var_potencia.get():.1f} kW
    - Unidades: {len(self.sistema.sistema.get_unidades_ativas())}

    RESUMO FINANCEIRO:
    - Investimento: R\$ {self.var_investimento.get():,.2f}
    - Tarifa: R\$ {self.var_tarifa.get():.2f}/kWh

    STATUS: Sistema operacional
    Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}
    """

                self.text_relatorio.delete(1.0, tk.END)
                self.text_relatorio.insert(1.0, relatorio)

                messagebox.showinfo("Sucesso", "Relatório resumido gerado!")

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao gerar relatório resumido: {e}")

        def abrir_janela_analises(self):
            """Abre a janela de análises avançadas"""
            try:
                from ui.janela_analises import JanelaAnalises
                janela_analises = JanelaAnalises(self.sistema)

            except ImportError:
                messagebox.showinfo("Info", "Janela de análises ainda não implementada")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao abrir análises: {e}")

        def mostrar_sobre(self):
            """Mostra informações sobre o sistema"""
            messagebox.showinfo("Sobre",
                                "Sistema de Energia Solar v2.0\n\n"
                                "Dashboard Principal\n"
                                "Desenvolvido para análise de sistemas fotovoltaicos\n\n"
                                "© 2024")

        def executar(self):
            """Executa a interface gráfica"""
            try:
                self.root.mainloop()
            except Exception as e:
                messagebox.showerror("Erro Crítico", f"Erro na execução: {e}")
            finally:
                print("👋 Dashboard encerrado!")

    def main():
        """Função principal para teste"""
        try:
            app = InterfacePrincipal()
            app.executar()
        except Exception as e:
            print(f"❌ Erro ao iniciar dashboard: {e}")
            import traceback
            traceback.print_exc()

    if __name__ == "__main__":
        main()