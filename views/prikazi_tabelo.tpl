<div class="table tabela">
	<table cellspacing="0" cellpadding="0">
		% for st_vrstice in range(1, velikost_tabele[0] + 1):
			<tr class="karta">
				% for st_stolpca in range(1, velikost_tabele[1] + 1):
					<td class="karta">
						<div class="karta" draggable="true">
							% karta = igra.tabela[(st_vrstice, st_stolpca)]
							% if karta is not None:
								% include("prikazi_karto.tpl")
							%	else:
							<img src="/img/ozadje.png" alt="ozadje" width="100px" class="ni_postavljena_karta">
							% end
						</div>
					</td>
				% end
			</tr>
		% end
	</table>
	% odmiki = [(-16, 50), (16, 50), (50, 16), (50, -16), (16, -50), (-16, -50), (-50, -16), (-50, 16)]
	% for i, igralec in enumerate(igra.igralci):
		%	vrstica, stolpec = igralec.polje
		%	polozaj = igralec.polozaj
		<img src="/img/igralec.png" alt="igralec" width="100px" class="igralec" style="--hue: {{barve[i]}}deg; --odmik_y: {{100 * (vrstica - 1) + odmiki[polozaj][1]}}px; --odmik_x: {{100 * (stolpec - 1) + odmiki[polozaj][0]}}px;">
	% end
</div>
