# Download and open the NASA Image of the day (iotd)
# Download to a path $TargetFolder (relative to this script's location)
# https://www.nasa.gov/multimedia/imagegallery/iotd.html

param
(
	[string]$TargetFolder = "images"
)

$ErrorActionPreference = "Stop"

# Get the most recent item from NASA's RSS feed
$rssFeed = [xml](Invoke-WebRequest "https://www.nasa.gov/rss/dyn/lg_image_of_the_day.rss")
$PageUrl = $rssFeed.rss.channel.item[0].link
echo "PageUrl = $PageUrl"
$mostRecentItem = (Invoke-WebRequest $PageUrl) 

# Find the image in the page
$ImageOfTheDay = $mostRecentItem.AllElements | Where-Object {$_.tagName -eq "meta" -and $_.OuterHTML -like "*og:image*"}
$ImageUrl = $ImageOfTheDay.content
echo "ImageUrl = $ImageUrl"

# Set the absolute target file path
$FileName = $ImageUrl.SubString($ImageUrl.LastIndexOf('/') + 1)
$AbsolutePath = Join-Path $PSScriptRoot ($TargetFolder)
$TargetFilePath = Join-Path $AbsolutePath ($FileName)

if (!(test-path($TargetFilePath)))
{
	# Download
	echo "Downloading $TargetFilePath"
	mkdir $AbsolutePath -Force | Out-Null
	Invoke-WebRequest $ImageUrl -OutFile $TargetFilePath

	# Open locally with the default app
	start $TargetFilePath
} else {
	echo "Target file already exists"
}

exit
