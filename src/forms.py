from wtforms import Form, validators
from wtforms import StringField, IntegerField, SubmitField, RadioField, BooleanField

class PedidoForm(Form):
    nombre = StringField("Nombre", [
        validators.DataRequired(message="El campo es requerido")])
    direccion = StringField("Direccion", [
        validators.DataRequired(message="El campo es requerido")])
    telefono = StringField("Telefono", [
        validators.DataRequired(message="El campo es requerido")])
    tamano = RadioField("Tamaño", [validators.DataRequired(message="El campo es requerido")],
                         choices=['Chica $40', 'Mediana $80', 'Grande $120'],)
    jamon = BooleanField("Jamon $10")
    pina = BooleanField("Piña $10")
    champinones = BooleanField("Champiñones $10")
    noPizzas = IntegerField("Num. de Pizzas", [
        validators.DataRequired(message="El campo es requerido")])
    