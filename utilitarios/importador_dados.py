"""
Importador de dados externos para o sistema - INCREMENTAL
"""

import json
import os
from typing import Dict, List, Optional
from nucleo.modelos import SistemaEnergia, UnidadeConsumidora, ConfiguracaoSistema


def importar_dados_reais_para_sistema():
    """Importa dados reais e cria sistema compatível"""
    try:
        from configuracao.dados_reais import (
            CONFIGURACAO_USINA_REAL, GERACAO_MENSAL_REAL,
            UNIDADES_REAIS, usar_dados_reais
        )

        # Verificar se deve usar dados reais
        if not usar_dados_reais():
            return None

        # Criar configuração com dados reais
        configuracao = ConfiguracaoSistema(
            potencia_instalada_kw=CONFIGURACAO_USINA_REAL["potencia_instalada_kw"],
            eficiencia_sistema=CONFIGURACAO_USINA_REAL["eficiencia_sistema"],
            tarifa_energia_kwh=CONFIGURACAO_USINA_REAL["tarifa_energia_kwh"],
            custo_investimento=CONFIGURACAO_USINA_REAL["custo_investimento"],
            geracao_mensal_kwh=GERACAO_MENSAL_REAL,
            # Manter outros valores padrão
            fator_capacidade=0.15,
            tarifa_tusd_kwh=0.25,
            tarifa_te_kwh=0.35,
            taxa_disponibilidade_mono=30.0,
            taxa_disponibilidade_bi=50.0,
            taxa_disponibilidade_tri=100.0,
            perdas_sistema=0.0,  # 100% eficiência = 0% perdas
            fator_simultaneidade=1.0,
            vida_util_sistema=25,
            validade_creditos_meses=60,
            percentual_injecao_rede=1.0
        )

        # Criar unidades com dados reais
        unidades = []
        for dados_unidade in UNIDADES_REAIS:
            unidade = UnidadeConsumidora(
                id=dados_unidade["id"],
                nome=dados_unidade["nome"],
                tipo_ligacao=dados_unidade["tipo_ligacao"],
                tipo_unidade=dados_unidade["tipo_unidade"],
                ativa=dados_unidade["ativa"],
                endereco=dados_unidade["endereco"],
                cidade="Londrina",  # Ajuste conforme necessário
                estado="PR",  # Ajuste conforme necessário
                cep="86000-000",  # Ajuste conforme necessário
                demanda_contratada_kw=0.0,
                grupo_tarifario="B3",  # Ajuste conforme necessário
                consumo_mensal_kwh=dados_unidade["consumo_mensal"],
                percentual_energia_alocada=dados_unidade["percentual_energia_alocada"],
                prioridade_distribuicao=dados_unidade["prioridade_distribuicao"]
            )
            # Adicionar código como atributo extra
            unidade.codigo = dados_unidade["codigo"]
            unidades.append(unidade)

        # Criar sistema
        sistema = SistemaEnergia(
            configuracao=configuracao,
            unidades=unidades,
            versao_sistema=CONFIGURACAO_USINA_REAL["versao_sistema"]
        )

        return sistema

    except ImportError:
        # Se não conseguir importar dados reais, retorna None
        return None
    except Exception as e:
        print(f"Erro ao importar dados reais: {e}")
        return None


def exportar_dados_atuais(sistema: SistemaEnergia, caminho_arquivo: str = "backup_sistema.json"):
    """Exporta dados atuais do sistema para JSON"""
    try:
        dados = {
            "versao": sistema.versao_sistema,
            "sistema": {
                "potencia_instalada": sistema.configuracao.potencia_instalada_kw,
                "eficiencia": sistema.configuracao.eficiencia_sistema,
                "tarifa": sistema.configuracao.tarifa_energia_kwh,
                "investimento": sistema.configuracao.custo_investimento,
                "geracao_mensal": sistema.configuracao.geracao_mensal_kwh
            },
            "unidades": []
        }

        for unidade in sistema.unidades:
            dados["unidades"].append({
                "id": unidade.id,
                "nome": unidade.nome,
                "tipo_ligacao": unidade.tipo_ligacao.value,
                "tipo_unidade": unidade.tipo_unidade.value,
                "consumo_mensal": unidade.consumo_mensal_kwh,
                "ativa": unidade.ativa,
                "codigo": getattr(unidade, 'codigo', ''),
                "endereco": unidade.endereco,
                "percentual_energia": unidade.percentual_energia_alocada
            })

        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)

        print(f"✅ Dados exportados para: {caminho_arquivo}")
        return True

    except Exception as e:
        print(f"❌ Erro ao exportar dados: {e}")
        return False


def verificar_dados_reais_disponiveis():
    """Verifica se os dados reais estão disponíveis"""
    try:
        from configuracao.dados_reais import usar_dados_reais
        return usar_dados_reais()
    except ImportError:
        return False