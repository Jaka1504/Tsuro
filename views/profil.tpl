% rebase("base.tpl", title = "Tsuro – Profil")
% statistika = uporabnik.statistika()

<h1>Profil – {{uporabnisko_ime}}</h1>
<div class="card bg-secondary mb-3">
  <div class="card-header fs-3">
    Statistika
  </div>
  <div class="card-body pt-0">
    <table class="table text-light">
      <tr>
        <td>
          Odigrane igre:
        </td>
        <td>
          {{statistika["skupaj"]}}
        </td>
      </tr>
      <tr>
        <td>
          Od tega proti računalniku:
        </td>
        <td>
          {{statistika["skupaj"] - statistika["prilagojene"]}}
        </td>
      </tr>
      <tr>
        <td>
          <img src="/img/igralec_povecan.png" alt="igralec" height="10px" class="hue" style="--hue: {{barve[0]}}deg">
          Zmage:
        </td>
        <td>
          {{statistika["zmage"]}}
        </td>
      </tr>
      <tr>
        <td>
          <img src="/img/igralec_povecan.png" alt="igralec" height="10px" class="siva-povezava">
          Izenačenja:
        </td>
        <td>
          {{statistika["izenacenja"]}}
        </td>
      </tr>
      <tr>
        <td>
          <img src="/img/igralec_povecan.png" alt="igralec" height="10px" class="hue" style="--hue: {{barve[1]}}deg">
          Porazi:
        </td>
        <td>
          {{statistika["porazi"]}}
        </td>
      </tr>
      <tr>
        <td>
          <img src="/img/igralec_povecan.png" alt="igralec" height="10px" class="bela-povezava">
          Nedokončane igre:
        </td>
        <td>
          {{statistika["nedokoncane"]}}
        </td>
      </tr>
      <tr>
        <td>
          Razmerje zmag in porazov:
        </td>
        <td>
          {{statistika["razmerje"]}}
        </td>
      </tr>
    </table>
    % include("prikaz_statistike.tpl", statistika=statistika)
  </div>
</div>
<div class="card bg-secondary mb-3">
  <div class="card-header fs-3">
    Upravljanje računa
  </div>
  <div class="card-body pt-1">
    <form action="/odjava/" method="post">
      <p class="fs-4 mb-0">Odjava</p>
      <div class="d-grid">
        <button class="btn btn-dark mt-1" type="submit">Odjava</button>
      </div>
    </form>
  </div>
  <div class="card-footer pt-1">
    <form action="/profil/" method="post">
      <p class="fs-4 mb-1">Uredi račun</p>
      <label for="spremeni_ime" class="input-label">Spremeni uporabniško ime:</label>
      <input type="text" class="form-control" id="spremeni_ime" name="spremeni_ime" placeholder="Vnesi novo uporabniško ime" minlength="3" maxlength="20">
      <label for="spremeni_geslo">Spremeni geslo:</label>
      <input type="password" class="form-control" id="spremeni_geslo" name="spremeni_geslo" placeholder="Vnesi novo geslo" minlength="6" maxlength="20">
      <label for="staro_geslo">Potrdi s starim geslom:</label>
      <input type="password" class="form-control mb-1" id="staro_geslo" name="staro_geslo" placeholder="Vnesi staro geslo" minlength="6" maxlength="20">
      % if napaka:
      <div class="alert alert-danger p-1 my-1 fs-6">{{napaka}}</div>
      %end
      <div class="d-grid">
        <button class="btn btn-dark mt-2" type="submit">Potrdi spremembe</button>
      </div>
    </form>
  </div>
</div>