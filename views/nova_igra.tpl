% rebase("base.tpl", title = "Tsuro - Nova igra")


<h1>Nova igra</h1>
<div class="card bg-secondary">
  <div class="card-body">
    <label for="nacin">Izberi način igre. V običajni igri se lahko pomeriš z računalnikom na tabeli velikosti 6×6, v hitri igri pa velikosti 4×4. Če želiš izbrati drugačno velikost tabele ali dodati več igralcev, izberi možnost "Prilagodi sam".</label>
    <form action="/nova-igra/" method="post">
      <div class="d-grid" role="group" id="nacin">
        <input name="nacin" value="Običajna igra" type="submit" class="btn btn-dark mt-3 besedilo">
        <input name="nacin" value="Hitra igra" type="submit" class="btn btn-dark mt-3 besedilo">
        <input name="nacin" value="Prilagodi sam" type="submit" class="btn btn-dark mt-3 besedilo">
      </div>
    </form>
  </div>
</div>
