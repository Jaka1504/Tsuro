% rebase("base.tpl", title = "Tsuro - Nova igra")


<h1>Prilagodi igro</h1>
<div class="card bg-secondary">
    <div class="card-body">
        <form>
            % for indeks in range(st_igralcev):
            <div class="input-group mb-3">
                <div class="input-group-text">
                    <img src="/img/igralec_povecan.png" alt="igralec" height="10px" class="hue" style="--hue: 0">
                </div>
                <input name="ime_igralca" placeholder="Igralec {{indeks + 1}}" class="form-control">
                <div class="input-group-text">
                    <input class="form-check-input" type="checkbox" value="je_bot" id="bot1">
                </div>
            </div>
            % end
        </form>
    </div>
</div>