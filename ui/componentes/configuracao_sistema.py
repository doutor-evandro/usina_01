# usina_01/ui/componentes/configuracao_sistema.py

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Callable

from nucleo.modelos import SistemaEnergia, ConfiguracaoSistema
from utilitarios.constantes import MESES_APENAS


class JanelaConfiguracaoSistema:
    """
    Janela para configuração dos parâmetros do sistema de energia solar.
    """

    def __init__(self, parent: tk.Tk, sistema: SistemaEnergia, callback_salvar: Optional[Callable] = None):
        self.parent = parent
        self.sistema = sistema
        self.callback_salvar = callback_salvar

        # Cria a janela
        self.janela = tk.Toplevel(parent)
        self.configurar_janela()
        self.criar_interface()
        self.carregar_dados()

    def configurar_janela(self):
        """Configura as propriedades da janela."""
        self.janela.title("Configuração do Sistema")
        self.janela.geometry("600x700")
        self.janela.resizable(False, False)

        # Centraliza a janela
        self.janela.update_idletasks()
        x = (self.janela.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.janela.winfo_screenheight() // 2) - (700 // 2)
        self.janela.geometry(f"600x700+{x}+{y}")

        # Torna a janela modal
        self.janela.transient(self.parent)
        self.janela.grab_set()

        # Foca na janela
        self.janela.focus_set()

    def criar_interface(self):
        """Cria a interface da janela."""
        # Frame principal com padding
        main_frame = ttk.Frame(self.janela, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        titulo_label = ttk.Label(main_frame, text="Configuração do Sistema de Energia Solar",
                                 font=("Arial", 14, "bold"))
        titulo_label.pack(pady=(0, 20))

        # Frame para configurações básicas
        config_frame = ttk.LabelFrame(main_frame, text="Configurações Básicas", padding="10")
        config_frame.pack(fill=tk.X, pady=(0, 10))

        # Potência do Inversor
        ttk.Label(config_frame, text="Potência do Inversor (W):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.potencia_inversor_var = tk.StringVar()
        self.potencia_inversor_entry = ttk.Entry(config_frame, textvariable=self.potencia_inversor_var, width=15)
        self.potencia_inversor_entry.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=5)

        # Potência dos Módulos
        ttk.Label(config_frame, text="Potência dos Módulos (W):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.potencia_modulos_var = tk.StringVar()
        self.potencia_modulos_entry = ttk.Entry(config_frame, textvariable=self.potencia_modulos_var, width=15)
        self.potencia_modulos_entry.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)

        # Eficiência
        ttk.Label(config_frame, text="Eficiência do Sistema (%):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.eficiencia_var = tk.StringVar()
        self.eficiencia_entry = ttk.Entry(config_frame, textvariable=self.eficiencia_var, width=15)
        self.eficiencia_entry.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=5)

        # Valor kWh
        ttk.Label(config_frame, text="Valor da Tarifa (R\$/kWh):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.valor_kwh_var = tk.StringVar()
        self.valor_kwh_entry = ttk.Entry(config_frame, textvariable=self.valor_kwh_var, width=15)
        self.valor_kwh_entry.grid(row=3, column=1, sticky=tk.W, padx=(10, 0), pady=5)

        # Frame para geração mensal
        geracao_frame = ttk.LabelFrame(main_frame, text="Geração Mensal (kWh)", padding="10")
        geracao_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))

        # Cria um canvas com scrollbar para a geração mensal
        canvas = tk.Canvas(geracao_frame, height=300)
        scrollbar = ttk.Scrollbar(geracao_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Variáveis para armazenar os valores de geração mensal
        self.geracao_vars = {}

        # Cria campos para cada mês
        for i, mes in enumerate(MESES_APENAS):
            row = i // 2
            col = (i % 2) * 2

            ttk.Label(scrollable_frame, text=f"{mes}:").grid(row=row, column=col, sticky=tk.W, padx=5, pady=2)

            var = tk.StringVar()
            self.geracao_vars[mes] = var
            entry = ttk.Entry(scrollable_frame, textvariable=var, width=12)
            entry.grid(row=row, column=col + 1, sticky=tk.W, padx=5, pady=2)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Frame para botões
        botoes_frame = ttk.Frame(main_frame)
        botoes_frame.pack(fill=tk.X, pady=(10, 0))

        # Botões de ação
        ttk.Button(botoes_frame, text="Salvar", command=self.salvar_configuracao).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(botoes_frame, text="Cancelar", command=self.janela.destroy).pack(side=tk.RIGHT)
        ttk.Button(botoes_frame, text="Aplicar Padrão", command=self.aplicar_padrao).pack(side=tk.LEFT)

    def carregar_dados(self):
        """Carrega os dados atuais do sistema na interface."""
        config = self.sistema.configuracao

        # Carrega configurações básicas
        self.potencia_inversor_var.set(str(config.potencia_inversor))
        self.potencia_modulos_var.set(str(config.potencia_modulos))
        self.eficiencia_var.set(str(config.eficiencia))
        self.valor_kwh_var.set(str(config.valor_kwh))

        # Carrega geração mensal
        for mes in MESES_APENAS:
            valor = config.geracao_mensal.get(mes, 0.0)
            self.geracao_vars[mes].set(str(valor))

    def aplicar_padrao(self):
        """Aplica valores padrão aos campos."""
        resposta = messagebox.askyesno("Aplicar Padrão",
                                       "Isso substituirá todos os valores atuais pelos padrões. Continuar?")
        if not resposta:
            return

        # Valores padrão
        self.potencia_inversor_var.set("10000")
        self.potencia_modulos_var.set("12000")
        self.eficiencia_var.set("78.0")
        self.valor_kwh_var.set("0.6305")

        # Geração mensal padrão (exemplo de sistema de 10kW)
        geracao_padrao = {
            "Janeiro": "1200", "Fevereiro": "1100", "Março": "1250",
            "Abril": "1150", "Maio": "1000", "Junho": "950",
            "Julho": "1050", "Agosto": "1200", "Setembro": "1100",
            "Outubro": "1300", "Novembro": "1250", "Dezembro": "1200"
        }

        for mes, valor in geracao_padrao.items():
            self.geracao_vars[mes].set(valor)

        messagebox.showinfo("Sucesso", "Valores padrão aplicados!")

    def validar_dados(self) -> bool:
        """Valida os dados inseridos."""
        try:
            # Valida configurações básicas
            potencia_inversor = float(self.potencia_inversor_var.get())
            potencia_modulos = float(self.potencia_modulos_var.get())
            eficiencia = float(self.eficiencia_var.get())
            valor_kwh = float(self.valor_kwh_var.get())

            if potencia_inversor <= 0:
                raise ValueError("Potência do inversor deve ser maior que zero")
            if potencia_modulos <= 0:
                raise ValueError("Potência dos módulos deve ser maior que zero")
            if not (0 < eficiencia <= 100):
                raise ValueError("Eficiência deve estar entre 0 e 100%")
            if valor_kwh <= 0:
                raise ValueError("Valor da tarifa deve ser maior que zero")

            # Valida geração mensal
            for mes in MESES_APENAS:
                valor = float(self.geracao_vars[mes].get())
                if valor < 0:
                    raise ValueError(f"Geração de {mes} não pode ser negativa")

            return True

        except ValueError as e:
            messagebox.showerror("Erro de Validação", str(e))
            return False

    def salvar_configuracao(self):
        """Salva a configuração no sistema."""
        if not self.validar_dados():
            return

        try:
            # Coleta os dados
            potencia_inversor = float(self.potencia_inversor_var.get())
            potencia_modulos = float(self.potencia_modulos_var.get())
            eficiencia = float(self.eficiencia_var.get())
            valor_kwh = float(self.valor_kwh_var.get())

            geracao_mensal = {}
            for mes in MESES_APENAS:
                geracao_mensal[mes] = float(self.geracao_vars[mes].get())

            # Cria nova configuração
            nova_configuracao = ConfiguracaoSistema(
                potencia_inversor=potencia_inversor,
                potencia_modulos=potencia_modulos,
                geracao_mensal=geracao_mensal,
                eficiencia=eficiencia,
                valor_kwh=valor_kwh
            )

            # Atualiza o sistema
            self.sistema.configuracao = nova_configuracao

            # Chama callback se fornecido
            if self.callback_salvar:
                self.callback_salvar()

            messagebox.showinfo("Sucesso", "Configuração salva com sucesso!")
            self.janela.destroy()

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar configuração: {e}")


# --- Bloco de Teste ---
if __name__ == "__main__":
    print("--- Teste: ui/componentes/configuracao_sistema.py ---")

    # Importa dados de exemplo para teste
    from configuracao.definicoes import CONFIG_EXEMPLO, UNIDADES_EXEMPLO, CONSUMOS_EXEMPLO

    # Cria sistema de teste
    sistema_teste = SistemaEnergia(
        configuracao=CONFIG_EXEMPLO,
        unidades=UNIDADES_EXEMPLO,
        consumos=CONSUMOS_EXEMPLO
    )


    def callback_teste():
        print("✓ Callback de salvamento chamado!")


    # Cria janela principal para teste
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal

    print("Abrindo janela de configuração...")
    janela_config = JanelaConfiguracaoSistema(root, sistema_teste, callback_teste)

    print("✓ Janela de configuração criada!")
    print("✓ Dados carregados na interface!")
    print("Interaja com a janela... (Feche para continuar)")

    root.mainloop()

    print("Teste de Configuração do Sistema concluído!")