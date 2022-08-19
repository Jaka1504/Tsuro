<!DOCTYPE html>
<html lang="si">
  <head>
    <title>{{title}}</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-0evHe/X+R7YkIZDRvuzKMRqM+OrBnVFBL6DOitfPri4tjfHxaWutUpFmBp4vmVor" crossorigin="anonymous">
    <link href="/static/style.css" rel="stylesheet">
  </head>
  <body class="bg-dark text-light">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.0-beta1/dist/js/bootstrap.bundle.min.js" integrity="sha384-pprn3073KE6tl6bjs2QrFaJGz5/SUsLqktiwsUTF55Jfv3qYSDhgCecCxMW52nD2" crossorigin="anonymous"></script>
    <div class="row">
      <div class="col" style="text-align:right">
        <img src="/img/zmaj.png" alt="Zmaj" class="sticky-top" width="80%" style="filter:invert()">
      </div>
      <div class="col">
        <nav class="navbar navbar-expand-xl sticky-top">
          <div class="container-fluid">
            <a class="navbar-brand text-light" href="/">
              <!-- <img src="/img/napis_tsuro.png" alt="Tsuro" height="24" class="d-inline-block align-text-top"> -->
              Tsuro
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
              <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
              <ul class="navbar-nav">
                <li class="nav-item">
                  <a class="nav-link active text-light" aria-current="page" href="#">Začetna stran</a>
                </li>
                <li class="nav-item dropdown">
                  <a class="nav-link dropdown-toggle text-light" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
                    Igra
                  </a>
                  <ul class="dropdown-menu bg-secondary">
                    <li><a class="dropdown-item text-light" href="#">Trenutna igra</a></li>
                    <li><a class="dropdown-item text-light" href="#">Nova igra</a></li>
                    <li><a class="dropdown-item text-light" href="#">Pregled mojih iger</a></li>
                  </ul>
                </li>
                <li class="nav-item">
                  <a class="nav-link text-light" href="#">Statistika</a>
                </li>
              </ul>
            </div>
          </div>
        </nav>
        {{!base}}
      </div>
      <div class="col">
        <img src="/img/feniks.png" alt="Feniks" class="sticky-top" width="100%" style="filter:invert()">
      </div>
    </div>
  </body>
</html>