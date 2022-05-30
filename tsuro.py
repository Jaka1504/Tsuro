import model
import bottle


tsuro = model.Tsuro()


@bottle.get("/")
def osnovna_stran():
    return bottle.template("index")


# To naj bo na dnu datoteke.
bottle.run(reloader=True, debug=True)