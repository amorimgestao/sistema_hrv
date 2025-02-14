import streamlit as st
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

st.title("Dashboard HRV - Dados da API")

# =============================================================================
# Função para gerar o HTML do tooltip
# =============================================================================
def tooltip_html(text):
    return f'<span class="tooltip">ℹ️<span class="tooltiptext">{text}</span></span>'

# =============================================================================
# Função para buscar dados na API do sistema de cobranças
# =============================================================================
def get_api_data():
    api_url = "https://sistemahrv-jyehvvbzwkqmwnu5q87gsy.streamlit.app/"  # Substitua pela URL correta da sua API
    api_token = "$aact_MzkwODA2MWY2OGM3MWRlMDU2NWM3MzJlNzZmNGZhZGY6OmYyMGRlN2RiLTVhM2QtNDA3My1hYjkxLWI2NTA5ZjhmZGExYjo6JGFhY2hfOTNmODQ4NmQtYjg4Yy00NWM1LTgxY2QtY2NjNGEyYTcyNDhm"
    headers = {
        "Authorization": f"Bearer {api_token}"
    }
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Levanta erro para status diferentes de 200
        return response.json()  # Supondo que a resposta seja em JSON
    except Exception as e:
        st.error("Erro ao carregar os dados da API.")
        st.error(e)
        st.stop()  # Para a execução se não conseguir os dados da API

# =============================================================================
# Obter dados da API
# =============================================================================
api_data = get_api_data()

# =============================================================================
# Configuração dos Indicadores
# =============================================================================
# Cada métrica possui:
# - "name": Nome do indicador (deve corresponder à chave da API em minúsculo)
# - "explanation": Breve explicação para o tooltip
# - "type": "revenue" para indicadores onde aumento é bom; "cost" para indicadores onde redução é boa
#
# **Importante:** A estrutura da resposta da API deve ser algo como:
# {
#    "receita": {"jan": 15191.00, "dec": 17897.00, "delta_val": -2706.00, "delta_perc": -13.67},
#    "custo fixo": {"jan": 3850.34, "dec": 4407.89, "delta_val": -557.55, "delta_perc": -12.64},
#    ...
# }
#
# Assim, usamos a chave (em minúsculo) para obter os dados de cada métrica.
metrics_config = [
    {
        "name": "Receita",
        "explanation": ("A Receita representa o total de dinheiro recebido pela empresa a partir das vendas ou serviços prestados. "
                        "Uma queda na receita pode indicar uma diminuição nas vendas ou perda de clientes, o que é negativo."),
        "type": "revenue"
    },
    {
        "name": "Custo Fixo",
        "explanation": ("Custos Fixos são despesas que não variam com o volume de produção, como aluguel e salários fixos. "
                        "Reduzir esses custos é positivo, pois melhora a margem de lucro."),
        "type": "cost"
    },
    {
        "name": "Custos Operacionais",
        "explanation": ("Custos Operacionais referem-se às despesas diretamente ligadas à operação do negócio, como manutenção e logística. "
                        "Uma redução nesses custos aumenta a eficiência operacional."),
        "type": "cost"
    },
    {
        "name": "Custo por Cliente",
        "explanation": ("O Custo por Cliente é o valor médio gasto para atender cada cliente. Uma diminuição nesse indicador é positiva, "
                        "indicando maior eficiência no atendimento."),
        "type": "cost"
    },
    {
        "name": "Custo Total",
        "explanation": ("O Custo Total é a soma de todas as despesas da empresa. Reduzir o custo total é fundamental para aumentar a rentabilidade."),
        "type": "cost"
    },
    {
        "name": "Taxa Asaas",
        "explanation": ("A Taxa Asaas é o valor cobrado pela plataforma de pagamentos. Embora seja um custo, uma redução nessa taxa é positiva, "
                        "pois impacta menos nos resultados financeiros."),
        "type": "cost"
    },
    {
        "name": "% Custo Asaas",
        "explanation": ("Este indicador mostra o percentual da receita gasto com a Taxa Asaas. Uma redução é positiva, pois indica que o custo da plataforma "
                        "tem menor impacto sobre o faturamento."),
        "type": "cost"
    },
    {
        "name": "Juros Recebido",
        "explanation": ("Juros Recebidos são os encargos cobrados dos clientes inadimplentes, representando dinheiro extra que entra na empresa. "
                        "Um aumento neste valor é positivo, indicando mais recursos, embora possa também sinalizar problemas de inadimplência."),
        "type": "revenue"
    }
]

# =============================================================================
# Montar lista final de métricas com os dados vindos da API
# =============================================================================
metrics = []
for m in metrics_config:
    key = m["name"].lower()  # Espera-se que a chave na API seja o nome da métrica em minúsculo
    if key in api_data:
        dados = api_data[key]
        m["jan"] = dados.get("jan")
        m["dec"] = dados.get("dec")
        m["delta_val"] = dados.get("delta_val")
        m["delta_perc"] = dados.get("delta_perc")
        metrics.append(m)
    else:
        st.warning(f"Dados para '{m['name']}' não encontrados na API.")

# Se nenhum dado foi carregado, interrompe a execução
if not metrics:
    st.error("Nenhum dado de métrica foi carregado da API.")
    st.stop()

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
        
        # Define a lógica de cores:
        delta_color = "normal" if metric["type"] == "revenue" else "inverse"
        
        st.metric(label="", value=value_str, delta=delta_display, delta_color=delta_color)

st.markdown("<hr><p style='text-align: center; color: #666;'>Dashboard HRV © 2025</p>", unsafe_allow_html=True)
