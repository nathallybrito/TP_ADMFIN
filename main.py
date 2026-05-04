import calculos_financeiros as motor
import dados_relatorios as relatorios

def main():
    print("Iniciando a aplicação de Administração Financeira...")
    
    # 1. Captura a inflação e converte para formato decimal (ex: 4.14% vira 0.0414)
    inflacao_percentual = relatorios.capturar_ipca_acumulado()
    inflacao_decimal = inflacao_percentual / 100.0
    
    # 2. Configura os dados do Título Fictício
    valor_face = 1000.00
    cupom_anual = 0.10
    ytm_atual = 0.12
    prazo_anos = 5
    
    # 3. Chama o processamento matemático com o NOME CORRETO da função da dupla
    resultados = motor.gerar_relatorio_risco_retorno_titulo(
        valor_face=valor_face,
        taxa_cupom_anual=cupom_anual,
        ytm=ytm_atual,
        periodos=prazo_anos,
        inflacao=inflacao_decimal
    )
    
    # 4. Gera os artefatos visuais e textuais
    # Passando a função correta de cálculo de preço para a geração do gráfico
    relatorios.gerar_grafico_convexidade(
        valor_face=valor_face, 
        cupom=cupom_anual, 
        prazo=prazo_anos, 
        funcao_calculo_preco=motor.calcular_preco_titulo_cupom
    )
    
    relatorios.gerar_relatorio_final(dados_calculados=resultados, inflacao_usada=inflacao_percentual)
    
    print("\n[SUCESSO] Processamento finalizado! Os artefatos estão na pasta atual.")

if __name__ == "__main__":
    main()