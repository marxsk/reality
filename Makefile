CITY=borsky-svaty-jur
TYPE=pozemky

#CITY=pezinok
#TYPE=domy
URL="http://www.nehnutelnosti.sk/$(CITY)/$(TYPE)"

# získaj listing stránku (single) 
# @todo: paging
$(TYPE):
	wget -O - --header="User-Agent: Mozilla/5.0 (Windows NT 5.1; rv:23.0) Gecko/20100101 Firefox/23.0" --header="Accept: image/png,image/*;q=0.8,*/*;q=0.5" --header="Accept-Language: en-US,en;q=0.5" --header="Accept-Encoding: gzip, deflate" $(URL) | gunzip - > $(TYPE)
