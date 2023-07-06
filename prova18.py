import pandas as pd
import streamlit as st
from pmdarima import auto_arima
import matplotlib.pyplot as plt
from pandas.tseries.offsets import DateOffset
import matplotlib.dates as mdates

def analyze_data(df):
    model = auto_arima(df['Fp'], seasonal=True, m=12)
    forecast = model.predict(n_periods=12)

    fig, ax = plt.subplots()
    ax.plot(df['Fp'], label='Dati storici', color='purple')
    ax.plot(pd.date_range(start=df.index[-1], periods=len(forecast)+1, freq='M')[1:], forecast, label='Forecast', color='black')
    ax.legend()

    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    st.pyplot(fig)

    future_dates = [df.index[-1] + DateOffset(months=x) for x in range(1, len(forecast)+1)]
    df_forecast = pd.DataFrame(forecast, index=future_dates, columns=['Forecast'])
    df_combined = pd.concat([df, df_forecast], axis=1)

    df_combined.index = df_combined.index.strftime('%Y-%m')

    return df_combined

st.title("Claster Forecaster")

uploaded_file = st.file_uploader("Scegli un file Excel", type=['xlsx'])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    df['Data'] = pd.to_datetime(df['Data'])
    df.set_index('Data', inplace=True)

    df_combined = analyze_data(df)

    output_filename = st.text_input("Nome del file di output:")
    if output_filename:
        if st.button("Salva Excel"):
            df_combined.to_excel(output_filename + ".xlsx")
            st.success("File salvato con successo come " + output_filename + ".xlsx")
    else:
        st.error("Per favore, inserisci un nome di file.")
