
from abc import ABC, abstractmethod
import csv

# === Abstrakcija + Polimorfizmas ===
class TransportoPriemone(ABC):
    def __init__(self, numeris, marke, metai):
        self._numeris = numeris  # Kapsuliacija
        self._marke = marke
        self._metai = metai

    @abstractmethod
    def gauti_info(self):
        pass

# === Paveldėjimas + Polimorfizmas ===
class Automobilis(TransportoPriemone):
    def __init__(self, numeris, marke, metai, durys):
        super().__init__(numeris, marke, metai)
        self._durys = durys

    def gauti_info(self):
        return f"Automobilis: {self._marke} ({self._metai}), numeris: {self._numeris}, durys: {self._durys}"

class Mikroautobusas(TransportoPriemone):
    def __init__(self, numeris, marke, metai, vietos):
        super().__init__(numeris, marke, metai)
        self._vietos = vietos

    def gauti_info(self):
        return f"Mikroautobusas: {self._marke} ({self._metai}), numeris: {self._numeris}, vietų skaičius: {self._vietos}"

# === Dizaino šablonas: Factory Method ===
class TransportoPriemoniuGamykla:
    @staticmethod
    def sukurti_transporto_priemone(tipas, **kwargs):
        if tipas == "automobilis":
            return Automobilis(**kwargs)
        elif tipas == "mikroautobusas":
            return Mikroautobusas(**kwargs)
        else:
            raise ValueError("Nežinomas transporto priemonės tipas.")

# === Agregacija: Klientas turi nuomos istoriją ===
class Klientas:
    def __init__(self, vardas):
        self.vardas = vardas
        self.nuomos = []

    def prideti_nuoma(self, transporto_priemone):
        self.nuomos.append(transporto_priemone)

    def parodyti_nuomas(self):
        for nuoma in self.nuomos:
            print(nuoma.gauti_info())

# === Skaitymas ir rašymas į CSV ===
def issaugoti_i_faila(klientai, failas):
    with open(failas, 'w', newline='') as f:
        writer = csv.writer(f)
        for klientas in klientai:
            for nuoma in klientas.nuomos:
                writer.writerow([klientas.vardas, nuoma.gauti_info()])

def nuskaityti_is_failo(failas):
    with open(failas, 'r') as f:
        reader = csv.reader(f)
        for eilute in reader:
            print(f"Įrašas: {eilute}")

# === Naudojimas ===
if __name__ == "__main__":
    gamykla = TransportoPriemoniuGamykla()
    masina1 = gamykla.sukurti_transporto_priemone("automobilis", numeris="ABC123", marke="Toyota", metai=2020, durys=4)
    masina2 = gamykla.sukurti_transporto_priemone("mikroautobusas", numeris="XYZ456", marke="Ford", metai=2018, vietos=8)

    klientas = Klientas("Jonas")
    klientas.prideti_nuoma(masina1)
    klientas.prideti_nuoma(masina2)

    klientas.parodyti_nuomas()

    klientai = [klientas]
    issaugoti_i_faila(klientai, "nuomos_duomenys.csv")
    nuskaityti_is_failo("nuomos_duomenys.csv")
