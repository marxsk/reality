all:
	@echo "nehnutelnosti | topreality"

nehnutelnosti.data:
	./download-nehnutelnosti.sh

topreality.data:
	./download-topreality.sh