import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
sns.set()


class Bono():
    def __init__(self, nominal, tasa, cupon, plazo, frecuencia):

        self.nominal = nominal
        self.tasa = (tasa / frecuencia) / 100
        self.cupon = (cupon / frecuencia) / 100
        self.plazo = plazo
        self.frecuencia = frecuencia
        self.descuento = 1 / (1 + self.tasa)
        self.precio = self.nominal * self.cupon * (1 - self.descuento ** (self.plazo * self.frecuencia))/(
            self.tasa) + self.nominal * (self.descuento ** (self.plazo * self.frecuencia))
        self.flujos = [
            self.nominal * self.cupon for i in range(1, self.plazo * self.frecuencia, 1)]
        self.flujos.append(self.nominal + self.nominal * self.cupon)

    def __str__(self):

        return "Características del bono:\n Valor nominal: ${}\n Tasa de interés: {}%\n Tasa cupón: {}%\n Plazo: {} años\n Frecuencia: {} veces al año\n Precio: ${}".format(self.nominal, round(self.tasa * 100), round(self.cupon * 100), self.plazo, self.frecuencia, round(self.precio, 2))

    def factor_duracion(self, t, tipo="mac"):

        if tipo not in ["mac", "mod"]:
            return "Tipo debe ser 'mac' ó 'mod'"

        if (t > self.plazo * self.frecuencia) or (t <= 0):
            return "t debe estar entre 1 y {}".format(self.frecuencia * self.plazo)

        if tipo == "mod":
            return (1 / (self.frecuencia * self.precio)) * (t * (self.descuento ** (t + 1)) * self.flujos[t - 1])

        return (1 / (self.frecuencia * self.precio)) * (t * (self.descuento ** t) * self.flujos[t - 1])

    def factor_convexidad(self, t, tipo="mac"):

        if tipo not in ["mac", "mod"]:
            return "Tipo debe ser 'mac' ó 'mod'"

        if (t > self.plazo * self.frecuencia) or (t <= 0):
            return "t debe estar entre 1 y {}".format(self.frecuencia * self.plazo)

        if tipo == "mod":
            return (1 / (self.precio * self.frecuencia ** 2)) * (t * (t+1) * self.descuento ** (t + 2) * (self.flujos[t - 1]))

        return (1 / (self.precio * self.frecuencia ** 2)) * ((t ** 2) * (self.descuento ** t) * (self.flujos[t - 1]))

    def duracion(self, tipo="mac"):

        duracion = 0

        for i in range(1, self.plazo * self.frecuencia + 1, 1):
            duracion += self.factor_duracion(i, tipo=tipo)

        return duracion

    def convexidad(self, tipo="mac"):

        convexidad = 0

        for i in range(1, self.plazo * self.frecuencia + 1, 1):
            convexidad += self.factor_convexidad(i, tipo=tipo)

        return convexidad

    def desgloce(self, tipo="mac"):
        tiempo = list(range(1, self.plazo * self.frecuencia + 1, 1))
        tiempo.insert(0, "totales")
        flujos = self.flujos.copy()
        flujos.insert(0, sum(flujos))
        flujos_vp = []
        duraciones = [self.duracion(tipo=tipo)]
        convexidades = [self.convexidad(tipo=tipo)]

        for i in range(1, self.plazo * self.frecuencia + 1, 1):
            flujos_vp.append(self.flujos[i - 1] * self.descuento ** i)
            duraciones.append(self.factor_duracion(i, tipo=tipo))
            convexidades.append(self.factor_convexidad(i, tipo=tipo))

        flujos_vp.insert(0, sum(flujos_vp))

        return pd.DataFrame({
            "Flujos": flujos,
            "VP": flujos_vp,
            "Dur": duraciones,
            "Conv": convexidades},
            index=tiempo
        )

    def graficar(self, limite=30):
        tasas = [i for i in range(1, limite, 1)]
        precios = []

        for tasa in tasas:
            precios.append(Bono(self.nominal, tasa, self.cupon,
                                self.plazo, self.frecuencia).precio)

        plt.plot(tasas, precios)
        plt.xlabel("Tasa de interés (%)")
        plt.ylabel("Precio")
        plt.show()
