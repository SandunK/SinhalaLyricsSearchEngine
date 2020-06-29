from flask import Flask, redirect, url_for, request, render_template
from elasticsearch import Elasticsearch
import sys

sys.path.append('../sinling-master')
from sinling import SinhalaTokenizer, preprocess, word_joiner, word_splitter

app = Flask(__name__)
tokenizer = SinhalaTokenizer()
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

music_by_list = [ 'සංගීතමය', 'සංගීතවත්','අධ්‍යක්ෂණය', 'සංගීත','තනු']
lyrics_by_list = ['ලියා', 'ලියූ', 'ලිව්ව', 'ලිව්', 'රචනා',  'ලියා ඇති', 'රචිත', 'ලියන ලද','ලියන', 'හදපු', 'පද', 'රචනය', 'හැදූ', 'හැදුව', 'ලියන', 'ලියන්න','ලීව', 'ලියපු', 'ලියා ඇත', 'ලිඛිත']
genre_list = ['පැරණි', 'පොප්ස්','පොප්','පරණ','ක්ලැසික්','ක්ලැසි','ඉල්ලීම','චිත්‍රපට','නව', 'වර්ගයේ', 'අයත්', 'වර්ගයට' ]
artist_list = ['ගේ', 'කීව', 'කී', 'ගායනා කරන', 'ගයන', 'ගායනා','‌ගේ', 'හඩින්', 'කියනා', 'කිව්ව', 'කිව්', 'කිව', 'ගායනය', 'ගායනා කළා', 'ගායනා කල', 'ගැයූ']
super_list = ['සුපිරි', 'නියම', 'පට්ට','ඉහළම', 'හොඳ', 'හොඳම', 'එලකිරි', 'එළකිරි', 'සුප්පර්', 'සුප්රකට', 'ඉහල',  'වැඩිපුර', 'වැඩිපුරම', 'සුප්‍රකට', 'ජනප්රිය', 'ජනප්රියම', 'ජනප්‍රිය', 'ජනප්‍රියම', 'ප්‍රකට', 'ප්‍රසිද්ධ']
neglect_list = ["ගීත", "සින්දු"]


@app.route('/', methods=['GET'])
def main():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    boosting_list = ["lyrics"]
    query_request = request.form["query"].strip()
    token_list = tokenizer.tokenize(query_request)
    popular = False

    for token in token_list:

        if (token in genre_list):
            boosting_list.append("genre_si^2")
        else:
            boosting_list.append("genre_si")
        if (token in lyrics_by_list):
            boosting_list.append("composer_si^2")
            token_list.remove(token)
        else:
            boosting_list.append("composer_si")
        if (token in music_by_list):
            boosting_list.append("music_si^2")
            token_list.remove(token)
        else:
            boosting_list.append("music_si")

        if (token in super_list):
            popular = True
            token_list.remove(token)

        if (token in neglect_list):
            token_list.remove(token)

        if (token in artist_list):
            boosting_list.append("artist_si^2")
            token_list.remove(token)
        else:
            boosting_list.append("artist_si")




    processed_query_request = " ".join(token_list)

    boosting_list = list(dict.fromkeys(boosting_list))
    print(query_request)
    print(token_list)
    print(processed_query_request)
    print(boosting_list)

    if (popular):
        print(popular)
        boosted_query = es.search(index="sinhalalyrics", body=
        {"query": {
            "query_string": {
                "query": processed_query_request,
                "fields": ["artist_si", "composer_si", "genre_si", "music_si","views^5"],
                "default_operator": "OR"
            }
        },
            "sort": [{
                "views": "desc"
            }
            ]
        })
    else:
        boosted_query = es.search(index="sinhalalyrics", body=
        {"query": {
            "query_string": {
                "query": processed_query_request,
                "fields": boosting_list,
                "default_operator": "OR"
            }
        }
        }

                                  )

    # boosted_query=es.search(index='sinhalalyrics', size= 1000, body={'query': {'match': {'genre_si': 'පොප්'}}})
    hits = boosted_query["hits"]["hits"]
    if (len(hits) == 0):
        return render_template('index.html', result="No search result exists")
    lyrcs_list = [lyrics["_source"] for lyrics in hits]
    return render_template('index.html', results=lyrcs_list)


if __name__ == '__main__':
    app.run(debug=True)
