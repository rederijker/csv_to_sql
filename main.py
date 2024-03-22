import streamlit as st
import pandas as pd
from io import StringIO

def csv_to_sql(csv_data, table_name="my_table"):
    # Converti i dati CSV in un DataFrame
    df = pd.read_csv(StringIO(csv_data))
    
    # Crea l'istruzione SQL per creare la tabella
    sql_create_table = f"CREATE TABLE {table_name} ("
    sql_create_table += ", ".join([f"{col} TEXT" for col in df.columns])
    sql_create_table += ");\n"
    
    # Genera le istruzioni SQL per inserire i dati
    sql_inserts = ""
    for _, row in df.iterrows():
        values = "', '".join([str(value).replace("'", "''") for value in row])
        sql_inserts += f"INSERT INTO {table_name} VALUES ('{values}');\n"
    
    # Combina le istruzioni SQL
    sql_commands = sql_create_table + sql_inserts
    return sql_commands

# Interfaccia utente Streamlit
st.title("Convertitore CSV in SQL")

uploaded_file = st.file_uploader("Carica un file CSV", type="csv")
if uploaded_file is not None:
    table_name = st.text_input("Nome della tabella SQL", value="my_table")
    
    if st.button("Converti in SQL"):
        # Legge i dati CSV
        csv_data = uploaded_file.getvalue().decode("utf-8")
        
        # Converte il CSV in stringhe SQL
        sql_commands = csv_to_sql(csv_data, table_name=table_name)
        
        # Mostra il bottone per scaricare il file SQL
        st.download_button(label="Scarica SQL",
                           data=sql_commands,
                           file_name=f"{table_name}.sql",
                           mime="text/plain")
