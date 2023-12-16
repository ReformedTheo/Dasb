import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

# Função para carregar os dados
def load_data():
    return pd.read_excel('mandar_pro_chat.xlsx')

# Inicializar o app Dash
app = dash.Dash(__name__)

# Layout do Dash app
app.layout = html.Div([
    html.H1("Análise de KPIs"),
    dcc.Dropdown(
        id='kpi-dropdown',
        options=[],  # As opções serão preenchidas pelo callback
        value=None
    ),
    dcc.Interval(
            id='interval-component',
            interval=60*1000,  # em milissegundos (atualizar a cada 1 minuto)
            n_intervals=0
    ),
    dcc.Graph(id='kpi-graph')
])

# Callback para atualizar as opções do dropdown
@app.callback(
    Output('kpi-dropdown', 'options'),
    [Input('interval-component', 'n_intervals')]
)
def update_dropdown_options(n):
    data = load_data()
    kpis = [{'label': kpi, 'value': kpi} for kpi in data['KPI - DETOX PARIS'].unique()]
    return kpis

# Callback para atualizar o gráfico
@app.callback(
    Output('kpi-graph', 'figure'),
    [Input('kpi-dropdown', 'value')]
)
def update_graph(selected_kpi):
    if not selected_kpi:
        return go.Figure()

    data = load_data()
    kpi_data = data[data['KPI - DETOX PARIS'] == selected_kpi]
    weeks = []
    weekly_earnings = []
    weekly_goal = kpi_data['META'].iloc[0]

    week_count = 1
    for month in ['JAN', 'FEV', 'MAR', 'ABR', 'MAI', 'JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV', 'DEZ']:
        for week in range(4):  # Assumindo 4 semanas por mês
            column_name = f'{month}.{week}' if week > 0 else month
            if column_name in kpi_data.columns:
                earnings = kpi_data[column_name].iloc[0]
                weekly_earnings.append(earnings)
                weeks.append(week_count)
                week_count += 1

    # Criando a figura Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=weeks, y=weekly_earnings, mode='lines+markers', name='Rendimento Semanal'))
    fig.add_hline(y=weekly_goal, line_dash="dash", line_color="red", annotation_text="Meta Semanal")

    return fig

# Executar o app
if __name__ == '__main__':
    app.run_server(debug=False)
