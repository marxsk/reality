#!/bin/bash

URL_TOPREALITY_TRAIL=".html?searchType=string&cat=&form=0&type%5B%5D=101&type%5B%5D=108&type%5B%5D=102&type%5B%5D=103&type%5B%5D=104&type%5B%5D=105&type%5B%5D=106&type%5B%5D=109&type%5B%5D=110&type%5B%5D=107&type%5B%5D=201&type%5B%5D=202&type%5B%5D=204&type%5B%5D=205&type%5B%5D=206&type%5B%5D=207&type%5B%5D=801&type%5B%5D=802&type%5B%5D=803&type%5B%5D=806&type%5B%5D=807&type%5B%5D=809&type%5B%5D=810&type%5B%5D=811&type%5B%5D=812&type%5B%5D=813&type%5B%5D=814&type%5B%5D=815&type%5B%5D=816&type%5B%5D=817&obec=c100-Bratislavský+kraj&distance=&q=&cena_od=&cena_do=&vymera_od=&vymera_do=&n_search=search&page=estate&gpsPolygon="
URL_TOPREALITY_PAGE="-2"

URL_TOPREALITY_START="https://www.topreality.sk/vyhladavanie-nehnutelnosti"

URL1="${URL_TOPREALITY_START}${URL_TOPREALITY_TRAIL}"

DATAFILE="topreality.data"

wget -O - --header="User-Agent: Mozilla/5.0 (Windows NT 5.1; rv:23.0) Gecko/20100101 Firefox/23.0" \
	--header="Accept: image/png,image/*;q=0.8,*/*;q=0.5" \
	--header="Accept-Language: en-US,en;q=0.5" --header="Accept-Encoding: gzip, deflate" $URL1 | gunzip - > $DATAFILE
sleep 1

PAGE=1

while [ $PAGE -lt 15 ];
do
	PAGE=$((PAGE+1))
	URL="${URL_TOPREALITY_START}-${PAGE}${URL_TOPREALITY_TRAIL}"

	wget -O - --header="User-Agent: Mozilla/5.0 (Windows NT 5.1; rv:23.0) Gecko/20100101 Firefox/23.0" \
		-w 10 --random-wait \
		--header="Accept: image/png,image/*;q=0.8,*/*;q=0.5" \
		--header="Accept-Language: en-US,en;q=0.5" --header="Accept-Encoding: gzip, deflate" "$URL" | gunzip - >> $DATAFILE

	cat ${DATAFILE} | ./parse-listing_topreality.py | grep update_date | sed '''s/.*u\(.*\),$/\1/''' | sed "s/'//g" | ./delta-time.py 2; 

	if [ $? -eq 1 ]; then
		exit 0
	fi
done

exit 1