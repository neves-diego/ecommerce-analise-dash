# 📊 Dashboard de E-commerce

Este projeto apresenta um **dashboard interativo** desenvolvido em **Python**, utilizando as bibliotecas **Dash** e **Plotly Express**, para análise de dados de clientes de um e-commerce.  
O objetivo é visualizar de forma intuitiva as relações entre **idade**, **salário** e **nível educacional**, com recursos interativos e layout limpo.

---

## 🚀 Tecnologias Utilizadas
- Python 3.x  
- Dash  
- Plotly Express  
- Pandas  

---

## 🧠 Como Executar o Projeto

1️⃣ **Instale as dependências:**  
Crie um ambiente virtual (opcional) e execute:
```bash
pip install dash plotly pandas

2️⃣ Execute o aplicativo Dash:
No terminal, rode o script principal:
python graficos_avancados.py

3️⃣ Acesse o dashboard no navegador:
👉 (http://0.0.0.0:8050/)

📁 Estrutura Sugerida de Pastas

dashboard-ecommerce/
│
├── graficos_avancados.py     # Código principal com o dashboard
├── README.md                 # Este arquivo de documentação
└── data/                     # (opcional) Pasta com o CSV usado no projeto

📊 Exemplo de Código (trecho principal)

import plotly.express as px
import pandas as pd
from dash import Dash, dcc, html

# Carrega os dados
df = pd.read_csv('data/clientes-v3-preparado.csv')

# Cria o aplicativo Dash
app = Dash(__name__)

# Gráfico de dispersão interativo
fig = px.scatter(
    df,
    x='idade',
    y='salario',
    color='nivel_educacao',
    hover_data=['estado_civil']
)

# Layout do aplicativo
app.layout = html.Div([
    html.H1('Idade vs Salário', style={'textAlign': 'center'}),
    dcc.Graph(figure=fig)
])

# Executa o servidor
if __name__ == '__main__':
    app.run(debug=True)  # ou app.run_server(debug=True)


📦 Dependências

dash
plotly
pandas

🪪 Licença

Este projeto está sob a licença MIT, permitindo o uso, modificação e distribuição do código.

✍️ Autor

Diego Neves
📎 LinkedIn

Este projeto está sob a licença MIT, permitindo o uso, modificação e distribuição do código.
