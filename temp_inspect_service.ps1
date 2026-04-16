$paths = @('/openapi.json','/','/verify/','/verify','/retrieve/','/planner/')
foreach ($path in $paths) {
    $url = "http://localhost:8000$path"
    try {
        if ($path -in @('/openapi.json','/')) {
            $resp = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 20
        } else {
            $resp = Invoke-WebRequest -Uri $url -Method POST -Body '{}' -ContentType 'application/json' -UseBasicParsing -TimeoutSec 20
        }
        Write-Host "$path $($resp.StatusCode)"
        if ($path -eq '/openapi.json') {
            $json = $resp.Content | ConvertFrom-Json
            Write-Host "paths: $($json.paths.Keys | Sort-Object -Unique | Out-String)"
        } else {
            Write-Host $resp.Content.Substring(0, [Math]::Min(300, $resp.Content.Length))
        }
    } catch {
        Write-Host "$path ERROR: $($_.Exception.Message)"
        if ($_.Exception.Response) {
            try { $_.Exception.Response.StatusCode.Value__ | Out-String } catch {}
            try { $_.Exception.Response.GetResponseStream().ReadToEnd() | Out-String } catch {}
        }
    }
}
