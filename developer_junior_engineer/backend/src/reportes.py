'''
Funcion que devuelve el total de cada pedido
Return: 
[
 {orderId, orderTotal}_1 , 
 ... , 
 {orderId, orderTotal}_numOrders
]
'''
def report1(orders, products):
    order_prices = []

    for row in orders:
        order_prices += [{
                        'id' : row['id'], 
                        'total' : sum(float(products[int(product)]['cost']) 
                            for product in row['products'].split(' '))
                        }]

    return order_prices
'''
Funcion que devuelve que clientes han comprado cada producto
Return:
[
 {productId, customer_ids}_1, 
 ... ,
 {productId, customer_ids}_numProducts
]
'''
def report2(orders, products):
    product_customers_aux = {}

    #Los productos que han sido comprados
    for row in orders:
        for product in row['products'].split(' '):
            if product not in product_customers_aux: 
                product_customers_aux[product] = [row['customer']]
            elif row['customer'] not in product_customers_aux[product]:
                product_customers_aux[product] += [row['customer']]

    #Los productos que no han sido comprados
    for row in products:
        if row['id'] not in product_customers_aux:
            product_customers_aux[row['id']] = []

    #Ordenamos, paso innecesario, pero se ve mejor para el usuario
    sorted_product_customers_aux = sorted(product_customers_aux.items())

    product_customers = []
    for (productId, customerIds) in sorted_product_customers_aux:
        product_customers += [{
                            'id' : productId, 
                            'customer_ids' : ' '.join(customerIds)
                            }]

    return product_customers    

'''
Funcion que devuelve todos los pedidos de cada cliente ordenados en orden
descendente por el total en euros
Return:
[
 {id, name, lastName, total}_1, 
 ... , 
 {id, name, lastName, total}_numClients
]
'''
def report3(customers, orders, products):
    customer_ranking_aux = {}

    #Clientes que han hecho pedidos
    for row in orders:
        total_pedido = sum(float(products[int(product)]['cost']) 
                        for product in row['products'].split(' '))
        
        if row['customer'] not in customer_ranking_aux: 
            customer_ranking_aux[row['customer']] = total_pedido
        else:
            customer_ranking_aux[row['customer']] += total_pedido

    #Clientes que no han comprado
    for row in customers:
        if row['id'] not in customer_ranking_aux:
            customer_ranking_aux[row['id']] = 0

    #Ordenamos por total descendentemente
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
