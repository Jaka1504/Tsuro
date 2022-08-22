% rebase("base.tpl", title = "Tsuro")

% include("prikazi_tabelo.tpl")
% if zmagovalci == nedokoncana:
  <p style="padding-top:20px; text-align:center; font-size:30px">Na potezi je {{igra.igralci[igra.na_vrsti].ime}}:</p>
  % include("karte_v_roki.tpl")
% elif zmagovalci == ni_zmagovalca:
  <p style="padding-top:20px; text-align:center; font-size:30px">Vsi igralci so izločeni, ni zmagovalca.</p>
% else:
  <p style="padding-top:20px; text-align:center; font-size:30px">Zmagovalec je {{igra.igralci[zmagovalci].ime}}.</p>
% end

