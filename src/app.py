from flask import Flask, render_template, request, json, jsonify, make_response
import forms
from datetime import datetime

app = Flask(__name__)

@app.route('/pizzeria', methods=['GET', 'POST'])
def pizzeria():
    deshabilitarBtns = False
    form = forms.PedidoForm(request.form)

    pedidoActual_str = request.cookies.get("pedidoActual", '[]')
    pedidoActual = json.loads(pedidoActual_str)

    ventas_str = request.cookies.get("ventas", '[]')
    ventas = json.loads(ventas_str)

    if request.method == 'POST':
        if request.form.get("boton") == 'Quitar':
            pedidoActual.pop()

        elif request.form.get("boton") == 'Terminar':
            nombre = pedidoActual[-1]["nombre"]
            total = pedidoActual[-1]["total"]
            encontrado = False

            print(ventas)

            for i, venta in enumerate(ventas):
                if ventas[i]["nombre"] == nombre:
                    ventas[i]["total"] += total
                    encontrado = True

            if not encontrado:
                direccion = pedidoActual[-1]["direccion"]
                telefono = pedidoActual[-1]["telefono"]
                fecha = pedidoActual[-1]["fecha"]

                datosVentas = {'nombre': nombre,
                           'direccion': direccion,
                           'telefono': telefono,
                           'fecha': fecha,
                           'total': total}
                
                ventas.append(datosVentas)
            
            pedidoActual.clear()

        elif form.validate():   
            if request.form.get("boton") == 'Agregar':
                deshabilitarBtns = True

                total = 0

                ingredientesCant = 0
                ingredientes = ''

                if form.jamon.data:
                    ingredientes += 'Jamon '
                    ingredientesCant += 1
                if form.pina.data:
                    ingredientes += 'Piña '
                    ingredientesCant += 1
                if form.champinones.data:
                    ingredientes += 'Champiñones '
                    ingredientesCant += 1

                nombre = form.nombre.data
                direccion = form.direccion.data
                telefono = form.telefono.data
                fecha = datetime.today().strftime('%d-%m-%Y %H:%M:%S')
                tamano = form.tamano.data
                costo = int(tamano.split("$")[1]) + (ingredientesCant * 10)
                noPizzas = form.noPizzas.data
                subtotal = costo * int(noPizzas)
                total += subtotal

                datosPedido = {'nombre': nombre,
                        'direccion': direccion,
                        'telefono': telefono,
                        'fecha': fecha,
                        'tamano': tamano,
                        'ingredientes': ingredientes,
                        'noPizzas': noPizzas,
                        'subtotal': subtotal,
                        'total': total}

                pedidoActual.append(datosPedido)
    
    totalVentas = 0
    for venta in ventas:
        totalVentas += venta["total"]
    
    response = make_response(render_template('Pizzeria.html', 
                    form=form, pedidoActual=pedidoActual, 
                    deshabilitarBtns=deshabilitarBtns,
                    ventas=ventas,
                    total=totalVentas))
        
    if request.method != 'GET':
            response.set_cookie('pedidoActual', json.dumps(pedidoActual))
            response.set_cookie('ventas', json.dumps(ventas))

    return response

@app.route("/getPedido_cookie")
def getPedido_cookie():
     
    pedidoActual_str = request.cookies.get("pedidoActual")
    if not pedidoActual_str:
        return "No hay cookie guardada", 404
 
    pedidoActual = json.loads(pedidoActual_str)
 
    return jsonify(pedidoActual)

@app.route("/getVentas_cookie")
def getVentas_cookie():
     
    ventas_str = request.cookies.get("ventas")
    if not ventas_str:
        return "No hay cookie guardada", 404
 
    pedidoActual = json.loads(ventas_str)
 
    return jsonify(pedidoActual)

if __name__ == '__main__':
    app.run(debug=True)