$procs = Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'python.exe' -and $_.CommandLine -like '*uvicorn main:app*' }
if ($procs) {
    $procs | Select-Object ProcessId, CommandLine | Format-List
    $procs | ForEach-Object { Stop-Process -Id $_.ProcessId -Force }
}
Start-Process -FilePath 'python' -ArgumentList '-m', 'uvicorn', 'main:app', '--reload', '--port', '8000' -WorkingDirectory 'C:\Users\dante\Desktop\Ragnostic-AI\agents-service'
Start-Sleep -Seconds 3
Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | Select-Object LocalPort, State, OwningProcess | Format-Table -AutoSize
