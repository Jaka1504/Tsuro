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
          <form action="/igra/" method="post">
            <div class="btn-group" role="group">
              <button name="zarotiraj" value="{{indeks}}1" type="submit" class="btn btn-outline-secondary">
                <img src="/img/arrow-counterclockwise.svg" height="20px" style="filter:invert()">
              </button>
              <button name="postavi-karto" value="{{indeks}}" type="submit" class="btn btn-outline-secondary">
                <img src="/img/box-arrow-in-up.svg" height="20px" style="filter:invert()">
              </button>
              <button name="zarotiraj" value="{{indeks}}3" type="submit" class="btn btn-outline-secondary">
                <img src="/img/arrow-clockwise.svg" height="20px" style="filter:invert()">
              </button>
            </div>
          </form>
        </div>
        <div class="col"></div>
      </div>
    % end
  </div>
</div>