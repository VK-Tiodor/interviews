#!/usr/bin/env python
import os
import reportes as rp
import csvOps as co
from flask import Flask, flash, request, render_template, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

def allowed_file(filename):
    return '.' in filename and filename.split('.')[1] == 'csv'

api = Flask(__name__)

#Variables de configuración de la api
api.config["SECRET_KEY"] = os.urandom(12).hex()
api.config["UPLOAD_FOLDER"] = "/reportesApi/uploadFiles"
api.config["DOWNLOAD_FOLDER"] = "/reportesApi/downloadFiles"
api.config["SECURE_NAMES"] = {}

#Si no existen las carpetas las creamos 
if not os.path.exists(api.config["UPLOAD_FOLDER"]): 
    os.makedirs(api.config["UPLOAD_FOLDER"])
if not os.path.exists(api.config["DOWNLOAD_FOLDER"]): 
    os.makedirs(api.config["DOWNLOAD_FOLDER"])

#Cargamos la página inicial
@api.route('/')
def init():
    return redirect(url_for('upload_files'))

#Subimos los archivos
@api.route('/upload', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'GET':
        return render_template('upload.html')
    
    for file in request.files:
        fileStorage = request.files[file]
    
        # Si el usuario no selecciona ningun archivo
        if fileStorage.filename == '':
            flash('No se ha seleccionado ningún archivo')
            return render_template('upload.html')
        
        # Si los archivos no son del tipo deseado
        if not allowed_file(fileStorage.filename):
            flash('Tiene que ser un archivo tipo CSV')
            return render_template('upload.html')

        #Nombre seguro, nunca fiarse del usuario
        secureFilename = secure_filename(fileStorage.filename)
        api.config["SECURE_NAMES"][file] = secureFilename
        
        #Guardamos
        fileStorage.save(os.path.join(api.config['UPLOAD_FOLDER'],
                                    secureFilename))
    
    return redirect(url_for('download_files'))

#Descargamos los reportes generados
@api.route('/download')
def download_files():
    #Leemos los CSV subidos
    customers = co.leer(os.path.join(api.config["UPLOAD_FOLDER"], 
                        api.config["SECURE_NAMES"]["customers"]))
    orders = co.leer(os.path.join(api.config["UPLOAD_FOLDER"], 
                        api.config["SECURE_NAMES"]["orders"]))
    products = co.leer(os.path.join(api.config["UPLOAD_FOLDER"], 
                        api.config["SECURE_NAMES"]["products"]))

    #Generamos los reportes
    order_prices = rp.report1(orders, products)
    product_customers = rp.report2(orders, products)
    customer_ranking = rp.report3(customers, orders, products)

    #Guardamos los reportes en la carpeta de descargas
    co.escribir(order_prices, ['id', 'total'], 
        os.path.join(api.config["DOWNLOAD_FOLDER"], 'order_prices.csv'))
    co.escribir(product_customers, ['id', 'customer_ids'], 
        os.path.join(api.config["DOWNLOAD_FOLDER"], 'product_customers.csv'))
    co.escribir(customer_ranking, ['id', 'name', 'lastname', 'total'],
        os.path.join(api.config["DOWNLOAD_FOLDER"], 'customer_ranking.csv'))

    return render_template('download.html', files=os.listdir(api.config["DOWNLOAD_FOLDER"]))

#Descargamos el fichero especificado
@api.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(api.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == "__main__":
    #Usamos el puerto expuesto en el Dockerfile
    api.run(debug=False, port=os.environ['PORT'], host='0.0.0.0')