def division(num1,num2):
    try:
        res = num1/num2
    except ZeroDivisionError:
        print("No se puede dividir por cero.")
        return None
    return res