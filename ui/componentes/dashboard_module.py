"""
Módulo Dashboard - Reutiliza janela_principal
"""

import tkinter as tk
from tkinter import ttk
from .base_module import BaseModule


class DashboardModule(BaseModule):
    """Módulo que reutiliza funcionalidades da janela_principal"""

    def __init__(self, parent_frame, sistema, cores=None):
        super().__init__(parent_frame, sistema, cores)
        self.janela_principal_ref = None

    def criar_interface(self):
        """Cria interface reutilizando janela_principal"""
        self.limpar_frame()

        try:
            # Importar e reutilizar janela_principal
            from ..janela_principal import InterfacePrincipal

            # Criar instância sem janela própria
            self.janela_principal_ref = self._criar_instancia_dashboard()

            # Recriar componentes no frame atual
            self._recriar_dashboard_no_frame()

        except Exception as e:
            print(f"Erro ao criar dashboard: {e}")
            import traceback
            traceback.print_exc()
            self._criar_dashboard_simples()

    def _criar_instancia_dashboard(self):
        """Cria instância do dashboard sem janela"""

        # Criar um mock da janela principal
        class MockDashboard:
            def __init__(self, sistema):
                self.sistema = sistema
                self.cores = {
                    'primaria': '#2E86AB',
                    'secundaria': '#A23B72',
                    'sucesso': '#F18F01',
                    'fundo': '#F5F5F5',
                    'texto': '#2C3E50'
                }

        return MockDashboard(self.sistema)

    def _recriar_dashboard_no_frame(self):
        """Recria componentes do dashboard no frame atual"""
        # Criar indicadores
        self._criar_indicadores_integrados()

        # Criar gráfico
        self._criar_grafico_integrado()

        # Atualizar dados
        self.atualizar_dados()

    def _criar_indicadores_integrados(self):
        """Cria indicadores integrados"""
        frame_indicadores = tk.LabelFrame(self.parent_frame,
                                          text="Indicadores Principais",
                                          font=('Arial', 14, 'bold'),
                                          bg=self.cores['content'])
        frame_indicadores.pack(fill=tk.X, padx=10, pady=10)

        # Grid de indicadores
        for i in range(5):
            frame_indicadores.columnconfigure(i, weight=1)

        # Criar cards (reutilizar método da classe base)
        self.card_geracao, self.label_geracao = self.criar_card(
            frame_indicadores, "Geração Anual", "0 kWh",
            self.cores['primaria'], 0, 0)

        self.card_consumo, self.label_consumo = self.criar_card(
            frame_indicadores, "Consumo Anual", "0 kWh",
            self.cores['secundaria'], 0, 1)

        self.card_economia, self.label_economia = self.criar_card(
            frame_indicadores, "Economia Anual", "R\$ 0,00",
            self.cores['sucesso'], 0, 2)

        self.card_payback, self.label_payback = self.criar_card(
            frame_indicadores, "Payback", "0 anos", '#9B59B6', 0, 3)

        self.card_roi, self.label_roi = self.criar_card(
            frame_indicadores, "ROI (25 anos)", "0%", '#E67E22', 0, 4)

    def _criar_grafico_integrado(self):
        """Cria gráfico integrado"""
        frame_grafico = tk.LabelFrame(self.parent_frame,
                                      text="Análise Mensal",
                                      font=('Arial', 14, 'bold'),
                                      bg=self.cores['content'])
        frame_grafico.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Controles
        frame_controles = tk.Frame(frame_grafico, bg=self.cores['content'])
        frame_controles.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(frame_controles, text="Tipo:",
                 bg=self.cores['content'], font=('Arial', 12, 'bold')).pack(side=tk.LEFT)

        self.var_tipo_grafico = tk.StringVar(value="Geração vs Consumo")
        combo_tipos = ttk.Combobox(frame_controles,
                                   textvariable=self.var_tipo_grafico,
                                   values=["Geração vs Consumo", "Economia Mensal", "Saldo Energético"],
                                   state="readonly", width=25,
                                   font=('Arial', 11))
        combo_tipos.pack(side=tk.LEFT, padx=10)

        # ✅ ADICIONAR: Evento para mudança automática
        combo_tipos.bind('<<ComboboxSelected>>', self._on_tipo_grafico_changed)

        # Frame para gráfico
        self.frame_grafico_canvas = tk.Frame(frame_grafico, bg=self.cores['content'])
        self.frame_grafico_canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # ✅ CRIAR: Gráfico inicial automaticamente
        self._atualizar_grafico_integrado()

    def _on_tipo_grafico_changed(self, event=None):
        """✅ MÉTODO ADICIONADO: Evento chamado quando o tipo de gráfico é alterado"""
        print(f"🔄 Tipo alterado para: {self.var_tipo_grafico.get()}")
        self._atualizar_grafico_integrado()

    def _atualizar_grafico_integrado(self):
        """Atualiza gráfico integrado"""
        try:
            print("🔄 Atualizando gráfico...")

            # Verificar se matplotlib está disponível
            try:
                import matplotlib.pyplot as plt
                from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
                print("✅ Matplotlib importado com sucesso")
            except ImportError as e:
                print(f"❌ Erro ao importar matplotlib: {e}")
                self._mostrar_erro_grafico("Matplotlib não disponível")
                return

            # Verificar se frame existe
            if not hasattr(self, 'frame_grafico_canvas'):
                print("❌ Frame do gráfico não existe")
                return

            # Limpar canvas anterior
            for widget in self.frame_grafico_canvas.winfo_children():
                widget.destroy()
            print("🧹 Canvas limpo")

            # Criar nova figura
            fig = plt.Figure(figsize=(10, 5), dpi=100, facecolor='white')
            ax = fig.add_subplot(111)

            # Dados de exemplo
            meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
                     'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
            geracao = [15162, 12453, 12500, 10423, 9002, 6675,
                       8197, 9954, 11561, 13234, 14000, 14606]
            consumo = [8800] * 12

            tipo = self.var_tipo_grafico.get()
            print(f"📊 Criando gráfico tipo: {tipo}")

            if tipo == "Geração vs Consumo":
                # Criar barras
                x_pos = range(len(meses))
                width = 0.35

                bars1 = ax.bar([x - width / 2 for x in x_pos], geracao, width,
                               label='Geração', color=self.cores['primaria'], alpha=0.8)
                bars2 = ax.bar([x + width / 2 for x in x_pos], consumo, width,
                               label='Consumo', color=self.cores['secundaria'], alpha=0.8)

                ax.set_ylabel('Energia (kWh)', fontsize=12)
                ax.set_title('Geração vs Consumo Mensal', fontsize=14, fontweight='bold')
                ax.set_xticks(x_pos)
                ax.set_xticklabels(meses)
                ax.legend(fontsize=11)

                # Adicionar valores nas barras (apenas alguns para não poluir)
                for i, bar in enumerate(bars1):
                    if i % 2 == 0:  # Mostrar apenas valores alternados
                        height = bar.get_height()
                        ax.text(bar.get_x() + bar.get_width()/2., height + 200,
                               f'{int(height/1000)}k', ha='center', va='bottom', fontsize=9)

            elif tipo == "Economia Mensal":
                economia = [4000, 3200, 3250, 2800, 2400, 1800, 2200, 2650, 3100, 3550, 3750, 3900]

                # Linha principal
                line = ax.plot(meses, economia, marker='o', linewidth=3,
                               color=self.cores['sucesso'], markersize=8,
                               markerfacecolor='white', markeredgewidth=2)

                # Área preenchida
                ax.fill_between(meses, economia, alpha=0.3, color=self.cores['sucesso'])

                ax.set_ylabel('Economia (R\$)', fontsize=12)  # ✅ CORRIGIDO: Removido escape
                ax.set_title('Economia Mensal Estimada', fontsize=14, fontweight='bold')

                # Adicionar valores nos pontos
                for i, v in enumerate(economia):
                    if i % 3 == 0:  # Mostrar apenas alguns valores
                        ax.text(i, v + 100, f'R\${v:,.0f}', ha='center', va='bottom', fontsize=9)  # ✅ CORRIGIDO

            elif tipo == "Saldo Energético":
                saldo = [6362, 3653, 3700, 1623, 202, -2125, -603, 1154, 2761, 4434, 5200, 5806]
                cores_saldo = ['#2ECC71' if s >= 0 else '#E74C3C' for s in saldo]

                bars = ax.bar(meses, saldo, color=cores_saldo, alpha=0.7, edgecolor='black', linewidth=0.5)
                ax.set_ylabel('Saldo (kWh)', fontsize=12)
                ax.set_title('Saldo Energético Mensal', fontsize=14, fontweight='bold')
                ax.axhline(y=0, color='black', linestyle='-', alpha=0.8, linewidth=2)

                # Adicionar rótulos nos valores extremos
                for i, (bar, valor) in enumerate(zip(bars, saldo)):
                    if abs(valor) > 3000:  # Mostrar apenas valores significativos
                        height = bar.get_height()
                        va = 'bottom' if height >= 0 else 'top'
                        offset = 200 if height >= 0 else -200
                        ax.text(bar.get_x() + bar.get_width()/2., height + offset,
                               f'{int(valor)}', ha='center', va=va, fontsize=9, fontweight='bold')

            # Configurações gerais
            ax.set_xlabel('Meses', fontsize=12)
            ax.grid(True, alpha=0.3, linestyle='--')
            ax.tick_params(axis='x', rotation=45, labelsize=10)
            ax.tick_params(axis='y', labelsize=10)

            # Melhorar aparência
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#CCCCCC')
            ax.spines['bottom'].set_color('#CCCCCC')

            # Ajustar layout
            fig.tight_layout(pad=2.0)

            # Criar canvas e adicionar ao frame
            canvas = FigureCanvasTkAgg(fig, self.frame_grafico_canvas)
            canvas.draw()
            canvas_widget = canvas.get_tk_widget()
            canvas_widget.pack(fill=tk.BOTH, expand=True)

            print(f"✅ Gráfico '{tipo}' criado com sucesso!")

        except Exception as e:
            print(f"❌ Erro detalhado ao atualizar gráfico: {e}")
            import traceback
            traceback.print_exc()
            self._mostrar_erro_grafico(str(e))

    def _mostrar_erro_grafico(self, erro):
        """Mostra erro no lugar do gráfico"""
        # Limpar frame
        for widget in self.frame_grafico_canvas.winfo_children():
            widget.destroy()

        # Mostrar erro
        frame_erro = tk.Frame(self.frame_grafico_canvas, bg='#FFEBEE', relief=tk.RAISED, bd=2)
        frame_erro.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        tk.Label(frame_erro, text="❌ Erro no Gráfico",
                 font=('Arial', 16, 'bold'), fg='#D32F2F', bg='#FFEBEE').pack(pady=10)

        tk.Label(frame_erro, text=f"Erro: {erro}",
                 font=('Arial', 10), fg='#666', bg='#FFEBEE', wraplength=400).pack()

        tk.Button(frame_erro, text="🔄 Tentar Novamente",
                  command=self._atualizar_grafico_integrado,
                  bg='#2196F3', fg='white', font=('Arial', 10, 'bold'),
                  relief=tk.RAISED, bd=2, padx=20, pady=5).pack(pady=10)

    def _criar_dashboard_simples(self):
        """Cria dashboard simples em caso de erro"""
        tk.Label(self.parent_frame,
                 text="📊 Dashboard Simplificado",
                 font=('Arial', 18, 'bold')).pack(pady=20)

        tk.Label(self.parent_frame,
                 text="Sistema carregado com sucesso!\nDados sendo processados...",
                 font=('Arial', 12)).pack(pady=10)

    def atualizar_dados(self):
        """Atualiza dados do dashboard"""
        try:
            if hasattr(self, 'label_geracao'):
                # Atualizar com dados reais do sistema
                from utilitarios.formatadores import formatar_energia, formatar_moeda

                # Simular dados (substituir por cálculos reais)
                self.label_geracao.config(text=formatar_energia(145000))
                self.label_consumo.config(text=formatar_energia(105600))
                self.label_economia.config(text=formatar_moeda(39400))
                self.label_payback.config(text="11.4 anos")
                self.label_roi.config(text="287%")

        except Exception as e:
            print(f"Erro ao atualizar dados: {e}")