$baseDir = "h:\2nd-Brain"
$logDir = Join-Path $baseDir "05_日誌"
$projectDir = Join-Path $baseDir "01_プロジェクト\ippo-experience-hub"
$dataFile = Join-Path $projectDir "data\dashboard.json"
$latestLog = Get-ChildItem -Path $logDir -Filter "*.md" | Where-Object { $_.Name -match "\d{4}-\d{2}-\d{2}" } | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if (-not $latestLog) { exit }
$content = [System.IO.File]::ReadAllText($latestLog.FullName, [System.Text.Encoding]::UTF8)
$rank = "N/A"
$score = 0
$rocketStatus = "No updates."
$lines = $content -split "`n"
foreach ($l in $lines) {
    $line = $l.Trim()
    if ($line.Contains(" / 100)")) {
        $idxScoreOpen = $line.IndexOf("(")
        $idxScoreClose = $line.IndexOf(" / 100)")
        if ($idxScoreOpen -ge 4 -and $idxScoreClose -gt $idxScoreOpen) {
            $score = [int]($line.Substring($idxScoreOpen + 1, $idxScoreClose - $idxScoreOpen - 1).Trim())
            $rank = $line.Substring($idxScoreOpen - 4, 1)
        }
    }
    if ($line.Contains("Artemis II") -and $line.Contains(":")) {
        $idxColon = $line.IndexOf(":")
        if ($idxColon -ge 0) { $rocketStatus = $line.Substring($idxColon + 1).Trim("- ").Trim() }
    }
}
$json = "{`"date`": `"$((Get-Date).ToString('yyyy.MM.dd'))`", `"starry_sky`": { `"rank`": `"$rank`", `"score`": $score }, `"rocket`": { `"mission`": `"Artemis II`", `"status`": `"$rocketStatus`" } }"
if (-not (Test-Path (Split-Path $dataFile))) { New-Item -ItemType Directory -Path (Split-Path $dataFile) -Force }
[System.IO.File]::WriteAllText($dataFile, $json, [System.Text.Encoding]::UTF8)
Write-Output "Done"
