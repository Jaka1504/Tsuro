% rebase("base.tpl", title="Tsuro – Registracija")

<h1>Registracija</h1>
<div class="card bg-secondary">
  <div class="card-body">
    <form action="/registracija/" method="post">
      <div class="form-group">
        <label for="uporabnisko_ime">Uporabniško ime:</label>
        <input type="text" class="form-control" id="uporabnisko_ime" name="uporabnisko_ime" placeholder="Uporabniško ime" minlength="3" maxlength="15">
      </div>
      <div class="form-group">
        <label for="geslo">Geslo:</label>
        <input type="password" class="form-control mb-1" id="geslo" name="geslo" placeholder="Geslo" minlength="5" maxlength="20">
      </div>
      % if napaka:
      <div class="alert alert-danger py-1 my-1 fs-6">{{napaka}}</div>
      % end
      <div class="d-grid">
        <button class="btn btn-dark mt-1" type="submit">Registracija</button>
      </div>
    </form>
  </div>
</div>
