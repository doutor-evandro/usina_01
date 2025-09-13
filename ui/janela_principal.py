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

        # Criar abas
        self.criar_aba_dashboard()
        self.criar_aba_configuracoes()
        self.criar_aba_relatorios()

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

    def criar_aba_configuracoes(self):
        """Cria a aba de configurações"""
        frame_config = ttk.Frame(self.notebook)
        self.notebook.add(frame_config, text="⚙️ Configurações")

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

    # ========== MÉTODOS DE ATUALIZAÇÃO ==========

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

    # ========== MÉTODOS DE AÇÃO ==========

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
- Tarifa: R$ {self.var_tarifa.get():.2f}/kWh
- Investimento: R$ {self.var_investimento.get():,.2f}

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
- Economia Total: R$ {financeiro['economia_total']:,.2f}
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
- Investimento: R$ {self.var_investimento.get():,.2f}
- Tarifa: R$ {self.var_tarifa.get():.2f}/kWh

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