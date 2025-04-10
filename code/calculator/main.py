from division import division
from multiplicacion import multiplicacion
from resta import resta
from suma import suma

def calcular(num1, num2, operador):
    match operador:
        case "+":
            return suma(num1, num2)
        case "-":
            return resta(num1, num2)
        case "*":
            return multiplicacion(num1, num2)
        case "/":
            return division(num1, num2)

def obtener_numero(mensaje):
    while True:
        try:
            return float(input(mensaje))
        except ValueError:
            print("Entrada inválida. Por favor, ingresa un número.")

def obtener_operador(mensaje):
    operadores_validos = {"+", "-", "*", "/"}
    while True:
        operador = input(mensaje)
        if operador in operadores_validos:
            return operador
        else:
            print("Operador inválido. Por favor, ingresa un operador válido.")

if __name__ == "__main__":
    print("Bienvenido a la calculadora del Grupo 35")
    print("Para operar vamos a solicitar que ingreses dos números y un operador")
    num1 = obtener_numero("Primer número: ")
    operador = obtener_operador("Operador (+, -, *, /): ")
    num2 = obtener_numero("Segundo número: ")
    resultado = calcular(num1, num2, operador)
    if resultado is not None:
        print(f"El resultado es {resultado}")