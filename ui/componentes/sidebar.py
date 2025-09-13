"""
Componente Sidebar para navegação
"""

import tkinter as tk
from datetime import datetime


class Sidebar:
    """Componente de barra lateral para navegação"""

    def __init__(self, parent, callback_navegacao, cores=None):
        self.parent = parent
        self.callback_navegacao = callback_navegacao
        self.cores = cores or self._cores_padrao()
        self.botoes_nav = {}
        self.secao_atual = None

        self.criar_sidebar()

    def _cores_padrao(self):
        """Cores padrão da sidebar"""
        return {
            'sidebar': '#2C3E50',
            'sidebar_hover': '#34495E',
            'sidebar_active': '#3498DB'
        }

    def criar_sidebar(self):
        """Cria a barra lateral"""
        self.frame_sidebar = tk.Frame(self.parent,
                                      bg=self.cores['sidebar'],
                                      width=250)
        self.frame_sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.frame_sidebar.pack_propagate(False)

        # Título
        self.criar_titulo()

        # Separador
        self.criar_separador()

        # Botões de navegação
        self.criar_botoes_navegacao()

        # Espaçador
        tk.Frame(self.frame_sidebar, bg=self.cores['sidebar']).pack(expand=True)

        # Informações do sistema
        self.criar_info_sistema()

    def criar_titulo(self):
        """Cria o título da sidebar"""
        titulo = tk.Label(self.frame_sidebar,
                          text="⚡ Energia Solar\nv2.0 Unificado",
                          bg=self.cores['sidebar'],
                          fg='white',
                          font=('Arial', 16, 'bold'),
                          justify=tk.CENTER)
        titulo.pack(pady=20)

    def criar_separador(self):
        """Cria separador visual"""
        separador = tk.Frame(self.frame_sidebar,
                             height=2,
                             bg=self.cores['sidebar_hover'])
        separador.pack(fill=tk.X, padx=20, pady=10)

    def criar_botoes_navegacao(self):
        """Cria os botões de navegação"""
        secoes = [
            ("dashboard", "�� Dashboard", "Visão geral do sistema"),
            ("analises", "📈 Análises", "Gráficos e tendências"),
            ("unidades", "🏠 Unidades", "Gestão de unidades"),
            ("creditos", "💰 Créditos", "Distribuição de créditos"),
            ("configuracoes", "⚙️ Configurações", "Parâmetros do sistema"),
            ("relatorios", "📋 Relatórios", "Geração de relatórios")
        ]

        for secao_id, texto, descricao in secoes:
            self.criar_botao_navegacao(secao_id, texto, descricao)

    def criar_botao_navegacao(self, secao_id, texto, descricao):
        """Cria um botão de navegação"""
        frame_botao = tk.Frame(self.frame_sidebar, bg=self.cores['sidebar'])
        frame_botao.pack(fill=tk.X, padx=10, pady=2)

        botao = tk.Button(frame_botao,
                          text=texto,
                          bg=self.cores['sidebar'],
                          fg='white',
                          font=('Arial', 12, 'bold'),
                          bd=0,
                          padx=20,
                          pady=15,
                          anchor='w',
                          command=lambda: self.navegar_para(secao_id))

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

        self.botoes_nav[secao_id] = botao

    def criar_info_sistema(self):
        """Cria informações do sistema no rodapé"""
        info_sistema = tk.Label(self.frame_sidebar,
                                text="Sistema Ativo\n🟢 Online",
                                bg=self.cores['sidebar'],
                                fg='#2ECC71',
                                font=('Arial', 10))
        info_sistema.pack(pady=20)

    def navegar_para(self, secao_id):
        """Navega para uma seção específica"""
        self.atualizar_botao_ativo(secao_id)
        self.callback_navegacao(secao_id)

    def atualizar_botao_ativo(self, secao_ativa):
        """Atualiza o visual do botão ativo"""
        for secao_id, botao in self.botoes_nav.items():
            if secao_id == secao_ativa:
                botao.config(bg=self.cores['sidebar_active'])
            else:
                botao.config(bg=self.cores['sidebar'])

        self.secao_atual = secao_ativa