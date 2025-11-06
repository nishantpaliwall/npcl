param(
    [string]$jsonPath
)

# Read JSON file
$paths = Get-Content -Raw -Path $jsonPath | ConvertFrom-Json

if ($paths.Count -eq 0) {
    Write-Host "No media files found in JSON."
    exit
}

Write-Host "Loaded $($paths.Count) media files."

# Filter valid existing files
$validPaths = @()
foreach ($path in $paths) {
    if (Test-Path $path) {
        $validPaths += $path
    } else {
        Write-Host "Skipping missing file: $path"
    }
}

if ($validPaths.Count -eq 0) {
    Write-Host "No valid files found. Exiting."
    exit
}

Write-Host "Starting slideshow for $($validPaths.Count) files..."

# Create argument list with all file paths, escaped for PowerShell
$quotedPaths = $validPaths | ForEach-Object { "`"$($_)`"" }
$argList = $quotedPaths -join " "

# Launch Photos app with all the files
Start-Process "explorer.exe" $argList

Write-Host "Slideshow launched successfully!"