% rebase("base.tpl", title = "Tsuro")
<div class="mb-4"></div>
% include("prikazi_tabelo.tpl")
% if zmagovalci == nedokoncana:
  <p class="pt-3 text-center fs-3">Na potezi je {{igra.igralci[igra.na_vrsti].ime}}:</p>
  % include("karte_v_roki.tpl")
% elif zmagovalci == ni_zmagovalca:
  <p class="pt-3 text-center fs-3">Vsi igralci so izločeni, ni zmagovalca.</p>
% else:
  <p class="pt-3 text-center fs-3">Zmagovalec je {{igra.igralci[zmagovalci].ime}}.</p>
% end

