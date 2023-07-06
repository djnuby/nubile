import base64
import io
import pandas as pd
from pmdarima import auto_arima
import plotly.graph_objects as go
from pandas.tseries.offsets import DateOffset
import streamlit as st


def analyze_data(df):
    model = auto_arima(df['Fp'], seasonal=True, m=12)
    forecast = model.predict(n_periods=12)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Fp'], mode='lines', name='Dati storici'))
    fig.add_trace(go.Scatter(x=pd.date_range(start=df.index[-1], periods=13, freq='M')[1:], y=forecast, mode='lines', name='Forecast'))
    st.plotly_chart(fig)

    future_dates = [df.index[-1] + DateOffset(months=x) for x in range(1, len(forecast)+1)]
    df_forecast = pd.DataFrame(forecast, index=future_dates, columns=['Forecast'])
    df_combined = pd.concat([df, df_forecast], axis=1)

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_combined.to_excel(writer)
    excel_data = output.getvalue()
    b64 = base64.b64encode(excel_data)
    payload = b64.decode()

    href = f'<a download="output.xlsx" href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{payload}" target="_blank">Scarica file Excel</a>'
    st.markdown(href, unsafe_allow_html=True)

st.title('Claster Forecaster')
uploaded_file = st.file_uploader("Carica file Excel", type='xlsx')

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    df['Data'] = pd.to_datetime(df['Data'])
    df.set_index('Data', inplace=True)
    analyze_data(df)
