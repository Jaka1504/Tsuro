from dataclasses import dataclass
from typing import Dict, List
from copy import deepcopy
from datetime import datetime
import random, json


NEDOKONCANA = "ND"
NI_ZMAGOVALCA = "NZ"
LOOP = "L"
# Barve za v css, hue-rotate glede na rdečo:
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
VRSTNI_RED_BARV = [ZELENA, RDECA, MODRA, RUMENA, AQUA, ROZA, VIJOLICNA, ORANZNA]


#
#   Terminologija, uporabljena v kodi:
#       - Polje: par dveh celih števil (i, j), predstavlja kvadratek v i-ti
#         vrstici in j-tem stolpcu tabele
#       - Položaj: celo število iz {0, 1, ..., 7}, ki pove, kje na robu polja
#         se nahaja igralec
#       - Pozicija: polje in položaj skupaj
#       - Povezava: na karti narisana črta, ki povezuje dva različna položaja
#         na nekem polju
#       - Pot: Zaporedne povezave, pri katerih se konec prejšnje ujema z
#         začetkom naslednje
#       - Mrtva pot: pot, vsaj eno krajišče katere vodi na rob tabele
#
#   Opombe:
#       - Številčenje položajev na karti oz polju:
#                  5     4
#              ----+-----+----
#              |             |
#            6 +             + 3
#              |             |
#            7 +             + 2
#              |             |
#              ----+-----+----
#                  0     1
#       - Igralec se nahaja na poju, do roba katerega je ravno prišel, torej
#         na tistem polju, kamor bi postavil karto. Tako pozicija določa tudi
#         "usmerjenost" igralca
#       - Polja tabele, na katerih poteka igra se zacnejo stevilciti z 1, za
#         enostavnejšo kodo je vrstica 0 vselej prazna. Če igralec pride na polje
#         v vrstici 0, je padel iz tabele. Podobno velja za stolpec 0 in zadnjo
#         vrstico ter stolpec.
#


@dataclass
class Karta:
    povezave: list
    barve: Dict[int, list] = None

    def __post_init__(self):
        if self.barve is None:
            self.barve = {i: BELA for i in range(8)}

    def v_slovar(self):
        """Vrne slovar z ustreznimi podatki."""
        return {"povezave": self.povezave, "barve": self.barve}

    @classmethod
    def iz_slovarja(cls, slovar):
        """Ustvari in vrne objekt s podatki iz slovarja."""
        return Karta(
            povezave=slovar["povezave"],
            barve={int(i): slovar["barve"][i] for i in slovar["barve"]},
        )

    def zarotiraj(self, st_rotacij=1):
        """Karto zarotira `st_rotacij`-krat in jo vrne."""
        nove_povezave = self.povezave[:]
        for _ in range(st_rotacij):
            nove_povezave = [(polozaj + 2) % 8 for polozaj in nove_povezave]
            nove_povezave = nove_povezave[-2:] + nove_povezave[:-2]
        self.povezave = nove_povezave[:]
        return self

    def prikaz_povezav(self):
        """Vrne seznam četveric, ki kodirajo prikaz povezav."""
        prikaz = []
        obdelano = []
        for konec, izvor in enumerate(self.povezave):
            if not izvor in obdelano:
                if (konec - izvor) % 8 > 4 or konec - izvor == 4:
                    izvor, konec = konec, izvor
                prikaz.append(
                    (
                        # če je kot bi izhajala iz položaja 0 ali 1 po nekaj rotacijah
                        izvor % 2,
                        # dolžina povezave - koliko položajev naprej v pozitivni smeri vodi
                        (konec - izvor) % 8,
                        # število rotacij da pride izvor na 0 ali 1
                        (izvor - izvor % 2) // 2,
                        # barva povezave
                        self.barve[izvor],
                    )
                )
                obdelano.append(izvor)
                obdelano.append(konec)
        return prikaz


@dataclass
class Igralec:
    ime: str = None
    polje: tuple = None  # (vrstica, stolpec) polje tabele v tej vrstici in stolpcu
    polozaj: int = None  # položaj na ploščici - int med 0 in 7 - glej sliko na vrhu
    karte_v_roki: List[Karta] = None
    v_igri: bool = True  # postane False ko je igralec izločen
    je_bot: bool = False  # True če s tem igralcem upravlja racunalnik

    def __post_init__(self):
        if self.karte_v_roki is None:
            self.karte_v_roki = []

    def v_slovar(self):
        """Vrne slovar z ustreznimi podatki."""
        return {
            "ime": self.ime,
            "polje": self.polje,
            "polozaj": self.polozaj,
            "karte_v_roki": [karta.v_slovar() for karta in self.karte_v_roki],
            "v_igri": self.v_igri,
            "je_bot": self.je_bot,
        }

    @classmethod
    def iz_slovarja(cls, slovar):
        """Ustvari in vrne objekt s podatki iz slovarja."""
        return Igralec(
            ime=slovar["ime"],
            polje=tuple(slovar["polje"]),
            polozaj=slovar["polozaj"],
            karte_v_roki=[Karta.iz_slovarja(karta) for karta in slovar["karte_v_roki"]],
            v_igri=slovar["v_igri"],
            je_bot=slovar["je_bot"],
        )


@dataclass
class Igra:
    id_igre: int
    cas: datetime = None
    igralci: List[Igralec] = None
    velikost_tabele: tuple = (6, 6)
    kupcek: List[Karta] = None
    tabela: Dict[tuple, Karta] = None
    na_vrsti: int = 0

    def __post_init__(self):
        if self.cas is None:
            self.cas = datetime.now()
        if self.igralci is None:
            self.igralci = []
        if self.tabela is None:
            self.tabela = {
                (x, y): None
                for x in range(self.velikost_tabele[0] + 2)
                for y in range(self.velikost_tabele[1] + 2)
            }
        if self.kupcek is None:
            self.ustvari_nov_kupcek()

    def v_slovar(self):
        """Vrne slovar z ustreznimi podatki."""
        seznam_tabele = []
        for vrstica in range(self.velikost_tabele[0] + 2):
            seznam_vrstice = []
            for stolpec in range(self.velikost_tabele[1] + 2):
                if self.tabela[(vrstica, stolpec)] is None:
                    seznam_vrstice.append(None)
                else:
                    seznam_vrstice.append(self.tabela[(vrstica, stolpec)].v_slovar())
            seznam_tabele.append(seznam_vrstice)
        return {
            "id_igre": self.id_igre,
            "cas": {
                "leto": self.cas.year,
                "mesec": self.cas.month,
                "dan": self.cas.day,
                "ura": self.cas.hour,
                "minuta": self.cas.minute,
                "sekunda": self.cas.second,
            },
            "igralci": [igralec.v_slovar() for igralec in self.igralci],
            "velikost_tabele": self.velikost_tabele,
            "kupcek": [karta.v_slovar() for karta in self.kupcek],
            "tabela": seznam_tabele,
            "na_vrsti": self.na_vrsti,
        }

    @classmethod
    def iz_slovarja(cls, slovar):
        """Ustvari in vrne objekt s podatki iz slovarja."""
        slovar_tabele = {}
        for vrstica in range(slovar["velikost_tabele"][0] + 2):
            for stolpec in range(slovar["velikost_tabele"][1] + 2):
                karta = slovar["tabela"][vrstica][stolpec]
                if karta is None:
                    slovar_tabele[(vrstica, stolpec)] = None
                else:
                    slovar_tabele[(vrstica, stolpec)] = Karta.iz_slovarja(karta)
        return Igra(
            id_igre=slovar["id_igre"],
            cas=datetime(
                year=slovar["cas"]["leto"],
                month=slovar["cas"]["mesec"],
                day=slovar["cas"]["dan"],
                hour=slovar["cas"]["ura"],
                minute=slovar["cas"]["minuta"],
                second=slovar["cas"]["sekunda"],
            ),
            igralci=[Igralec.iz_slovarja(igralec) for igralec in slovar["igralci"]],
            velikost_tabele=tuple(slovar["velikost_tabele"]),
            kupcek=[Karta.iz_slovarja(karta) for karta in slovar["kupcek"]],
            tabela=slovar_tabele,
            na_vrsti=slovar["na_vrsti"],
        )

    def ustvari_nov_kupcek(self):
        """Ustvari nov premešan kupček iz vseh 35 možnih kart."""
        self.kupcek = [
            karta.zarotiraj(st_rotacij=random.randint(0, 3))
            for karta in Igra.vse_karte()
        ]
        random.shuffle(self.kupcek)

    def dodaj_novega_igralca(self, ime=None, je_bot=False):
        """Doda v igro novega igralca z imenom `ime` in ga postavi na naključno
        prosto pozicijo na robu tabele. Vrne indeks igralca."""
        nov_igralec = Igralec(ime=ime, je_bot=je_bot)
        slaba_pozicija = True
        while slaba_pozicija:
            zacetno_polje, zacetni_polozaj = random.choice(
                [pozicija for pozicija in self.robne_pozicije()]
            )
            slaba_pozicija = False
            for igralec in self.igralci:
                if (
                    igralec.polje == zacetno_polje
                    and igralec.polozaj == zacetni_polozaj
                ):
                    slaba_pozicija = True
        nov_igralec.polje, nov_igralec.polozaj = zacetno_polje, zacetni_polozaj
        self.igralci.append(nov_igralec)
        return len(self.igralci) - 1  # indeks novega igralca

    def igralec_postavi_karto_na_tabelo(self, st_karte, polje=None):
        """Vzame karto z indeksom `st_karte` iz roke igralca, ki je na potezi,
        jo postavi na polje `polje` (če ni podano, pred njim), povleče novo
        karto iz kupčka."""
        st_igralca = self.na_vrsti
        igralec = self.igralci[st_igralca]
        if polje is None:
            polje = igralec.polje
        karta = igralec.karte_v_roki.pop(st_karte)
        self.postavi_karto_na_tabelo(polje, karta)
        self.vleci_karto(st_igralca)
        for indeks in (
            list(range(len(self.igralci)))[self.na_vrsti :]
            + list(range(len(self.igralci)))[: self.na_vrsti]
        ):
            self.napreduj_po_tabeli(indeks)
        self.primerno_pobarvaj_poti()
        self.predaj_potezo()

    def predaj_potezo(self):
        """Preda potezo prvemu naslednjemu igralcu, ki je še v igri.
        Če je ta igralec bot, izvede njegovo potezo in se pokliče
        ponovno."""
        st_igralcev_v_igri = len(
            [igralec_ for igralec_ in self.igralci if igralec_.v_igri]
        )
        if st_igralcev_v_igri > 1:
            while True:
                self.na_vrsti = (self.na_vrsti + 1) % len(self.igralci)
                if self.igralci[self.na_vrsti].v_igri:
                    # Poskusi narediti botovo potezo
                    self.botova_poteza()
                    break

    def botova_poteza(self):
        """Izbere, katero karto naj igra bot, in jo postavi ter preda
        potezo."""
        igralec = self.igralci[self.na_vrsti]
        aktivni_igralci = [
            aktivni_igralec
            for aktivni_igralec in self.igralci
            if aktivni_igralec.v_igri
        ]
        if igralec.je_bot:
            tockovane_moznosti = {}
            for st_karte in range(3):
                for st_rotacij in range(4):
                    hipoteticna_igra = deepcopy(self)
                    bot = hipoteticna_igra.igralci[hipoteticna_igra.na_vrsti]
                    bot.karte_v_roki[st_karte].zarotiraj(st_rotacij=st_rotacij)
                    hipoteticna_igra.postavi_karto_na_tabelo(
                        bot.polje, bot.karte_v_roki[st_karte]
                    )
                    for indeks in range(len(hipoteticna_igra.igralci)):
                        hipoteticna_igra.napreduj_po_tabeli(indeks)
                    tockovane_moznosti[
                        (st_karte, st_rotacij)
                    ] = hipoteticna_igra.tockuj_polozaj_bota(len(aktivni_igralci))
            izbrana_karta, izbrana_rotacija = max(
                tockovane_moznosti, key=tockovane_moznosti.get
            )
            igralec.karte_v_roki[izbrana_karta].zarotiraj(izbrana_rotacija)
            self.igralec_postavi_karto_na_tabelo(izbrana_karta)

    def tockuj_polozaj_bota(self, st_igralcev_pred_potezo):
        """Dodeli situaciji vrednost iz intervala (0, 1), tako da višja vrednost
        ustreza boljšim razmeram za igralca na potezi."""
        bot = self.igralci[self.na_vrsti]
        najvecja_razdalja = self.velikost_tabele[0] + self.velikost_tabele[1] - 2
        aktivni_igralci = [igralec for igralec in self.igralci if igralec.v_igri]
        tocke = 0.5
        # Botu je praviloma cilj končati potezo na lihi oddaljenosti od igralca,
        # saj pri razdalji 0 igralec odloča o njegovi usodi, navadno pa se po celem
        # krogu potez parnosti razdalj ohranjajo. Prednost oziroma slabost je bolj
        # občutna pri nižji razdalji do igralca.
        for igralec in aktivni_igralci:
            if igralec != bot:
                razdalja = Igra.taksi_razdalja(bot.polje, igralec.polje)
                tocke += (
                    (-1) ** (razdalja + 1)
                    * (najvecja_razdalja - razdalja)
                    / (3 * najvecja_razdalja * (razdalja + 1) * len(aktivni_igralci))
                )
        # Botu je cilj ostati čim dlje od roba, saj ga je tako težje izločiti.
        vrstica, stolpec = bot.polje
        tocke = 1 - (1 - tocke) * 0.95 ** min(
            vrstica,
            stolpec,
            self.velikost_tabele[0] + 1 - vrstica,
            self.velikost_tabele[1] + 1 - stolpec,
        )
        # Bot hoče eliminirati igralce.
        tocke = 1 - (1 - tocke) * 0.25 ** (
            st_igralcev_pred_potezo - len(aktivni_igralci)
        )
        # Bot seveda noče izgubiti.
        if not bot.v_igri:
            tocke *= 0.1
        # Da dodamo še nekaj nepredvivljivosti.
        EPSILON = 0.05
        return tocke * (1 + EPSILON * (2 * random.random() - 1))

    def zmagovalci(self):
        """Vrne indeks zmagovalca igre.
        Če so vsi igralci izločeni, vrne `NI_ZMAGOVALCA`.
        Če je v igri še več igralcev, vrne `NEDOKONCANA`."""
        aktivni_igralci = [
            indeks for indeks, igralec in enumerate(self.igralci) if igralec.v_igri
        ]
        if len(aktivni_igralci) == 0:
            return NI_ZMAGOVALCA
        elif len(aktivni_igralci) == 1:
            return aktivni_igralci[0]
        else:
            return NEDOKONCANA

    def nacin_igre(self):
        """Vrne način igre, ustrezno izmed vrednosti `"Običajna"`, `"Hitra"` in
        `"Prilagojena"`."""
        if len(self.igralci) == 2:
            if not self.igralci[0].je_bot and self.igralci[1].je_bot:
                if self.velikost_tabele == (6, 6):
                    return "Običajna"
                elif self.velikost_tabele == (4, 4):
                    return "Hitra"
        return "Prilagojena"

    def vleci_karto(self, st_igralca):
        """Vzame karto iz vrha kupčka in jo da v roke igralca `st_igralca`.
        Če je kupček prazen, ustvari novega."""
        try:
            zgornja_karta = self.kupcek.pop()
            self.igralci[st_igralca].karte_v_roki.append(zgornja_karta)
        # ce je prazen kupcek, zmesa novega, sicer problem pri vecjih tabelah
        except IndexError:
            self.ustvari_nov_kupcek()
            self.vleci_karto(st_igralca)

    def razdeli_karte(self):
        """Vsakemu igralcu dodeli 3 karte iz vrha kupčka."""
        for _ in range(3):
            for st_igralca in range(len(self.igralci)):
                self.vleci_karto(st_igralca)

    def napreduj_po_tabeli(self, st_igralca=None):
        """Premakne igralca `st_igralca` vzdolž poti. Če pristane na rob
        tabele ali se zaleti v drugega igralca, ga izloči iz igre."""
        if st_igralca is None:
            st_igralca = self.na_vrsti
        igralec = self.igralci[st_igralca]
        while True:
            polje, polozaj = igralec.polje, igralec.polozaj
            # ce igralec zapusti tabelo
            if not (
                0 < polje[0] < self.velikost_tabele[0] + 1
                and 0 < polje[1] < self.velikost_tabele[1] + 1
            ):
                igralec.v_igri = False
                break
            # ce se dva zaletita
            dva_igralca = False
            for indeks in range(len(self.igralci)):
                if (
                    self.igralci[indeks].polje,
                    self.igralci[indeks].polozaj,
                ) == self.obrni_se_na_mestu(polje, polozaj):
                    igralec.v_igri = False
                    self.igralci[indeks].v_igri = False
                    dva_igralca = True
            if dva_igralca:
                break
            # normalen zakljucek poteze
            if self.tabela[polje] is None:
                break
            polje, polozaj = self.naslednja_pozicija(polje, polozaj)
            igralec.polje, igralec.polozaj = polje, polozaj

    def postavi_karto_na_tabelo(self, polje, karta):
        """Na polje `polje` postavi karto `karta`."""
        self.tabela[polje] = karta

    def barvaj_povezave_od_pozicije(self, polje, polozaj, barva):
        """Vsem povezavam na poti, ki vodi od pozicije `polje, polozaj`
        dodeli barvo `barva`."""
        while not self.tabela[polje] is None:
            karta = self.tabela[polje]
            karta.barve[polozaj] = barva
            karta.barve[karta.povezave[polozaj]] = barva
            polje, polozaj = self.naslednja_pozicija(polje, polozaj)

    def primerno_pobarvaj_poti(self):
        """Pobarva poti za igralci z njihovimi barvami, mrtve poti s
        sivo, ostale pa z belo barvo."""
        for polje in self.tabela:
            karta = self.tabela[polje]
            if not karta is None:
                for polozaj in range(8):
                    karta.barve[polozaj] = BELA
        for polje, polozaj in self.robne_pozicije():
            self.barvaj_povezave_od_pozicije(polje, polozaj, SIVA)
        for indeks in range(len(self.igralci)):
            polje, polozaj = Igra.obrni_se_na_mestu(
                self.igralci[indeks].polje, self.igralci[indeks].polozaj
            )
            barva = VRSTNI_RED_BARV[indeks]
            self.barvaj_povezave_od_pozicije(polje, polozaj, barva)

    def naslednja_pozicija(self, staro_polje, star_polozaj):
        """Vrne pozicijo, ki jo dobi, če se premakne po eni povezavi
        na sosednje polje."""
        nov_polozaj = self.tabela[staro_polje].povezave[star_polozaj]
        return Igra.obrni_se_na_mestu(staro_polje, nov_polozaj)

    def robne_pozicije(self):
        """Generator, ki vrača po vrsti vse pozicije na robu tabele
        (od levega zgornjega kota v pozitivni smer po vrsti)."""
        for i in range(1, self.velikost_tabele[0] + 1):
            yield ((i, 1), 6)
            yield ((i, 1), 7)
        for j in range(1, self.velikost_tabele[1] + 1):
            yield ((self.velikost_tabele[0], j), 0)
            yield ((self.velikost_tabele[0], j), 1)
        for i in range(self.velikost_tabele[0], 0, -1):
            yield ((i, self.velikost_tabele[1]), 2)
            yield ((i, self.velikost_tabele[1]), 3)
        for j in range(self.velikost_tabele[1], 0, -1):
            yield ((1, j), 4)
            yield ((1, j), 5)

    @staticmethod
    def taksi_razdalja(polje1, polje2):
        """Vrne taksi razdaljo med poljema `polje1` in `polje2`."""
        x1, y1 = polje1
        x2, y2 = polje2
        return abs(x1 - x2) + abs(y1 - y2)

    @staticmethod
    def nasproten_polozaj(polozaj):
        """Vrne položaj, ki je nasproti položaju `polozaj`."""
        return [5, 4, 7, 6, 1, 0, 3, 2][polozaj]

    @staticmethod
    def obrni_se_na_mestu(polje, polozaj):
        """Vrne pozicijo, ki jo dobimo, če igralca pustimo na
        isti lokaciji, a mu obrnemo smer."""
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
        """Generator, ki vrača vse možne razdelitve seznama
        `seznam` na disjunktne pare."""
        # more biti sodo mnogo, sicer se ne da
        assert len(seznam) % 2 == 0
        if len(seznam) == 2:
            yield [seznam]
        else:
            # po vseh možnostih para (0, i):
            for i in range(1, len(seznam)):
                nov_seznam = seznam[:]
                nov_seznam.pop(i)
                nov_seznam.pop(0)
                for pari in Igra.razdeli_na_pare(nov_seznam):
                    novi_pari = [[seznam[0], seznam[i]]]
                    novi_pari.extend(pari)
                    yield novi_pari

    @staticmethod
    def pari_v_povezave(seznam_parov):
        """Vrne seznam, ki ustreza karti, katere povezave
        povezujejo položaje iz parov iz seznama `seznam_parov`."""
        povezave = [None for _ in range(2 * len(seznam_parov))]
        for par in seznam_parov:
            povezave[par[0]] = par[1]
            povezave[par[1]] = par[0]
        return povezave

    @staticmethod
    def vse_karte():
        """Generator, ki vrača vseh 35 možnih različnih kart."""
        stare = []
        for seznam_parov in Igra.razdeli_na_pare():
            povezave = Igra.pari_v_povezave(seznam_parov)
            karta = Karta(povezave)
            vrni = True
            for _ in range(4):
                if karta in stare:
                    vrni = False
                karta.zarotiraj()
            if vrni:
                stare.append(karta)
                yield karta


@dataclass
class Uporabnik:
    uporabnisko_ime: str
    geslo: int
    igre: Dict[int, Igra] = None

    def __post_init__(self):
        if self.igre is None:
            self.igre = {}

    def v_slovar(self):
        """Vrne slovar z ustreznimi podatki."""
        return {
            "uporabnisko_ime": self.uporabnisko_ime,
            "geslo": self.geslo,
            "igre": {
                str(id_igre): igra.v_slovar() for id_igre, igra in self.igre.items()
            },
        }

    @classmethod
    def iz_slovarja(cls, slovar):
        """Ustvari in vrne objekt s podatki iz slovarja."""
        return Uporabnik(
            uporabnisko_ime=slovar["uporabnisko_ime"],
            geslo=slovar["geslo"],
            igre={
                int(id_igre): Igra.iz_slovarja(slovar["igre"][id_igre])
                for id_igre in slovar["igre"]
            },
        )

    def ustvari_novo_igro(
        self,
        id_igre=None,
        cas=None,
        igralci=None,
        velikost_tabele=(6, 6),
        kupcek=None,
        tabela=None,
        na_vrsti=0,
    ):
        """Ustvari novo igro s podanimi parametri in jo doda
        v slovar `self.igre`. Vrne ustvarjeno igro."""
        if id_igre is None:
            id_igre = self.prost_id_igre()
        igra = Igra(
            id_igre=id_igre,
            cas=cas,
            igralci=igralci,
            velikost_tabele=velikost_tabele,
            kupcek=kupcek,
            tabela=tabela,
            na_vrsti=na_vrsti,
        )
        self.igre[id_igre] = igra
        return igra

    def inicializiraj_igro(
        self, imena_igralcev, boti_in_igralci, velikost_tabele=(6, 6)
    ):
        """Ustvari in vrne novo igro s tabelo velikosti `velikost_tabele`,
        v kateri imajo igralci imena iz seznama `imena_igralcev` in so
        morebiti boti skladno s seznamom Boolovih vrednosti `boti_in_igralci`.
        Igralcem razdeli karte in pokliče botove poteze, če ti začnejo."""
        igra = self.ustvari_novo_igro(
            id_igre=None,
            cas=None,
            igralci=None,
            velikost_tabele=velikost_tabele,
            kupcek=None,
            tabela=None,
            na_vrsti=0,
        )
        for indeks in range(len(boti_in_igralci)):
            igra.dodaj_novega_igralca(
                ime=imena_igralcev[indeks], je_bot=boti_in_igralci[indeks]
            )
            if not igra.igralci[indeks].ime:
                igra.igralci[indeks].ime = f"Igralec {indeks + 1}"
        igra.razdeli_karte()
        igra.botova_poteza()
        return igra

    def prost_id_igre(self):
        """Vrne prost id za novo igro."""
        return len(self.igre) + 1

    def statistika(self):
        """Vrne slovar, ki vsebuje statistiko običajnih in hitrih iger."""
        zmage, izenacenja, porazi, nedokoncane = 0, 0, 0, 0
        for igra in self.igre.values():
            if igra.nacin_igre() in ["Hitra", "Običajna"]:
                zmagovalec = igra.zmagovalci()
                if zmagovalec == 0:
                    zmage += 1
                elif zmagovalec == 1:
                    porazi += 1
                elif zmagovalec == NI_ZMAGOVALCA:
                    izenacenja += 1
                elif zmagovalec == NEDOKONCANA:
                    nedokoncane += 1
        return {
            "zmage": zmage,
            "izenacenja": izenacenja,
            "porazi": porazi,
            "nedokoncane": nedokoncane,
            "prilagojene": len(
                [
                    igra
                    for igra in self.igre.values()
                    if igra.nacin_igre() == "Prilagojena"
                ]
            ),
            "skupaj": len(self.igre),
            "razmerje": (round(zmage / porazi, 2) if porazi != 0 else 999.9)
            if zmage != 0
            else 0,
            "vseh_iger_proti_racunalniku": zmage + porazi + izenacenja
        }

    def spremeni_ime_v_starih_igrah(self, novo_ime):
        """Nastavi ime igralca v shranjenih običajnih in hitrih igrah na `novo_ime`."""
        for igra in self.igre.values():
            if igra.nacin_igre() in ["Običajna", "Hitra"]:
                igra.igralci[0].ime = novo_ime

    @staticmethod
    def zasifriraj_geslo(geslo_v_cistopisu: str):
        """Vrne celo število, iz katerega ni moč enostavno razbrati
        vnesenega `geslo_v_cistopisu`."""
        zaporedje = "QWERTZUIOPŠĐASDFGHJKLČĆŽYXCVBNMqwertzuiopšđasdfghjklčćžyxcvbnm 0123456789.,_<>!#&%$()[]-@€ß"
        for znak in geslo_v_cistopisu:
            if not znak in zaporedje:
                geslo_v_cistopisu = geslo_v_cistopisu.replace(znak, "ß")
        return sum(
            [
                2 ** zaporedje.index(geslo_v_cistopisu[indeks_znaka])
                * 3**indeks_znaka
                for indeks_znaka in range(len(geslo_v_cistopisu))
            ]
        )


@dataclass
class Tsuro:
    uporabniki: Dict[str, Uporabnik] = None

    def __post_init__(self):
        if self.uporabniki is None:
            self.uporabniki = {}

    def v_slovar(self):
        """Vrne slovar z ustreznimi podatki."""
        return {ime: self.uporabniki[ime].v_slovar() for ime in self.uporabniki}

    @classmethod
    def iz_slovarja(cls, slovar):
        """Ustvari in vrne objekt s podatki iz slovarja."""
        return Tsuro(
            uporabniki={ime: Uporabnik.iz_slovarja(slovar[ime]) for ime in slovar}
        )

    def preveri_geslo(self, uporabnisko_ime, zasifrirano_geslo):
        """Vrne `True` natanko tedaj, ko ima uporabnik z imenom
        `uporabnisko_ime` geslo v zašifrirani obliki `zasifrirano_geslo`."""
        return self.uporabniki[uporabnisko_ime].geslo == zasifrirano_geslo

    def dodaj_uporabnika(self, ime, geslo):
        """Ustvari novega uporabnika z imenom `ime` in zašifriranim geslom `geslo`."""
        nov_uporabnik = Uporabnik(ime, geslo)
        self.uporabniki[ime] = nov_uporabnik
        return nov_uporabnik

    def v_datoteko(self, ime_datoteke):
        """Shrani objekt v JSON datoteko `ime_datoteke`"""
        with open(ime_datoteke, "w") as datoteka:
            json.dump(self.v_slovar(), datoteka, ensure_ascii=False, indent=4)

    @classmethod
    def iz_datoteke(cls, ime_datoteke):
        """Iz JSON datoteke `ime_datoteke` ustvari in vrne objekt razreda `Tsuro`."""
        with open(ime_datoteke) as datoteka:
            return cls.iz_slovarja(json.load(datoteka))
