import requests
import mysql.connector

# Consulta à API do SIDRA
url = "https://apisidra.ibge.gov.br/values/t/8880/v/7169/C11046/56734/n3/all/p/all?formato=json"
response = requests.get(url)
data = response.json()

# Conexão com MySQL
conn = mysql.connector.connect(
    host="192.168.0.192",
    user="destino",
    password="098Daiane.",
    database="sidra"
)
cursor = conn.cursor()

# SQL de inserção com IGNORE para não inserir duplicados
sql = """
INSERT IGNORE INTO pmc_88802 (
    valor,
    indice,
    uf,
    mesano_codigo,
    mesano
) VALUES (%s, %s, %s, %s, %s)
"""

inseridos = 0
ignorados = 0
nulos = 0

for record in data[1:]:
    valor_str = record.get("V", "").strip()

    try:
        valor = float(valor_str)
    except ValueError:
        valor = None
        nulos += 1

    valores = (
        valor,
        record.get("D2N"),  # indice
        record.get("D3N"),  # uf
        record.get("D4C"),  # mesano_codigo
        record.get("D4N")   # mesano
    )

    cursor.execute(sql, valores)
    inseridos += cursor.rowcount  # Só conta se realmente inseriu (0 se duplicado)

conn.commit()
print(f"{inseridos} registros inseridos.")
print(f"{nulos} valores estavam indisponíveis e foram salvos como NULL.")
print(f"{len(data)-1 - inseridos} registros ignorados por serem duplicados.")

cursor.close()
conn.close()
