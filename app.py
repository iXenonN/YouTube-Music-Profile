import base64
from colorthief import ColorThief
import firebase_admin
from firebase_admin import credentials, storage
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from io import BytesIO
from lxml import etree
import numpy as np
import os
from PIL import Image, ImageDraw, ImageFont
import re
import requests
import time
import urllib
from ytmusicapi import YTMusic

ytmusic = YTMusic('YOUR BROWSER.JSON FILE')

cred = credentials.Certificate('YOUR FIREBASE CRED JSON FILE')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'YOUR FIREBASE PROJECT URL'
})

YouTube_Music_is_opened = None

app = Flask(__name__)
CORS(app)

@app.route('/status', methods=['POST'])
def receive_status():
    global YouTube_Music_is_opened
    status = request.json.get('status')
    print(f"YouTube Music status: {status}")
    if status == "Off":
        YouTube_Music_is_opened = False
        print(YouTube_Music_is_opened)
        recent_songs = ytmusic.get_history()

        playback = recent_songs[0]

        recent_song_vid_id = recent_songs[0]['videoId']
        recent_song = ytmusic.get_song(recent_song_vid_id)
        recent_song_title = recent_songs[0]['title']

        recent_song_artist = recent_song['videoDetails']['author']

        recent_song_thumbnail_url = recent_song['videoDetails']['thumbnail']['thumbnails'][-1]['url']
        print(recent_song_title, recent_song_vid_id)

        dominant_color = get_dominant_color_from_thumbnail(recent_song_thumbnail_url)
        hex_color = rgb_to_hex(dominant_color)
        print("Dominant color (HEX):", hex_color)
        old_color = "#eb2121"

        
        update_svg_with_data_recently_played("themes/recentlyPlayed.svg", "themes/YouTube_Music_UI_BAR_UPDATED.svg", recent_song_title, recent_song_artist, recent_song_thumbnail_url, hex_color)

        bucket_name = "what-am-i-listening"
        source_file_name = "themes/YouTube_Music_UI_BAR_UPDATED.svg"
        destination_blob_name = "listening-on-ytmusic.svg"
        
        bucket = storage.bucket()
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_filename(source_file_name)

        blob.make_public()

        print(f"Public URL: {blob.public_url}")
        return jsonify({'message': 'SVG changed', 'url': blob.public_url}), 200
        
    elif status == "Open":
        YouTube_Music_is_opened = True
        print(YouTube_Music_is_opened)
        recent_songs = ytmusic.get_history()

        playback = recent_songs[0]

        recent_song_vid_id = recent_songs[0]['videoId']
        recent_song = ytmusic.get_song(recent_song_vid_id)
        recent_song_title = recent_songs[0]['title']

        recent_song_artist = recent_song['videoDetails']['author']

        recent_song_thumbnail_url = recent_song['videoDetails']['thumbnail']['thumbnails'][-1]['url']
        print(recent_song_title, recent_song_vid_id)

        dominant_color = get_dominant_color_from_thumbnail(recent_song_thumbnail_url)
        hex_color = rgb_to_hex(dominant_color)
        print("Dominant color (HEX):", hex_color)
        old_color = "#eb2121"

        
        update_svg_with_data("themes/YouTube_Music_UI.svg", "themes/YouTube_Music_UI_UPDATED.svg", recent_song_title, recent_song_artist, recent_song_thumbnail_url, hex_color)
        overwrite_bar_background("themes/YouTube_Music_UI_UPDATED.svg", "themes/YouTube_Music_UI_BAR_UPDATED.svg", old_color, hex_color)

        bucket_name = "what-am-i-listening"
        source_file_name = "themes/YouTube_Music_UI_BAR_UPDATED.svg"
        destination_blob_name = "listening-on-ytmusic.svg"
        
        bucket = storage.bucket()
        blob = bucket.blob(destination_blob_name)

        blob.upload_from_filename(source_file_name)

        blob.make_public()

        print(f"Public URL: {blob.public_url}")
        return jsonify({'message': 'SVG changed', 'url': blob.public_url}), 200
        

    print("ÇIKTI")    
    return "Stataus received", 200


def download_and_resize_image_base64(image_url, size=(300, 300)):
    
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    img = img.resize(size, Image.LANCZOS)
    
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return f"data:image/png;base64,{img_base64}"


def get_dominant_color_from_thumbnail(thumbnail_url):
    response = requests.get(thumbnail_url)
    img = BytesIO(response.content)
    
    color_thief = ColorThief(img)
    dominant_color = color_thief.get_color(quality=1)
    
    return dominant_color

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

def check_file_content(output_file):
    try:
        with open(output_file, 'r', encoding='utf-8') as file:
            content = file.read()
            print("Güncellenmiş Dosya İçeriği:")
            print(content)
    except Exception as e:
        print(f"Dosya okunurken bir hata oluştu: {e}")


def overwrite_bar_background(svg_file, output_file, old_color, new_color):
    try:
        with open(svg_file, 'r', encoding='utf-8') as file:
            svg_content = file.read()

        style_block = f"""
.bar {{
    background: {new_color};
    bottom: 1px;
    height: 3px;
    position: absolute;
    width: 3px;
    animation: sound 0ms -800ms linear infinite alternate;
}}
"""

        updated_svg_content = re.sub(r'\.bar\s*\{[^}]*\}', style_block, svg_content)

        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(updated_svg_content)

        print(f"Bar color in SVG file succesfully changed to {new_color} color.")
    
    except Exception as e:
        print(f"An error occured while try to change bar color: {e}")


def update_svg_with_data(svg_file, output_file, song_title, artist_name, new_thumbnail_url, new_color):

    global YouTube_Music_is_opened
    
    ns = {
        'svg': 'http://www.w3.org/2000/svg',
        'xhtml': 'http://www.w3.org/1999/xhtml'
    }
    tree = etree.parse(svg_file)
    root = tree.getroot()

    base64_thumbnail = download_and_resize_image_base64(new_thumbnail_url)

    style_element = root.find(".//{http://www.w3.org/1999/xhtml}style")
            
    for element in root.findall(".//xhtml:div[@class='artist']", namespaces=ns):
        if "Rose of Sharyn" in element.text:
            element.text = song_title  
            print("Song name updated")
        elif song_title in element.text:
            element.text = song_title
            print("Song name updated")

    for element in root.findall(".//xhtml:div[@class='song']", namespaces=ns):
        if "The Neighbourhood" in element.text:
            element.text = artist_name  
            print("Artist updated")
        elif song_title in element.text:
            element.text = artist_name
            print("Artist updated")
            
    for element in root.findall(".//xhtml:a[@target='_BLANK']//xhtml:img", namespaces=ns):
        if 'src' in element.attrib:
            element.attrib['src'] = base64_thumbnail
            print("Thumbnail updated")

    if YouTube_Music_is_opened is True:
        song_status = "Now playing on"
        print(song_status)
        for element in root.findall(".//xhtml:div[@class='playing']", namespaces=ns):
            if "Recently played on" in element.text:
                element.text = "Now playing on"
                print("'playing' status updated")
        
    elif YouTube_Music_is_opened is False:
        song_status = "Recently played on"
        print(song_status)
        for element in root.findall(".//xhtml:div[@class='playing']", namespaces=ns):
            if "Now playing on" in element.text:
                element.text = "Recently played on"  
                print("'playing' status updated")
            

    tree.write(output_file, pretty_print=True)

def update_svg_with_data_recently_played(svg_file, output_file, song_title, artist_name, new_thumbnail_url, new_color):

    global YouTube_Music_is_opened
    
    ns = {
    'svg': 'http://www.w3.org/2000/svg',
    'xlink': 'http://www.w3.org/1999/xlink',
    'xhtml': 'http://www.w3.org/1999/xhtml'
    }
    tree = etree.parse(svg_file)
    root = tree.getroot()

    base64_thumbnail = download_and_resize_image_base64(new_thumbnail_url)
            
    for element in root.findall(".//xhtml:div[@class='artist']", namespaces=ns):
        if "See You Again (feat. Charlie Puth)" in element.text:
            element.text = song_title  
            print("Song name updated")
        elif song_title in element.text:
            element.text = song_title
            print("Song name updated")

    for element in root.findall(".//xhtml:div[@class='song']", namespaces=ns):
        if "Wiz Khalifa" in element.text:
            element.text = artist_name  
            print("Artist updated")
        elif song_title in element.text:
            element.text = artist_name
            print("Artist updated")
            
    for element in root.findall(".//xhtml:a[@target='_BLANK']//xhtml:img", namespaces=ns):
        if 'src' in element.attrib:
            element.attrib['src'] = base64_thumbnail
            print("Thumbnail updated")
    
    if YouTube_Music_is_opened is True:
        song_status = "Now playing on"
        print(song_status)
        for element in root.findall(".//xhtml:div[@class='playing']", namespaces=ns):
            if "Recently played on" in element.text:
                element.text = "Now playing on"
                print("'playing' status updated")
        
    elif YouTube_Music_is_opened is False:
        song_status = "Recently played on"
        print(song_status)
        for element in root.findall(".//xhtml:div[@class='playing']", namespaces=ns):
            if "Now playing on" in element.text:
                element.text = "Recently played on"  
                print("'playing' status updated")
            

    tree.write(output_file, pretty_print=True)

def update_svg_with_data_Theme_2(svg_file, output_file, song_title, artist_name, new_thumbnail_url, new_color):

    global YouTube_Music_is_opened
    
    ns = {
        'svg': 'http://www.w3.org/2000/svg',
        'xhtml': 'http://www.w3.org/1999/xhtml'
    }
    tree = etree.parse(svg_file)
    root = tree.getroot()

    base64_thumbnail = download_and_resize_image_base64(new_thumbnail_url)

    style_element = root.find(".//{http://www.w3.org/1999/xhtml}style")
            
    for element in root.findall(".//xhtml:div[@class='artist']", namespaces=ns):
        if "See You Again (feat. Charlie Puth)" in element.text:
            element.text = song_title  
            print("Song name updated")
        elif song_title in element.text:
            element.text = song_title
            print("Song name updated")

    for element in root.findall(".//xhtml:div[@class='song']", namespaces=ns):
        if "Wiz Khalifa" in element.text:
            element.text = artist_name  
            print("Artist updated")
        elif song_title in element.text:
            element.text = artist_name
            print("Artist updated")
            
    for element in root.findall(".//xhtml:a[@target='_BLANK']//xhtml:img", namespaces=ns):
        if 'src' in element.attrib:
            element.attrib['src'] = base64_thumbnail
            print("Thumbnail updated")

    if YouTube_Music_is_opened is True:
        song_status = "Now playing on"
        print(song_status)
        for element in root.findall(".//xhtml:div[@class='playing']", namespaces=ns):
            if "Recently played on" in element.text:
                element.text = "Now playing on"
                print("'playing' status updated")
        
    elif YouTube_Music_is_opened is False:
        song_status = "Recently played on"
        print(song_status)
        for element in root.findall(".//xhtml:div[@class='playing']", namespaces=ns):
            if "Now playing on" in element.text:
                element.text = "Recently played on"  
                print("'playing' status updated")
            

    tree.write(output_file, pretty_print=True)

def update_svg_with_data_Theme_Slider(svg_file, output_file, song_title, artist_name, new_thumbnail_url, new_color):

    global YouTube_Music_is_opened
    
    ns = {
        'svg': 'http://www.w3.org/2000/svg',
        'xhtml': 'http://www.w3.org/1999/xhtml'
    }
    tree = etree.parse(svg_file)
    root = tree.getroot()

    base64_thumbnail = download_and_resize_image_base64(new_thumbnail_url)

    style_element = root.find(".//{http://www.w3.org/1999/xhtml}style")
            
    for element in root.findall(".//xhtml:div[@class='song scrolling']", namespaces=ns):
        if "See You Again (feat. Charlie Puth)" in element.text:
            element.text = song_title  
            print("Song name updated")
        elif song_title in element.text:
            element.text = song_title
            print("Song name updated")

    for element in root.findall(".//xhtml:div[@class='artist']", namespaces=ns):
        if "Whiz Khalifa" in element.text:
            element.text = artist_name  
            print("Artist updated")
        elif song_title in element.text:
            element.text = artist_name
            print("Artist updated")
            
    for element in root.findall(".//xhtml:a[@target='_BLANK']//xhtml:img", namespaces=ns):
        if 'src' in element.attrib:
            element.attrib['src'] = base64_thumbnail
            print("Thumbnail updated")

    if YouTube_Music_is_opened is True:
        song_status = "Now playing on"
        print(song_status)
        for element in root.findall(".//xhtml:div[@class='playing']", namespaces=ns):
            if "Recently played on" in element.text:
                element.text = "Now playing on"
                print("'playing' status updated")
        
    elif YouTube_Music_is_opened is False:
        song_status = "Recently played on"
        print(song_status)
        for element in root.findall(".//xhtml:div[@class='playing']", namespaces=ns):
            if "Now playing on" in element.text:
                element.text = "Recently played on"  
                print("'playing' status updated")
            

    tree.write(output_file, pretty_print=True)

def update_svg_with_data_Theme_Horizontal_Slider(svg_file, output_file, song_title, artist_name, new_thumbnail_url, new_color):

    global YouTube_Music_is_opened
    
    ns = {
        'svg': 'http://www.w3.org/2000/svg',
        'xhtml': 'http://www.w3.org/1999/xhtml'
    }
    tree = etree.parse(svg_file)
    root = tree.getroot()

    base64_thumbnail = download_and_resize_image_base64(new_thumbnail_url)

    style_element = root.find(".//{http://www.w3.org/1999/xhtml}style")
            
    for element in root.findall(".//xhtml:div[@class='song scrolling']", namespaces=ns):
        if "See You Again (feat. Charlie Puth)" in element.text:
            element.text = song_title  
            print("Song name updated")
        elif song_title in element.text:
            element.text = song_title
            print("Song name updated")

    for element in root.findall(".//xhtml:div[@class='artist']", namespaces=ns):
        if "Whiz Khalifa" in element.text:
            element.text = artist_name  
            print("Artist updated")
        elif song_title in element.text:
            element.text = artist_name
            print("Artist updated")
            
    for element in root.findall(".//xhtml:a[@target='_BLANK']//xhtml:img", namespaces=ns):
        if 'src' in element.attrib:
            element.attrib['src'] = base64_thumbnail
            print("Thumbnail updated")

    if YouTube_Music_is_opened is True:
        song_status = "Now playing on"
        print(song_status)
        for element in root.findall(".//xhtml:div[@class='playing']", namespaces=ns):
            if "Recently played on" in element.text:
                element.text = "Now playing on"
                print("'playing' status updated")
        
    elif YouTube_Music_is_opened is False:
        song_status = "Recently played on"
        print(song_status)
        for element in root.findall(".//xhtml:div[@class='playing']", namespaces=ns):
            if "Now playing on" in element.text:
                element.text = "Recently played on"  
                print("'playing' status updated")
            

    tree.write(output_file, pretty_print=True)

def update_svg_with_data_Theme_Horizontal_Slider_Without_Bars(svg_file, output_file, song_title, artist_name, new_thumbnail_url, new_color):

    global YouTube_Music_is_opened
    
    ns = {
        'svg': 'http://www.w3.org/2000/svg',
        'xhtml': 'http://www.w3.org/1999/xhtml'
    }
    tree = etree.parse(svg_file)
    root = tree.getroot()

    base64_thumbnail = download_and_resize_image_base64(new_thumbnail_url)
            
    for element in root.findall(".//xhtml:div[@class='song scrolling']", namespaces=ns):
        if "See You Again (feat. Charlie Puth)" in element.text:
            element.text = song_title  
            print("Song name updated")
        elif song_title in element.text:
            element.text = song_title
            print("Song name updated")

    for element in root.findall(".//xhtml:div[@class='artist']", namespaces=ns):
        if "Whiz Khalifa" in element.text:
            element.text = artist_name  
            print("Artist updated")
        elif song_title in element.text:
            element.text = artist_name
            print("Artist updated")
            
    for element in root.findall(".//xhtml:a[@target='_BLANK']//xhtml:img", namespaces=ns):
        if 'src' in element.attrib:
            element.attrib['src'] = base64_thumbnail
            print("Thumbnail updated")

    if YouTube_Music_is_opened is True:
        song_status = "Now playing on"
        print(song_status)
        for element in root.findall(".//xhtml:div[@class='playing']", namespaces=ns):
            if "Recently played on" in element.text:
                element.text = "Now playing on"
                print("'playing' status updated")
        
    elif YouTube_Music_is_opened is False:
        song_status = "Recently played on"
        print(song_status)
        for element in root.findall(".//xhtml:div[@class='playing']", namespaces=ns):
            if "Now playing on" in element.text:
                element.text = "Recently played on"  
                print("'playing' status updated")
            

    tree.write(output_file, pretty_print=True)

if __name__ == '__main__':
        app.run(port=5000)
