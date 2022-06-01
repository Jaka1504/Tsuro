<table cellspacing="0" cellpadding="0">
% for st_vrstice in range(1, velikost_tabele[0] + 1):
    <tr class="karta">
% for st_stolpca in range(1, velikost_tabele[1] + 1):
    <td class="karta">
        <div class="karta" draggable="true">
% karta = tabela[(st_vrstice, st_stolpca)]
% if karta is not None:
% for krivulja in karta.prikaz_povezav():
        <img src="/img/{{krivulja[0]}}{{krivulja[1]}}.png" alt="pot {{krivulja[0]}}{{krivulja[1]}}" width="100px" class="potka" style="--rot: {{(-90 * krivulja[2]) % 360}}deg; --hue: 180deg;">
% end
% end
        <img src="/img/ozadje.png" alt="ozadje" width="100px">
        </div>
    </td>
% end
    </tr>
% end
</table>
    