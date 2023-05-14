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
    
    # Inserisco almeno 3 lettere del cognome nella password in modo casuale
    password_list = list(password)
    surname_letters = random.sample(surname, min(3, len(surname)))
    for letter in surname_letters:
        random_index = random.randint(0, length-1)
        password_list[random_index] = letter
    password = ''.join(password_list)
    
    return password

# Interfaccia con Streamlit
def main():
    st.title("Generatore di password")
    st.write("Gabriele Garasi, creami la password perfetta")
    surname = st.text_input("Inserisci il cognome")
    length = st.number_input("Inserisci la lunghezza della password", min_value=8, max_value=20, step=1, value=12, format="%d")
    
    if st.button("Genera password"):
        password = generate_password(surname, length)
        st.success("La password generata è: " + password)

if __name__ == '__main__':
    main()
