param
(
	[string]$WallpaperStyle = "22",
    [string]$TileImage = "0"
)

# RefreshWallpaper from: https://kelleymd.wordpress.com/2015/01/10/update-wallpaper-image/
function RefreshWallpaper ($wallpaper)
{
  Add-Type 'using System;using System.Runtime.InteropServices;using Microsoft.Win32;namespace Wallpaper{public class UpdateImage{[DllImport("user32.dll", SetLastError = true, CharSet = CharSet.Auto)]private static extern int SystemParametersInfo (int uAction, int uParam, string lpvParam, int fuWinIni);public static void Refresh(string path) {SystemParametersInfo( 20, 0, path, 0x01 | 0x02 ); }}}'

  [Wallpaper.UpdateImage]::Refresh($wallpaper)
}

# set regedit key for wallpaper style (22 = span)
Set-ItemProperty -Path 'HKCU:\Control Panel\Desktop' -Name WallpaperStyle -Value $WallpaperStyle -Force

# set TileImage if requested
if ($TileImage -eq "1") {
    Set-ItemProperty -Path 'HKCU:\Control Panel\Desktop' -Name TileWallpaper -Value $TileImage -Force
}

# Refresh
$CurrentWallpaper = (Get-ItemProperty -Path 'HKCU:\Control Panel\Desktop' -Name WallPaper).WallPaper
RefreshWallpaper $CurrentWallPaper
