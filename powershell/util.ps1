function GetHDUrl ($PageUrl)
{
	$response = Invoke-WebRequest -Uri $PageUrl -UseBasicParsing
	if ($response.StatusCode -eq 200)
	{
		$responseContent = $response.Content
		$hdurlMatch = ($responseContent.split(",") | select-string("hdurl"))
		if ($hdurlMatch)
		{
			$hdurl = $hdurlMatch.Line -replace '"hdurl":"', '' -replace '"', ''
			return $hdurl
		} else {
			# sometimes the picture of the day is a video
			Throw "hdurl not found sry"
		}
	}
	else
	{
		Throw "invalid response code"
	}
}

function DownloadImage ($ImageUrl, $TargetFolder)
{
	# Set the absolute target file path
	$AbsolutePath = Join-Path $PSScriptRoot $TargetFolder

	$startPosition = $ImageUrl.LastIndexOf('/')
	$FileName = $ImageUrl.SubString($ImageUrl.LastIndexOf('/') + 1)
	$TargetFilePath = Join-Path $AbsolutePath $FileName

	if (!(test-path($TargetFilePath)))
	{
		# Download
		mkdir $AbsolutePath -Force | Out-Null
		Invoke-WebRequest -Uri $ImageUrl -OutFile $TargetFilePath -UseBasicParsing

		# Open locally with the default app
		Start-Process $TargetFilePath

		# Switch the background to span
		# - Want: "Choose a fit" on the Windows Background screen to always be "span"
		# 	- if you choose "set as background" in the images app, it will reset the fit to "fit", and this will subsequently set it to span
		# 	- if you didn't choose a new background, this doesn't do anything, but it doesn't hurt anything either
		. ".\RefreshWallpaper.ps1" -WallpaperStyle 22
	} else {
		Write-Output "Target file already exists"
	}
}
