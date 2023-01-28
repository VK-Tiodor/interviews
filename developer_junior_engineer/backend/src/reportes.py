#!/usr/bin/env python
import sys
import csv

#Comprobamos que se esten pasando los archivos csv
if len(sys.argv) < 4:
    print('Usage: %s <customers.csv> <orders.csv> <products.csv>' % sys.argv[0])

def leerCSV(fileName):
    rowsList = []
    #Leemos los ficheros y almacenamos la informacion
    with open(fileName, newline='') as file:  
        reader = csv.reader(file)
        #La primera línea (cabecera de la tabla) no nos interesa
        reader.__next__()
        for row in reader: 
            rowsList += [tuple(row)] 
    
    return rowsList

customers = leerCSV(sys.argv[1])
orders =leerCSV (sys.argv[2])
products = leerCSV(sys.argv[3])

print(customers)
print(orders)
print(products)