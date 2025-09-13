"""
Módulo Gestão de Unidades - CRUD e controle completo com dados reais - VERSÃO FINAL CORRIGIDA
"""

import tkinter as tk
from tkinter import ttk, messagebox
from .base_module import BaseModule


class UnidadesModule(BaseModule):
    """Módulo responsável pela gestão completa de unidades"""

    def __init__(self, parent_frame, sistema, cores=None):
        super().__init__(parent_frame, sistema, cores)
        self.unidade_selecionada = None
        self.dados_unidades = self._carregar_dados_reais()

    def _carregar_dados_reais(self):
        """Carrega dados reais das unidades e consumos com persistência"""
        try:
            import json
            import os

            # ✅ TENTAR: Carregar dados salvos do arquivo
            if os.path.exists("dados/unidades_sistema.json"):
                print("📂 Carregando dados salvos do arquivo...")
                with open("dados/unidades_sistema.json", "r", encoding="utf-8") as arquivo:
                    dados_salvos = json.load(arquivo)
                    print(f"✅ Dados carregados: {len(dados_salvos.get('unidades', []))} unidades")
                    return dados_salvos
            else:
                print("📝 Arquivo não encontrado, usando dados padrão...")

        except Exception as e:
            print(f"⚠️ Erro ao carregar arquivo, usando dados padrão: {e}")

        # ✅ FALLBACK: Dados padrão se não conseguir carregar do arquivo
        return {
            "unidades": [
                {"codigo": "112761577", "nome": "Lanchonet", "tipo": "tri", "endereco": "Av. Pres Getulio Vargas 1890",
                 "ativa": True},
                {"codigo": "114789592", "nome": "My Beach", "tipo": "tri",
                 "endereco": "Av. Pres Getulio Vargas 1890 - Mybeach", "ativa": True},
                {"codigo": "104775009", "nome": "Loja", "tipo": "tri", "endereco": "R. Guilherme Casteletto 34 - loja",
                 "ativa": True},
                {"codigo": "94926239", "nome": "Sobreloja", "tipo": "tri",
                 "endereco": "R. Guilherme Casteletto 34 - sobreloja1", "ativa": True},
                {"codigo": "101839405", "nome": "Casa Adriano", "tipo": "bi", "endereco": "R Luiz Roncalha, 198",
                 "ativa": True},
                {"codigo": "95268278", "nome": "Depósito", "tipo": "tri", "endereco": "R. Apucarana 125",
                 "ativa": True},
                {"codigo": "70796270", "nome": "Fernando Lomas", "tipo": "tri", "endereco": "R. Sertanopolis 465",
                 "ativa": True},
                {"codigo": "81788541", "nome": "Mário 1", "tipo": "tri", "endereco": "R. Santa Fé 218 - Sala 02",
                 "ativa": True},
                {"codigo": "76103684", "nome": "Mário 2", "tipo": "bi", "endereco": "R. Santa Fé 218 - Sala 01",
                 "ativa": True}
            ],
            "consumos": {
                "112761577": {"Janeiro": 1739, "Fevereiro": 1739, "Março": 1739, "Abril": 1739, "Maio": 1739,
                              "Junho": 1739, "Julho": 1739, "Agosto": 1739, "Setembro": 1739, "Outubro": 1739,
                              "Novembro": 1739, "Dezembro": 1739},
                "114789592": {"Janeiro": 500, "Fevereiro": 500, "Março": 500, "Abril": 500, "Maio": 500, "Junho": 500,
                              "Julho": 500, "Agosto": 500, "Setembro": 500, "Outubro": 500, "Novembro": 500,
                              "Dezembro": 500},
                "104775009": {"Janeiro": 1454, "Fevereiro": 2346, "Março": 2486, "Abril": 1955, "Maio": 1682,
                              "Junho": 1220, "Julho": 1341, "Agosto": 1208, "Setembro": 1849, "Outubro": 1845,
                              "Novembro": 2181, "Dezembro": 2282},
                "94926239": {"Janeiro": 701, "Fevereiro": 1944, "Março": 2184, "Abril": 1824, "Maio": 1646,
                             "Junho": 1115, "Julho": 1186, "Agosto": 1014, "Setembro": 1504, "Outubro": 1572,
                             "Novembro": 1635, "Dezembro": 1697},
                "101839405": {"Janeiro": 663, "Fevereiro": 731, "Março": 847, "Abril": 705, "Maio": 542, "Junho": 352,
                              "Julho": 384, "Agosto": 376, "Setembro": 539, "Outubro": 540, "Novembro": 452,
                              "Dezembro": 750},
                "95268278": {"Janeiro": 176, "Fevereiro": 202, "Março": 387, "Abril": 286, "Maio": 269, "Junho": 213,
                             "Julho": 216, "Agosto": 173, "Setembro": 185, "Outubro": 251, "Novembro": 245,
                             "Dezembro": 277},
                "70796270": {"Janeiro": 650, "Fevereiro": 1239, "Março": 1307, "Abril": 1082, "Maio": 795, "Junho": 803,
                             "Julho": 519, "Agosto": 844, "Setembro": 924, "Outubro": 971, "Novembro": 1018,
                             "Dezembro": 1016},
                "81788541": {"Janeiro": 1000, "Fevereiro": 1000, "Março": 1000, "Abril": 1000, "Maio": 1000,
                             "Junho": 1000, "Julho": 1000, "Agosto": 1000, "Setembro": 1000, "Outubro": 1000,
                             "Novembro": 1000, "Dezembro": 1000},
                "76103684": {"Janeiro": 500, "Fevereiro": 500, "Março": 500, "Abril": 500, "Maio": 500, "Junho": 500,
                             "Julho": 500, "Agosto": 500, "Setembro": 500, "Outubro": 500, "Novembro": 500,
                             "Dezembro": 500}
            }
        }

    def criar_interface(self):
        """Cria a interface de gestão de unidades"""
        print("🏠 Criando interface de gestão de unidades...")
        self.limpar_frame()

        try:
            # Criar layout principal
            self._criar_dashboard_unidades()
            self._criar_area_principal()

            print("✅ Interface de gestão de unidades criada!")

        except Exception as e:
            print(f"❌ Erro ao criar gestão de unidades: {e}")
            import traceback
            traceback.print_exc()
            self._criar_unidades_simples()

    def _criar_dashboard_unidades(self):
        """✅ CORRIGIDO: Dashboard com 5 cards e formatação brasileira"""
        frame_dashboard = tk.LabelFrame(self.parent_frame, text="📊 Resumo Geral das Unidades",
                                        font=('Arial', 14, 'bold'), bg=self.cores['content'])
        frame_dashboard.pack(fill=tk.X, padx=10, pady=10)

        # ✅ GRID: Para 5 colunas
        frame_indicadores = tk.Frame(frame_dashboard, bg=self.cores['content'])
        frame_indicadores.pack(fill=tk.X, padx=10, pady=10)

        for i in range(5):
            frame_indicadores.columnconfigure(i, weight=1)

        # ✅ CALCULAR: Dados reais das unidades ativas
        dados_calculados = self._calcular_dados_unidades()

        # ✅ CARDS: 5 indicadores
        self.card_ativas, self.label_ativas = self.criar_card(
            frame_indicadores, "Unidades Ativas", str(dados_calculados['unidades_ativas']), '#2ECC71', 0, 0)

        self.card_consumo_medio, self.label_consumo_medio = self.criar_card(
            frame_indicadores, "Consumo Médio Mensal",
            f"{dados_calculados['consumo_medio_mensal']:,.0f} kWh".replace(',', '.'), self.cores['secundaria'], 0, 1)

        self.card_consumo_anual, self.label_consumo_anual = self.criar_card(
            frame_indicadores, "Consumo Total Anual",
            f"{dados_calculados['consumo_total_anual']:,.0f} kWh".replace(',', '.'), self.cores['primaria'], 0, 2)

        self.card_receita_mensal, self.label_receita_mensal = self.criar_card(
            frame_indicadores, "Receita Mensal", self._formatar_moeda(dados_calculados['receita_mensal']),
            self.cores['sucesso'], 0, 3)

        self.card_receita_anual, self.label_receita_anual = self.criar_card(
            frame_indicadores, "Receita Anual", self._formatar_moeda(dados_calculados['receita_anual']), '#9C27B0', 0,
            4)

    def _formatar_moeda(self, valor):
        """✅ NOVO: Formata valores em moeda brasileira"""
        try:
            # Formatar com separadores brasileiros
            valor_formatado = f"R\$ {valor:,.2f}"
            # Trocar separadores para padrão brasileiro
            valor_formatado = valor_formatado.replace(',', 'X').replace('.', ',').replace('X', '.')
            return valor_formatado
        except:
            return "R\$ 0,00"

    def _calcular_dados_unidades(self):
        """✅ CORRIGIDO: Cálculo correto da receita com formatação brasileira"""
        try:
            # ✅ CONFIGURAÇÕES: Tarifas e limites mínimos
            tarifa_cooperativa = 0.39  # R\$/kWh
            limite_bifasico = 50  # kWh mínimo
            limite_trifasico = 100  # kWh mínimo

            # ✅ FILTRAR: Apenas unidades ativas
            unidades_ativas = [u for u in self.dados_unidades["unidades"] if u["ativa"]]
            qtd_unidades_ativas = len(unidades_ativas)

            # ✅ CALCULAR: Consumos e receita
            consumo_total_anual = 0
            receita_total_anual = 0

            print("💰 Calculando receita da cooperativa:")

            for unidade in unidades_ativas:
                codigo = unidade["codigo"]
                nome = unidade["nome"]
                tipo = unidade["tipo"]  # "tri" ou "bi"

                if codigo in self.dados_unidades["consumos"]:
                    consumos_mensais = self.dados_unidades["consumos"][codigo]
                    consumo_anual_unidade = sum(consumos_mensais.values())
                    consumo_total_anual += consumo_anual_unidade

                    # ✅ CALCULAR: Receita anual da unidade
                    receita_anual_unidade = 0

                    for mes, consumo_mes in consumos_mensais.items():
                        # ✅ CORRIGIDO: Definir limite mínimo baseado no tipo
                        limite_minimo = limite_trifasico if tipo == "tri" else limite_bifasico

                        # ✅ CORRIGIDO: Calcular consumo faturável (acima do mínimo)
                        consumo_faturavel = max(0, consumo_mes - limite_minimo)

                        # ✅ CORRIGIDO: Receita da cooperativa para este mês
                        receita_mes_unidade = consumo_faturavel * tarifa_cooperativa
                        receita_anual_unidade += receita_mes_unidade

                    receita_total_anual += receita_anual_unidade

                    print(
                        f"   • {nome} ({tipo}): {consumo_anual_unidade:,.0f} kWh → R\$ {receita_anual_unidade:,.2f}/ano")

            # ✅ CALCULAR: Médias
            consumo_medio_mensal = consumo_total_anual / 12 if consumo_total_anual > 0 else 0
            receita_media_mensal = receita_total_anual / 12 if receita_total_anual > 0 else 0

            print(f"\n📊 RESUMO FINAL:")
            print(f"   • Unidades ativas: {qtd_unidades_ativas}")
            print(f"   • Consumo total anual: {consumo_total_anual:,.0f} kWh")
            print(f"   • Consumo médio mensal: {consumo_medio_mensal:,.0f} kWh")
            print(f"   • Receita total anual: R\$ {receita_total_anual:,.2f}")
            print(f"   • Receita média mensal: R\$ {receita_media_mensal:,.2f}")

            return {
                'unidades_ativas': qtd_unidades_ativas,
                'consumo_total_anual': consumo_total_anual,
                'consumo_medio_mensal': consumo_medio_mensal,
                'receita_mensal': receita_media_mensal,
                'receita_anual': receita_total_anual
            }

        except Exception as e:
            print(f"❌ Erro ao calcular dados das unidades: {e}")
            import traceback
            traceback.print_exc()
            return {
                'unidades_ativas': 0,
                'consumo_total_anual': 0,
                'consumo_medio_mensal': 0,
                'receita_mensal': 0,
                'receita_anual': 0
            }

    def _criar_area_principal(self):
        """Cria área principal com lista e controles"""
        # Frame principal dividido
        frame_principal = tk.Frame(self.parent_frame, bg=self.cores['content'])
        frame_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Lado esquerdo - Lista de unidades
        self._criar_lista_unidades(frame_principal)

        # Lado direito - Detalhes e controles
        self._criar_painel_controles(frame_principal)

    def _criar_lista_unidades(self, parent):
        """✅ LIMPO: Cria lista de unidades sem botão atualizar desnecessário"""
        frame_lista = tk.LabelFrame(parent, text="📋 Lista de Unidades Cadastradas",
                                    font=('Arial', 12, 'bold'))
        frame_lista.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        # ✅ BARRA DE FERRAMENTAS: Apenas botões essenciais
        toolbar = tk.Frame(frame_lista)
        toolbar.pack(fill=tk.X, padx=10, pady=5)

        # ✅ BOTÕES ESSENCIAIS: Apenas os realmente necessários
        btn_nova = ttk.Button(toolbar, text="➕ Nova Unidade", command=self._nova_unidade)
        btn_nova.pack(side=tk.LEFT, padx=5)

        btn_editar = ttk.Button(toolbar, text="✏️ Editar", command=self._editar_unidade)
        btn_editar.pack(side=tk.LEFT, padx=5)

        btn_remover = ttk.Button(toolbar, text="🗑️ Remover", command=self._remover_unidade)
        btn_remover.pack(side=tk.LEFT, padx=5)

        # ✅ REMOVIDO: btn_atualizar (era redundante)

        # ✅ NOVO: Status da última atualização (informativo)
        self.label_status_lista = tk.Label(toolbar, text="✅ Dados atualizados",
                                           fg='#666666', font=('Arial', 9))
        self.label_status_lista.pack(side=tk.RIGHT, padx=10)

        print("✅ Botões da toolbar criados (sem atualizar)")

        # Treeview com dados das unidades
        frame_tree = tk.Frame(frame_lista)
        frame_tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Colunas
        colunas = ('Código', 'Nome', 'Tipo', 'Status', 'Consumo Mensal', 'Consumo Anual')
        self.tree_unidades = ttk.Treeview(frame_tree, columns=colunas, show='headings', height=12)

        # Configurar colunas
        self.tree_unidades.heading('Código', text='Código UC')
        self.tree_unidades.heading('Nome', text='Nome da Unidade')
        self.tree_unidades.heading('Tipo', text='Tipo')
        self.tree_unidades.heading('Status', text='Status')
        self.tree_unidades.heading('Consumo Mensal', text='Consumo Médio/Mês')
        self.tree_unidades.heading('Consumo Anual', text='Consumo Anual')

        # Larguras das colunas
        self.tree_unidades.column('Código', width=100)
        self.tree_unidades.column('Nome', width=120)
        self.tree_unidades.column('Tipo', width=60)
        self.tree_unidades.column('Status', width=80)
        self.tree_unidades.column('Consumo Mensal', width=120)
        self.tree_unidades.column('Consumo Anual', width=120)

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tree, orient=tk.VERTICAL, command=self.tree_unidades.yview)
        self.tree_unidades.configure(yscrollcommand=scrollbar.set)

        # Pack
        self.tree_unidades.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind para seleção
        self.tree_unidades.bind('<<TreeviewSelect>>', self._on_unidade_selecionada)
        self.tree_unidades.bind('<Double-1>', self._on_duplo_clique)

        print("✅ TreeView configurado com eventos")

    def _criar_painel_controles(self, parent):
        """Cria painel de controles e detalhes"""
        frame_controles = tk.LabelFrame(parent, text="🔧 Controles e Detalhes",
                                        font=('Arial', 12, 'bold'))
        frame_controles.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        # Detalhes da unidade selecionada
        frame_detalhes = tk.LabelFrame(frame_controles, text="📋 Detalhes da Unidade",
                                       font=('Arial', 11, 'bold'))
        frame_detalhes.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.text_detalhes = tk.Text(frame_detalhes, wrap=tk.WORD, height=8, font=('Courier', 9))
        scroll_detalhes = ttk.Scrollbar(frame_detalhes, orient=tk.VERTICAL,
                                        command=self.text_detalhes.yview)
        self.text_detalhes.configure(yscrollcommand=scroll_detalhes.set)

        self.text_detalhes.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scroll_detalhes.pack(side=tk.RIGHT, fill=tk.Y, pady=10)

        # Mensagem inicial
        self.text_detalhes.insert(1.0, "📋 Selecione uma unidade na lista\npara ver os detalhes completos...")

        # Ações rápidas
        frame_acoes = tk.LabelFrame(frame_controles, text="⚡ Ações Rápidas",
                                    font=('Arial', 11, 'bold'))
        frame_acoes.pack(fill=tk.X, padx=10, pady=10)

        # Botões de ação
        btn_frame = tk.Frame(frame_acoes)
        btn_frame.pack(fill=tk.X, padx=10, pady=10)

        self.btn_ativar = ttk.Button(btn_frame, text="🟢 Ativar",
                                     command=self._ativar_unidade, state=tk.DISABLED)
        self.btn_ativar.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        self.btn_desativar = ttk.Button(btn_frame, text="🔴 Desativar",
                                        command=self._desativar_unidade, state=tk.DISABLED)
        self.btn_desativar.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        print("✅ Botões de ação criados")

        # Gráfico de consumo da unidade
        frame_grafico = tk.LabelFrame(frame_controles, text="📊 Consumo Mensal da Unidade",
                                      font=('Arial', 11, 'bold'))
        frame_grafico.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.frame_grafico_unidade = tk.Frame(frame_grafico)
        self.frame_grafico_unidade.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Mensagem inicial no gráfico
        tk.Label(self.frame_grafico_unidade,
                 text="📊 Selecione uma unidade\npara ver o gráfico de consumo",
                 font=('Arial', 10), fg='gray').pack(expand=True)

        # Carregar dados iniciais
        self._carregar_unidades()

    def _carregar_unidades(self):
        """✅ MELHORADO: Carrega unidades com diferenciação visual sutil para inativas"""
        try:
            print("🔄 Carregando unidades...")

            # Limpar lista
            for item in self.tree_unidades.get_children():
                self.tree_unidades.delete(item)

            # ✅ CONFIGURAR: Tags para diferenciação visual
            self.tree_unidades.tag_configure('ativa', foreground='#000000')  # Preto normal
            self.tree_unidades.tag_configure('inativa', foreground='#757575',
                                             font=('Arial', 9, 'italic'))  # Cinza + itálico

            # Carregar dados reais
            for unidade in self.dados_unidades["unidades"]:
                codigo = unidade["codigo"]
                nome = unidade["nome"]
                tipo = "Trifásica" if unidade["tipo"] == "tri" else "Bifásica"
                status = "🟢 Ativa" if unidade["ativa"] else "🔴 Inativa"

                # Calcular consumos
                if codigo in self.dados_unidades["consumos"]:
                    consumos_mensais = list(self.dados_unidades["consumos"][codigo].values())
                    consumo_medio_mensal = sum(consumos_mensais) / len(consumos_mensais)
                    consumo_anual = sum(consumos_mensais)
                else:
                    consumo_medio_mensal = 0
                    consumo_anual = 0

                # ✅ MELHORADO: Inserir com tag baseada no status
                tag_status = 'ativa' if unidade["ativa"] else 'inativa'

                item_id = self.tree_unidades.insert('', 'end', values=(
                    codigo,
                    nome,
                    tipo,
                    status,
                    f"{consumo_medio_mensal:.0f} kWh",
                    f"{consumo_anual:,} kWh"
                ), tags=(tag_status,))

                print(f"✅ Unidade carregada: {nome} - {codigo}")

        except Exception as e:
            print(f"❌ Erro ao carregar unidades: {e}")
            import traceback
            traceback.print_exc()

    def _on_unidade_selecionada(self, event):
        """✅ TOTALMENTE CORRIGIDO: Evento quando uma unidade é selecionada"""
        try:
            print("🔄 Unidade selecionada - evento disparado")

            selection = self.tree_unidades.selection()
            if not selection:
                print("❌ Nenhuma seleção encontrada")
                return

            item = self.tree_unidades.item(selection[0])
            valores = item['values']

            if not valores:
                print("❌ Valores vazios na seleção")
                return

            codigo = str(valores[0])  # ✅ GARANTIR que é string
            nome = valores[1]

            print(f"✅ Unidade selecionada: {nome} ({codigo})")
            print(f"🔍 Buscando código: '{codigo}' nos dados...")
            print(f"🔍 Códigos disponíveis: {list(self.dados_unidades['consumos'].keys())}")

            # ✅ CORRIGIDO: Definir unidade_selecionada IMEDIATAMENTE
            self.unidade_selecionada = valores

            # Habilitar botões
            self.btn_ativar.config(state=tk.NORMAL)
            self.btn_desativar.config(state=tk.NORMAL)

            # ✅ CORRIGIDO: Buscar dados completos da unidade
            unidade_dados = None
            for unidade in self.dados_unidades["unidades"]:
                if str(unidade["codigo"]) == codigo:  # ✅ COMPARAÇÃO STRING-STRING
                    unidade_dados = unidade
                    break

            if unidade_dados:
                print(f"✅ Dados da unidade encontrados: {unidade_dados['nome']}")

                # ✅ CORRIGIDO: Buscar consumos
                consumos = self.dados_unidades["consumos"].get(codigo, {})
                print(f"✅ Consumos encontrados: {len(consumos)} meses")

                consumo_total = sum(consumos.values()) if consumos else 0
                consumo_medio = consumo_total / 12 if consumos else 0
                economia_anual = consumo_total * 0.65

                # ✅ CORRIGIDO: Mostrar detalhes formatados (sem escape sequences)
                detalhes = f"""UNIDADE SELECIONADA: {unidade_dados['nome']}
{'=' * 60}

🆔 Código UC: {unidade_dados['codigo']}
🏠 Nome: {unidade_dados['nome']}
🏢 Tipo: {'Trifásica' if unidade_dados['tipo'] == 'tri' else 'Bifásica'}
📍 Endereço: {unidade_dados['endereco']}
📊 Status: {'🟢 Ativa' if unidade_dados['ativa'] else '🔴 Inativa'}

CONSUMO ENERGÉTICO:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ Consumo Médio Mensal: {consumo_medio:.0f} kWh
📊 Consumo Total Anual: {consumo_total:,} kWh
💰 Economia Potencial/Ano: R\$ {economia_anual:,.2f}

INFORMAÇÕES TÉCNICAS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔌 Grupo Tarifário: {'B3 (Comercial)' if unidade_dados['tipo'] == 'tri' else 'B1 (Residencial)'}
💵 Tarifa Aplicada: R\$ 0,65/kWh
📋 Modalidade: Compensação de Energia Elétrica
🔄 Medição: Convencional

HISTÓRICO DE CONSUMO (kWh):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

                # Adicionar consumos mensais se existirem
                if consumos:
                    meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                             'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']

                    for i, mes in enumerate(meses):
                        if i % 3 == 0:  # Nova linha a cada 3 meses
                            detalhes += "\n"
                        consumo_mes = consumos.get(mes, 0)
                        detalhes += f"{mes[:3]}: {consumo_mes:4d} kWh  "

                # Atualizar texto
                self.text_detalhes.delete(1.0, tk.END)
                self.text_detalhes.insert(1.0, detalhes)

                print("✅ Detalhes atualizados")

                # Criar gráfico da unidade
                self._criar_grafico_unidade(unidade_dados['nome'], codigo)

            else:
                print(f"❌ Dados da unidade {codigo} não encontrados")
                print(f"🔍 Códigos nas unidades: {[u['codigo'] for u in self.dados_unidades['unidades']]}")

                # Mostrar erro nos detalhes
                self.text_detalhes.delete(1.0, tk.END)
                self.text_detalhes.insert(1.0,
                                          f"❌ Erro: Dados da unidade {codigo} não encontrados.\n\nVerifique os logs para mais detalhes.")

        except Exception as e:
            print(f"❌ Erro ao selecionar unidade: {e}")
            import traceback
            traceback.print_exc()

    def _criar_grafico_unidade(self, nome_unidade, codigo):
        """✅ CORRIGIDO: Cria gráfico de consumo da unidade selecionada com dados reais"""
        try:
            print(f"📊 Criando gráfico para {nome_unidade} ({codigo})")

            # Limpar frame
            for widget in self.frame_grafico_unidade.winfo_children():
                widget.destroy()

            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

            fig = plt.Figure(figsize=(6, 4), dpi=80, facecolor='white')
            ax = fig.add_subplot(111)

            # ✅ CORRIGIDO: Buscar dados reais de consumo
            consumos = self.dados_unidades["consumos"].get(str(codigo), {})
            print(f"📊 Dados de consumo encontrados: {len(consumos)} registros")

            if consumos:
                meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
                         'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
                meses_completos = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                                   'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']

                valores_consumo = [consumos.get(mes_completo, 0) for mes_completo in meses_completos]
                print(f"📊 Valores de consumo: {valores_consumo}")

                # Criar gráfico de barras
                bars = ax.bar(meses, valores_consumo, color=self.cores['primaria'], alpha=0.7,
                              edgecolor='black', linewidth=0.5)

                # Configurações do gráfico
                ax.set_title(f'Consumo Mensal - {nome_unidade}', fontsize=10, fontweight='bold')
                ax.set_ylabel('Consumo (kWh)', fontsize=9)
                ax.tick_params(axis='x', labelsize=8, rotation=45)
                ax.tick_params(axis='y', labelsize=8)
                ax.grid(True, alpha=0.3, axis='y')

                # Adicionar valores nas barras (apenas valores significativos)
                max_valor = max(valores_consumo) if valores_consumo else 0
                for bar, valor in zip(bars, valores_consumo):
                    if valor > max_valor * 0.1:  # Mostrar apenas valores > 10% do máximo
                        height = bar.get_height()
                        ax.text(bar.get_x() + bar.get_width() / 2., height + max_valor * 0.02,
                                f'{valor}', ha='center', va='bottom', fontsize=7, fontweight='bold')

                # Adicionar linha de média
                media = sum(valores_consumo) / len(valores_consumo) if valores_consumo else 0
                ax.axhline(y=media, color='red', linestyle='--', alpha=0.7, linewidth=2,
                           label=f'Média: {media:.0f} kWh')
                ax.legend(fontsize=8)

                print(f"✅ Gráfico criado com {len(valores_consumo)} pontos de dados")

            else:
                # Sem dados
                ax.text(0.5, 0.5, 'Sem dados de consumo\ndisponíveis',
                        ha='center', va='center', transform=ax.transAxes,
                        fontsize=12, bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray"))
                ax.set_title(f'Consumo - {nome_unidade}', fontsize=10, fontweight='bold')
                print("⚠️ Sem dados de consumo para esta unidade")

            fig.tight_layout()

            canvas = FigureCanvasTkAgg(fig, self.frame_grafico_unidade)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

            print("✅ Gráfico adicionado ao frame")

        except Exception as e:
            print(f"❌ Erro ao criar gráfico da unidade: {e}")
            import traceback
            traceback.print_exc()

            # Mostrar erro no frame
            for widget in self.frame_grafico_unidade.winfo_children():
                widget.destroy()
            tk.Label(self.frame_grafico_unidade,
                     text="❌ Erro ao carregar gráfico\nVerifique os logs",
                     font=('Arial', 10), fg='red').pack(expand=True)

    def _on_duplo_clique(self, event):
        """Evento de duplo clique"""
        print("🖱️ Duplo clique detectado - editando unidade")
        self._editar_unidade()

    def _nova_unidade(self):
        """Abre janela para criar nova unidade"""
        print("➕ Abrindo janela para nova unidade")
        try:
            self._abrir_janela_unidade("Nova Unidade", None)
        except Exception as e:
            print(f"❌ Erro ao abrir nova unidade: {e}")
            messagebox.showerror("Erro", f"Erro ao abrir janela: {e}")

    def _editar_unidade(self, event=None):
        """Edita unidade selecionada"""
        print("✏️ Tentando editar unidade")
        try:
            if not self.unidade_selecionada:
                print("⚠️ Nenhuma unidade selecionada")
                messagebox.showwarning("Aviso", "Selecione uma unidade para editar.")
                return

            print(f"✏️ Editando unidade: {self.unidade_selecionada[1]}")
            self._abrir_janela_unidade("Editar Unidade", self.unidade_selecionada)

        except Exception as e:
            print(f"❌ Erro ao editar unidade: {e}")
            messagebox.showerror("Erro", f"Erro ao editar: {e}")

    def _remover_unidade(self):
        """✅ CORRIGIDO: Remove unidade selecionada do sistema"""
        print("🗑️ Tentando remover unidade")
        try:
            if not self.unidade_selecionada:
                print("⚠️ Nenhuma unidade selecionada para remoção")
                messagebox.showwarning("Aviso", "Selecione uma unidade para remover.")
                return

            codigo_unidade = str(self.unidade_selecionada[0])
            nome_unidade = self.unidade_selecionada[1]
            print(f"🗑️ Removendo unidade: {nome_unidade} ({codigo_unidade})")

            # ✅ CONFIRMAÇÃO: Mostrar detalhes da unidade antes de remover
            unidade_dados = None
            for unidade in self.dados_unidades["unidades"]:
                if str(unidade["codigo"]) == codigo_unidade:
                    unidade_dados = unidade
                    break

            if unidade_dados:
                # Calcular dados para mostrar no resumo
                consumos = self.dados_unidades["consumos"].get(codigo_unidade, {})
                total_anual = sum(consumos.values()) if consumos else 0

                confirmacao = f"""🗑️ CONFIRMAR REMOÇÃO:

    🏠 Nome: {nome_unidade}
    🆔 Código UC: {codigo_unidade}
    🏢 Tipo: {'Trifásica' if unidade_dados['tipo'] == 'tri' else 'Bifásica'}
    📍 Endereço: {unidade_dados['endereco']}
    📊 Consumo Anual: {total_anual:,} kWh

    ⚠️ ATENÇÃO: Esta ação não pode ser desfeita!
    Todos os dados de consumo também serão removidos.

    Deseja realmente remover esta unidade?"""

                resposta = messagebox.askyesno("Confirmar Remoção", confirmacao)

                if resposta:
                    print(f"✅ Remoção confirmada para: {nome_unidade}")

                    # ✅ REMOVER: Unidade da lista de unidades
                    unidades_atualizadas = []
                    for unidade in self.dados_unidades["unidades"]:
                        if str(unidade["codigo"]) != codigo_unidade:
                            unidades_atualizadas.append(unidade)

                    self.dados_unidades["unidades"] = unidades_atualizadas
                    print(f"✅ Unidade removida da lista de unidades")

                    # ✅ REMOVER: Consumos da unidade
                    if codigo_unidade in self.dados_unidades["consumos"]:
                        del self.dados_unidades["consumos"][codigo_unidade]
                        print(f"✅ Consumos da unidade removidos")

                    # ✅ SALVAR: Dados atualizados no arquivo
                    self._salvar_dados_em_arquivo()

                    # ✅ ATUALIZAR: Interface
                    self._atualizar_lista()

                    # ✅ LIMPAR: Seleção atual
                    self.unidade_selecionada = None

                    # ✅ FEEDBACK: Sucesso
                    messagebox.showinfo("Sucesso",
                                        f"✅ Unidade '{nome_unidade}' removida com sucesso!\n\n"
                                        f"🗑️ Código UC: {codigo_unidade}\n"
                                        f"📊 {len(consumos)} meses de consumo removidos")

                    print(f"✅ Remoção concluída com sucesso: {nome_unidade}")

                else:
                    print("❌ Remoção cancelada pelo usuário")
            else:
                print(f"❌ Dados da unidade {codigo_unidade} não encontrados")
                messagebox.showerror("Erro", f"Dados da unidade '{nome_unidade}' não encontrados!")

        except Exception as e:
            print(f"❌ Erro ao remover unidade: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Erro", f"Erro ao remover unidade: {e}")

    def _ativar_unidade(self):
        """✅ CORRIGIDO: Ativa unidade selecionada no sistema"""
        print("🟢 Tentando ativar unidade")
        try:
            if not self.unidade_selecionada:
                print("⚠️ Nenhuma unidade selecionada para ativação")
                messagebox.showwarning("Aviso", "Selecione uma unidade para ativar.")
                return

            codigo_unidade = str(self.unidade_selecionada[0])
            nome_unidade = self.unidade_selecionada[1]
            print(f"🟢 Ativando unidade: {nome_unidade} ({codigo_unidade})")

            # ✅ BUSCAR: Unidade nos dados do sistema
            unidade_encontrada = None
            indice_unidade = None

            for i, unidade in enumerate(self.dados_unidades["unidades"]):
                if str(unidade["codigo"]) == codigo_unidade:
                    unidade_encontrada = unidade
                    indice_unidade = i
                    break

            if unidade_encontrada:
                # ✅ VERIFICAR: Se já está ativa
                if unidade_encontrada["ativa"]:
                    messagebox.showinfo("Informação",
                                        f"A unidade '{nome_unidade}' já está ativa!")
                    print(f"ℹ️ Unidade {nome_unidade} já estava ativa")
                    return

                # ✅ ATIVAR: Unidade no sistema
                self.dados_unidades["unidades"][indice_unidade]["ativa"] = True
                print(f"✅ Status da unidade alterado para ATIVA")

                # ✅ SALVAR: Dados atualizados
                self._salvar_dados_em_arquivo()

                # ✅ ATUALIZAR: Interface
                self._atualizar_lista()

                # ✅ RESELECIONAR: A unidade para manter contexto
                self._reselecionar_unidade(codigo_unidade)

                # ✅ FEEDBACK: Sucesso
                messagebox.showinfo("Sucesso",
                                    f"✅ Unidade '{nome_unidade}' ativada com sucesso!\n\n"
                                    f"🆔 Código UC: {codigo_unidade}\n"
                                    f"   Status: 🟢 Ativa")

                print(f"✅ Unidade ativada com sucesso: {nome_unidade}")

            else:
                print(f"❌ Unidade {codigo_unidade} não encontrada nos dados")
                messagebox.showerror("Erro", f"Dados da unidade '{nome_unidade}' não encontrados!")

        except Exception as e:
            print(f"❌ Erro ao ativar unidade: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Erro", f"Erro ao ativar unidade: {e}")

    def _desativar_unidade(self):
        """✅ CORRIGIDO: Desativa unidade selecionada no sistema"""
        print("🔴 Tentando desativar unidade")
        try:
            if not self.unidade_selecionada:
                print("⚠️ Nenhuma unidade selecionada para desativação")
                messagebox.showwarning("Aviso", "Selecione uma unidade para desativar.")
                return

            codigo_unidade = str(self.unidade_selecionada[0])
            nome_unidade = self.unidade_selecionada[1]
            print(f"🔴 Desativando unidade: {nome_unidade} ({codigo_unidade})")

            # ✅ BUSCAR: Unidade nos dados do sistema
            unidade_encontrada = None
            indice_unidade = None

            for i, unidade in enumerate(self.dados_unidades["unidades"]):
                if str(unidade["codigo"]) == codigo_unidade:
                    unidade_encontrada = unidade
                    indice_unidade = i
                    break

            if unidade_encontrada:
                # ✅ VERIFICAR: Se já está inativa
                if not unidade_encontrada["ativa"]:
                    messagebox.showinfo("Informação",
                                        f"A unidade '{nome_unidade}' já está inativa!")
                    print(f"ℹ️ Unidade {nome_unidade} já estava inativa")
                    return

                # ✅ CONFIRMAÇÃO: Para desativação (ação mais crítica)
                confirmacao = f"""🔴 CONFIRMAR DESATIVAÇÃO:

    🏠 Nome: {nome_unidade}
    🆔 Código UC: {codigo_unidade}
    📊 Status Atual: 🟢 Ativa

    ⚠️ A unidade será marcada como INATIVA.
    Isso pode afetar cálculos e relatórios.

    Deseja realmente desativar esta unidade?"""

                resposta = messagebox.askyesno("Confirmar Desativação", confirmacao)

                if resposta:
                    # ✅ DESATIVAR: Unidade no sistema
                    self.dados_unidades["unidades"][indice_unidade]["ativa"] = False
                    print(f"✅ Status da unidade alterado para INATIVA")

                    # ✅ SALVAR: Dados atualizados
                    self._salvar_dados_em_arquivo()

                    # ✅ ATUALIZAR: Interface
                    self._atualizar_lista()

                    # ✅ RESELECIONAR: A unidade para manter contexto
                    self._reselecionar_unidade(codigo_unidade)

                    # ✅ FEEDBACK: Sucesso
                    messagebox.showinfo("Sucesso",
                                        f"✅ Unidade '{nome_unidade}' desativada com sucesso!\n\n"
                                        f"🆔 Código UC: {codigo_unidade}\n"
                                        f"📊 Status: 🔴 Inativa")

                    print(f"✅ Unidade desativada com sucesso: {nome_unidade}")
                else:
                    print("❌ Desativação cancelada pelo usuário")

            else:
                print(f"❌ Unidade {codigo_unidade} não encontrada nos dados")
                messagebox.showerror("Erro", f"Dados da unidade '{nome_unidade}' não encontrados!")

        except Exception as e:
            print(f"❌ Erro ao desativar unidade: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Erro", f"Erro ao desativar unidade: {e}")

    def _reselecionar_unidade(self, codigo_unidade):
        """✅ NOVO: Reseleciona a unidade após alteração para manter contexto"""
        try:
            print(f"🔄 Reselecionando unidade: {codigo_unidade}")

            # Buscar item na TreeView
            for item in self.tree_unidades.get_children():
                valores = self.tree_unidades.item(item)['values']
                if valores and str(valores[0]) == codigo_unidade:
                    # Selecionar o item
                    self.tree_unidades.selection_set(item)
                    self.tree_unidades.focus(item)

                    # Disparar evento de seleção manualmente
                    self._on_unidade_selecionada(None)

                    print(f"✅ Unidade {codigo_unidade} reselecionada")
                    break

        except Exception as e:
            print(f"⚠️ Erro ao reselecionar unidade: {e}")

    def _atualizar_lista(self):
        """✅ MELHORADO: Atualiza lista de unidades e dashboard com status"""
        print("🔄 Atualizando lista de unidades...")
        try:
            # ✅ RECARREGAR: Unidades na lista
            self._carregar_unidades()

            # ✅ ATUALIZAR: Dashboard com novos totais
            self._atualizar_dashboard()

            # ✅ ATUALIZAR: Status da lista
            import datetime
            agora = datetime.datetime.now().strftime("%H:%M:%S")
            self.label_status_lista.config(text=f"✅ Atualizado às {agora}")

            # ✅ LIMPAR: Seleção atual
            self.unidade_selecionada = None
            self.btn_ativar.config(state=tk.DISABLED)
            self.btn_desativar.config(state=tk.DISABLED)

            # ✅ LIMPAR: Detalhes
            self.text_detalhes.delete(1.0, tk.END)
            self.text_detalhes.insert(1.0, "📋 Selecione uma unidade na lista\npara ver os detalhes completos...")

            # ✅ LIMPAR: Gráfico
            for widget in self.frame_grafico_unidade.winfo_children():
                widget.destroy()
            tk.Label(self.frame_grafico_unidade,
                     text="📊 Selecione uma unidade\npara ver o gráfico de consumo",
                     font=('Arial', 10), fg='gray').pack(expand=True)

            print("✅ Lista atualizada com sucesso")

        except Exception as e:
            print(f"❌ Erro ao atualizar lista: {e}")
            # ✅ ATUALIZAR: Status com erro
            self.label_status_lista.config(text="❌ Erro na atualização", fg='red')
            messagebox.showerror("Erro", f"Erro ao atualizar: {e}")

    def _abrir_janela_unidade(self, titulo, dados_unidade):
        """✅ MELHORADO: Abre janela de cadastro/edição de unidade com consumos mensais"""
        print(f"🪟 Abrindo janela: {titulo}")
        try:
            janela = tk.Toplevel(self.parent_frame)
            janela.title(titulo)
            janela.geometry("800x700")  # ✅ AUMENTADO: Janela maior para acomodar consumos
            janela.resizable(True, True)  # ✅ PERMITIR: Redimensionamento

            # Centralizar janela
            janela.transient(self.parent_frame.winfo_toplevel())
            janela.grab_set()

            # ✅ NOVO: Notebook para organizar em abas
            notebook = ttk.Notebook(janela)
            notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

            # ✅ ABA 1: Dados Básicos
            frame_dados = ttk.Frame(notebook)
            notebook.add(frame_dados, text="📋 Dados Básicos")

            # Campos básicos do formulário
            frame_form = tk.LabelFrame(frame_dados, text="Informações da Unidade", font=('Arial', 12, 'bold'))
            frame_form.pack(fill=tk.X, padx=20, pady=20)

            # Código UC
            tk.Label(frame_form, text="Código UC:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W,
                                                                                     padx=10, pady=5)
            entry_codigo = tk.Entry(frame_form, width=30, font=('Arial', 10))
            entry_codigo.grid(row=0, column=1, padx=10, pady=5)

            # Nome
            tk.Label(frame_form, text="Nome:", font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky=tk.W, padx=10,
                                                                                pady=5)
            entry_nome = tk.Entry(frame_form, width=30, font=('Arial', 10))
            entry_nome.grid(row=1, column=1, padx=10, pady=5)

            # Tipo
            tk.Label(frame_form, text="Tipo de Ligação:", font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky=tk.W,
                                                                                           padx=10, pady=5)
            combo_tipo = ttk.Combobox(frame_form, values=["Bifásica", "Trifásica"],
                                      state="readonly", width=27)
            combo_tipo.grid(row=2, column=1, padx=10, pady=5)

            # Endereço
            tk.Label(frame_form, text="Endereço:", font=('Arial', 10, 'bold')).grid(row=3, column=0, sticky=tk.W,
                                                                                    padx=10, pady=5)
            entry_endereco = tk.Entry(frame_form, width=30, font=('Arial', 10))
            entry_endereco.grid(row=3, column=1, padx=10, pady=5)

            # Status
            var_ativa = tk.BooleanVar(value=True)
            check_ativa = tk.Checkbutton(frame_form, text="Unidade Ativa", variable=var_ativa,
                                         font=('Arial', 10, 'bold'))
            check_ativa.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

            # ✅ ABA 2: Consumos Mensais
            frame_consumos = ttk.Frame(notebook)
            notebook.add(frame_consumos, text="⚡ Consumos Mensais")

            # Frame para consumos
            frame_consumo_form = tk.LabelFrame(frame_consumos, text="Consumo Mensal por Mês (kWh)",
                                               font=('Arial', 12, 'bold'))
            frame_consumo_form.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

            # ✅ NOVO: Criar campos para todos os meses
            meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
                     'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']

            # Dicionário para armazenar os campos de entrada
            entries_consumo = {}

            # ✅ LAYOUT: Organizar em 3 colunas x 4 linhas
            for i, mes in enumerate(meses):
                linha = i // 3  # 0, 1, 2, 3
                coluna = i % 3  # 0, 1, 2

                # Label do mês
                tk.Label(frame_consumo_form, text=f"{mes}:",
                         font=('Arial', 10, 'bold')).grid(row=linha * 2, column=coluna * 2,
                                                          sticky=tk.W, padx=10, pady=5)

                # Entry para consumo
                entry_mes = tk.Entry(frame_consumo_form, width=15, font=('Arial', 10))
                entry_mes.grid(row=linha * 2, column=coluna * 2 + 1, padx=10, pady=5)
                entries_consumo[mes] = entry_mes

                # Placeholder inicial
                entry_mes.insert(0, "0")

            # ✅ NOVO: Botões de ação rápida para consumos
            frame_acoes_consumo = tk.Frame(frame_consumos)
            frame_acoes_consumo.pack(fill=tk.X, padx=20, pady=10)

            def aplicar_valor_todos():
                """Aplica o mesmo valor para todos os meses"""
                try:
                    valor = tk.simpledialog.askstring("Valor Uniforme",
                                                      "Digite o valor (kWh) para aplicar em todos os meses:")
                    if valor:
                        valor_int = int(float(valor))
                        for entry in entries_consumo.values():
                            entry.delete(0, tk.END)
                            entry.insert(0, str(valor_int))
                        print(f"✅ Valor {valor_int} aplicado a todos os meses")
                except ValueError:
                    messagebox.showerror("Erro", "Digite um valor numérico válido!")

            def limpar_todos():
                """Limpa todos os campos de consumo"""
                for entry in entries_consumo.values():
                    entry.delete(0, tk.END)
                    entry.insert(0, "0")
                print("🧹 Todos os consumos zerados")

            def calcular_media():
                """Calcula e mostra a média dos consumos"""
                try:
                    valores = []
                    for entry in entries_consumo.values():
                        valor = entry.get().strip()
                        if valor:
                            valores.append(float(valor))

                    if valores:
                        media = sum(valores) / len(valores)
                        total = sum(valores)
                        messagebox.showinfo("Estatísticas",
                                            f"📊 Estatísticas dos Consumos:\n\n"
                                            f"• Média Mensal: {media:.0f} kWh\n"
                                            f"• Total Anual: {total:,.0f} kWh\n"
                                            f"• Maior Consumo: {max(valores):.0f} kWh\n"
                                            f"• Menor Consumo: {min(valores):.0f} kWh")
                    else:
                        messagebox.showwarning("Aviso", "Nenhum valor válido encontrado!")
                except ValueError:
                    messagebox.showerror("Erro", "Verifique se todos os valores são numéricos!")

            # Botões de ação rápida
            ttk.Button(frame_acoes_consumo, text="📊 Valor Uniforme",
                       command=aplicar_valor_todos).pack(side=tk.LEFT, padx=5)

            ttk.Button(frame_acoes_consumo, text="🧹 Limpar Todos",
                       command=limpar_todos).pack(side=tk.LEFT, padx=5)

            ttk.Button(frame_acoes_consumo, text="📈 Calcular Média",
                       command=calcular_media).pack(side=tk.LEFT, padx=5)

            # ✅ CORRIGIDO: Preencher dados se for edição
            if dados_unidade:
                print(f"🔄 Preenchendo dados para edição: {dados_unidade[1]}")

                # ✅ LIMPAR: Campos antes de preencher
                entry_codigo.delete(0, tk.END)
                entry_nome.delete(0, tk.END)
                entry_endereco.delete(0, tk.END)

                # ✅ PREENCHER: Dados básicos
                codigo_unidade = str(dados_unidade[0])
                entry_codigo.insert(0, codigo_unidade)
                entry_nome.insert(0, dados_unidade[1])
                combo_tipo.set(dados_unidade[2])

                print(f"✅ Dados básicos preenchidos: {codigo_unidade}, {dados_unidade[1]}, {dados_unidade[2]}")

                # ✅ BUSCAR: Dados completos da unidade nos dados do sistema
                unidade_encontrada = None
                for unidade in self.dados_unidades["unidades"]:
                    if str(unidade["codigo"]) == codigo_unidade:
                        unidade_encontrada = unidade
                        break

                if unidade_encontrada:
                    entry_endereco.insert(0, unidade_encontrada["endereco"])
                    var_ativa.set(unidade_encontrada["ativa"])
                    print(f"✅ Endereço preenchido: {unidade_encontrada['endereco']}")
                    print(f"✅ Status preenchido: {unidade_encontrada['ativa']}")
                else:
                    print(f"⚠️ Dados completos da unidade {codigo_unidade} não encontrados")

                # ✅ CORRIGIDO: Preencher consumos mensais
                consumos_existentes = self.dados_unidades["consumos"].get(codigo_unidade, {})
                print(f"📊 Consumos encontrados para {codigo_unidade}: {len(consumos_existentes)} meses")

                if consumos_existentes:
                    for mes, entry in entries_consumo.items():
                        # Limpar campo antes de preencher
                        entry.delete(0, tk.END)

                        if mes in consumos_existentes:
                            valor_consumo = consumos_existentes[mes]
                            entry.insert(0, str(valor_consumo))
                            print(f"✅ {mes}: {valor_consumo} kWh preenchido")
                        else:
                            entry.insert(0, "0")
                            print(f"⚠️ {mes}: sem dados, usando 0")

                    # ✅ CALCULAR: Totais para verificação
                    total_anual = sum(consumos_existentes.values())
                    media_mensal = total_anual / 12
                    print(f"📊 Total anual carregado: {total_anual:,} kWh")
                    print(f"📈 Média mensal: {media_mensal:.0f} kWh")
                else:
                    print("⚠️ Nenhum consumo encontrado para esta unidade")
                    # Manter valores padrão (0) que já foram inseridos

                # ✅ DESABILITAR: Campo código na edição para evitar alteração acidental
                entry_codigo.config(state='readonly')

                print(f"✅ Todos os dados preenchidos para edição de: {dados_unidade[1]}")

            # ✅ BOTÕES: Principais na parte inferior
            frame_botoes = tk.Frame(janela)
            frame_botoes.pack(fill=tk.X, padx=20, pady=10)

            def validar_e_salvar():
                """Valida e salva os dados da unidade"""
                try:
                    # Validar dados básicos
                    # ✅ CORRIGIDO: Validar dados básicos (considerando readonly na edição)
                    codigo = entry_codigo.get().strip()

                    # ✅ DEBUG: Mostrar dados sendo validados
                    print(f"💾 Validando dados:")
                    print(f"   Código: {codigo}")
                    print(f"   Título: {titulo}")

                    nome = entry_nome.get().strip()
                    tipo = combo_tipo.get()
                    endereco = entry_endereco.get().strip()

                    if not all([codigo, nome, tipo, endereco]):
                        messagebox.showerror("Erro", "Preencha todos os campos básicos!")
                        notebook.select(0)  # Voltar para aba de dados básicos
                        return

                    # ✅ VALIDAR: Consumos mensais
                    consumos_validados = {}
                    erros_consumo = []

                    for mes, entry in entries_consumo.items():
                        valor_str = entry.get().strip()
                        try:
                            if valor_str:
                                valor = int(float(valor_str))
                                if valor < 0:
                                    erros_consumo.append(f"{mes}: valor não pode ser negativo")
                                else:
                                    consumos_validados[mes] = valor
                            else:
                                consumos_validados[mes] = 0
                        except ValueError:
                            erros_consumo.append(f"{mes}: '{valor_str}' não é um número válido")

                    if erros_consumo:
                        messagebox.showerror("Erro nos Consumos",
                                             "Corrija os seguintes erros:\n\n" + "\n".join(erros_consumo))
                        notebook.select(1)  # Ir para aba de consumos
                        return

                    # ✅ VERIFICAR: Se código já existe (para nova unidade)
                    if titulo == "Nova Unidade":
                        for unidade in self.dados_unidades["unidades"]:
                            if unidade["codigo"] == codigo:
                                messagebox.showerror("Erro",
                                                     f"Código UC '{codigo}' já existe!\n"
                                                     f"Unidade: {unidade['nome']}")
                                notebook.select(0)
                                return

                    # ✅ SALVAR: Dados
                    total_anual = sum(consumos_validados.values())
                    media_mensal = total_anual / 12

                    # Mostrar resumo antes de salvar
                    resumo = f"""   RESUMO DA UNIDADE:

            🏠 Nome: {nome}
            🆔 Código UC: {codigo}
            🏢 Tipo: {tipo}
            📍 Endereço: {endereco}
            📊 Status: {'Ativa' if var_ativa.get() else 'Inativa'}

            ⚡ CONSUMO ENERGÉTICO:
            • Total Anual: {total_anual:,} kWh
            • Média Mensal: {media_mensal:.0f} kWh
            • Maior Consumo: {max(consumos_validados.values()):,} kWh
            • Menor Consumo: {min(consumos_validados.values()):,} kWh

            💰 ECONOMIA ESTIMADA:
            • Economia Anual: R\$ {total_anual * 0.65:,.2f}

            Confirma o salvamento?"""

                    resposta = messagebox.askyesno("Confirmar Salvamento", resumo)

                    if resposta:
                        print(f"💾 Salvando unidade: {nome}")
                        print(f"📊 Consumos: {consumos_validados}")

                        # ✅ CORRIGIDO: Salvar unidade real no sistema
                        sucesso = self._salvar_unidade_no_sistema(
                            codigo, nome, tipo, endereco, var_ativa.get(), consumos_validados
                        )

                        if sucesso:
                            messagebox.showinfo("Sucesso",
                                                f"✅ Unidade '{nome}' salva com sucesso!\n\n"
                                                f"📊 Total anual: {total_anual:,} kWh\n"
                                                f"💰 Economia estimada: R\$ {total_anual * 0.65:,.2f}")

                            janela.destroy()
                            self._atualizar_lista()  # ✅ Atualizar lista para mostrar nova unidade
                        else:
                            messagebox.showerror("Erro", "Falha ao salvar unidade. Verifique os logs.")

                except Exception as e:
                    print(f"❌ Erro ao salvar: {e}")
                    import traceback
                    traceback.print_exc()
                    messagebox.showerror("Erro", f"Erro ao salvar unidade: {e}")

            def validar_consumos():
                """Valida apenas os consumos sem salvar"""
                try:
                    total = 0
                    erros = []

                    for mes, entry in entries_consumo.items():
                        valor_str = entry.get().strip()
                        try:
                            if valor_str:
                                valor = int(float(valor_str))
                                if valor < 0:
                                    erros.append(f"{mes}: valor negativo")
                                else:
                                    total += valor
                        except ValueError:
                            erros.append(f"{mes}: valor inválido")

                    if erros:
                        messagebox.showerror("Erros Encontrados", "\n".join(erros))
                    else:
                        media = total / 12
                        messagebox.showinfo("Validação OK",
                                            f"✅ Todos os consumos são válidos!\n\n"
                                            f"📊 Total Anual: {total:,} kWh\n"
                                            f"📈 Média Mensal: {media:.0f} kWh")

                except Exception as e:
                    messagebox.showerror("Erro", f"Erro na validação: {e}")

            # Botões principais
            ttk.Button(frame_botoes, text="✅ Validar Consumos",
                       command=validar_consumos).pack(side=tk.LEFT, padx=5)

            ttk.Button(frame_botoes, text="💾 Salvar Unidade",
                       command=validar_e_salvar).pack(side=tk.LEFT, padx=5)

            ttk.Button(frame_botoes, text="❌ Cancelar",
                       command=janela.destroy).pack(side=tk.RIGHT, padx=5)

            # ✅ IMPORTAR: tkinter.simpledialog para valor uniforme
            import tkinter.simpledialog

            print(f"✅ Janela '{titulo}' criada com consumos mensais")

        except Exception as e:
            print(f"❌ Erro ao criar janela: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Erro", f"Erro ao criar janela: {e}")

    def _salvar_unidade_no_sistema(self, codigo, nome, tipo, endereco, ativa, consumos):
        """✅ NOVO: Salva unidade real no sistema de dados"""
        try:
            print(f"💾 Salvando unidade no sistema: {nome} ({codigo})")

            # Converter tipo para formato interno
            tipo_interno = "tri" if tipo == "Trifásica" else "bi"

            # ✅ VERIFICAR: Se é nova unidade ou edição
            unidade_existente = None
            for i, unidade in enumerate(self.dados_unidades["unidades"]):
                if unidade["codigo"] == codigo:
                    unidade_existente = i
                    break

            # Criar/atualizar dados da unidade
            dados_unidade = {
                "codigo": codigo,
                "nome": nome,
                "tipo": tipo_interno,
                "endereco": endereco,
                "ativa": ativa
            }

            if unidade_existente is not None:
                # ✅ EDITAR: Unidade existente
                self.dados_unidades["unidades"][unidade_existente] = dados_unidade
                print(f"✅ Unidade editada: {nome}")
            else:
                # ✅ NOVA: Adicionar nova unidade
                self.dados_unidades["unidades"].append(dados_unidade)
                print(f"✅ Nova unidade adicionada: {nome}")

            # ✅ SALVAR: Consumos mensais
            self.dados_unidades["consumos"][codigo] = consumos.copy()
            print(f"✅ Consumos salvos: {len(consumos)} meses")

            # ✅ OPCIONAL: Salvar em arquivo (se você quiser persistência)
            self._salvar_dados_em_arquivo()

            return True

        except Exception as e:
            print(f"❌ Erro ao salvar unidade no sistema: {e}")
            import traceback
            traceback.print_exc()
            return False

    def _salvar_dados_em_arquivo(self):
        """✅ OPCIONAL: Salva dados em arquivo JSON para persistência"""
        try:
            import json
            import os

            # Criar diretório se não existir
            os.makedirs("dados", exist_ok=True)

            # Salvar dados em arquivo
            with open("dados/unidades_sistema.json", "w", encoding="utf-8") as arquivo:
                json.dump(self.dados_unidades, arquivo, indent=2, ensure_ascii=False)

            print("✅ Dados salvos em arquivo: dados/unidades_sistema.json")

        except Exception as e:
            print(f"⚠️ Erro ao salvar arquivo (não crítico): {e}")

    def _criar_unidades_simples(self):
        """Cria interface simples em caso de erro"""
        tk.Label(self.parent_frame,
                 text="🏠 Gestão de Unidades",
                 font=('Arial', 18, 'bold')).pack(pady=20)

        tk.Label(self.parent_frame,
                 text="Erro ao carregar módulo de unidades.\nVerifique os logs para mais detalhes.",
                 font=('Arial', 12), fg='red').pack(pady=10)

    def _atualizar_dashboard(self):
        """✅ ATUALIZADO: Atualiza os 5 cards do dashboard"""
        try:
            print("📊 Atualizando dashboard...")

            # ✅ CALCULAR: Dados atualizados
            dados_calculados = self._calcular_dados_unidades()

            # ✅ ATUALIZAR: Labels dos 5 cards
            self.label_ativas.config(text=str(dados_calculados['unidades_ativas']))

            self.label_consumo_medio.config(
                text=f"{dados_calculados['consumo_medio_mensal']:,.0f} kWh".replace(',', '.'))

            self.label_consumo_anual.config(
                text=f"{dados_calculados['consumo_total_anual']:,.0f} kWh".replace(',', '.'))

            self.label_receita_mensal.config(text=self._formatar_moeda(dados_calculados['receita_mensal']))

            self.label_receita_anual.config(text=self._formatar_moeda(dados_calculados['receita_anual']))

            print(f"✅ Dashboard atualizado: {dados_calculados['unidades_ativas']} unidades ativas")
            print(f"💰 Receita mensal: {self._formatar_moeda(dados_calculados['receita_mensal'])}")
            print(f"💰 Receita anual: {self._formatar_moeda(dados_calculados['receita_anual'])}")

        except Exception as e:
            print(f"❌ Erro ao atualizar dashboard: {e}")

    def atualizar_dados(self):
        """Atualiza dados do módulo"""
        print("🔄 Atualizando dados das unidades...")
        self._carregar_unidades()