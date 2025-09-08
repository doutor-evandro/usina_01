# usina_01/utilitarios/constantes.py

from enum import Enum

# --- Meses ---
class Mes(Enum):
    JANEIRO = "Janeiro"
    FEVEREIRO = "Fevereiro"
    MARCO = "Março"
    ABRIL = "Abril"
    MAIO = "Maio"
    JUNHO = "Junho"
    JULHO = "Julho"
    AGOSTO = "Agosto"
    SETEMBRO = "Setembro"
    OUTUBRO = "Outubro"
    NOVEMBRO = "Novembro"
    DEZEMBRO = "Dezembro"

MESES_APENAS = [mes.value for mes in Mes]
MESES_COM_ANUAL = ["Resultado Anual"] + MESES_APENAS

# --- Tipos de Ligação ---
TIPOS_LIGACAO = {
    "mono": {"nome": "Monofásica", "tarifa": 30},
    "bi": {"nome": "Bifásica", "tarifa": 50},
    "tri": {"nome": "Trifásica", "tarifa": 100}
}

# --- Cores para Gráficos (Exemplos) ---
CORES_GRAFICO = [
    "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4",
    "#FFEAA7", "#DDA0DD", "#98D8C8", "#F7DC6F",
    "#BB8FCE", "#85C1E9", "#F8C471", "#82E0AA"
]

COR_SOBRA = "#28A745"    # Verde para sobra
COR_DEFICIT = "#DC3545"  # Vermelho para déficit

# --- Bloco de Teste ---
if __name__ == "__main__":
    print("--- Teste: utilitarios/constantes.py ---")
    print(f"MESES_APENAS: {MESES_APENAS}")
    print(f"MESES_COM_ANUAL: {MESES_COM_ANUAL}")
    print(f"Tipo de Ligação Monofásica: {TIPOS_LIGACAO['mono']}")
    print(f"Tarifa da Ligação Trifásica: {TIPOS_LIGACAO['tri']['tarifa']}")
    print(f"Cor para Sobra: {COR_SOBRA}")