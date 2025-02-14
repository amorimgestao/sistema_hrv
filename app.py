import streamlit as st
import pandas as pd
import requests

# =============================================================================
# Configuração da Página
# =============================================================================
st.set_page_config(page_title="Dashboard HRV", layout="wide", page_icon=":bar_chart:")

# =============================================================================
# CSS Customizado: Fundo branco, visual limpo, tooltip com fonte 9px e redução do espaçamento
# =============================================================================
st.markdown("""
    <style>
        body {
            background-color: #ffffff;
            color: #333;
            font-family: 'Segoe UI', sans-serif;
        }
        .main > div:first-child {
            background-color: #ffffff;
            padding: 1rem 2rem;
            border-radius: 0.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        /* Estilo para o tooltip */
        .tooltip {
            position: relative;
            display: inline-block;
            cursor: pointer;
            color: #4a90e2;
            font-size: 14px;
            margin-left: 4px;
        }
        .tooltip .tooltiptext {
            visibility: hidden;
            width: 250px;
            background-color: #555;
            color: #fff;
            text-align: left;
            border-radius: 6px;
            padding: 5px;
            position: absolute;
            z-index: 1;
            bottom: 125%;
            left: 50%;
            margin-left: -125px;
            opacity: 0;
            transition: opacity 0.3s;
            font-size: 9px;
        }
        .tooltip:hover .tooltiptext {
            visibility: visible;
            opacity: 1;
        }
        /* Contêiner para título com tooltip */
        .indicator-container {
            margin-bottom: -50px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("Dashboard HRV - Dezembro vs. Janeiro")

# =============================================================================
# Função para gerar o HTML do tooltip
# =============================================================================
def tooltip_html(text):
    return f'<span class="tooltip">ℹ️<span class="tooltiptext">{text}</span></span>'

# =============================================================================
# Função para buscar dados na API do sistema de cobranças
# =============================================================================
def get_api_data():
    # Substitua pela URL correta da sua API
    api_url = "https://sistemahrv-jyehvvbzwkqmwnu5q87gsy.streamlit.app/"  
    # Token de autenticação
    api_token = "$aact_MzkwODA2MWY2OGM3MWRlMDU2NWM3MzJlNzZmNGZhZGY6OmYyMGRlN2RiLTVhM2QtNDA3My1hYjkxLWI2NTA5ZjhmZGExYjo6JGFhY2hfOTNmODQ4NmQtYjg4Yy00NWM1LTgxY2QtY2NjNGEyYTcyNDhm"
    
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Levanta erro para status != 200
        return response.json()  # Supondo que a resposta seja em JSON
    except Exception as e:
        st.error("Erro ao carregar os dados da API.")
        st.error(e)
        return None

# =============================================================================
# Dados dos Indicadores (KPIs)
# =============================================================================
# Estrutura padrão caso a API não retorne dados ou para teste local.
metrics = [
    {
        "name": "Receita",
        "jan": 15191.00,
        "dec": 15191.00 + 2706.00,  # 17897.00
        "delta_val": -2706.00,
        "delta_perc": -13.67,
        "type": "revenue",
        "explanation": ("A Receita representa o total de dinheiro recebido pela empresa a partir das vendas ou serviços prestados. "
                        "Uma queda na receita pode indicar uma diminuição nas vendas ou perda de clientes, o que é negativo.")
    },
    {
        "name": "Custo Fixo",
        "jan": 3850.34,
        "dec": 3850.34 + 557.55,  # 4407.89
        "delta_val": -557.55,
        "delta_perc": -12.64,
        "type": "cost",
        "explanation": ("Custos Fixos são despesas que não variam com o volume de produção, como aluguel e salários fixos. "
                        "Reduzir esses custos é positivo, pois melhora a margem de lucro.")
    },
    {
        "name": "Custos Operacionais",
        "jan": 1696.83,
        "dec": 1696.83 + 1521.11,  # 3217.94
        "delta_val": -1521.11,
        "delta_perc": -47.27,
        "type": "cost",
        "explanation": ("Custos Operacionais referem-se às despesas diretamente ligadas à operação do negócio, como manutenção e logística. "
                        "Uma redução nesses custos aumenta a eficiência operacional.")
    },
    {
        "name": "Custo por Cliente",
        "jan": 205.45,
        "dec": 205.45 + 76.99,  # 282.44
        "delta_val": -76.99,
        "delta_perc": -27.25,
        "type": "cost",
        "explanation": ("O Custo por Cliente é o valor médio gasto para atender cada cliente. Uma diminuição nesse indicador é positiva, "
                        "indicando maior eficiência no atendimento.")
    },
    {
        "name": "Custo Total",
        "jan": 5547.17,
        "dec": 5547.17 + 2078.66,  # 7625.83
        "delta_val": -2078.66,
        "delta_perc": -27.25,
        "type": "cost",
        "explanation": ("O Custo Total é a soma de todas as despesas da empresa. Reduzir o custo total é fundamental para aumentar a rentabilidade.")
    },
    {
        "name": "Taxa Asaas",
        "jan": 154.66,
        "dec": 154.66 - 15.73,  # 138.93
        "delta_val": +15.73,
        "delta_perc": +11.32,
        "type": "cost",
        "explanation": ("A Taxa Asaas é o valor cobrado pela plataforma de pagamentos. Embora seja um custo, uma redução nessa taxa é positiva, "
                        "pois impacta menos nos resultados financeiros.")
    },
    {
        "name": "% Custo Asaas",
        "jan": 1.04,
        "dec": 1.04 + 0.54,  # 1.58%
        "delta_val": -0.54,
        "delta_perc": None,
        "type": "cost",
        "explanation": ("Este indicador mostra o percentual da receita gasto com a Taxa Asaas. Uma redução é positiva, pois indica que o custo da plataforma "
                        "tem menor impacto sobre o faturamento.")
    },
    {
        "name": "Juros Recebido",
        "jan": 300.00,
        "dec": 300.00 - 204.00,  # 96.00
        "delta_val": +204.00,
        "delta_perc": +312.5,
        "type": "revenue",
        "explanation": ("Juros Recebidos são os encargos cobrados dos clientes inadimplentes, representando dinheiro extra que entra na empresa. "
                        "Um aumento neste valor é positivo, indicando mais recursos, embora possa também sinalizar problemas de inadimplência.")
    }
]

# =============================================================================
# Atualiza os indicadores com os dados da API, se disponíveis
# =============================================================================
api_data = get_api_data()

if api_data:
    # Supondo que a resposta da API seja um dicionário onde cada chave corresponde ao nome da métrica em minúsculas
    # e os valores são dicionários com os dados atualizados.
    # Exemplo: 
    # {
    #   "receita": {"jan": 15200.00, "dec": 18000.00, "delta_val": -2800.00, "delta_perc": -14.00},
    #   "custo fixo": {...},
    #    ...
    # }
    for metric in metrics:
        key = metric["name"].lower()
        if key in api_data:
            dados = api_data[key]
            metric["jan"] = dados.get("jan", metric["jan"])
            metric["dec"] = dados.get("dec", metric["dec"])
            metric["delta_val"] = dados.get("delta_val", metric["delta_val"])
            metric["delta_perc"] = dados.get("delta_perc", metric["delta_perc"])

# =============================================================================
# Exibição dos Cards com KPIs e Tooltip
# =============================================================================
st.markdown("### Indicadores Financeiros")
num_cols = 4
cols = st.columns(num_cols)

for i, metric in enumerate(metrics):
    with cols[i % num_cols]:
        # Título com tooltip
        title_html = f"<div class='indicator-container'><span style='font-weight:bold;'>{metric['name']}</span>{tooltip_html(metric['explanation'])}</div>"
        st.markdown(title_html, unsafe_allow_html=True)
        
        # Formatação dos valores
        if metric["name"] == "% Custo Asaas":
            value_str = f"{metric['jan']:.2f}%"
            delta_str = f"{abs(metric['delta_val']):.2f}%"
        else:
            value_str = f"R$ {metric['jan']:,.2f}"
            delta_str = f"R$ {abs(metric['delta_val']):,.2f}"
        
        if metric["delta_perc"] is not None:
            delta_perc_str = f"{abs(metric['delta_perc']):.2f}%"
            delta_display = f"{'-' if metric['delta_val'] < 0 else '+'}{delta_str} ({'-' if metric['delta_perc'] < 0 else '+'}{delta_perc_str})"
        else:
            delta_display = f"{'-' if metric['delta_val'] < 0 else '+'}{delta_str}"
        
        # Define a cor do delta (exemplo: verde para revenue, vermelho para cost)
        delta_color = "normal" if metric["type"] == "revenue" else "inverse"
        st.metric(label="", value=value_str, delta=delta_display, delta_color=delta_color)

st.markdown("<hr><p style='text-align: center; color: #666;'>Dashboard HRV © 2025</p>", unsafe_allow_html=True)
