"""
Migrador de dados - Versão adaptada para importar dados do sistema legacy
"""

import json
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import os
from pathlib import Path

from nucleo.modelos import (
    SistemaEnergia, ConfiguracaoSistema, UnidadeConsumidora,
    TipoLigacao, TipoUnidade, BandeiraTarifaria,
    converter_dados_legacy
)
from nucleo.excecoes import ErroMigracaoDados
from dados.repositorio import RepositorioDados


class MigradorDados:
    """Migrador principal para dados do sistema"""

    def __init__(self):
        self.repositorio = RepositorioDados()
        self.log_migracoes = []

    def migrar_excel_legacy(self, caminho_arquivo: str) -> SistemaEnergia:
        """
        Migra dados de arquivo Excel do sistema legacy
        """
        try:
            self._log("Iniciando migração de arquivo Excel legacy")

            if not os.path.exists(caminho_arquivo):
                raise ErroMigracaoDados(f"Arquivo não encontrado: {caminho_arquivo}")

            # Ler arquivo Excel
            dados_excel = self._ler_excel_legacy(caminho_arquivo)

            # Converter para formato novo
            sistema = self._converter_excel_para_sistema(dados_excel)

            # Validar dados migrados
            erros = sistema.validar_integridade()
            if erros:
                self._log(f"Avisos na validação: {erros}")

            self._log("Migração de Excel concluída com sucesso")
            return sistema

        except Exception as e:
            raise ErroMigracaoDados(f"Erro na migração de Excel: {e}")

    def migrar_json_legacy(self, caminho_arquivo: str) -> SistemaEnergia:
        """
        Migra dados de arquivo JSON do sistema legacy
        """
        try:
            self._log("Iniciando migração de arquivo JSON legacy")

            if not os.path.exists(caminho_arquivo):
                raise ErroMigracaoDados(f"Arquivo não encontrado: {caminho_arquivo}")

            # Ler arquivo JSON
            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                dados_json = json.load(f)

            # Converter usando função do modelo
            sistema = converter_dados_legacy(dados_json)

            # Validar dados migrados
            erros = sistema.validar_integridade()
            if erros:
                self._log(f"Avisos na validação: {erros}")

            self._log("Migração de JSON concluída com sucesso")
            return sistema

        except Exception as e:
            raise ErroMigracaoDados(f"Erro na migração de JSON: {e}")

    def migrar_csv_consumos(self, caminho_arquivo: str, sistema: SistemaEnergia) -> SistemaEnergia:
        """
        Migra dados de consumo de arquivo CSV
        """
        try:
            self._log("Iniciando migração de consumos CSV")

            if not os.path.exists(caminho_arquivo):
                raise ErroMigracaoDados(f"Arquivo não encontrado: {caminho_arquivo}")

            # Ler CSV
            df = pd.read_csv(caminho_arquivo, encoding='utf-8')

            # Processar dados de consumo
            self._processar_consumos_csv(df, sistema)

            self._log("Migração de consumos CSV concluída")
            return sistema

        except Exception as e:
            raise ErroMigracaoDados(f"Erro na migração de CSV: {e}")

    def exportar_para_novo_formato(self, sistema: SistemaEnergia, caminho_destino: str = None) -> str:
        """
        Exporta sistema migrado para o novo formato JSON
        """
        try:
            if caminho_destino is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                caminho_destino = f"sistema_migrado_{timestamp}.json"

            # Salvar usando repositório
            self.repositorio.salvar_sistema(sistema, caminho_destino)

            self._log(f"Sistema exportado para: {caminho_destino}")
            return caminho_destino

        except Exception as e:
            raise ErroMigracaoDados(f"Erro ao exportar sistema: {e}")

    def criar_backup_sistema_atual(self, caminho_backup: str = None) -> str:
        """
        Cria backup do sistema atual antes da migração
        """
        try:
            if caminho_backup is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                caminho_backup = f"backup_sistema_{timestamp}.json"

            # Tentar carregar sistema atual
            try:
                sistema_atual = self.repositorio.carregar_sistema()
                self.repositorio.salvar_sistema(sistema_atual, caminho_backup)
                self._log(f"Backup criado: {caminho_backup}")
                return caminho_backup
            except:
                self._log("Nenhum sistema atual encontrado para backup")
                return ""

        except Exception as e:
            raise ErroMigracaoDados(f"Erro ao criar backup: {e}")

    def validar_arquivo_legacy(self, caminho_arquivo: str) -> Dict[str, Any]:
        """
        Valida arquivo legacy antes da migração
        """
        try:
            extensao = Path(caminho_arquivo).suffix.lower()
            resultado_validacao = {
                'valido': False,
                'tipo_arquivo': extensao,
                'erros': [],
                'avisos': [],
                'estatisticas': {}
            }

            if not os.path.exists(caminho_arquivo):
                resultado_validacao['erros'].append("Arquivo não encontrado")
                return resultado_validacao

            if extensao == '.xlsx' or extensao == '.xls':
                resultado_validacao.update(self._validar_excel_legacy(caminho_arquivo))
            elif extensao == '.json':
                resultado_validacao.update(self._validar_json_legacy(caminho_arquivo))
            elif extensao == '.csv':
                resultado_validacao.update(self._validar_csv_legacy(caminho_arquivo))
            else:
                resultado_validacao['erros'].append(f"Tipo de arquivo não suportado: {extensao}")

            resultado_validacao['valido'] = len(resultado_validacao['erros']) == 0
            return resultado_validacao

        except Exception as e:
            return {
                'valido': False,
                'tipo_arquivo': 'desconhecido',
                'erros': [f"Erro na validação: {e}"],
                'avisos': [],
                'estatisticas': {}
            }

    def obter_log_migracoes(self) -> List[str]:
        """Retorna log das migrações realizadas"""
        return self.log_migracoes.copy()

    def limpar_log(self):
        """Limpa log de migrações"""
        self.log_migracoes.clear()

    # Métodos privados

    def _ler_excel_legacy(self, caminho_arquivo: str) -> Dict[str, Any]:
        """Lê arquivo Excel do sistema legacy"""
        try:
            # Ler diferentes abas do Excel
            excel_data = pd.ExcelFile(caminho_arquivo)
            dados = {}

            # Aba de configurações (assumindo nome padrão)
            abas_config = ['Configuracao', 'Config', 'Sistema', 'Configurações']
            for aba in abas_config:
                if aba in excel_data.sheet_names:
                    df_config = pd.read_excel(caminho_arquivo, sheet_name=aba)
                    dados['configuracao'] = self._processar_aba_configuracao(df_config)
                    break

            # Aba de unidades
            abas_unidades = ['Unidades', 'Consumidores', 'Clientes']
            for aba in abas_unidades:
                if aba in excel_data.sheet_names:
                    df_unidades = pd.read_excel(caminho_arquivo, sheet_name=aba)
                    dados['unidades'] = self._processar_aba_unidades(df_unidades)
                    break

            # Aba de consumos
            abas_consumos = ['Consumos', 'Historico', 'Dados']
            for aba in abas_consumos:
                if aba in excel_data.sheet_names:
                    df_consumos = pd.read_excel(caminho_arquivo, sheet_name=aba)
                    dados['consumos'] = self._processar_aba_consumos(df_consumos)
                    break

            return dados

        except Exception as e:
            raise ErroMigracaoDados(f"Erro ao ler Excel: {e}")

    def _processar_aba_configuracao(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Processa aba de configuração do Excel"""
        config = {}

        # Tentar diferentes formatos de configuração
        if 'Parametro' in df.columns and 'Valor' in df.columns:
            # Formato chave-valor
            for _, row in df.iterrows():
                parametro = str(row['Parametro']).lower().replace(' ', '_')
                valor = row['Valor']

                # Mapear parâmetros conhecidos
                if 'potencia' in parametro:
                    config['potencia_sistema'] = float(valor) if pd.notna(valor) else 100.0
                elif 'eficiencia' in parametro:
                    config['eficiencia'] = float(valor) if pd.notna(valor) else 0.85
                elif 'tarifa' in parametro:
                    config['tarifa_energia'] = float(valor) if pd.notna(valor) else 0.75
                elif 'investimento' in parametro or 'custo' in parametro:
                    config['custo_investimento'] = float(valor) if pd.notna(valor) else 0.0

        # Valores padrão se não encontrados
        config.setdefault('potencia_sistema', 100.0)
        config.setdefault('eficiencia', 0.85)
        config.setdefault('tarifa_energia', 0.75)
        config.setdefault('custo_investimento', 0.0)

        # Geração mensal padrão
        config.setdefault('geracao_mensal', [8000] * 12)

        return config

    def _processar_aba_unidades(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Processa aba de unidades do Excel"""
        unidades = []

        for index, row in df.iterrows():
            unidade = {
                'nome': str(row.get('Nome', f'Unidade {index + 1}')),
                'tipo_ligacao': str(row.get('Tipo_Ligacao', 'monofasica')).lower(),
                'consumo_mensal': [0] * 12,
                'percentual_alocacao': float(row.get('Percentual', 0.0)) if pd.notna(row.get('Percentual')) else 0.0
            }

            # Processar consumo mensal se estiver nas colunas
            meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
                     'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

            for i, mes in enumerate(meses):
                if mes in row and pd.notna(row[mes]):
                    unidade['consumo_mensal'][i] = float(row[mes])

            unidades.append(unidade)

        return unidades

    def _processar_aba_consumos(self, df: pd.DataFrame) -> Dict[str, List[float]]:
        """Processa aba de consumos do Excel"""
        consumos = {}

        # Assumir que primeira coluna é identificador da unidade
        if len(df.columns) >= 13:  # ID + 12 meses
            for _, row in df.iterrows():
                id_unidade = str(row.iloc[0])
                consumo_mensal = []

                for i in range(1, min(13, len(row))):
                    valor = row.iloc[i]
                    consumo_mensal.append(float(valor) if pd.notna(valor) else 0.0)

                # Completar com zeros se necessário
                while len(consumo_mensal) < 12:
                    consumo_mensal.append(0.0)

                consumos[id_unidade] = consumo_mensal

        return consumos

    def _converter_excel_para_sistema(self, dados_excel: Dict[str, Any]) -> SistemaEnergia:
        """Converte dados do Excel para objeto SistemaEnergia"""

        # Criar configuração
        config_data = dados_excel.get('configuracao', {})
        config = ConfiguracaoSistema(
            potencia_instalada_kw=config_data.get('potencia_sistema', 100.0),
            eficiencia_sistema=config_data.get('eficiencia', 0.85),
            tarifa_energia_kwh=config_data.get('tarifa_energia', 0.75),
            geracao_mensal_kwh=config_data.get('geracao_mensal', [8000] * 12),
            custo_investimento=config_data.get('custo_investimento', 0.0)
        )

        # Criar unidades
        unidades_data = dados_excel.get('unidades', [])
        unidades = []

        for i, unidade_data in enumerate(unidades_data):
            # Mapear tipo de ligação
            tipo_ligacao_str = unidade_data.get('tipo_ligacao', 'monofasica').lower()
            if 'trifasica' in tipo_ligacao_str or 'tri' in tipo_ligacao_str:
                tipo_ligacao = TipoLigacao.TRIFASICA
            elif 'bifasica' in tipo_ligacao_str or 'bi' in tipo_ligacao_str:
                tipo_ligacao = TipoLigacao.BIFASICA
            else:
                tipo_ligacao = TipoLigacao.MONOFASICA

            unidade = UnidadeConsumidora(
                id=f"migrado_{i + 1:03d}",
                nome=unidade_data.get('nome', f'Unidade {i + 1}'),
                tipo_ligacao=tipo_ligacao,
                consumo_mensal_kwh=unidade_data.get('consumo_mensal', [0] * 12),
                percentual_energia_alocada=unidade_data.get('percentual_alocacao', 0.0)
            )

            unidades.append(unidade)

        # Aplicar consumos se disponíveis separadamente
        consumos_data = dados_excel.get('consumos', {})
        for unidade in unidades:
            if unidade.id in consumos_data:
                unidade.consumo_mensal_kwh = consumos_data[unidade.id]

        # Criar sistema
        sistema = SistemaEnergia(
            configuracao=config,
            unidades=unidades,
            versao_sistema="2.0-Migrado-Excel"
        )

        # Armazenar dados originais
        sistema.dados_importacao = dados_excel

        return sistema

    def _processar_consumos_csv(self, df: pd.DataFrame, sistema: SistemaEnergia):
        """Processa consumos de arquivo CSV"""

        # Mapear colunas
        colunas_id = ['id', 'ID', 'Id', 'nome', 'Nome', 'unidade', 'Unidade']
        coluna_id = None

        for col in colunas_id:
            if col in df.columns:
                coluna_id = col
                break

        if coluna_id is None:
            raise ErroMigracaoDados("Coluna de identificação não encontrada no CSV")

        # Processar cada linha
        for _, row in df.iterrows():
            id_unidade = str(row[coluna_id])

            # Buscar unidade correspondente
            unidade = None
            for u in sistema.unidades:
                if u.id == id_unidade or u.nome == id_unidade:
                    unidade = u
                    break

            if unidade is None:
                self._log(f"Unidade não encontrada para ID: {id_unidade}")
                continue

            # Atualizar consumos
            meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
                     'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

            for i, mes in enumerate(meses):
                if mes in row and pd.notna(row[mes]):
                    unidade.consumo_mensal_kwh[i] = float(row[mes])

    def _validar_excel_legacy(self, caminho_arquivo: str) -> Dict[str, Any]:
        """Valida arquivo Excel legacy"""
        resultado = {'erros': [], 'avisos': [], 'estatisticas': {}}

        try:
            excel_data = pd.ExcelFile(caminho_arquivo)
            resultado['estatisticas']['abas_encontradas'] = len(excel_data.sheet_names)
            resultado['estatisticas']['nomes_abas'] = excel_data.sheet_names

            # Verificar abas essenciais
            abas_essenciais = ['Configuracao', 'Config', 'Unidades', 'Consumidores']
            abas_encontradas = [aba for aba in abas_essenciais if aba in excel_data.sheet_names]

            if not abas_encontradas:
                resultado['avisos'].append("Nenhuma aba padrão encontrada, tentarei processar as disponíveis")

        except Exception as e:
            resultado['erros'].append(f"Erro ao validar Excel: {e}")

        return resultado

    def _validar_json_legacy(self, caminho_arquivo: str) -> Dict[str, Any]:
        """Valida arquivo JSON legacy"""
        resultado = {'erros': [], 'avisos': [], 'estatisticas': {}}

        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                dados = json.load(f)

            # Verificar estrutura básica
            if not isinstance(dados, dict):
                resultado['erros'].append("JSON deve ser um objeto")
                return resultado

            resultado['estatisticas']['chaves_principais'] = list(dados.keys())

            # Verificar chaves essenciais
            chaves_essenciais = ['configuracao', 'unidades']
            for chave in chaves_essenciais:
                if chave not in dados:
                    resultado['avisos'].append(f"Chave '{chave}' não encontrada")

        except json.JSONDecodeError as e:
            resultado['erros'].append(f"JSON inválido: {e}")
        except Exception as e:
            resultado['erros'].append(f"Erro ao validar JSON: {e}")

        return resultado

    def _validar_csv_legacy(self, caminho_arquivo: str) -> Dict[str, Any]:
        """Valida arquivo CSV legacy"""
        resultado = {'erros': [], 'avisos': [], 'estatisticas': {}}

        try:
            df = pd.read_csv(caminho_arquivo, encoding='utf-8')
            resultado['estatisticas']['linhas'] = len(df)
            resultado['estatisticas']['colunas'] = len(df.columns)
            resultado['estatisticas']['nomes_colunas'] = list(df.columns)

            # Verificar se tem pelo menos uma coluna de ID
            colunas_id = ['id', 'ID', 'nome', 'Nome']
            tem_id = any(col in df.columns for col in colunas_id)

            if not tem_id:
                resultado['erros'].append("Nenhuma coluna de identificação encontrada")

        except Exception as e:
            resultado['erros'].append(f"Erro ao validar CSV: {e}")

        return resultado

    def _log(self, mensagem: str):
        """Adiciona mensagem ao log"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_migracoes.append(f"[{timestamp}] {mensagem}")


# Classe auxiliar para migração em lote
class MigradorLote:
    """Migrador para processar múltiplos arquivos"""

    def __init__(self):
        self.migrador = MigradorDados()
        self.resultados = []

    def migrar_diretorio(self, caminho_diretorio: str, padrao_arquivos: str = "*") -> List[Dict[str, Any]]:
        """
        Migra todos os arquivos de um diretório
        """
        try:
            diretorio = Path(caminho_diretorio)
            if not diretorio.exists():
                raise ErroMigracaoDados(f"Diretório não encontrado: {caminho_diretorio}")

            arquivos = list(diretorio.glob(padrao_arquivos))
            self.resultados = []

            for arquivo in arquivos:
                resultado = self._migrar_arquivo_individual(str(arquivo))
                self.resultados.append(resultado)

            return self.resultados

        except Exception as e:
            raise ErroMigracaoDados(f"Erro na migração em lote: {e}")

    def _migrar_arquivo_individual(self, caminho_arquivo: str) -> Dict[str, Any]:
        """Migra um arquivo individual"""
        resultado = {
            'arquivo': caminho_arquivo,
            'sucesso': False,
            'sistema': None,
            'erros': [],
            'log': []
        }

        try:
            # Validar arquivo
            validacao = self.migrador.validar_arquivo_legacy(caminho_arquivo)
            if not validacao['valido']:
                resultado['erros'] = validacao['erros']
                return resultado

            # Migrar baseado no tipo
            extensao = Path(caminho_arquivo).suffix.lower()

            if extensao in ['.xlsx', '.xls']:
                sistema = self.migrador.migrar_excel_legacy(caminho_arquivo)
            elif extensao == '.json':
                sistema = self.migrador.migrar_json_legacy(caminho_arquivo)
            else:
                resultado['erros'].append(f"Tipo de arquivo não suportado: {extensao}")
                return resultado

            resultado['sistema'] = sistema
            resultado['sucesso'] = True
            resultado['log'] = self.migrador.obter_log_migracoes()

        except Exception as e:
            resultado['erros'].append(str(e))

        return resultado


# Funções de conveniência
def migrar_arquivo_legacy(caminho_arquivo: str) -> SistemaEnergia:
    """Função de conveniência para migrar um arquivo legacy"""
    migrador = MigradorDados()

    extensao = Path(caminho_arquivo).suffix.lower()

    if extensao in ['.xlsx', '.xls']:
        return migrador.migrar_excel_legacy(caminho_arquivo)
    elif extensao == '.json':
        return migrador.migrar_json_legacy(caminho_arquivo)
    else:
        raise ErroMigracaoDados(f"Tipo de arquivo não suportado: {extensao}")


def validar_antes_migrar(caminho_arquivo: str) -> bool:
    """Função de conveniência para validar arquivo antes da migração"""
    migrador = MigradorDados()
    validacao = migrador.validar_arquivo_legacy(caminho_arquivo)
    return validacao['valido']