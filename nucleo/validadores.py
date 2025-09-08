# usina_01/nucleo/validadores.py

from typing import Dict, List
from nucleo.modelos import UnidadeConsumidora, ConfiguracaoSistema, SistemaEnergia, TipoLigacao
from nucleo.excecoes import ErroValidacao
from utilitarios.constantes import MESES_APENAS


class ValidadorUnidade:
    """
    Validador para unidades consumidoras.
    """

    def validar_unidade(self, unidade: UnidadeConsumidora) -> None:
        """
        Valida uma unidade consumidora.

        Args:
            unidade: Unidade a ser validada

        Raises:
            ErroValidacao: Se a unidade for inválida
        """
        if not unidade.codigo or not unidade.codigo.strip():
            raise ErroValidacao("Código da unidade é obrigatório")

        if not unidade.nome or not unidade.nome.strip():
            raise ErroValidacao("Nome da unidade é obrigatório")

        if unidade.tarifa_minima < 0:
            raise ErroValidacao("Tarifa mínima não pode ser negativa")

        if not isinstance(unidade.tipo_ligacao, TipoLigacao):
            raise ErroValidacao("Tipo de ligação inválido")

    def validar_codigo_unico(self, codigo: str, unidades: List[UnidadeConsumidora],
                             excluir_unidade: UnidadeConsumidora = None) -> None:
        """
        Valida se o código da unidade é único.

        Args:
            codigo: Código a ser validado
            unidades: Lista de unidades existentes
            excluir_unidade: Unidade a ser excluída da validação (para edição)

        Raises:
            ErroValidacao: Se o código não for único
        """
        for unidade in unidades:
            if unidade != excluir_unidade and unidade.codigo == codigo:
                raise ErroValidacao(f"Código '{codigo}' já existe")


class ValidadorConfiguracao:
    """
    Validador para configurações do sistema.
    """

    def validar_configuracao(self, config: ConfiguracaoSistema) -> None:
        """
        Valida uma configuração do sistema.

        Args:
            config: Configuração a ser validada

        Raises:
            ErroValidacao: Se a configuração for inválida
        """
        if config.potencia_inversor <= 0:
            raise ErroValidacao("Potência do inversor deve ser maior que zero")

        if config.potencia_modulos <= 0:
            raise ErroValidacao("Potência dos módulos deve ser maior que zero")

        if not (0 < config.eficiencia <= 100):
            raise ErroValidacao("Eficiência deve estar entre 0 e 100%")

        if config.valor_kwh <= 0:
            raise ErroValidacao("Valor da tarifa deve ser maior que zero")

        # Valida geração mensal
        for mes in MESES_APENAS:
            if mes not in config.geracao_mensal:
                raise ErroValidacao(f"Geração para o mês '{mes}' não foi definida")

            if config.geracao_mensal[mes] < 0:
                raise ErroValidacao(f"Geração para '{mes}' não pode ser negativa")


class ValidadorConsumo:
    """
    Validador para dados de consumo.
    """

    def validar_consumo_mensal(self, consumo: float, mes: str) -> None:
        """
        Valida um valor de consumo mensal.

        Args:
            consumo: Valor do consumo
            mes: Nome do mês

        Raises:
            ErroValidacao: Se o consumo for inválido
        """
        if consumo < 0:
            raise ErroValidacao(f"Consumo para '{mes}' não pode ser negativo")

        if mes not in MESES_APENAS:
            raise ErroValidacao(f"Mês '{mes}' é inválido")

    def validar_consumos_unidade(self, consumos: Dict[str, float], codigo_unidade: str) -> None:
        """
        Valida todos os consumos de uma unidade.

        Args:
            consumos: Dicionário com consumos mensais
            codigo_unidade: Código da unidade

        Raises:
            ErroValidacao: Se algum consumo for inválido
        """
        for mes, consumo in consumos.items():
            try:
                self.validar_consumo_mensal(consumo, mes)
            except ErroValidacao as e:
                raise ErroValidacao(f"Unidade '{codigo_unidade}': {e}")


class ValidadorSistema:
    """
    Validador para o sistema completo.
    """

    def __init__(self):
        self.validador_unidade = ValidadorUnidade()
        self.validador_configuracao = ValidadorConfiguracao()
        self.validador_consumo = ValidadorConsumo()

    def validar_sistema(self, sistema: SistemaEnergia) -> None:
        """
        Valida um sistema completo.

        Args:
            sistema: Sistema a ser validado

        Raises:
            ErroValidacao: Se o sistema for inválido
        """
        # Valida configuração
        self.validador_configuracao.validar_configuracao(sistema.configuracao)

        # Valida se há pelo menos uma unidade
        if not sistema.unidades:
            raise ErroValidacao("Sistema deve ter pelo menos uma unidade consumidora")

        # Valida cada unidade
        codigos_vistos = set()
        for unidade in sistema.unidades:
            self.validador_unidade.validar_unidade(unidade)

            # Verifica códigos únicos
            if unidade.codigo in codigos_vistos:
                raise ErroValidacao(f"Código '{unidade.codigo}' está duplicado")
            codigos_vistos.add(unidade.codigo)

        # Valida consumos
        for codigo_unidade, consumos in sistema.consumos.items():
            # Verifica se a unidade existe
            if not any(u.codigo == codigo_unidade for u in sistema.unidades):
                raise ErroValidacao(f"Consumos definidos para unidade inexistente: '{codigo_unidade}'")

            # Valida os consumos da unidade
            self.validador_consumo.validar_consumos_unidade(consumos, codigo_unidade)


# --- Bloco de Teste ---
if __name__ == "__main__":
    print("--- Teste: nucleo/validadores.py ---")

    # Importa dados de exemplo para teste
    from configuracao.definicoes import CONFIG_EXEMPLO, UNIDADES_EXEMPLO, CONSUMOS_EXEMPLO

    # Testa ValidadorUnidade
    print("\n--- Teste 1: ValidadorUnidade ---")
    validador_unidade = ValidadorUnidade()

    try:
        validador_unidade.validar_unidade(UNIDADES_EXEMPLO[0])
        print("✓ Unidade válida passou na validação")
    except ErroValidacao as e:
        print(f"❌ Erro inesperado: {e}")

    # Testa ValidadorConfiguracao
    print("\n--- Teste 2: ValidadorConfiguracao ---")
    validador_config = ValidadorConfiguracao()

    try:
        validador_config.validar_configuracao(CONFIG_EXEMPLO)
        print("✓ Configuração válida passou na validação")
    except ErroValidacao as e:
        print(f"❌ Erro inesperado: {e}")

    # Testa ValidadorConsumo
    print("\n--- Teste 3: ValidadorConsumo ---")
    validador_consumo = ValidadorConsumo()

    try:
        validador_consumo.validar_consumo_mensal(250.0, "Janeiro")
        print("✓ Consumo válido passou na validação")
    except ErroValidacao as e:
        print(f"❌ Erro inesperado: {e}")

    # Testa ValidadorSistema
    print("\n--- Teste 4: ValidadorSistema ---")
    validador_sistema = ValidadorSistema()

    sistema_teste = SistemaEnergia(
        configuracao=CONFIG_EXEMPLO,
        unidades=UNIDADES_EXEMPLO,
        consumos=CONSUMOS_EXEMPLO
    )

    try:
        validador_sistema.validar_sistema(sistema_teste)
        print("✓ Sistema válido passou na validação completa")
    except ErroValidacao as e:
        print(f"❌ Erro inesperado: {e}")

    # Testa validação com erro
    print("\n--- Teste 5: Validação com erro ---")
    try:
        validador_consumo.validar_consumo_mensal(-100.0, "Janeiro")
        print("❌ Deveria ter dado erro!")
    except ErroValidacao as e:
        print(f"✓ Erro esperado capturado: {e}")

    print("\nTeste de Validadores concluído com sucesso!")