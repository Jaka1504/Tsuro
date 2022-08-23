% rebase("base.tpl", title = "Tsuro - profil")
% statistika = uporabnik.statistika()

<h1 class="mb-3">Profil - {{uporabnisko_ime}}</h1>
<div class="card bg-secondary mb-3">
  <div class="card-header fs-3">
    Statistika
  </div>
  <div class="card-body">
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
    % vse = statistika["skupaj"] - statistika["prilagojene"]
    % delez_zmag = 100 * statistika["zmage"] / vse
    % delez_porazov = 100 * statistika["porazi"] / vse
    % delez_izenacenj = 100 * statistika["izenacenja"] / vse
    % delez_nedokoncanih = 100 * statistika["nedokoncane"] / vse
    <div class="progress">
      <div class="progress-bar progress-bar-striped bg-danger" role="progressbar" style="width: {{delez_zmag}}%" aria-valuenow="{{delez_zmag}}" aria-valuemin="0" aria-valuemax="100"></div>
      <div class="progress-bar progress-bar-striped bg-dark" role="progressbar" style="width: {{delez_izenacenj}}%" aria-valuenow="{{delez_izenacenj}}" aria-valuemin="0" aria-valuemax="100"></div>
      <div class="progress-bar progress-bar-striped bg-success" role="progressbar" style="width: {{delez_porazov}}%" aria-valuenow="{{delez_porazov}}" aria-valuemin="0" aria-valuemax="100"></div>
      <div class="progress-bar progress-bar-striped bg-light" role="progressbar" style="width: {{delez_nedokoncanih}}%" aria-valuenow="{{delez_nedokoncanih}}" aria-valuemin="0" aria-valuemax="100"></div>
    </div>
  </div>
</div>
<div class="card bg-secondary mb-3">
  <div class="card-header fs-3">
    Upravljanje računa
  </div>
  <div class="card-body">
    <form action="/odjava/" method="post">
      <p class="fs-4 mb-0">Odjava</p>
      <div class="d-grid">
        <button class="btn btn-dark mt-1" type="submit">Odjava</button>
      </div>
    </form>
    <hr>
    <form action="/profil/" method="post">
      <p class="fs-4 mb-1">Uredi račun</p>
      <label for="spremeni_ime" class="input-label">Spremeni uporabniško ime:</label>
      <input type="text" class="form-control" id="spremeni_ime" name="spremeni_ime" placeholder="Vnesi novo uporabniško ime" minlength="3" maxlength="20">
      <label for="spremeni_geslo">Spremeni geslo:</label>
      <input type="password" class="form-control" id="spremeni_geslo" name="spremeni_geslo" placeholder="Vnesi novo geslo" minlength="6" maxlength="20">
      <label for="staro_geslo">Potrdi s starim geslom:</label>
      <input type="password" class="form-control" id="staro_geslo" name="staro_geslo" placeholder="Vnesi staro geslo" minlength="6" maxlength="20">
      % if napaka:
      <small class="form-text opozorilo">{{napaka}}</small>
      %end
      <div class="d-grid">
        <button class="btn btn-dark mt-3" type="submit">Potrdi spremembe</button>
      </div>
    </form>
  </div>
</div>