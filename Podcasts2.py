from ttkbootstrap import Window, Label, Progressbar
root = Window(themename='darkly')
root.title('RSS Podcast Downloader')
root.geometry('900x630')

loading = Label(root, text='Loading...')
loading.pack()

pbload = Progressbar(root, bootstyle='danger striped', maximum=100, mode='determinate', value=0, length=300)
pbload.pack()

root.update()
import requests
pbload['value'] +=5
root.update()
import xml.etree.ElementTree as ET
pbload['value'] +=5
root.update()
import io
pbload['value'] +=5
root.update()
import re
pbload['value'] +=5
root.update()
import os
pbload['value'] +=5
root.update()
import sys
pbload['value'] +=5
root.update()
import uuid
pbload['value'] +=5
root.update()
from mutagen.easyid3 import EasyID3
pbload['value'] +=5
root.update()
from mutagen.mp3 import MP3
pbload['value'] +=5
root.update()
from mutagen.id3 import ID3, APIC, PictureType, Encoding
pbload['value'] +=5
root.update()
import mutagen
pbload['value'] +=5
root.update()
import tkinter as tk
pbload['value'] +=5
root.update()
from PIL import Image
pbload['value'] +=5
root.update()
from io import BytesIO
pbload['value'] +=5
root.update()
Image.CUBIC = Image.BICUBIC
pbload['value'] +=5
root.update()
from ttkbootstrap import *
pbload['value'] +=5
root.update()
from ttkbootstrap.scrolled import ScrolledFrame, ScrolledText
pbload['value'] +=5
root.update()
import sqlite3 as sql
pbload['value'] +=5
root.update()
from notifypy import Notify
pbload['value'] +=5
root.update()
import tempfile
pbload['value'] +=5
root.update()

loading.destroy()
pbload.destroy()

global choice
choice=IntVar()

def begin_fetch():
    global submain, feed_title, episodes, cover_image, episodeloaderSB, statusL, c, conn
    try:
        loadertest = int(episodeloaderSB.get())
    except: 
        statusL.config(text='Please input an integer')
    else:
        feed_title, episodes, cover_image, podcast_description = parse_feed(feedE.get(), max_items=int(episodeloaderSB.get()))
        headerL.config(text=feed_title)
        subheaderL.config(text=podcast_description)
        c.execute("""SELECT * FROM podcasts WHERE name='{}' AND link='{}'""".format(feed_title, feedE.get()))
        cgrabonlyone = c.fetchall()
        if cgrabonlyone == []:
            temp_feedurl = feedE.get()
            c.execute("""INSERT INTO podcasts VALUES('{}', '{}')""".format(feed_title, feedE.get()))
            conn.commit()
            Button(sideF, text=feed_title, command=lambda: (feedE.delete(0, END), feedE.insert(0, temp_feedurl), begin_fetch())).pack(fill='x', padx=3, pady=3)

        try:
            submain.destroy()
        except:
            pass
        submain = Frame(mainF)
        submain.pack(fill='both', expand=True)
        for idx, episode in enumerate(episodes, 1):
                global choice
                title = episode.get("title", "No Title")
                date = episode.get("pubDate", episode.get("published", "No date"))
                summary = episode.get("summary", "No Summary")

                randoF = Frame(submain, bootstyle='secondary')
                randoF.pack(fill='x', padx=10, pady=10)
                hj = ScrolledText(randoF, font=('Calibri light', 10), bootstyle='dark round', height=4, hbar=False, vbar=True, wrap='word')
                hj.pack(side='bottom', pady=5, fill='x')
                hj.insert(0.0, summary)
                Label(randoF, text=f"{idx}. {title}", font=('Calibri', 12, 'bold'), bootstyle='secondary inverse').pack(padx=10, pady=5, side='left')
                
                Button(randoF, text="Download", command=lambda idx=idx: (choice.set(idx), commencedownload())).pack(padx=10, pady=5, side='right')
                root.update()

        root.update()
    
def commencedownload():
    global choice, episodes, feed_title, cover_image
    episode = episodes[choice.get() - 1]
    enclosures = episode.get("enclosures", [])
    media_url = None
    
    for enc in enclosures:
        url = enc.get("url")
        mimetype = enc.get("type", "")
        if url and "audio" in mimetype and ("mp3" in url.lower() or "mpeg" in mimetype):
            media_url = url
    if not media_url and enclosures:
        media_url = enclosures[0].get("url")
    if not media_url:
        statusL.config(text="No valid media URL found for this episode.")
        return
    
    # Generate a more user-friendly filename based on the episode title
    safe_title = re.sub(r'[^\w\-_\. ]', '_', episode.get('title', 'podcast'))[:50]  # Truncate long titles
    filename = f"{safe_title}.mp3"
    
    # Create a more descriptive output filename for easier identification
    if 'pubDate' in episode:
        try:
            date_str = episode['pubDate'][:10].replace('-', '').replace(' ', '')
            filename = f"{date_str}_{safe_title}.mp3"
        except:
            pass
    
    # Debug information
    # print(f"\nDownloading episode: {episode.get('title', 'Unknown')}")
    # print(f"Media URL: {media_url}")
    # print(f"Output filename: {filename}")
    
    # Find episode-specific image if available
    episode_image = None
    # Look for episode-specific image in various formats
    if 'itunes:image' in episode:
        episode_image = episode['itunes:image']
    elif 'image' in episode:
        episode_image = episode['image']
        
    # Try to use episode image first, fall back to podcast image
    image_to_use = episode_image if episode_image else cover_image
    # print(f"Using image: {image_to_use}")
        
    if download_file(media_url, filename):
        set_metadata(filename, episode, feed_title, image_to_use)
    else:
        statusL.config(text="Download failed.")


def parse_feed(rss_feed_url, max_items=20):
    global feed_title, episodes, cover_image, podcast_description
    try:
        response = requests.get(rss_feed_url, stream=True)
        response.raise_for_status()
    except Exception as e:
        statusL.config(text=f"Error retrieving RSS feed: {e}")
        sys.exit(1)

    response.raw.decode_content = True  # Enables decompression if needed
    feed_title = "No Title"
    episodes = []

    statusL.config(text='Loading Episodes...')
    cover_image = None
    inside_channel = False
    current_item = None
    podcast_description = None
    
    # print(f"Starting to parse feed: {rss_feed_url}")

    try:
        for event, elem in ET.iterparse(response.raw, events=("start", "end")):
            tag = elem.tag.split('}', 1)[-1]  # Remove namespace if present

            if event == "start" and tag == "item":
                current_item = {}  # Start a new item
                
            elif event == "end" and tag == "image" and not current_item:
                # Only process channel-level images (not inside an item)
                url_elem = elem.find("url")
                if url_elem is not None:
                    cover_image = url_elem.text
                    # print(f"Found standard podcast image URL: {cover_image}")

            elif event == "end" and tag == "itunes:image" and not current_item:
                # Only process channel-level iTunes images
                cover_image = elem.get("href")
                # print(f"Found iTunes podcast image URL: {cover_image}")
            
            if event == "start" and tag == "channel":
                inside_channel = True  # Enter <channel>

            elif event == "end" and inside_channel and tag == "title":
                feed_title = elem.text.strip() if elem.text else "No Title"
                #inside_channel = False  # Reset after extracting title

            elif event == "end" and inside_channel and tag == "description":
                podcast_description = elem.text.strip() if elem.text else "No Description"
                inside_channel = False  # Reset after extracting description
                
            elif event == "end" and tag == "item":  # Episode processing
                item = current_item if current_item else {}
                
                # Process all child elements of the item
                for child in elem:
                    child_tag = child.tag.split('}', 1)[-1]
                    
                    if child_tag == "enclosure":
                        if "enclosures" not in item:
                            item["enclosures"] = []
                        item["enclosures"].append(child.attrib)
                    elif child_tag == "itunes:image":
                        # Store episode-specific image URL
                        item["itunes:image"] = child.get("href")
                        # print(f"Found episode-specific iTunes image: {item['itunes:image']}")
                    else:
                        if child.text:
                            text = child.text.strip()
                            item[child_tag] = text
                
                episodes.append(item)
                current_item = None  # Reset current item

                statusL.config(text=f"Loading episodes... found {len(episodes)}/{max_items}")
                elem.clear()


                if len(episodes) >= max_items:
                    break  # Stop parsing once max_items is reached

    except Exception as e:
        statusL.config(text=f"Error parsing XML: {e}")
        sys.exit(1)

    if not episodes:
        statusL.config(text="No episodes found in the RSS feed.")
        sys.exit(1)

    return feed_title, episodes, cover_image, podcast_description


def set_metadata(filename, episode, feed_title, cover_image):
    """
    Set basic ID3 metadata tags and embed cover art into the MP3 file.
    Uses multiple approaches to ensure compatibility with different media players.
    """
    try:
        # First set basic metadata with EasyID3
        try:
            audio = EasyID3(filename)
        except mutagen.id3.ID3NoHeaderError:
            # Create ID3 tag if it doesn't exist
            mutagen.id3.ID3().save(filename)
            audio = EasyID3(filename)
        
        # Set standard metadata
        audio['title'] = episode.get('title', 'Unknown Title')
        if 'author' in episode and episode['author']:
            audio['artist'] = episode['author']
        elif feed_title:
            audio['artist'] = feed_title
        else:
            audio['artist'] = "Unknown Artist"
        
        audio['album'] = feed_title if feed_title else "Unknown Album"
        
        pub_date = episode.get('pubDate', episode.get('published', None))
        if pub_date:
            audio['date'] = pub_date
        
        audio.save()
        
        # Now handle album art using both ID3 versions for compatibility
        if cover_image:
            statusL.config(text="Downloading cover art...")
            root.update()
            
            try:
                # Download image
                response = requests.get(cover_image)
                response.raise_for_status()
                image_data = response.content
                
                # Try to optimize the image first
                try:
                    img = Image.open(BytesIO(image_data))
                    # Resize if very large
                    if img.width > 1000 or img.height > 1000:
                        img.thumbnail((800, 800), Image.LANCZOS)
                    
                    # Save optimized JPEG
                    output = BytesIO()
                    img.convert('RGB').save(output, format='JPEG', quality=85)
                    image_data = output.getvalue()
                    #print("Image optimized for embedding")
                except Exception as img_err:
                    print(f"Image optimization failed, using original: {img_err}")
                
                # Load ID3 tags
                audio = ID3(filename)
                
                # Remove any existing images
                for key in list(audio.keys()):
                    if key.startswith('APIC'):
                        del audio[key]
                
                # Add album art with explicit parameters for maximum compatibility
                audio.add(APIC(
                    encoding=Encoding.UTF8,            # UTF-8
                    mime='image/jpeg',                 # JPEG format
                    type=PictureType.COVER_FRONT,      # Front cover (explicitly using enum)
                    desc='Cover',
                    data=image_data
                ))
                
                # Save with v2.3 which has better compatibility
                audio.save(filename, v2_version=3)
                
                # Verify the image was added
                verification = ID3(filename)
                apic_found = False
                for key in verification.keys():
                    if key.startswith('APIC'):
                        apic_found = True
                        #print(f"Verified cover art is present in file ({len(verification[key].data)} bytes)")
                        break
                
                if apic_found:
                    statusL.config(text=f"Album art successfully added to {os.path.basename(filename)}")

                    temp_dir = temp_dir = tempfile.gettempdir()
                    temp_image_path = os.path.join(temp_dir, "temp_notification_image.png")

                    image = Image.open(io.BytesIO(image_data))
                    image.save(temp_image_path)

                    notification = Notify()
                    notification.title = 'Download complete!'
                    notification.message = f'{episode.get('title', 'Unknown Title')} completed downloading and is saved as {os.path.basename(filename)}'
                    notification.icon = temp_image_path
                    notification.send()
                else:
                    statusL.config(text="Warning: Cover art may not have been properly added")
                
                root.update()
                
            except Exception as e:
                statusL.config(text=f"Failed to add cover art: {str(e)}")
                #print(f"Cover art error: {e}")
                root.update()
    
    except Exception as e:
        statusL.config(text=f"Error setting metadata: {str(e)}")
        #print(f"Metadata error: {e}")
        root.update()


def download_file(url, filename):
    """Download file in chunks with a progress indicator and save to filename."""
    statusL.config(text=f"Downloading from {url}...")
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            total_size = r.headers.get("Content-Length")
            if total_size is not None:
                total_size = int(total_size)
            downloaded_size = 0

            with open(filename, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        if total_size:
                            percent = downloaded_size / total_size * 100
                            statusL.config(text=f"Downloading: {percent:6.2f}% complete")
                            pb['value'] = percent
                            root.update()
                        else:
                            statusL.config(text=f"Downloaded: {downloaded_size} bytes")
                            root.update()
            statusL.config(text=f"Download completed and saved as '{filename}'. ({downloaded_size} bytes)")
        return True
    except Exception as e:
        statusL.config(text=f"Error downloading file: {e}")
        return False

global conn, c
conn = sql.connect('infopod.db')
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS podcasts (
    name TEXT,
    link TEXT)""")


# Shows list of rss feeds
outerside = Frame(root)
outerside.pack(fill='y', side='left')

sideF = ScrolledFrame(outerside, width=200, autohide=True)
sideF.pack(fill='both', expand=True)



sideheaderL = Label(sideF, text='Feeds', font=('Calibri', 20, 'bold'))
sideheaderL.pack(pady=15, padx=5)

c.execute('''SELECT * FROM podcasts''')
links_grabber = c.fetchall()

for feedlink in links_grabber:
    Button(sideF, text=feedlink[0], command=lambda feedlink=feedlink: (feedE.delete(0, END), feedE.insert(0, feedlink[1]), begin_fetch())).pack(fill='x', padx=3, pady=3)


if links_grabber == []:
    nonepods = Label(sideF, text='You have no saved podcasts.', font=('Calibri light', 10))
    nonepods.pack(pady=5, padx=5)


# Numberbox to choose how many episodes to display
sideheader2L = Label(outerside, text='Loading 20 episodes', font=('Calibri', 10, 'bold'))
sideheader2L.pack(pady=5, padx=5)

global episodeloaderSB, pb
episodeloaderSB = Spinbox(outerside, bootstyle='danger', from_=1, to=500, command=lambda: sideheader2L.config(text=f'Loading {episodeloaderSB.get()} episodes'))
episodeloaderSB.pack(side='bottom', pady=5)
episodeloaderSB.set(20)

topF = Frame(root)
topF.pack(fill='x', padx=20, pady=10)

headerL = Label(topF, text='Enter RSS Feed', font=('Calibri', 30))
headerL.pack()
def updatewidth(event):
    root.after(50, lambda: subheaderL.config(wraplength=root.winfo_width()-250))
subheaderL = Label(topF, text='', font=('Calibri', 10), wraplength=400)
subheaderL.pack()
root.bind('<Configure>', updatewidth)
feedE = Entry(topF, font=('Calibri', 16))
feedE.pack(fill='x', expand=True, padx=10, pady=10)

Button(feedE, text='Fetch Feed', command=lambda: begin_fetch()).pack(side='right', pady=2)


suggestionsF = Frame(root, bootstyle='secondary')
suggestionsF.pack(fill='x', padx=20, pady=10)

Button(suggestionsF, text='The Mark Levin Show', command=lambda: (feedE.delete(0, END), feedE.insert(0, 'https://feeds.megaphone.fm/mark-levin-podcast'), begin_fetch())).grid(row=0, column=0, padx=3, pady=3)
Button(suggestionsF, text='Joe Rogan Podcast', command=lambda: (feedE.delete(0, END), feedE.insert(0, 'https://feeds.megaphone.fm/GLT1412515089'), begin_fetch())).grid(row=0, column=1, padx=3, pady=3)
Button(suggestionsF, text='LARRY', command=lambda: (feedE.delete(0, END), feedE.insert(0, 'https://www.omnycontent.com/d/playlist/5e27a451-e6e6-4c51-aa03-a7370003783c/744234dd-ebe9-465c-8f0d-b111012fc6d0/195549dc-0ff1-4325-8dfc-b111015d2739/podcast.rss'), begin_fetch())).grid(row=0, column=2, padx=3, pady=3)
Button(suggestionsF, text='Unexplained Mysteries', command=lambda: (feedE.delete(0, END), feedE.insert(0, 'https://feeds.megaphone.fm/END9329892371'), begin_fetch())).grid(row=0, column=3, padx=3, pady=3)


# bottom bar
bottomF = Frame(root)
bottomF.pack(side='bottom', fill='x')

statusL = Label(bottomF, text='Ready', font=('Calibri', 10))
statusL.pack(side='right', pady=5)

pb = Progressbar(bottomF, bootstyle='success striped', maximum=100, mode='determinate', value=0, length=300)
pb.pack(side='left')

# Shows main content
mainF = ScrolledFrame(root)
mainF.pack(fill='both', expand=True)

# Initialize submain as a global variable
submain = None

root.mainloop()