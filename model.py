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
    kupcek: List[Karta]
    tabela: Dict[tuple, Karta] = None


    def __post_init__(self):
        if self.tabela is None:
            self.tabela = {(x, y): None for x in range(VELIKOST_TABELE[0]) for y in range(VELIKOST_TABELE[1])}

    def ustvari_nov_kupcek(self):
        pass


@dataclass
class Tsuro:
    igre: List[Igra]
    uporabniki: List[Uporabnik]


def razdeli_na_pare(seznam=[0, 1, 2, 3, 4, 5, 6, 7]):
    assert len(seznam) % 2 == 0 # more biti sodo mnogo, sicer se ne da
    if len(seznam) == 2:
        yield [seznam]
    else:
        for i in range(1, len(seznam)):
            nov_seznam = seznam[:]
            nov_seznam.pop(i)
            for pari in razdeli_na_pare(nov_seznam[1:]):
                novi_pari = [[seznam[0], seznam[i]]]
                novi_pari.extend(pari)
                yield novi_pari


def pari_v_povezave(seznam_parov):
    povezave = [None for _ in range(2 * len(seznam_parov))]
    for par in seznam_parov:
        povezave[par[0]] = par[1]
        povezave[par[1]] = par[0]
    return povezave


def zarotiraj(povezave, k=1):
    nove_povezave = povezave[:]
    for _ in range(k):
        nove_povezave = [(num + 2) % 8 for num in nove_povezave]
        nove_povezave = nove_povezave[-2:] + nove_povezave[:-2]
    return nove_povezave


def vse_karte():
    stare = []
    for seznam_parov in razdeli_na_pare():
        vrni = True
        povezave = pari_v_povezave(seznam_parov)
        for rotacija in range(1, 4):
            if zarotiraj(povezave, rotacija) in stare:
                vrni = False
        if vrni:
            stare.append(povezave)
            yield povezave


# Testni podatki:

deck = [zarotiraj(karta, random.randint(0,3)) for karta in vse_karte()]
random.shuffle(deck)

uporabnik1 = Uporabnik("Jaka")

igralec1 = Igralec(uporabnik=uporabnik1, barva=3, lokacija=((0, 2), 7), karte_v_roki=[])



for i, karta in enumerate(deck):
    print(f"{i} --> {karta}")