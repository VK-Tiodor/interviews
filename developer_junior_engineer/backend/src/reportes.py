#!/usr/bin/env python
import sys
import csv

#Comprobamos que se esten pasando los archivos csv
if len(sys.argv) < 4:
    print('Usage: %s <customers.csv> <orders.csv> <products.csv>' % sys.argv[0])

customers = []
#Leemos los ficheros y almacenamos la informacion
with open(sys.argv[1], newline='') as customersFile:  
    reader = csv.reader(customersFile)
    #La primera línea (cabecera de la tabla) no nos interesa
    reader.__next__()
    for (id,firstname,lastname) in reader: #Convertimos los datos de listas a tuplas mientras leemos
        customers += [(id,firstname,lastname)]

orders = []
with open(sys.argv[2], newline='') as ordersFile:  
    reader = csv.reader(ordersFile)
    reader.__next__()
    for (id,customer,products) in reader:
        orders += [((id,customer,products))]

products = []
with open(sys.argv[3], newline='') as productsFile:  
    reader = csv.reader(productsFile)
    reader.__next__()
    for (id,name,cost) in reader:
        products += [(id,name,cost)]

print(customers)
print(orders)
print(products)