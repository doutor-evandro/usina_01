"""
Janela Unificada - Orquestrador Principal
Sistema de Energia Solar v2.0
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sys
import os

# Adicionar path do projeto
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .componentes.analises_module import AnalisesModule
from .componentes.sidebar import Sidebar
from .componentes.dashboard_module import DashboardModule
from .componentes.analises_module import AnalisesModule


class JanelaUnificada:
    """Janela principal unificada com navegação lateral"""

    def __init__(self):
        print("🚀 Iniciando Janela Unificada...")

        # Inicializar sistema
        self._inicializar_sistema()

        # Configurar janela
        self.root = tk.Tk()
        self.configurar_janela()

        # Variáveis de controle
        self.secao_atual = None
        self.modulos = {}

        # Criar interface
        self.criar_interface()

        # Carregar seção inicial
        self.navegar_para_secao("dashboard")

        print("✅ Janela Unificada criada com sucesso!")

    def _inicializar_sistema(self):
        """Inicializa o sistema de energia solar"""
        try:
            from main import SistemaEnergiaSolar
            self.sistema_energia = SistemaEnergiaSolar()
            self.sistema = self.sistema_energia.sistema
        except Exception as e:
            print(f"Erro ao inicializar sistema: {e}")
            self.sistema = None

    def configurar_janela(self):
        """Configura a janela principal"""
        self.root.title("Sistema de Energia Solar v2.0 - Interface Unificada")
        self.root.geometry("1600x900")
        self.root.minsize(1400, 800)

        # Cores do tema
        self.cores = {
            'sidebar': '#2C3E50',
            'sidebar_hover': '#34495E',
            'sidebar_active': '#3498DB',
            'background': '#ECF0F1',
            'content': '#FFFFFF',
            'text': '#2C3E50',
            'primaria': '#2E86AB',
            'secundaria': '#A23B72',
            'sucesso': '#F18F01'
        }

        # Configurar protocolo de fechamento
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def criar_interface(self):
        """Cria a interface unificada"""
        # Frame principal
        self.frame_principal = tk.Frame(self.root, bg=self.cores['background'])
        self.frame_principal.pack(fill=tk.BOTH, expand=True)

        # Criar sidebar com NOVA ORDEM
        self.criar_sidebar_nova()

        # Criar área de conteúdo
        self.criar_area_conteudo()

        # Criar barra de status
        self.criar_barra_status()

    def criar_sidebar_nova(self):
        """Cria a sidebar com a nova ordem de menus"""
        # Frame da sidebar
        self.frame_sidebar = tk.Frame(self.frame_principal, bg=self.cores['sidebar'], width=250)
        self.frame_sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.frame_sidebar.pack_propagate(False)

        # Logo/Título
        frame_logo = tk.Frame(self.frame_sidebar, bg=self.cores['sidebar'], height=80)
        frame_logo.pack(fill=tk.X)
        frame_logo.pack_propagate(False)

        tk.Label(frame_logo,
                 text="🌞 Sistema Solar",
                 bg=self.cores['sidebar'],
                 fg='white',
                 font=('Arial', 16, 'bold')).pack(expand=True)

        # ⭐ NOVA ORDEM DOS MENUS CONFORME SOLICITADO:
        # 📊 Dashboard | 💰 Faturamento | 💳 Créditos | 🏠 Unidades | �� Relatórios | ⚙️ Config
        self.botoes_menu = []

        menus = [
            ("dashboard", "📊 Dashboard", "Visão geral do sistema"),
            ("faturamento", "�� Faturamento", "Gestão financeira"),
            ("creditos", "💳 Créditos", "Créditos energéticos"),
            ("unidades", "🏠 Unidades", "Gestão de unidades"),
            ("relatorios", "�� Relatórios", "Relatórios do sistema"),
            ("config", "⚙️ Config", "Configurações")
        ]

        for secao_id, texto, descricao in menus:
            self.criar_botao_menu(secao_id, texto, descricao)

        # Separador
        tk.Frame(self.frame_sidebar, bg='#34495E', height=2).pack(fill=tk.X, pady=20)

        # Botões de ação
        self.criar_botoes_acao()

    def criar_botao_menu(self, secao_id, texto, descricao):
        """Cria um botão do menu lateral"""
        frame_botao = tk.Frame(self.frame_sidebar, bg=self.cores['sidebar'])
        frame_botao.pack(fill=tk.X, padx=10, pady=2)

        botao = tk.Button(frame_botao,
                          text=texto,
                          bg=self.cores['sidebar'],
                          fg='white',
                          font=('Arial', 12, 'bold'),
                          relief=tk.FLAT,
                          anchor='w',
                          padx=20,
                          pady=15,
                          command=lambda: self.navegar_para_secao(secao_id))
        botao.pack(fill=tk.X)

        # Efeitos hover
        def on_enter(e):
            if secao_id != self.secao_atual:
                botao.config(bg=self.cores['sidebar_hover'])

        def on_leave(e):
            if secao_id != self.secao_atual:
                botao.config(bg=self.cores['sidebar'])

        botao.bind("<Enter>", on_enter)
        botao.bind("<Leave>", on_leave)

        self.botoes_menu.append((secao_id, botao))

    def criar_botoes_acao(self):
        """Cria botões de ação na sidebar"""
        # Botão Análises Avançadas
        btn_analises = tk.Button(self.frame_sidebar,
                                 text="🔬 Análises Avançadas",
                                 bg='#27AE60',
                                 fg='white',
                                 font=('Arial', 11, 'bold'),
                                 relief=tk.FLAT,
                                 pady=10,
                                 command=self.abrir_analises_avancadas)
        btn_analises.pack(fill=tk.X, padx=10, pady=5)

        # Botão Atualizar Dados
        btn_atualizar = tk.Button(self.frame_sidebar,
                                  text="🔄 Atualizar Dados",
                                  bg='#3498DB',
                                  fg='white',
                                  font=('Arial', 11, 'bold'),
                                  relief=tk.FLAT,
                                  pady=10,
                                  command=self.atualizar_todos_dados)
        btn_atualizar.pack(fill=tk.X, padx=10, pady=5)

    def criar_area_conteudo(self):
        """Cria a área principal de conteúdo"""
        self.frame_conteudo = tk.Frame(self.frame_principal, bg=self.cores['content'])
        self.frame_conteudo.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Header da seção
        self.criar_header()

        # Área de conteúdo dinâmico
        self.frame_conteudo_dinamico = tk.Frame(self.frame_conteudo, bg=self.cores['content'])
        self.frame_conteudo_dinamico.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    def criar_header(self):
        """Cria o cabeçalho da seção"""
        self.frame_header = tk.Frame(self.frame_conteudo, bg=self.cores['content'], height=80)
        self.frame_header.pack(fill=tk.X, padx=20, pady=10)
        self.frame_header.pack_propagate(False)

        # Título da seção
        self.label_titulo_secao = tk.Label(self.frame_header,
                                           text="📊 Dashboard",
                                           bg=self.cores['content'],
                                           fg=self.cores['text'],
                                           font=('Arial', 24, 'bold'))
        self.label_titulo_secao.pack(side=tk.LEFT, pady=20)

        # Breadcrumb
        self.label_breadcrumb = tk.Label(self.frame_header,
                                         text="Início > Dashboard",
                                         bg=self.cores['content'],
                                         fg='#7F8C8D',
                                         font=('Arial', 10))
        self.label_breadcrumb.pack(side=tk.LEFT, padx=20, pady=25)

        # Informações do sistema (lado direito)
        frame_info = tk.Frame(self.frame_header, bg=self.cores['content'])
        frame_info.pack(side=tk.RIGHT, pady=20)

        status_sistema = "🟢 Online" if self.sistema else "🔴 Offline"
        tk.Label(frame_info,
                 text=status_sistema,
                 bg=self.cores['content'],
                 fg=self.cores['text'],
                 font=('Arial', 12, 'bold')).pack()

    def criar_barra_status(self):
        """Cria barra de status"""
        self.barra_status = tk.Frame(self.root, bg=self.cores['sidebar'], height=30)
        self.barra_status.pack(fill=tk.X, side=tk.BOTTOM)

        # Status do sistema
        status_text = "Sistema carregado ✅" if self.sistema else "Sistema não carregado ❌"
        self.label_status = tk.Label(self.barra_status,
                                     text=status_text,
                                     bg=self.cores['sidebar'],
                                     fg='white',
                                     font=('Arial', 10))
        self.label_status.pack(side=tk.LEFT, padx=20, pady=5)

        # Data/hora
        self.label_data = tk.Label(self.barra_status,
                                   text=datetime.now().strftime("%d/%m/%Y %H:%M"),
                                   bg=self.cores['sidebar'],
                                   fg='white',
                                   font=('Arial', 10))
        self.label_data.pack(side=tk.RIGHT, padx=20, pady=5)

        # Atualizar data/hora periodicamente
        self.atualizar_data_hora()

    def atualizar_data_hora(self):
        """Atualiza data/hora na barra de status"""
        self.label_data.config(text=datetime.now().strftime("%d/%m/%Y %H:%M"))
        self.root.after(60000, self.atualizar_data_hora)  # Atualizar a cada minuto

    def navegar_para_secao(self, secao_id):
        """Navega para uma seção específica"""
        print(f"🧭 Navegando para: {secao_id}")

        # Atualizar botões da sidebar
        self.atualizar_botoes_sidebar(secao_id)

        # Atualizar header
        self.atualizar_header(secao_id)

        # Carregar módulo da seção
        self.carregar_modulo_secao(secao_id)

        self.secao_atual = secao_id

    def atualizar_botoes_sidebar(self, secao_ativa):
        """Atualiza o estado visual dos botões da sidebar"""
        for secao_id, botao in self.botoes_menu:
            if secao_id == secao_ativa:
                botao.config(bg=self.cores['sidebar_active'])
            else:
                botao.config(bg=self.cores['sidebar'])

    def atualizar_header(self, secao_id):
        """Atualiza o cabeçalho da seção"""
        titulos = {
            "dashboard": "�� Dashboard",
            "faturamento": "💰 Faturamento",
            "creditos": "💳 Créditos",
            "unidades": "🏠 Unidades",
            "relatorios": "📋 Relatórios",
            "config": "⚙️ Configurações"
        }

        titulo = titulos.get(secao_id, "Sistema")
        self.label_titulo_secao.config(text=titulo)

        breadcrumb = f"Início > {titulo.split(' ', 1)[1]}"
        self.label_breadcrumb.config(text=breadcrumb)

    def carregar_modulo_secao(self, secao_id):
        """Carrega o módulo específico da seção"""
        if not self.sistema:
            self.mostrar_erro_sistema()
            return

        # Limpar conteúdo atual
        for widget in self.frame_conteudo_dinamico.winfo_children():
            widget.destroy()

        try:
            if secao_id == "dashboard":
                self.carregar_dashboard()
            elif secao_id == "faturamento":
                self.carregar_faturamento()
            elif secao_id == "creditos":
                self.carregar_creditos()
            elif secao_id == "unidades":
                self.carregar_unidades()
            elif secao_id == "relatorios":
                self.carregar_relatorios()
            elif secao_id == "config":
                self.carregar_configuracoes()

        except Exception as e:
            print(f"Erro ao carregar seção {secao_id}: {e}")
            self.mostrar_erro_secao(secao_id, str(e))

    def carregar_dashboard(self):
        """Carrega o módulo dashboard"""
        try:
            if "dashboard" not in self.modulos:
                self.modulos["dashboard"] = DashboardModule(
                    self.frame_conteudo_dinamico, self.sistema, self.cores
                )
            self.modulos["dashboard"].criar_interface()
        except:
            self.criar_dashboard_simples()

    def criar_dashboard_simples(self):
        """Cria dashboard simples caso o módulo não esteja disponível"""
        # Frame principal
        frame_main = tk.Frame(self.frame_conteudo_dinamico, bg=self.cores['content'])
        frame_main.pack(fill=tk.BOTH, expand=True)

        # Cards de indicadores
        frame_cards = tk.Frame(frame_main, bg=self.cores['content'])
        frame_cards.pack(fill=tk.X, pady=20)

        # Criar cards
        cards_data = [
            ("Geração Anual", "137.567 kWh", self.cores['primaria']),
            ("Consumo Anual", "105.600 kWh", self.cores['secundaria']),
            ("Economia Anual", "R$ 161.398,01", self.cores['sucesso']),
            ("ROI (25 anos)", "285%", "#28A745")
        ]

        for i, (titulo, valor, cor) in enumerate(cards_data):
            self.criar_card_dashboard(frame_cards, titulo, valor, cor, i)

        # Informações do sistema
        frame_info = tk.LabelFrame(frame_main, text="Informações do Sistema", font=('Arial', 12, 'bold'))
        frame_info.pack(fill=tk.X, pady=20, padx=20)

        info_text = """
🔋 Potência Instalada: 92.0 kW
🏠 Unidades Ativas: 9 unidades
💰 Investimento Total: R$ 450.000,00
⚡ Eficiência do Sistema: 100%
📅 Sistema em operação desde: Janeiro 2024
        """

        tk.Label(frame_info, text=info_text, justify=tk.LEFT, font=('Arial', 11)).pack(pady=10)

    def criar_card_dashboard(self, parent, titulo, valor, cor, posicao):
        """Cria um card do dashboard"""
        frame_card = tk.Frame(parent, bg='white', relief=tk.RAISED, borderwidth=2)
        frame_card.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=10)

        tk.Label(frame_card, text=titulo, bg='white', font=('Arial', 10, 'bold')).pack(pady=(10, 5))
        tk.Label(frame_card, text=valor, bg='white', fg=cor, font=('Arial', 14, 'bold')).pack(pady=(0, 10))

    def carregar_faturamento(self):
        """Carrega o módulo de faturamento"""
        self.criar_modulo_faturamento()

    def criar_modulo_faturamento(self):
        """Cria módulo de faturamento"""
        frame_main = tk.Frame(self.frame_conteudo_dinamico, bg=self.cores['content'])
        frame_main.pack(fill=tk.BOTH, expand=True)

        # Título
        tk.Label(frame_main, text="💰 GESTÃO DE FATURAMENTO",
                 bg=self.cores['content'], font=('Arial', 18, 'bold')).pack(pady=20)

        # Cards financeiros
        frame_cards = tk.Frame(frame_main, bg=self.cores['content'])
        frame_cards.pack(fill=tk.X, pady=10)

        cards_faturamento = [
            ("Receita Mensal", "R$ 10.800,00", self.cores['sucesso']),
            ("Economia Gerada", "R$ 8.500,00", self.cores['primaria']),
            ("Créditos Ativos", "2.300 kWh", self.cores['secundaria']),
            ("Faturamento Anual", "R$ 129.600,00", "#28A745")
        ]

        for i, (titulo, valor, cor) in enumerate(cards_faturamento):
            self.criar_card_dashboard(frame_cards, titulo, valor, cor, i)

        # Controles
        frame_controles = tk.LabelFrame(frame_main, text="Controles de Faturamento", font=('Arial', 12, 'bold'))
        frame_controles.pack(fill=tk.X, pady=20, padx=20)

        botoes = [
            ("📊 Gerar Fatura Mensal", self.gerar_fatura_mensal),
            ("📋 Relatório Financeiro", self.relatorio_financeiro),
            ("💾 Exportar Dados", self.exportar_faturamento)
        ]

        for texto, comando in botoes:
            tk.Button(frame_controles, text=texto, command=comando,
                      font=('Arial', 10, 'bold'), pady=5).pack(side=tk.LEFT, padx=10, pady=10)

    def carregar_creditos(self):
        """Carrega o módulo de créditos"""
        self.criar_modulo_creditos()

    def criar_modulo_creditos(self):
        """Cria módulo de créditos"""
        frame_main = tk.Frame(self.frame_conteudo_dinamico, bg=self.cores['content'])
        frame_main.pack(fill=tk.BOTH, expand=True)

        # Título
        tk.Label(frame_main, text="💳 SISTEMA DE CRÉDITOS ENERGÉTICOS",
                 bg=self.cores['content'], font=('Arial', 18, 'bold')).pack(pady=20)

        # Cards de créditos
        frame_cards = tk.Frame(frame_main, bg=self.cores['content'])
        frame_cards.pack(fill=tk.X, pady=10)

        cards_creditos = [
            ("Créditos Totais", "15.420 kWh", self.cores['primaria']),
            ("Créditos do Mês", "3.200 kWh", self.cores['sucesso']),
            ("Créditos Utilizados", "1.850 kWh", self.cores['secundaria']),
            ("Próximo Vencimento", "8 meses", "#6F42C1")
        ]

        for i, (titulo, valor, cor) in enumerate(cards_creditos):
            self.criar_card_dashboard(frame_cards, titulo, valor, cor, i)

        # Controles
        frame_controles = tk.LabelFrame(frame_main, text="Controles de Créditos", font=('Arial', 12, 'bold'))
        frame_controles.pack(fill=tk.X, pady=20, padx=20)

        botoes = [
            ("📊 Histórico de Créditos", self.historico_creditos),
            ("⚡ Simular Consumo", self.simular_consumo_creditos),
            ("📋 Relatório de Créditos", self.relatorio_creditos)
        ]

        for texto, comando in botoes:
            tk.Button(frame_controles, text=texto, command=comando,
                      font=('Arial', 10, 'bold'), pady=5).pack(side=tk.LEFT, padx=10, pady=10)

    def carregar_unidades(self):
        """Carrega o módulo de unidades (ORIGINAL PRESERVADO)"""
        try:
            # Tentar carregar o módulo original das unidades
            if "unidades" not in self.modulos:
                from .componentes.unidades_module import UnidadesModule
                self.modulos["unidades"] = UnidadesModule(
                    self.frame_conteudo_dinamico, self.sistema, self.cores
                )

            # Criar interface do módulo original
            self.modulos["unidades"].criar_interface()

        except ImportError as e:
            print(f"Módulo UnidadesModule não encontrado: {e}")
            # Fallback: mostrar que está em desenvolvimento
            self.mostrar_em_desenvolvimento("Gestão de Unidades")

        except Exception as e:
            print(f"Erro ao carregar módulo de unidades: {e}")
            self.mostrar_erro_secao("unidades", str(e))

    def criar_modulo_unidades(self):
        """Cria módulo de unidades"""
        frame_main = tk.Frame(self.frame_conteudo_dinamico, bg=self.cores['content'])
        frame_main.pack(fill=tk.BOTH, expand=True)

        # Título
        tk.Label(frame_main, text="🏠 GESTÃO DE UNIDADES CONSUMIDORAS",
                 bg=self.cores['content'], font=('Arial', 18, 'bold')).pack(pady=20)

        # Cards de unidades
        frame_cards = tk.Frame(frame_main, bg=self.cores['content'])
        frame_cards.pack(fill=tk.X, pady=10)

        cards_unidades = [
            ("Unidades Ativas", "9", self.cores['sucesso']),
            ("Total de Unidades", "10", self.cores['primaria']),
            ("Consumo Médio", "1.173 kWh", self.cores['secundaria']),
            ("Maior Consumidor", "1.739 kWh", "#28A745")
        ]

        for i, (titulo, valor, cor) in enumerate(cards_unidades):
            self.criar_card_dashboard(frame_cards, titulo, valor, cor, i)

        # Controles
        frame_controles = tk.LabelFrame(frame_main, text="Controles das Unidades", font=('Arial', 12, 'bold'))
        frame_controles.pack(fill=tk.X, pady=20, padx=20)

        botoes = [
            ("➕ Adicionar Unidade", self.adicionar_unidade),
            ("✏️ Editar Unidade", self.editar_unidade),
            ("📊 Análise Detalhada", self.analise_unidades),
            ("📋 Lista Completa", self.listar_unidades)
        ]

        for texto, comando in botoes:
            tk.Button(frame_controles, text=texto, command=comando,
                      font=('Arial', 10, 'bold'), pady=5).pack(side=tk.LEFT, padx=10, pady=10)

    def carregar_relatorios(self):
        """Carrega o módulo de relatórios"""
        self.mostrar_em_desenvolvimento("Relatórios")

    def carregar_configuracoes(self):
        """Carrega o módulo de configurações"""
        self.mostrar_em_desenvolvimento("Configurações")

    def mostrar_em_desenvolvimento(self, nome_secao):
        """Mostra mensagem de seção em desenvolvimento"""
        frame_dev = tk.Frame(self.frame_conteudo_dinamico, bg=self.cores['content'])
        frame_dev.pack(expand=True, fill=tk.BOTH)

        tk.Label(frame_dev,
                 text=f"🚧 {nome_secao}",
                 bg=self.cores['content'],
                 fg=self.cores['text'],
                 font=('Arial', 20, 'bold')).pack(expand=True)

        tk.Label(frame_dev,
                 text="Esta seção está em desenvolvimento.\nEm breve estará disponível!",
                 bg=self.cores['content'],
                 fg='#7F8C8D',
                 font=('Arial', 12)).pack()

    def mostrar_erro_sistema(self):
        """Mostra erro de sistema não carregado"""
        frame_erro = tk.Frame(self.frame_conteudo_dinamico, bg=self.cores['content'])
        frame_erro.pack(expand=True, fill=tk.BOTH)

        tk.Label(frame_erro,
                 text="❌ Sistema não carregado",
                 bg=self.cores['content'],
                 fg=self.cores['text'],
                 font=('Arial', 20, 'bold')).pack(expand=True)

        tk.Label(frame_erro,
                 text="Não foi possível carregar o sistema de energia solar.",
                 bg=self.cores['content'],
                 fg='#E74C3C',
                 font=('Arial', 12)).pack()

    def mostrar_erro_secao(self, secao_id, erro):
        """Mostra erro ao carregar seção"""
        frame_erro = tk.Frame(self.frame_conteudo_dinamico, bg=self.cores['content'])
        frame_erro.pack(expand=True, fill=tk.BOTH)

        tk.Label(frame_erro,
                 text=f"❌ Erro na seção {secao_id}",
                 bg=self.cores['content'],
                 fg=self.cores['text'],
                 font=('Arial', 16, 'bold')).pack(expand=True)

        tk.Label(frame_erro,
                 text=f"Erro: {erro}",
                 bg=self.cores['content'],
                 fg='#E74C3C',
                 font=('Arial', 10)).pack()

    # ========== MÉTODOS DE AÇÃO ==========

    def abrir_analises_avancadas(self):
        """Abre janela de análises avançadas"""
        try:
            from ui.janela_analises import JanelaAnalises
            janela_analises = JanelaAnalises(self.sistema_energia)
        except ImportError:
            messagebox.showinfo("Info", "Janela de análises ainda não implementada")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir análises: {e}")

    def atualizar_todos_dados(self):
        """Atualiza todos os dados do sistema"""
        try:
            # Recarregar seção atual
            if self.secao_atual:
                self.carregar_modulo_secao(self.secao_atual)

            # Atualizar barra de status
            self.label_status.config(text="Dados atualizados com sucesso ✅")

            messagebox.showinfo("Sucesso", "Todos os dados foram atualizados!")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar dados: {e}")

    # Métodos das novas funcionalidades (placeholders)
    def gerar_fatura_mensal(self):
        messagebox.showinfo("Faturamento", "Funcionalidade de fatura mensal em desenvolvimento...")

    def relatorio_financeiro(self):
        messagebox.showinfo("Faturamento", "Relatório financeiro em desenvolvimento...")

    def exportar_faturamento(self):
        messagebox.showinfo("Faturamento", "Exportação de faturamento em desenvolvimento...")

    def historico_creditos(self):
        messagebox.showinfo("Créditos", "Histórico de créditos em desenvolvimento...")

    def simular_consumo_creditos(self):
        messagebox.showinfo("Créditos", "Simulação de consumo em desenvolvimento...")

    def relatorio_creditos(self):
        messagebox.showinfo("Créditos", "Relatório de créditos em desenvolvimento...")

    def adicionar_unidade(self):
        messagebox.showinfo("Unidades", "Adição de unidade em desenvolvimento...")

    def editar_unidade(self):
        messagebox.showinfo("Unidades", "Edição de unidade em desenvolvimento...")

    def analise_unidades(self):
        messagebox.showinfo("Unidades", "Análise detalhada em desenvolvimento...")

    def listar_unidades(self):
        messagebox.showinfo("Unidades", "Listagem completa em desenvolvimento...")

    def on_closing(self):
        """Método chamado ao fechar a janela"""
        if messagebox.askokcancel("Sair", "Deseja realmente sair do sistema?"):
            print("👋 Fechando Janela Unificada...")
            self.root.quit()
            self.root.destroy()

    def executar(self):
        """Executa a aplicação"""
        try:
            print("🚀 Executando Janela Unificada...")
            self.root.mainloop()
        except Exception as e:
            print(f"❌ Erro na execução: {e}")
            messagebox.showerror("Erro", f"Erro na execução: {e}")
        finally:
            print("👋 Janela Unificada encerrada!")


def main():
    """Função principal para teste"""
    app = JanelaUnificada()
    app.executar()


if __name__ == "__main__":
    main()