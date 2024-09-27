import pandas as pd
import os
import glob

# Definir las carpetas de entrada y salida
input_folder = 'input'   # Carpeta donde están los archivos de entrada
output_folder = 'output' # Carpeta donde se guardará el archivo de salida

# Crear las carpetas si no existen
os.makedirs(input_folder, exist_ok=True)
os.makedirs(output_folder, exist_ok=True)

# Definir la ruta del archivo de salida
output_file = os.path.join(output_folder, 'output.xlsx')

# Usar glob para obtener todos los archivos .xls en la carpeta de entrada
input_files = glob.glob(os.path.join(input_folder, '*.xls'))

# Leer y concatenar todas las hojas de cada archivo .xls
df_list = []
for file in input_files:
    df_temp = pd.concat(pd.read_excel(file, sheet_name=None), ignore_index=True)  # Leer todas las hojas de cada archivo
    df_list.append(df_temp)

# Concatenar todos los DataFrames en uno solo
df = pd.concat(df_list, ignore_index=True)

# Procesar los datos
df = df[['Dispositivo', 'Estado', 'Sub-Estado', 'Id. Aplicación', 'TIPO_DISCADOR', 'Inicio', 'País/Provincia', 'ANI/Teléfono']]  # Filtramos las columnas de interés

df["Inicio"] = df["Inicio"].astype(str)  # Convertir a string
timestamp = df["Inicio"].str.split(' ', expand=True)  # Separar por espacio
timestamp.columns = ['Fecha', 'Hora']  # Renombrar columnas

hora = timestamp['Hora'].apply(lambda x: x[:2])  # Tomar los dos primeros caracteres de la hora
hora = pd.DataFrame(hora)

timestamp = timestamp.drop(['Hora'], axis=1)  # Eliminar la columna Hora original

# Concatenar las nuevas columnas
fechahora = pd.concat([timestamp, hora], axis=1)
df = pd.concat([df, fechahora], axis=1)
df = df.drop(['Inicio'], axis=1)  # Eliminar la columna "Inicio"

# Procesar la columna de teléfonos
df["ANI/Teléfono"] = df["ANI/Teléfono"].astype(str)  # Convertir a string
caract = df['ANI/Teléfono'].apply(lambda x: x[:3])  # Tomar los tres primeros caracteres del número de teléfono
caract = pd.DataFrame(caract)

df = df.drop(['ANI/Teléfono'], axis=1)  # Eliminar la columna original
df = pd.concat([df, caract], axis=1)  # Concatenar con el DataFrame original

# Guardar el archivo de salida en la carpeta output
df.to_excel(output_file, index=False, sheet_name="Hoja1")

print(f"Archivos procesados y guardados en {output_file}")
