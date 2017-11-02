#!/bin/bash

URL_NEHNUTELNOSTI="http://www.nehnutelnosti.sk/bratislavsky-kraj?p%5Bcategories%5D%5Bids%5D=10000.10001.10002.10003.10004.10005.10006.10007.10008.20001.20002.20003.20004.20005.20006.20007.30001.30002.30003.30004.60001.60002.60003.60004.60005.60006.60007.60008.60009.60010.60011.60012.60013.60014.60015.60016&p[limit]=60"
DATAFILE="nehnutelnosti.data"

wget -O - --header="User-Agent: Mozilla/5.0 (Windows NT 5.1; rv:23.0) Gecko/20100101 Firefox/23.0" \
	--header="Accept: image/png,image/*;q=0.8,*/*;q=0.5" \
	--header="Accept-Language: en-US,en;q=0.5" --header="Accept-Encoding: gzip, deflate" "$URL_NEHNUTELNOSTI" | gunzip - > $DATAFILE
sleep 1

PAGE=1

while [ $PAGE -lt 15 ];
do
	PAGE=$((PAGE+1))
	URL="${URL_NEHNUTELNOSTI}&p[page]=${PAGE}"

	wget -O - --header="User-Agent: Mozilla/5.0 (Windows NT 5.1; rv:23.0) Gecko/20100101 Firefox/23.0" \
		-w 10 --random-wait \
		--header="Accept: image/png,image/*;q=0.8,*/*;q=0.5" \
		--header="Accept-Language: en-US,en;q=0.5" --header="Accept-Encoding: gzip, deflate" "$URL" | gunzip - >> $DATAFILE

	cat ${DATAFILE} | ./parse-listing_nehnutelnosti.py | grep update_date | sed '''s/.*u\(.*\),$/\1/''' | sed "s/'//g" | ./delta-time.py 2;

	if [ $? -eq 1 ]; then
		exit 0
	fi
done

exit 1
