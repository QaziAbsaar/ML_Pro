Param(
    [string]$HFUsername = $env:HF_USERNAME,
    [string]$HFSpace = $env:HF_SPACE,
    [string]$HFToken = $env:HF_TOKEN
)

$ErrorActionPreference = 'Stop'

if (-not $HFUsername -or -not $HFSpace -or -not $HFToken) {
    Write-Error 'Missing environment variables. Set HF_USERNAME, HF_SPACE, and HF_TOKEN before running this script.'
    exit 1
}

 $env:HF_USERNAME = $HFUsername
 $env:HF_SPACE = $HFSpace
 $env:HF_TOKEN = $HFToken

Write-Host 'Uploading the Space through the Hugging Face Hub API...'
python .\deploy_to_hf.py

if ($LASTEXITCODE -ne 0) {
    throw 'Deployment failed. Check the error above and verify the token, Space name, and required files.'
}
