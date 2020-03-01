# Download and open the Astronomy picture of the day
# Download to target folder $TargetFolder (relative to this script's location)

param
(
	[string]$TargetFolder = "images"
)

$ErrorActionPreference = "Stop"

# Page URL derived from the current date
$date = Get-Date -format "yyMMdd"
$RootUrl = "https://apod.nasa.gov/apod"
$PageUrl = "${RootUrl}/ap${date}.html"
echo "PageUrl = $PageUrl"

# Get the page contents
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$page = (Invoke-WebRequest $PageUrl) 

# Find the image in the page
$ImageOfTheDay = $page.AllElements | Where-Object {$_.tagName -eq "IMG"}
$ShortImageUrl = $ImageOfTheDay.src
if ($ShortImageUrl)
{
	# Get the image url
	$ImageUrl = "${RootUrl}/${ShortImageUrl}"
	echo "ImageUrl = $ImageUrl"

	# Set the absolute target file path
	$AbsolutePath = Join-Path $PSScriptRoot ($TargetFolder)
	$FileName = $ImageUrl.SubString($ImageUrl.LastIndexOf('/') + 1)
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
}
else
{
	# sometimes the picture of the day is a video
	echo "No image found sry"
}

exit
