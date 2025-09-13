"""
Exceções personalizadas do sistema de energia solar
Versão adaptada com exceções do sistema legacy
"""

import json


class ErroSistemaEnergia(Exception):
    """Exceção base para erros do sistema de energia"""
    pass


class ErroValidacao(ErroSistemaEnergia):
    """Erro de validação de dados"""
    pass


class ErroCalculoEnergia(ErroSistemaEnergia):
    """Erro nos cálculos energéticos"""
    pass


class ErroCalculoFinanceiro(ErroSistemaEnergia):
    """Erro nos cálculos financeiros"""
    pass


class ErroPersistenciaDados(ErroSistemaEnergia):
    """Erro na persistência de dados"""
    pass


class ErroCarregamentoDados(ErroSistemaEnergia):
    """Erro no carregamento de dados"""
    pass


class ErroSalvamentoDados(ErroSistemaEnergia):
    """Erro no salvamento de dados"""
    pass


class ErroMigracaoDados(ErroSistemaEnergia):
    """Erro na migração de dados legacy"""
    pass


class ErroImportacaoArquivo(ErroMigracaoDados):
    """Erro na importação de arquivo"""
    pass


class ErroExportacaoArquivo(ErroSistemaEnergia):
    """Erro na exportação de arquivo"""
    pass


class ErroConfiguracaoSistema(ErroSistemaEnergia):
    """Erro na configuração do sistema"""
    pass


class ErroUnidadeConsumidora(ErroSistemaEnergia):
    """Erro relacionado a unidade consumidora"""
    pass


class ErroGeracao(ErroSistemaEnergia):
    """Erro na geração de energia"""
    pass


class ErroConsumo(ErroSistemaEnergia):
    """Erro no consumo de energia"""
    pass


class ErroCreditos(ErroSistemaEnergia):
    """Erro no gerenciamento de créditos"""
    pass


class ErroTarifa(ErroSistemaEnergia):
    """Erro relacionado a tarifas"""
    pass


class ErroBandeiraTarifaria(ErroTarifa):
    """Erro específico de bandeira tarifária"""
    pass


class ErroRelatorio(ErroSistemaEnergia):
    """Erro na geração de relatórios"""
    pass


class ErroGrafico(ErroSistemaEnergia):
    """Erro na geração de gráficos"""
    pass


class ErroInterface(ErroSistemaEnergia):
    """Erro na interface do usuário"""
    pass


class ErroConexao(ErroSistemaEnergia):
    """Erro de conexão (para futuras integrações)"""
    pass


# Exceções específicas do sistema legacy

class ErroCompatibilidadeLegacy(ErroSistemaEnergia):
    """Erro de compatibilidade com sistema legacy"""
    pass


class ErroConversaoFormato(ErroMigracaoDados):
    """Erro na conversão de formato de dados"""
    pass


class ErroValidacaoLegacy(ErroValidacao):
    """Erro na validação de dados legacy"""
    pass


class ErroArquivoLegacy(ErroImportacaoArquivo):
    """Erro específico de arquivo legacy"""
    pass


# Exceções adicionais para repositório e dados

class ErroArquivoNaoEncontrado(ErroCarregamentoDados):
    """Erro quando arquivo não é encontrado"""
    pass


class ErroPermissaoArquivo(ErroSalvamentoDados):
    """Erro de permissão de arquivo"""
    pass


class ErroFormatoArquivo(ErroCarregamentoDados):
    """Erro de formato de arquivo"""
    pass


class ErroEspacoDisco(ErroSalvamentoDados):
    """Erro de espaço em disco"""
    pass


class ErroCorrupcaoDados(ErroCarregamentoDados):
    """Erro de corrupção de dados"""
    pass


# Funções auxiliares para tratamento de erros

def capturar_erro_sistema(func):
    """Decorator para capturar erros do sistema"""

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ErroSistemaEnergia:
            raise  # Re-raise erros conhecidos do sistema
        except Exception as e:
            # Converter erros desconhecidos em ErroSistemaEnergia
            raise ErroSistemaEnergia(f"Erro inesperado em {func.__name__}: {e}")

    return wrapper


def validar_parametro(valor, nome_parametro, tipo_esperado=None, valor_minimo=None, valor_maximo=None):
    """Valida parâmetro e levanta exceção se inválido"""

    if valor is None:
        raise ErroValidacao(f"Parâmetro '{nome_parametro}' não pode ser None")

    if tipo_esperado and not isinstance(valor, tipo_esperado):
        raise ErroValidacao(
            f"Parâmetro '{nome_parametro}' deve ser do tipo {tipo_esperado.__name__}, "
            f"recebido {type(valor).__name__}"
        )

    if valor_minimo is not None and valor < valor_minimo:
        raise ErroValidacao(
            f"Parâmetro '{nome_parametro}' deve ser >= {valor_minimo}, recebido {valor}"
        )

    if valor_maximo is not None and valor > valor_maximo:
        raise ErroValidacao(
            f"Parâmetro '{nome_parametro}' deve ser <= {valor_maximo}, recebido {valor}"
        )


def validar_mes(mes):
    """Valida se o mês está no intervalo correto"""
    validar_parametro(mes, "mes", int, 1, 12)


def validar_ano(ano):
    """Valida se o ano é válido"""
    ano_atual = 2024  # Pode ser obtido dinamicamente
    validar_parametro(ano, "ano", int, 2000, ano_atual + 50)


def validar_potencia(potencia):
    """Valida potência do sistema"""
    validar_parametro(potencia, "potencia", (int, float), 0.1, 10000.0)


def validar_eficiencia(eficiencia):
    """Valida eficiência do sistema"""
    validar_parametro(eficiencia, "eficiencia", (int, float), 0.1, 1.0)


def validar_tarifa(tarifa):
    """Valida tarifa de energia"""
    validar_parametro(tarifa, "tarifa", (int, float), 0.01, 10.0)


def validar_consumo(consumo):
    """Valida consumo de energia"""
    validar_parametro(consumo, "consumo", (int, float), 0.0, 100000.0)


# Context manager para tratamento de erros
class TratadorErroSistema:
    """Context manager para tratamento centralizado de erros"""

    def __init__(self, operacao="operação do sistema"):
        self.operacao = operacao
        self.erro_capturado = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            return False  # Nenhum erro

        self.erro_capturado = exc_val

        # Log do erro (pode ser expandido para logging real)
        print(f"Erro durante {self.operacao}: {exc_val}")

        # Converter erros não tratados em ErroSistemaEnergia
        if not isinstance(exc_val, ErroSistemaEnergia):
            raise ErroSistemaEnergia(f"Erro durante {self.operacao}: {exc_val}")

        return False  # Propagar o erro


# Mapeamento de erros comuns para facilitar tratamento
MAPEAMENTO_ERROS = {
    FileNotFoundError: ErroArquivoNaoEncontrado,
    PermissionError: ErroPermissaoArquivo,
    OSError: ErroSalvamentoDados,
    ValueError: ErroValidacao,
    TypeError: ErroValidacao,
    KeyError: ErroCarregamentoDados,
    json.JSONDecodeError: ErroFormatoArquivo
}


def mapear_erro_sistema(erro_original):
    """Mapeia erro padrão do Python para erro do sistema"""
    tipo_erro = type(erro_original)

    if tipo_erro in MAPEAMENTO_ERROS:
        erro_mapeado = MAPEAMENTO_ERROS[tipo_erro]
        return erro_mapeado(str(erro_original))

    return ErroSistemaEnergia(f"Erro não mapeado: {erro_original}")

# Exemplo de uso do context manager:
# with TratadorErroSistema("cálculo de energia"):
#     resultado = calcular_energia()