# Nasa Images

Powershell Scripts to download images from NASA feeds, typically updated daily: 

---

- `iotd.ps1` | Image Of the Day | https://www.nasa.gov/image-of-the-day/
  - no authentication required

- `apod.ps1` | Astronomy Picture of the Day | https://apod.nasa.gov/apod/  
  - requires an api key 
    1.  you can get one here https://api.nasa.gov/
    2.  then put it in a file in the project root called `./ApiKey.txt`

- `RefreshWallpaper.ps1`
  - after setting a new image as desktop background, the fit reverts to "Fill". 
  - if you prefer to span images across multiple monitors, this will set the fit to "Span"

---

Notes: 
- when images are found, they will be downloaded to `./images/`
- sometimes the article doesn't have an image, and instead is a video

---

Suggestions and contributions are welcome.

