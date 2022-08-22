import model
import bottle
import random  # potem odstrani !!!


ST_IGRALCEV = 8  # za testiranje
SKRIVNOST = "bhjčkeibvcjčbdnjsbcv"


tsuro = model.Tsuro.iz_datoteke("tsuro.json")
uporabnik = tsuro.dodaj_uporabnika("Testni uporabnik", "geslo")
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


@bottle.get("/nova-igra/")
def izbira_nove_igre():
    return bottle.template("nova_igra")


@bottle.post("/nova-igra/")
def nova_igra():
    nacin = bottle.request.forms.getunicode("nacin")
    if nacin == "Običajna igra":
        # dodaj da preveri kdo je uporabnik
        igra = uporabnik.inicializiraj_igro(boti_in_igralci=[False, True],velikost_tabele=(6, 6))
        bottle.response.set_cookie(name="id_igre", value=igra.id_igre, secret=SKRIVNOST, path="/")
        return bottle.redirect("/igra/")
    elif nacin == "Hitra igra":
        igra = uporabnik.inicializiraj_igro(boti_in_igralci=[False, True],velikost_tabele=(4, 4))
        bottle.response.set_cookie(name="id_igre", value=igra.id_igre, secret=SKRIVNOST, path="/")
        return bottle.redirect("/igra/")
    else:
        return bottle.redirect("/nova-igra/prilagodi/osnovno/")


@bottle.get("/nova-igra/prilagodi/osnovno/")
def prilagodi():
    return bottle.template("prilagodi_osnovno")


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
        barve=model.VRSTNI_RED_BARV
    )


@bottle.post("/nova-igra/prilagodi/igralci/")
def ustvari_prilagojeno_igro():
    st_igralcev=bottle.request.get_cookie("st_igralcev", secret=SKRIVNOST)
    velikost_tabele=bottle.request.get_cookie("velikost_tabele", secret=SKRIVNOST)
    boti_in_igralci=[(not bottle.request.forms.getunicode(f"bot{i}") is None) for i in range(st_igralcev)]
    print(boti_in_igralci)
    igra=uporabnik.inicializiraj_igro(boti_in_igralci=boti_in_igralci, velikost_tabele=velikost_tabele)
    bottle.response.set_cookie(name="id_igre", value=igra.id_igre, secret=SKRIVNOST, path="/")
    return bottle.redirect("/igra/")

    


@bottle.get("/igra/")
def stran_z_igro():
    igra = uporabnik.igre[bottle.request.get_cookie("id_igre", secret=SKRIVNOST)]
    zmagovalci=igra.zmagovalci()
    return bottle.template(
        "index",
        igra=igra,
        velikost_tabele=igra.velikost_tabele,
        bela=model.BELA,
        siva=model.SIVA,
        barve=model.VRSTNI_RED_BARV,
        ni_zmagovalca=model.NI_ZMAGOVALCA,
        nedokoncana=model.NEDOKONCANA,
        zmagovalci=zmagovalci
    )


@bottle.post("/igra/")
def poteza():
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
        return bottle.redirect("/igra/")


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


# To naj bo na dnu datoteke.
bottle.run(reloader=True, debug=True)

