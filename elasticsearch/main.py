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

    print ("Data mapping started ...")
    for song in lyrics_data:
        efunc.store_record(es, index_name, songId, song)
        songId += 1
        print(songId)
        print (song)
    print("Data was mapped successfully")

    # search data
    # print (len(es.search(index=index_name, size= 1000, body={'query': {'match': {'genre_en': 'Old Pops'}}})['hits']['hits']))
    # print (es.search(index=index_name, size= 1000, body={"query" : {
    #               "query_string" : {
    #                     "query" : 'වික්ටර් රත්නායක ගීත',
    #                     "fields" : ['genre_si', 'composer_si', 'music_si', 'artist_si', 'artist_si^2'],
    #                     "default_operator": "OR"
    #               }}})['hits']['hits'])
    # #
    # # result = es.search(index="lyrics", doc_type="doc", body={"query": {"match": {"genre": "පොප්"}}})
    # for token in ['වික්ටර්', 'රත්නායක', 'ගැයූ', 'ඉහළම', 'ගීත']:
    #     print(token)

if __name__ == '__main__':
    main()

