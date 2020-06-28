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
    with open("lyricsObj.json", encoding="utf8") as input:
        lyrics_data = json.load(input)

    print ("Data mapping started ...")
    for song in lyrics_data:
        efunc.store_record(es, index_name, songId, song)
        songId += 1
    print("Data was mapped successfully")

    # search data
    # print (len(es.search(index=index_name, size= 1000, body={'query': {'match': {'genre_en': 'Old Pops'}}})['hits']['hits']))


if __name__ == '__main__':
    main()
