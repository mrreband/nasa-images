# Download and open the NASA Astronomy picture of the day (apod)
# Download to target folder $TargetFolder (relative to this script's location)
# https://apod.nasa.gov/apod/archivepix.html

param
(
	[string]$TargetFolder = "images"
)

$ErrorActionPreference = "Stop"
. ./util.ps1

$api_key = Get-Content("./ApiKey.txt")
$date = Get-Date -format "yyyy-MM-dd"
$RootUrl = "https://api.nasa.gov/planetary/apod"
$PageUrl = "${RootUrl}?api_key=${api_key}&date=${date}"
Write-Output "PageUrl = $PageUrl"

$hdurl = GetHdUrl($PageUrl)
Write-Output "ImageUrl = $hdurl"

DownloadImage($hdurl)
