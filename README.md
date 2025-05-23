# RSS Podcast Downloader

A modern, user-friendly desktop application for downloading podcast episodes from RSS feeds. Built with Python and ttkbootstrap for a beautiful interface, this app allows you to:

- Add and save podcast RSS feeds
- View and search episodes
- Download episodes with a single click
- Queue multiple downloads (no waiting for one to finish)
- Automatically tag MP3s with episode and podcast metadata
- Embed cover art in downloaded files
- Track your most-used podcasts

## Features
- **Modern UI:** Built with ttkbootstrap for a dark, responsive look
- **Download Queue:** Click 'Download' on as many episodes as you want; downloads are queued and processed in the background
- **Metadata & Cover Art:** MP3s are tagged with title, artist, album, date, and cover art
- **Feed Management:** Save, delete, and quickly access your favorite podcasts
- **Progress Bars & Notifications:** See download progress and get desktop notifications when downloads complete

## Requirements
- Python 3.8+
- [ttkbootstrap](https://ttkbootstrap.readthedocs.io/)
- [mutagen](https://mutagen.readthedocs.io/)
- [Pillow](https://python-pillow.org/)
- [notifypy](https://pypi.org/project/notifypy/)

Install dependencies with:

```
pip install ttkbootstrap mutagen Pillow notifypy
```

## Usage
1. Run the script:
   ```
   python Podcasts2.py
   ```
2. Enter a podcast RSS feed URL or use one of the suggestions.
3. Click 'Fetch Feed' to load episodes.
4. Click 'Download' on any episode(s) you want. Downloads will queue and process in the background.
5. Downloaded files are saved in the current directory, tagged and with cover art.

## Database
- Podcast feeds are saved in a local SQLite database (`infopod.db`).
- The app tracks how often you use each feed and shows your top 5 most-used feeds for quick access.

## Notes
- The app is Windows-friendly but should work on any OS with Python and the required packages.
- If you encounter issues with feeds or downloads, check the status bar for error messages.

## License
MIT License

---

Enjoy your podcasts!
