from dataclasses import dataclass
from typing import Dict, List
from uuid import uuid4
import random



VELIKOST_TABELE = (6, 6)    # 6×6 tabela
LOOP = "L"
# Barve za v css:
RDECA = 0
ORANZNA = 67
RUMENA = 70
ZELENA = 80
AQUA = 180
MODRA = 234
VIJOLICNA = 255.5
ROZA = 330
BELA = "bela"
SIVA = "siva"
VRSTNI_RED_BARV = [RDECA, ZELENA, MODRA, RUMENA, AQUA, ROZA, VIJOLICNA, ORANZNA]

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
    barve: Dict[int, list] = None


    def __post_init__(self):
        if self.barve is None:
            self.barve = {i: BELA for i in range(8)}


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
                prikaz.append((izvor % 2, (konec - izvor) % 8, (izvor - izvor % 2) // 2, self.barve[izvor]))
                obdelano.append(izvor)
                obdelano.append(konec)
        return prikaz


@dataclass
class Igralec:
    uporabnik: Uporabnik
    # st_igralca: int     # barve bi bile kar 0, 1, 2, ...
    polje: tuple = None        # (vrstica, stolpec) polje tabele v tej vrstici in stolpcu
    polozaj: int = None        # položaj na ploščici - int med 0 in 7
    karte_v_roki: List[Karta] = None


    def __post_init__(self):
        if self.karte_v_roki is None:
            self.karte_v_roki = []


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


    def ustvari_nov_kupcek(self):
        self.kupcek = [karta.zarotiraj(st_rotacij=random.randint(0,3)) for karta in Igra.vse_karte()]
        random.shuffle(self.kupcek)


    def dodaj_novega_igralca(self, uporabnik):
        nov_igralec = Igralec(uporabnik)
        slaba_pozicija = True
        while slaba_pozicija:
            zacetno_polje, zacetni_polozaj = random.choice([pozicija for pozicija in Igra.robne_pozicije()])
            slaba_pozicija = False
            for igralec in self. igralci:
                if igralec.polje == zacetno_polje and igralec.polozaj == zacetni_polozaj:
                    slaba_pozicija = True
        nov_igralec.polje, nov_igralec.polozaj = zacetno_polje, zacetni_polozaj
        self.igralci.append(nov_igralec)
        return len(self.igralci) - 1                   # indeks novega igralca


    def igralec_postavi_karto_na_tabelo(self, st_igralca, st_karte, polje):
        igralec = self.igralci[st_igralca]
        karta = igralec.karte_v_roki.pop(st_karte)
        self.postavi_karto_na_tabelo(polje, karta)
        self.vleci_karto(igralec)


    def vleci_karto(self, st_igralca):
        try:
            zgornja_karta = self.kupcek.pop()       # ce je prazen kupcek ne naredi nicesar
            self.igralci[st_igralca].karte_v_roki.append(zgornja_karta)
        except IndexError:
            pass
    

    def razdeli_karte(self):
        for _ in range(3):
            for st_igralca in range(len(self.igralci)):
                self.vleci_karto(st_igralca)


    def poisci_pot_od_tocke(self, polje, polozaj):
        zacetno_polje, zaceten_polozaj = polje, polozaj
        while not self.tabela[polje] is None:
            novo = self.napreduj_po_tabeli(polje, polozaj)
            polje = novo[0]
            polozaj = novo[1]
            if polje == zacetno_polje and polozaj == zaceten_polozaj:
                return LOOP
        return (polje, polozaj)


    def postavi_karto_na_tabelo(self, polje, karta):
        self.tabela[polje] = karta

    
    def barvaj_povezave_od_tocke(self, polje, polozaj, barva):
        while not self.tabela[polje] is None:
            karta = self.tabela[polje]
            karta.barve[polozaj] = barva
            karta.barve[karta.povezave[polozaj]] = barva
            polje, polozaj = self.napreduj_po_tabeli(polje, polozaj)


    def primerno_pobarvaj_poti(self):
        for polje, polozaj in Igra.robne_pozicije():
            self.barvaj_povezave_od_tocke(polje, polozaj, SIVA)
        for indeks in range(len(self.igralci)):
            # polje, polozaj = Igra.obrni_se_na_mestu(self.igralci[indeks].polje, self.igralci[indeks].polozaj)
            polje, polozaj = self.igralci[indeks].polje, self.igralci[indeks].polozaj
            barva = VRSTNI_RED_BARV[indeks]
            self.barvaj_povezave_od_tocke(polje, polozaj, barva)



    def napreduj_po_tabeli(self, staro_polje, star_polozaj):
        nov_polozaj = self.tabela[staro_polje].povezave[star_polozaj]
        return (Igra.obrni_se_na_mestu(staro_polje, nov_polozaj))


    @staticmethod
    def robne_pozicije():
        for i in range(1, VELIKOST_TABELE[0] + 1):
            yield ((i, 1), 6)
            yield ((i, 1), 7)
        for j in range(1, VELIKOST_TABELE[1] + 1):
            yield ((VELIKOST_TABELE[0], j), 0)
            yield ((VELIKOST_TABELE[0], j), 1)
        for i in range(VELIKOST_TABELE[0], 0, -1):
            yield ((i, VELIKOST_TABELE[1]), 2)
            yield ((i, VELIKOST_TABELE[1]), 3)
        for j in range(VELIKOST_TABELE[1], 0, -1):
            yield ((1, j), 4)
            yield ((1, j), 5)


    @staticmethod
    def nasproten_polozaj(polozaj):
        return [5, 4, 7, 6, 1, 0, 3, 2][polozaj]

    
    @staticmethod
    def obrni_se_na_mestu(polje, polozaj):
        st_vrstice, st_stolpca = polje
        polozaj = Igra.nasproten_polozaj(polozaj)
        if polozaj in [0, 1]:
            st_vrstice += -1
        elif polozaj in [2, 3]:
            st_stolpca += -1
        elif polozaj in [4, 5]:
            st_vrstice += 1
        else:
            st_stolpca += 1
        return ((st_vrstice, st_stolpca), polozaj)


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
    igralec1 = Igralec(uporabnik=uporabnik1, polje=(0, 2), polozaj=7, karte_v_roki=[])
    igra = Igra("prva igra", igralci=[igralec1])
    igra.ustvari_nov_kupcek()
    karta1 = igra.kupcek[0]
    karta2 = igra.kupcek[1]
    karta3 = igra.kupcek[2]
    for i in range(1, 4):
        igra.postavi_karto_na_tabelo((1, i), igra.kupcek[i - 1])
