param(
    [Parameter(Mandatory = $true)]
    [ValidateSet("local", "remote")]
    [string]$Environment
)

# Copia environments/<env>.json -> project-config.json y sobrepone DB_ORA_DW_*
# desde docs/credenciales/<env>.txt. No copia SysPassword. No escribe secretos en stdout.
# Uso: .\switch-env.ps1 local   |   .\switch-env.ps1 remote

$ErrorActionPreference = "Stop"

$envFile  = Join-Path $PSScriptRoot "environments\$Environment.json"
$projFile = Join-Path $PSScriptRoot "project-config.json"
$credFile = Join-Path $PSScriptRoot "docs\credenciales\$Environment.txt"

if (-not (Test-Path -LiteralPath $envFile)) {
    throw "No existe la plantilla: $envFile"
}

function New-HopProject([object[]]$Variables) {
    return [pscustomobject]@{
        metadataBaseFolder          = '${PROJECT_HOME}/metadata'
        unitTestsBasePath           = '${PROJECT_HOME}'
        dataSetsCsvFolder           = '${PROJECT_HOME}/datasets'
        enforcingExecutionInHome    = $true
        parentProjectName           = "default"
        config                      = [pscustomobject]@{ variables = $Variables }
    }
}

function Read-Cred([string]$Path) {
    $allowed = @{
        host = "DB_ORA_DW_HOST"
        port = "DB_ORA_DW_PORT"
        service = "DB_ORA_DW_DATABASE"
        user = "DB_ORA_DW_USERNAME"
        password = "DB_ORA_DW_PASSWORD"
        schema = "DB_ORA_DW_SCHEMA"
    }
    $found = @{}
    foreach ($raw in Get-Content -LiteralPath $Path) {
        $line = $raw.Trim()
        if (-not $line -or $line.StartsWith("#") -or -not $line.Contains(":")) { continue }
        $idx = $line.IndexOf(":")
        $key = $line.Substring(0, $idx).Trim().ToLower()
        $value = $line.Substring($idx + 1).Trim()
        if ($key -eq "syspassword" -or -not $allowed.ContainsKey($key) -or -not $value) { continue }
        $found[$key] = $value
    }
    return $found
}

function Set-Var([System.Collections.Generic.List[object]]$Vars, [string]$Name, [string]$Value, [string]$Description) {
    foreach ($item in $Vars) {
        if ($item.name -eq $Name) {
            $item.value = $Value
            return
        }
    }
    $Vars.Add([pscustomobject]@{
        name = $Name
        value = $Value
        description = $Description
    }) | Out-Null
}

$envCfg = Get-Content -LiteralPath $envFile -Raw | ConvertFrom-Json
$vars = New-Object 'System.Collections.Generic.List[object]'
foreach ($item in @($envCfg.variables)) { $vars.Add($item) | Out-Null }

if (-not (Test-Path -LiteralPath $credFile)) {
    Write-Host "AVISO: no existe $credFile; DB_ORA_DW_* quedan como en $envFile"
} else {
    $cred = Read-Cred $credFile
    if (-not $cred.ContainsKey("schema") -and $cred.ContainsKey("user") -and $cred["user"]) {
        $cred["schema"] = $cred["user"].ToUpper()
    }
    $map = @{
        host = "DB_ORA_DW_HOST"
        port = "DB_ORA_DW_PORT"
        service = "DB_ORA_DW_DATABASE"
        user = "DB_ORA_DW_USERNAME"
        password = "DB_ORA_DW_PASSWORD"
        schema = "DB_ORA_DW_SCHEMA"
    }
    $desc = "Oracle DW desde docs/credenciales/$Environment.txt"
    foreach ($key in $map.Keys) {
        if ($cred.ContainsKey($key) -and $cred[$key]) {
            Set-Var $vars $map[$key] $cred[$key] $desc
        }
    }
    if ($cred.ContainsKey("host") -and $cred.ContainsKey("port") -and $cred.ContainsKey("service")) {
        $url = "jdbc:oracle:thin:@//$($cred.host):$($cred.port)/$($cred.service)"
        Set-Var $vars "DB_ORA_DW_URL" $url $desc
    }
    $schema = ""
    if ($cred.ContainsKey("schema")) { $schema = $cred["schema"] }
    Write-Host "OK: overlay DB_ORA_DW_* desde $credFile (schema=$schema)"
}

$proj = New-HopProject @($vars.ToArray())
$json = $proj | ConvertTo-Json -Depth 10
[System.IO.File]::WriteAllText($projFile, $json, (New-Object System.Text.UTF8Encoding($false)))
Write-Host "OK: $envFile -> $projFile"
