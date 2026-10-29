$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
& 'C:/Users/mason/.cache/codex-tools/blender/blender-4.5.9-windows-x64/blender.exe' --background metallic.blend --python render.py *> render.log
if ($LASTEXITCODE -ne 0) { throw 'Blender render failed; inspect render.log' }
& 'C:/Users/mason/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' encode.py *> encode.log
if ($LASTEXITCODE -ne 0) { throw 'Encoding or validation failed; inspect encode.log' }
