all: nehnutelnosti.sk topreality.sk

topreality.sk: 
	./download-topreality.sh
	cat topreality.data | ./parse-listing_topreality.py csv > topreality-listing.csv
	# detaily
	#cat topreality-listing.csv | awk -F 'Ā' '{print $14}' | tail -n +2 > topreality.url
	#./download-topreality-detail.sh > topreality-detail.csv

nehnutelnosti.sk:
	./download-nehnutelnosti.sh > nehnutelnosti-listing.csv
