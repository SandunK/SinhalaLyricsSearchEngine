import re
from googletrans import Translator

import scrapy
import json


class LyricsSpider(scrapy.Spider):
    name = "lyricsSpyder"
    jsonLst = []
    count = 0
    start_urls = ['https://sinhalasongbook.com/all-sinhala-song-lyrics-and-chords/?_page=' + str(i) for i in
                  range(1, 23)]

    def parse(self, response):
        songList = (response.xpath(
            '//div[@class="col-md-6 col-sm-6 col-xs-12 pt-cv-content-item pt-cv-1-col"]//a/@href')).extract()
        for song in songList:
            yield scrapy.Request(song, callback=self.parseSong)

    def parseSong(self, response):
        translator = Translator()

        artist = (response.xpath('//div[@class="su-row"]//span[@class="entry-categories"]//a/text()')).extract()
        binder = ','
        artist_en = binder.join(artist)
        artist_si = translator.translate(artist_en, dest='si').text

        genre = (response.xpath('//div[@class="su-row"]//span[@class="entry-tags"]//a/text()')).extract()
        binder = ','
        genre_en = binder.join(genre)
        genre_si = translator.translate(genre_en, dest='si').text

        composer = (response.xpath('//div[@class="su-row"]//span[@class="lyrics"]//a/text()')).extract()
        binder = ','
        composer_en = binder.join(composer)
        composer_si = translator.translate(composer_en, dest='si').text

        music = (response.xpath('//div[@class="su-row"]//span[@class="music"]//a/text()')).extract()
        binder = ','
        music_en = binder.join(music)
        music_si = translator.translate(music_en, dest='si').text

        views_entry = (response.xpath('//div[@class="tptn_counter"]/text()')).get()
        views = int(''.join(filter(str.isdigit, views_entry)))

        lyrics_entry = (response.xpath('//div[@class="entry-content"]//pre/text()')).extract()
        lyrics = self.processLyrics(lyrics_entry)

        data = {"artist_en": artist_en,
                "artist_si": artist_si,
                "genre_en": genre_en,
                "genre_si": genre_si,
                "composer_en": composer_en,
                "composer_si": composer_si,
                "music_en": music_en,
                "music_si": music_si,
                "views": views,
                "lyrics": lyrics}

        self.jsonLst.append(data)
        print(self.count)
        self.count+=1
        yield data

    def processLyrics(self, lyrics):
        lyricsTxt = ''
        for section in lyrics:
            lines = section.split('\n')
            for line in lines:
                result = re.search(r"[a-zA-Z+|]+", line)
                if not result:
                    lyricsTxt += line.strip()
                    lyricsTxt += "\n"
        return lyricsTxt.strip()

    def close(self, reason):
        with open("lyricsObj.json", 'w', encoding="utf8") as outfile:
            json.dump(self.jsonLst, outfile, indent=4, ensure_ascii=False)
