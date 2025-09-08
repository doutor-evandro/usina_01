# criar_estrutura_interna.py
import os


def criar_estrutura_interna_usina_01():
    """
    Cria a estrutura de diretórios e arquivos vazios DENTRO do diretório atual.
    Assume que o script está sendo executado a partir da pasta raiz do projeto (usina_01).
    """

    # A base agora é o diretório atual onde o script está sendo executado
    base_path = os.getcwd()

    # Define a estrutura do projeto como uma lista de tuplas (caminho_relativo, tipo)
    # 'dir' para diretórios, 'file' para arquivos.
    # Certifique-se de incluir '__init__.py' para cada pacote Python.
    structure = [
        # Arquivos na raiz do projeto (se ainda não existirem)
        (os.path.join(base_path, "main.py"), 'file'),
        (os.path.join(base_path, "requirements.txt"), 'file'),
        (os.path.join(base_path, "README.md"), 'file'),

        # nucleo/
        (os.path.join(base_path, "nucleo"), 'dir'),
        (os.path.join(base_path, "nucleo", "__init__.py"), 'file'),
        (os.path.join(base_path, "nucleo", "modelos.py"), 'file'),
        (os.path.join(base_path, "nucleo", "validadores.py"), 'file'),
        (os.path.join(base_path, "nucleo", "excecoes.py"), 'file'),

        # negocio/
        (os.path.join(base_path, "negocio"), 'dir'),
        (os.path.join(base_path, "negocio", "__init__.py"), 'file'),
        (os.path.join(base_path, "negocio", "calculadora_energia.py"), 'file'),
        (os.path.join(base_path, "negocio", "gerenciador_distribuicao.py"), 'file'),
        (os.path.join(base_path, "negocio", "gerador_relatorios.py"), 'file'),

        # dados/
        (os.path.join(base_path, "dados"), 'dir'),
        (os.path.join(base_path, "dados", "__init__.py"), 'file'),
        (os.path.join(base_path, "dados", "repositorio.py"), 'file'),
        (os.path.join(base_path, "dados", "migrador.py"), 'file'),
        (os.path.join(base_path, "dados", "exportador_excel.py"), 'file'),

        # ui/
        (os.path.join(base_path, "ui"), 'dir'),
        (os.path.join(base_path, "ui", "__init__.py"), 'file'),
        (os.path.join(base_path, "ui", "janela_principal.py"), 'file'),

        # ui/componentes/
        (os.path.join(base_path, "ui", "componentes"), 'dir'),
        (os.path.join(base_path, "ui", "componentes", "__init__.py"), 'file'),
        (os.path.join(base_path, "ui", "componentes", "gerenciador_unidades.py"), 'file'),
        (os.path.join(base_path, "ui", "componentes", "painel_consumo.py"), 'file'),
        (os.path.join(base_path, "ui", "componentes", "configuracao_sistema.py"), 'file'),
        (os.path.join(base_path, "ui", "componentes", "painel_relatorio_texto.py"), 'file'),
        (os.path.join(base_path, "ui", "componentes", "painel_selecao_unidade.py"), 'file'),
        (os.path.join(base_path, "ui", "componentes", "painel_historico_unidade.py"), 'file'),

        # ui/graficos/
        (os.path.join(base_path, "ui", "graficos"), 'dir'),
        (os.path.join(base_path, "ui", "graficos", "__init__.py"), 'file'),
        (os.path.join(base_path, "ui", "graficos", "gerenciador_graficos.py"), 'file'),
        (os.path.join(base_path, "ui", "graficos", "graficos_analise.py"), 'file'),

        # utilitarios/
        (os.path.join(base_path, "utilitarios"), 'dir'),
        (os.path.join(base_path, "utilitarios", "__init__.py"), 'file'),
        (os.path.join(base_path, "utilitarios", "formatadores.py"), 'file'),
        (os.path.join(base_path, "utilitarios", "constantes.py"), 'file'),

        # configuracao/
        (os.path.join(base_path, "configuracao"), 'dir'),
        (os.path.join(base_path, "configuracao", "__init__.py"), 'file'),
        (os.path.join(base_path, "configuracao", "definicoes.py"), 'file'),
    ]

    print(f"Iniciando a criação da estrutura interna do projeto no diretório atual ({base_path})...")

    for path, item_type in structure:
        if item_type == 'dir':
            os.makedirs(path, exist_ok=True)
            print(f"  Diretório '{os.path.relpath(path, base_path)}' criado/verificado.")
        elif item_type == 'file':
            # Garante que o diretório pai exista antes de criar o arquivo
            directory = os.path.dirname(path)
            if directory:
                os.makedirs(directory, exist_ok=True)

            # Cria o arquivo vazio, mas apenas se ele não existir
            if not os.path.exists(path):
                with open(path, 'w', encoding='utf-8') as f:
                    pass
                print(f"  Arquivo '{os.path.relpath(path, base_path)}' criado.")
            else:
                print(f"  Arquivo '{os.path.relpath(path, base_path)}' já existe, ignorando.")

    print(f"\nEstrutura interna do projeto criada com sucesso no diretório atual!")


if __name__ == "__main__":
    criar_estrutura_interna_usina_01()