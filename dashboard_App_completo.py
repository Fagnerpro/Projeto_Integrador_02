
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
import plotly.express as px
import pandas as pd
from pymongo import MongoClient

# Tema tecnológico e institucional
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MORPH])
app.title = "Projeto Smart Saneamento | Dashboard"

# Conexão com MongoDB
client = MongoClient("mongodb://localhost:27017/")
df = pd.DataFrame(list(client["saneamento"]["dados_operacionais"].find()))

# Pré-processamento
df["ano"] = df["ano"].astype(int)
df["agua_cobertura"] = df["agua"].apply(lambda x: x.get("indice_atendimento_percentual", 0)) * 100
df["esgoto_cobertura"] = df["esgoto"].apply(lambda x: x.get("indice_atendimento_percentual", 0)) * 100
df["perda_percentual"] = df["indice_perda_agua"]

# Gráficos
fig_agua = px.line(df, x="ano", y="agua_cobertura", markers=True,
                   title="Cobertura de Água (%)", color_discrete_sequence=["#007BFF"])
fig_esgoto = px.line(df, x="ano", y="esgoto_cobertura", markers=True,
                     title="Cobertura de Esgoto (%)", color_discrete_sequence=["#28A745"])
fig_perda = px.line(df, x="ano", y="perda_percentual", markers=True,
                    title="Índice de Perdas de Água (%)", color_discrete_sequence=["#DC3545"])

# Layout visual com identidade forte
app.layout = dbc.Container([
    html.Div([
        html.H2("Projeto Integrador - Tecnologia em Inteligência Artificial", className="text-center text-primary fw-bold mb-1"),
        html.H4("Sistema de Monitoramento de Indicadores Operacionais da Saneago", className="text-center text-secondary mb-4")
    ]),
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("Cobertura de Água", className="fw-bold text-primary"),
            dbc.CardBody(dcc.Graph(figure=fig_agua, config={"displayModeBar": False}))
        ], className="shadow-sm rounded border-0"), md=4),
        dbc.Col(dbc.Card([
            dbc.CardHeader("Cobertura de Esgoto", className="fw-bold text-success"),
            dbc.CardBody(dcc.Graph(figure=fig_esgoto, config={"displayModeBar": False}))
        ], className="shadow-sm rounded border-0"), md=4),
        dbc.Col(dbc.Card([
            dbc.CardHeader("Índice de Perdas", className="fw-bold text-danger"),
            dbc.CardBody(dcc.Graph(figure=fig_perda, config={"displayModeBar": False}))
        ], className="shadow-sm rounded border-0"), md=4),
    ], className="mb-4"),
    html.Div(html.Footer("Fonte: MongoDB | Projeto Integrador - SENAI FATESG | Desenvolvido por Fagner", 
             className="text-center text-muted fst-italic mt-3"), style={"fontSize": "0.9rem"})
], fluid=True)

if __name__ == "__main__":
    app.run(debug=True)