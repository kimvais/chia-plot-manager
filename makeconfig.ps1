Import-Module powershell-yaml
$YAML=Get-Content .\config.yaml.default -Raw
$DAEMONDIR=(Get-ChildItem -Path $HOME/AppData/Local/chia-blockchain -Recurse -Name daemon -Directory)
$chia_location="$HOME\AppData\Local\chia-blockchain"+$DAEMONDIR
$config=ConvertFrom-YAML $YAML
$config.chia_location=$chia_location
Set-content config.yaml $(ConvertTo-YAML $config)
