# usina_01/ui/graficos/gerenciador_graficos.py

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Callable
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

from nucleo.modelos import SistemaEnergia
from ui.graficos.graficos_analise import GraficosAnalise

# Configuração do Matplotlib
plt.style.use('default')
plt.rcParams['font.size'] = 9
plt.rcParams['axes.grid'] = True
plt.rcParams['grid.alpha'] = 0.3


class GerenciadorGraficos:
    """
    Gerenciador principal para visualização de gráficos do sistema.
    Coordena a criação e exibição de diferentes tipos de análises gráficas.
    """

    def __init__(self, parent: tk.Tk, sistema: SistemaEnergia):
        self.parent = parent
        self.sistema = sistema
        self.graficos_analise = GraficosAnalise(sistema)

        # Cria a janela
        self.janela = tk.Toplevel(parent)
        self.configurar_janela()
        self.criar_interface()
        self.carregar_grafico_inicial()

    def configurar_janela(self):
        """Configura as propriedades da janela."""
        self.janela.title("Análise Gráfica - Sistema de Energia Solar")
        self.janela.geometry("1100x750")
        self.janela.resizable(True, True)

        # Centraliza a janela
        self.janela.update_idletasks()
        x = (self.janela.winfo_screenwidth() // 2) - (1100 // 2)
        y = (self.janela.winfo_screenheight() // 2) - (750 // 2)
        self.janela.geometry(f"1100x750+{x}+{y}")

        # Torna a janela modal
        self.janela.transient(self.parent)
        self.janela.grab_set()

        # Foca na janela
        self.janela.focus_set()

    def criar_interface(self):
        """Cria a interface da janela."""
        # Frame principal
        main_frame = ttk.Frame(self.janela, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        titulo_label = ttk.Label(main_frame, text="Análise Gráfica - Sistema de Energia Solar",
                                 font=("Arial", 16, "bold"))
        titulo_label.pack(pady=(0, 15))

        # Frame para controles
        controles_frame = ttk.LabelFrame(main_frame, text="Tipos de Análise", padding="10")
        controles_frame.pack(fill=tk.X, pady=(0, 10))

        # Primeira linha de botões
        linha1_frame = ttk.Frame(controles_frame)
        linha1_frame.pack(fill=tk.X, pady=(0, 5))

        ttk.Button(linha1_frame, text="📊 Geração vs Consumo",
                   command=self.mostrar_geracao_consumo, width=22).pack(side=tk.LEFT, padx=(0, 5))

        ttk.Button(linha1_frame, text="💰 Economia Mensal",
                   command=self.mostrar_economia_mensal, width=22).pack(side=tk.LEFT, padx=(0, 5))

        ttk.Button(linha1_frame, text="⚡ Saldo Energético",
                   command=self.mostrar_saldo_energetico, width=22).pack(side=tk.LEFT, padx=(0, 5))

        ttk.Button(linha1_frame, text="🥧 Distribuição Unidades",
                   command=self.mostrar_distribuicao_unidades, width=22).pack(side=tk.LEFT, padx=(0, 5))

        # Segunda linha de botões
        linha2_frame = ttk.Frame(controles_frame)
        linha2_frame.pack(fill=tk.X, pady=(0, 5))

        ttk.Button(linha2_frame, text="📈 Análise Financeira",
                   command=self.mostrar_analise_financeira, width=22).pack(side=tk.LEFT, padx=(0, 5))

        ttk.Button(linha2_frame, text="🔄 Comparativo Anual",
                   command=self.mostrar_comparativo_anual, width=22).pack(side=tk.LEFT, padx=(0, 5))

        ttk.Button(linha2_frame, text="⚙️ Eficiência Sistema",
                   command=self.mostrar_eficiencia_sistema, width=22).pack(side=tk.LEFT, padx=(0, 5))

        ttk.Button(linha2_frame, text="💾 Salvar Gráfico",
                   command=self.salvar_grafico, width=22).pack(side=tk.LEFT, padx=(0, 5))

        # Frame para informações do gráfico atual
        info_frame = ttk.LabelFrame(main_frame, text="Informações do Gráfico", padding="5")
        info_frame.pack(fill=tk.X, pady=(0, 10))

        self.info_grafico_var = tk.StringVar()
        self.info_grafico_var.set("Selecione um tipo de gráfico para visualizar")
        ttk.Label(info_frame, textvariable=self.info_grafico_var,
                  font=("Arial", 10)).pack(anchor=tk.W)

        # Frame para o gráfico
        grafico_frame = ttk.LabelFrame(main_frame, text="Visualização", padding="5")
        grafico_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Cria a figura do matplotlib
        self.figura = Figure(figsize=(13, 7), dpi=100, facecolor='white')
        self.canvas = FigureCanvasTkAgg(self.figura, grafico_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Toolbar de navegação
        toolbar_frame = ttk.Frame(grafico_frame)
        toolbar_frame.pack(fill=tk.X, pady=(5, 0))

        self.toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        self.toolbar.update()

        # Frame para botões principais
        botoes_frame = ttk.Frame(main_frame)
        botoes_frame.pack(fill=tk.X)

        ttk.Button(botoes_frame, text="🔄 Atualizar Dados",
                   command=self.atualizar_dados).pack(side=tk.LEFT)

        ttk.Button(botoes_frame, text="❓ Ajuda",
                   command=self.mostrar_ajuda).pack(side=tk.LEFT, padx=(10, 0))

        ttk.Button(botoes_frame, text="✖️ Fechar",
                   command=self.janela.destroy).pack(side=tk.RIGHT)

        # Variável para controlar o gráfico atual
        self.grafico_atual = None

    def limpar_grafico(self):
        """Limpa o gráfico atual."""
        self.figura.clear()
        self.canvas.draw()

    def atualizar_info_grafico(self, titulo: str, descricao: str):
        """Atualiza as informações do gráfico atual."""
        info = f"{titulo} - {descricao}"
        self.info_grafico_var.set(info)

    def carregar_grafico_inicial(self):
        """Carrega o gráfico inicial."""
        self.mostrar_geracao_consumo()

    def mostrar_geracao_consumo(self):
        """Mostra gráfico de geração vs consumo."""
        try:
            self.limpar_grafico()
            self.grafico_atual = "geracao_consumo"

            self.atualizar_info_grafico(
                "Geração vs Consumo",
                "Comparação mensal entre energia gerada pelo sistema solar e consumo total das unidades"
            )

            ax = self.figura.add_subplot(111)
            self.graficos_analise.criar_grafico_geracao_consumo(ax)

            self.figura.tight_layout()
            self.canvas.draw()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar gráfico: {e}")

    def mostrar_economia_mensal(self):
        """Mostra gráfico de economia mensal."""
        try:
            self.limpar_grafico()
            self.grafico_atual = "economia_mensal"

            self.atualizar_info_grafico(
                "Economia Mensal",
                "Economia financeira mensal proporcionada pelo sistema de energia solar"
            )

            ax = self.figura.add_subplot(111)
            self.graficos_analise.criar_grafico_economia_mensal(ax)

            self.figura.tight_layout()
            self.canvas.draw()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar gráfico: {e}")

    def mostrar_saldo_energetico(self):
        """Mostra gráfico de saldo energético."""
        try:
            self.limpar_grafico()
            self.grafico_atual = "saldo_energetico"

            self.atualizar_info_grafico(
                "Saldo Energético",
                "Diferença mensal entre geração e consumo (valores positivos = excesso, negativos = déficit)"
            )

            ax = self.figura.add_subplot(111)
            self.graficos_analise.criar_grafico_saldo_energetico(ax)

            self.figura.tight_layout()
            self.canvas.draw()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar gráfico: {e}")

    def mostrar_distribuicao_unidades(self):
        """Mostra gráfico de distribuição por unidades."""
        try:
            self.limpar_grafico()
            self.grafico_atual = "distribuicao_unidades"

            self.atualizar_info_grafico(
                "Distribuição por Unidades",
                "Percentual de consumo de cada unidade consumidora em relação ao total"
            )

            ax = self.figura.add_subplot(111)
            self.graficos_analise.criar_grafico_distribuicao_unidades(ax)

            self.figura.tight_layout()
            self.canvas.draw()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar gráfico: {e}")

    def mostrar_analise_financeira(self):
        """Mostra gráfico de análise financeira."""
        try:
            self.limpar_grafico()
            self.grafico_atual = "analise_financeira"

            self.atualizar_info_grafico(
                "Análise Financeira",
                "Economia mensal e acumulada ao longo do ano"
            )

            ax1 = self.figura.add_subplot(111)
            ax2 = ax1.twinx()
            self.graficos_analise.criar_grafico_analise_financeira(ax1, ax2)

            self.figura.tight_layout()
            self.canvas.draw()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar gráfico: {e}")

    def mostrar_comparativo_anual(self):
        """Mostra gráfico comparativo anual."""
        try:
            self.limpar_grafico()
            self.grafico_atual = "comparativo_anual"

            self.atualizar_info_grafico(
                "Comparativo Anual",
                "Comparação de custos mensais com e sem sistema de energia solar"
            )

            ax = self.figura.add_subplot(111)
            self.graficos_analise.criar_grafico_comparativo_anual(ax)

            self.figura.tight_layout()
            self.canvas.draw()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar gráfico: {e}")

    def mostrar_eficiencia_sistema(self):
        """Mostra gráfico de eficiência do sistema."""
        try:
            self.limpar_grafico()
            self.grafico_atual = "eficiencia_sistema"

            self.atualizar_info_grafico(
                "Eficiência do Sistema",
                "Percentual de autossuficiência energética mensal do sistema"
            )

            ax = self.figura.add_subplot(111)
            self.graficos_analise.criar_grafico_eficiencia_sistema(ax)

            self.figura.tight_layout()
            self.canvas.draw()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar gráfico: {e}")

    def salvar_grafico(self):
        """Salva o gráfico atual."""
        try:
            if not self.grafico_atual:
                messagebox.showwarning("Aviso", "Nenhum gráfico para salvar.")
                return

            from tkinter import filedialog

            arquivo = filedialog.asksaveasfilename(
                title="Salvar Gráfico",
                defaultextension=".png",
                filetypes=[
                    ("PNG files", "*.png"),
                    ("PDF files", "*.pdf"),
                    ("SVG files", "*.svg"),
                    ("JPG files", "*.jpg")
                ]
            )

            if arquivo:
                self.figura.savefig(arquivo, dpi=300, bbox_inches='tight',
                                    facecolor='white', edgecolor='none')
                messagebox.showinfo("Sucesso", f"Gráfico salvo em:\n{arquivo}")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar gráfico: {e}")

    def atualizar_dados(self):
        """Atualiza os dados e recarrega o gráfico atual."""
        try:
            # Recria o objeto de análise
            self.graficos_analise = GraficosAnalise(self.sistema)

            # Recarrega o gráfico atual
            if self.grafico_atual == "geracao_consumo":
                self.mostrar_geracao_consumo()
            elif self.grafico_atual == "economia_mensal":
                self.mostrar_economia_mensal()
            elif self.grafico_atual == "saldo_energetico":
                self.mostrar_saldo_energetico()
            elif self.grafico_atual == "distribuicao_unidades":
                self.mostrar_distribuicao_unidades()
            elif self.grafico_atual == "analise_financeira":
                self.mostrar_analise_financeira()
            elif self.grafico_atual == "comparativo_anual":
                self.mostrar_comparativo_anual()
            elif self.grafico_atual == "eficiencia_sistema":
                self.mostrar_eficiencia_sistema()
            else:
                self.carregar_grafico_inicial()

            messagebox.showinfo("Sucesso", "Dados atualizados com sucesso!")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar dados: {e}")

    def mostrar_ajuda(self):
        """Mostra ajuda sobre os gráficos."""
        ajuda_texto = """AJUDA - ANÁLISE GRÁFICA

TIPOS DE GRÁFICOS DISPONÍVEIS:

📊 Geração vs Consumo
   Compara a energia gerada pelo sistema solar com o consumo total mensal.

💰 Economia Mensal  
   Mostra a economia financeira proporcionada pelo sistema a cada mês.

⚡ Saldo Energético
   Exibe a diferença entre geração e consumo (excesso ou déficit).

🥧 Distribuição por Unidades
   Gráfico de pizza mostrando o percentual de consumo de cada unidade.

📈 Análise Financeira
   Economia mensal e acumulada ao longo do ano.

🔄 Comparativo Anual
   Comparação de custos com e sem energia solar.

⚙️ Eficiência do Sistema
   Percentual de autossuficiência energética mensal.

CONTROLES:
• Use a toolbar para navegar, fazer zoom e configurar o gráfico
• Clique em "Salvar Gráfico" para exportar em alta resolução
• "Atualizar Dados" recarrega informações do sistema

DICAS:
• Gráficos são atualizados automaticamente quando dados mudam
• Formatos de exportação: PNG, PDF, SVG, JPG
• Use zoom para analisar períodos específicos"""

        messagebox.showinfo("Ajuda - Gráficos", ajuda_texto)


# --- Bloco de Teste ---
# usina_01/ui/graficos/gerenciador_graficos.py

# ... (código anterior, mantenha tudo igual até o if __name__ == "__main__":) ...

# --- Bloco de Teste ---
if __name__ == "__main__":
    print("--- Teste: ui/graficos/gerenciador_graficos.py ---")

    # Importa dados de exemplo para teste
    from configuracao.definicoes import CONFIG_EXEMPLO, UNIDADES_EXEMPLO, CONSUMOS_EXEMPLO
    from nucleo.modelos import SistemaEnergia  # Importar SistemaEnergia aqui também

    # Cria sistema de teste
    sistema_teste = SistemaEnergia(
        configuracao=CONFIG_EXEMPLO,
        unidades=UNIDADES_EXEMPLO,
        consumos=CONSUMOS_EXEMPLO
    )

    # Cria janela principal para teste
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal

    print("Abrindo gerenciador de gráficos...")
    try:
        gerenciador = GerenciadorGraficos(root, sistema_teste)

        print("✓ Gerenciador de gráficos criado!")
        print("✓ Interface carregada!")
        print("Interaja com a janela... (Feche para continuar)")
        print("Dicas:")
        print("  - Teste todos os tipos de gráfico")
        print("  - Use a toolbar para navegar")
        print("  - Experimente salvar um gráfico")

        root.mainloop()  # Mantém a janela aberta

        print("Teste de Gerenciador de Gráficos concluído!")

    except Exception as e:
        print(f"❌ ERRO FATAL AO INICIALIZAR GRÁFICOS: {e}")
        import traceback

        traceback.print_exc()  # Imprime o traceback completo para depuração
        messagebox.showerror("Erro Fatal", f"Ocorreu um erro inesperado ao abrir os gráficos: {e}")
    finally:
        root.destroy()  # Garante que a janela principal seja fechada no final