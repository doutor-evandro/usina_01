# usina_01/nucleo/modelos.py

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum


# --- Enum para Tipo de Ligação ---
class TipoLigacao(Enum):
    MONO = "mono"
    BI = "bi"
    TRI = "tri"


# --- Modelo: Unidade Consumidora ---
@dataclass
class UnidadeConsumidora:
    codigo: str
    nome: str
    tipo_ligacao: TipoLigacao
    endereco: str = ""

    @property
    def tarifa_minima(self) -> float:
        """Retorna a tarifa mínima em kWh para o tipo de ligação."""
        tarifas = {
            TipoLigacao.MONO: 30,
            TipoLigacao.BI: 50,
            TipoLigacao.TRI: 100
        }
        return tarifas.get(self.tipo_ligacao, 0)  # Retorna 0 se tipo não for encontrado


# --- Modelo: Configuração do Sistema (Usina) ---
@dataclass
class ConfiguracaoSistema:
    potencia_inversor: float = 0.0
    potencia_modulos: float = 0.0
    geracao_mensal: Dict[str, float] = field(default_factory=dict)  # Geração esperada por mês
    eficiencia: float = 100.0  # Eficiência da usina em porcentagem (ex: 78.0)
    valor_kwh: float = 0.6305  # Valor de referência do kWh para cálculos monetários (R\$)

    @property
    def potencia_resultante(self) -> float:
        """Retorna a potência resultante da usina (menor entre inversor e módulos)."""
        return min(self.potencia_inversor, self.potencia_modulos)


# --- Modelo: Sistema de Energia (Agregador de Dados) ---
@dataclass
class SistemaEnergia:
    configuracao: ConfiguracaoSistema = field(default_factory=ConfiguracaoSistema)
    unidades: List[UnidadeConsumidora] = field(default_factory=list)
    consumos: Dict[str, Dict[str, float]] = field(default_factory=dict)  # {codigo_unidade: {mes: consumo_kwh}}


# --- Bloco de Teste ---
if __name__ == "__main__":
    print("--- Teste: nucleo/modelos.py ---")

    # Teste UnidadeConsumidora
    unidade1 = UnidadeConsumidora(codigo="UC001", nome="Casa do João", tipo_ligacao=TipoLigacao.MONO,
                                  endereco="Rua A, 123")
    unidade2 = UnidadeConsumidora(codigo="UC002", nome="Comércio da Maria", tipo_ligacao=TipoLigacao.TRI)
    print(
        f"Unidade 1: {unidade1.nome}, Tipo: {unidade1.tipo_ligacao.value}, Tarifa Mínima: {unidade1.tarifa_minima} kWh")
    print(
        f"Unidade 2: {unidade2.nome}, Tipo: {unidade2.tipo_ligacao.value}, Tarifa Mínima: {unidade2.tarifa_minima} kWh")

    # Teste ConfiguracaoSistema
    config = ConfiguracaoSistema(
        potencia_inversor=10000,
        potencia_modulos=12000,
        geracao_mensal={"Janeiro": 1200, "Fevereiro": 1100},
        eficiencia=78.5,
        valor_kwh=0.72
    )
    print(
        f"Configuração: Potência Resultante: {config.potencia_resultante} W, Eficiência: {config.eficiencia}%, Valor kWh: R\${config.valor_kwh}")

    # Teste SistemaEnergia
    sistema = SistemaEnergia(configuracao=config)
    sistema.unidades.append(unidade1)
    sistema.unidades.append(unidade2)
    sistema.consumos = {
        "UC001": {"Janeiro": 300, "Fevereiro": 320},
        "UC002": {"Janeiro": 700, "Fevereiro": 680}
    }
    print(f"Sistema: Total de Unidades: {len(sistema.unidades)}")
    print(f"Consumo UC001 em Janeiro: {sistema.consumos['UC001']['Janeiro']} kWh")