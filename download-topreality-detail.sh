#!/bin/bash
for i in `cat def.url`; do 
	wget -O - --header="User-Agent: Mozilla/5.0 (Windows NT 5.1; rv:23.0) Gecko/20100101 Firefox/23.0" \
		 --header="Accept: image/png,image/*;q=0.8,*/*;q=0.5" \
		--header="Accept-Language: en-US,en;q=0.5" --header="Accept-Encoding: gzip, deflate" $i | gunzip | \
	./parse-detail_topreality.py $i;
	sleep 1s;
done
