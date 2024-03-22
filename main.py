import streamlit as st
import pandas as pd
from io import StringIO

def csv_to_sql(df, table_name="my_table"):
    # Crea l'istruzione SQL per creare la tabella
    # Nota: Qui si assume che tutte le colonne siano di tipo TEXT per semplicità.
    sql_create_table = f"CREATE TABLE {table_name} ("
    sql_create_table += ", ".join([f"{col} TEXT" for col in df.columns])
    sql_create_table += ");\n"

    # Genera le istruzioni SQL per inserire i dati
    sql_inserts = ""
    for _, row in df.iterrows():
        values = "', '".join(str(value).replace("'", "''") for value in row)  # Gestisce le singole virgolette nei dati
        sql_inserts += f"INSERT INTO {table_name} VALUES ('{values}');\n"
    
    return sql_create_table + sql_inserts

# Interfaccia utente di Streamlit
def main():
    st.title("Convertitore CSV to SQL")
    uploaded_file = st.file_uploader("Carica un file CSV", type=['csv'])
    table_name = st.text_input("Nome della tabella SQL", value="my_table")
    
    if uploaded_file is not None:
        # Legge il file CSV in un DataFrame
        df = pd.read_csv(uploaded_file)
        
        # Converti il DataFrame in stringhe SQL
        sql_commands = csv_to_sql(df, table_name=table_name)

        # Crea un buffer di output per il file SQL
        output_buffer = StringIO()
        output_buffer.write(sql_commands)
        output_buffer.seek(0)
        
        # Permette all'utente di scaricare il file SQL
        st.download_button(label="Scarica SQL",
                           data=sql_commands.encode('utf-8'),
                           file_name=f"{table_name}.sql",
                           mime="application/sql")

if __name__ == "__main__":
    main()
