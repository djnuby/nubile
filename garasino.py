import random
import string
import streamlit as st

def generate_password(surname, length):
    # Converto il cognome in una lista di lettere
    letters = list(surname)
    
    # Verifico se le lettere sono consecutive
    consecutive = True
    for i in range(len(letters)-1):
        if ord(letters[i+1].lower()) - ord(letters[i].lower()) == 1:
            consecutive = False
            break
    
    # Se le lettere sono consecutive, le mescolo
    if consecutive:
        random.shuffle(letters)
    
    # Aggiungo caratteri speciali alla lista di lettere
    special_chars = list(string.punctuation)
    letters += special_chars
    
    # Genero la password come stringa
    password = ''.join(random.sample(letters, length))
    
    return password

# Interfaccia con Streamlit
def main():
    st.title("Generatore di password")
    st.write("Gabriele Garasi, creami la password perfetta!!!")
    surname = st.text_input("Inserisci il cognome")
    length = st.number_input("Inserisci la lunghezza della password", min_value=8, max_value=20, step=1, value=12, format="%d")
    
    if st.button("Genera password"):
        password = generate_password(surname, length)
        st.success("La password generata è: " + password)

if __name__ == '__main__':
    main()
