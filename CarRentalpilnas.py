
from abc import ABC, abstractmethod
from datetime import datetime
import csv

# === Abstrakcija + Polimorfizmas ===
class TransportoPriemone(ABC):
    def __init__(self, numeris, marke, metai, is_nuomota=True):
        self._numeris = numeris
        self._marke = marke
        self._metai = metai
        self._is_nuomota = is_nuomota

    def ar_isnuomota(self):
        return "Taip" if self._is_nuomota else "Ne"

    @abstractmethod
    def gauti_info(self):
        pass

class Automobilis(TransportoPriemone):
    def __init__(self, numeris, marke, metai, durys, is_nuomota=True):
        super().__init__(numeris, marke, metai, is_nuomota)
        self._durys = durys

    def gauti_info(self):
        return f"Automobilis: {self._marke} ({self._metai}), numeris: {self._numeris}, durys: {self._durys}"

class Mikroautobusas(TransportoPriemone):
    def __init__(self, numeris, marke, metai, vietos, is_nuomota=True):
        super().__init__(numeris, marke, metai, is_nuomota)
        self._vietos = vietos

    def gauti_info(self):
        return f"Mikroautobusas: {self._marke} ({self._metai}), numeris: {self._numeris}, vietų skaičius: {self._vietos}"

class TransportoPriemoniuGamykla:
    @staticmethod
    def sukurti_transporto_priemone(tipas, **kwargs):
        if tipas == "automobilis":
            return Automobilis(**kwargs)
        elif tipas == "mikroautobusas":
            return Mikroautobusas(**kwargs)
        else:
            raise ValueError("Nežinomas transporto priemonės tipas.")

class Klientas:
    def __init__(self, vardas):
        self.vardas = vardas
        self.nuomos = []

    def prideti_nuoma(self, transporto_priemone):
        self.nuomos.append(transporto_priemone)

    def parodyti_nuomas(self):
        for nuoma in self.nuomos:
            print(nuoma.gauti_info(), "| Išnuomota:", nuoma.ar_isnuomota())

def issaugoti_i_faila(klientai, failas):
    with open(failas, 'w', newline='') as f:
        writer = csv.writer(f)
        for klientas in klientai:
            for nuoma in klientas.nuomos:
                if isinstance(nuoma, Automobilis):
                    writer.writerow([
                        klientas.vardas, "Automobilis", nuoma._marke, nuoma._numeris,
                        nuoma._metai, nuoma._durys, nuoma.ar_isnuomota(), str(datetime.today().date())
                    ])
                elif isinstance(nuoma, Mikroautobusas):
                    writer.writerow([
                        klientas.vardas, "Mikroautobusas", nuoma._marke, nuoma._numeris,
                        nuoma._metai, nuoma._vietos, nuoma.ar_isnuomota(), str(datetime.today().date())
                    ])

def nuskaityti_is_failo(failas):
    with open(failas, 'r') as f:
        reader = csv.reader(f)
        for eilute in reader:
            print(f"Įrašas: Klientas: {eilute[0]}, Tipas: {eilute[1]}, Marke: {eilute[2]}, "
                  f"Numeris: {eilute[3]}, Būsena: {eilute[6]}, Data: {eilute[7]}")

# Nauja funkcija: atkuriami objektai is CSV
def importuoti_klientus_is_csv(failas):
    klientai_dict = {}
    with open(failas, 'r') as f:
        reader = csv.reader(f)
        for eilute in reader:
            vardas, tipas, marke, numeris, metai, spec, is_nuomota_str, data = eilute
            is_nuomota = True if is_nuomota_str == "Taip" else False
            metai = int(metai)
            spec = int(spec)

            if tipas == "Automobilis":
                transportas = Automobilis(numeris, marke, metai, spec, is_nuomota)
            elif tipas == "Mikroautobusas":
                transportas = Mikroautobusas(numeris, marke, metai, spec, is_nuomota)

            if vardas not in klientai_dict:
                klientai_dict[vardas] = Klientas(vardas)

            klientai_dict[vardas].prideti_nuoma(transportas)
    return list(klientai_dict.values())

# === Naudojimas ===
if __name__ == "__main__":
    gamykla = TransportoPriemoniuGamykla()
    masina1 = gamykla.sukurti_transporto_priemone(
        "automobilis", numeris="ABC123", marke="Toyota", metai=2020, durys=4, is_nuomota=True)
    masina2 = gamykla.sukurti_transporto_priemone(
        "mikroautobusas", numeris="XYZ456", marke="Ford", metai=2018, vietos=8, is_nuomota=False)

    klientas = Klientas("Jonas")
    klientas.prideti_nuoma(masina1)
    klientas.prideti_nuoma(masina2)

    klientai = [klientas]
    issaugoti_i_faila(klientai, "nuomos_duomenys.csv")

    print("\n== Duomenys iš failo ==")
    nuskaityti_is_failo("nuomos_duomenys.csv")

    print("\n== Atkurtos nuomos ==")
    atkurti_klientai = importuoti_klientus_is_csv("nuomos_duomenys.csv")
    for k in atkurti_klientai:
        print(f"Klientas: {k.vardas}")
        k.parodyti_nuomas()
