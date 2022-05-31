from dataclasses import dataclass
from typing import Dict, List
from uuid import uuid4
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
        self.povezave = nove_povezave[:]
        return self

    def prikaz_povezav(self):
        prikaz = []
        obdelano = []
        for konec, izvor in enumerate(self.povezave):
            if not izvor in obdelano:
                if (konec - izvor) % 8 > 4 or konec - izvor == 4:
                    izvor, konec = konec, izvor
                prikaz.append((izvor % 2, (konec - izvor) % 8, (izvor - izvor % 2) // 2))
                obdelano.append(izvor)
                obdelano.append(konec)
        return prikaz


@dataclass
class Igralec:
    uporabnik: Uporabnik
    barva: int          # barve bi bile kar 0, 1, 2, ...
    polje: tuple        # (x, y) ... na ploščici s koordinatama x, y
    polozaj: int        # položaj na ploščici - int med 0 in 7
    karte_v_roki: List[Karta]


@dataclass
class Igra:
    id_igre: int
    igralci: List[Igralec] = None
    kupcek: List[Karta] = None
    tabela: Dict[tuple, Karta] = None
    na_vrsti: int = 0


    def __post_init__(self):
        if self.igralci is None:
            self.igralci = []
        if self.tabela is None:
            self.tabela = {(x, y): None for x in range(VELIKOST_TABELE[0] + 2) for y in range(VELIKOST_TABELE[1] + 2)}
        if self.kupcek is None:
            self.ustvari_nov_kupcek()


    def postavi_karto_na_tabelo(self, polje, karta):
        self.tabela[polje] = karta
    

    def poisci_pot_od_tocke(self, polje, polozaj):
        while not self.tabela[polje] is None:
            novo = Igra.napreduj_po_tabeli(polje, polozaj, self.tabela[polje].povezave)
            polje = novo["novo_polje"]
            polozaj = novo["nov_polozaj"]
        return (polje, polozaj)
    

    @staticmethod
    def napreduj_po_tabeli(staro_polje, star_polozaj, povezave_karte):
        st_vrstice, st_stolpca = staro_polje
        nov_polozaj = povezave_karte[star_polozaj]
        nov_polozaj = Igra.nasproten_polozaj(nov_polozaj)
        if nov_polozaj in [0, 1]:
            st_vrstice += -1
        elif nov_polozaj in [2, 3]:
            st_stolpca += -1
        elif nov_polozaj in [4, 5]:
            st_vrstice += 1
        else:
            st_stolpca += 1
        return {"novo_polje": (st_vrstice, st_stolpca),
                "nov_polozaj": nov_polozaj}
    
    @staticmethod
    def nasproten_polozaj(polozaj):
        return [5, 4, 7, 6, 1, 0, 3, 2][polozaj]


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
                stare.append(karta)
                yield karta


    def ustvari_nov_kupcek(self):
        self.kupcek = [karta.zarotiraj(st_rotacij=random.randint(0,3)) for karta in Igra.vse_karte()]
        random.shuffle(self.kupcek)


@dataclass
class Tsuro:
    igre: Dict[str, Igra] = None
    uporabniki: Dict[str, Uporabnik] = None

    def __post_init__(self):
        if self.igre is None:
            self.igre = {}
        if self. uporabniki is None:
            self.uporabniki = {}


    def dodaj_uporabnika(self, ime=None):
        if ime is None:
            ime = f"Uporabnik {len(self.uporabniki) + 1}"
        nov_uporabnik = Uporabnik(ime)
        self.uporabniki[ime] = nov_uporabnik
        return nov_uporabnik
    

    def ustvari_novo_igro(self, id_igre=None, igralci=None, kupcek=None, tabela=None, na_vrsti=0):
        if id_igre is None:
            id_igre = self.prost_id_igre()
        igra = Igra(id_igre, igralci, kupcek, tabela, na_vrsti)
        self.igre[id_igre] = igra
        return igra


    def prost_id_igre(self):
        while True:
            kandidat = uuid4().int
            if not kandidat in self.igre:
                return kandidat



# Testni podatki:


if __name__ == "__main__":
    uporabnik1 = Uporabnik("Jaka")
    igralec1 = Igralec(uporabnik=uporabnik1, barva=3, polje=(0, 2), polozaj=7, karte_v_roki=[])
    igra = Igra("prva igra", igralci=[igralec1])
    igra.ustvari_nov_kupcek()
    karta1 = igra.kupcek[0]
    karta2 = igra.kupcek[1]
    karta3 = igra.kupcek[2]
    for i in range(1, 4):
        igra.postavi_karto_na_tabelo(igra.kupcek[i - 1], (1, i))
