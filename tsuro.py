import model
import bottle
import random  # potem odstrani !!!


ST_IGRALCEV = 9  # za testiranje


tsuro = model.Tsuro()
uporabnik = tsuro.dodaj_uporabnika("Testni uporabnik", "geslo")
uporabnik.ustvari_novo_igro(id_igre="test", velikost_tabele=(6, 6))
igra = uporabnik.igre["test"]


# igra.dodaj_novega_igralca()
for _ in range(ST_IGRALCEV - 1):
    igra.dodaj_novega_igralca(je_bot=True)
# igra.primerno_pobarvaj_poti()
igra.razdeli_karte()


@bottle.get("/img/<ime_slike:path>")
def staticne_slike(ime_slike):
    return bottle.static_file(ime_slike, root="img")


@bottle.get("/static/<ime_datoteke:path>")
def css(ime_datoteke):
    return bottle.static_file(ime_datoteke, root="views")


@bottle.get("/")
def osnovna_stran():
    return bottle.redirect("/igra/")


@bottle.get("/igra/")
def stran_z_igro():
    return bottle.template(
        "index",
        igra=igra,
        velikost_tabele=igra.velikost_tabele,
        bela=model.BELA,
        siva=model.SIVA,
        barve=model.VRSTNI_RED_BARV,
    )


@bottle.post("/zarotiraj/<rotacija>")
def zarotiraj(rotacija):
    indeks_karte = int(rotacija[0])
    st_rotacij = int(rotacija[1])
    igra.igralci[igra.na_vrsti].karte_v_roki[indeks_karte].zarotiraj(st_rotacij)
    return bottle.redirect("/igra/")


@bottle.post("/postavi-karto/<indeks>")
def postavi_karto(indeks):
    novo_stanje = igra.igralec_postavi_karto_na_tabelo(int(indeks))
    print(novo_stanje) # potem izbrisi
    if novo_stanje == model.NEDOKONCANA:
        return bottle.redirect("/igra/")
    elif novo_stanje == model.ZMAGA:
        raise ValueError
    elif novo_stanje == model.NI_ZMAGOVALCA:
        raise ValueError
    else:
        raise ValueError


# To naj bo na dnu datoteke.
bottle.run(reloader=True, debug=True)

