# Nasa Images

Python Scripts to download images from NASA feeds, typically updated daily:

---

Usage:

1. get an api key here https://api.nasa.gov/
2. `cp .env.example .env`
3. set `API_KEY` in `.env`
4. `python -m venv venv && pip install -r requirements.txt`
5. `. ./get-images.sh`

---

Modules:

- `iotd.py` | Image Of the Day | https://www.nasa.gov/image-of-the-day/
  - no authentication required

- `apod.py` | Astronomy Picture of the Day | https://apod.nasa.gov/apod/
  - requires an api key

---

Notes:
- when images are found, they will be downloaded to `./images/`
- sometimes the article doesn't have an image, and instead is a video

---

Suggestions and contributions are welcome.
