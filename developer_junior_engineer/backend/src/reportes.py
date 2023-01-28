#!/usr/bin/env python
import sys
import csv
import numpy as np

#Comprobamos que se esten pasando los archivos csv
if len(sys.argv) < 4:
    print('Usage: %s <customers.csv> <orders.csv> <products.csv>' % sys.argv[0])

#Funcion que devuelve las filas leidas de un csv en forma de diccionario
#Return: 
#[
# {(colName:val)_1, ..., (colName:val)_cols}_1, 
# ... ,
# {(colName:val)_1, ..., (colName:val)_n}_rows
#]
def leerCSV(fileName):
    rowsList = []
    #Leemos los ficheros y almacenamos la informacion
    with open(fileName, newline='') as file:  
        reader = csv.DictReader(file)
        for row in reader: 
            rowsList += [row] 
    
    return rowsList

#Funcion que devuelve el total de cada pedido
#Return: 
#[
# {orderId, orderTotal}_1 , 
# ... , 
# {orderId, orderTotal}_numOrders
#]
def report1(orders, products):
    order_prices = []

    for row in orders:
        order_prices += [{
                        'id' : row['id'], 
                        'total' : sum(float(products[int(product)]['cost']) 
                            for product in row['products'].split(' '))
                        }]

    return order_prices

#Funcion que devuelve que clientes han comprado cada producto
#Return:
#[
# {productId, customer_ids}_1, 
# ... ,
# {productId, customer_ids}_numProducts
#]
def report2(orders):
    product_customers_aux = {}

    for row in orders:
        for product in row['products']:
            if product not in product_customers_aux: 
                product_customers_aux[product] = [row['customer']]
            elif row['customer'] not in product_customers_aux[product]:
                product_customers_aux[product] += [row['customer']]

    product_customers = []
    for productId in product_customers_aux:
        product_customers += [{
                            'id' : productId, 
                            'customer_ids' : ' '.join(product_customers_aux[productId])
                            }]

    return product_customers    

#Funcion que devuelve todos los pedidos de cada cliente ordenados en orden
#descendente por el total en euros
#Return:
#[
# {id, name, lastName, total}_1, 
# ... , 
# {id, name, lastName, total}_numClients
#]
def report3(customers, orders, products):
    customer_ranking_aux = {}

    for row in orders:
        total_pedido = sum(float(products[int(product)]['cost']) 
                        for product in row['products'].split(' '))
        
        if row['customer'] not in customer_ranking_aux: 
            customer_ranking_aux[row['customer']] = total_pedido
        else:
            customer_ranking_aux[row['customer']] += total_pedido

    sorted_customer_ranking_aux = sorted(customer_ranking_aux.items(),
                                        key=lambda x:x[1], reverse=True)

    customer_ranking = []
    for (customerId, totalPedido) in sorted_customer_ranking_aux:
        id = int(customerId)
        name, lastName = customers[id]['firstname'], customers[id]['lastname']
        customer_ranking += [{
                            'id' : customerId,
                            'name' : name,
                            'lastname' : lastName, 
                            'total' : totalPedido
                            }]

    return customer_ranking

customers = leerCSV(sys.argv[1])
orders = leerCSV(sys.argv[2])
products = leerCSV(sys.argv[3])

order_prices = report1(orders, products)
#print(order_prices)
product_customers = report2(orders)
#print(product_customers)
customer_ranking = report3(customers, orders, products)
#print(customer_ranking)
