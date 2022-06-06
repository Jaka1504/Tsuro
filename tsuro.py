import model
import bottle
import random # potem odstrani !!!


tsuro = model.Tsuro()
uporabnik = tsuro.dodaj_uporabnika()
tsuro.ustvari_novo_igro(id_igre="test")
igra = tsuro.igre["test"]
st_karte = 0
for i in range(1, model.VELIKOST_TABELE[0] + 1):
    for j in range(1, model.VELIKOST_TABELE[1] + 1):
        if random.random() > 0.05:
            igra.postavi_karto_na_tabelo((i, j), igra.kupcek[st_karte])
            st_karte += 1



igra.dodaj_novega_igralca(uporabnik)
igra.dodaj_novega_igralca(uporabnik)
igra.dodaj_novega_igralca(uporabnik)
igra.dodaj_novega_igralca(uporabnik)
igra.dodaj_novega_igralca(uporabnik)
igra.dodaj_novega_igralca(uporabnik)
igra.dodaj_novega_igralca(uporabnik)
igra.dodaj_novega_igralca(uporabnik)
igra.primerno_pobarvaj_poti()
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
    return bottle.template("index", igra=igra, velikost_tabele=model.VELIKOST_TABELE, bela=model.BELA, siva=model.SIVA, barve=model.VRSTNI_RED_BARV)


@bottle.post("/zarotiraj/<rotacija>")
def zarotiraj(rotacija):
    indeks_karte = int(rotacija[0])
    st_rotacij = int(rotacija[1])
    igra.igralci[igra.na_vrsti].karte_v_roki[indeks_karte].zarotiraj(st_rotacij)
    igra.primerno_pobarvaj_poti()           # potem izbrisi
    return bottle.redirect("/igra/")


# To naj bo na dnu datoteke.
bottle.run(reloader=True, debug=True)
# reloader=True, debug=True