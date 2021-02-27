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
# import geopandas as gpd
import plotly.express as px
import pandas as pd
import dash_table
# import pandas as pd
# import dash_table_experiments as dt

# Cargamos la base
df = pd.read_excel('Base_mes.xlsx')

# Convertimos el campo YYYYMM a fecha y le quitamos el numero de dia (siempre es el 1ro, de cada mes, cuando
#   en realidad es el ultimo dia del mes)
df['yyyymm'] = pd.to_datetime(df['yyyymm'], format='%Y%m')
range_x1 = df['yyyymm'].iloc[0]
range_x2 = df['yyyymm'].iloc[-1]
print(range_x2)
# range_x2
df['yyyymm'] = df['yyyymm'].dt.date.apply(lambda x: x.strftime('%Y-%m'))
df = df.rename(columns={'yyyymm': 'fecha'})

# Convertimos en millones las variables de credito
df['credito_devengado'] = (df['credito_devengado'].astype(float)/1000000).round(2)
df['credito_vigente'] = (df['credito_vigente'].astype(float)/1000000).round(2)
df['credito_inicial'] = (df['credito_inicial'].astype(float)/1000000).round(2)

# Filtramos programas e incisos
df = df.loc[df['programa_id']<40]
df = df.loc[df['inciso_id']<6]
vigente = df['credito_vigente'].sum
devengado = df['credito_devengado'].sum
ejecucion = ((devengado(0)/vigente(0)).round(2))*100
ejecucion_texto = "Ejecucion:" + str(ejecucion) + "%"
actualizacion = df['actualizacion'].iloc[0]
actualizacion = "Última actualización:" + df['actualizacion'].iloc[0]


# print(df.columns)

# dt = datetime.datetime.today()
# inicio = date(2020,1,1)
# # dias = dt - inicio
# # dias_de_ejecucion = dias.days
# # delta = end-start
# # >>> delta.days
# print(dt)



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


alert = dbc.Alert("Por favor seleccione un programa.",
                  color="danger",
                  duration = 3000,
                  # dismissable=True
                  )  # use dismissable or duration=5000 for alert to close in x milliseconds


# Grafico estatico
table= df.groupby(['fecha','fuente_de_financiamiento_desc'])['credito_devengado'].sum().unstack()
table = table.assign(TOTAL=table.sum(1)).stack().to_frame('credito_devengado')
table.reset_index(inplace=True)
saf = px.line(table,
              x='fecha',
              y='credito_devengado',
              color = 'fuente_de_financiamiento_desc',
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
    )
)
saf.update_xaxes(range=[range_x1, range_x2])

# saf.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)')

app.title = 'Ejecución Presupuestaria'
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([html.H1("Ejecución Presupuestaria SAF322",
                         className='text-center text-primary, mb-4'),
                 ], width=12)
    ]),
    dbc.Row(
        [
            dbc.Col(html.H3(ejecucion_texto)),
            dbc.Col(html.H3(actualizacion)),
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
                config={
                    'displayModeBar': False}
                ),
         ], width = 12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id='prg-dpdn',
                options=[{'label': x.title(), 'value': x} for x in sorted(df.programa_desc.unique())],
                value=['Actividades Centrales'],
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
                    {'name': 'Programa', 'id': 'programa_desc'},
                    {'name': 'Credito Inicial', 'id': 'credito_inicial'},
                    {'name': 'Credito Vigente', 'id': 'credito_vigente'},
                    {'name': 'Credito Devengado', 'id': 'credito_devengado'},
                    # {'name': 'Provincia', 'id': 'name_prov'}
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
    dbc.Row(html.H1(" "))
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
        dff = df[df.programa_desc.isin(programa)]
        dff = dff.groupby(['fecha','programa_desc']).sum().reset_index()
        fig = px.line(dff,
                      x='fecha',
                      y='credito_devengado',
                      color='programa_desc',
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
                )
            )
        fig.update_xaxes(range=[range_x1, range_x2])

        # fig.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)')

        dff_tbl = df[df.programa_desc.isin(programa)]
        dff_tbl = dff_tbl.groupby(['programa_desc'])['credito_vigente', 'credito_devengado','credito_inicial'].sum().reset_index()
        dff_tbl = dff_tbl.round(3)
        # print(dff_tbl)
        return dash.no_update, fig, dff_tbl.to_dict(orient='records')
    elif len(programa) == 0:
        return alert, dash.no_update, dash.no_update


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)

