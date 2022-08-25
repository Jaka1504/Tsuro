% rebase("base.tpl", title="Tsuro – Prijava")

<h1>Prijava</h1>
<div class="card bg-secondary">
  <div class="card-body">
    <form action="/prijava/" method="post">
      <div class="form-group">
        <label for="uporabnisko_ime">Uporabniško ime:</label>
        <input type="text" class="form-control" id="uporabnisko_ime" name="uporabnisko_ime" placeholder="Uporabniško ime" minlength="3" maxlength="20">
      </div>
      <div class="form-group">
        <label for="geslo">Geslo:</label>
        <input type="password" class="form-control" id="geslo" name="geslo" placeholder="Geslo" minlength="6" maxlength="20">
      </div>
      % if napaka:
      <small class="form-text opozorilo">{{napaka}}</small>
      %end
      <div class="d-grid">
        <button class="btn btn-dark my-3" type="submit">Prijava</button>
      </div>
    </form>
    <label for="registracija">Še nimaš računa? Registriraj se:</label>
    <div class="d-grid">
      <a class="btn btn-dark" href="/registracija/" id="registracija">Registracija</a>
    </div>
  </div>
</div>
