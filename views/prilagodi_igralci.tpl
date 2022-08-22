% rebase("base.tpl", title = "Tsuro - Nova igra")


<h1>Prilagodi igro</h1>
<div class="card bg-secondary">
    <div class="card-body">
        <form action="/nova-igra/prilagodi/igralci/" method="post">
            % for indeks in range(st_igralcev):
            <div class="input-group mb-3">
                <div class="input-group-text">
                    <img src="/img/igralec_povecan.png" alt="igralec" height="10px" class="hue" style="--hue: {{barve[indeks]}}deg">
                </div>
                <input name="ime_igralca{{indeks}}" placeholder="Igralec {{indeks + 1}}" class="form-control">
                <div class="input-group-text">
                    <input class="form-check-input" type="checkbox" name="bot{{indeks}}" value="je_bot">
                </div>
            </div>
            % end
            <div class="d-grid">
                <button class="btn btn-dark besedilo" type="submit">Potrdi</button>
            </div>
        </form>
    </div>
</div>