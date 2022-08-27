import model
import bottle

with open("skrivnost.txt", mode="r", encoding="utf-8") as datoteka:
    SKRIVNOST = datoteka.read()
DAT = "tsuro.json"


tsuro = model.Tsuro.iz_datoteke(DAT)


@bottle.get("/img/<ime_slike:path>")
def staticne_slike(ime_slike):
    return bottle.static_file(ime_slike, root="img")


@bottle.get("/static/<ime_datoteke:path>")
def css(ime_datoteke):
    return bottle.static_file(ime_datoteke, root="views")


@bottle.get("/")
def get_index():
    return bottle.template("index", uporabnisko_ime=poisci_uporabnisko_ime())


@bottle.get("/pravila/")
def get_pravila():
    demo_igra_prazna = model.Igra(id_igre="DEMO", velikost_tabele=(4, 4))
    for _ in range(5):
        demo_igra_prazna.dodaj_novega_igralca()
    karte = demo_igra_prazna.kupcek[:3]
    return bottle.template(
        "pravila",
        igra=demo_igra_prazna,
        karte=karte,
        bela=model.BELA,
        siva=model.SIVA,
        barve=model.VRSTNI_RED_BARV,
        uporabnisko_ime=poisci_uporabnisko_ime(),
    )


@bottle.get("/prijava/")
def get_prijava():
    return bottle.template(
        "prijava",
        napaka=None,
        uporabnisko_ime=poisci_uporabnisko_ime(),
    )


@bottle.post("/prijava/")
def post_prijava():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    geslo = model.Uporabnik.zasifriraj_geslo(bottle.request.forms.getunicode("geslo"))
    napaka = None
    if uporabnisko_ime in tsuro.uporabniki.keys():
        if tsuro.preveri_geslo(
            uporabnisko_ime=uporabnisko_ime, zasifrirano_geslo=geslo
        ):
            bottle.response.set_cookie(
                name="uporabnisko_ime",
                value=uporabnisko_ime,
                secret=SKRIVNOST,
                path="/",
            )
        else:
            napaka = "Uporabniško ime in geslo se ne ujemata!"
    else:
        napaka = "Ta uporabnik ne obstaja. Preveri črkovanje ali ustvari nov račun!"
    if napaka:
        return bottle.template(
            "prijava", napaka=napaka, uporabnisko_ime=poisci_uporabnisko_ime()
        )
    else:
        return bottle.redirect("/")


@bottle.get("/registracija/")
def get_registracija():
    return bottle.template(
        "registracija",
        napaka=None,
        uporabnisko_ime=poisci_uporabnisko_ime(),
    )


@bottle.post("/registracija/")
def post_registracija():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    geslo = model.Uporabnik.zasifriraj_geslo(bottle.request.forms.getunicode("geslo"))
    napaka = None
    if uporabnisko_ime in tsuro.uporabniki.keys():
        napaka = "To uporabniško ime je že zasedeno. Prosim, izberi drugačno ime."
        return bottle.template(
            "registracija", napaka=napaka, uporabnisko_ime=poisci_uporabnisko_ime()
        )
    else:
        tsuro.dodaj_uporabnika(ime=uporabnisko_ime, geslo=geslo)
        bottle.response.set_cookie(
            name="uporabnisko_ime", value=uporabnisko_ime, secret=SKRIVNOST, path="/"
        )
        tsuro.v_datoteko(DAT)
        return bottle.redirect("/")


@bottle.get("/nova-igra/")
def get_nova_igra():
    return bottle.template(
        "nova_igra",
        uporabnisko_ime=poisci_uporabnisko_ime(),
    )


@bottle.post("/nova-igra/")
def post_nova_igra():
    uporabnik = poisci_uporabnika()
    nacin = bottle.request.forms.getunicode("nacin")
    if nacin == "Običajna igra":
        igra = uporabnik.inicializiraj_igro(
            imena_igralcev=[uporabnik.uporabnisko_ime, "Bot"],
            boti_in_igralci=[False, True],
            velikost_tabele=(6, 6),
        )
        nastavi_id_igre(igra.id_igre)
        tsuro.v_datoteko(DAT)
        return bottle.redirect("/igra/")
    elif nacin == "Hitra igra":
        igra = uporabnik.inicializiraj_igro(
            imena_igralcev=[uporabnik.uporabnisko_ime, "Bot"],
            boti_in_igralci=[False, True],
            velikost_tabele=(4, 4),
        )
        nastavi_id_igre(igra.id_igre)
        tsuro.v_datoteko(DAT)
        return bottle.redirect("/igra/")
    else:
        return bottle.redirect("/nova-igra/prilagodi/osnovno/")


@bottle.get("/nova-igra/prilagodi/osnovno/")
def get_nova_igra_prilagodi_osnovno():
    return bottle.template(
        "prilagodi_osnovno",
        uporabnisko_ime=poisci_uporabnisko_ime(),
    )


@bottle.post("/nova-igra/prilagodi/osnovno/")
def post_nova_igra_prilagodi_osnovno():
    st_igralcev = int(bottle.request.forms.getunicode("st_igralcev"))
    st_vrstic = int(bottle.request.forms.getunicode("st_vrstic"))
    st_stolpcev = int(bottle.request.forms.getunicode("st_stolpcev"))
    bottle.response.set_cookie(
        name="st_igralcev",
        value=st_igralcev,
        secret=SKRIVNOST,
        path="/nova-igra/prilagodi/",
    )
    bottle.response.set_cookie(
        name="velikost_tabele",
        value=(st_vrstic, st_stolpcev),
        secret=SKRIVNOST,
        path="/nova-igra/",
    )
    return bottle.redirect("/nova-igra/prilagodi/igralci/")


@bottle.get("/nova-igra/prilagodi/igralci/")
def get_nova_igra_prilagodi_igralci():
    st_igralcev = bottle.request.get_cookie("st_igralcev", secret=SKRIVNOST)
    return bottle.template(
        "prilagodi_igralci",
        st_igralcev=st_igralcev,
        barve=model.VRSTNI_RED_BARV,
        uporabnisko_ime=poisci_uporabnisko_ime(),
    )


@bottle.post("/nova-igra/prilagodi/igralci/")
def post_nova_igra_prilagodi_igralci():
    uporabnik = poisci_uporabnika()
    st_igralcev = bottle.request.get_cookie("st_igralcev", secret=SKRIVNOST)
    velikost_tabele = bottle.request.get_cookie("velikost_tabele", secret=SKRIVNOST)
    boti_in_igralci = [
        (not bottle.request.forms.getunicode(f"bot{i}") is None)
        for i in range(st_igralcev)
    ]
    imena_igralcev = [
        bottle.request.forms.getunicode(f"ime_igralca{i}") for i in range(st_igralcev)
    ]
    igra = uporabnik.inicializiraj_igro(
        imena_igralcev=imena_igralcev,
        boti_in_igralci=boti_in_igralci,
        velikost_tabele=velikost_tabele,
    )
    nastavi_id_igre(igra.id_igre)
    tsuro.v_datoteko(DAT)
    return bottle.redirect("/igra/")


@bottle.post("/nova-igra/enaka/")
def post_nova_igra_enaka():
    uporabnik = poisci_uporabnika()
    trenutna_igra = uporabnik.igre[poisci_id_igre()]
    nova_igra = uporabnik.inicializiraj_igro(
        imena_igralcev=[igralec.ime for igralec in trenutna_igra.igralci],
        boti_in_igralci=[igralec.je_bot for igralec in trenutna_igra.igralci],
        velikost_tabele=trenutna_igra.velikost_tabele,
    )
    nastavi_id_igre(nova_igra.id_igre)
    tsuro.v_datoteko(DAT)
    return bottle.redirect("/igra/")


@bottle.get("/igra/")
def get_igra():
    uporabnik = poisci_uporabnika()
    id_igre = poisci_id_igre()
    if id_igre:
        igra = uporabnik.igre[id_igre]
        return bottle.template(
            "igra",
            igra=igra,
            bela=model.BELA,
            siva=model.SIVA,
            barve=model.VRSTNI_RED_BARV,
            ni_zmagovalca=model.NI_ZMAGOVALCA,
            nedokoncana=model.NEDOKONCANA,
            zmagovalci=igra.zmagovalci(),
            uporabnisko_ime=poisci_uporabnisko_ime(),
        )
    else:
        return bottle.redirect("/nova-igra/")


@bottle.post("/igra/")
def post_igra():
    uporabnik = poisci_uporabnika()
    igra = uporabnik.igre[poisci_id_igre()]
    rotacija = bottle.request.forms.getunicode("zarotiraj")
    postavi_karto = bottle.request.forms.getunicode("postavi-karto")
    if not rotacija is None:
        indeks_karte = int(rotacija[0])
        st_rotacij = int(rotacija[1])
        igra.igralci[igra.na_vrsti].karte_v_roki[indeks_karte].zarotiraj(st_rotacij)
        return bottle.redirect("/igra/")
    elif not postavi_karto is None:
        igra.igralec_postavi_karto_na_tabelo(int(postavi_karto))
        tsuro.v_datoteko(DAT)
        return bottle.redirect("/igra/")


@bottle.get("/pregled-iger/bot/")
def get_pregled_iger_bot():
    uporabnik = poisci_uporabnika()
    return bottle.template(
        "pregled_iger_bot",
        nedokoncana=model.NEDOKONCANA,
        ni_zmagovalca=model.NI_ZMAGOVALCA,
        barve=model.VRSTNI_RED_BARV,
        igre=uporabnik.igre,
        uporabnisko_ime=uporabnik.uporabnisko_ime,
    )


@bottle.post("/pregled-iger/bot/")
def post_pregled_iger_bot():
    id_igre = bottle.request.forms.getunicode("id_igre")
    nastavi_id_igre(id_igre)
    return bottle.redirect("/igra/")


@bottle.get("/pregled-iger/prilagojene/")
def get_pregled_iger_prilagojene():
    uporabnik = poisci_uporabnika()
    return bottle.template(
        "pregled_iger_prilagojene",
        nedokoncana=model.NEDOKONCANA,
        ni_zmagovalca=model.NI_ZMAGOVALCA,
        barve=model.VRSTNI_RED_BARV,
        igre=uporabnik.igre,
        uporabnisko_ime=uporabnik.uporabnisko_ime,
    )


@bottle.post("/pregled-iger/prilagojene/")
def post_pregled_iger_prilagojene():
    id_igre = bottle.request.forms.getunicode("id_igre")
    nastavi_id_igre(id_igre)
    return bottle.redirect("/igra/")


@bottle.get("/profil/")
def get_profil():
    uporabnik = poisci_uporabnika()
    return bottle.template(
        "profil",
        barve=model.VRSTNI_RED_BARV,
        uporabnisko_ime=uporabnik.uporabnisko_ime,
        uporabnik=uporabnik,
        napaka=None,
    )


@bottle.post("/profil/")
def post_profil():
    uporabnik = poisci_uporabnika()
    napaka = None
    spremeni_ime = bottle.request.forms.getunicode("spremeni_ime")
    spremeni_geslo = model.Uporabnik.zasifriraj_geslo(
        bottle.request.forms.getunicode("spremeni_geslo")
    )
    staro_geslo = model.Uporabnik.zasifriraj_geslo(
        bottle.request.forms.getunicode("staro_geslo")
    )
    print(spremeni_ime, spremeni_geslo, staro_geslo)
    if spremeni_ime and spremeni_ime in tsuro.uporabniki.keys():
        napaka = "To uporabniško ime je že zasedeno. Prosim, izberi drugačno ime."
    if not tsuro.preveri_geslo(
        uporabnisko_ime=uporabnik.uporabnisko_ime, zasifrirano_geslo=staro_geslo
    ):
        napaka = "Geslo za potrditev je napačno. Poskusi ponovno."
    if napaka:
        return bottle.template(
            "profil",
            barve=model.VRSTNI_RED_BARV,
            uporabnisko_ime=uporabnik.uporabnisko_ime,
            uporabnik=uporabnik,
            napaka=napaka,
        )
    else:
        if spremeni_geslo:
            uporabnik.geslo = spremeni_geslo
        if spremeni_ime:
            tsuro.uporabniki[spremeni_ime] = tsuro.uporabniki.pop(
                uporabnik.uporabnisko_ime
            )
            uporabnik.uporabnisko_ime = spremeni_ime
            tsuro.v_datoteko(DAT)
            bottle.response.set_cookie(
                name="uporabnisko_ime", value=spremeni_ime, secret=SKRIVNOST, path="/"
            )
        return bottle.redirect("/")


@bottle.get("/lestvica/")
def get_lestvica():
    uporabnik = poisci_uporabnika()
    return bottle.template(
        "lestvica",
        uporabnisko_ime=uporabnik.uporabnisko_ime,
        uporabniki=tsuro.uporabniki,
    )


@bottle.post("/odjava/")
def post_odjava():
    bottle.response.delete_cookie("uporabnisko_ime", path="/")
    return bottle.redirect("/")


def poisci_uporabnika():
    uporabnisko_ime = poisci_uporabnisko_ime()
    if not uporabnisko_ime:
        return bottle.redirect("/prijava/")
    else:
        return tsuro.uporabniki[uporabnisko_ime]


def poisci_id_igre():
    """Poišče in vrne vrednost piškotka `id_igre`, ki jo spremeni v celo število."""
    id_igre = bottle.request.get_cookie(key="id_igre", secret=SKRIVNOST)
    if id_igre is None:
        return None
    else:
        return int(id_igre)


def poisci_uporabnisko_ime():
    """Poišče in vrne vrednost piškotka `uporabnisko_ime`."""
    return bottle.request.get_cookie(key="uporabnisko_ime", secret=SKRIVNOST)


def nastavi_id_igre(id):
    """Nastavi vrednost piškotka `id_igre` na `id`, ki ga pretvori v niz."""
    bottle.response.set_cookie(
        name="id_igre",
        value=str(id),
        secret=SKRIVNOST,
        path="/",
    )


# To naj bo na dnu datoteke.
bottle.run()
