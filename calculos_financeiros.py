import numpy as np

# ============================================================================
# DISCIPLINA: Administração Financeira - CAD 167
# TEMA: Risco e Retorno - Avaliação de Títulos de Dívida (Renda Fixa)
# ============================================================================

def calcular_preco_titulo_cupom(valor_face, taxa_cupom_anual, ytm, periodos):
    """
    Calcula o preço (Valor Presente) de um título que paga cupons periódicos 
    (ex: NTN-F).
    
    Retorno (YTM): A rentabilidade até o vencimento é a taxa de desconto que 
    iguala o valor presente dos fluxos de caixa futuros ao preço de mercado.
    
    Parâmetros:
    - valor_face: O valor principal do título (ex: R$ 1000).
    - taxa_cupom_anual: A taxa do cupom em decimal (ex: 0.10 para 10%).
    - ytm: Yield to Maturity (Rentabilidade até o vencimento) em decimal.
    - periodos: Prazo do título (anos).
    """
    if periodos <= 0:
    raise ValueError("O prazo do título deve ser maior que zero.")
    if preco <= 0:
    raise ValueError("O preço do título deve ser positivo.")
    cupom = valor_face * taxa_cupom_anual
    
    # Cria um vetor de tempo: [1, 2, ..., N]
    t = np.arange(1, periodos + 1)
    
    # O fluxo de caixa é o cupom em todos os períodos
    fluxos_caixa = np.full(periodos, cupom)
    # No último período, o investidor recebe o cupom + o valor de face (Principal)
    fluxos_caixa[-1] += valor_face  
    
    # Descapitaliza todos os fluxos de caixa trazendo-os para o valor presente
    valores_presentes = fluxos_caixa / ((1 + ytm) ** t)
    preco = np.sum(valores_presentes)
    
    return preco, valores_presentes

def calcular_ytm_cupom_zero(valor_face, preco_mercado, periodos):
    """
    Calcula a Rentabilidade até o Vencimento (YTM) para um título de 
    cupom zero (ex: LTN), onde os investidores recebem apenas o valor de face 
    no vencimento.
    """
    # Fórmula isolando o YTM: 1 + YTM = (Valor de Face / Preço)^(1/n)
    ytm = ((valor_face / preco_mercado) ** (1 / periodos)) - 1
    return ytm

def calcular_duration_macaulay(valores_presentes, preco, periodos):
    """
    Calcula a Duration de Macaulay (Dm).
    Mede o prazo médio ponderado de recebimento dos fluxos de caixa do título.
    """
    t = np.arange(1, periodos + 1)
    
    # Soma ponderada pelo tempo: Sum(t * PV(Fluxo_t)) / Preço
    duration_macaulay = np.sum(t * valores_presentes) / preco
    return duration_macaulay

def calcular_duration_modificada(duration_macaulay, ytm):
    """
    Calcula a Duration Modificada (D*).
    Métrica de RISCO: Mede a variação percentual aproximada no preço do 
    título para uma variação de 1% nas taxas de juros. Títulos de longo 
    prazo são mais sensíveis a mudanças nas taxas.
    """
    # D* = Dm / (1 + y)
    duration_modificada = duration_macaulay / (1 + ytm)
    return duration_modificada

def calcular_convexidade(valor_face, taxa_cupom_anual, ytm, preco, periodos):
    """
    Calcula a Convexidade de um título.
    Métrica de RISCO (Avançada): Ajusta a Duration, pois a relação entre o 
    preço do título e a taxa de juros não é linear, mas sim uma curva convexa.
    A convexidade mede a curvatura (segunda derivada do preço em relação ao YTM).
    """
    cupom = valor_face * taxa_cupom_anual
    t = np.arange(1, periodos + 1)
    
    # Implementação do somatório da segunda derivada
    # Termo 1: Somatório sobre os cupons
    soma_cupons = np.sum((t * (t + 1) * cupom) / ((1 + ytm) ** t))
    
    # Termo 2: Efeito do Principal no vencimento
    fator_principal = (periodos * (periodos + 1) * valor_face) / ((1 + ytm) ** periodos)
    
    # Cálculo final da Convexidade
    convexidade = (1 / (preco * ((1 + ytm) ** 2))) * (soma_cupons + fator_principal)
    return convexidade

def calcular_taxa_real(taxa_nominal, taxa_inflacao):
    """
    Calcula a Taxa de Juros Real.
    Dada uma taxa de juros nominal e a inflação do período, indica o crescimento 
    real do poder aquisitivo.
    """
    # Fórmula: Taxa Real = ((1 + Taxa Nominal) / (1 + Taxa Inflação)) - 1
    # Matematicamente equivalente a: (Nominal - Inflacao) / (1 + Inflacao)
    taxa_real = (taxa_nominal - taxa_inflacao) / (1 + taxa_inflacao)
    return taxa_real

# ============================================================================
# Função consolidadora (Interface  usar no main.py)
# ============================================================================

def gerar_relatorio_risco_retorno_titulo(valor_face, taxa_cupom_anual, ytm, periodos, inflacao=0.0):
    """
    Recebe os parâmetros do título, executa toda a modelagem matemática de 
    Risco e Retorno e devolve um dicionário formatado com os resultados.
    """
    # 1. Avaliação do Retorno
    preco, pv_fluxos = calcular_preco_titulo_cupom(valor_face, taxa_cupom_anual, ytm, periodos)
    taxa_real = calcular_taxa_real(ytm, inflacao)
    
    # 2. Avaliação do Risco (Sensibilidade)
    d_mac = calcular_duration_macaulay(pv_fluxos, preco, periodos)
    d_mod = calcular_duration_modificada(d_mac, ytm)
    convexidade = calcular_convexidade(valor_face, taxa_cupom_anual, ytm, preco, periodos)
    
    return {
        "Retorno": {
            "Preco_Justo (R$)": round(preco, 2),
            "YTM_Nominal (%)": round(ytm * 100, 2),
            "YTM_Real (%)": round(taxa_real * 100, 2)
        },
        "Risco": {
            "Duration_Macaulay (Anos)": round(d_mac, 4),
            "Duration_Modificada (%)": round(d_mod * 100, 4),
            "Convexidade": round(convexidade, 4)
        }
    }