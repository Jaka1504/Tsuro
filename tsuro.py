import model
import bottle


tsuro = model.Tsuro()


@bottle.get("/img/<file>")
def staticne_slike(file):
    return bottle.static_file(file, root="img")


@bottle.get("/views/style.css")
def css():
    return bottle.static_file("style.css", root="views")


@bottle.get("/")
def osnovna_stran():
    return bottle.template("index")


# To naj bo na dnu datoteke.
bottle.run(reloader=True, debug=True)