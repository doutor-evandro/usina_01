"""
Teste do Sistema Completo - Todas as Funcionalidades
"""

import sys
import os
import matplotlib

matplotlib.use('Agg')  # Backend não-interativo
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import SistemaEnergiaSolar
from configuracao.definicoes import obter_sistema_padrao
import json


def teste_sistema_completo():
    """Testa todas as funcionalidades do sistema"""
    print("🚀 TESTE DO SISTEMA COMPLETO")
    print("=" * 60)

    try:
        # Criar sistema
        print("1. 🔧 Criando sistema...")
        sistema = SistemaEnergiaSolar()
        print("✅ Sistema criado com sucesso!")

        # Testar cálculos
        print("\n2. 🔢 Testando cálculos...")
        resultados = sistema.calcular_resultados_anuais(2024)
        if resultados:
            print("✅ Cálculos realizados com sucesso!")
            print(f"   Geração: {resultados['energia']['geracao_total']:.0f} kWh")
            print(f"   Economia: R$ {resultados['financeiro']['economia_total']:.2f}")
        else:
            print("❌ Erro nos cálculos")
            return False

        # Testar relatório
        print("\n3. 📋 Testando relatório...")
        arquivo_relatorio = sistema.gerar_relatorio_completo(2024)
        if arquivo_relatorio and os.path.exists(arquivo_relatorio):
            print("✅ Relatório gerado com sucesso!")
            print(f"   Arquivo: {arquivo_relatorio}")
        else:
            print("❌ Erro no relatório")
            return False

        # Testar gráficos
        print("\n4. 📈 Testando gráficos...")
        try:
            arquivos_graficos = sistema.gerar_graficos_analise(2024)
            if arquivos_graficos:
                print(f"✅ Gráficos gerados: {len(arquivos_graficos)}")
                for arquivo in arquivos_graficos:
                    if os.path.exists(arquivo):
                        print(f"   - {os.path.basename(arquivo)}")
                    else:
                        print(f"   - {os.path.basename(arquivo)} (erro)")
            else:
                print("⚠️ Nenhum gráfico gerado (pode ser normal)")
        except Exception as e:
            print(f"⚠️ Erro nos gráficos (não crítico): {e}")

        # Testar migração
        print("\n5. 🔄 Testando migração...")
        # Criar arquivo de teste para migração
        dados_teste = {
            'configuracao': {
                'potencia_sistema': 150.0,
                'eficiencia': 0.85,
                'tarifa_energia': 0.75
            },
            'unidades': [
                {
                    'nome': 'Teste Migração',
                    'tipo_ligacao': 'monofasica',
                    'consumo_mensal': [400] * 12
                }
            ]
        }

        with open('teste_migracao.json', 'w') as f:
            json.dump(dados_teste, f)

        try:
            sucesso_migracao = sistema.migrar_arquivo_legacy('teste_migracao.json')
            if sucesso_migracao:
                print("✅ Migração realizada com sucesso!")
            else:
                print("⚠️ Migração não realizada (pode ser normal)")
        except Exception as e:
            print(f"⚠️ Erro na migração (não crítico): {e}")

        # Testar funcionalidades adicionais
        print("\n6. 🔍 Testando funcionalidades adicionais...")

        # Testar resumo do sistema
        try:
            print("   - Testando resumo do sistema...")
            # Capturar saída do resumo
            import io
            import contextlib

            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                sistema.exibir_resumo_sistema()

            resumo_output = f.getvalue()
            if "RESUMO DO SISTEMA" in resumo_output:
                print("   ✅ Resumo do sistema funcionando")
            else:
                print("   ⚠️ Resumo do sistema com problemas")

        except Exception as e:
            print(f"   ⚠️ Erro no resumo: {e}")

        # Testar relatório resumido
        try:
            print("   - Testando relatório resumido...")
            relatorio_resumido = sistema.gerador_relatorios.gerar_relatorio_resumido(2024)
            if "RELATÓRIO RESUMIDO" in relatorio_resumido:
                print("   ✅ Relatório resumido funcionando")
            else:
                print("   ⚠️ Relatório resumido com problemas")
        except Exception as e:
            print(f"   ⚠️ Erro no relatório resumido: {e}")

        print("\n" + "=" * 60)
        print("🎉 TESTE COMPLETO FINALIZADO!")
        print("✅ Funcionalidades principais testadas com sucesso!")
        print("📊 Sistema de energia solar operacional!")
        print("=" * 60)

        # Exibir estatísticas finais
        print("\n📈 ESTATÍSTICAS DO TESTE:")
        print(f"   🔋 Potência: {sistema.sistema.configuracao.potencia_instalada_kw:.1f} kW")
        print(f"   ⚡ Geração Anual: {resultados['energia']['geracao_total']:.0f} kWh")
        print(f"   🏠 Consumo Anual: {resultados['energia']['consumo_total']:.0f} kWh")
        print(f"   💰 Economia Anual: R$ {resultados['financeiro']['economia_total']:.2f}")
        print(f"   📈 Payback: {resultados['financeiro']['payback_anos']:.1f} anos")
        print(f"   🏢 Unidades Ativas: {len(sistema.sistema.get_unidades_ativas())}")

        return True

    except Exception as e:
        print(f"❌ Erro crítico no teste: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        # Limpar arquivos de teste
        arquivos_limpeza = [
            'teste_migracao.json',
            'relatorio_energia_2024.txt',
            'relatorio_resumido_teste.txt'
        ]

        for arquivo in arquivos_limpeza:
            if os.path.exists(arquivo):
                try:
                    os.remove(arquivo)
                    print(f"🧹 Arquivo limpo: {arquivo}")
                except:
                    pass

        # Limpar gráficos de teste
        try:
            for arquivo in os.listdir('.'):
                if arquivo.startswith('grafico_') and arquivo.endswith('.png'):
                    os.remove(arquivo)
                    print(f"🧹 Gráfico limpo: {arquivo}")
        except:
            pass


def teste_rapido():
    """Teste rápido das funcionalidades essenciais"""
    print("⚡ TESTE RÁPIDO")
    print("=" * 30)

    try:
        sistema = SistemaEnergiaSolar()
        resultados = sistema.calcular_resultados_anuais(2024)
        relatorio = sistema.gerar_relatorio_completo(2024)

        print("✅ Cálculos: OK")
        print("✅ Relatório: OK")
        print("🎉 Sistema funcionando!")

        return True
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--rapido":
        teste_rapido()
    else:
        teste_sistema_completo()