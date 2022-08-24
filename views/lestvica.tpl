% rebase("base.tpl", title="Tsuro - Lestvica")

<h1 class="mb-3">Lestvica uporabnikov</h1>
<div class="card bg-secondary">
  <div class="card-body py-0">
    <div class="tabela-scroll d-grid">
      <table class="table text-light">
        <thead class="sticky-top bg-secondary">
          <tr>
            <th scope="col">#</th>
            <th scope="col">Ime</th>
            <th scope="col">Vseh iger</th>
            <th scope="col" colspan="2">Razmerje zmag in porazov</th>
          </tr>
        </thead>
        <tbody>
          % urejeni = sorted(list(uporabniki.keys()), key=lambda ime: -uporabniki[ime].statistika()["razmerje"])
          % for ime in urejeni:
          <tr>
            <th scope="row">
              {{urejeni.index(ime) + 1}}.
            </th>
            <td>
              {{ime}}
            </td>
            <td>
              {{uporabniki[ime].statistika()["skupaj"]}}
            </td>
            <td width="10%">
              {{uporabniki[ime].statistika()["razmerje"]}}
            </td>
            <td class="progress-bar-lestvica">
              % include("prikaz_statistike.tpl", statistika=uporabniki[ime].statistika())
            </td>
          </tr>
          % end
        </tbody>
      </table>
    </div>
  </div>
</div>