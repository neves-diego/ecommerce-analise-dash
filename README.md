# 📊 Dashboard de E-commerce

Este projeto apresenta um **dashboard interativo** desenvolvido em **Python**, utilizando as bibliotecas **Dash** e **Plotly Express**, para análise de dados de um e-commerce.  
O objetivo é visualizar de forma intuitiva as relações entre **notas**, **preços**, **avaliações** e **descontos** dos produtos, com recursos interativos e layout responsivo.

---

## 🚀 Tecnologias Utilizadas

- **Python 3.x**
- **Dash** - Framework para aplicações web
- **Plotly Express** - Visualizações interativas
- **Pandas** - Manipulação de dados

---

## 🧠 Como Executar o Projeto

### 1️⃣ **Instale as dependências:**
```bash
pip install dash plotly pandas statsmodels
2️⃣ Execute o aplicativo Dash:
bash
python dash_ecommerce_estatistica.py
3️⃣ Acesse o dashboard no navegador:
👉 http://localhost:8050

📊 Funcionalidades do Dashboard
📈 10 Gráficos Interativos incluindo:

Distribuição de notas dos produtos

Relação preço vs avaliações

Mapa de calor de correlações

Análise por gênero, marca e material

Tendência entre desconto e nota

🎛️ Filtros Dinâmicos por:

Gênero do produto

Temporada

Marca

📱 Layout Responsivo com grid CSS

📁 Estrutura do Projeto
text
dashboard-ecommerce/
│
├── dash_ecommerce_estatistica.py  # Código principal do dashboard
├── ecommerce_estatistica.csv      # Dataset de produtos
├── README.md                      # Documentação
└── requirements.txt              # Dependências (opcional)
🎯 Exemplo de Código (Trecho Principal)
python
import plotly.express as px
import pandas as pd
from dash import Dash, dcc, html, Input, Output

# Carrega os dados
df = pd.read_csv('ecommerce_estatistica.csv')

# Cria o aplicativo Dash
app = Dash(__name__)

# Layout com gráficos interativos
app.layout = html.Div([
    html.H1("Dashboard: E-commerce - Análise Exploratória", 
            style={'textAlign': 'center'}),
    
    # Filtros
    html.Div([
        dcc.Dropdown(id='genero-filter', options=[]),
        dcc.Dropdown(id='temporada-filter', options=[])
    ]),
    
    # Gráficos
    html.Div([
        dcc.Graph(id='hist-notas'),
        dcc.Graph(id='scatter-preco-avaliacoes')
    ])
])

# Callbacks para interatividade
@app.callback(
    Output('hist-notas', 'figure'),
    Input('genero-filter', 'value')
)
def update_histogram(genero):
    # Lógica de atualização...
    return fig

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)
📦 Dependências
txt
dash>=2.0.0
plotly>=5.0.0
pandas>=1.0.0
statsmodels>=0.13.0  # Para trendlines LOWESS
🔧 Personalização
O código foi desenvolvido com arquitetura modular:

Funções específicas para cada tipo de gráfico

Tratamento robusto de dados ausentes

Callbacks centralizados para melhor manutenção

🪪 Licença
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

✍️ Autor
Diego Neves
📧 LinkedIn
