# usina_01/ui/janela_principal.py

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from typing import Optional

from nucleo.modelos import SistemaEnergia
from dados.repositorio import RepositorioDados
from negocio.calculadora_energia import CalculadoraEnergia
from negocio.gerenciador_distribuicao import GerenciadorDistribuicao
from negocio.gerador_relatorios import GeradorRelatorios
from nucleo.excecoes import ErroCarregamentoDados, ErroSalvamentoDados


class JanelaPrincipal:
    """
    Janela principal da aplicação de análise de energia solar.
    Coordena todas as funcionalidades e interfaces do sistema.
    """

    def __init__(self):
        self.root = tk.Tk()
        self.sistema: Optional[SistemaEnergia] = None
        self.repositorio = RepositorioDados()

        # Configuração da janela principal
        self.configurar_janela()
        self.criar_menu()
        self.criar_interface()

        # Carrega dados iniciais
        self.carregar_dados_iniciais()

    def configurar_janela(self):
        """Configura as propriedades básicas da janela principal."""
        self.root.title("Sistema de Análise de Energia Solar - Usina 01")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)

        # Centraliza a janela na tela
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.root.winfo_screenheight() // 2) - (800 // 2)
        self.root.geometry(f"1200x800+{x}+{y}")

        # Configura o comportamento de fechamento
        self.root.protocol("WM_DELETE_WINDOW", self.ao_fechar)

    def criar_menu(self):
        """Cria a barra de menu da aplicação."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Menu Arquivo
        menu_arquivo = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=menu_arquivo)
        menu_arquivo.add_command(label="Novo Sistema", command=self.novo_sistema)
        menu_arquivo.add_command(label="Abrir...", command=self.abrir_arquivo)
        menu_arquivo.add_command(label="Salvar", command=self.salvar_dados)
        menu_arquivo.add_command(label="Salvar Como...", command=self.salvar_como)
        menu_arquivo.add_separator()
        menu_arquivo.add_command(label="Exportar Relatório...", command=self.exportar_relatorio)
        menu_arquivo.add_separator()
        menu_arquivo.add_command(label="Sair", command=self.ao_fechar)

        # Menu Ferramentas
        menu_ferramentas = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ferramentas", menu=menu_ferramentas)
        menu_ferramentas.add_command(label="Configurar Sistema", command=self.abrir_configuracao_sistema)
        menu_ferramentas.add_command(label="Gerenciar Unidades", command=self.abrir_gerenciador_unidades)
        menu_ferramentas.add_command(label="Inserir Consumos", command=self.abrir_painel_consumo)
        menu_ferramentas.add_separator()
        menu_ferramentas.add_command(label="Atualizar Cálculos", command=self.atualizar_calculos)

        # Menu Ajuda
        menu_ajuda = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ajuda", menu=menu_ajuda)
        menu_ajuda.add_command(label="Sobre", command=self.mostrar_sobre)

    def criar_interface(self):
        """Cria a interface principal da aplicação."""
        # Frame principal com padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configura redimensionamento
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Título
        titulo_label = ttk.Label(main_frame, text="Sistema de Análise de Energia Solar",
                                 font=("Arial", 16, "bold"))
        titulo_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Frame esquerdo - Controles
        controles_frame = ttk.LabelFrame(main_frame, text="Controles", padding="10")
        controles_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))

        # Botões de ação
        ttk.Button(controles_frame, text="Configurar Sistema",
                   command=self.abrir_configuracao_sistema, width=20).pack(pady=5, fill=tk.X)

        ttk.Button(controles_frame, text="Gerenciar Unidades",
                   command=self.abrir_gerenciador_unidades, width=20).pack(pady=5, fill=tk.X)

        ttk.Button(controles_frame, text="Inserir Consumos",
                   command=self.abrir_painel_consumo, width=20).pack(pady=5, fill=tk.X)

        ttk.Separator(controles_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        ttk.Button(controles_frame, text="Atualizar Cálculos",
                   command=self.atualizar_calculos, width=20).pack(pady=5, fill=tk.X)

        ttk.Button(controles_frame, text="Gerar Relatório",
                   command=self.gerar_relatorio, width=20).pack(pady=5, fill=tk.X)

        ttk.Separator(controles_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        ttk.Button(controles_frame, text="Salvar Dados",
                   command=self.salvar_dados, width=20).pack(pady=5, fill=tk.X)

        # Frame direito - Informações
        info_frame = ttk.LabelFrame(main_frame, text="Informações do Sistema", padding="10")
        info_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Notebook para abas de informações
        self.notebook = ttk.Notebook(info_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Aba Resumo
        self.frame_resumo = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_resumo, text="Resumo")

        # Text widget para mostrar informações
        self.text_resumo = tk.Text(self.frame_resumo, wrap=tk.WORD, font=("Consolas", 10))
        scrollbar_resumo = ttk.Scrollbar(self.frame_resumo, orient=tk.VERTICAL, command=self.text_resumo.yview)
        self.text_resumo.configure(yscrollcommand=scrollbar_resumo.set)

        self.text_resumo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_resumo.pack(side=tk.RIGHT, fill=tk.Y)

        # Aba Relatório
        self.frame_relatorio = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_relatorio, text="Relatório Completo")

        self.text_relatorio = tk.Text(self.frame_relatorio, wrap=tk.WORD, font=("Consolas", 9))
        scrollbar_relatorio = ttk.Scrollbar(self.frame_relatorio, orient=tk.VERTICAL, command=self.text_relatorio.yview)
        self.text_relatorio.configure(yscrollcommand=scrollbar_relatorio.set)

        self.text_relatorio.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_relatorio.pack(side=tk.RIGHT, fill=tk.Y)

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Sistema carregado. Pronto para uso.")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))

    def carregar_dados_iniciais(self):
        """Carrega os dados iniciais do sistema."""
        try:
            self.sistema = self.repositorio.carregar_sistema()
            self.atualizar_interface()
            self.status_var.set("Dados carregados com sucesso.")
        except ErroCarregamentoDados as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados: {e}")
            self.status_var.set("Erro ao carregar dados.")

    def atualizar_interface(self):
        """Atualiza todas as informações exibidas na interface."""
        if not self.sistema:
            return

        # Atualiza resumo
        self.atualizar_resumo()

        # Atualiza relatório se a aba estiver selecionada
        if self.notebook.index(self.notebook.select()) == 1:
            self.atualizar_relatorio()

    def atualizar_resumo(self):
        """Atualiza o resumo do sistema."""
        if not self.sistema:
            self.text_resumo.delete(1.0, tk.END)
            self.text_resumo.insert(tk.END, "Nenhum sistema carregado.")
            return

        try:
            calculadora = CalculadoraEnergia(self.sistema)
            gerenciador = GerenciadorDistribuicao(self.sistema)

            # Calcula dados principais
            _, resumo_anual = calculadora.calcular_resultados_anuais()
            _, resumo_fin_anual = gerenciador.calcular_resultados_financeiros_anuais()

            # Monta texto do resumo
            resumo = f"""RESUMO DO SISTEMA DE ENERGIA SOLAR
{'=' * 50}

CONFIGURAÇÃO:
• Potência Inversor: {self.sistema.configuracao.potencia_inversor:,.0f} W
• Potência Módulos: {self.sistema.configuracao.potencia_modulos:,.0f} W
• Eficiência: {self.sistema.configuracao.eficiencia:.1f}%
• Valor kWh: R\$ {self.sistema.configuracao.valor_kwh:.4f}

UNIDADES CONSUMIDORAS:
• Total de Unidades: {len(self.sistema.unidades)}
"""

            for unidade in self.sistema.unidades:
                resumo += f"• {unidade.codigo} - {unidade.nome} ({unidade.tipo_ligacao.value.upper()})\n"

            resumo += f"""
RESULTADOS ANUAIS:
• Geração Total: {resumo_anual.geracao_total_kwh:,.2f} kWh
• Consumo Total: {resumo_anual.consumo_total_kwh:,.2f} kWh
• Autossuficiência: {resumo_anual.percentual_autossuficiencia:.1f}%
• Economia Total: R\$ {resumo_fin_anual.economia_total_reais:,.2f}
• Economia Percentual: {resumo_fin_anual.percentual_economia:.1f}%
• Economia Mensal Média: R\$ {resumo_fin_anual.economia_total_reais / 12:,.2f}

STATUS: Sistema operacional e calculado.
"""

            self.text_resumo.delete(1.0, tk.END)
            self.text_resumo.insert(tk.END, resumo)

        except Exception as e:
            self.text_resumo.delete(1.0, tk.END)
            self.text_resumo.insert(tk.END, f"Erro ao calcular resumo: {e}")

    def atualizar_relatorio(self):
        """Atualiza o relatório completo."""
        if not self.sistema:
            self.text_relatorio.delete(1.0, tk.END)
            self.text_relatorio.insert(tk.END, "Nenhum sistema carregado.")
            return

        try:
            gerador = GeradorRelatorios(self.sistema)
            relatorio_texto = gerador.gerar_relatorio_texto()

            self.text_relatorio.delete(1.0, tk.END)
            self.text_relatorio.insert(tk.END, relatorio_texto)

        except Exception as e:
            self.text_relatorio.delete(1.0, tk.END)
            self.text_relatorio.insert(tk.END, f"Erro ao gerar relatório: {e}")

    # Métodos de ação dos botões e menus
    def novo_sistema(self):
        """Cria um novo sistema."""
        resposta = messagebox.askyesno("Novo Sistema",
                                       "Isso criará um novo sistema e perderá os dados não salvos. Continuar?")
        if resposta:
            # Aqui você implementaria a criação de um novo sistema
            messagebox.showinfo("Info", "Funcionalidade 'Novo Sistema' será implementada.")

    def abrir_arquivo(self):
        """Abre um arquivo de dados."""
        arquivo = filedialog.askopenfilename(
            title="Abrir arquivo de dados",
            filetypes=[("Arquivos JSON", "*.json"), ("Todos os arquivos", "*.*")]
        )
        if arquivo:
            try:
                self.repositorio = RepositorioDados(arquivo)
                self.sistema = self.repositorio.carregar_sistema()
                self.atualizar_interface()
                self.status_var.set(f"Arquivo carregado: {os.path.basename(arquivo)}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao abrir arquivo: {e}")

    def salvar_dados(self):
        """Salva os dados atuais."""
        if not self.sistema:
            messagebox.showwarning("Aviso", "Nenhum sistema carregado para salvar.")
            return

        try:
            self.repositorio.salvar_sistema(self.sistema)
            self.status_var.set("Dados salvos com sucesso.")
            messagebox.showinfo("Sucesso", "Dados salvos com sucesso!")
        except ErroSalvamentoDados as e:
            messagebox.showerror("Erro", f"Erro ao salvar dados: {e}")

    def salvar_como(self):
        """Salva os dados em um novo arquivo."""
        if not self.sistema:
            messagebox.showwarning("Aviso", "Nenhum sistema carregado para salvar.")
            return

        arquivo = filedialog.asksaveasfilename(
            title="Salvar como",
            defaultextension=".json",
            filetypes=[("Arquivos JSON", "*.json"), ("Todos os arquivos", "*.*")]
        )
        if arquivo:
            try:
                novo_repositorio = RepositorioDados(arquivo)
                novo_repositorio.salvar_sistema(self.sistema)
                self.repositorio = novo_repositorio
                self.status_var.set(f"Dados salvos em: {os.path.basename(arquivo)}")
                messagebox.showinfo("Sucesso", "Dados salvos com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar arquivo: {e}")

    def exportar_relatorio(self):
        """Exporta o relatório para um arquivo de texto."""
        if not self.sistema:
            messagebox.showwarning("Aviso", "Nenhum sistema carregado.")
            return

        arquivo = filedialog.asksaveasfilename(
            title="Exportar relatório",
            defaultextension=".txt",
            filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")]
        )
        if arquivo:
            try:
                gerador = GeradorRelatorios(self.sistema)
                relatorio_texto = gerador.gerar_relatorio_texto()

                with open(arquivo, 'w', encoding='utf-8') as f:
                    f.write(relatorio_texto)

                messagebox.showinfo("Sucesso", f"Relatório exportado para: {os.path.basename(arquivo)}")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao exportar relatório: {e}")

    def abrir_configuracao_sistema(self):
        """Abre a janela de configuração do sistema."""
        messagebox.showinfo("Info", "Janela de configuração será implementada.")

    def abrir_gerenciador_unidades(self):
        """Abre o gerenciador de unidades."""
        messagebox.showinfo("Info", "Gerenciador de unidades será implementado.")

    def abrir_painel_consumo(self):
        """Abre o painel de inserção de consumos."""
        messagebox.showinfo("Info", "Painel de consumo será implementado.")

    def atualizar_calculos(self):
        """Atualiza todos os cálculos e a interface."""
        if self.sistema:
            self.atualizar_interface()
            self.status_var.set("Cálculos atualizados.")
        else:
            messagebox.showwarning("Aviso", "Nenhum sistema carregado.")

    def gerar_relatorio(self):
        """Gera e exibe o relatório completo."""
        if self.sistema:
            self.notebook.select(1)  # Seleciona a aba do relatório
            self.atualizar_relatorio()
            self.status_var.set("Relatório gerado.")
        else:
            messagebox.showwarning("Aviso", "Nenhum sistema carregado.")

    def mostrar_sobre(self):
        """Mostra informações sobre o sistema."""
        sobre_texto = """Sistema de Análise de Energia Solar - Usina 01
Versão 1.0

Desenvolvido para análise e gerenciamento de sistemas
de energia solar fotovoltaica com múltiplas unidades
consumidoras.

Funcionalidades:
• Configuração de sistema solar
• Gerenciamento de unidades consumidoras
• Cálculos energéticos e financeiros
• Geração de relatórios completos
• Análise de payback

© 2025 - Sistema Usina 01"""

        messagebox.showinfo("Sobre", sobre_texto)

    def ao_fechar(self):
        """Ação executada ao fechar a aplicação."""
        resposta = messagebox.askyesnocancel("Sair", "Deseja salvar os dados antes de sair?")
        if resposta is True:  # Sim
            self.salvar_dados()
            self.root.destroy()
        elif resposta is False:  # Não
            self.root.destroy()
        # Se Cancel, não faz nada (não fecha)

    def executar(self):
        """Inicia o loop principal da aplicação."""
        self.root.mainloop()


# --- Bloco de Teste ---
if __name__ == "__main__":
    print("--- Teste: ui/janela_principal.py ---")
    print("Iniciando interface gráfica...")

    try:
        app = JanelaPrincipal()
        print("✓ Interface criada com sucesso!")
        print("✓ Dados carregados!")
        print("Executando aplicação... (Feche a janela para continuar)")
        app.executar()
        print("✓ Aplicação encerrada com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao executar interface: {e}")

    print("Teste de Janela Principal concluído!")