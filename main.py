# usina_01/main.py

"""
Sistema de Análise de Energia Solar - Usina 01
Arquivo principal da aplicação.

Este sistema permite:
- Configurar sistemas de energia solar
- Gerenciar unidades consumidoras
- Inserir dados de consumo
- Calcular resultados energéticos e financeiros
- Gerar relatórios completos

Desenvolvido em Python com Tkinter para interface gráfica.
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox
import traceback

# Adiciona o diretório raiz ao path para importações
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from ui.janela_principal import JanelaPrincipal
    from nucleo.excecoes import ErroSistema
    from configuracao.definicoes import VERSAO_SISTEMA
except ImportError as e:
    print(f"Erro ao importar módulos: {e}")
    print("Verifique se todos os arquivos estão no local correto.")
    sys.exit(1)


class AplicacaoUsina01:
    """
    Classe principal da aplicação Usina 01.
    Gerencia a inicialização e execução do sistema.
    """

    def __init__(self):
        self.janela_principal = None

    def verificar_dependencias(self) -> bool:
        """
        Verifica se todas as dependências estão disponíveis.

        Returns:
            bool: True se todas as dependências estão OK
        """
        try:
            # Verifica módulos essenciais
            import tkinter
            import json
            import datetime
            import dataclasses
            import typing

            print("✓ Todas as dependências verificadas com sucesso!")
            return True

        except ImportError as e:
            print(f"❌ Dependência faltando: {e}")
            return False

    def verificar_estrutura_arquivos(self) -> bool:
        """
        Verifica se a estrutura de arquivos está correta.

        Returns:
            bool: True se a estrutura está OK
        """
        arquivos_essenciais = [
            "nucleo/modelos.py",
            "nucleo/validadores.py",
            "nucleo/excecoes.py",
            "dados/repositorio.py",
            "negocio/calculadora_energia.py",
            "negocio/gerenciador_distribuicao.py",
            "negocio/gerador_relatorios.py",
            "ui/janela_principal.py",
            "ui/componentes/configuracao_sistema.py",
            "ui/componentes/gerenciador_unidades.py",
            "ui/componentes/painel_consumo.py",
            "utilitarios/formatadores.py",
            "utilitarios/constantes.py",
            "configuracao/definicoes.py"
        ]

        arquivos_faltando = []
        for arquivo in arquivos_essenciais:
            if not os.path.exists(arquivo):
                arquivos_faltando.append(arquivo)

        if arquivos_faltando:
            print("❌ Arquivos faltando:")
            for arquivo in arquivos_faltando:
                print(f"   - {arquivo}")
            return False

        print("✓ Estrutura de arquivos verificada com sucesso!")
        return True

    def inicializar_sistema(self) -> bool:
        """
        Inicializa o sistema e verifica se tudo está funcionando.

        Returns:
            bool: True se a inicialização foi bem-sucedida
        """
        try:
            print("Inicializando Sistema de Análise de Energia Solar...")
            print(f"Versão: {VERSAO_SISTEMA}")
            print("-" * 50)

            # Verifica dependências
            if not self.verificar_dependencias():
                return False

            # Verifica estrutura de arquivos
            if not self.verificar_estrutura_arquivos():
                return False

            # Testa importações críticas
            from dados.repositorio import RepositorioDados
            from negocio.calculadora_energia import CalculadoraEnergia
            from negocio.gerenciador_distribuicao import GerenciadorDistribuicao

            print("✓ Módulos de negócio carregados com sucesso!")

            # Testa criação da interface
            root_teste = tk.Tk()
            root_teste.withdraw()  # Esconde janela de teste
            root_teste.destroy()

            print("✓ Interface gráfica disponível!")
            print("-" * 50)
            print("Sistema inicializado com sucesso!")

            return True

        except Exception as e:
            print(f"❌ Erro na inicialização: {e}")
            traceback.print_exc()
            return False

    def executar(self):
        """
        Executa a aplicação principal.
        """
        try:
            # Inicializa o sistema
            if not self.inicializar_sistema():
                print("Falha na inicialização. Encerrando...")
                return False

            print("Abrindo interface principal...")

            # Cria e executa a janela principal
            self.janela_principal = JanelaPrincipal()
            self.janela_principal.executar()

            print("Aplicação encerrada pelo usuário.")
            return True

        except KeyboardInterrupt:
            print("\nAplicação interrompida pelo usuário (Ctrl+C)")
            return True

        except Exception as e:
            print(f"❌ Erro durante execução: {e}")
            traceback.print_exc()

            # Tenta mostrar erro em janela se possível
            try:
                root = tk.Tk()
                root.withdraw()
                messagebox.showerror(
                    "Erro Fatal",
                    f"Erro inesperado na aplicação:\n\n{e}\n\nVerifique o console para mais detalhes."
                )
                root.destroy()
            except:
                pass

            return False

    def mostrar_ajuda(self):
        """Mostra informações de ajuda sobre o sistema."""
        ajuda = f"""
Sistema de Análise de Energia Solar - Usina 01
Versão: {VERSAO_SISTEMA}

DESCRIÇÃO:
Sistema para análise e gerenciamento de sistemas de energia solar
fotovoltaica com múltiplas unidades consumidoras.

FUNCIONALIDADES:
• Configuração de sistema solar (potências, eficiência, tarifa)
• Gerenciamento de unidades consumidoras
• Inserção de dados de consumo mensal
• Cálculos energéticos automáticos
• Análises financeiras e payback
• Geração de relatórios completos
• Exportação de dados

COMO USAR:
1. Execute: python main.py
2. Configure o sistema (Menu Ferramentas > Configurar Sistema)
3. Adicione unidades (Menu Ferramentas > Gerenciar Unidades)
4. Insira consumos (Menu Ferramentas > Inserir Consumos)
5. Visualize resultados na interface principal
6. Gere relatórios (Menu Arquivo > Exportar Relatório)

ARQUIVOS DE DADOS:
• dados_sistema.json - Dados principais do sistema
• Backups automáticos são criados

SUPORTE:
• Verifique a documentação no código
• Consulte os exemplos em configuracao/definicoes.py

© 2025 - Sistema Usina 01
"""
        print(ajuda)


def main():
    """
    Função principal do programa.
    """
    # Verifica argumentos da linha de comando
    if len(sys.argv) > 1:
        if sys.argv[1] in ["-h", "--help", "help"]:
            app = AplicacaoUsina01()
            app.mostrar_ajuda()
            return
        elif sys.argv[1] in ["-v", "--version", "version"]:
            print(f"Sistema Usina 01 - Versão {VERSAO_SISTEMA}")
            return

    # Executa a aplicação
    app = AplicacaoUsina01()
    sucesso = app.executar()

    # Código de saída
    sys.exit(0 if sucesso else 1)


if __name__ == "__main__":
    main()