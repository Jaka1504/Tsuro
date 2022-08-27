% rebase("base.tpl", title = "Tsuro – Pregled iger")

<h1>Pregled prilagojenih iger</h1>
<div class="card bg-secondary">
  <div class="card-body py-0">
    <form action="/pregled-iger/prilagojene/" method="post" id="igre">
      <div class="tabela-scroll d-grid">
        <table class="table text-light">
          <thead>
            <tr>
              <th scope="col">Datum</th>
              <th scope="col">Ura</th>
              <th scope="col">Tabela</th>
              <th scope="col">Zmagovalec</th>
              <th scope="col">Ogled tabele</th>
            </tr>
          </thead>
          <tbody>
            % for id_igre in list(igre.keys())[::-1]:
            % if igre[id_igre].nacin_igre() == "Prilagojena":
            <tr>
              <td>{{f"{igre[id_igre].cas.day}. {igre[id_igre].cas.month}. {igre[id_igre].cas.year}"}}</td>
              <td>{{f"{str(igre[id_igre].cas.hour).zfill(2)}:{str(igre[id_igre].cas.minute).zfill(2)}"}}</td>
              <td>{{igre[id_igre].velikost_tabele[0]}} x {{igre[id_igre].velikost_tabele[1]}}</td>
              % zmagovalec = igre[id_igre].zmagovalci()
              % if zmagovalec == nedokoncana:
              <td>
                <img src="/img/igralec_povecan.png" alt="igralec" class="bela-povezava igralec-text">
                Nedokončana
              </td>
              % elif zmagovalec == ni_zmagovalca:
              <td>
                <img src="/img/igralec_povecan.png" alt="igralec" class="siva-povezava igralec-text">
                Izenačenje
              </td>
              % else:
              <td>
                <img src="/img/igralec_povecan.png" alt="igralec" class="hue igralec-text" style="--hue: {{barve[zmagovalec]}}deg">
                {{igre[id_igre].igralci[zmagovalec].ime}}
              </td>
              % end
              <td>
                <div class="d-grid">
                  <button class="btn btn-outline-light btn-sm" name="id_igre" type="submit" value="{{id_igre}}">Prikaži</button>
                </div>
              </td>
            </tr>
            % end
            % end
          </tbody>
        </table>
      </div>
    </form>
  </div>
</div>