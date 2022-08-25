% rebase("base.tpl", title = "Tsuro – Igra")
<div class="mb-4"></div>
% include("prikazi_tabelo.tpl")
% if zmagovalci == nedokoncana:
  <p class="pt-3 text-center fs-4">Na potezi je {{igra.igralci[igra.na_vrsti].ime}}:</p>
  % include("karte_v_roki.tpl")
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
  <p class="pt-3 text-center fs-4">Zmagovalec je {{igra.igralci[zmagovalci].ime}}.</p>
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

