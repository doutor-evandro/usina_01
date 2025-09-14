# criar_estrutura_real_completa_corrigida.py
import os


def criar_estrutura_real_completa_corrigida_usina_01():
    """
    Cria a estrutura REAL COMPLETA CORRIGIDA baseada no GitHub.
    Inclui TODOS os arquivos identificados + correções cirúrgicas.
    """

    base_path = os.getcwd()

    # ✅ ESTRUTURA REAL COMPLETA CORRIGIDA
    structure = [
        # 📁 RAIZ DO PROJETO (15 arquivos)
        (os.path.join(base_path, "main.py"), 'file'),
        (os.path.join(base_path, "requirements.txt"), 'file'),
        (os.path.join(base_path, "README.md"), 'file'),
        (os.path.join(base_path, "criar_estrutura_projeto.py"), 'file'),
        (os.path.join(base_path, "dados_sistema.json.backup"), 'file'),
        (os.path.join(base_path, "teste_legacy.xlsx"), 'file'),
        (os.path.join(base_path, "teste_sistema_completo.py"), 'file'),
        (os.path.join(base_path, "grafico_dashboard_1.png"), 'file'),
        (os.path.join(base_path, "grafico_dashboard_2025.png"), 'file'),
        (os.path.join(base_path, "grafico_economia_1.png"), 'file'),
        (os.path.join(base_path, "grafico_economia_2025.png"), 'file'),
        (os.path.join(base_path, "grafico_geracao_consumo_1.png"), 'file'),
        (os.path.join(base_path, "grafico_geracao_consumo_2025.png"), 'file'),
        (os.path.join(base_path, "grafico_saldo_1.png"), 'file'),
        (os.path.join(base_path, "grafico_saldo_2025.png"), 'file'),

        # 🎨 UI (14 arquivos - COMPLETO)
        (os.path.join(base_path, "ui"), 'dir'),
        (os.path.join(base_path, "ui", "__init__.py"), 'file'),
        (os.path.join(base_path, "ui", "janela_principal.py"), 'file'),
        (os.path.join(base_path, "ui", "janela_analises.py"), 'file'),
        (os.path.join(base_path, "ui", "janela_unificada.py"), 'file'),

        # 🎨 UI/COMPONENTES (12 arquivos - CORRIGIDO)
        (os.path.join(base_path, "ui", "componentes"), 'dir'),
        (os.path.join(base_path, "ui", "componentes", "__init__.py"), 'file'),
        (os.path.join(base_path, "ui", "componentes", "analises_module.py"), 'file'),
        (os.path.join(base_path, "ui", "componentes", "base_module.py"), 'file'),
        (os.path.join(base_path, "ui", "componentes", "configuracao_sistema.py"), 'file'),
        (os.path.join(base_path, "ui", "componentes", "dashboard_module.py"), 'file'),
        (os.path.join(base_path, "ui", "componentes", "gerenciador_unidades.py"), 'file'),
        (os.path.join(base_path, "ui", "componentes", "painel_consumo.py"), 'file'),
        (os.path.join(base_path, "ui", "componentes", "painel_historico_unidade.py"), 'file'),
        (os.path.join(base_path, "ui", "componentes", "painel_relatorio_texto.py"), 'file'),
        (os.path.join(base_path, "ui", "componentes", "painel_selecao_unidade.py"), 'file'),
        (os.path.join(base_path, "ui", "componentes", "sidebar.py"), 'file'),
        (os.path.join(base_path, "ui", "componentes", "unidades_module.py"), 'file'),

        # 📊 UI/GRÁFICOS (4 arquivos - CORRIGIDO)
        (os.path.join(base_path, "ui", "graficos"), 'dir'),
        (os.path.join(base_path, "ui", "graficos", "__init__.py"), 'file'),
        (os.path.join(base_path, "ui", "graficos", "gerenciador_graficos.py"), 'file'),
        (os.path.join(base_path, "ui", "graficos", "graficos_analise.py"), 'file'),
        (os.path.join(base_path, "ui", "graficos", "graficos_legacy.py"), 'file'),  # ⭐ ADICIONADO

        # 💼 NEGÓCIO (5 arquivos - CORRIGIDO)
        (os.path.join(base_path, "negocio"), 'dir'),
        (os.path.join(base_path, "negocio", "__init__.py"), 'file'),
        (os.path.join(base_path, "negocio", "calculadora_energia.py"), 'file'),
        (os.path.join(base_path, "negocio", "calculadora_creditos.py"), 'file'),  # ⭐ ADICIONADO
        (os.path.join(base_path, "negocio", "gerenciador_distribuicao.py"), 'file'),
        (os.path.join(base_path, "negocio", "gerador_relatorios.py"), 'file'),

        # 💾 DADOS (5 arquivos - CORRIGIDO)
        (os.path.join(base_path, "dados"), 'dir'),
        (os.path.join(base_path, "dados", "__init__.py"), 'file'),
        (os.path.join(base_path, "dados", "exportador_excel.py"), 'file'),
        (os.path.join(base_path, "dados", "gerenciador_dados_legacy.py"), 'file'),  # ⭐ ADICIONADO
        (os.path.join(base_path, "dados", "migrador.py"), 'file'),
        (os.path.join(base_path, "dados", "repositorio.py"), 'file'),

        # 🔧 NÚCLEO (4 arquivos)
        (os.path.join(base_path, "nucleo"), 'dir'),
        (os.path.join(base_path, "nucleo", "__init__.py"), 'file'),
        (os.path.join(base_path, "nucleo", "excecoes.py"), 'file'),
        (os.path.join(base_path, "nucleo", "modelos.py"), 'file'),
        (os.path.join(base_path, "nucleo", "validadores.py"), 'file'),

        # 🛠️ UTILITÁRIOS (5 arquivos - CORRIGIDO)
        (os.path.join(base_path, "utilitarios"), 'dir'),
        (os.path.join(base_path, "utilitarios", "__init__.py"), 'file'),
        (os.path.join(base_path, "utilitarios", "constantes.py"), 'file'),
        (os.path.join(base_path, "utilitarios", "formatadores.py"), 'file'),
        (os.path.join(base_path, "utilitarios", "funcoes_legacy.py"), 'file'),  # ⭐ ADICIONADO
        (os.path.join(base_path, "utilitarios", "importador_dados.py"), 'file'),  # ⭐ ADICIONADO

        # ⚙️ CONFIGURAÇÃO (3 arquivos - CORRIGIDO)
        (os.path.join(base_path, "configuracao"), 'dir'),
        (os.path.join(base_path, "configuracao", "__init__.py"), 'file'),
        (os.path.join(base_path, "configuracao", "dados_reais.py"), 'file'),  # ⭐ ADICIONADO
        (os.path.join(base_path, "configuracao", "definicoes.py"), 'file'),
    ]

    print(f"🎯 Criando estrutura REAL COMPLETA CORRIGIDA...")
    print(f"📊 Total de arquivos: {len([s for s in structure if s[1] == 'file'])}")
    print(f"📁 Total de diretórios: {len([s for s in structure if s[1] == 'dir'])}")

    for path, item_type in structure:
        if item_type == 'dir':
            os.makedirs(path, exist_ok=True)
            print(f"  📁 {os.path.relpath(path, base_path)}")

        elif item_type == 'file':
            directory = os.path.dirname(path)
            if directory:
                os.makedirs(directory, exist_ok=True)

            if not os.path.exists(path):
                with open(path, 'w', encoding='utf-8') as f:
                    if path.endswith('.py'):
                        f.write(f'"""\n{os.path.basename(path)} - Sistema Cooperativa de Energia Solar\n"""\n\n')
                    elif path.endswith('.json'):
                        f.write('{\n  "versao": "1.0"\n}\n')

                print(f"  📄 {os.path.relpath(path, base_path)} ➕ CRIADO")
            else:
                print(f"  📄 {os.path.relpath(path, base_path)} ✅ EXISTE")

    print(f"\n✅ ESTRUTURA REAL COMPLETA CORRIGIDA CRIADA!")
    print(f"📊 TOTAL FINAL: {len([s for s in structure if s[1] == 'file'])} arquivos em 7 diretórios principais")
    print(f"⭐ ADICIONADOS: 6 arquivos nas correções cirúrgicas")


if __name__ == "__main__":
    criar_estrutura_real_completa_corrigida_usina_01()