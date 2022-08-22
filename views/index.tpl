% rebase("base.tpl", title = "Tsuro")

% include("prikazi_tabelo.tpl")
% if zmagovalci == nedokoncana:
  <p style="padding-top:20px; text-align:center; font-size:30px">Na potezi je Igralec {{igra.na_vrsti + 1}}:</p>
  % include("karte_v_roki.tpl")
% elif zmagovalci == ni_zmagovalca:
  <p style="padding-top:20px; text-align:center; font-size:30px">Vsi igralci so izločeni, ni zmagovalca.</p>
% else:
  <p style="padding-top:20px; text-align:center; font-size:30px">Zmagovalec je Igralec {{zmagovalci + 1}}.</p>
% end

