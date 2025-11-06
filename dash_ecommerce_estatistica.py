"""
Dash app refatorado para visualizar ecommerce_estatistica.csv
Autor: Diego Neves (refatorado)
Observações:
- Pré-processamento é feito ao carregar o arquivo.
- Callbacks apenas filtram e chamam builders de figura.
- Funções pequenas e documentadas.
"""

import pandas as pd
from typing import Tuple
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go

# -----------------------
# Configurações / Constantes
# -----------------------
CSV_PATH = "ecommerce_estatistica.csv"
NUMERIC_COLS_DEFAULT = ['Nota', 'N_Avaliações', 'Desconto', 'Preço', 'Nota_MinMax', 'N_Avaliações_MinMax']
TOP_N_MARCAS = 10
TOP_N_MATERIAIS = 8

# -----------------------
# Leitura e pré-processamento (única vez)
# -----------------------
def load_and_prepare(path: str) -> pd.DataFrame:
    """
    Lê CSV e aplica limpeza mínima (preenche NA em colunas categóricas usadas no dashboard).
    Retorna DataFrame pronto para uso.
    """
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")
    # Garantir colunas categóricas com valores padrão
    for col in ['Gênero', 'Marca', 'Material', 'Temporada']:
        if col in df.columns:
            df[col] = df[col].fillna('Não definido')
        else:
            # cria coluna vazia caso não exista (evita erros downstream)
            df[col] = 'Não definido'
    # Se colunas numéricas faltarem, cria com NaN (manter workflow previsível)
    for col in NUMERIC_COLS_DEFAULT:
        if col not in df.columns:
            df[col] = pd.NA
    return df

df = load_and_prepare(CSV_PATH)

# Pré-calculados para layout (listas de opções)
GENERO_OPTS = ['all'] + sorted(df['Gênero'].unique().tolist())
TEMPORADA_OPTS = ['all'] + sorted(df['Temporada'].unique().tolist())
MARCA_OPTS = ['all'] + sorted(df['Marca'].unique().tolist())

# -----------------------
# Helpers de filtragem e criação de figuras
# -----------------------
def filter_df(base: pd.DataFrame, genero: str, temporada: str, marca: str) -> pd.DataFrame:
    """Aplica filtros simples e retorna novo DataFrame."""
    d = base
    if genero and genero != 'all':
        d = d[d['Gênero'] == genero]
    if temporada and temporada != 'all':
        d = d[d['Temporada'] == temporada]
    if marca and marca != 'all':
        d = d[d['Marca'] == marca]
    return d

def safe_fig_empty(message: str = "Sem dados para os filtros selecionados"):
    """Figura simples mostrando mensagem quando não há dados."""
    fig = go.Figure()
    fig.update_layout(
        xaxis={'visible': False},
        yaxis={'visible': False},
        annotations=[{
            'text': message,
            'xref': 'paper',
            'yref': 'paper',
            'x': 0.5,
            'y': 0.5,
            'showarrow': False,
            'font': {'size': 16}
        }]
    )
    return fig

def build_histogram(df_local: pd.DataFrame) -> go.Figure:
    if df_local.empty:
        return safe_fig_empty()
    fig = px.histogram(df_local, x='Nota', nbins=20)
    fig.update_layout(xaxis_title='Nota (1-5)', yaxis_title='Frequência', showlegend=False)
    return fig

def build_scatter_preco_avaliacoes(df_local: pd.DataFrame) -> go.Figure:
    if df_local.empty:
        return safe_fig_empty()
    fig = px.scatter(df_local, x='Preço', y='N_Avaliações', opacity=0.6, hover_data=['Título', 'Marca'])
    fig.update_layout(xaxis_title='Preço (R$)', yaxis_title='Nº Avaliações')
    return fig

def build_heatmap_corr(df_local: pd.DataFrame, numeric_cols=NUMERIC_COLS_DEFAULT) -> go.Figure:
    # proteger caso nem todas colunas numéricas existam ou sejam todas NA
    valid_cols = [c for c in numeric_cols if c in df_local.columns and df_local[c].notna().any()]
    if len(valid_cols) < 2:
        return safe_fig_empty("Correlação: dados numéricos insuficientes")
    corr = df_local[valid_cols].corr().round(2)
    fig = go.Figure(data=go.Heatmap(z=corr.values, x=corr.columns, y=corr.columns, colorscale='RdBu', zmin=-1, zmax=1))
    fig.update_layout(height=420)
    return fig

def build_bar_avgnota_por_genero(df_local: pd.DataFrame) -> go.Figure:
    if df_local.empty:
        return safe_fig_empty()
    grp = df_local.groupby('Gênero')['Nota'].mean().reset_index().sort_values('Nota', ascending=False)
    fig = px.bar(grp, x='Gênero', y='Nota')
    fig.update_layout(xaxis_title='Gênero', yaxis_title='Nota média')
    return fig

def build_pie_genero(df_local: pd.DataFrame) -> go.Figure:
    if df_local.empty:
        return safe_fig_empty()
    dist = df_local['Gênero'].value_counts().reset_index()
    dist.columns = ['Gênero', 'Quantidade']
    fig = px.pie(dist, values='Quantidade', names='Gênero')
    return fig

def build_price_density(df_local: pd.DataFrame) -> go.Figure:
    if df_local.empty:
        return safe_fig_empty()
    fig = px.histogram(df_local, x='Preço', nbins=40)
    fig.update_layout(xaxis_title='Preço (R$)', yaxis_title='Contagem')
    return fig

def build_trend_desconto_nota(df_local: pd.DataFrame) -> go.Figure:
    if df_local.empty:
        return safe_fig_empty()
    fig = px.scatter(df_local, x='Desconto', y='Nota', trendline='lowess', opacity=0.6)
    fig.update_layout(xaxis_title='Desconto (%)', yaxis_title='Nota')
    return fig

def build_top_marcas(df_local: pd.DataFrame, topn=TOP_N_MARCAS) -> go.Figure:
    if df_local.empty:
        return safe_fig_empty()
    top = df_local['Marca'].value_counts().head(topn).reset_index()
    top.columns = ['Marca', 'Quantidade']
    fig = px.bar(top, x='Marca', y='Quantidade')
    fig.update_layout(xaxis_title='Marca', yaxis_title='Quantidade de produtos')
    return fig

def build_box_by_material(df_local: pd.DataFrame, col_y: str, topn=TOP_N_MATERIAIS) -> go.Figure:
    if df_local.empty:
        return safe_fig_empty()
    top_materials = df_local['Material'].value_counts().head(topn).index
    sub = df_local[df_local['Material'].isin(top_materials)]
    if sub.empty:
        return safe_fig_empty()
    fig = px.box(sub, x='Material', y=col_y)
    return fig

# -----------------------
# App Dash (layout)
# -----------------------
app = dash.Dash(__name__)
app.title = "E-commerce — Dashboard"

app.layout = html.Div([
    html.H1("Dashboard: E-commerce (Análise Exploratória)", style={'textAlign': 'center'}),
    # filtros
    html.Div([
        dcc.Dropdown(id='genero-filter', options=[{'label': g, 'value': g} for g in GENERO_OPTS], value='all', clearable=False),
        dcc.Dropdown(id='temporada-filter', options=[{'label': t, 'value': t} for t in TEMPORADA_OPTS], value='all', clearable=False),
        dcc.Dropdown(id='marca-filter', options=[{'label': m, 'value': m} for m in MARCA_OPTS], value='all', clearable=False)
    ], style={'display': 'flex', 'gap': '10px', 'margin': '20px'}),
    # gráficos (grid simples)
    html.Div([
        dcc.Graph(id='hist-notas'),
        dcc.Graph(id='scatter-preco-avaliacoes'),
        dcc.Graph(id='heatmap-corr'),
        dcc.Graph(id='avg-nota-genero'),
        dcc.Graph(id='pie-genero'),
        dcc.Graph(id='densidade-precos'),
        dcc.Graph(id='desconto-nota'),
        dcc.Graph(id='top-marcas'),
        dcc.Graph(id='box-preco-material'),
        dcc.Graph(id='box-nota-material'),
    ], style={'display': 'grid', 'gridTemplateColumns': 'repeat(2, 1fr)', 'gap': '20px', 'padding': '0 20px'}),
    # insights simples (texto dinâmico)
    html.Div(id='insights', style={'padding': '20px', 'backgroundColor': '#f4f6f8', 'margin': '20px'})
])

# -----------------------
# Callback principal (centralizado)
# -----------------------
@app.callback(
    [
        Output('hist-notas', 'figure'),
        Output('scatter-preco-avaliacoes', 'figure'),
        Output('heatmap-corr', 'figure'),
        Output('avg-nota-genero', 'figure'),
        Output('pie-genero', 'figure'),
        Output('densidade-precos', 'figure'),
        Output('desconto-nota', 'figure'),
        Output('top-marcas', 'figure'),
        Output('box-preco-material', 'figure'),
        Output('box-nota-material', 'figure'),
        Output('insights', 'children')
    ],
    [Input('genero-filter', 'value'),
     Input('temporada-filter', 'value'),
     Input('marca-filter', 'value')]
)
def update_all(genero, temporada, marca):
    # Filtra
    dff = filter_df(df, genero, temporada, marca)
    # Gera figuras (cada builder trata do caso vazio)
    figs = [
        build_histogram(dff),
        build_scatter_preco_avaliacoes(dff),
        build_heatmap_corr(dff),
        build_bar_avgnota_por_genero(dff),
        build_pie_genero(dff),
        build_price_density(dff),
        build_trend_desconto_nota(dff),
        build_top_marcas(dff),
        build_box_by_material(dff, 'Preço'),
        build_box_by_material(dff, 'Nota'),
    ]
    # Insights (texto simples)
    if dff.empty:
        insights_children = html.Div("Sem dados para os filtros selecionados.", style={'color': 'red', 'fontWeight': 'bold'})
    else:
        total = len(dff)
        insights_children = html.Div([
            html.P(f"Total produtos: {total}"),
            html.P(f"Nota média: {dff['Nota'].mean():.2f}"),
            html.P(f"Preço médio: R$ {dff['Preço'].mean():.2f}"),
            html.P(f"Marca mais comum: {dff['Marca'].mode().iat[0] if not dff['Marca'].mode().empty else 'N/A'}")
        ])
    return (*figs, insights_children)

# -----------------------
# Executar app
# -----------------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)
