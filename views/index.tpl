% rebase("base.tpl", title = "Tsuro")
<div class="row">
  <div class="col-2"></div>
  <div class="col">
    <h1>Igra Tsuro</h1>
    % include("prikazi_tabelo.tpl")
    <p>Karte, ki jih ima v roki Igralec {{igra.na_vrsti}} so:</p>
    <div class="table">
      <div class="row">
        % for karta in igra.igralci[igra.na_vrsti].karte_v_roki:
          <div class="col-1">
            % include("prikazi_karto.tpl")
          </div>
        % end
      </div>
    </div>
  </div>
  <div class="col-2"></div>
</div>


<!-- , tabela=igra.tabela, velikost_tabele=velikost_tabele -->
