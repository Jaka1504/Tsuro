<div class="tabela">
	<table cellspacing="0" cellpadding="0">
		% for st_vrstice in range(1, velikost_tabele[0] + 1):
			<tr class="karta">
				% for st_stolpca in range(1, velikost_tabele[1] + 1):
					<td class="karta">
						<div class="karta" draggable="true">
							% karta = tabela[(st_vrstice, st_stolpca)]
							% if karta is not None:
								% for krivulja in karta.prikaz_povezav():
									%if krivulja[3] == bela:
										<img src="/img/{{krivulja[0]}}{{krivulja[1]}}.png" alt="pot {{krivulja[0]}}{{krivulja[1]}}" width="100px" class="povezava bela_povezava" style="--rot: {{(-90 * krivulja[2]) % 360}}deg;">
									%elif krivulja[3] == siva:
										<img src="/img/{{krivulja[0]}}{{krivulja[1]}}.png" alt="pot {{krivulja[0]}}{{krivulja[1]}}" width="100px" class="povezava siva_povezava" style="--rot: {{(-90 * krivulja[2]) % 360}}deg;">
									%else:
										<img src="/img/{{krivulja[0]}}{{krivulja[1]}}.png" alt="pot {{krivulja[0]}}{{krivulja[1]}}" width="100px" class="povezava barvna_povezava" style="--rot: {{(-90 * krivulja[2]) % 360}}deg; --hue: {{krivulja[3]}}deg;">
									%end
								% end
							<img src="/img/ozadje.png" alt="ozadje" width="100px">
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
