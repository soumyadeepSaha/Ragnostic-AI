$procs = Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'node.exe' -and $_.CommandLine -like '*server.js*' }
if ($procs) {
    $procs | Select-Object ProcessId, CommandLine | Format-List
    $procs | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
}
Start-Process -FilePath 'node' -ArgumentList 'server.js' -WorkingDirectory 'C:\Users\dante\Desktop\Ragnostic-AI\gateway'
Start-Sleep -Seconds 2
Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue | Select-Object LocalPort, State, OwningProcess | Format-Table -AutoSize
