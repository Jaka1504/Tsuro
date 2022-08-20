% rebase("base.tpl", title = "Tsuro - Nova igra")

<h1>Prilagodi igro</h1>
<div class="card bg-secondary">
    <div class="card-body">
        <form action="/nova-igra/prilagodi/osnovno/" method="post">
            <label for="st_igralcev">Število igralcev (vključno z boti):</label>
            <select class="form-select" id="st_igralcev" name="st_igralcev">
                <option value="2" selected>2</option>
                % for indeks in range(3, 9):
                <option value="{{indeks}}">{{indeks}}</option>
                % end
            </select>
            <label for="st_vrstic">Število vrstic tabele:</label>
            <select class="form-select" id="st_vrstic">
                % for indeks in range(8):
                % if indeks == 5:
                <option value="{{indeks + 1}}" selected>{{indeks + 1}}</option>
                % else:
                <option value="{{indeks + 1}}">{{indeks + 1}}</option>
                % end
                % end
            </select>
            <label for="st_stolpcev">Število stolpcev tabele:</label>
            <select class="form-select mb-3" id="st_stolpcev">
                % for indeks in range(8):
                % if indeks == 5:
                <option value="{{indeks + 1}}" selected>{{indeks + 1}}</option>
                % else:
                <option value="{{indeks + 1}}">{{indeks + 1}}</option>
                % end
                % end
            </select>
            <div class="d-grid">
                <button class="btn btn-dark besedilo" type="submit">Potrdi</button>
            </div>
        </form>
    </div>
</div>