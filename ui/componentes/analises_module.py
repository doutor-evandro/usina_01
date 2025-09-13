"""
Módulo Análises - Funcionalidades avançadas de análise
"""

import tkinter as tk
from tkinter import ttk
from .base_module import BaseModule


class AnalisesModule(BaseModule):
    """Módulo responsável pelas análises avançadas"""

    def __init__(self, parent_frame, sistema, cores=None):
        super().__init__(parent_frame, sistema, cores)
        self.notebook = None

    def criar_interface(self):
        """Cria a interface de análises"""
        print("🔧 Criando interface de análises...")
        self.limpar_frame()

        try:
            # Criar notebook para as abas de análises
            self.notebook = ttk.Notebook(self.parent_frame)
            self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            # Criar abas
            self._criar_aba_graficos_personalizados()
            self._criar_aba_unidades_detalhadas()
            self._criar_aba_analise_creditos()

            print("✅ Interface de análises criada com sucesso!")

        except Exception as e:
            print(f"❌ Erro ao criar análises: {e}")
            import traceback
            traceback.print_exc()
            self._criar_analises_simples()

    def _criar_aba_graficos_personalizados(self):
        """Cria aba de gráficos personalizados"""
        frame_graficos = ttk.Frame(self.notebook)
        self.notebook.add(frame_graficos, text="📈 Gráficos Personalizados")

        # Controles
        frame_controles = tk.LabelFrame(frame_graficos, text="Controles de Análise",
                                        font=('Arial', 12, 'bold'))
        frame_controles.pack(fill=tk.X, padx=10, pady=10)

        # Primeira linha de controles
        frame_linha1 = tk.Frame(frame_controles)
        frame_linha1.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(frame_linha1, text="Tipo de Análise:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT)

        self.var_tipo_analise = tk.StringVar()
        combo_tipos = ttk.Combobox(frame_linha1, textvariable=self.var_tipo_analise,
                                   values=["Distribuição por Unidade", "Análise de Tendências",
                                           "Eficiência Mensal", "Comparativo Anual"],
                                   state="readonly", width=25)
        combo_tipos.pack(side=tk.LEFT, padx=10)
        combo_tipos.set("Distribuição por Unidade")

        ttk.Button(frame_linha1, text="📈 Gerar Análise",
                   command=self._gerar_analise_personalizada).pack(side=tk.LEFT, padx=10)

        # Frame para resultado
        self.frame_resultado_analise = tk.LabelFrame(frame_graficos, text="Resultado da Análise",
                                                     font=('Arial', 12, 'bold'))
        self.frame_resultado_analise.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Gerar análise inicial
        self._gerar_analise_personalizada()

    def _criar_aba_unidades_detalhadas(self):
        """Cria aba de unidades detalhadas"""
        frame_unidades = ttk.Frame(self.notebook)
        self.notebook.add(frame_unidades, text="🏠 Unidades Detalhadas")

        # Cabeçalho
        frame_header = tk.Frame(frame_unidades)
        frame_header.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(frame_header, text="Gestão Detalhada de Unidades",
                 font=('Arial', 16, 'bold')).pack(side=tk.LEFT)

        ttk.Button(frame_header, text="🔄 Atualizar",
                   command=self._atualizar_unidades).pack(side=tk.RIGHT)

        # Lista de unidades
        frame_lista = tk.LabelFrame(frame_unidades, text="Unidades Cadastradas",
                                    font=('Arial', 12, 'bold'))
        frame_lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Treeview com scrollbar
        frame_tree = tk.Frame(frame_lista)
        frame_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Colunas da tabela
        colunas = ('Nome', 'Tipo', 'Status', 'Consumo Mensal', 'Consumo Anual', 'Economia')
        self.tree_unidades = ttk.Treeview(frame_tree, columns=colunas, show='headings', height=10)

        # Configurar colunas
        for col in colunas:
            self.tree_unidades.heading(col, text=col)
            if col == 'Nome':
                self.tree_unidades.column(col, width=150)
            elif col in ['Consumo Mensal', 'Consumo Anual', 'Economia']:
                self.tree_unidades.column(col, width=120)
            else:
                self.tree_unidades.column(col, width=100)

        # Scrollbar
        scrollbar_unidades = ttk.Scrollbar(frame_tree, orient=tk.VERTICAL,
                                           command=self.tree_unidades.yview)
        self.tree_unidades.configure(yscrollcommand=scrollbar_unidades.set)

        # Pack treeview e scrollbar
        self.tree_unidades.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_unidades.pack(side=tk.RIGHT, fill=tk.Y)

        # Carregar dados das unidades
        self._carregar_dados_unidades()

        # Frame de detalhes
        frame_detalhes = tk.LabelFrame(frame_unidades, text="Detalhes da Unidade Selecionada",
                                       font=('Arial', 12, 'bold'))
        frame_detalhes.pack(fill=tk.X, padx=10, pady=10)

        self.text_detalhes = tk.Text(frame_detalhes, height=6, wrap=tk.WORD)
        scrollbar_detalhes = ttk.Scrollbar(frame_detalhes, orient=tk.VERTICAL,
                                           command=self.text_detalhes.yview)
        self.text_detalhes.configure(yscrollcommand=scrollbar_detalhes.set)

        self.text_detalhes.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar_detalhes.pack(side=tk.RIGHT, fill=tk.Y, pady=10)

        # Bind para seleção
        self.tree_unidades.bind('<<TreeviewSelect>>', self._on_unidade_selecionada)

    def _criar_aba_analise_creditos(self):
        """Cria aba de análise de créditos"""
        frame_creditos = ttk.Frame(self.notebook)
        self.notebook.add(frame_creditos, text="💰 Análise de Créditos")

        # Cabeçalho
        tk.Label(frame_creditos, text="Análise de Créditos Energéticos",
                 font=('Arial', 16, 'bold')).pack(pady=10)

        # Controles
        frame_controles = tk.LabelFrame(frame_creditos, text="Parâmetros de Análise",
                                        font=('Arial', 12, 'bold'))
        frame_controles.pack(fill=tk.X, padx=10, pady=10)

        # Linha de controles
        frame_ctrl_linha = tk.Frame(frame_controles)
        frame_ctrl_linha.pack(fill=tk.X, padx=10, pady=10)

        tk.Label(frame_ctrl_linha, text="Mês:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT)

        self.var_mes_credito = tk.IntVar(value=1)
        combo_mes = ttk.Combobox(frame_ctrl_linha, textvariable=self.var_mes_credito,
                                 values=list(range(1, 13)), state="readonly", width=10)
        combo_mes.pack(side=tk.LEFT, padx=10)

        tk.Label(frame_ctrl_linha, text="Ano:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=(20, 0))

        self.var_ano_credito = tk.IntVar(value=2024)
        combo_ano = ttk.Combobox(frame_ctrl_linha, textvariable=self.var_ano_credito,
                                 values=[2023, 2024, 2025], state="readonly", width=10)
        combo_ano.pack(side=tk.LEFT, padx=10)

        ttk.Button(frame_ctrl_linha, text="💰 Calcular Créditos",
                   command=self._calcular_creditos_detalhado).pack(side=tk.LEFT, padx=20)

        # Resultado em duas colunas
        frame_resultado = tk.Frame(frame_creditos)
        frame_resultado.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Coluna esquerda - Resumo
        frame_resumo = tk.LabelFrame(frame_resultado, text="Resumo do Período",
                                     font=('Arial', 12, 'bold'))
        frame_resumo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        self.text_resumo_creditos = tk.Text(frame_resumo, wrap=tk.WORD, height=15)
        scroll_resumo = ttk.Scrollbar(frame_resumo, orient=tk.VERTICAL,
                                      command=self.text_resumo_creditos.yview)
        self.text_resumo_creditos.configure(yscrollcommand=scroll_resumo.set)

        self.text_resumo_creditos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scroll_resumo.pack(side=tk.RIGHT, fill=tk.Y, pady=10)

        # Coluna direita - Detalhamento
        frame_detalhamento = tk.LabelFrame(frame_resultado, text="Detalhamento por Unidade",
                                           font=('Arial', 12, 'bold'))
        frame_detalhamento.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        self.text_detalhamento_creditos = tk.Text(frame_detalhamento, wrap=tk.WORD, height=15)
        scroll_detalhamento = ttk.Scrollbar(frame_detalhamento, orient=tk.VERTICAL,
                                            command=self.text_detalhamento_creditos.yview)
        self.text_detalhamento_creditos.configure(yscrollcommand=scroll_detalhamento.set)

        self.text_detalhamento_creditos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scroll_detalhamento.pack(side=tk.RIGHT, fill=tk.Y, pady=10)

        # Calcular créditos inicial
        self._calcular_creditos_detalhado()

    def _gerar_analise_personalizada(self):
        """Gera análise baseada no tipo selecionado"""
        tipo = self.var_tipo_analise.get()

        # Limpar frame
        for widget in self.frame_resultado_analise.winfo_children():
            widget.destroy()

        print(f"📊 Gerando análise: {tipo}")

        if tipo == "Distribuição por Unidade":
            self._criar_grafico_distribuicao()
        elif tipo == "Análise de Tendências":
            self._criar_grafico_tendencias()
        elif tipo == "Eficiência Mensal":
            self._criar_grafico_eficiencia()
        elif tipo == "Comparativo Anual":
            self._criar_grafico_comparativo()

    def _criar_grafico_distribuicao(self):
        """Cria gráfico de distribuição por unidades"""
        try:
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

            fig = plt.Figure(figsize=(10, 6), dpi=100)
            ax = fig.add_subplot(111)

            # Dados de exemplo
            unidades = ['Lanchonet', 'Loja', 'Sobreloja', 'Residência']
            consumo = [800, 850, 750, 600]
            cores = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']

            # Gráfico de pizza
            wedges, texts, autotexts = ax.pie(consumo, labels=unidades, colors=cores,
                                              autopct='%1.1f%%', startangle=90)

            ax.set_title('Distribuição de Consumo por Unidade', fontsize=14, fontweight='bold')

            # Melhorar aparência
            for autotext in autotexts:
                autotext.set_color('white')
                autotext.set_fontweight('bold')

            canvas = FigureCanvasTkAgg(fig, self.frame_resultado_analise)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        except Exception as e:
            print(f"Erro ao criar gráfico de distribuição: {e}")
            self._mostrar_erro_analise(str(e))

    def _criar_grafico_tendencias(self):
        """Cria gráfico de tendências"""
        try:
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

            fig = plt.Figure(figsize=(10, 6), dpi=100)
            ax = fig.add_subplot(111)

            # Dados de exemplo
            meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun']
            geracao = [15162, 12453, 12500, 10423, 9002, 8675]
            consumo = [8800, 8900, 8750, 8600, 8500, 8400]

            ax.plot(meses, geracao, marker='o', linewidth=3, label='Geração', color='#2E86AB')
            ax.plot(meses, consumo, marker='s', linewidth=3, label='Consumo', color='#A23B72')

            ax.set_title('Tendência de Geração vs Consumo', fontsize=14, fontweight='bold')
            ax.set_ylabel('Energia (kWh)')
            ax.legend()
            ax.grid(True, alpha=0.3)

            canvas = FigureCanvasTkAgg(fig, self.frame_resultado_analise)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        except Exception as e:
            print(f"Erro ao criar gráfico de tendências: {e}")
            self._mostrar_erro_analise(str(e))

    def _criar_grafico_eficiencia(self):
        """Cria gráfico de eficiência"""
        try:
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

            fig = plt.Figure(figsize=(10, 6), dpi=100)
            ax = fig.add_subplot(111)

            # Dados de exemplo
            meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun']
            eficiencia = [92, 89, 94, 87, 85, 88]

            bars = ax.bar(meses, eficiencia, color='#F18F01', alpha=0.8)
            ax.set_title('Eficiência Mensal do Sistema', fontsize=14, fontweight='bold')
            ax.set_ylabel('Eficiência (%)')
            ax.set_ylim(80, 100)

            # Adicionar valores nas barras
            for bar, valor in zip(bars, eficiencia):
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width() / 2., height + 0.5,
                        f'{valor}%', ha='center', va='bottom', fontweight='bold')

            ax.grid(True, alpha=0.3, axis='y')

            canvas = FigureCanvasTkAgg(fig, self.frame_resultado_analise)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        except Exception as e:
            print(f"Erro ao criar gráfico de eficiência: {e}")
            self._mostrar_erro_analise(str(e))

    def _criar_grafico_comparativo(self):
        """Cria gráfico comparativo anual"""
        try:
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

            fig = plt.Figure(figsize=(10, 6), dpi=100)
            ax = fig.add_subplot(111)

            # Dados de exemplo
            anos = ['2022', '2023', '2024']
            geracao = [145000, 152000, 158000]
            consumo = [105000, 108000, 106000]

            x = range(len(anos))
            width = 0.35

            bars1 = ax.bar([i - width / 2 for i in x], geracao, width,
                           label='Geração', color='#2E86AB', alpha=0.8)
            bars2 = ax.bar([i + width / 2 for i in x], consumo, width,
                           label='Consumo', color='#A23B72', alpha=0.8)

            ax.set_title('Comparativo Anual - Geração vs Consumo', fontsize=14, fontweight='bold')
            ax.set_ylabel('Energia (kWh)')
            ax.set_xticks(x)
            ax.set_xticklabels(anos)
            ax.legend()
            ax.grid(True, alpha=0.3, axis='y')

            canvas = FigureCanvasTkAgg(fig, self.frame_resultado_analise)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        except Exception as e:
            print(f"Erro ao criar gráfico comparativo: {e}")
            self._mostrar_erro_analise(str(e))

    def _carregar_dados_unidades(self):
        """Carrega dados das unidades na tabela"""
        try:
            # Limpar tabela
            for item in self.tree_unidades.get_children():
                self.tree_unidades.delete(item)

            # Dados de exemplo (substituir por dados reais)
            unidades_dados = [
                ("Lanchonet", "Comercial", "Ativa", "800 kWh", "9.600 kWh", "R$ 6.240,00"),
                ("Loja", "Comercial", "Ativa", "850 kWh", "10.200 kWh", "R$ 6.630,00"),
                ("Sobreloja", "Comercial", "Ativa", "750 kWh", "9.000 kWh", "R$ 5.850,00"),
                ("Residência", "Residencial", "Ativa", "600 kWh", "7.200 kWh", "R$ 4.680,00"),
            ]

            for dados in unidades_dados:
                self.tree_unidades.insert('', 'end', values=dados)

        except Exception as e:
            print(f"Erro ao carregar unidades: {e}")

    def _atualizar_unidades(self):
        """Atualiza dados das unidades"""
        print("🔄 Atualizando dados das unidades...")
        self._carregar_dados_unidades()

    def _on_unidade_selecionada(self, event):
        """Evento quando uma unidade é selecionada"""
        selection = self.tree_unidades.selection()
        if selection:
            item = self.tree_unidades.item(selection[0])
            valores = item['values']

            detalhes = f"""DETALHES DA UNIDADE: {valores[0]}
{'=' * 50}

Tipo de Ligação: {valores[1]}
Status: {valores[2]}
Consumo Mensal Médio: {valores[3]}
Consumo Anual Total: {valores[4]}
Economia Anual Estimada: {valores[5]}

INFORMAÇÕES ADICIONAIS:
• Tarifa Aplicada: R$ 0,65/kWh
• Tipo de Medição: Convencional
• Grupo Tarifário: B1 (Residencial) / B3 (Comercial)
• Modalidade: Compensação de Energia

HISTÓRICO RECENTE:
• Último mês: Consumo dentro da média
• Tendência: Estável
• Eficiência: 92% da capacidade instalada
"""

            self.text_detalhes.delete(1.0, tk.END)
            self.text_detalhes.insert(1.0, detalhes)

    def _calcular_creditos_detalhado(self):
        """Calcula distribuição de créditos detalhada"""
        mes = self.var_mes_credito.get()
        ano = self.var_ano_credito.get()

        # Resumo
        resumo = f"""ANÁLISE DE CRÉDITOS - {mes:02d}/{ano}
{'=' * 40}

GERAÇÃO DO PERÍODO:
🌞 Energia Gerada: 11.472 kWh
⚡ Energia Consumida: 8.800 kWh
💰 Créditos Disponíveis: 2.672 kWh

VALORES FINANCEIROS:
💵 Tarifa Média: R$ 0,65/kWh
💰 Valor dos Créditos: R$ 1.736,80
📊 Economia Total: R$ 5.720,00

DISTRIBUIÇÃO:
🏠 4 unidades ativas
📈 Eficiência: 92%
⚖️ Saldo: +2.672 kWh

PROJEÇÃO ANUAL:
📅 Créditos/Ano: 32.064 kWh
💰 Economia/Ano: R$ 20.841,60
📊 ROI Estimado: 287%
"""

        # Detalhamento
        detalhamento = f"""DISTRIBUIÇÃO POR UNIDADE
{'=' * 30}

🏪 LANCHONET
   Consumo: 800 kWh
   Créditos: 800 kWh
   Economia: R$ 520,00
   Status: ✅ Coberto

🏬 LOJA
   Consumo: 850 kWh
   Créditos: 850 kWh
   Economia: R$ 552,50
   Status: ✅ Coberto

🏢 SOBRELOJA
   Consumo: 750 kWh
   Créditos: 750 kWh
   Economia: R$ 487,50
   Status: ✅ Coberto

🏠 RESIDÊNCIA
   Consumo: 600 kWh
   Créditos: 272 kWh
   Economia: R$ 176,80
   Status: ⚠️ Parcial

SALDO FINAL:
💡 Créditos Restantes: 0 kWh
�� Utilização: 100%
✅ Otimização: Máxima
"""

        # Atualizar textos
        self.text_resumo_creditos.delete(1.0, tk.END)
        self.text_resumo_creditos.insert(1.0, resumo)

        self.text_detalhamento_creditos.delete(1.0, tk.END)
        self.text_detalhamento_creditos.insert(1.0, detalhamento)

    def _mostrar_erro_analise(self, erro):
        """Mostra erro na análise"""
        tk.Label(self.frame_resultado_analise,
                 text=f"❌ Erro na análise: {erro}",
                 font=('Arial', 12), fg='red').pack(pady=20)

    def _criar_analises_simples(self):
        """Cria análises simples em caso de erro"""
        tk.Label(self.parent_frame,
                 text="📈 Análises Avançadas",
                 font=('Arial', 18, 'bold')).pack(pady=20)

        tk.Label(self.parent_frame,
                 text="Erro ao carregar módulo de análises.\nVerifique os logs para mais detalhes.",
                 font=('Arial', 12), fg='red').pack(pady=10)

    def atualizar_dados(self):
        """Atualiza dados das análises"""
        print("🔄 Atualizando dados das análises...")
        if hasattr(self, 'tree_unidades'):
            self._carregar_dados_unidades()