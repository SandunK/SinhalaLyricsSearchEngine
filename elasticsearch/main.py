import es_functions as efunc
import json


def main():
    index_name = "sinhalalyrics"
    songId = 0

    # connect into elastic server
    es = efunc.connect_elasticsearch()

    # create index
    print(efunc.create_index(es, index_name))

    # add data into database
    with open("../lyrics_data/lyricsObj.json", encoding="utf8") as input:
        lyrics_data = json.load(input)

    print("Data mapping started ...")
    for song in lyrics_data:
        efunc.store_record(es, index_name, songId, song)
        songId += 1
        print(songId)
        print(song)
    print("Data was mapped successfully")


if __name__ == '__main__':
    main()
