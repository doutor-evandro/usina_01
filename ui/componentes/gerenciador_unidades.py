# usina_01/ui/componentes/gerenciador_unidades.py

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Callable, List

from nucleo.modelos import SistemaEnergia, UnidadeConsumidora, TipoLigacao
from nucleo.validadores import ValidadorUnidade


class JanelaGerenciadorUnidades:
    """
    Janela para gerenciamento das unidades consumidoras do sistema.
    """

    def __init__(self, parent: tk.Tk, sistema: SistemaEnergia, callback_salvar: Optional[Callable] = None):
        self.parent = parent
        self.sistema = sistema
        self.callback_salvar = callback_salvar
        self.validador = ValidadorUnidade()

        # Cria a janela
        self.janela = tk.Toplevel(parent)
        self.configurar_janela()
        self.criar_interface()
        self.atualizar_lista()

    def configurar_janela(self):
        """Configura as propriedades da janela."""
        self.janela.title("Gerenciador de Unidades Consumidoras")
        self.janela.geometry("800x600")
        self.janela.resizable(True, True)

        # Centraliza a janela
        self.janela.update_idletasks()
        x = (self.janela.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.janela.winfo_screenheight() // 2) - (600 // 2)
        self.janela.geometry(f"800x600+{x}+{y}")

        # Torna a janela modal
        self.janela.transient(self.parent)
        self.janela.grab_set()

        # Foca na janela
        self.janela.focus_set()

    def criar_interface(self):
        """Cria a interface da janela."""
        # Frame principal com padding
        main_frame = ttk.Frame(self.janela, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        titulo_label = ttk.Label(main_frame, text="Gerenciador de Unidades Consumidoras",
                                 font=("Arial", 14, "bold"))
        titulo_label.pack(pady=(0, 20))

        # Frame superior - Lista de unidades
        lista_frame = ttk.LabelFrame(main_frame, text="Unidades Cadastradas", padding="10")
        lista_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Treeview para mostrar as unidades
        colunas = ("codigo", "nome", "tipo", "tarifa", "endereco")
        self.tree = ttk.Treeview(lista_frame, columns=colunas, show="headings", height=10)

        # Configura as colunas
        self.tree.heading("codigo", text="Código")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("tipo", text="Tipo")
        self.tree.heading("tarifa", text="Tarifa Mín. (kWh)")
        self.tree.heading("endereco", text="Endereço")

        self.tree.column("codigo", width=80, minwidth=80)
        self.tree.column("nome", width=200, minwidth=150)
        self.tree.column("tipo", width=80, minwidth=80)
        self.tree.column("tarifa", width=120, minwidth=100)
        self.tree.column("endereco", width=250, minwidth=200)

        # Scrollbar para o Treeview
        scrollbar_tree = ttk.Scrollbar(lista_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_tree.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_tree.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind para seleção
        self.tree.bind("<<TreeviewSelect>>", self.ao_selecionar_unidade)
        self.tree.bind("<Double-1>", self.editar_unidade)

        # Frame inferior - Formulário de edição
        form_frame = ttk.LabelFrame(main_frame, text="Dados da Unidade", padding="10")
        form_frame.pack(fill=tk.X, pady=(0, 10))

        # Primeira linha
        linha1_frame = ttk.Frame(form_frame)
        linha1_frame.pack(fill=tk.X, pady=(0, 5))

        ttk.Label(linha1_frame, text="Código:").pack(side=tk.LEFT)
        self.codigo_var = tk.StringVar()
        self.codigo_entry = ttk.Entry(linha1_frame, textvariable=self.codigo_var, width=15)
        self.codigo_entry.pack(side=tk.LEFT, padx=(5, 20))

        ttk.Label(linha1_frame, text="Nome:").pack(side=tk.LEFT)
        self.nome_var = tk.StringVar()
        self.nome_entry = ttk.Entry(linha1_frame, textvariable=self.nome_var, width=30)
        self.nome_entry.pack(side=tk.LEFT, padx=(5, 0))

        # Segunda linha
        linha2_frame = ttk.Frame(form_frame)
        linha2_frame.pack(fill=tk.X, pady=(0, 5))

        ttk.Label(linha2_frame, text="Tipo de Ligação:").pack(side=tk.LEFT)
        self.tipo_var = tk.StringVar()
        self.tipo_combo = ttk.Combobox(linha2_frame, textvariable=self.tipo_var,
                                       values=["mono", "bi", "tri"], state="readonly", width=12)
        self.tipo_combo.pack(side=tk.LEFT, padx=(5, 20))

        ttk.Label(linha2_frame, text="Tarifa Mínima (kWh):").pack(side=tk.LEFT)
        self.tarifa_var = tk.StringVar()
        self.tarifa_entry = ttk.Entry(linha2_frame, textvariable=self.tarifa_var, width=15)
        self.tarifa_entry.pack(side=tk.LEFT, padx=(5, 0))

        # Terceira linha
        linha3_frame = ttk.Frame(form_frame)
        linha3_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(linha3_frame, text="Endereço:").pack(side=tk.LEFT)
        self.endereco_var = tk.StringVar()
        self.endereco_entry = ttk.Entry(linha3_frame, textvariable=self.endereco_var, width=60)
        self.endereco_entry.pack(side=tk.LEFT, padx=(5, 0))

        # Frame para botões do formulário
        botoes_form_frame = ttk.Frame(form_frame)
        botoes_form_frame.pack(fill=tk.X)

        self.btn_adicionar = ttk.Button(botoes_form_frame, text="Adicionar", command=self.adicionar_unidade)
        self.btn_adicionar.pack(side=tk.LEFT, padx=(0, 5))

        self.btn_atualizar = ttk.Button(botoes_form_frame, text="Atualizar", command=self.atualizar_unidade,
                                        state=tk.DISABLED)
        self.btn_atualizar.pack(side=tk.LEFT, padx=(0, 5))

        self.btn_remover = ttk.Button(botoes_form_frame, text="Remover", command=self.remover_unidade,
                                      state=tk.DISABLED)
        self.btn_remover.pack(side=tk.LEFT, padx=(0, 5))

        self.btn_limpar = ttk.Button(botoes_form_frame, text="Limpar", command=self.limpar_formulario)
        self.btn_limpar.pack(side=tk.LEFT, padx=(0, 5))

        # Frame para botões principais
        botoes_frame = ttk.Frame(main_frame)
        botoes_frame.pack(fill=tk.X)

        ttk.Button(botoes_frame, text="Salvar e Fechar", command=self.salvar_e_fechar).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(botoes_frame, text="Cancelar", command=self.janela.destroy).pack(side=tk.RIGHT)

        # Variável para controlar edição
        self.unidade_selecionada = None

    def atualizar_lista(self):
        """Atualiza a lista de unidades no Treeview."""
        # Limpa a lista atual
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Adiciona as unidades
        for unidade in self.sistema.unidades:
            self.tree.insert("", tk.END, values=(
                unidade.codigo,
                unidade.nome,
                unidade.tipo_ligacao.value.upper(),
                f"{unidade.tarifa_minima:.0f}",
                unidade.endereco or ""
            ))

    def ao_selecionar_unidade(self, event):
        """Ação executada ao selecionar uma unidade na lista."""
        selection = self.tree.selection()
        if not selection:
            self.limpar_formulario()
            return

        # Pega o item selecionado
        item = selection[0]
        valores = self.tree.item(item, "values")

        if valores:
            # Encontra a unidade correspondente
            codigo = valores[0]
            self.unidade_selecionada = next(
                (u for u in self.sistema.unidades if u.codigo == codigo), None
            )

            if self.unidade_selecionada:
                # Preenche o formulário
                self.codigo_var.set(self.unidade_selecionada.codigo)
                self.nome_var.set(self.unidade_selecionada.nome)
                self.tipo_var.set(self.unidade_selecionada.tipo_ligacao.value)
                self.tarifa_var.set(str(self.unidade_selecionada.tarifa_minima))
                self.endereco_var.set(self.unidade_selecionada.endereco or "")

                # Habilita botões de edição
                self.btn_atualizar.config(state=tk.NORMAL)
                self.btn_remover.config(state=tk.NORMAL)
                self.btn_adicionar.config(state=tk.DISABLED)

    def limpar_formulario(self):
        """Limpa todos os campos do formulário."""
        self.codigo_var.set("")
        self.nome_var.set("")
        self.tipo_var.set("")
        self.tarifa_var.set("")
        self.endereco_var.set("")

        self.unidade_selecionada = None

        # Restaura estado dos botões
        self.btn_adicionar.config(state=tk.NORMAL)
        self.btn_atualizar.config(state=tk.DISABLED)
        self.btn_remover.config(state=tk.DISABLED)

        # Limpa seleção da lista
        self.tree.selection_remove(self.tree.selection())

    def validar_formulario(self) -> bool:
        """Valida os dados do formulário."""
        try:
            codigo = self.codigo_var.get().strip()
            nome = self.nome_var.get().strip()
            tipo = self.tipo_var.get()
            tarifa_str = self.tarifa_var.get().strip()
            endereco = self.endereco_var.get().strip()

            if not codigo:
                raise ValueError("Código é obrigatório")
            if not nome:
                raise ValueError("Nome é obrigatório")
            if not tipo:
                raise ValueError("Tipo de ligação é obrigatório")
            if not tarifa_str:
                raise ValueError("Tarifa mínima é obrigatória")

            try:
                tarifa = float(tarifa_str)
                if tarifa < 0:
                    raise ValueError("Tarifa mínima não pode ser negativa")
            except ValueError:
                raise ValueError("Tarifa mínima deve ser um número válido")

            # Verifica se o código já existe (apenas para adição)
            if not self.unidade_selecionada:
                if any(u.codigo == codigo for u in self.sistema.unidades):
                    raise ValueError(f"Código '{codigo}' já existe")

            return True

        except ValueError as e:
            messagebox.showerror("Erro de Validação", str(e))
            return False

    def adicionar_unidade(self):
        """Adiciona uma nova unidade."""
        if not self.validar_formulario():
            return

        try:
            # Cria a nova unidade
            nova_unidade = UnidadeConsumidora(
                codigo=self.codigo_var.get().strip(),
                nome=self.nome_var.get().strip(),
                tipo_ligacao=TipoLigacao(self.tipo_var.get()),
                tarifa_minima=float(self.tarifa_var.get()),
                endereco=self.endereco_var.get().strip() or None
            )

            # Valida usando o validador
            self.validador.validar_unidade(nova_unidade)

            # Adiciona ao sistema
            self.sistema.unidades.append(nova_unidade)

            # Inicializa consumos vazios para a nova unidade
            self.sistema.consumos[nova_unidade.codigo] = {}

            # Atualiza a interface
            self.atualizar_lista()
            self.limpar_formulario()

            messagebox.showinfo("Sucesso", f"Unidade '{nova_unidade.codigo}' adicionada com sucesso!")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar unidade: {e}")

    def atualizar_unidade(self):
        """Atualiza a unidade selecionada."""
        if not self.unidade_selecionada or not self.validar_formulario():
            return

        try:
            # Atualiza os dados da unidade
            codigo_antigo = self.unidade_selecionada.codigo
            codigo_novo = self.codigo_var.get().strip()

            self.unidade_selecionada.codigo = codigo_novo
            self.unidade_selecionada.nome = self.nome_var.get().strip()
            self.unidade_selecionada.tipo_ligacao = TipoLigacao(self.tipo_var.get())
            self.unidade_selecionada.tarifa_minima = float(self.tarifa_var.get())
            self.unidade_selecionada.endereco = self.endereco_var.get().strip() or None

            # Valida usando o validador
            self.validador.validar_unidade(self.unidade_selecionada)

            # Se o código mudou, atualiza também nos consumos
            if codigo_antigo != codigo_novo:
                if codigo_antigo in self.sistema.consumos:
                    self.sistema.consumos[codigo_novo] = self.sistema.consumos.pop(codigo_antigo)

            # Atualiza a interface
            self.atualizar_lista()
            self.limpar_formulario()

            messagebox.showinfo("Sucesso", f"Unidade '{codigo_novo}' atualizada com sucesso!")

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar unidade: {e}")

    def remover_unidade(self):
        """Remove a unidade selecionada."""
        if not self.unidade_selecionada:
            return

        resposta = messagebox.askyesno(
            "Confirmar Remoção",
            f"Tem certeza que deseja remover a unidade '{self.unidade_selecionada.codigo}'?\n\n"
            "Todos os dados de consumo desta unidade também serão removidos."
        )

        if resposta:
            try:
                # Remove a unidade
                self.sistema.unidades.remove(self.unidade_selecionada)

                # Remove os consumos da unidade
                if self.unidade_selecionada.codigo in self.sistema.consumos:
                    del self.sistema.consumos[self.unidade_selecionada.codigo]

                # Atualiza a interface
                self.atualizar_lista()
                self.limpar_formulario()

                messagebox.showinfo("Sucesso", f"Unidade '{self.unidade_selecionada.codigo}' removida com sucesso!")

            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao remover unidade: {e}")

    def editar_unidade(self, event):
        """Ação de duplo clique para editar unidade."""
        # A seleção já foi tratada pelo evento de seleção
        pass

    def salvar_e_fechar(self):
        """Salva as alterações e fecha a janela."""
        try:
            # Chama callback se fornecido
            if self.callback_salvar:
                self.callback_salvar()

            messagebox.showinfo("Sucesso", "Unidades salvas com sucesso!")
            self.janela.destroy()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar: {e}")


# --- Bloco de Teste ---
if __name__ == "__main__":
    print("--- Teste: ui/componentes/gerenciador_unidades.py ---")

    # Importa dados de exemplo para teste
    from configuracao.definicoes import CONFIG_EXEMPLO, UNIDADES_EXEMPLO, CONSUMOS_EXEMPLO

    # Cria sistema de teste
    sistema_teste = SistemaEnergia(
        configuracao=CONFIG_EXEMPLO,
        unidades=UNIDADES_EXEMPLO.copy(),  # Cópia para não modificar o original
        consumos=CONSUMOS_EXEMPLO.copy()
    )


    def callback_teste():
        print("✓ Callback de salvamento chamado!")
        print(f"Total de unidades: {len(sistema_teste.unidades)}")
        for unidade in sistema_teste.unidades:
            print(f"  - {unidade.codigo}: {unidade.nome}")


    # Cria janela principal para teste
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal

    print("Abrindo gerenciador de unidades...")
    janela_gerenciador = JanelaGerenciadorUnidades(root, sistema_teste, callback_teste)

    print("✓ Gerenciador de unidades criado!")
    print("✓ Lista de unidades carregada!")
    print("Interaja com a janela... (Feche para continuar)")
    print("Dicas:")
    print("  - Clique em uma unidade para selecioná-la")
    print("  - Duplo clique para editar")
    print("  - Use os botões para adicionar/atualizar/remover")

    root.mainloop()

    print("Teste de Gerenciador de Unidades concluído!")