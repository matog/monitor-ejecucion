# -*- coding: utf-8 -*-
import datetime

from datetime import date
import dash
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import plotly.express as px
# import calendar
import plotly.express as px
import pandas as pd
import dash_table
import pandas as pd

# Cargamos la base
df = pd.read_csv('base.csv')


# Convertimos el campo impacto_presupuestario_mes a fecha
df['impacto_presupuestario_mes'] = pd.to_datetime(df['impacto_presupuestario_mes'], format='%m').dt.month


# Rango del eje X de los gráficos
range_x1 = df['impacto_presupuestario_mes'].iloc[0]
range_x2 = df['impacto_presupuestario_mes'].iloc[-1]

# Filtramos incisos
df = df.loc[df['inciso_id']<6]

# Obtención de la ejecucion, ultima actualizacion, y SAF
vigente = df['credito_vigente'].sum
devengado = df['credito_devengado'].sum
ejecucion = ((devengado(0)/vigente(0)).round(2))*100
ejecucion = str(round(ejecucion, 2))
ejecucion_texto = "Ejecucion:" + str(ejecucion) + "%"
actualizacion = df['ultima_actualizacion_fecha'].iloc[0]
saf_id = df['servicio_id'].iloc[0]
titulo = "Ejecución Presupuestaria SAF " + str(saf_id)
programas = df['programa_desc'].unique()

df.rename(columns = {'credito_devengado': 'Credito Devengado',
                     'impacto_presupuestario_mes': 'Mes',
                     'fuente_financiamiento_desc' : 'Fuente de Financiamiento',
                     'programa_desc' : 'Programa'
                     },
                inplace = True)

# -------------------------------------------------------
# APP DE DASH
# -------------------------------------------------------

app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.MATERIA],
                meta_tags=[{'name': 'viewport',
                            # "content": "width=device-width, initial-scale=1"
                            'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'
                            }]
                )
server = app.server

alert = dbc.Alert("Por favor seleccione un programa.",
                  color="danger",
                  duration = 3000,
                  # dismissable=True
                  )  # use dismissable or duration=5000 for alert to close in x milliseconds


# Grafico estatico
table= df.groupby(['Mes','Fuente de Financiamiento'])['Credito Devengado'].sum().unstack()
table = table.assign(TOTAL=table.sum(1)).stack().to_frame('Credito Devengado')
table.reset_index(inplace=True)
saf = px.line(table,
              x='Mes',
              y='Credito Devengado',
              color = 'Fuente de Financiamiento',
              template = 'plotly_white'
              # template = 'plotly_dark',
             )
saf.update_layout(
    legend=dict(
        x=0.01,
        y=0.95,
        traceorder="normal",
        font=dict(
            # family="sans-serif",
            # size=10,
            color="black"
        ),
    ),
    xaxis=dict(
        tickmode='linear',
        tick0=1,
        dtick=1
    )
)
saf.update_xaxes(range=[range_x1, range_x2])





app.title = 'Ejecución Presupuestaria'
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([html.H1(titulo,
                         className='text-center text-primary, mb-4'),
                 ], width=12)
    ]),
    dbc.Row(
        [
            dbc.Col(html.H4(ejecucion_texto)),
            dbc.Col(html.H4(actualizacion)),
        ]
    ),
    dbc.Row(
        dbc.Col([
            html.Div(
                id="alert_prg",
                children=[]
            )
        ], width = 12)
    ),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='saf-graph',
                figure=saf,
                responsive=True,
                config={
                    'displayModeBar': False}
                ),
         ], width = 12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='prg-dpdn',
                options=[{'label': x.title(), 'value': x} for x in sorted(programas)],
                value=[df['Programa'].iloc[0]],
                placeholder="Seleccione Programa",
                # bs_size="sm",
                multi=True,
                style=dict(
                    width='100%',
                    display='inline-block',
                    # verticalAlign="middle",
                    # fontSize=10,
                    height="100%",
                ),
            ),
            ], width=12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='prg-graph',
                responsive=True,
                config={
                    'displayModeBar': False}

                ),
            ],width=12)
    ]),
    dbc.Row(
        dbc.Col([
            dash_table.DataTable(
                id='prg-tbl',
                columns=[
                    {'name': 'Programa', 'id': 'Programa'},
                    {'name': 'Credito Vigente', 'id': 'credito_vigente'},
                    {'name': 'Credito Devengado', 'id': 'Credito Devengado'},
                ],
                page_action="native",
                page_size=10,
                style_as_list_view=True,
                style_cell={
                    # 'font_family': 'cursive',
                    # 'font_size': '8px',
                    'padding': '1px',
                    # 'text_align': 'center'
                },
            ),
        ], width = 12)
    ),
    dbc.Row([
        dbc.Col([
            html.Br(),
            html.Br()
            ]),
    ]),
    dbc.Row([
        dbc.Col(html.A('Fuente: Presupuesto Abierto', href='http://www.presupuestoabierto.gob.ar', target="_blank")),
        dbc.Col(),
        dbc.Col(html.A('By Mato', href='http://matog.github.io/cv', target="_blank"), style={'text-align': 'right'})
    ]),
])




# ---------------------------------------------------------------
# Callback
# ---------------------------------------------------------------

# Graficamos los programas
@app.callback(
    Output("alert_prg", "children"),
    Output("prg-graph", 'figure'),
    Output("prg-tbl", 'data'),
    Input('prg-dpdn', 'value'),
)
def programas(programa):
    if len(programa) > 0:
        dff = df[df.Programa.isin(programa)]
        dff = dff.groupby(['Mes','Programa']).sum().reset_index()
        fig = px.line(dff,
                      x='Mes',
                      y='Credito Devengado',
                      color='Programa',
                      template = 'plotly_white'
                      )
        fig.update_layout(
            legend=dict(
                x=0.01,
                y=0.95,
                traceorder="normal",
                font=dict(
                    # family="sans-serif",
                    # size=10,
                    color="black"
                    ),
                ),
            xaxis=dict(
                tickmode='linear',
                tick0=1,
                dtick=1
            )
        )

        fig.update_xaxes(range=[range_x1, range_x2])
        dff_tbl = df[df.Programa.isin(programa)]
        dff_tbl = dff_tbl.groupby(['Programa'])['credito_vigente', 'Credito Devengado'].sum().reset_index()
        dff_tbl = dff_tbl.round(3)
        # print(dff_tbl)
        return dash.no_update, fig, dff_tbl.to_dict(orient='records')
    elif len(programa) == 0:
        return alert, dash.no_update, dash.no_update


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)

