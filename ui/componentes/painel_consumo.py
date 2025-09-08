# usina_01/ui/componentes/painel_consumo.py

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Callable, Dict

from nucleo.modelos import SistemaEnergia
from nucleo.validadores import ValidadorConsumo
from utilitarios.constantes import MESES_APENAS


class JanelaPainelConsumo:
    """
    Janela para inserção e edição dos dados de consumo das unidades.
    """

    def __init__(self, parent: tk.Tk, sistema: SistemaEnergia, callback_salvar: Optional[Callable] = None):
        self.parent = parent
        self.sistema = sistema
        self.callback_salvar = callback_salvar
        self.validador = ValidadorConsumo()

        # Variáveis de controle
        self.unidade_selecionada = None
        self.consumo_vars = {}  # Dicionário para armazenar as variáveis dos campos

        # Cria a janela
        self.janela = tk.Toplevel(parent)
        self.configurar_janela()
        self.criar_interface()
        self.carregar_primeira_unidade()

    def configurar_janela(self):
        """Configura as propriedades da janela."""
        self.janela.title("Painel de Consumo - Inserção de Dados")
        self.janela.geometry("700x600")
        self.janela.resizable(False, False)

        # Centraliza a janela
        self.janela.update_idletasks()
        x = (self.janela.winfo_screenwidth() // 2) - (700 // 2)
        y = (self.janela.winfo_screenheight() // 2) - (600 // 2)
        self.janela.geometry(f"700x600+{x}+{y}")

        # Torna a janela modal
        self.janela.transient(self.parent)
        self.janela.grab_set()

        # Foca na janela
        self.janela.focus_set()

    def criar_interface(self):
        """Cria a interface da janela."""
        # Frame principal com padding
        main_frame = ttk.Frame(self.janela, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        titulo_label = ttk.Label(main_frame, text="Painel de Consumo - Dados Mensais",
                                 font=("Arial", 14, "bold"))
        titulo_label.pack(pady=(0, 20))

        # Frame para seleção de unidade
        selecao_frame = ttk.LabelFrame(main_frame, text="Selecionar Unidade", padding="10")
        selecao_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(selecao_frame, text="Unidade Consumidora:").pack(side=tk.LEFT)

        # Combobox para seleção de unidade
        self.unidade_var = tk.StringVar()
        self.unidade_combo = ttk.Combobox(selecao_frame, textvariable=self.unidade_var,
                                          state="readonly", width=40)
        self.unidade_combo.pack(side=tk.LEFT, padx=(10, 0))
        self.unidade_combo.bind("<<ComboboxSelected>>", self.ao_selecionar_unidade)

        # Atualiza lista de unidades
        self.atualizar_lista_unidades()

        # Frame para informações da unidade
        info_frame = ttk.LabelFrame(main_frame, text="Informações da Unidade", padding="10")
        info_frame.pack(fill=tk.X, pady=(0, 15))

        self.info_text = tk.Text(info_frame, height=3, wrap=tk.WORD, state=tk.DISABLED,
                                 font=("Arial", 9), bg="#f0f0f0")
        self.info_text.pack(fill=tk.X)

        # Frame para dados de consumo
        consumo_frame = ttk.LabelFrame(main_frame, text="Dados de Consumo Mensal (kWh)", padding="10")
        consumo_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        # Cria um canvas com scrollbar para os dados de consumo
        canvas = tk.Canvas(consumo_frame, height=300)
        scrollbar = ttk.Scrollbar(consumo_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Cria campos para cada mês
        for i, mes in enumerate(MESES_APENAS):
            row = i // 3  # 3 colunas
            col = (i % 3) * 2

            # Label do mês
            ttk.Label(scrollable_frame, text=f"{mes}:", font=("Arial", 9, "bold")).grid(
                row=row, column=col, sticky=tk.W, padx=(10, 5), pady=5
            )

            # Entry para o valor
            var = tk.StringVar()
            self.consumo_vars[mes] = var
            entry = ttk.Entry(scrollable_frame, textvariable=var, width=12, font=("Arial", 9))
            entry.grid(row=row, column=col + 1, sticky=tk.W, padx=(0, 20), pady=5)

            # Bind para validação em tempo real
            var.trace_add("write", lambda *args, m=mes: self.validar_campo_tempo_real(m))

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Frame para estatísticas
        stats_frame = ttk.LabelFrame(main_frame, text="Estatísticas", padding="10")
        stats_frame.pack(fill=tk.X, pady=(0, 15))

        # Labels para estatísticas
        stats_inner_frame = ttk.Frame(stats_frame)
        stats_inner_frame.pack(fill=tk.X)

        ttk.Label(stats_inner_frame, text="Total Anual:").grid(row=0, column=0, sticky=tk.W)
        self.total_anual_var = tk.StringVar(value="0,00 kWh")
        ttk.Label(stats_inner_frame, textvariable=self.total_anual_var, font=("Arial", 9, "bold")).grid(
            row=0, column=1, sticky=tk.W, padx=(10, 30)
        )

        ttk.Label(stats_inner_frame, text="Média Mensal:").grid(row=0, column=2, sticky=tk.W)
        self.media_mensal_var = tk.StringVar(value="0,00 kWh")
        ttk.Label(stats_inner_frame, textvariable=self.media_mensal_var, font=("Arial", 9, "bold")).grid(
            row=0, column=3, sticky=tk.W, padx=(10, 30)
        )

        ttk.Label(stats_inner_frame, text="Maior Consumo:").grid(row=1, column=0, sticky=tk.W)
        self.maior_consumo_var = tk.StringVar(value="0,00 kWh")
        ttk.Label(stats_inner_frame, textvariable=self.maior_consumo_var, font=("Arial", 9, "bold")).grid(
            row=1, column=1, sticky=tk.W, padx=(10, 30)
        )

        ttk.Label(stats_inner_frame, text="Menor Consumo:").grid(row=1, column=2, sticky=tk.W)
        self.menor_consumo_var = tk.StringVar(value="0,00 kWh")
        ttk.Label(stats_inner_frame, textvariable=self.menor_consumo_var, font=("Arial", 9, "bold")).grid(
            row=1, column=3, sticky=tk.W, padx=(10, 30)
        )

        # Frame para botões de ação
        acoes_frame = ttk.Frame(main_frame)
        acoes_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Button(acoes_frame, text="Aplicar Padrão", command=self.aplicar_padrao).pack(side=tk.LEFT)
        ttk.Button(acoes_frame, text="Limpar Tudo", command=self.limpar_todos_campos).pack(side=tk.LEFT, padx=(10, 0))
        ttk.Button(acoes_frame, text="Copiar do Mês Anterior", command=self.copiar_mes_anterior).pack(side=tk.LEFT,
                                                                                                      padx=(10, 0))

        # Frame para botões principais
        botoes_frame = ttk.Frame(main_frame)
        botoes_frame.pack(fill=tk.X)

        ttk.Button(botoes_frame, text="Salvar e Fechar", command=self.salvar_e_fechar).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(botoes_frame, text="Salvar", command=self.salvar_dados).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(botoes_frame, text="Cancelar", command=self.janela.destroy).pack(side=tk.RIGHT)

    def atualizar_lista_unidades(self):
        """Atualiza a lista de unidades no combobox."""
        valores = []
        for unidade in self.sistema.unidades:
            valores.append(f"{unidade.codigo} - {unidade.nome}")

        self.unidade_combo['values'] = valores

    def carregar_primeira_unidade(self):
        """Carrega a primeira unidade disponível."""
        if self.sistema.unidades:
            self.unidade_combo.current(0)
            self.ao_selecionar_unidade()

    def ao_selecionar_unidade(self, event=None):
        """Ação executada ao selecionar uma unidade."""
        selecao = self.unidade_var.get()
        if not selecao:
            return

        # Extrai o código da unidade
        codigo = selecao.split(" - ")[0]

        # Encontra a unidade
        self.unidade_selecionada = next(
            (u for u in self.sistema.unidades if u.codigo == codigo), None
        )

        if self.unidade_selecionada:
            self.atualizar_info_unidade()
            self.carregar_dados_consumo()
            self.atualizar_estatisticas()

    def atualizar_info_unidade(self):
        """Atualiza as informações da unidade selecionada."""
        if not self.unidade_selecionada:
            return

        info = f"Código: {self.unidade_selecionada.codigo} | "
        info += f"Nome: {self.unidade_selecionada.nome} | "
        info += f"Tipo: {self.unidade_selecionada.tipo_ligacao.value.upper()} | "
        info += f"Tarifa Mínima: {self.unidade_selecionada.tarifa_minima:.0f} kWh"

        if self.unidade_selecionada.endereco:
            info += f"\nEndereço: {self.unidade_selecionada.endereco}"

        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete(1.0, tk.END)
        self.info_text.insert(1.0, info)
        self.info_text.config(state=tk.DISABLED)

    def carregar_dados_consumo(self):
        """Carrega os dados de consumo da unidade selecionada."""
        if not self.unidade_selecionada:
            return

        consumos = self.sistema.consumos.get(self.unidade_selecionada.codigo, {})

        for mes in MESES_APENAS:
            valor = consumos.get(mes, 0.0)
            self.consumo_vars[mes].set(str(valor) if valor > 0 else "")

    def validar_campo_tempo_real(self, mes: str):
        """Valida um campo em tempo real e atualiza estatísticas."""
        try:
            valor_str = self.consumo_vars[mes].get()
            if valor_str:
                valor = float(valor_str.replace(",", "."))
                if valor < 0:
                    # Valor negativo - pode mostrar feedback visual aqui
                    pass
        except ValueError:
            # Valor inválido - pode mostrar feedback visual aqui
            pass

        # Atualiza estatísticas
        self.atualizar_estatisticas()

    def atualizar_estatisticas(self):
        """Atualiza as estatísticas de consumo."""
        valores_validos = []

        for mes in MESES_APENAS:
            try:
                valor_str = self.consumo_vars[mes].get()
                if valor_str:
                    valor = float(valor_str.replace(",", "."))
                    if valor >= 0:
                        valores_validos.append(valor)
            except ValueError:
                continue

        if valores_validos:
            total = sum(valores_validos)
            media = total / len(valores_validos)
            maior = max(valores_validos)
            menor = min(valores_validos)

            self.total_anual_var.set(f"{total:,.2f} kWh".replace(",", "X").replace(".", ",").replace("X", "."))
            self.media_mensal_var.set(f"{media:,.2f} kWh".replace(",", "X").replace(".", ",").replace("X", "."))
            self.maior_consumo_var.set(f"{maior:,.2f} kWh".replace(",", "X").replace(".", ",").replace("X", "."))
            self.menor_consumo_var.set(f"{menor:,.2f} kWh".replace(",", "X").replace(".", ",").replace("X", "."))
        else:
            self.total_anual_var.set("0,00 kWh")
            self.media_mensal_var.set("0,00 kWh")
            self.maior_consumo_var.set("0,00 kWh")
            self.menor_consumo_var.set("0,00 kWh")

    def aplicar_padrao(self):
        """Aplica valores padrão baseados no tipo de ligação."""
        if not self.unidade_selecionada:
            messagebox.showwarning("Aviso", "Selecione uma unidade primeiro.")
            return

        resposta = messagebox.askyesno("Aplicar Padrão",
                                       "Isso substituirá todos os valores atuais pelos padrões. Continuar?")
        if not resposta:
            return

        # Define padrões baseados no tipo de ligação
        tipo = self.unidade_selecionada.tipo_ligacao.value
        if tipo == "mono":
            padrao = 150  # kWh para monofásico
        elif tipo == "bi":
            padrao = 300  # kWh para bifásico
        else:  # trifásico
            padrao = 500  # kWh para trifásico

        # Aplica variação sazonal
        for mes in MESES_APENAS:
            if mes in ["Dezembro", "Janeiro", "Fevereiro"]:  # Verão
                valor = padrao * 1.2  # +20% no verão
            elif mes in ["Junho", "Julho", "Agosto"]:  # Inverno
                valor = padrao * 0.9  # -10% no inverno
            else:
                valor = padrao

            self.consumo_vars[mes].set(f"{valor:.0f}")

        self.atualizar_estatisticas()
        messagebox.showinfo("Sucesso", "Valores padrão aplicados!")

    def limpar_todos_campos(self):
        """Limpa todos os campos de consumo."""
        resposta = messagebox.askyesno("Limpar Campos",
                                       "Isso apagará todos os valores de consumo. Continuar?")
        if resposta:
            for mes in MESES_APENAS:
                self.consumo_vars[mes].set("")
            self.atualizar_estatisticas()

    def copiar_mes_anterior(self):
        """Copia valores do mês anterior para meses vazios."""
        valor_anterior = ""
        copiados = 0

        for mes in MESES_APENAS:
            valor_atual = self.consumo_vars[mes].get()

            if not valor_atual and valor_anterior:
                self.consumo_vars[mes].set(valor_anterior)
                copiados += 1
            elif valor_atual:
                valor_anterior = valor_atual

        if copiados > 0:
            self.atualizar_estatisticas()
            messagebox.showinfo("Sucesso", f"{copiados} valores copiados do mês anterior!")
        else:
            messagebox.showinfo("Info", "Nenhum valor foi copiado.")

    def validar_todos_dados(self) -> bool:
        """Valida todos os dados inseridos."""
        if not self.unidade_selecionada:
            messagebox.showerror("Erro", "Nenhuma unidade selecionada.")
            return False

        try:
            for mes in MESES_APENAS:
                valor_str = self.consumo_vars[mes].get()
                if valor_str:
                    valor = float(valor_str.replace(",", "."))
                    self.validador.validar_consumo_mensal(valor, mes)

            return True

        except Exception as e:
            messagebox.showerror("Erro de Validação", str(e))
            return False

    def salvar_dados(self):
        """Salva os dados de consumo."""
        if not self.validar_todos_dados():
            return

        try:
            # Coleta os dados
            consumos = {}
            for mes in MESES_APENAS:
                valor_str = self.consumo_vars[mes].get()
                if valor_str:
                    valor = float(valor_str.replace(",", "."))
                    consumos[mes] = valor
                else:
                    consumos[mes] = 0.0

            # Salva no sistema
            self.sistema.consumos[self.unidade_selecionada.codigo] = consumos

            messagebox.showinfo("Sucesso", f"Dados de consumo salvos para '{self.unidade_selecionada.codigo}'!")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar dados: {e}")

    def salvar_e_fechar(self):
        """Salva os dados e fecha a janela."""
        if not self.validar_todos_dados():
            return

        self.salvar_dados()

        # Chama callback se fornecido
        if self.callback_salvar:
            self.callback_salvar()

        self.janela.destroy()


# --- Bloco de Teste ---
if __name__ == "__main__":
    print("--- Teste: ui/componentes/painel_consumo.py ---")

    # Importa dados de exemplo para teste
    from configuracao.definicoes import CONFIG_EXEMPLO, UNIDADES_EXEMPLO, CONSUMOS_EXEMPLO

    # Cria sistema de teste
    sistema_teste = SistemaEnergia(
        configuracao=CONFIG_EXEMPLO,
        unidades=UNIDADES_EXEMPLO,
        consumos=CONSUMOS_EXEMPLO.copy()  # Cópia para não modificar o original
    )


    def callback_teste():
        print("✓ Callback de salvamento chamado!")
        print("Dados de consumo atualizados:")
        for codigo, consumos in sistema_teste.consumos.items():
            total = sum(consumos.values())
            print(f"  {codigo}: Total anual = {total:.2f} kWh")


    # Cria janela principal para teste
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal

    print("Abrindo painel de consumo...")
    janela_consumo = JanelaPainelConsumo(root, sistema_teste, callback_teste)

    print("✓ Painel de consumo criado!")
    print("✓ Primeira unidade carregada!")
    print("Interaja com a janela... (Feche para continuar)")
    print("Dicas:")
    print("  - Selecione diferentes unidades no combobox")
    print("  - Insira valores de consumo nos campos")
    print("  - Use os botões de ação para facilitar a entrada")
    print("  - Observe as estatísticas sendo atualizadas")

    root.mainloop()

    print("Teste de Painel de Consumo concluído!")