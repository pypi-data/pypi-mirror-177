#!usr\bin\python

''' este modulo se llama primos
 como su nombre lo dice se trata de un modulo que generara numeros primos y que contara con varias funciones 
 desde comprobar si un numero es primo como devolver una cierta cantidad de numeros primos '''
from math import sqrt
from time import time


class Primos:

    def __init__(self):

        self.count = 0

    # comprueba si el argumento pasado a number es o no un numero primo          si es devuelve True else False .

    def isprimo(self, number):

        rango = int(sqrt(number)) + 1

        for i in range(2, rango):

            if number % i == 0:

                return False

        return True

    # devuelve los numeros primos que estan en el rango de los argumentos entre el parametro star y stop             si stop > start devuelve 0

    def rangePrimos(self, start, stop):

        if stop < start:

            return 0

        for i in range(start, stop+1):

            if self.isprimo(i):

                yield i

    # devuelve la cantidad de8 numeros primos que se le pase al parametro cant .

    def cantidadPrimos(self, desde, cant):

        count = 0
        num = desde

        while count < cant:

            if self.isprimo(num):

                count += 1
                yield num

            num += 1

    # este metodo recibe como argumento un numero no Primo y devuelve su descomposicion en factores primos en una lista ; pero si el numero es primo retorna el mismo numero .

    def factoresPrimos(self, num):

        if self.isprimo(num):

            return [num]

        copia = num
        primo = 2

        n = primo

        print(" ->>  ", end="")

        while num != 1:

            if self.isprimo(num):
                print(num, end=" = ")
                break

            while (num % primo) == 0:

                num = num//primo

                print(f"{primo}", end="x" if num != 1 else " = ")

            else:

                primos = self.cantidadPrimos(n+1, 1)

                primo = next(primos)
                n = primo

        print(copia)
