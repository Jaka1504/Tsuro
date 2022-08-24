<div class="row">
	<div class="col"></div>
	<div class="col tabela brez-robov">
		<table cellspacing="0" cellpadding="0" class="mx-auto">
			% for st_vrstice in range(1, velikost_tabele[0] + 1):
				<tr class="brez-robov">
					% for st_stolpca in range(1, velikost_tabele[1] + 1):
						<td class="brez-robov">
							<div class="brez-robov">
								% karta = igra.tabela[(st_vrstice, st_stolpca)]
								% if karta is not None:
									% include("prikazi_karto.tpl")
								%	else:
								<img src="/img/ozadje.png" alt="ozadje" class="ni-postavljena-karta karta">
								% end
							</div>
						</td>
					% end
				</tr>
			% end
		</table>
		% odmiki = [(-0.6667, 2), (0.6667, 2), (2, 0.6667), (2, -0.6667), (0.6667, -2), (-0.6667, -2), (-2, -0.6667), (-2, 0.6667)]
		% for i, igralec in enumerate(igra.igralci):
			% vrstica, stolpec = igralec.polje
			% polozaj = igralec.polozaj
			<img src="/img/igralec.png" alt="igralec" class="igralec hue karta" style="--hue: {{barve[i]}}deg; --odmik_y: {{4 * (vrstica - 1) + odmiki[polozaj][1]}}vw; --odmik_x: {{4 * (stolpec - 1) + odmiki[polozaj][0]}}vw;">
		% end
	</div>
	<div class="col"></div>
</div>