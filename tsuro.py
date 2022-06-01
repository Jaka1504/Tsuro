import model
import bottle


tsuro = model.Tsuro()
uporabnik = tsuro.dodaj_uporabnika()
tsuro.ustvari_novo_igro(id_igre="test")
igra = tsuro.igre["test"]
for i in range(1, model.VELIKOST_TABELE[0] + 1):
    for j in range(1, model.VELIKOST_TABELE[1] + 1):
        igra.postavi_karto_na_tabelo((i, j), igra.kupcek[(6 * i + j) % 35])
        

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
    return bottle.template("index", igra=igra, velikost_tabele = model.VELIKOST_TABELE)


# To naj bo na dnu datoteke.
bottle.run(reloader=True, debug=True)