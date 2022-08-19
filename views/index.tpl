% rebase("base.tpl", title = "Tsuro")

<h1>Igra Tsuro</h1>  
% include("prikazi_tabelo.tpl")
<p style="padding-top:20px; text-align:center; font-size:30px">Na potezi je Igralec {{igra.na_vrsti}}:</p>
<div class="table">
  <div class="row">
    % for indeks, karta in enumerate(igra.igralci[igra.na_vrsti].karte_v_roki):
      <div class="col row">
        <div class="col"></div>
        <div class="col">
          % include("prikazi_karto.tpl")
        </div>
        <div class="col"></div>
      </div>
    % end
  </div>
  <div class="row">
    % for indeks in range(len(igra.igralci[igra.na_vrsti].karte_v_roki)):
      <div class="row col">
        <div class="col"></div>
        <div class="col">
          <div class="btn-group" role="group">
            <form action="/zarotiraj/{{indeks}}1" method="post">
              <button type="submit" class="btn btn-outline-light">
                <img src="/img/arrow-counterclockwise.svg" height="20px" style="filter:invert()">
              </button>
            </form>
            <form action="/postavi-karto/{{indeks}}" method="post">
              <button $type="submit" class="btn btn-outline-light">
                <img src="/img/box-arrow-in-up.svg" height="20px" style="filter:invert()">
              </button>
            </form>
            <form action="/zarotiraj/{{indeks}}3" method="post">
              <button type="submit" class="btn btn-outline-light">
                <img src="/img/arrow-clockwise.svg" height="20px" style="filter:invert()">
              </button>
            </form>
          </div>
      </div>
      <div class="col"></div>
    </div>
    % end
  </div>
</div>

