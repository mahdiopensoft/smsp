$VenvPath = "C:\Users\ebrahim\Desktop\MyWork\sharing\work_core_venv"
# $VenvPath = "D:\UEP Systems Production Version\backends full securty all\work_core_venv"
$ProjectPath = Get-Location
Set-Location -Path "$VenvPath\Scripts"
& .\Activate.ps1
$env:PYTHONPATH = "C:\Users\ebrahim\Desktop\MyWork\smsp-main\backend"
Set-Location -Path $ProjectPath


