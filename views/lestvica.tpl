% rebase("base.tpl", title="Tsuro – Lestvica")

<h1>Lestvica igralcev</h1>
<div class="card bg-secondary">
  <div class="card-header">
    <p class="mb-0">
      Na lestvici so prikazani igralci, ki so do konca odigrali vsaj tri tekme proti računalniku. Kriterij za razvrstitev je razmerje med številom zmag in porazov. Z zeleno barvo so predstavljene njihove zmage, s sivo izenačenja, z rdečo pa porazi. Prilagojene igre niso vštete v to statistiko.
    </p>
  </div>
  <div class="card-body py-0">
    <div class="tabela-scroll d-grid">
      <table class="table text-light">
        <thead>
          <tr>
            <th scope="col" class="text-end">#</th>
            <th scope="col">Ime</th>
            <th scope="col" colspan="2">Razmerje zmag in porazov</th>
            <th scope="col">Odigrano</th>
          </tr>
        </thead>
        <tbody>
          % urejeni = sorted(
          %   [ime for ime in uporabniki if uporabniki[ime].statistika()["vseh_iger_proti_racunalniku"] >= 3],
          %   key=lambda ime: [-uporabniki[ime].statistika()["razmerje"], -uporabniki[ime].statistika()["vseh_iger_proti_racunalniku"], ime]
          % )
          % for ime in urejeni:
          % statistika = uporabniki[ime].statistika()
          <tr>
            <th scope="row" width="5%" class="text-end">
              {{urejeni.index(ime) + 1}}.
            </th>
            <td>
              {{ime}}
            </td>
            <td width="10%"  class="text-end">
              {{statistika["razmerje"]}}
            </td>
            <td class="progress-bar-lestvica">
              % include("prikaz_statistike.tpl", statistika=statistika)
            </td>
            <td width="10%" class="text-end">
              {{statistika["vseh_iger_proti_racunalniku"]}}
            </td>
          </tr>
          % end
        </tbody>
      </table>
    </div>
  </div>
</div>