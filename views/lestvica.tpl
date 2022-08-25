% rebase("base.tpl", title="Tsuro – Lestvica")

<h1>Lestvica uporabnikov</h1>
<div class="card bg-secondary">
  <div class="card-body py-0">
    <div class="tabela-scroll d-grid">
      <table class="table text-light">
        <thead class="sticky-top bg-secondary">
          <tr>
            <th scope="col" class="text-end">#</th>
            <th scope="col">Ime</th>
            <th scope="col" colspan="2">Razmerje zmag in porazov</th>
            <th scope="col">Odigrano</th>
          </tr>
        </thead>
        <tbody>
          % urejeni = sorted(list(uporabniki.keys()), key=lambda ime: -uporabniki[ime].statistika()["razmerje"])
          % for ime in urejeni:
          <tr>
            <th scope="row" width="5%" class="text-end">
              {{urejeni.index(ime) + 1}}.
            </th>
            <td>
              {{ime}}
            </td>
            <td width="10%"  class="text-end">
              {{uporabniki[ime].statistika()["razmerje"]}}
            </td>
            <td class="progress-bar-lestvica">
              % include("prikaz_statistike.tpl", statistika=uporabniki[ime].statistika())
            </td>
            <td width="10%" class="text-end">
              {{uporabniki[ime].statistika()["skupaj"] - uporabniki[ime].statistika()["prilagojene"]}}
            </td>
          </tr>
          % end
        </tbody>
      </table>
    </div>
  </div>
</div>