# usina_01/utilitarios/formatadores.py

import locale


class FormatadorBrasileiro:
    def __init__(self):
        # Tenta configurar o locale, mas a formatação de números será feita
        # manualmente para maior robustez, ignorando o resultado do locale.
        self._configurar_locale()

    def _configurar_locale(self):
        """
        Tenta configurar o locale para português do Brasil.
        Este método é mantido para compatibilidade ou futuras necessidades
        de outras funções dependentes de locale, mas não afeta diretamente
        a formatação de números float/int neste módulo.
        """
        try:
            locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
        except locale.Error:
            try:
                locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')
            except locale.Error:
                # Se nenhum locale for encontrado, não há problema,
                # pois a formatação de números será manual.
                pass

    def formatar_numero(self, numero: float) -> str:
        """
        Formata um número float no padrão brasileiro (ex: 1.234.567,89).
        Sempre usa a formatação manual para maior consistência e robustez.
        """
        return self._formatacao_manual_float(numero)

    def _formatacao_manual_float(self, numero: float) -> str:
        """
        Formatação manual de float para o padrão brasileiro.
        Ex: 1234567.89 -> "1.234.567,89"
        """
        # Formata o número para uma string com 2 casas decimais, usando ponto como separador decimal.
        s = f"{numero:.2f}"

        # Lida com números negativos
        sign = ""
        if s.startswith('-'):
            sign = "-"
            s = s[1:]

        parts = s.split('.')
        integer_part = parts[0]
        decimal_part = parts[1]

        formatted_integer = ""
        # Itera a parte inteira de trás para frente para adicionar os separadores de milhar
        for i, digit in enumerate(reversed(integer_part)):
            if i > 0 and i % 3 == 0:
                formatted_integer = "." + formatted_integer
            formatted_integer = digit + formatted_integer

        return f"{sign}{formatted_integer},{decimal_part}"

    def formatar_inteiro(self, numero: int) -> str:
        """
        Formata um número inteiro no padrão brasileiro (ex: 1.234.567).
        Sempre usa a formatação manual para maior consistência e robustez.
        """
        return self._formatacao_manual_int(numero)

    def _formatacao_manual_int(self, numero: int) -> str:
        """
        Formatação manual de int para o padrão brasileiro.
        Ex: 9876543 -> "9.876.543"
        """
        s = str(int(numero))

        # Lida com números negativos
        sign = ""
        if s.startswith('-'):
            sign = "-"
            s = s[1:]

        formatted_integer = ""
        # Itera o número de trás para frente para adicionar os separadores de milhar
        for i, digit in enumerate(reversed(s)):
            if i > 0 and i % 3 == 0:
                formatted_integer = "." + formatted_integer
            formatted_integer = digit + formatted_integer

        return f"{sign}{formatted_integer}"

    def formatar_porcentagem(self, valor: float) -> str:
        """
        Formata um valor float como porcentagem no padrão brasileiro (ex: 15,86%).
        """
        # A f-string formatará com ponto decimal, que é então substituído por vírgula.
        return f"{valor:.2f}%".replace('.', ',')


# --- Bloco de Teste ---
if __name__ == "__main__":
    print("--- Teste: utilitarios/formatadores.py ---")
    formatter = FormatadorBrasileiro()

    print(f"Número 1234567.89: {formatter.formatar_numero(1234567.89)}")
    print(f"Número 123.45: {formatter.formatar_numero(123.45)}")
    print(f"Número 0.5: {formatter.formatar_numero(0.5)}")
    print(f"Número -9876.54: {formatter.formatar_numero(-9876.54)}")
    print(f"Número 1000: {formatter.formatar_numero(1000.0)}")  # Teste com float que parece inteiro
    print(f"Número -1000: {formatter.formatar_numero(-1000.0)}")  # Teste com float negativo que parece inteiro

    print(f"Inteiro 9876543: {formatter.formatar_inteiro(9876543)}")
    print(f"Inteiro 123: {formatter.formatar_inteiro(123)}")
    print(f"Inteiro -456789: {formatter.formatar_inteiro(-456789)}")

    print(f"Porcentagem 15.789: {formatter.formatar_porcentagem(15.789)}")
    print(f"Porcentagem 0.5: {formatter.formatar_porcentagem(0.5)}")
    print(f"Porcentagem 100: {formatter.formatar_porcentagem(100)}")