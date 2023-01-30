#!/usr/bin/env python
import os
import reportes as rp
import csvOps as co
from flask import Flask, flash, request, render_template, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

def allowed_file(filename):
    return '.' in filename and filename.split('.')[1] == 'csv'

api = Flask(__name__)

api.config['SECRET_KEY'] = os.urandom(12).hex()
api.config["UPLOAD_FOLDER"] = os.path.abspath(os.path.join(os.getcwd(), 'input'))
#"/reportesApi/uploadFiles"
api.config["DOWNLOAD_FOLDER"] = os.path.abspath(os.path.join(os.getcwd(), 'output'))
#"/reportesApi/downloadFiles"
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

@api.route('/upload', methods=['GET', 'POST'])
def upload_files():
    if request.method == 'GET':
        return render_template('upload.html')
    
    for file in request.files:
        fileStorage = request.files[file]
    
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if fileStorage.filename == '':
            flash('No se ha seleccionado ningún archivo')
            return render_template('upload.html')
        
        if not allowed_file(fileStorage.filename):
            flash('Tiene que ser un archivo tipo CSV')
            return render_template('upload.html')

        secureFilename = secure_filename(fileStorage.filename)
        api.config["SECURE_NAMES"][file] = secureFilename
        
        fileStorage.save(os.path.join(api.config['UPLOAD_FOLDER'],
                                    secureFilename))
    
    return redirect(url_for('download_files'))

@api.route('/download')
def download_files():
    customers = co.leer(os.path.join(api.config["UPLOAD_FOLDER"], 
                        api.config["SECURE_NAMES"]["customers"]))
    orders = co.leer(os.path.join(api.config["UPLOAD_FOLDER"], 
                        api.config["SECURE_NAMES"]["orders"]))
    products = co.leer(os.path.join(api.config["UPLOAD_FOLDER"], 
                        api.config["SECURE_NAMES"]["products"]))

    order_prices = rp.report1(orders, products)
    product_customers = rp.report2(orders)
    customer_ranking = rp.report3(customers, orders, products)

    reportPaths = [os.path.join(api.config["DOWNLOAD_FOLDER"], 'order_prices.csv'),
                os.path.join(api.config["DOWNLOAD_FOLDER"], 'product_customers.csv'),
                os.path.join(api.config["DOWNLOAD_FOLDER"], 'customer_ranking.csv')]

    co.escribir(order_prices, ['id', 'total'], reportPaths[0])
    co.escribir(product_customers, ['id', 'customer_ids'], reportPaths[1])
    co.escribir(customer_ranking, ['id', 'name', 'lastname', 'total'], reportPaths[2])

    return render_template('download.html', files=os.listdir(api.config["DOWNLOAD_FOLDER"]))

@api.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(api.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == "__main__":
    #Usamos el puerto expuesto en el Dockerfile
    api.run(debug=True, port=5000, host='localhost')#os.environ['PORT']