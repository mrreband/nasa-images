function GetHDUrl ($PageUrl)
{
	$response = Invoke-WebRequest -URI $PageUrl
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
		Invoke-WebRequest -Uri $ImageUrl -OutFile $TargetFilePath

		# Open locally with the default app
		Start-Process $TargetFilePath
	} else {
		Write-Output "Target file already exists"
	}
}
