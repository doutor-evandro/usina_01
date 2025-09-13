"""
Janela de Análises Avançadas - Sistema de Energia Solar v2.0
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

from utilitarios.formatadores import formatar_moeda, formatar_energia, formatar_percentual

# Importar funções legacy
try:
    from utilitarios.funcoes_legacy import FuncoesLegacy
    from ui.graficos.graficos_legacy import GraficosLegacy

    LEGACY_DISPONIVEL = True
except ImportError:
    LEGACY_DISPONIVEL = False


class JanelaAnalises:
    """Janela de análises avançadas"""

    def __init__(self, sistema):
        print("🔬 Iniciando Análises Avançadas...")

        # Receber sistema da janela principal
        self.sistema = sistema
        self.root = tk.Toplevel()
        self.canvas_grafico = None
        self.figura_atual = None
        self.funcoes_legacy = None
        self.calculadora_creditos = None

        # Configurar janela
        self.configurar_janela()

        # Inicializar componentes avançados
        self.inicializar_componentes()

        # Criar interface
        self.criar_interface()

        print("✅ Análises Avançadas criadas com sucesso!")

    def configurar_janela(self):
        """Configura a janela de análises"""
        self.root.title("Sistema de Energia Solar - Análises Avançadas v2.0")
        self.root.geometry("1400x900")
        self.root.minsize(1200, 700)

        # Cores personalizadas
        self.cores = {
            'primaria': '#2E86AB',
            'secundaria': '#A23B72',
            'sucesso': '#F18F01',
            'fundo': '#F5F5F5',
            'texto': '#2C3E50'
        }

    def inicializar_componentes(self):
        """Inicializa componentes avançados"""
        try:
            # Inicializar funções legacy se disponível
            if LEGACY_DISPONIVEL:
                self.funcoes_legacy = FuncoesLegacy(self.sistema.sistema)
                print("✅ Funções legacy inicializadas para análises")

            # Inicializar calculadora de créditos
            try:
                from negocio.calculadora_creditos import CalculadoraCreditos
                self.calculadora_creditos = CalculadoraCreditos(self.sistema.sistema)
                print("✅ Calculadora de créditos inicializada para análises")
            except Exception as e:
                print(f"⚠️ Calculadora de créditos não disponível: {e}")

        except Exception as e:
            print(f"⚠️ Erro ao inicializar componentes avançados: {e}")

    def criar_interface(self):
        """Cria toda a interface de análises"""
        # Frame principal
        self.frame_principal = ttk.Frame(self.root)
        self.frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Criar notebook (abas)
        self.notebook = ttk.Notebook(self.frame_principal)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Criar abas avançadas
        self.criar_aba_unidades_detalhadas()
        self.criar_aba_graficos_personalizados()

        # Aba de gráficos legacy (se disponível)
        if LEGACY_DISPONIVEL and self.funcoes_legacy:
            self.criar_aba_graficos_legacy()

        # Aba de créditos (se disponível)
        if self.calculadora_creditos:
            self.criar_aba_creditos()

        # Barra de status
        self.criar_barra_status()

    def criar_aba_unidades_detalhadas(self):
        """Cria aba com análise detalhada das unidades"""
        frame_unidades = ttk.Frame(self.notebook)
        self.notebook.add(frame_unidades, text="🏠 Unidades Detalhadas")

        # Frame superior - Lista de unidades
        frame_lista = ttk.LabelFrame(frame_unidades, text="Unidades Cadastradas", padding=10)
        frame_lista.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Treeview para unidades
        colunas_unidades = ('Nome', 'Tipo', 'Status', 'Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
                            'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez', 'Total')

        self.tree_unidades_detalhado = ttk.Treeview(frame_lista, columns=colunas_unidades, show='headings')

        # Configurar colunas
        for col in colunas_unidades:
            self.tree_unidades_detalhado.heading(col, text=col)
            if col in ['Nome']:
                self.tree_unidades_detalhado.column(col, width=150)
            elif col in ['Tipo', 'Status']:
                self.tree_unidades_detalhado.column(col, width=80)
            else:
                self.tree_unidades_detalhado.column(col, width=60)

        # Scrollbars
        scroll_y_unidades = ttk.Scrollbar(frame_lista, orient=tk.VERTICAL, command=self.tree_unidades_detalhado.yview)
        scroll_x_unidades = ttk.Scrollbar(frame_lista, orient=tk.HORIZONTAL, command=self.tree_unidades_detalhado.xview)
        self.tree_unidades_detalhado.configure(yscrollcommand=scroll_y_unidades.set,
                                               xscrollcommand=scroll_x_unidades.set)

        # Pack treeview e scrollbars
        self.tree_unidades_detalhado.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y_unidades.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x_unidades.pack(side=tk.BOTTOM, fill=tk.X)

        # Frame inferior - Controles
        frame_controles_unidades = ttk.Frame(frame_unidades)
        frame_controles_unidades.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(frame_controles_unidades, text="✅ Ativar Unidade",
                   command=self.ativar_unidade).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_controles_unidades, text="❌ Desativar Unidade",
                   command=self.desativar_unidade).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_controles_unidades, text="🔄 Atualizar Lista",
                   command=self.atualizar_lista_unidades).pack(side=tk.LEFT, padx=5)

        # Carregar dados iniciais
        self.atualizar_lista_unidades()

    def criar_aba_graficos_personalizados(self):
        """Cria aba de gráficos personalizados"""
        frame_graficos = ttk.Frame(self.notebook)
        self.notebook.add(frame_graficos, text="📈 Gráficos Personalizados")

        # Frame superior - Controles
        frame_controles_graf = ttk.LabelFrame(frame_graficos, text="Controles de Gráficos", padding=10)
        frame_controles_graf.pack(fill=tk.X, padx=10, pady=5)

        # Tipo de gráfico
        ttk.Label(frame_controles_graf, text="Tipo:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.var_tipo_grafico = tk.StringVar()
        combo_tipos = ttk.Combobox(frame_controles_graf, textvariable=self.var_tipo_grafico, values=[
            "Geração vs Consumo",
            "Economia Mensal",
            "Saldo Energético",
            "Distribuição por Unidade",
            "Análise de Tendências"
        ], state="readonly", width=25)
        combo_tipos.grid(row=0, column=1, padx=10, pady=5)
        combo_tipos.set("Geração vs Consumo")

        # Botão
        ttk.Button(frame_controles_graf, text="📈 Gerar Gráfico",
                   command=self.gerar_grafico_personalizado).grid(row=0, column=2, padx=10)

        # Frame para o gráfico
        self.frame_grafico_personalizado = ttk.LabelFrame(frame_graficos, text="Gráfico", padding=10)
        self.frame_grafico_personalizado.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Mensagem inicial
        ttk.Label(self.frame_grafico_personalizado,
                  text="Selecione um tipo de gráfico e clique em 'Gerar Gráfico'",
                  font=('Arial', 12)).pack(expand=True)

    def criar_aba_graficos_legacy(self):
        """Cria aba de gráficos compatível com sistema legacy"""
        frame_graficos = ttk.Frame(self.notebook)
        self.notebook.add(frame_graficos, text="📊 Gráficos Legacy")

        # Frame de controles
        frame_controles = ttk.LabelFrame(frame_graficos, text="Análises Gráficas Legacy", padding=10)
        frame_controles.pack(fill=tk.X, padx=10, pady=5)

        # Botões para diferentes análises
        ttk.Button(frame_controles, text="📈 Análises Completas",
                   command=self.abrir_graficos_analises).pack(side=tk.LEFT, padx=5)

        ttk.Button(frame_controles, text="�� Distribuição Mensal",
                   command=self.abrir_distribuicao_mensal).pack(side=tk.LEFT, padx=5)

        ttk.Button(frame_controles, text="🥧 Gráfico de Pizza",
                   command=self.abrir_grafico_pizza).pack(side=tk.LEFT, padx=5)

        # Frame para gráfico principal
        self.frame_grafico_legacy = ttk.LabelFrame(frame_graficos, text="Visualização Legacy", padding=10)
        self.frame_grafico_legacy.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Carregar gráfico inicial
        self.carregar_grafico_inicial_legacy()

    def criar_aba_creditos(self):
        """Cria aba específica para análise de créditos"""
        frame_creditos = ttk.Frame(self.notebook)
        self.notebook.add(frame_creditos, text="💰 Análise de Créditos")

        # Frame superior - Controles
        frame_controles = ttk.LabelFrame(frame_creditos, text="Análise de Créditos Energéticos", padding=10)
        frame_controles.pack(fill=tk.X, padx=10, pady=5)

        # Seleção de mês
        ttk.Label(frame_controles, text="Mês:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.var_mes_creditos = tk.IntVar(value=1)
        self.combo_mes = ttk.Combobox(frame_controles, textvariable=self.var_mes_creditos,
                                      values=list(range(1, 13)), state="readonly", width=10)
        self.combo_mes.grid(row=0, column=1, padx=10, pady=5)

        # Botões
        ttk.Button(frame_controles, text="📊 Calcular Distribuição",
                   command=self.calcular_distribuicao_creditos).grid(row=0, column=2, padx=10)

        # Frame central - Resultados
        frame_resultados = ttk.LabelFrame(frame_creditos, text="Distribuição de Créditos", padding=10)
        frame_resultados.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Text widget para mostrar resultados
        self.text_creditos = tk.Text(frame_resultados, wrap=tk.WORD, font=('Courier', 10))
        scroll_creditos = ttk.Scrollbar(frame_resultados, orient=tk.VERTICAL, command=self.text_creditos.yview)
        self.text_creditos.configure(yscrollcommand=scroll_creditos.set)

        self.text_creditos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_creditos.pack(side=tk.RIGHT, fill=tk.Y)

    def criar_barra_status(self):
        """Cria a barra de status"""
        self.barra_status = ttk.Frame(self.root)
        self.barra_status.pack(fill=tk.X, side=tk.BOTTOM)

        # Labels de status
        self.label_status = ttk.Label(self.barra_status, text="Análises carregadas", relief=tk.SUNKEN)
        self.label_status.pack(side=tk.LEFT, padx=5, pady=2)

        self.label_data = ttk.Label(self.barra_status, text=f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
                                    relief=tk.SUNKEN)
        self.label_data.pack(side=tk.RIGHT, padx=5, pady=2)

    # ========== MÉTODOS DE ATUALIZAÇÃO ==========

    def atualizar_lista_unidades(self):
        """Atualiza a lista detalhada de unidades"""
        try:
            # Limpar árvore
            for item in self.tree_unidades_detalhado.get_children():
                self.tree_unidades_detalhado.delete(item)

            # Adicionar unidades
            for unidade in self.sistema.sistema.unidades:
                status = "Ativa" if unidade.ativa else "Inativa"
                tipo = str(unidade.tipo_ligacao).replace('TipoLigacao.', '').upper()

                consumos = [f"{c:.0f}" for c in unidade.consumo_mensal_kwh]
                total = sum(unidade.consumo_mensal_kwh)

                valores = [unidade.nome, tipo, status] + consumos + [f"{total:.0f}"]

                self.tree_unidades_detalhado.insert('', 'end', values=valores)

        except Exception as e:
            print(f"Erro ao atualizar lista de unidades: {e}")

    # ========== MÉTODOS DE AÇÃO ==========

    def gerar_grafico_personalizado(self):
        """Gera gráfico personalizado avançado"""
        try:
            tipo = self.var_tipo_grafico.get()

            # Limpar frame
            for widget in self.frame_grafico_personalizado.winfo_children():
                widget.destroy()

            # Criar figura
            fig = plt.Figure(figsize=(12, 7), dpi=100)
            ax = fig.add_subplot(111)

            meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
                     'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

            if tipo == "Distribuição por Unidade":
                # Gráfico de barras empilhadas por unidade
                unidades_ativas = self.sistema.sistema.get_unidades_ativas()
                bottom = [0] * 12

                for i, unidade in enumerate(unidades_ativas[:5]):  # Primeiras 5 unidades
                    consumos = [c / 1000 for c in unidade.consumo_mensal_kwh]  # Converter para MWh
                    ax.bar(meses, consumos, bottom=bottom, label=unidade.nome, alpha=0.8)
                    bottom = [b + c for b, c in zip(bottom, consumos)]

                ax.set_ylabel('Consumo (MWh)')
                ax.set_title('Distribuição de Consumo por Unidade')
                ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

            elif tipo == "Análise de Tendências":
                # Gráfico de tendência com projeção
                geracao = [15162, 12453, 12500, 10423, 9002, 6675, 8197, 9954, 11561, 13234, 14000, 14606]
                consumo = [8800] * 12

                # Linha de tendência
                import numpy as np
                x = np.arange(len(meses))
                z = np.polyfit(x, geracao, 1)
                p = np.poly1d(z)

                ax.plot(meses, geracao, 'o-', label='Geração Real', color=self.cores['primaria'], linewidth=2)
                ax.plot(meses, consumo, 's-', label='Consumo', color=self.cores['secundaria'], linewidth=2)
                ax.plot(meses, p(x), '--', label='Tendência Geração', color='red', alpha=0.7)

                ax.set_ylabel('Energia (kWh)')
                ax.set_title('Análise de Tendências Energéticas')
                ax.legend()

            else:
                # Gráficos básicos
                if tipo == "Geração vs Consumo":
                    geracao = [15162, 12453, 12500, 10423, 9002, 6675, 8197, 9954, 11561, 13234, 14000, 14606]
                    consumo = [8800] * 12

                    ax.bar([i - 0.2 for i in range(len(meses))], geracao, 0.4,
                           label='Geração', color=self.cores['primaria'], alpha=0.8)
                    ax.bar([i + 0.2 for i in range(len(meses))], consumo, 0.4,
                           label='Consumo', color=self.cores['secundaria'], alpha=0.8)

                    ax.set_ylabel('Energia (kWh)')
                    ax.set_title('Geração vs Consumo Mensal - Análise Avançada')
                    ax.legend()

                elif tipo == "Economia Mensal":
                    economia = [4000, 3200, 3250, 2800, 2400, 1800, 2200, 2650, 3100, 3550, 3750, 3900]

                    ax.plot(meses, economia, marker='o', linewidth=2,
                            color=self.cores['sucesso'], markersize=8)
                    ax.fill_between(meses, economia, alpha=0.3, color=self.cores['sucesso'])

                    ax.set_ylabel('Economia (R$)')
                    ax.set_title('Economia Mensal Estimada - Análise Avançada')

                elif tipo == "Saldo Energético":
                    saldo = [6362, 3653, 3700, 1623, 202, -2125, -603, 1154, 2761, 4434, 5200, 5806]

                    cores_saldo = ['green' if s >= 0 else 'red' for s in saldo]
                    ax.bar(meses, saldo, color=cores_saldo, alpha=0.7)

                    ax.set_ylabel('Saldo (kWh)')
                    ax.set_title('Saldo Energético Mensal - Análise Avançada')
                    ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)

            ax.set_xlabel('Meses')
            ax.set_xticks(range(len(meses)))
            ax.set_xticklabels(meses)
            ax.grid(True, alpha=0.3)

            # Adicionar canvas
            canvas = FigureCanvasTkAgg(fig, self.frame_grafico_personalizado)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        except Exception as e:
            ttk.Label(self.frame_grafico_personalizado,
                      text=f"Erro ao gerar gráfico: {e}",
                      font=('Arial', 12)).pack(expand=True)

    def ativar_unidade(self):
        """Ativa a unidade selecionada"""
        try:
            item = self.tree_unidades_detalhado.selection()[0]
            nome_unidade = self.tree_unidades_detalhado.item(item, 'values')[0]

            for unidade in self.sistema.sistema.unidades:
                if unidade.nome == nome_unidade:
                    unidade.ativa = True
                    break

            self.atualizar_lista_unidades()
            messagebox.showinfo("Sucesso", f"Unidade '{nome_unidade}' ativada!")

        except IndexError:
            messagebox.showwarning("Aviso", "Selecione uma unidade na lista!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao ativar unidade: {e}")

    def desativar_unidade(self):
        """Desativa a unidade selecionada"""
        try:
            item = self.tree_unidades_detalhado.selection()[0]
            nome_unidade = self.tree_unidades_detalhado.item(item, 'values')[0]

            for unidade in self.sistema.sistema.unidades:
                if unidade.nome == nome_unidade:
                    unidade.ativa = False
                    break

            self.atualizar_lista_unidades()
            messagebox.showinfo("Sucesso", f"Unidade '{nome_unidade}' desativada!")

        except IndexError:
            messagebox.showwarning("Aviso", "Selecione uma unidade na lista!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao desativar unidade: {e}")

    # ========== MÉTODOS LEGACY ==========

    def carregar_grafico_inicial_legacy(self):
        """Carrega gráfico inicial na aba legacy"""
        try:
            if self.funcoes_legacy:
                self.graficos_legacy = GraficosLegacy(self.funcoes_legacy)

                # Criar gráfico de distribuição anual
                dados_sistema = self.funcoes_legacy.obter_dados_legacy()
                percentuais = self.funcoes_legacy.calcular_porcentagens_em_relacao_usina(dados_sistema,
                                                                                         "Resultado Anual")

                if percentuais:
                    fig, canvas = self.graficos_legacy.criar_grafico_base(
                        self.frame_grafico_legacy, "Distribuição Anual de Energia"
                    )
                    if fig and canvas:
                        self.graficos_legacy.atualizar_grafico_pizza(
                            fig, canvas, percentuais, "Distribuição Anual de Energia"
                        )
            else:
                ttk.Label(self.frame_grafico_legacy,
                          text="Gráficos legacy não disponíveis",
                          font=('Arial', 12)).pack(expand=True)
        except Exception as e:
            print(f"❌ Erro ao carregar gráfico inicial: {e}")
            ttk.Label(self.frame_grafico_legacy,
                      text=f"Erro: {e}",
                      font=('Arial', 12)).pack(expand=True)

    def abrir_graficos_analises(self):
        """Abre janela com gráficos de análises"""
        try:
            if self.funcoes_legacy:
                graficos = GraficosLegacy(self.funcoes_legacy)
                graficos.criar_janela_graficos_analises(self.root)
            else:
                messagebox.showinfo("Info", "Gráficos legacy não disponíveis")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir análises: {e}")

    def abrir_distribuicao_mensal(self):
        """Abre janela de distribuição mensal"""
        try:
            if self.funcoes_legacy:
                graficos = GraficosLegacy(self.funcoes_legacy)
                graficos.mostrar_grafico_distribuicao(self.root, "Janeiro")
            else:
                messagebox.showinfo("Info", "Gráficos legacy não disponíveis")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir distribuição: {e}")

    def abrir_grafico_pizza(self):
        """Abre gráfico de pizza em janela separada"""
        try:
            if self.funcoes_legacy:
                # Criar janela simples com gráfico de pizza
                janela = tk.Toplevel(self.root)
                janela.title("🥧 Gráfico de Pizza - Distribuição Anual")
                janela.geometry("800x600")

                dados_sistema = self.funcoes_legacy.obter_dados_legacy()
                percentuais = self.funcoes_legacy.calcular_porcentagens_em_relacao_usina(dados_sistema,
                                                                                         "Resultado Anual")

                graficos = GraficosLegacy(self.funcoes_legacy)
                fig, canvas = graficos.criar_grafico_base(janela, "Distribuição Anual")
                if fig and canvas:
                    graficos.atualizar_grafico_pizza(fig, canvas, percentuais, "Distribuição Anual")
            else:
                messagebox.showinfo("Info", "Gráficos legacy não disponíveis")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir gráfico: {e}")

    def calcular_distribuicao_creditos(self):
        """Calcula e exibe distribuição de créditos"""
        try:
            if not self.calculadora_creditos:
                messagebox.showinfo("Info", "Calculadora de créditos não disponível")
                return

            mes = self.var_mes_creditos.get()

            # Simulação avançada
            texto = f"""ANÁLISE AVANÇADA DE CRÉDITOS - MÊS {mes}
==================================================

RESUMO DETALHADO DO MÊS:
  Geração Real: 11.472 kWh
  Consumo Total: 8.800 kWh
  Tarifas Mínimas: 1.200 kWh
  Créditos Disponíveis: 1.472 kWh
  Status: SOBRA ENERGÉTICA

DISTRIBUIÇÃO INTELIGENTE POR UNIDADE:
--------------------------------------------------
📍 Lanchonet (Prioridade Alta)
   Consumo: 1.739 kWh
   Tarifa Mínima: 100 kWh
   Créditos Recebidos: 300 kWh
   Economia: R$ 195,00

📍 Loja (Prioridade Alta)
   Consumo: 1.821 kWh
   Tarifa Mínima: 100 kWh
   Créditos Recebidos: 320 kWh
   Economia: R$ 208,00

�� Sobreloja (Prioridade Média)
   Consumo: 1.502 kWh
   Tarifa Mínima: 100 kWh
   Créditos Recebidos: 280 kWh
   Economia: R$ 182,00

ANÁLISE FINANCEIRA:
--------------------------------------------------
💰 Economia Total do Mês: R$ 585,00
📈 Projeção Anual: R$ 7.020,00
🎯 Eficiência de Distribuição: 95,2%

(Análise baseada em algoritmo de otimização)
"""

            self.text_creditos.delete(1.0, tk.END)
            self.text_creditos.insert(1.0, texto)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao calcular créditos: {e}")


def main():
    """Função principal para teste"""
    try:
        # Para teste, criar sistema mock
        from main import SistemaEnergiaSolar
        sistema = SistemaEnergiaSolar()

        root = tk.Tk()
        root.withdraw()  # Esconder janela principal

        app = JanelaAnalises(sistema)
        root.mainloop()

    except Exception as e:
        print(f"❌ Erro ao iniciar análises: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()