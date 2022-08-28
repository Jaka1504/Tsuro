% rebase("base.tpl", title = "Tsuro – Igra")
<div class="mb-4"></div>
% include("prikazi_tabelo.tpl")
% if zmagovalci == nedokoncana:
  <p class="pt-3 text-center fs-4">
    Na potezi je <img src="/img/igralec_povecan.png" alt="igralec" class="hue igralec-text" style="--hue: {{barve[igra.na_vrsti]}}deg"> {{igra.igralci[igra.na_vrsti].ime}}:
  </p>
  % include("karte_v_roki.tpl")
  <div class="card bg-dark border-secondary mt-4">
    <div class="card-body py-1">
      <p class="text-secondary mb-0 fs-6">S klikom na gumba <img src="/img/arrow-counterclockwise.svg" alt="Obrni karto - gumb" class="igralec-text invert"> in <img src="/img/arrow-clockwise.svg" alt="Obrni karto - gumb" class="igralec-text invert"> lahko zasučeš karto v prikazani smeri. Če želiš karto pri trenutni usmerjenosti postaviti na tabelo, klikni na gumb <img src="/img/box-arrow-in-up.svg" alt="Postavi karto - gumb" class="igralec-text invert">. Karta bo postavljena na polje ob žetonu tvoje barve.</p>
    </div>
  </div>
% elif zmagovalci == ni_zmagovalca:
  <p class="pt-3 text-center fs-4">Vsi igralci so izločeni, ni zmagovalca.</p>
  <div class="row" width="100%">
    <div class="col">
      <form action="/nova-igra/enaka/" method="post">
        <div class="d-grid"><button class="btn btn-secondary btn-block" type="submit">Igraj ponovno</button></div>
      </form>
    </div>
    <div class="col d-grid">
      <a class="btn btn-secondary btn-block" href="/">Na začetno stran</a>
    </div>
  </div>
% else:
  <p class="pt-3 text-center fs-4">Zmagovalec je <img src="/img/igralec_povecan.png" alt="igralec" class="hue igralec-text" style="--hue: {{barve[zmagovalci]}}deg"> {{igra.igralci[zmagovalci].ime}}.</p>
  <div class="row" width="100%">
    <div class="col">
      <form action="/nova-igra/enaka/" method="post">
        <div class="d-grid"><button class="btn btn-secondary btn-block" type="submit">Igraj ponovno</button></div>
      </form>
    </div>
    <div class="col d-grid">
      <a class="btn btn-secondary btn-block" href="/">Na začetno stran</a>
    </div>
  </div>
% end

