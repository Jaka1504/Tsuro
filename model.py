from dataclasses import dataclass
from typing import Dict, List
import random



VELIKOST_TABELE = (6, 6)    # 6×6 tabela

# Opombe zase:
#
#   Številčenje položajev na karti oz polju:
#       5   4
#   ----+---+----
#   |           |
# 6 +           + 3
#   |           |
# 7 +           + 2
#   |           |
#   ----+---+----
#       0   1



@dataclass 
class Uporabnik:
    uporabnisko_ime: str


@dataclass
class Karta:
    povezave: list

    def zarotiraj(self, st_rotacij=1):
        nove_povezave = self.povezave[:]
        for _ in range(st_rotacij):
            nove_povezave = [(num + 2) % 8 for num in nove_povezave]
            nove_povezave = nove_povezave[-2:] + nove_povezave[:-2]
        self.povezave = nove_povezave
        return self


@dataclass
class Igralec:
    uporabnik: Uporabnik
    barva: int          # barve bi bile kar 0, 1, 2, ...
    lokacija: tuple     # ((x, y), k) ... na ploščici s koordinatama x, y na položaju k
    karte_v_roki: List[Karta]


@dataclass
class Igra:
    id_igre: int
    igralci: List[Igralec]
    kupcek: List[Karta] = None
    tabela: Dict[tuple, Karta] = None


    def __post_init__(self):
        if self.tabela is None:
            self.tabela = {(x, y): None for x in range(VELIKOST_TABELE[0]) for y in range(VELIKOST_TABELE[1])}
        if self.kupcek is None:
            self.kupcek = []


    @staticmethod
    def razdeli_na_pare(seznam=[0, 1, 2, 3, 4, 5, 6, 7]):
        assert len(seznam) % 2 == 0 # more biti sodo mnogo, sicer se ne da
        if len(seznam) == 2:
            yield [seznam]
        else:
            for i in range(1, len(seznam)):
                nov_seznam = seznam[:]
                nov_seznam.pop(i)
                for pari in Igra.razdeli_na_pare(nov_seznam[1:]):
                    novi_pari = [[seznam[0], seznam[i]]]
                    novi_pari.extend(pari)
                    yield novi_pari

    @staticmethod
    def pari_v_povezave(seznam_parov):
        povezave = [None for _ in range(2 * len(seznam_parov))]
        for par in seznam_parov:
            povezave[par[0]] = par[1]
            povezave[par[1]] = par[0]
        return povezave

    # @staticmethod
    # def zarotiraj(povezave, k=1):
    #     nove_povezave = povezave[:]
    #     for _ in range(k):
    #         nove_povezave = [(num + 2) % 8 for num in nove_povezave]
    #         nove_povezave = nove_povezave[-2:] + nove_povezave[:-2]
    #     return nove_povezave

    @staticmethod
    def vse_karte():
        stare = []
        for seznam_parov in Igra.razdeli_na_pare():
            vrni = True
            povezave = Igra.pari_v_povezave(seznam_parov)
            karta = Karta(povezave)
            for _ in range(4):
                if karta in stare:
                    vrni = False
                karta.zarotiraj()
            if vrni:
                stare.append(povezave)
                yield Karta(povezave)


    def ustvari_nov_kupcek(self):
        self.kupcek = [karta.zarotiraj(st_rotacij=random.randint(0,3)) for karta in Igra.vse_karte()]
        random.shuffle(self.kupcek)


@dataclass
class Tsuro:
    igre: List[Igra]
    uporabniki: List[Uporabnik]



# Testni podatki:



uporabnik1 = Uporabnik("Jaka")
igralec1 = Igralec(uporabnik=uporabnik1, barva=3, lokacija=((0, 2), 7), karte_v_roki=[])
igra = Igra("prva igra", igralci=[igralec1])