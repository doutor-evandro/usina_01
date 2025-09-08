# usina_01/ui/componentes/painel_relatorio_texto.py

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from nucleo.modelos import SistemaEnergia
from negocio.calculadora_energia import CalculadoraEnergia
from negocio.gerenciador_distribuicao import GerenciadorDistribuicao
from nucleo.excecoes import ErroCalculoEnergia, ErroCalculoFinanceiro


class PainelRelatorioTextoUI(ttk.Frame):
    """
    Interface para exibir relatórios textuais detalhados sobre o sistema.
    """

    def __init__(self, parent, sistema_energia):
        super().__init__(parent)
        self.sistema_energia = sistema_energia
        self.calculadora_energia = CalculadoraEnergia(sistema_energia)
        self.gerenciador_distribuicao = GerenciadorDistribuicao(sistema_energia)

        self.criar_widgets()
        self.gerar_relatorio()  # Gera o relatório inicial

    def criar_widgets(self):
        """Cria e organiza os widgets da interface."""
        main_frame = ttk.LabelFrame(self, text="Relatório Detalhado do Sistema", padding="15")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Área de texto para o relatório
        self.relatorio_text = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, width=100, height=30,
                                                        font=("Courier New", 10))
        self.relatorio_text.pack(fill="both", expand=True, pady=10)
        self.relatorio_text.config(state="disabled")  # Torna a área de texto somente leitura

        # Botão para atualizar o relatório
        ttk.Button(main_frame, text="Atualizar Relatório", command=self.gerar_relatorio).pack(pady=5)

    def gerar_relatorio(self):
        """Gera o relatório completo e exibe na área de texto."""
        self.relatorio_text.config(state="normal")  # Habilita edição temporariamente
        self.relatorio_text.delete(1.0, tk.END)  # Limpa o conteúdo anterior

        relatorio = []
        relatorio.append("=" * 50)
        relatorio.append(f"RELATÓRIO DO SISTEMA DE ENERGIA SOLAR")
        relatorio.append("=" * 50)
        relatorio.append("\n")

        # --- Seção de Configurações ---
        relatorio.append("--- CONFIGURAÇÕES DO SISTEMA ---")
        config = self.sistema_energia.configuracao
        relatorio.append(f"Potência de Pico: {config.potencia_pico_kwp:.2f} kWp")
        relatorio.append(f"Eficiência do Sistema: {config.eficiencia_sistema:.2f}%")
        relatorio.append(f"Tarifa kWh: R\$ {config.tarifa_kwh:.3f}/kWh")
        relatorio.append(f"Custo Fixo Mensal: R\$ {config.custo_fixo_mensal:.2f}")
        relatorio.append(f"Tarifa Mínima: {config.tarifa_minima:.2f} kWh")
        relatorio.append(f"Bandeira Tarifária: {config.bandeira_tarifaria_atual.value.upper()}")
        relatorio.append(f"Custo Bandeira kWh: R\$ {config.custo_bandeira_kwh:.3f}/kWh")
        relatorio.append("\nGeração Mensal Esperada (kWh):")
        for mes, geracao in config.geracao_mensal.items():
            relatorio.append(f"  {mes}: {geracao:.2f} kWh")
        relatorio.append("\n")

        # --- Seção de Unidades Consumidoras ---
        relatorio.append("--- UNIDADES CONSUMIDORAS ---")
        if not self.sistema_energia.unidades:
            relatorio.append("Nenhuma unidade consumidora cadastrada.")
        else:
            for i, uc in enumerate(self.sistema_energia.unidades):
                relatorio.append(f"  Unidade {i + 1}:")
                relatorio.append(f"    Código: {uc.codigo}")
                relatorio.append(f"    Nome: {uc.nome}")
                relatorio.append(f"    Endereço: {uc.endereco if uc.endereco else 'Não informado'}")
                relatorio.append(f"    Tipo de Ligação: {uc.tipo_ligacao.value.upper()}")
                relatorio.append("-" * 20)
        relatorio.append("\n")

        # --- Seção de Consumo Mensal ---
        relatorio.append("--- CONSUMO MENSAL POR UNIDADE (kWh) ---")
        if not self.sistema_energia.consumos:
            relatorio.append("Nenhum dado de consumo registrado.")
        else:
            for codigo_uc, consumos_mes in self.sistema_energia.consumos.items():
                relatorio.append(f"  Unidade: {codigo_uc}")
                for mes in MESES_APENAS:
                    relatorio.append(f"    {mes}: {consumos_mes.get(mes, 0.0):.2f} kWh")
                relatorio.append("-" * 20)
        relatorio.append("\n")

        # --- Seção de Resultados Energéticos Anuais ---
        relatorio.append("--- RESULTADOS ENERGÉTICOS ANUAIS ---")
        try:
            resultados_energeticos, resumo_energia = self.calculadora_energia.calcular_resultados_anuais()
            relatorio.append(f"Total Geração Anual: {resumo_energia.total_geracao_anual_kwh:.2f} kWh")
            relatorio.append(f"Total Consumo Anual: {resumo_energia.total_consumo_anual_kwh:.2f} kWh")
            relatorio.append(f"Total Excedente Anual: {resumo_energia.total_excedente_anual_kwh:.2f} kWh")
            relatorio.append(f"Total Déficit Anual: {resumo_energia.total_deficit_anual_kwh:.2f} kWh")

            relatorio.append("\nDetalhes Mensais (Energia):")
            for mes, res_mes in resultados_energeticos.resultados_por_mes.items():
                relatorio.append(
                    f"  {res_mes.mes}: Geração={res_mes.geracao_kwh:.2f} kWh, Consumo={res_mes.consumo_total_kwh:.2f} kWh, Saldo={res_mes.saldo_kwh:.2f} kWh, Excedente={res_mes.excedente_kwh:.2f} kWh, Déficit={res_mes.deficit_kwh:.2f} kWh")

        except (ErroCalculoEnergia, Exception) as e:
            relatorio.append(f"Erro ao calcular resultados energéticos: {e}")
        relatorio.append("\n")

        # --- Seção de Resultados Financeiros Anuais ---
        relatorio.append("--- RESULTADOS FINANCEIROS ANUAIS ---")
        try:
            resultados_financeiros, resumo_financeiro = self.gerenciador_distribuicao.calcular_resultados_financeiros_anuais()
            relatorio.append(f"Total Economia Anual Estimada: R\$ {resumo_financeiro.total_economia_anual_reais:.2f}")
            # Adicionar Payback e ROI aqui quando implementados no gerenciador_distribuicao

            relatorio.append("\nDetalhes Mensais (Financeiro):")
            for mes, res_mes_fin in resultados_financeiros.resultados_por_mes.items():
                relatorio.append(
                    f"  {res_mes_fin.mes}: Custo Sem Solar=R\$ {res_mes_fin.custo_sem_solar_reais:.2f}, Custo Com Solar=R\$ {res_mes_fin.custo_com_solar_reais:.2f}, Economia=R\$ {res_mes_fin.economia_reais:.2f}, Crédito Gerado={res_mes_fin.credito_gerado_kwh:.2f} kWh, Crédito Utilizado={res_mes_fin.credito_utilizado_kwh:.2f} kWh, Crédito Acumulado={res_mes_fin.credito_acumulado_kwh:.2f} kWh")

        except (ErroCalculoFinanceiro, Exception) as e:
            relatorio.append(f"Erro ao calcular resultados financeiros: {e}")
        relatorio.append("\n")

        relatorio.append("=" * 50)
        relatorio.append("FIM DO RELATÓRIO")
        relatorio.append("=" * 50)

        self.relatorio_text.insert(tk.END, "\n".join(relatorio))
        self.relatorio_text.config(state="disabled")  # Desabilita edição novamente


# --- Bloco de Teste ---
if __name__ == "__main__":
    print("--- Teste: ui/componentes/painel_relatorio_texto.py ---")
    import sys
    import os

    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

    from nucleo.modelos import SistemaEnergia
    from configuracao.definicoes import CONFIG_EXEMPLO, UNIDADES_EXEMPLO, CONSUMOS_EXEMPLO

    root = tk.Tk()
    root.title("Teste de Painel de Relatório")

    sistema_teste = SistemaEnergia(
        configuracao=CONFIG_EXEMPLO,
        unidades=UNIDADES_EXEMPLO,
        consumos=CONSUMOS_EXEMPLO
    )

    painel_relatorio = PainelRelatorioTextoUI(root, sistema_teste)
    painel_relatorio.pack(fill="both", expand=True)

    root.mainloop()
    print("✓ Teste de PainelRelatorioTextoUI concluído!")