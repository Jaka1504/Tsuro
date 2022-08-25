% rebase("base.tpl", title="Tsuro - Pravila igre")

<h1>Pravila igre</h1>
<div class="card bg-secondary mb-3">
  <div class="card-body">
    <p>
      Igra tsuro se običajno igra na tabeli s šestimi vrsticami in šestimi stolpci, katere polja so kvadrati, vendar je mogoče z enakimi pravili igrati tudi na drugačnih dimenzijah tabele. Igro igra od dva do osem igralcev, ki po vrsti izvajajo svoje poteze. Zanjo je potreben kupček kart, ki po velikosti ustrezajo poljam tabele.
    </p>
    <p>
      Na vsaki karti imamo na vsakem robu po dve točki enako oddaljeni druga od druge in od oglišč karte. Vsaka od teh točk je s povezavo povezana z natanko eno drugo točko, torej so na vsaki karti štiri povezave. Tu je nekaj primerov tovrstnih kart:
    </p>
    <div class="row mb-3">
      % for karta in karte:
      <div class="col d-flex justify-content-center">
        % include("prikazi_karto.tpl", karta=karta)
      </div>
      %end
    </div>
    <p>
      Na začetku so vsa polja tabele prazna. Poimenujmo <i>položaj</i> točko na mreži tabele, ki je za eno tretjino dolžine polja oddaljena od najbližjega oglišča. Vsak igralec ima svoj žeton na začetku igre postavljen na nek položaj na robu tabele. Tako torej izgleda tabela velikosti 4×4 na začetku igre s petimi igralci:
    </p>
    <div class="d-flex justify-content-center my-3">
      % include("prikazi_tabelo", igra=igra)
    </div>
    <p>
      Igralec prične igro z tremi kartami v roki. Na svoji potezi izbere eno od svojih kart, jo poljubno zasuče in postavi na polje tabele pred svojim žetonom. Nato premakne svoj žeton (in morebitne ostale žetone od tem polju) vzdolž tiste povezave na postavljeni karti, ki vodi od položaja žetona, s čimer potezo zopet konča na enem od dovoljenih položajev. Če s tega položaja vodijo povezave še naprej, mora igralec žeton premikati po njih, dokler ne pride do praznega polja, drugega žetona ali roba tabele. Na koncu povleče novo karto in s svojo potezo nadaljuje naslednji igralec po vrsti.
    </p>
    <p>
      Igralec je <i>izločen</i> iz igre, če ne more več storiti poteze, t.j. če se njegov žeton vrne na rob tabele ali pa če se zaleti v žeton drugega igralca (v tem primeru sta izločena oba). Zmagovalec igre je zadnji igralec, ki še ni izločen. V primeru, da je več igralcev izločenih v isti potezi in po njej v igri ne ostane nihče, je izid izenačen.
    </p>
    <p class="mb-0">
      Za lažjo vizualizacijo so povezave v igri pobarvane z različnimi barvami:
    </p>
    <ul>
      <li>
        Z <i>belo</i> barvo so pobarvane povezave, ki na obeh straneh vodijo na prazno polje. Če se igralec poveže na belo povezavo, iz igre ni izločen.
      </li>
      <li>
        S <i>sivo</i> barvo so pobarvane povezave, ki vsaj na eni strani vodijo do roba tabele. Če se igralec poveže na sivo povezavo, je iz igre izločen.
      </li>
      <li>
        Z <i>ostalimi</i> barvami so pobarvane povezave, ki povezujejo ustrezno obarvan žeton z njegovo začetno lokacijo. Hiter razmislek pokaže, da se na te povezave ni mogoče povezati.
      </li>
    </ul>
    <div class="row" width="100%">
      <div class="col d-grid pe-3">
        <a class="btn btn-dark btn-block" href="/">Na začetno stran</a>
      </div>
      <div class="col d-grid ps-3">
        <a class="btn btn-dark btn-block" href="/nova-igra/">Začni novo igro</a>
      </div>
    </div>
  </div>
</div>