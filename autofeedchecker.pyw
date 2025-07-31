import sqlite3
import requests
import xml.etree.ElementTree as ET
import os

from notifypy import Notify



DB_PATH = os.path.join(os.path.dirname(__file__), "infopod.db")

def parse_feed(rss_feed_url, max_items=1):
    """Fetch and parse the RSS feed, returning a list of episode dicts."""
    try:
        response = requests.get(rss_feed_url, timeout=10)
        response.raise_for_status()
        root = ET.fromstring(response.content)
        items = []
        for item in root.findall(".//item")[:max_items]:
            title = item.findtext("title", default="No Title")
            pubDate = item.findtext("pubDate", default="")
            guid = item.findtext("guid", default=title+pubDate)  # fallback if no guid
            items.append({"title": title, "pubDate": pubDate, "guid": guid})
        return items
    except Exception as e:
        return []

def main():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("UPDATE podcasts SET last_seen_guid='None'")
    conn.commit()

    # Add a column to store last_seen_guid if not present
    try:
        c.execute("ALTER TABLE podcasts ADD COLUMN last_seen_guid TEXT")
    except sqlite3.OperationalError:
        pass

    c.execute("SELECT rowid, name, link, last_seen_guid, cover_image FROM podcasts WHERE auto_check=1")
    feeds = c.fetchall()
    for rowid, name, link, last_seen_guid, cover_image in feeds:
        episodes = parse_feed(link)
        if not episodes:
            continue
        latest = episodes[0]
        latest_guid = latest["guid"]
        if last_seen_guid != latest_guid:
            # New episode detected
            notification = Notify()
            notification.title = f"New Episode from {name}"
            notification.message = latest["title"]
            if cover_image and os.path.isfile(cover_image):
                notification.icon = cover_image  # Use local file if available
            elif cover_image and cover_image.startswith("http"):
                # Download image to temp file if it's a URL
                import tempfile
                try:
                    img_data = requests.get(cover_image, timeout=10).content
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                        tmp.write(img_data)
                        notification.icon = tmp.name
                except Exception:
                    pass
            notification.send()
            # Update the last_seen_guid in the database
            c.execute("UPDATE podcasts SET last_seen_guid=? WHERE rowid=?", (latest_guid, rowid))
            conn.commit()
    conn.close()



if __name__ == "__main__":
    main()