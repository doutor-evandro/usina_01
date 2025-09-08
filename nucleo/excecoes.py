# usina_01/nucleo/excecoes.py

"""
Módulo de exceções personalizadas do sistema.
Define todas as exceções específicas do domínio da aplicação.
"""


class ErroSistema(Exception):
    """
    Exceção base para todos os erros do sistema.
    """
    pass


class ErroValidacao(ErroSistema):
    """
    Exceção para erros de validação de dados.
    """
    pass


class ErroCarregamentoDados(ErroSistema):
    """
    Exceção para erros ao carregar dados.
    """
    pass


class ErroSalvamentoDados(ErroSistema):
    """
    Exceção para erros ao salvar dados.
    """
    pass


class ErroCalculoEnergia(ErroSistema):
    """
    Exceção para erros nos cálculos energéticos.
    """
    pass


class ErroCalculoFinanceiro(ErroSistema):
    """
    Exceção para erros nos cálculos financeiros.
    """
    pass


class ErroGeracaoRelatorio(ErroSistema):
    """
    Exceção para erros na geração de relatórios.
    """
    pass


class ErroConfiguracaoSistema(ErroSistema):
    """
    Exceção para erros na configuração do sistema.
    """
    pass


class ErroUnidadeConsumidora(ErroSistema):
    """
    Exceção para erros relacionados a unidades consumidoras.
    """
    pass


class ErroFormatacao(ErroSistema):
    """
    Exceção para erros de formatação de dados.
    """
    pass


class ErroArquivo(ErroSistema):
    """
    Exceção para erros de manipulação de arquivos.
    """
    pass


class ErroInterface(ErroSistema):
    """
    Exceção para erros da interface gráfica.
    """
    pass


# --- Bloco de Teste ---
if __name__ == "__main__":
    print("--- Teste: nucleo/excecoes.py ---")

    # Testa todas as exceções
    excecoes_teste = [
        (ErroSistema, "Erro base do sistema"),
        (ErroValidacao, "Erro de validação"),
        (ErroCarregamentoDados, "Erro ao carregar dados"),
        (ErroSalvamentoDados, "Erro ao salvar dados"),
        (ErroCalculoEnergia, "Erro no cálculo energético"),
        (ErroCalculoFinanceiro, "Erro no cálculo financeiro"),
        (ErroGeracaoRelatorio, "Erro na geração de relatório"),
        (ErroConfiguracaoSistema, "Erro na configuração"),
        (ErroUnidadeConsumidora, "Erro na unidade consumidora"),
        (ErroFormatacao, "Erro de formatação"),
        (ErroArquivo, "Erro de arquivo"),
        (ErroInterface, "Erro de interface")
    ]

    print("Testando criação de exceções...")

    for i, (ExcecaoClass, mensagem) in enumerate(excecoes_teste, 1):
        try:
            # Testa se a exceção pode ser criada
            excecao = ExcecaoClass(mensagem)

            # Testa se é subclasse de ErroSistema
            if issubclass(ExcecaoClass, ErroSistema):
                print(f"✓ {i:2d}. {ExcecaoClass.__name__}: OK")
            else:
                print(f"❌ {i:2d}. {ExcecaoClass.__name__}: Não é subclasse de ErroSistema")

        except Exception as e:
            print(f"❌ {i:2d}. {ExcecaoClass.__name__}: Erro ao criar - {e}")

    # Testa hierarquia de exceções
    print("\nTestando hierarquia de exceções...")
    try:
        raise ErroValidacao("Teste de validação")
    except ErroSistema as e:
        print("✓ ErroValidacao é capturada como ErroSistema")
    except Exception as e:
        print(f"❌ Erro na hierarquia: {e}")

    # Testa captura específica
    print("\nTestando captura específica...")
    try:
        raise ErroCarregamentoDados("Teste de carregamento")
    except ErroCarregamentoDados as e:
        print("✓ ErroCarregamentoDados capturada especificamente")
    except Exception as e:
        print(f"❌ Erro na captura específica: {e}")

    print("\nTeste de Exceções concluído com sucesso!")