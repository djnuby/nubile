import base64
import pandas as pd
from pmdarima import auto_arima
import matplotlib.pyplot as plt
from pandas.tseries.offsets import DateOffset
import matplotlib.dates as mdates
import streamlit as st

def analyze_data(df, filename):
    # Adattare il nome della colonna al tuo file Excel
    model = auto_arima(df['Fp'], seasonal=True, m=12)
    forecast = model.predict(n_periods=12)

    # Crea un grafico con matplotlib
    fig, ax = plt.subplots()
    ax.plot(df['Fp'], label='Dati storici', color='purple')
    ax.plot(pd.date_range(start=df.index[-1], periods=len(forecast)+1, freq='M')[1:], forecast, label='Forecast', color='yellow')
    ax.legend()

    # Formatta l'asse x con anni
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    # Aggiungi il titolo del file Excel al grafico
    ax.set_title(filename) 

    st.pyplot(fig)  # Mostra il grafico in Streamlit

    # Scrittura del risultato e dei dati su file Excel
    future_dates = [df.index[-1] + DateOffset(months=x) for x in range(1, len(forecast)+1)]
    df_forecast = pd.DataFrame(forecast, index=future_dates, columns=['Forecast'])
    df_combined = pd.concat([df, df_forecast], axis=1)

    # Modifica il formato della data prima di scriverla su file
    df_combined.index = df_combined.index.strftime('%Y-%m')
    df_combined.index.name = 'Data'

    return df_combined

# Aggiungi un titolo e un pulsante di upload del file all'app Streamlit
st.title("ClAster Forecaster, analisi previsionale Sarima per  il tuo cluster in un istante")
uploaded_file = st.file_uploader("Scegli un file Excel", type="xlsx")

# Quando l'utente carica un file, leggilo e analizzalo
if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    # Converte la colonna 'Data' in datetime e la imposta come indice
    df['Data'] = pd.to_datetime(df['Data'])
    df.set_index('Data', inplace=True)

    df_combined = analyze_data(df, uploaded_file.name)
    
    # Salva il dataframe come CSV (Streamlit non supporta direttamente il salvataggio di file Excel)
    csv = df_combined.to_csv(index=True)
    b64 = base64.b64encode(csv.encode()).decode()  # alcuni byte magici per la codifica
    href = f'<a href="data:file/csv;base64,{b64}" download="output.csv">Scarica il CSV</a>'
    st.markdown(href, unsafe_allow_html=True)
