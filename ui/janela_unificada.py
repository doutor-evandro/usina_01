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

        # Criar sidebar
        self.sidebar = Sidebar(self.frame_principal, self.navegar_para_secao, self.cores)

        # Criar área de conteúdo
        self.criar_area_conteudo()

        # Criar barra de status
        self.criar_barra_status()

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

    def navegar_para_secao(self, secao_id):
        """Navega para uma seção específica"""
        print(f"🧭 Navegando para: {secao_id}")

        # Atualizar header
        self.atualizar_header(secao_id)

        # Carregar módulo da seção
        self.carregar_modulo_secao(secao_id)

        self.secao_atual = secao_id

    def atualizar_header(self, secao_id):
        """Atualiza o cabeçalho da seção"""
        titulos = {
            "dashboard": "📊 Dashboard",
            "analises": "📈 Análises Avançadas",
            "unidades": "🏠 Gestão de Unidades",
            "creditos": "💰 Análise de Créditos",
            "configuracoes": "⚙️ Configurações",
            "relatorios": "📋 Relatórios"
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
            elif secao_id == "analises":
                self.carregar_analises()
            elif secao_id == "unidades":
                self.carregar_unidades()
            elif secao_id == "creditos":
                self.carregar_creditos()
            elif secao_id == "configuracoes":
                self.carregar_configuracoes()
            elif secao_id == "relatorios":
                self.carregar_relatorios()

        except Exception as e:
            print(f"Erro ao carregar seção {secao_id}: {e}")
            self.mostrar_erro_secao(secao_id, str(e))

    def carregar_dashboard(self):
        """Carrega o módulo dashboard"""
        if "dashboard" not in self.modulos:
            self.modulos["dashboard"] = DashboardModule(
                self.frame_conteudo_dinamico, self.sistema, self.cores
            )

        self.modulos["dashboard"].criar_interface()

    def carregar_analises(self):
        """Carrega o módulo de análises"""
        if "analises" not in self.modulos:
            self.modulos["analises"] = AnalisesModule(
                self.frame_conteudo_dinamico, self.sistema, self.cores
            )

        self.modulos["analises"].criar_interface()

    def carregar_unidades(self):
        """Carrega o módulo de unidades"""
        if "unidades" not in self.modulos:
            from .componentes.unidades_module import UnidadesModule
            self.modulos["unidades"] = UnidadesModule(
                self.frame_conteudo_dinamico, self.sistema, self.cores
            )

        self.modulos["unidades"].criar_interface()

    def carregar_creditos(self):
        """Carrega o módulo de créditos"""
        # Implementar módulo de créditos
        self.mostrar_em_desenvolvimento("Análise de Créditos")

    def carregar_configuracoes(self):
        """Carrega o módulo de configurações"""
        # Reutilizar da janela_principal
        self.mostrar_em_desenvolvimento("Configurações")

    def carregar_relatorios(self):
        """Carrega o módulo de relatórios"""
        # Reutilizar da janela_principal
        self.mostrar_em_desenvolvimento("Relatórios")

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