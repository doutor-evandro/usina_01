"""
Sistema de Energia Solar - Versão 2.0 Legacy Compatible
Arquivo principal de execução - Interface Gráfica
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox, filedialog
import traceback

# Adicionar o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from configuracao.definicoes import (
    obter_sistema_padrao, VERSAO_SISTEMA,
    CONFIGURACOES_UI, MENSAGENS_SISTEMA
)
from dados.repositorio import RepositorioDados
from dados.migrador import migrar_arquivo_legacy, validar_antes_migrar
from negocio.calculadora_energia import CalculadoraEnergia
from negocio.gerenciador_distribuicao import GerenciadorDistribuicao
from negocio.gerador_relatorios import GeradorRelatorios
from ui.graficos.graficos_analise import GeradorGraficosAnalise, gerar_grafico_sistema_legacy
from nucleo.excecoes import ErroSistemaEnergia
from utilitarios.formatadores import formatar_moeda, formatar_energia, formatar_percentual


class SistemaEnergiaSolar:
    """Classe principal do sistema de energia solar"""

    def __init__(self):
        self.sistema = None
        self.repositorio = RepositorioDados()
        self.calculadora = None
        self.gerenciador = None
        self.gerador_relatorios = None
        self.gerador_graficos = None

        # Tentar carregar sistema existente
        self._carregar_sistema_inicial()

    def _carregar_sistema_inicial(self):
        """Carrega sistema inicial ou cria um padrão"""
        try:
            # Tentar carregar sistema existente
            self.sistema = self.repositorio.carregar_sistema()
            print(f"✅ Sistema carregado: {self.sistema.versao_sistema}")
        except:
            # Se não conseguir carregar, usar sistema padrão
            self.sistema = obter_sistema_padrao()
            print(f"✅ Sistema padrão criado: {self.sistema.versao_sistema}")

        # Inicializar componentes
        self._inicializar_componentes()

    def _inicializar_componentes(self):
        """Inicializa todos os componentes do sistema"""
        self.calculadora = CalculadoraEnergia(self.sistema)
        self.gerenciador = GerenciadorDistribuicao(self.sistema)
        self.gerador_relatorios = GeradorRelatorios(self.sistema)
        self.gerador_graficos = GeradorGraficosAnalise(self.sistema)

    def migrar_arquivo_legacy(self, caminho_arquivo: str) -> bool:
        """Migra arquivo do sistema legacy"""
        try:
            print(f"🔄 Migrando arquivo: {caminho_arquivo}")

            # Validar arquivo antes de migrar
            if not validar_antes_migrar(caminho_arquivo):
                print("❌ Arquivo inválido para migração")
                return False

            # Migrar arquivo
            sistema_migrado = migrar_arquivo_legacy(caminho_arquivo)

            # Atualizar sistema atual
            self.sistema = sistema_migrado
            self._inicializar_componentes()

            # Salvar sistema migrado
            self.repositorio.salvar_sistema(self.sistema)

            print("✅ Migração concluída com sucesso!")
            return True

        except Exception as e:
            print(f"❌ Erro na migração: {e}")
            return False

    def gerar_relatorio_completo(self, ano: int = None) -> str:
        """Gera relatório completo do sistema"""
        try:
            print("📊 Gerando relatório completo...")

            relatorio = self.gerador_relatorios.gerar_relatorio_completo(ano)

            # Salvar relatório
            nome_arquivo = f"relatorio_energia_{ano or 2024}.txt"
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                f.write(relatorio)

            print(f"✅ Relatório salvo: {nome_arquivo}")
            return nome_arquivo

        except Exception as e:
            print(f"❌ Erro ao gerar relatório: {e}")
            return ""

    def gerar_graficos_analise(self, ano: int = None) -> list:
        """Gera gráficos de análise"""
        try:
            print("📈 Gerando gráficos de análise...")

            arquivos_gerados = []

            # Gráficos principais
            graficos = [
                ('geracao_consumo', 'Geração vs Consumo'),
                ('economia', 'Economia Mensal'),
                ('saldo', 'Saldo Energético'),
                ('distribuicao', 'Distribuição de Consumo'),
                ('dashboard', 'Dashboard Completo')
            ]

            for tipo, nome in graficos:
                try:
                    arquivo = gerar_grafico_sistema_legacy(
                        self.sistema, tipo, ano=ano, salvar=True,
                        caminho=f"grafico_{tipo}_{ano or 2024}.png"
                    )
                    arquivos_gerados.append(arquivo)
                    print(f"  ✅ {nome}: {arquivo}")
                except Exception as e:
                    print(f"  ❌ {nome}: {e}")

            print(f"✅ Gráficos gerados: {len(arquivos_gerados)}")
            return arquivos_gerados

        except Exception as e:
            print(f"❌ Erro ao gerar gráficos: {e}")
            return []

    def calcular_resultados_anuais(self, ano: int = None) -> dict:
        """Calcula resultados anuais do sistema"""
        try:
            print("🔢 Calculando resultados anuais...")

            resultado_energia = self.calculadora.calcular_resultado_anual_energia(ano)
            resultado_financeiro = self.gerenciador.calcular_resultado_financeiro_anual(ano)

            # Usar apenas os atributos que existem nos modelos
            resultados = {
                'energia': {
                    'geracao_total': resultado_energia.geracao_total_kwh,
                    'consumo_total': resultado_energia.consumo_total_kwh,
                    'saldo_anual': resultado_energia.saldo_anual_kwh,
                    'eficiencia_media': resultado_energia.eficiencia_media
                },
                'financeiro': {
                    'economia_total': resultado_financeiro.economia_total,
                    'payback_anos': resultado_financeiro.payback_simples_anos,
                    'roi_percentual': resultado_financeiro.roi_percentual,
                    'valor_investimento': resultado_financeiro.valor_investimento
                }
            }

            print("✅ Resultados calculados com sucesso!")
            return resultados

        except Exception as e:
            print(f"❌ Erro ao calcular resultados: {e}")
            import traceback
            traceback.print_exc()
            return {}

    def exibir_resumo_sistema(self):
        """Exibe resumo do sistema atual"""
        print("\n" + "=" * 60)
        print(f"📋 RESUMO DO SISTEMA - {self.sistema.versao_sistema}")
        print("=" * 60)

        # Informações do sistema
        config = self.sistema.configuracao
        print(f"🔋 Potência Instalada: {config.potencia_instalada_kw:.1f} kW")
        print(f"⚡ Eficiência: {config.eficiencia_sistema:.1%}")
        print(f"💰 Investimento: {formatar_moeda(config.custo_investimento)}")
        print(f"💡 Tarifa Energia: {formatar_moeda(config.tarifa_energia_kwh)}/kWh")

        # Unidades ativas
        unidades_ativas = self.sistema.get_unidades_ativas()
        print(f"�� Unidades Ativas: {len(unidades_ativas)}")

        for unidade in unidades_ativas:
            consumo_anual = sum(unidade.consumo_mensal_kwh)
            print(f"  - {unidade.nome}: {formatar_energia(consumo_anual)}/ano")

        # Resultados anuais
        try:
            resultados = self.calcular_resultados_anuais()
            if resultados:
                energia = resultados['energia']
                financeiro = resultados['financeiro']

                print(f"\n📊 RESULTADOS ANUAIS:")
                print(f"⚡ Geração: {formatar_energia(energia['geracao_total'])}")
                print(f"🏠 Consumo: {formatar_energia(energia['consumo_total'])}")
                print(f"💰 Economia: {formatar_moeda(financeiro['economia_total'])}")
                print(f"📈 Payback: {financeiro['payback_anos']:.1f} anos")
                print(f"💹 ROI (25 anos): {formatar_percentual(financeiro['roi_percentual'])}")
        except:
            print("⚠️ Não foi possível calcular resultados anuais")

        print("=" * 60)


def iniciar_interface_grafica():
    """Inicia a interface gráfica do sistema"""
    try:
        print("🖼️ Iniciando interface gráfica...")

        # Importar janela unificada
        from ui.janela_unificada import JanelaUnificada

        # Criar e executar aplicação
        app = JanelaUnificada()
        app.executar()

        print("👋 Interface gráfica encerrada!")

    except ImportError as e:
        print(f"❌ Erro ao importar interface: {e}")
        print("💡 Tentando fallback para janela principal...")

        # Fallback para janela principal
        try:
            from ui.janela_principal import InterfacePrincipal
            app = InterfacePrincipal()
            app.executar()
        except Exception as fallback_error:
            print(f"❌ Erro no fallback: {fallback_error}")
            return False

    except Exception as e:
        print(f"❌ Erro na interface gráfica: {e}")
        traceback.print_exc()
        return False

    return True


def _on_tipo_grafico_changed(self, event=None):
    """Evento chamado quando o tipo de gráfico é alterado"""
    print(f"🔄 Tipo alterado para: {self.var_tipo_grafico.get()}")
    self._atualizar_grafico_integrado()


def _atualizar_grafico_integrado(self):
    """Atualiza gráfico integrado"""
    try:
        tipo = self.var_tipo_grafico.get()
        print(f"📊 Gerando gráfico: {tipo}")

        # Verificar se matplotlib está disponível
        try:
            import matplotlib.pyplot as plt
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        except ImportError as e:
            print(f"❌ Erro ao importar matplotlib: {e}")
            self._mostrar_erro_grafico("Matplotlib não disponível")
            return

        # Verificar se frame existe
        if not hasattr(self, 'frame_grafico_canvas'):
            print("❌ Frame do gráfico não existe")
            return

        # Limpar canvas anterior
        for widget in self.frame_grafico_canvas.winfo_children():
            widget.destroy()

        # Criar nova figura
        fig = plt.Figure(figsize=(10, 5), dpi=100, facecolor='white')
        ax = fig.add_subplot(111)

        # Dados de exemplo
        meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
                 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        geracao = [15162, 12453, 12500, 10423, 9002, 6675,
                   8197, 9954, 11561, 13234, 14000, 14606]
        consumo = [8800] * 12

        if tipo == "Geração vs Consumo":
            # Criar barras
            x_pos = range(len(meses))
            width = 0.35

            bars1 = ax.bar([x - width / 2 for x in x_pos], geracao, width,
                           label='Geração', color=self.cores['primaria'], alpha=0.8)
            bars2 = ax.bar([x + width / 2 for x in x_pos], consumo, width,
                           label='Consumo', color=self.cores['secundaria'], alpha=0.8)

            ax.set_ylabel('Energia (kWh)', fontsize=12)
            ax.set_title('Geração vs Consumo Mensal', fontsize=14, fontweight='bold')
            ax.set_xticks(x_pos)
            ax.set_xticklabels(meses)
            ax.legend(fontsize=11)

            # Adicionar valores nas barras (apenas alguns para não poluir)
            for i, bar in enumerate(bars1):
                if i % 2 == 0:  # Mostrar apenas valores alternados
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width() / 2., height + 200,
                            f'{int(height / 1000)}k', ha='center', va='bottom', fontsize=9)

        elif tipo == "Economia Mensal":
            economia = [4000, 3200, 3250, 2800, 2400, 1800, 2200, 2650, 3100, 3550, 3750, 3900]

            # Linha principal
            line = ax.plot(meses, economia, marker='o', linewidth=3,
                           color=self.cores['sucesso'], markersize=8,
                           markerfacecolor='white', markeredgewidth=2)

            # Área preenchida
            ax.fill_between(meses, economia, alpha=0.3, color=self.cores['sucesso'])

            # Linha de tendência
            import numpy as np
            x_num = np.arange(len(economia))
            z = np.polyfit(x_num, economia, 1)
            p = np.poly1d(z)
            ax.plot(meses, p(x_num), "--", alpha=0.8, color='red', linewidth=2, label='Tendência')

            ax.set_ylabel('Economia (R$)', fontsize=12)
            ax.set_title('Economia Mensal Estimada', fontsize=14, fontweight='bold')
            ax.legend(fontsize=11)

            # Adicionar valores nos pontos
            for i, v in enumerate(economia):
                if i % 3 == 0:  # Mostrar apenas alguns valores
                    ax.text(i, v + 100, f'R${v:,.0f}', ha='center', va='bottom', fontsize=9)

        elif tipo == "Saldo Energético":
            saldo = [6362, 3653, 3700, 1623, 202, -2125, -603, 1154, 2761, 4434, 5200, 5806]
            cores_saldo = ['#2ECC71' if s >= 0 else '#E74C3C' for s in saldo]

            bars = ax.bar(meses, saldo, color=cores_saldo, alpha=0.7, edgecolor='black', linewidth=0.5)
            ax.set_ylabel('Saldo (kWh)', fontsize=12)
            ax.set_title('Saldo Energético Mensal', fontsize=14, fontweight='bold')
            ax.axhline(y=0, color='black', linestyle='-', alpha=0.8, linewidth=2)

            # Adicionar rótulos nos valores extremos
            for i, (bar, valor) in enumerate(zip(bars, saldo)):
                if abs(valor) > 3000:  # Mostrar apenas valores significativos
                    height = bar.get_height()
                    va = 'bottom' if height >= 0 else 'top'
                    offset = 200 if height >= 0 else -200
                    ax.text(bar.get_x() + bar.get_width() / 2., height + offset,
                            f'{int(valor)}', ha='center', va=va, fontsize=9, fontweight='bold')

        # Configurações gerais
        ax.set_xlabel('Meses', fontsize=12)
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.tick_params(axis='x', rotation=45, labelsize=10)
        ax.tick_params(axis='y', labelsize=10)

        # Melhorar aparência
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#CCCCCC')
        ax.spines['bottom'].set_color('#CCCCCC')

        # Ajustar layout
        fig.tight_layout(pad=2.0)

        # Criar canvas e adicionar ao frame
        canvas = FigureCanvasTkAgg(fig, self.frame_grafico_canvas)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)

        print(f"✅ Gráfico '{tipo}' criado com sucesso!")

    except Exception as e:
        print(f"❌ Erro detalhado ao atualizar gráfico: {e}")
        import traceback
        traceback.print_exc()
        self._mostrar_erro_grafico(str(e))


def _mostrar_erro_grafico(self, erro):
    """Mostra erro no lugar do gráfico"""
    # Limpar frame
    for widget in self.frame_grafico_canvas.winfo_children():
        widget.destroy()

    # Mostrar erro
    frame_erro = tk.Frame(self.frame_grafico_canvas, bg='#FFEBEE', relief=tk.RAISED, bd=2)
    frame_erro.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    tk.Label(frame_erro, text="❌ Erro no Gráfico",
             font=('Arial', 16, 'bold'), fg='#D32F2F', bg='#FFEBEE').pack(pady=10)

    tk.Label(frame_erro, text=f"Erro: {erro}",
             font=('Arial', 10), fg='#666', bg='#FFEBEE', wraplength=400).pack()

    tk.Button(frame_erro, text="🔄 Tentar Novamente",
              command=self._atualizar_grafico_integrado,
              bg='#2196F3', fg='white', font=('Arial', 10, 'bold'),
              relief=tk.RAISED, bd=2, padx=20, pady=5).pack(pady=10)

def main():
    """Função principal - Inicia diretamente a interface gráfica"""
    try:
        print(f"🌞 Iniciando Sistema de Energia Solar - {VERSAO_SISTEMA}")
        print("=" * 60)
        print("🖼️ Modo: Interface Gráfica")
        print("=" * 60)

        # Verificar se tkinter está disponível
        try:
            import tkinter as tk
            # Teste rápido do tkinter
            root = tk.Tk()
            root.withdraw()  # Ocultar janela de teste
            root.destroy()
            print("✅ Tkinter disponível")
        except Exception as e:
            print(f"❌ Tkinter não disponível: {e}")
            print("💡 Instale o tkinter para usar a interface gráfica")
            return

        # Iniciar interface gráfica
        sucesso = iniciar_interface_grafica()

        if not sucesso:
            print("\n" + "=" * 60)
            print("❌ Não foi possível iniciar a interface gráfica")
            print("💡 Executando modo console como fallback...")
            print("=" * 60)

            # Fallback para modo console (opcional)
            sistema = SistemaEnergiaSolar()
            sistema.exibir_resumo_sistema()

    except KeyboardInterrupt:
        print("\n👋 Sistema encerrado pelo usuário")
    except Exception as e:
        print(f"❌ Erro crítico: {e}")
        print("📋 Traceback:")
        traceback.print_exc()


if __name__ == "__main__":
    main()