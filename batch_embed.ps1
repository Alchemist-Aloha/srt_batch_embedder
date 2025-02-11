param (
    [string]$directory
)

# Prompt for input if no directory is provided
if (-not $directory) {
    $directory = Read-Host "Enter the directory containing M4V and SRT files"
}

# Verify if the directory exists
if (-not (Test-Path -Path $directory -PathType Container)) {
    Write-Host "Error: Directory not found: $directory" -ForegroundColor Red
    exit 1
}

# Get all M4V and SRT files in the directory
$videos = Get-ChildItem -Path $directory -Filter "*.m4v" | ForEach-Object { $_.BaseName, $_.FullName } | ConvertFrom-Csv -Header "BaseName", "Path"
$subtitles = Get-ChildItem -Path $directory -Filter "*.srt" | ForEach-Object { $_.BaseName, $_.FullName } | ConvertFrom-Csv -Header "BaseName", "Path"

# Match videos with their corresponding subtitles
$matchedPairs = @{}
foreach ($video in $videos) {
    foreach ($subtitle in $subtitles) {
        if ($video.BaseName -eq $subtitle.BaseName) {
            $matchedPairs[$video.Path] = $subtitle.Path
        }
    }
}

# Process each matched pair
foreach ($pair in $matchedPairs.GetEnumerator()) {
    $videoPath = $pair.Key
    $subtitlePath = $pair.Value
    $outputPath = [System.IO.Path]::ChangeExtension($videoPath, "_subtitled.mp4")

    Write-Host "Processing: $videoPath with subtitles $subtitlePath"

    # FFmpeg command to embed subtitles
    $ffmpegCmd = "ffmpeg -i `"$videoPath`" -i `"$subtitlePath`" -c copy -c:s mov_text `"$outputPath`""

    try {
        Invoke-Expression $ffmpegCmd
        Write-Host "✅ Subtitle embedded successfully: $outputPath" -ForegroundColor Green
    } catch {
        Write-Host "❌ Error embedding subtitles for: $videoPath" -ForegroundColor Red
    }
}

Write-Host "Batch processing complete!" -ForegroundColor Cyan
