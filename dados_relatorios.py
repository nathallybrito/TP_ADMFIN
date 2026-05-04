import requests
import matplotlib.pyplot as plt
import datetime

def capturar_ipca_acumulado():
    """
    Captura o IPCA acumulado de 12 meses mais recente utilizando a API do Banco Central do Brasil (SGS).
    """
    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.13522/dados/ultimos/1"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        dados = response.json()
        ipca = float(dados[0]['valor'])
        print(f"[OK] Dados capturados com sucesso. IPCA 12m: {ipca}% (Data-base: {dados[0]['data']})")
        return ipca
    except Exception as e:
        print(f"[AVISO] Falha ao acessar a API do BCB: {e}. Usando valor de fallback de 4.5%.")
        return 4.5

def gerar_grafico_convexidade(valor_face, cupom, prazo, funcao_calculo_preco):
    """
    Gera o gráfico ilustrativo de convexidade do título simulando diferentes taxas de juros (YTM).
    """
    taxas_simuladas = range(1, 21)
    precos_simulados = []

    for taxa in taxas_simuladas:
        taxa_decimal = taxa / 100.0
        
        preco = funcao_calculo_preco(valor_face, cupom, taxa_decimal, prazo)[0]
        precos_simulados.append(preco)

    plt.figure(figsize=(10, 6))
    plt.plot(list(taxas_simuladas), precos_simulados, marker='o', linestyle='-', color='b')
    plt.title("Risco e Retorno: Relação Preço vs Taxa de Juros (Convexidade)")
    plt.xlabel("Taxa de Juros - YTM (%)")
    plt.ylabel("Preço do Título (R$)")
    plt.grid(True)
    
    nome_arquivo = "convexidade_titulo.png"
    plt.savefig(nome_arquivo)
    plt.close()
    print(f"[OK] Gráfico de convexidade salvo como '{nome_arquivo}'.")

def gerar_relatorio_final(dados_calculados, inflacao_usada):
    """
    Gera um relatório formatado em .txt contendo os resultados matemáticos e os dados da disciplina.
    """
    nome_arquivo = "relatorio_final_admfin.txt"
    data_atual = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    
    retorno = dados_calculados.get("Retorno", {})
    risco = dados_calculados.get("Risco", {})
    
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write("========================================================\n")
        f.write("      UNIVERSIDADE FEDERAL DE MINAS GERAIS (UFMG)\n")
        f.write("          Sistemas de Informação - CAD 167\n")
        f.write("             Prof: Bruno Pérez Ferreira\n")
        f.write("========================================================\n")
        f.write(f"Data de Execução: {data_atual}\n\n")
        
        f.write("--- DADOS MACROECONÔMICOS CAPTURADOS ---\n")
        f.write(f"Inflação (IPCA Acumulado 12m): {inflacao_usada}%\n\n")
        
        f.write("--- MÉTRICAS DE RETORNO ---\n")
        f.write(f"Preço Justo (Valor Presente): R$ {retorno.get('Preco_Justo (R$)', 'N/D')}\n")
        f.write(f"YTM Nominal: {retorno.get('YTM_Nominal (%)', 'N/D')}%\n")
        f.write(f"YTM Real (Descontada Inflação): {retorno.get('YTM_Real (%)', 'N/D')}%\n\n")
        
        f.write("--- MÉTRICAS DE RISCO ---\n")
        f.write(f"Duration de Macaulay: {risco.get('Duration_Macaulay (Anos)', 'N/D')} anos\n")
        f.write(f"Duration Modificada: {risco.get('Duration_Modificada (%)', 'N/D')}%\n")
        f.write(f"Convexidade: {risco.get('Convexidade', 'N/D')}\n")
        f.write("========================================================\n")
        f.write("Aplicação concluída. Verifique também o gráfico gerado.\n")
        
    print(f"[OK] Relatório final salvo como '{nome_arquivo}'.")