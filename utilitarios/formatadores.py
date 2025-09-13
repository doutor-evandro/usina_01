"""
Formatadores de dados para exibição
"""

from typing import Union, Optional
from datetime import datetime, date
import locale

# Tentar configurar locale brasileiro
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')
    except:
        pass  # Usar configuração padrão


def formatar_moeda(valor: Union[float, int], simbolo: str = "R$") -> str:
    """
    Formata valor monetário

    Args:
        valor: Valor a ser formatado
        simbolo: Símbolo da moeda

    Returns:
        String formatada com valor monetário
    """
    try:
        if valor is None:
            return f"{simbolo} 0,00"

        # Formatação brasileira
        valor_formatado = f"{abs(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

        if valor < 0:
            return f"-{simbolo} {valor_formatado}"
        else:
            return f"{simbolo} {valor_formatado}"

    except (ValueError, TypeError):
        return f"{simbolo} 0,00"


def formatar_energia(valor: Union[float, int], unidade: str = "kWh") -> str:
    """
    Formata valor de energia

    Args:
        valor: Valor a ser formatado
        unidade: Unidade de medida

    Returns:
        String formatada com valor de energia
    """
    try:
        if valor is None:
            return f"0,0 {unidade}"

        # Formatação com separador decimal brasileiro
        if abs(valor) >= 1000:
            valor_formatado = f"{valor:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")
        else:
            valor_formatado = f"{valor:.1f}".replace(".", ",")

        return f"{valor_formatado} {unidade}"

    except (ValueError, TypeError):
        return f"0,0 {unidade}"


def formatar_percentual(valor: Union[float, int], casas_decimais: int = 1) -> str:
    """
    Formata valor percentual

    Args:
        valor: Valor a ser formatado (em decimal, ex: 0.15 para 15%)
        casas_decimais: Número de casas decimais

    Returns:
        String formatada com percentual
    """
    try:
        if valor is None:
            return "0,0%"

        # Converter para percentual se necessário
        if abs(valor) <= 1:
            percentual = valor * 100
        else:
            percentual = valor

        formato = f"{{:.{casas_decimais}f}}"
        valor_formatado = formato.format(percentual).replace(".", ",")

        return f"{valor_formatado}%"

    except (ValueError, TypeError):
        return "0,0%"


def formatar_potencia(valor: Union[float, int], unidade: str = "kW") -> str:
    """
    Formata valor de potência

    Args:
        valor: Valor a ser formatado
        unidade: Unidade de medida

    Returns:
        String formatada com valor de potência
    """
    try:
        if valor is None:
            return f"0,0 {unidade}"

        # Formatação com separador decimal brasileiro
        if abs(valor) >= 1000:
            valor_formatado = f"{valor:,.1f}".replace(",", "X").replace(".", ",").replace("X", ".")
        else:
            valor_formatado = f"{valor:.1f}".replace(".", ",")

        return f"{valor_formatado} {unidade}"

    except (ValueError, TypeError):
        return f"0,0 {unidade}"


def formatar_numero(valor: Union[float, int], casas_decimais: int = 2) -> str:
    """
    Formata número com separadores brasileiros

    Args:
        valor: Valor a ser formatado
        casas_decimais: Número de casas decimais

    Returns:
        String formatada com número
    """
    try:
        if valor is None:
            return "0"

        formato = f"{{:,.{casas_decimais}f}}"
        valor_formatado = formato.format(valor).replace(",", "X").replace(".", ",").replace("X", ".")

        return valor_formatado

    except (ValueError, TypeError):
        return "0"


def formatar_data(data: Union[datetime, date, str], formato: str = "%d/%m/%Y") -> str:
    """
    Formata data

    Args:
        data: Data a ser formatada
        formato: Formato de saída

    Returns:
        String formatada com data
    """
    try:
        if isinstance(data, str):
            return data
        elif isinstance(data, (datetime, date)):
            return data.strftime(formato)
        else:
            return datetime.now().strftime(formato)

    except (ValueError, TypeError):
        return datetime.now().strftime(formato)


def formatar_tempo(segundos: Union[float, int]) -> str:
    """
    Formata tempo em formato legível

    Args:
        segundos: Tempo em segundos

    Returns:
        String formatada com tempo
    """
    try:
        if segundos is None or segundos < 0:
            return "0s"

        horas = int(segundos // 3600)
        minutos = int((segundos % 3600) // 60)
        segs = int(segundos % 60)

        if horas > 0:
            return f"{horas}h {minutos}m {segs}s"
        elif minutos > 0:
            return f"{minutos}m {segs}s"
        else:
            return f"{segs}s"

    except (ValueError, TypeError):
        return "0s"


# Funções de conveniência para valores específicos do sistema de energia
def formatar_kwh(valor: Union[float, int]) -> str:
    """Formata valor em kWh"""
    return formatar_energia(valor, "kWh")


def formatar_kw(valor: Union[float, int]) -> str:
    """Formata valor em kW"""
    return formatar_potencia(valor, "kW")


def formatar_reais(valor: Union[float, int]) -> str:
    """Formata valor em reais"""
    return formatar_moeda(valor, "R$")


def formatar_eficiencia(valor: Union[float, int]) -> str:
    """Formata eficiência em percentual"""
    return formatar_percentual(valor, 1)


def formatar_anos(valor: Union[float, int]) -> str:
    """Formata valor em anos"""
    try:
        if valor is None:
            return "0 anos"

        if valor == 1:
            return "1 ano"
        else:
            return f"{valor:.1f} anos".replace(".", ",")

    except (ValueError, TypeError):
        return "0 anos"


# Classe para compatibilidade com código legacy
class FormatadorBrasileiro:
    """Classe de formatação para compatibilidade legacy"""

    @staticmethod
    def formatar_moeda(valor):
        return formatar_moeda(valor)

    @staticmethod
    def formatar_energia(valor):
        return formatar_energia(valor)

    @staticmethod
    def formatar_percentual(valor):
        return formatar_percentual(valor)

    @staticmethod
    def formatar_numero(valor):
        return formatar_numero(valor)