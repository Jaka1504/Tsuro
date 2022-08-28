% rebase("base.tpl", title="Tsuro")

<h1>Tsuro</h1>
<div class="card bg-secondary mb-3">
  <div class="card-body">
    <p class="fs-5 fw-bold">
      Pozdravljen/-a{{f", {uporabnisko_ime}," if uporabnisko_ime else ""}} in dobrodošel/-a v igri Tsuro!
    </p>
    <p>
      Tsuro je namizna igra, ki jo je leta 1979 ustvaril Tom McMurchie in jo izdaja podjetje Calliope Games. Igra je dobila ime po japonski besedi <i>"tsūro"</i> (通路), ki pomeni "pot". Več o igri si lahko prebereš na strani <a href="https://en.wikipedia.org/wiki/Tsuro" class="link text-dark">Wikipedia</a>.
    </p>
    <p>
      Ker so pravila v tej različici nekoliko prirejena, je priporočljivo, da si prebereš stran s <a class="link text-dark" href="/pravila/">pravili</a>, kjer je opisan potek igre s primeri.
    </p>
  </div>
</div>

<div class="card bg-dark border-secondary mb-3">
  <div class="card-body pt-1 pb-0">
    <blockquote class="blockquote">
      <p class="fs-5 text-secondary">Does the walker choose the path, or the path the walker?</p>
      <footer class="blockquote-footer text-secondary fs-6">Garth Nix, Sabriel</footer>
    </blockquote>
  </div>
</div>

<div class="card bg-secondary mb-3">
  <div class="card-body">
    % if not uporabnisko_ime:
    <p>
      Da si omogočiš dostop do vseh funkcij te aplikacije, se prosim prijavi ali registriraj.
    </p>
    <div class="row" width="100%">
      <div class="col d-grid">
        <a class="btn btn-dark btn-block" href="/prijava/">Prijava</a>
      </div>
      <div class="col d-grid">
        <a class="btn btn-dark btn-block" href="/registracija/">Registracija</a>
      </div>
    </div>
    % else:
    <p>
      S pomočjo spodnjih povezav si lahko pogledaš pravila igre, ustvariš novo igro, pogledaš zgodovino svojih iger in mnogo drugega. Vse te bližnjice so dostopne tudi v navigacijski vrstici na vrhu vsake strani.
    </p>
    <div class="row mb-2" width="100%">
      <div class="col d-grid pe-1">
        <a class="btn btn-dark btn-block" href="/pravila/">Pravila igre</a>
      </div>
      <div class="col d-grid ps-1">
        <a class="btn btn-dark btn-block" href="/nova-igra/">Nova igra</a>
      </div>
    </div>
    <div class="row mb-2" width="100%">
      <div class="col d-grid pe-1">
        <a class="btn btn-dark btn-block" href="/profil/">Profil</a>
      </div>
      <div class="col d-grid ps-1">
        <a class="btn btn-dark btn-block" href="/lestvica/">Lestvica igralcev</a>
      </div>
    </div>
    <div class="row" width="100%">
      <div class="col d-grid pe-1">
        <a class="btn btn-dark btn-block" href="/pregled-iger/bot/">Pregled iger proti računalniku</a>
      </div>
      <div class="col d-grid ps-1">
        <a class="btn btn-dark btn-block" href="/pregled-iger/prilagojene/">Pregled prilagojenih iger</a>
      </div>
    </div>
    % end
  </div>
</div>


<!-- <form action="/nova-igra/" method="post">
  <div class="d-grid" role="group" id="nacin">
    <input name="nacin" value="Običajna igra" type="submit" class="btn btn-dark mt-3 besedilo">
    <input name="nacin" value="Hitra igra" type="submit" class="btn btn-dark mt-3 besedilo">
    <input name="nacin" value="Prilagodi sam" type="submit" class="btn btn-dark mt-3 besedilo">
  </div>
</form> -->