$VenvPath = "C:\Users\ibrahim\Desktop\ibrahim\2026\portal\portal_backend\work_core_venv"
# $VenvPath = "D:\UEP Systems Production Version\backends full securty all\work_core_venv"
$ProjectPath = Get-Location
Set-Location -Path "$VenvPath\Scripts"
& .\Activate.ps1
Set-Location -Path $ProjectPath


