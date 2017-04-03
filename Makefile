URL_NEHNUTELNOSTI_1="http://www.nehnutelnosti.sk/bratislavsky-kraj?p%5Bcategories%5D%5Bids%5D=10000.10001.10002.10003.10004.10005.10006.10007.10008.20001.20002.20003.20004.20005.20006.20007.30001.30002.30003.30004.60001.60002.60003.60004.60005.60006.60007.60008.60009.60010.60011.60012.60013.60014.60015.60016&p[limit]=60"
URL_NEHNUTELNOSTI_PAGE="[page]="

URL_TOPREALITY="https://www.topreality.sk/vyhladavanie-nehnutelnosti.html?searchType=string&cat=&form=0&type%5B%5D=101&type%5B%5D=108&type%5B%5D=102&type%5B%5D=103&type%5B%5D=104&type%5B%5D=105&type%5B%5D=106&type%5B%5D=109&type%5B%5D=110&type%5B%5D=107&type%5B%5D=201&type%5B%5D=202&type%5B%5D=204&type%5B%5D=205&type%5B%5D=206&type%5B%5D=207&type%5B%5D=801&type%5B%5D=802&type%5B%5D=803&type%5B%5D=806&type%5B%5D=807&type%5B%5D=809&type%5B%5D=810&type%5B%5D=811&type%5B%5D=812&type%5B%5D=813&type%5B%5D=814&type%5B%5D=815&type%5B%5D=816&type%5B%5D=817&obec=c100-Bratislavský+kraj&distance=&q=&cena_od=&cena_do=&vymera_od=&vymera_do=&n_search=search&page=estate&gpsPolygon="
URL_TOPREALITY_PAGE="vyhladavanie-nehnutelnosti-2.html"

## stiahni prvu stranu
## @TODO: stiahni druhu stranu -> ziskaj datumy (+ |tee) -> delta -> $? == 1 ===> skonci (inak max. 100)
## @TODO: extra

$(TYPE):
	wget -O - --header="User-Agent: Mozilla/5.0 (Windows NT 5.1; rv:23.0) Gecko/20100101 Firefox/23.0" --header="Accept: image/png,image/*;q=0.8,*/*;q=0.5" --header="Accept-Language: en-US,en;q=0.5" --header="Accept-Encoding: gzip, deflate" $(URL) | gunzip - > $(TYPE)

