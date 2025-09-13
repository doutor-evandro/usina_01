"""
Gerenciador de dados compatível com sistema legacy
Adaptação das funções originais para a nova estrutura
"""

import json
import os
from typing import Dict, List, Tuple, Any
from nucleo.modelos import SistemaEnergia, UnidadeConsumidora, ConfiguracaoSistema, TipoLigacao, TipoUnidade


class GerenciadorDadosLegacy:
    """Gerenciador de dados compatível com formato legacy"""

    def __init__(self, arquivo_dados: str = "dados_sistema.json"):
        self.arquivo_dados = arquivo_dados
        self.meses_completos = [
            "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
        ]

        # Mapeamento de tipos de ligação
        self.tipos_ligacao_map = {
            "mono": TipoLigacao.MONOFASICA,
            "bi": TipoLigacao.BIFASICA,
            "tri": TipoLigacao.TRIFASICA
        }

        # Tarifas mínimas por tipo
        self.tarifas_minimas = {
            "mono": 30,
            "bi": 50,
            "tri": 100
        }

    def carregar_dados(self) -> Dict:
        """Carrega dados do arquivo JSON ou cria dados de exemplo"""
        if os.path.exists(self.arquivo_dados):
            try:
                with open(self.arquivo_dados, 'r', encoding='utf-8') as f:
                    dados = json.load(f)

                # Migração automática
                dados = self.migrar_meses_para_formato_completo(dados)

                # Verificar eficiência
                if "eficiencia_usina" not in dados.get("sistema", {}):
                    dados["sistema"]["eficiencia_usina"] = 1.0  # 100% para dados reais

                print("✅ Dados carregados do arquivo")
                return dados

            except Exception as e:
                print(f"❌ Erro ao carregar dados: {e}")
                return self.criar_dados_exemplo()
        else:
            return self.criar_dados_exemplo()

    def migrar_meses_para_formato_completo(self, dados: Dict) -> Dict:
        """Migra dados de meses abreviados para formato completo"""
        mapeamento_meses = {
            "Jan": "Janeiro", "Fev": "Fevereiro", "Mar": "Março", "Abr": "Abril",
            "Mai": "Maio", "Jun": "Junho", "Jul": "Julho", "Ago": "Agosto",
            "Set": "Setembro", "Out": "Outubro", "Nov": "Novembro", "Dez": "Dezembro"
        }

        if "consumos" in dados:
            for codigo_unidade in dados["consumos"]:
                consumos_originais = dados["consumos"][codigo_unidade].copy()
                dados["consumos"][codigo_unidade] = {}

                for mes_original, consumo in consumos_originais.items():
                    if mes_original in mapeamento_meses:
                        # Converter mês abreviado para completo
                        mes_completo = mapeamento_meses[mes_original]
                        dados["consumos"][codigo_unidade][mes_completo] = consumo
                    elif mes_original in self.meses_completos:
                        # Já está no formato correto
                        dados["consumos"][codigo_unidade][mes_original] = consumo

        print("🔄 Migração de meses concluída")
        return dados

    def salvar_dados(self, dados: Dict) -> bool:
        """Salva dados no arquivo JSON"""
        try:
            with open(self.arquivo_dados, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
            print("✅ Dados salvos com sucesso")
            return True
        except Exception as e:
            print(f"❌ Erro ao salvar dados: {e}")
            return False

    def criar_dados_exemplo(self) -> Dict:
        """Cria dados de exemplo usando dados reais"""
        print("📝 Criando dados com informações reais...")

        # Importar dados reais se disponível
        try:
            from configuracao.dados_reais import (
                CONFIGURACAO_USINA_REAL, GERACAO_MENSAL_REAL, UNIDADES_REAIS
            )

            # Estrutura compatível com sistema legacy
            dados = {
                "sistema": {
                    "potencia_inversor": CONFIGURACAO_USINA_REAL["potencia_inversor_kw"],
                    "potencia_modulos": CONFIGURACAO_USINA_REAL["potencia_instalada_kw"],
                    "eficiencia_usina": CONFIGURACAO_USINA_REAL["eficiencia_sistema"],
                    "geracao_mensal": {
                        mes: geracao for mes, geracao in zip(self.meses_completos, GERACAO_MENSAL_REAL)
                    }
                },
                "unidades": [],
                "consumos": {}
            }

            # Converter unidades reais para formato legacy
            for unidade_real in UNIDADES_REAIS:
                # Mapear tipo de ligação
                tipo_legacy = "mono"
                if unidade_real["tipo_ligacao"].value == "BIFASICA":
                    tipo_legacy = "bi"
                elif unidade_real["tipo_ligacao"].value == "TRIFASICA":
                    tipo_legacy = "tri"

                # Adicionar unidade
                dados["unidades"].append({
                    "codigo": unidade_real["codigo"],
                    "nome": unidade_real["nome"],
                    "tipo": tipo_legacy,
                    "endereco": unidade_real["endereco"]
                })

                # Adicionar consumos
                dados["consumos"][unidade_real["codigo"]] = {
                    mes: consumo for mes, consumo in zip(self.meses_completos, unidade_real["consumo_mensal"])
                }

            return dados

        except ImportError:
            # Fallback para dados básicos
            return {
                "sistema": {
                    "potencia_inversor": 75.0,
                    "potencia_modulos": 92.0,
                    "eficiencia_usina": 1.0,
                    "geracao_mensal": {mes: 10000 for mes in self.meses_completos}
                },
                "unidades": [],
                "consumos": {}
            }

    def obter_tarifa_minima(self, tipo_ligacao: str) -> float:
        """Obtém a tarifa mínima baseada no tipo de ligação"""
        return self.tarifas_minimas.get(tipo_ligacao, 30)

    def adicionar_unidade(self, dados: Dict, codigo: str, nome: str, tipo: str, endereco: str = "") -> Tuple[bool, str]:
        """Adiciona uma nova unidade aos dados"""
        nova_unidade = {
            "codigo": codigo,
            "nome": nome,
            "tipo": tipo,
            "endereco": endereco
        }

        # Verificar se código já existe
        for unidade in dados["unidades"]:
            if unidade["codigo"] == codigo:
                return False, "Código já existe"

        dados["unidades"].append(nova_unidade)

        # Inicializar consumos se não existir
        if codigo not in dados["consumos"]:
            dados["consumos"][codigo] = {mes: 0 for mes in self.meses_completos}

        return True, "Unidade adicionada com sucesso"

    def remover_unidade(self, dados: Dict, codigo: str) -> Tuple[bool, str]:
        """Remove uma unidade dos dados"""
        # Remover da lista de unidades
        dados["unidades"] = [u for u in dados["unidades"] if u["codigo"] != codigo]

        # Remover consumos
        if codigo in dados["consumos"]:
            del dados["consumos"][codigo]

        return True, "Unidade removida com sucesso"

    def adicionar_consumo(self, dados: Dict, codigo: str, mes: str, consumo: float) -> Tuple[bool, str]:
        """Adiciona consumo para uma unidade em um mês"""
        if codigo not in dados["consumos"]:
            dados["consumos"][codigo] = {m: 0 for m in self.meses_completos}

        dados["consumos"][codigo][mes] = float(consumo)
        return True, f"Consumo adicionado: {codigo} - {mes}: {consumo} kWh"

    def obter_consumo(self, dados: Dict, codigo: str, mes: str) -> float:
        """Obtém o consumo de uma unidade em um mês"""
        return dados["consumos"].get(codigo, {}).get(mes, 0.0)

    def calcular_media_anual(self, dados: Dict, codigo: str) -> float:
        """Calcula a média anual de consumo de uma unidade"""
        consumos = dados["consumos"].get(codigo, {})
        if not consumos:
            return 0.0

        # Filtrar apenas meses válidos
        consumos_validos = {k: v for k, v in consumos.items() if k in self.meses_completos}
        if not consumos_validos:
            return 0.0

        return sum(consumos_validos.values()) / len(consumos_validos)

    def obter_eficiencia_usina(self, dados: Dict) -> float:
        """Obtém a eficiência da usina dos dados"""
        return dados.get("sistema", {}).get("eficiencia_usina", 1.0)

    def atualizar_eficiencia_usina(self, dados: Dict, nova_eficiencia: float) -> bool:
        """Atualiza a eficiência da usina"""
        if "sistema" not in dados:
            dados["sistema"] = {}
        dados["sistema"]["eficiencia_usina"] = nova_eficiencia
        return True

    def converter_para_sistema_energia(self, dados: Dict) -> SistemaEnergia:
        """Converte dados legacy para SistemaEnergia"""
        try:
            # Configuração do sistema
            sistema_dados = dados.get("sistema", {})

            configuracao = ConfiguracaoSistema(
                potencia_instalada_kw=sistema_dados.get("potencia_modulos", 92.0),
                eficiencia_sistema=sistema_dados.get("eficiencia_usina", 1.0),
                tarifa_energia_kwh=0.65,  # Valor padrão
                custo_investimento=450000.0,  # Valor padrão
                # Geração mensal
                geracao_mensal_kwh=list(sistema_dados.get("geracao_mensal", {}).values()) if isinstance(
                    sistema_dados.get("geracao_mensal"), dict) else [10000] * 12,
                # Outros parâmetros padrão
                fator_capacidade=0.15,
                tarifa_tusd_kwh=0.25,
                tarifa_te_kwh=0.35,
                taxa_disponibilidade_mono=30.0,
                taxa_disponibilidade_bi=50.0,
                taxa_disponibilidade_tri=100.0,
                perdas_sistema=0.0,
                fator_simultaneidade=1.0,
                vida_util_sistema=25,
                validade_creditos_meses=60,
                percentual_injecao_rede=1.0
            )

            # Unidades consumidoras
            unidades = []
            for unidade_dados in dados.get("unidades", []):
                codigo = unidade_dados["codigo"]
                consumos = dados.get("consumos", {}).get(codigo, {})

                # Converter consumos para lista
                consumo_mensal = []
                for mes in self.meses_completos:
                    consumo_mensal.append(consumos.get(mes, 0))

                # Mapear tipo de ligação
                tipo_ligacao = self.tipos_ligacao_map.get(unidade_dados["tipo"], TipoLigacao.TRIFASICA)

                unidade = UnidadeConsumidora(
                    id=codigo,
                    nome=unidade_dados["nome"],
                    tipo_ligacao=tipo_ligacao,
                    tipo_unidade=TipoUnidade.COMERCIAL,
                    ativa=True,
                    endereco=unidade_dados.get("endereco", ""),
                    cidade="Londrina",
                    estado="PR",
                    cep="86000-000",
                    demanda_contratada_kw=0.0,
                    grupo_tarifario="B3",
                    consumo_mensal_kwh=consumo_mensal,
                    percentual_energia_alocada=0.0,
                    prioridade_distribuicao=1
                )

                # Adicionar código como atributo extra
                unidade.codigo = codigo
                unidades.append(unidade)

            # Criar sistema
            sistema = SistemaEnergia(
                configuracao=configuracao,
                unidades=unidades,
                versao_sistema="2.0-Legacy-Real"
            )

            return sistema

        except Exception as e:
            print(f"❌ Erro ao converter dados: {e}")
            raise

    def converter_de_sistema_energia(self, sistema: SistemaEnergia) -> Dict:
        """Converte SistemaEnergia para formato legacy"""
        try:
            dados = {
                "sistema": {
                    "potencia_inversor": 75.0,  # Valor fixo
                    "potencia_modulos": sistema.configuracao.potencia_instalada_kw,
                    "eficiencia_usina": sistema.configuracao.eficiencia_sistema,
                    "geracao_mensal": {}
                },
                "unidades": [],
                "consumos": {}
            }

            # Geração mensal
            if hasattr(sistema.configuracao, 'geracao_mensal_kwh') and sistema.configuracao.geracao_mensal_kwh:
                for i, mes in enumerate(self.meses_completos):
                    if i < len(sistema.configuracao.geracao_mensal_kwh):
                        dados["sistema"]["geracao_mensal"][mes] = sistema.configuracao.geracao_mensal_kwh[i]
                    else:
                        dados["sistema"]["geracao_mensal"][mes] = 10000
            else:
                dados["sistema"]["geracao_mensal"] = {mes: 10000 for mes in self.meses_completos}

            # Unidades
            for unidade in sistema.unidades:
                # Mapear tipo de ligação para legacy
                tipo_legacy = "tri"
                if unidade.tipo_ligacao == TipoLigacao.MONOFASICA:
                    tipo_legacy = "mono"
                elif unidade.tipo_ligacao == TipoLigacao.BIFASICA:
                    tipo_legacy = "bi"

                dados["unidades"].append({
                    "codigo": getattr(unidade, 'codigo', unidade.id),
                    "nome": unidade.nome,
                    "tipo": tipo_legacy,
                    "endereco": unidade.endereco
                })

                # Consumos
                codigo = getattr(unidade, 'codigo', unidade.id)
                dados["consumos"][codigo] = {}
                for i, mes in enumerate(self.meses_completos):
                    if i < len(unidade.consumo_mensal_kwh):
                        dados["consumos"][codigo][mes] = unidade.consumo_mensal_kwh[i]
                    else:
                        dados["consumos"][codigo][mes] = 0

            return dados

        except Exception as e:
            print(f"❌ Erro ao converter sistema: {e}")
            raise


# Funções de compatibilidade (para manter interface similar ao código original)
def carregar_dados():
    """Função de compatibilidade"""
    gerenciador = GerenciadorDadosLegacy()
    return gerenciador.carregar_dados()


def salvar_dados(dados):
    """Função de compatibilidade"""
    gerenciador = GerenciadorDadosLegacy()
    return gerenciador.salvar_dados(dados)


def obter_eficiencia_usina(dados):
    """Função de compatibilidade"""
    gerenciador = GerenciadorDadosLegacy()
    return gerenciador.obter_eficiencia_usina(dados)


def obter_tarifa_minima(tipo_ligacao):
    """Função de compatibilidade"""
    gerenciador = GerenciadorDadosLegacy()
    return gerenciador.obter_tarifa_minima(tipo_ligacao)