import csv
import os

#Funcion que devuelve las filas leidas de un csv en forma de diccionario
#Return: 
#[
# {(colName:val)_1, ..., (colName:val)_cols}_1, 
# ... ,
# {(colName:val)_1, ..., (colName:val)_n}_rows
#]
def leer(filePath):
    rowsList = []
    print('Leyendo datos: ' + os.path.abspath(filePath))
    with open(filePath, newline='') as file:  
        reader = csv.DictReader(file)
        for row in reader: 
            rowsList += [row] 
    
    return rowsList

#Funcion que escribe los datos de un diccionario en un archivo csv
def escribir(data, fieldNames, filePath):
    with open(filePath, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldNames)
        writer.writeheader()
        writer.writerows(data)

    print('Resultados almacenados en: ' + os.path.abspath(filePath))
