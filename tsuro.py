import model
import bottle


# ST_IGRALCEV = 8  # za testiranje
SKRIVNOST = "bhjčkeibvcjčbdnjsbcv"
DAT = "tsuro.json"


tsuro = model.Tsuro.iz_datoteke(DAT)
# uporabnik = tsuro.dodaj_uporabnika("Testni uporabnik", "geslo")
# uporabnik.ustvari_novo_igro(id_igre="test", velikost_tabele=(6, 6))
# igra = uporabnik.igre["test"]


# igra.dodaj_novega_igralca()
# for _ in range(ST_IGRALCEV - 1):
#     igra.dodaj_novega_igralca(je_bot=True)
# igra.razdeli_karte()


@bottle.get("/img/<ime_slike:path>")
def staticne_slike(ime_slike):
    return bottle.static_file(ime_slike, root="img")


@bottle.get("/static/<ime_datoteke:path>")
def css(ime_datoteke):
    return bottle.static_file(ime_datoteke, root="views")


@bottle.get("/")
def osnovna_stran():
    return bottle.redirect("/nova-igra/")


@bottle.get("/prijava/")
def get_prijava():
    return bottle.template("prijava", napaka=None, uporabnisko_ime=bottle.request.get_cookie("uporabnisko_ime", secret=SKRIVNOST))


@bottle.post("/prijava/")
def post_prijava():
    uporabnisko_ime=bottle.request.forms.getunicode("uporabnisko_ime")
    geslo=model.Uporabnik.zasifriraj_geslo(bottle.request.forms.getunicode("geslo"))
    napaka = None
    if uporabnisko_ime in tsuro.uporabniki.keys():
        if tsuro.preveri_geslo(uporabnisko_ime=uporabnisko_ime, zasifrirano_geslo=geslo):
            bottle.response.set_cookie(
                name="uporabnisko_ime",
                value=uporabnisko_ime,
                secret=SKRIVNOST,
                path="/"
            )
        else:
            napaka = "Uporabniško ime in geslo se ne ujemata!"
    else:
        napaka = "Ta uporabnik ne obstaja. Preveri črkovanje ali ustvari nov račun!"
    if napaka:
        return bottle.template("prijava", napaka=napaka, uporabnisko_ime=bottle.request.get_cookie("uporabnisko_ime", secret=SKRIVNOST))
    else:
        return bottle.redirect("/")


@bottle.get("/registracija/")
def get_registracija():
    return bottle.template("registracija", napaka=None, uporabnisko_ime=bottle.request.get_cookie("uporabnisko_ime", secret=SKRIVNOST))


@bottle.post("/registracija/")
def post_registracija():
    uporabnisko_ime=bottle.request.forms.getunicode("uporabnisko_ime")
    geslo=model.Uporabnik.zasifriraj_geslo(bottle.request.forms.getunicode("geslo"))
    napaka = None
    if uporabnisko_ime in tsuro.uporabniki.keys():
        napaka="To uporabniško ime je že zasedeno. Prosim, izberi drugačno ime."
        return bottle.template("registracija", napaka=napaka, uporabnisko_ime=bottle.request.get_cookie("uporabnisko_ime", secret=SKRIVNOST))
    else:
        tsuro.dodaj_uporabnika(ime=uporabnisko_ime, geslo=geslo)
        bottle.response.set_cookie(
            name="uporabnisko_ime",
            value=uporabnisko_ime,
            secret=SKRIVNOST,
            path="/"
        )
        tsuro.v_datoteko(DAT)
        return bottle.redirect("/")


@bottle.get("/nova-igra/")
def izbira_nove_igre():
    return bottle.template("nova_igra", uporabnisko_ime=bottle.request.get_cookie("uporabnisko_ime", secret=SKRIVNOST))


@bottle.post("/nova-igra/")
def nova_igra():
    uporabnik = poisci_uporabnika()
    nacin = bottle.request.forms.getunicode("nacin")
    if nacin == "Običajna igra":
        # dodaj da preveri kdo je uporabnik
        igra = uporabnik.inicializiraj_igro(imena_igralcev=[uporabnik.uporabnisko_ime, "Bot"], boti_in_igralci=[False, True], velikost_tabele=(6, 6))
        bottle.response.set_cookie(name="id_igre", value=int(igra.id_igre), secret=SKRIVNOST, path="/")
        tsuro.v_datoteko(DAT)
        return bottle.redirect("/igra/")
    elif nacin == "Hitra igra":
        igra = uporabnik.inicializiraj_igro(imena_igralcev=[uporabnik.uporabnisko_ime, "Bot"], boti_in_igralci=[False, True], velikost_tabele=(4, 4))
        bottle.response.set_cookie(name="id_igre", value=int(igra.id_igre), secret=SKRIVNOST, path="/")
        tsuro.v_datoteko(DAT)
        return bottle.redirect("/igra/")
    else:
        return bottle.redirect("/nova-igra/prilagodi/osnovno/")


@bottle.get("/nova-igra/prilagodi/osnovno/")
def prilagodi():
    return bottle.template("prilagodi_osnovno", uporabnisko_ime=bottle.request.get_cookie("uporabnisko_ime", secret=SKRIVNOST))


@bottle.post("/nova-igra/prilagodi/osnovno/")
def naslednja_stran_prilagodi():
    st_igralcev = int(bottle.request.forms.getunicode("st_igralcev"))
    st_vrstic = int(bottle.request.forms.getunicode("st_vrstic"))
    st_stolpcev = int(bottle.request.forms.getunicode("st_stolpcev"))
    bottle.response.set_cookie(name="st_igralcev", value=st_igralcev, secret=SKRIVNOST, path="/nova-igra/prilagodi/")
    bottle.response.set_cookie(name="velikost_tabele", value=(st_vrstic, st_stolpcev), secret=SKRIVNOST, path="/nova-igra/")
    return bottle.redirect("/nova-igra/prilagodi/igralci/")


@bottle.get("/nova-igra/prilagodi/igralci/")
def izbor_igralcev():
    st_igralcev=bottle.request.get_cookie("st_igralcev", secret=SKRIVNOST)
    return bottle.template(
        "prilagodi_igralci",
        st_igralcev=st_igralcev,
        barve=model.VRSTNI_RED_BARV,
        uporabnisko_ime=bottle.request.get_cookie("uporabnisko_ime", secret=SKRIVNOST)
    )


@bottle.post("/nova-igra/prilagodi/igralci/")
def ustvari_prilagojeno_igro():
    uporabnik = poisci_uporabnika()
    st_igralcev = bottle.request.get_cookie("st_igralcev", secret=SKRIVNOST)
    velikost_tabele = bottle.request.get_cookie("velikost_tabele", secret=SKRIVNOST)
    boti_in_igralci = [(not bottle.request.forms.getunicode(f"bot{i}") is None) for i in range(st_igralcev)]
    imena_igralcev = [bottle.request.forms.getunicode(f"ime_igralca{i}") for i in range(st_igralcev)]
    igra = uporabnik.inicializiraj_igro(imena_igralcev=imena_igralcev, boti_in_igralci=boti_in_igralci, velikost_tabele=velikost_tabele)
    bottle.response.set_cookie(name="id_igre", value=int(igra.id_igre), secret=SKRIVNOST, path="/")
    tsuro.v_datoteko(DAT)
    return bottle.redirect("/igra/")


@bottle.get("/igra/")
def stran_z_igro():
    uporabnik = poisci_uporabnika()
    igra = uporabnik.igre[bottle.request.get_cookie("id_igre", secret=SKRIVNOST)]
    zmagovalci=igra.zmagovalci()
    return bottle.template(
        "igra",
        igra=igra,
        velikost_tabele=igra.velikost_tabele,
        bela=model.BELA,
        siva=model.SIVA,
        barve=model.VRSTNI_RED_BARV,
        ni_zmagovalca=model.NI_ZMAGOVALCA,
        nedokoncana=model.NEDOKONCANA,
        zmagovalci=zmagovalci,
        uporabnisko_ime=bottle.request.get_cookie("uporabnisko_ime", secret=SKRIVNOST)
    )


@bottle.post("/igra/")
def poteza():
    uporabnik = poisci_uporabnika()
    igra = uporabnik.igre[bottle.request.get_cookie("id_igre", secret=SKRIVNOST)]
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
    return bottle.template("pregled_iger_bot",
        nedokoncana=model.NEDOKONCANA,
        ni_zmagovalca=model.NI_ZMAGOVALCA,
        barve=model.VRSTNI_RED_BARV,
        igre=uporabnik.igre,
        uporabnisko_ime=uporabnik.uporabnisko_ime
    )


@bottle.post("/pregled-iger/bot/")
def post_pregled_iger_bot():
    id_igre = bottle.request.forms.getunicode("id_igre")
    bottle.response.set_cookie(name="id_igre", value=int(id_igre), secret=SKRIVNOST, path="/")
    return bottle.redirect("/igra/")


@bottle.get("/pregled-iger/prilagojene/")
def get_pregled_iger_prilagojene():
    uporabnik = poisci_uporabnika()
    return bottle.template("pregled_iger_prilagojene",
        nedokoncana=model.NEDOKONCANA,
        ni_zmagovalca=model.NI_ZMAGOVALCA,
        barve=model.VRSTNI_RED_BARV,
        igre=uporabnik.igre,
        uporabnisko_ime=uporabnik.uporabnisko_ime
    )


@bottle.post("/pregled-iger/prilagojene/")
def post_pregled_iger_prilagojene():
    id_igre = bottle.request.forms.getunicode("id_igre")
    bottle.response.set_cookie(name="id_igre", value=int(id_igre), secret=SKRIVNOST, path="/")
    return bottle.redirect("/igra/")


@bottle.get("/profil/")
def get_profil():
    uporabnik = poisci_uporabnika()
    return bottle.template(
        "profil",
        barve=model.VRSTNI_RED_BARV,
        uporabnisko_ime=uporabnik.uporabnisko_ime,
        uporabnik=uporabnik,
        napaka=None
    )

@bottle.post("/profil/")
def post_profil():
    uporabnik = poisci_uporabnika()
    napaka = None
    spremeni_ime = bottle.request.forms.getunicode("spremeni_ime")
    spremeni_geslo = model.Uporabnik.zasifriraj_geslo(bottle.request.forms.getunicode("spremeni_geslo"))
    staro_geslo = model.Uporabnik.zasifriraj_geslo(bottle.request.forms.getunicode("staro_geslo"))
    print(spremeni_ime, spremeni_geslo, staro_geslo)
    if spremeni_ime and spremeni_ime in tsuro.uporabniki.keys():
        napaka = "To uporabniško ime je že zasedeno. Prosim, izberi drugačno ime."
    if not tsuro.preveri_geslo(uporabnisko_ime=uporabnik.uporabnisko_ime, zasifrirano_geslo=staro_geslo):
        napaka = "Geslo za potrditev je napačno. Poskusi ponovno."
    if napaka:
        return bottle.template(
            "profil",
            barve=model.VRSTNI_RED_BARV,
            uporabnisko_ime=uporabnik.uporabnisko_ime,
            uporabnik=uporabnik,
            napaka=napaka
        )
    else:
        if spremeni_geslo:
            uporabnik.geslo = spremeni_geslo
        if spremeni_ime:
            tsuro.uporabniki[spremeni_ime] = tsuro.uporabniki.pop(uporabnik.uporabnisko_ime)
            uporabnik.uporabnisko_ime = spremeni_ime
            tsuro.v_datoteko(DAT)
            bottle.response.set_cookie(
                name="uporabnisko_ime",
                value=spremeni_ime,
                secret=SKRIVNOST,
                path="/"
            )
        return bottle.redirect("/")

    

@bottle.post("/odjava/")
def post_odjava():
    bottle.response.delete_cookie("uporabnisko_ime", path="/")
    return bottle.redirect("/")



# @bottle.post("/zarotiraj/<rotacija>")
# def zarotiraj(rotacija):
#     igra = uporabnik.igre[bottle.request.get_cookie("id_igre", secret=SKRIVNOST)]
    


# @bottle.post("/postavi-karto/<indeks>")
# def postavi_karto(indeks):
#     igra = uporabnik.igre[bottle.request.get_cookie("id_igre", secret=SKRIVNOST)]
#     novo_stanje = igra.igralec_postavi_karto_na_tabelo(int(indeks))
#     print(novo_stanje) # potem izbrisi
#     if novo_stanje == model.NEDOKONCANA:
#         return bottle.redirect("/igra/")
#     elif novo_stanje == model.ZMAGA:
#         raise ValueError
#     elif novo_stanje == model.NI_ZMAGOVALCA:
#         raise ValueError
#     else:
#         raise ValueError


def poisci_uporabnika():
    uporabnisko_ime = bottle.request.get_cookie(key="uporabnisko_ime", secret=SKRIVNOST)
    if not uporabnisko_ime:
        return bottle.redirect("/prijava/")
    else:
        return tsuro.uporabniki[uporabnisko_ime]


# To naj bo na dnu datoteke.
bottle.run(reloader=True, debug=True)

