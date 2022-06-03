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