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
          <div class="col">
            % include("prikazi_karto.tpl")
          </div>
        % end
      </div>
      <div class="row">
        % for indeks in range(len(igra.igralci[igra.na_vrsti].karte_v_roki)):
          <div class="col">
            <div class="btn-group" role="group">
              <form action="/zarotiraj/{{indeks}}1" method="post">
                <button type="submit" class="btn btn-outline-primary">
                  <img src="/img/arrow-counterclockwise.svg" height="20px">
                </button>
              </form>
              <form action="/postavi-karto/{{indeks}}" method="post">
                <button $type="submit" class="btn btn-outline-primary">
                  <img src="/img/box-arrow-in-up.svg" height="20px">
                </button>
              </form>
              <form action="/zarotiraj/{{indeks}}3" method="post">
                <button type="submit" class="btn btn-outline-primary">
                  <img src="/img/arrow-clockwise.svg" height="20px">
                </button>
              </form>
            </div>
          </div>
        % end
      </div>
    </div>
  </div>
  <div class="col-2"></div>
</div>
