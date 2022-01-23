import os
import time
import requests
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class SpotiAuth:

    @staticmethod
    def currently_playing(token):
        current_song_url = 'https://api.spotify.com/v1/me/player/currently-playing'
        player_url = 'https://api.spotify.com/v1/me/player'
        try:
            # current_song_data = requests.get(current_song_url, headers={"Authorization": f"Bearer {token}"}).json()
            player_data = requests.get(player_url, headers={"Authorization": f"Bearer {token}"}).json()
            song_name = player_data.get('item', {}).get('name')
            artist_name_data = []
            artist_name_data.extend(player_data.get('item', {}).get('artists'))
            artist_name = [i['name'] for i in artist_name_data if 'name' in i]
            is_playing = player_data.get('is_playing')
            time_elapsed = player_data.get('progress_ms')
            total_time = player_data.get('item', {}).get('duration_ms')
            time_left = total_time - time_elapsed
            return song_name, artist_name[0], is_playing, time_left
        except json.decoder.JSONDecodeError:
            song_name = 'JSONDecodeError'
            artist_name = ['']
            is_playing = True
            time_left = 10000
            return song_name, artist_name[0], is_playing, time_left
        except TypeError:
            song_name = 'TypeError'
            artist_name = ['']
            is_playing = True
            time_left = 10000
            return song_name, artist_name[0], is_playing, time_left


class WebScraper:
    def __init__(self):
        pass

    @staticmethod
    def query_cleaner(query1):
        if '/' in query1:
            query1 = query1.replace('/', ' ')
            if '   ' in query1:
                query1 = query1.replace('   ', ' ')
        if ',' in query1:
            query1 = query1.replace(',', '')
        if "'" in query1:
            query1 = query1.replace("'", '')
        if 'ó' in query1:
            query1 = query1.replace('ó', 'o')
        if 'ō' in query1:
            query1 = query1.replace('ō', 'o')
        if '&' in query1:
            query1 = query1.replace("&", 'and')
        if ':' in query1:
            query1 = query1.replace(":", '')
        if '.' in query1:
            query1 = query1.replace('.', '')
        if '(' in query1:
            query1 = query1.replace('(', '')
        if ')' in query1:
            query1 = query1.replace(')', '')
        if 'ü' in query1:
            query1 = query1.replace('ü', 'u')
        if 'ğ' in query1:
            query1 = query1.replace('ğ', 'g')
        if 'ö' in query1:
            query1 = query1.replace('ö', 'o')
        if 'ç' in query1:
            query1 = query1.replace('ç', 'c')
        if 'ş' in query1:
            query1 = query1.replace('ş', 's')
        if 'ı' in query1:
            query1 = query1.replace('ı', 'i')
        query1 = query1.strip()
        return query1

    @staticmethod
    def lyrics_method_iterator(song, artist):
        lyrics = WebScraper.get_lyrics_songlyrics_soup(song, artist)
        source = "songlyrics.com"
        if len(lyrics) < 2:
            # lyrics string is empty, try another method
            lyrics = WebScraper.get_lyrics_genius_soup(song, artist)
            source = "genius.com"
            if len(lyrics) < 2:
                # lyrics string is empty, try another method
                lyrics = WebScraper.get_lyrics_az_soup(song, artist)
                source = "azlyrics.com"
                if len(lyrics) < 2:
                    # lyrics string is empty, try another method
                    lyrics = WebScraper.get_lyrics_lyricsdb_soup(song, artist)
                    source = "lyricsdb.co"
                    if len(lyrics) < 2:
                        # lyrics string is empty, try another method
                        lyrics = WebScraper.get_lyrics_lyricsmania_soup(song, artist)
                        source = "lyricsmania.com"
                        if len(lyrics) < 2:
                            # it's ok, just give up
                            lyrics = f"Could not find lyrics."
                            source = "N/A"
        retrieved_song = song
        return lyrics, source, retrieved_song

    @staticmethod
    def get_lyrics_genius_soup(song_name2, artist_name2):
        songname = song_name2.split(' - ')[0]
        query = artist_name2 + ' ' + songname
        query1 = WebScraper.query_cleaner(query)
        query2 = query1.replace(' ', '-').lower()
        url = f"https://genius.com/{query2}-lyrics"
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                     "Chrome/90.0.4430.212 Safari/537.36"
        headers = {'user-agent': user_agent}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        time.sleep(2)
        try:
            result = soup.body.find('div', class_='lyrics')
            lyrics = result.p.text.strip()
        except AttributeError:
            lyrics = ""
        return lyrics

    @staticmethod
    def get_lyrics_songlyrics_soup(song_name2, artist_name2):
        try:
            song_name2 = song_name2.split(' - ')[0]
            if " & " in song_name2:
                song_name2.replace(" & ", "")
            if " & " in artist_name2:
                artist_name2.replace(" & ", "")
            artist_name = WebScraper.query_cleaner(artist_name2)
            songname3 = WebScraper.query_cleaner(song_name2)
            songname_final = songname3.replace(' ', '-').lower()
            artistname_final = artist_name.replace(' ', '-').lower()

            url = f"http://www.songlyrics.com/{artistname_final}/{songname_final}-lyrics/"
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                         "Chrome/90.0.4430.212 Safari/537.36"
            headers = {'user-agent': user_agent}
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            lyrics = soup.find(id='songLyricsDiv').text.strip()
            if "do not have the lyrics for" in lyrics:
                lyrics = ""
            elif "Sorry, we have no" in lyrics:
                lyrics = ""
            return lyrics
        except AttributeError:
            lyrics = ""
            return lyrics

    @staticmethod
    def get_lyrics_lyricsdb_soup(song_name2, artist_name2):
        try:
            song_name2 = song_name2.split(' - ')[0]
            artist_name = WebScraper.query_cleaner(artist_name2)
            songname3 = WebScraper.query_cleaner(song_name2)
            songname_final = songname3.replace(' ', '+').lower()
            artistname_final = artist_name.replace(' ', '+').lower()
            url = f"http://www.lyricsdb.co/{artistname_final}/{songname_final}"
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                         "Chrome/90.0.4430.212 Safari/537.36"
            headers = {'user-agent': user_agent}
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            lyrics = soup.find(id='lyric').text.strip()
            with open('song_lyric.txt', 'w', encoding='utf-16') as txt_file:
                txt_file.write(lyrics)
            with open('song_lyric.txt', 'r', encoding='utf-16') as txt_file:
                lines = txt_file.readlines()
            with open('song_lyric.txt', 'w', encoding='utf-16') as txt_file:
                txt_file.writelines(lines[18:-25])
            with open('song_lyric.txt', 'r', encoding='utf-16') as txt_file:
                lyric = txt_file.readlines()
                lyrics = ""
                for line in lyric:
                    lyrics += line
            os.remove("song_lyric.txt")
        except AttributeError:
            lyrics = ""
        return lyrics

    @staticmethod
    def get_lyrics_lyricsmania_soup(song_name2, artist_name2):
        try:
            song_name2 = song_name2.split(' - ')[0]
            artist_name = WebScraper.query_cleaner(artist_name2)
            songname3 = WebScraper.query_cleaner(song_name2)
            songname_final = songname3.replace(' ', '_').lower()
            artistname_final = artist_name.replace(' ', '_').lower()
            url = f"http://www.lyricsmania.com/{songname_final}_lyrics_{artistname_final}.html"
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                         "Chrome/90.0.4430.212 Safari/537.36"
            headers = {'user-agent': user_agent}
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            lyrics = soup.find(class_='lyrics-body').text.strip()
        except AttributeError:
            lyrics = ""
        return lyrics

    @staticmethod
    def get_lyrics_az_soup(song_name2, artist_name2):
        try:
            song_name2 = song_name2.split(' - ')[0]
            artistname3 = WebScraper.query_cleaner(artist_name2)
            songname3 = WebScraper.query_cleaner(song_name2)
            songname3 = songname3.replace("+", "")
            artistname3 = artistname3.replace("+", "")
            songname_final = songname3.replace(" ", "").lower()
            artistname_final = artistname3.replace(" ", "").lower()
            url = f"http://www.azlyrics.com/lyrics/{artistname_final}/{songname_final}.html"
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                         "Chrome/90.0.4430.212 Safari/537.36"
            headers = {'user-agent': user_agent}
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            lyrics = soup.body.text.strip()
            with open('song_lyric.txt', 'w', encoding='utf-16') as txt_file:
                txt_file.write(lyrics)
            with open('song_lyric.txt', 'r', encoding='utf-16') as txt_file:
                lines = txt_file.readlines()
            with open('song_lyric.txt', 'w', encoding='utf-16') as txt_file:
                txt_file.writelines(lines[88:-102])
            with open('song_lyric.txt', 'r', encoding='utf-16') as txt_file:
                lyric = txt_file.readlines()
                for line in lyric:
                    if "Submit Corrections" in line:
                        with open('song_lyric.txt', 'w', encoding='utf-16') as txt_file2:
                            txt_file2.writelines(lyric[:-48])
            with open('song_lyric.txt', 'r', encoding='utf-16') as txt_file:
                lyric = txt_file.readlines()
                lyrics = ""
                for line in lyric:
                    lyrics += line
            os.remove("song_lyric.txt")
        except AttributeError:
            lyrics = ""
        return lyrics


class ChordScraper:
    def __init__(self):
        pass

    @staticmethod
    def query_cleaner(query1):
        if ',' in query1:
            query1 = query1.replace(',', '')
        if "'" in query1:
            query1 = query1.replace("'", '')
        if 'ó' in query1:
            query1 = query1.replace('ó', 'o')
        if '&' in query1:
            query1 = query1.replace("&", 'and')
        if ':' in query1:
            query1 = query1.replace(":", '')
        if '.' in query1:
            query1 = query1.replace('.', '')
        if '(' in query1:
            query1 = query1.replace('(', '')
        if ')' in query1:
            query1 = query1.replace(')', '')
        if 'ü' in query1:
            query1 = query1.replace('ü', 'u')
        if 'ğ' in query1:
            query1 = query1.replace('ğ', 'g')
        if 'ö' in query1:
            query1 = query1.replace('ö', 'o')
        if 'ç' in query1:
            query1 = query1.replace('ç', 'c')
        if 'ş' in query1:
            query1 = query1.replace('ş', 's')
        if 'ı' in query1:
            query1 = query1.replace('ı', 'i')
        query1 = query1.strip()
        query1 = query1.lower()
        return query1

    @staticmethod
    def search_string_creator(song, artist):
        song = ChordScraper.query_cleaner(song)
        if " - " in song:
            ind = song.index(" - ")
            song = song[:ind]
        if " (" in song:
            ind = song.index(" (")
            song = song[:ind]
        artist = ChordScraper.query_cleaner(artist)
        if " and" in artist:
            ind = artist.index(" and")
            artist = artist[:ind]
        ulti_search_words = []
        nsong = song.split(" ")
        nartist = artist.split(" ")
        for word in nsong:
            ulti_search_words.append(word)
        for word in nartist:
            ulti_search_words.append(word)
        search_term = ""
        for word in ulti_search_words:
            search_term += f"{word}%20"
        search_term_final = search_term[:-3:]
        return search_term_final

    @staticmethod
    def chord_entry_selector(search_term_final):
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                     "Chrome/90.0.4430.212 Safari/537.36"
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument(f'user-agent={user_agent}')
        ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
        # chrome_options.add_argument('--disable-gpu')  # is this necessary?
        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

        driver.get(f"https://www.ultimate-guitar.com/search.php?search_type=title&value={search_term_final}")
        try:
            WebDriverWait(driver, 20, ignored_exceptions=ignored_exceptions) \
                .until(EC.presence_of_element_located((By.CLASS_NAME, "_3uKbA")))
        except TimeoutException:
            print("Timeout Exception Occured in chord_entry_selector")
            chord_link = ""
            return driver, chord_link
        tabs_list = driver.find_elements(By.CLASS_NAME, "_3uKbA")
        tabs_list_only_chords = []
        time.sleep(0.3)
        for tab in tabs_list:
            try:
                WebDriverWait(driver, 20, ignored_exceptions=ignored_exceptions) \
                    .until(EC.presence_of_element_located((By.CLASS_NAME, "_2Fdo4")))
                tab_type = tab.find_element(By.CLASS_NAME, "_2Fdo4").text
                if "ords" in tab_type:
                    tabs_list_only_chords.append(tab)
                else:
                    pass
            except NoSuchElementException:
                pass
            except StaleElementReferenceException:
                print("StaleElementReferenceException Raised")
            except TimeoutException:
                print("Timeout Exception Occured in chord_entry_selector #2")
        tabs_list_5star = []
        tabs_list_4halfstar = []
        tabs_list_4star = []
        tabs_list_3halfstar = []
        for tab in tabs_list_only_chords:
            rating_selector = tab.find_elements(By.CLASS_NAME, "_1foT2")
            star_full = 0
            star_half = 0
            star_empty = 0
            for star in rating_selector:
                starclass = star.get_attribute('class')
                if 'A5Qy' in starclass:
                    star_empty += 1
                elif '3f1m' in starclass:
                    star_half += 1
                else:
                    star_full += 1
            if star_full == 5:
                tabs_list_5star.append(tab)
            elif star_full == 4 and star_half == 1:
                tabs_list_4halfstar.append(tab)
            elif star_full == 4 and star_half == 0:
                tabs_list_4star.append(tab)
            elif star_full == 3 and star_half == 1:
                tabs_list_3halfstar.append(tab)
            else:
                pass

        if len(tabs_list_5star) != 0:
            if len(tabs_list_5star) == 1:
                chord_link = tabs_list_5star[0].find_element(By.CSS_SELECTOR, "a._3DU-x.JoRLr._3dYeW").get_attribute(
                    "href")
                return driver, chord_link
            else:
                times_rated = []
                for tab in tabs_list_5star:
                    rating_count = tab.find_element(By.CLASS_NAME, "zNNoF").text
                    if ',' in rating_count:
                        rating_count = rating_count.replace(",", "")
                    times_rated.append(int(rating_count))
                index_of_highest_rated = times_rated.index(max(times_rated))
                chord_link = tabs_list_5star[index_of_highest_rated].find_element(By.CSS_SELECTOR, "a._3DU-x.JoRLr._3dYeW").get_attribute(
                    "href")
                return driver, chord_link
        elif len(tabs_list_4halfstar) != 0:
            if len(tabs_list_4halfstar) == 1:
                chord_link = tabs_list_4halfstar[0].find_element(By.CSS_SELECTOR, "a._3DU-x.JoRLr._3dYeW").get_attribute(
                    "href")
                return driver, chord_link
            else:
                times_rated = []
                for tab in tabs_list_4halfstar:
                    rating_count = tab.find_element(By.CLASS_NAME, "zNNoF").text
                    if ',' in rating_count:
                        rating_count = rating_count.replace(",", "")
                    times_rated.append(int(rating_count))
                index_of_highest_rated = times_rated.index(max(times_rated))
                chord_link = tabs_list_4halfstar[index_of_highest_rated].find_element(By.CSS_SELECTOR, "a._3DU-x.JoRLr._3dYeW").get_attribute(
                    "href")
                return driver, chord_link
        elif len(tabs_list_4star) != 0:
            if len(tabs_list_4star) == 1:
                chord_link = tabs_list_4star[0].find_element(By.CSS_SELECTOR, "a._3DU-x.JoRLr._3dYeW").get_attribute(
                    "href")
                return driver, chord_link
            else:
                times_rated = []
                for tab in tabs_list_4star:
                    rating_count = tab.find_element(By.CLASS_NAME, "zNNoF").text
                    if ',' in rating_count:
                        rating_count = rating_count.replace(",", "")
                    times_rated.append(int(rating_count))
                index_of_highest_rated = times_rated.index(max(times_rated))
                chord_link = tabs_list_4star[index_of_highest_rated].find_element(By.CSS_SELECTOR, "a._3DU-x.JoRLr._3dYeW").get_attribute(
                    "href")
                return driver, chord_link
        elif len(tabs_list_3halfstar) != 0:
            if len(tabs_list_3halfstar) == 1:
                chord_link = tabs_list_3halfstar[0].find_element(By.CSS_SELECTOR, "a._3DU-x.JoRLr._3dYeW").get_attribute(
                    "href")
                return driver, chord_link
            else:
                times_rated = []
                for tab in tabs_list_3halfstar:
                    rating_count = tab.find_element(By.CLASS_NAME, "zNNoF").text
                    if ',' in rating_count:
                        rating_count = rating_count.replace(",", "")
                    times_rated.append(int(rating_count))
                index_of_highest_rated = times_rated.index(max(times_rated))
                chord_link = tabs_list_3halfstar[index_of_highest_rated].find_element(By.CSS_SELECTOR, "a._3DU-x.JoRLr._3dYeW").get_attribute(
                    "href")
                return driver, chord_link
        else:
            print("No decent chords were found.")
            chord_link = ""
            return driver, chord_link

    @staticmethod
    def chords_retriever(driver, chordlink):
        if len(chordlink) < 2:
            html_source_text = "Sorry, no decent chords were found."
            source = ""
            driver.close()
        else:
            driver.get(chordlink)
            article_xpath = '/html/body/div[1]/div[2]/main/div[2]/article/div[1]/div/article/section[3]'
            try:
                html_source_text = driver.find_element(By.XPATH, article_xpath).get_attribute("innerHTML")
            except NoSuchElementException:
                html_source_text = "Sorry, no decent chords were found."
            driver.close()
            source = "ultimate-guitar.com"
        return html_source_text, source

    @staticmethod
    def get_chords(song, artist):
        search_term1 = ChordScraper.search_string_creator(song, artist)
        driver, chord_link = ChordScraper.chord_entry_selector(search_term1)
        html_source_text, source = ChordScraper.chords_retriever(driver, chord_link)
        retrieved_song = song
        return html_source_text, retrieved_song, source
