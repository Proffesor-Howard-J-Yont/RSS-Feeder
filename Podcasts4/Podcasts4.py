from customtkinter import CTk, set_appearance_mode, set_default_color_theme, CTkFrame, CTkLabel, CTkProgressBar

set_appearance_mode('dark')
set_default_color_theme('blue')

root = CTk()
root.title('RSS Podcast Downloader')
root.geometry('1300x800')

loadframe = CTkFrame(root)
loadframe.place(relx=0.5, rely=0.4, anchor='center')

loadinglabel = CTkLabel(loadframe, text='RSS Podcasts', font=('Calibri', 30))
loadinglabel.pack(pady=5)

pbload = CTkProgressBar(loadframe, mode='determinate', width=300)
pbload.pack(pady=10)
pbload.start()

root.update()

from customtkinter import *
pbload.set(pbload.get()+.01587)
root.update()

import requests
pbload.set(pbload.get()+.01587)
root.update()

import xml.etree.ElementTree as ET
pbload.set(pbload.get()+.01587)
root.update()

import io
pbload.set(pbload.get()+.01587)
root.update()

import re
pbload.set(pbload.get()+.01587)
root.update()

import os
pbload.set(pbload.get()+.01587)
root.update()

import subprocess
pbload.set(pbload.get()+.01587)
root.update()

import sys
pbload.set(pbload.get()+.01587)
root.update()

import uuid
pbload.set(pbload.get()+.01587)
root.update()

from mutagen.easyid3 import EasyID3
pbload.set(pbload.get()+.01587)
root.update()

from mutagen.mp3 import MP3
pbload.set(pbload.get()+.01587)
root.update()

from mutagen.id3 import ID3, APIC, PictureType, Encoding, COMM, USLT
pbload.set(pbload.get()+.01587)
root.update()

import mutagen
pbload.set(pbload.get()+.01587)
root.update()

from PIL import Image
pbload.set(pbload.get()+.01587)
root.update()

from io import BytesIO
pbload.set(pbload.get()+.01587)
root.update()

import sqlite3 as sql
pbload.set(pbload.get()+.01587)
root.update()

from notifypy import Notify
pbload.set(pbload.get()+.01587)
root.update()

import tempfile
pbload.set(pbload.get()+.01587)
root.update()

import threading
pbload.set(pbload.get()+.01587)
root.update()

import queue
pbload.set(pbload.get()+.01587)
root.update()

import database_handler
pbload.set(pbload.get()+.01587)
root.update()

topbgimage = CTkImage(light_image=Image.open('assets/sunrise.png'), dark_image=Image.open('assets/sunrise.png'), size=(1500, 300))

loadframe.destroy()
# --- FUNCTIONS ---
def clear_board():
    for widget in mainframe.winfo_children():
        widget.destroy()

def confirm_feed(feedurl):
    try:
        response = requests.get(feedurl)
        if response.status_code == 200:
            channel = ET.fromstring(response.content)
            title = channel.find("./channel/title").text if channel.find("./channel/title") is not None else "No Title"
            description = channel.find("./channel/description").text if channel.find("./channel/description") is not None else "No Description"
            image_url = channel.find("./channel/image/url").text if channel.find("./channel/image/url") is not None else None
            image_data = None
            if image_url:
                try:
                    image_response = requests.get(image_url)
                    image_data = image_response.content
                except Exception as e:
                    print(f"Error fetching image: {e}")
            secret_key = str(uuid.uuid4())
            last_checked_number = 0  # Initialize to 0 or fetch from existing data if needed
            database_handler.add_podcast(title, description, image_data, feedurl, 1, secret_key, last_checked_number)
    except Exception as e:
        print(f"Error confirming feed: {e}")


def checknewfeed(feedurl):
    try:
        response = requests.get(feedurl)
        if response.status_code == 200:
            # Try to parse the feed to ensure it's valid
            try:
                channel = ET.fromstring(response.content)
                CTkLabel(mainframe, text='Feed is valid and available!', font=('Calibri', 20), text_color='green').pack(pady=10)
                clear_board()
                new_feed_success_frame = CTkFrame(mainframe, corner_radius=20, height=300, width=500)
                new_feed_success_frame.place(relx=0.5, rely=0.5, anchor='center')
                CTkLabel(new_feed_success_frame, text=channel.find("./channel/title").text, font=('Calibri', 30, 'bold')).grid(row=0, column=1, padx=5, pady=20)
                # Cover image
                cover_url = channel.find("./channel/image/url").text if channel.find("./channel/image/url") is not None else None
                if cover_url:
                    try:
                        cover_response = requests.get(cover_url)
                        cover_image = Image.open(BytesIO(cover_response.content))
                        cover_image = cover_image.resize((150, 150))
                        cover_photo = CTkImage(light_image=cover_image, dark_image=cover_image, size=(100, 100))
                        CTkLabel(new_feed_success_frame, image=cover_photo, text='').grid(row=0, column=0, padx=5, pady=10)
                    except Exception as e:
                        print(f"Error loading cover image: {e}")
                CTkLabel(new_feed_success_frame, text=channel.find("./channel/description").text if channel.find("./channel/description") is not None else "No description available.", font=('Calibri', 15), wraplength=400, justify='left').grid(row=1, column=0, columnspan=2, padx=10)
                bottom_success_frame = CTkFrame(new_feed_success_frame, corner_radius=10)
                bottom_success_frame.grid(row=2, column=0, columnspan=2, pady=20, padx=20)
                confim_new_feed = CTkButton(bottom_success_frame, text='Confirm', font=('Calibri', 20), width=100, command=lambda: (confirm_feed(feedurl), clear_board(), home()))
                confim_new_feed.grid(row=0, column=0, pady=10, padx=20)
                cancel_new_feed = CTkButton(bottom_success_frame, text='Cancel', font=('Calibri', 20), width=100, command=lambda: (clear_board(), home()))
                cancel_new_feed.grid(row=0, column=1, pady=10, padx=20)
            except ET.ParseError:
                CTkLabel(mainframe, text='Feed URL is not a valid RSS feed.', font=('Calibri', 20), text_color='red').pack(pady=10)

        else:
            CTkLabel(mainframe, text='Feed URL is not reachable.', font=('Calibri', 20), text_color='red').pack(pady=10)

    except requests.exceptions.RequestException as e:
        CTkLabel(mainframe, text=f'Error: {e}', font=('Calibri', 20), text_color='red').pack(pady=10)
def add_new_feed():
    clear_board()
    new_feed_frame = CTkFrame(mainframe, corner_radius=20, height=300, width=500)
    new_feed_frame.place(relx=0.5, rely=0.5, anchor='center')

    new_feed_label = CTkLabel(new_feed_frame, text='Enter Feed URL', font=('Calibri', 30, 'bold'))
    new_feed_label.pack(pady=20)

    new_feed_entry = CTkEntry(new_feed_frame, width=350, font=('Calibri', 20))
    new_feed_entry.pack(pady=10)

    bottom_new_feed_frame = CTkFrame(new_feed_frame, corner_radius=10)
    bottom_new_feed_frame.pack(fill='x', side='bottom', pady=20, padx=20)

    new_feed_check_availability_button = CTkButton(bottom_new_feed_frame, text='Check Availability', font=('Calibri', 20), width=100, command=lambda: checknewfeed(new_feed_entry.get()))
    new_feed_check_availability_button.grid(row=0, column=0, pady=10, padx=20)

    new_feed_cancel_button = CTkButton(bottom_new_feed_frame, text='Cancel', font=('Calibri', 20), width=100, command=lambda: (clear_board(), home()))
    new_feed_cancel_button.grid(row=0, column=1, pady=10, padx=20)


def home():
    # --------- Top Bar -------------
    top_frame = CTkFrame(mainframe, corner_radius=0, height=200)
    top_frame.pack(fill='x')

    homeL = CTkLabel(top_frame, text='Home', image=topbgimage, font=('Calibri', 70, 'bold'), justify='left', text_color='white')
    homeL.pack()

    # --------- Suggested Podcast Bar -------------
    suggested_frame = CTkFrame(mainframe, corner_radius=20, height=150)
    suggested_frame.pack(fill='x', pady=10)

    suggestedL = CTkLabel(suggested_frame, text='For You', font=('Calibri', 30, 'bold'), justify='left')
    suggestedL.grid(row=0, column=0, padx=20, pady=10)

    # NEW FEED BUTTON
    newfeedimage = CTkImage(light_image=Image.open('assets/plus_light.png'), dark_image=Image.open('assets/plus_dark.png'), size=(120, 120))
    newfeed_button = CTkButton(suggested_frame, text='New Feed', width=150, height=150, fg_color='transparent', hover_color='gray25', font=('Calibri', 15, 'bold'), image=newfeedimage, compound='top', command=lambda: add_new_feed())
    newfeed_button.grid(row=1, column=0, padx=20, pady=10)

    # SAMPLE PODCAST BUTTON
    #sample_picture = CTkImage(light_image=Image.open('assets/TheMarkLevinShow.png'), dark_image=Image.open('assets/TheMarkLevinShow.png'), size=(120, 120))
    #sample_button = CTkButton(suggested_frame, text='The Mark Levin Show', image=sample_picture, compound='top', width=150, height=150, fg_color='transparent', hover_color='gray25', font=('Calibri', 15, 'bold'), command=lambda: display_podcast('The Mark Levin Show'))
    #sample_button.grid(row=1, column=1, padx=20, pady=10)

    suggested_podcasts = database_handler.get_suggested_podcasts()
    for index, podcast in enumerate(suggested_podcasts):
        podcast_name, podcast_description, podcast_image_data, podcast_feed, podcast_secret_key = podcast
        #print(f'Name: {podcast_name}')
        #print(f'Description: {podcast_description}')
        #print(f'Feed: {podcast_feed}')
        #print(f'Key: {podcast_secret_key}')
        if podcast_image_data:
            try:
                image = Image.open(io.BytesIO(podcast_image_data))
                image = image.resize((120, 120))
                podcast_image = CTkImage(light_image=image, dark_image=image, size=(120, 120))
            except Exception as e:
                print(f"Error loading podcast image: {e}")
                podcast_image = None
        else:
            podcast_image = None

        podcast_button = CTkButton(suggested_frame, text=podcast_name, image=podcast_image, compound='top', width=150, height=150, fg_color='transparent', hover_color='gray25', font=('Calibri', 15, 'bold'), command=lambda key=podcast_secret_key: display_podcast(key))
        podcast_button.grid(row=1, column=index+1, padx=20, pady=10)


    # Show the rest of the podcasts in the database that are not in suggested or recent
    other_podcasts = database_handler.get_other_podcasts()
    if other_podcasts:
        other_frame = CTkFrame(mainframe, corner_radius=20, height=150)
        other_frame.pack(fill='x', pady=10)

        otherL = CTkLabel(other_frame, text='More Podcasts', font=('Calibri', 30, 'bold'), justify='left')
        otherL.grid(row=0, column=1, padx=20, pady=10)

        for index, podcast in enumerate(other_podcasts):
            podcast_name, podcast_description, podcast_image_data, podcast_feed, podcast_secret_key = podcast
            if podcast_image_data:
                try:
                    image = Image.open(io.BytesIO(podcast_image_data))
                    image = image.resize((120, 120))
                    podcast_image = CTkImage(light_image=image, dark_image=image, size=(120, 120))
                except Exception as e:
                    print(f"Error loading podcast image: {e}")
                    podcast_image = None
            else:
                podcast_image = None

            podcast_button = CTkButton(other_frame, text=podcast_name, image=podcast_image, compound='top', width=150, height=150, fg_color='transparent', hover_color='gray25', font=('Calibri', 15, 'bold'), command=lambda podcast_secret_key=podcast_secret_key: display_podcast(podcast_secret_key))
            # If more than 6 podcasts, move to next row
            podcast_button.grid(row=1 + index // 6, column=1 + index % 6, padx=20, pady=10)
    
     # --------- Recent Podcast Bar -------------
    recent_frame = CTkFrame(mainframe, corner_radius=20, height=150)
    recent_frame.pack(fill='x', pady=10)

    recentL = CTkLabel(recent_frame, text='Recently Viewed', font=('Calibri', 30, 'bold'), justify='left')
    recentL.grid(row=0, column=1, padx=20, pady=10)

    recent_podcasts = database_handler.get_recent_podcasts()
    for index, podcast in enumerate(recent_podcasts):
        podcast_name, podcast_description, podcast_image_data, podcast_feed, podcast_secret_key = podcast
        if podcast_image_data:
            try:
                image = Image.open(io.BytesIO(podcast_image_data))
                image = image.resize((120, 120))
                podcast_image = CTkImage(light_image=image, dark_image=image, size=(120, 120))
            except Exception as e:
                print(f"Error loading podcast image: {e}")
                podcast_image = None
        else:
            podcast_image = None

        podcast_button = CTkButton(recent_frame, text=podcast_name, image=podcast_image, compound='top', width=150, height=150, fg_color='transparent', hover_color='gray25', font=('Calibri', 15, 'bold'), command=lambda podcast_name=podcast_name: display_podcast(podcast_secret_key))
        podcast_button.grid(row=1, column=index+1, padx=20, pady=10)


def display_podcast(podcast_secret_key):
    clear_board()
    database_handler.increment_click_count(podcast_secret_key)
    #print('Hello!!')
    #print(podcast_secret_key)

    pod_info = database_handler.grab_podcast(podcast_secret_key)
    if pod_info is None:
        CTkLabel(mainframe, text='Podcast not found.', font=('Calibri', 20), text_color='red').pack(pady=10)
        back_button = CTkButton(mainframe, text='< Back', font=('Calibri', 20), width=100, command=lambda: [clear_board(), home()])
        back_button.pack(pady=10, padx=20, anchor='nw')
        return
    podcast_name = pod_info[0]
    podcast_description = pod_info[1]
    podcast_image_data = pod_info[2]

     # Back Button

    back_button = CTkButton(mainframe, text='< Back', font=('Calibri', 20), width=100, command=lambda: [clear_board(), home()])
    back_button.pack(pady=10, padx=20, anchor='nw')

    info_frame = CTkFrame(mainframe, corner_radius=20, height=300)
    info_frame.pack(fill='x', padx=20, pady=10)

    if podcast_image_data:
        try:
            image = Image.open(io.BytesIO(podcast_image_data))
            image = image.resize((200, 200))
            podcast_image = CTkImage(light_image=image, dark_image=image, size=(200, 200))
            CTkLabel(info_frame, image=podcast_image, text='').grid(row=0, column=0, rowspan=2, padx=20, pady=20)
        except Exception as e:
            print(f"Error loading podcast image: {e}")

    CTkLabel(info_frame, text=podcast_name, font=('Calibri', 30, 'bold')).grid(row=0, column=1, padx=20, pady=20)
    CTkLabel(info_frame, text=podcast_description, font=('Calibri', 15), wraplength=800, justify='left').grid(row=1, column=1, padx=20)

    # Episodes

    CTkLabel(mainframe, text='Latest', font=('Calibri', 30, 'bold')).pack(pady=50)

    # Fetch and display episodes from the feed
    pod_feed = pod_info[4]

    try:
        response = requests.get(pod_feed)
        if response.status_code == 200:
            channel = ET.fromstring(response.content)
            items = channel.findall("./channel/item")
            
            for idx, item in enumerate(items):
                if idx >= 20:
                    break
                display_episode(item, podcast_name)
    except Exception as e:
        print(f"Error fetching feed: {e}")
        CTkLabel(mainframe, text='Failed to fetch episodes.', font=('Calibri', 20), text_color='red').pack(pady=10)

class display_episode:
    def __init__(self, item, podcast_name):
        episode_title = item.find("title").text if item.find("title") is not None else "No Title"
        episode_description = item.find("description").text if item.find("description") is not None else "No Description"
        episode_pubDate = item.find("pubDate").text if item.find("pubDate") is not None else "No Publication Date"
        episode_enclosure = item.find("enclosure")
        episode_audio_url = episode_enclosure.get('url') if episode_enclosure is not None else None
        episode_image = item.find("{http://www.itunes.com/dtds/podcast-1.0.dtd}image")
        episode_image_url = episode_image.get('href') if episode_image is not None else None


        self.episode_frame = CTkFrame(mainframe, corner_radius=10)
        self.episode_frame.pack(fill='both', pady=10, padx=10)

        # Episode Image
        if episode_image_url:
            try:
                image_response = requests.get(episode_image_url)
                image_data = image_response.content
                image = Image.open(BytesIO(image_data))
                image = image.resize((150, 150))
                episode_image_ctk = CTkImage(light_image=image, dark_image=image, size=(150, 150))
                CTkLabel(self.episode_frame, image=episode_image_ctk, text='').grid(row=0, column=0, rowspan=3, padx=10, pady=10)
            except Exception as e:
                print(f"Error loading episode image: {e}")
                
                print(f"Error loading podcast image as fallback: {e}")

        CTkLabel(self.episode_frame, text=episode_title, font=('Calibri', 20, 'bold')).grid(row=0, column=1, sticky='w', padx=10, pady=5)
        CTkLabel(self.episode_frame, text=episode_pubDate, font=('Calibri', 12, 'italic')).grid(row=1, column=1, sticky='w', padx=10)
        CTkLabel(self.episode_frame, text=episode_description, font=('Calibri', 15), wraplength=700, justify='left').grid(row=2, column=1, sticky='w', padx=10, pady=5)
        if episode_audio_url:
             download_button = CTkButton(self.episode_frame, text='Download Episode', font=('Calibri', 15), width=150, command=lambda url=episode_audio_url: self.download_episode(url, podcast_name, episode_title, episode_image_url))
             download_button.grid(row=0, column=2, padx=10, pady=10)                  

        else:
            CTkLabel(mainframe, text='Failed to fetch episodes.', font=('Calibri', 20), text_color='red').pack(pady=10)
    
    def download_episode(self, url, podcast_name, episode_title, episode_image_url):
        def sanitize_filename(name):
            return re.sub(r'[\\/*?:"<>|]', "", name)

        def download_thread(url, podcast_name, episode_title, episode_image_url, progress_queue):
            try:
                response = requests.get(url, stream=True)
                response.raise_for_status()

                total_length = int(response.headers.get('content-length', 0))
                progress_bar = CTkProgressBar(self.episode_frame, width=400)
                progress_bar.grid(row=4, column=0, columnspan=4, sticky='we')
                progress_bar.set(0)
                downloaded = 0

                total_size = int(response.headers.get('content-length', 0))
                block_size = 1024
                downloaded_size = 0

                sanitized_podcast_name = sanitize_filename(podcast_name)
                sanitized_episode_title = sanitize_filename(episode_title)

                podcast_dir = os.path.join(os.getcwd(), 'Podcasts', sanitized_podcast_name)
                os.makedirs(podcast_dir, exist_ok=True)

                file_path = os.path.join(podcast_dir, f"{sanitized_episode_title}.mp3")

                with open(file_path, 'wb') as file:
                    for chunk in response.iter_content(chunk_size=4096):
                        if chunk:
                            file.write(chunk)
                            downloaded += len(chunk)
                            progress = downloaded / total_length if total_length else 0
                            progress_bar.set(progress)
                            root.update()
                progress_bar.set(1)
                # Add metadata
                try:
                    audio = MP3(file_path, ID3=ID3)
                    try:
                        audio.add_tags()
                    except mutagen.id3.error:
                        pass
                    # Use EasyID3 for simple tags
                    try:
                        easy_tags = EasyID3(file_path)
                    except mutagen.id3.ID3NoHeaderError:
                        easy_tags = mutagen.File(file_path, easy=True)
                        easy_tags.add_tags()
                    easy_tags["title"] = episode_title
                    easy_tags["artist"] = podcast_name
                    easy_tags.save()
                    # Add cover image using ID3 APIC frame
                    if episode_image_url:
                        try:
                            image_response = requests.get(episode_image_url)
                            image_data = image_response.content
                            audio.tags.add(
                                APIC(
                                    encoding=3,
                                    mime='image/jpeg',
                                    type=3,
                                    desc='Cover',
                                    data=image_data
                                )
                            )
                        except Exception as e:
                            print(f"Error fetching episode image for metadata: {e}")
                    audio.save()
                except Exception as e:
                    print(f"Error adding metadata: {e}")

                notification = Notify()
                notification.title = "Download Complete"
                notification.message = f"{episode_title} has been downloaded."
                notification.send()

            except Exception as e:
                print(f"Error downloading episode: {e}")
            finally:
                progress_queue.put(None)
        
        download_thread(url, podcast_name, episode_title, episode_image_url, queue.Queue())
                
        
        
# --- Main Application ---
root_color = root.cget("fg_color")
mainframe = CTkScrollableFrame(root, fg_color=root_color)
mainframe.pack(fill='both', expand=True)


home()

root.mainloop()