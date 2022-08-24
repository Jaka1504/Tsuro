<table width="100%">
  <tr>
    % for indeks, karta in enumerate(igra.igralci[igra.na_vrsti].karte_v_roki):
    <td>
      <div class="d-flex justify-content-center">
        % include("prikazi_karto.tpl")
      </div>
    </td>
    % end
  </tr>
  <tr>
    % for indeks in range(len(igra.igralci[igra.na_vrsti].karte_v_roki)):
    <td>
      <div class="d-flex justify-content-center mt-3">
        <form action="/igra/" method="post">
          <div class="btn-group" role="group">
            <button name="zarotiraj" value="{{indeks}}1" type="submit" class="btn btn-outline-secondary btn-sm">
              <img src="/img/arrow-counterclockwise.svg" class="invert gumb">
            </button>
            <button name="postavi-karto" value="{{indeks}}" type="submit" class="btn btn-outline-secondary btn-sm">
              <img src="/img/box-arrow-in-up.svg" class="invert gumb">
            </button>
            <button name="zarotiraj" value="{{indeks}}3" type="submit" class="btn btn-outline-secondary btn-sm">
              <img src="/img/arrow-clockwise.svg" class="invert gumb">
            </button>
          </div>
        </form>
      </div>
    </td>
    % end
  </tr>
    
  <!-- <div class="row">
    % for indeks in range(len(igra.igralci[igra.na_vrsti].karte_v_roki)):
      <div class="row col">
        <div class="col"></div>
        <div class="col">
          <form action="/igra/" method="post">
            <div class="btn-group" role="group">
              <button name="zarotiraj" value="{{indeks}}1" type="submit" class="btn btn-outline-secondary btn-sm">
                <img src="/img/arrow-counterclockwise.svg" class="invert gumb">
              </button>
              <button name="postavi-karto" value="{{indeks}}" type="submit" class="btn btn-outline-secondary btn-sm">
                <img src="/img/box-arrow-in-up.svg" class="invert gumb">
              </button>
              <button name="zarotiraj" value="{{indeks}}3" type="submit" class="btn btn-outline-secondary btn-sm">
                <img src="/img/arrow-clockwise.svg" class="invert gumb">
              </button>
            </div>
          </form>
        </div>
        <div class="col"></div>
      </div>
    % end
  </div> -->
</table>