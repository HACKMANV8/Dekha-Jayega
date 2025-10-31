# RenderPrepAgent Setup and Test Script
# Run this to verify the integration is working

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "RenderPrepAgent Integration Setup" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installations
Write-Host "1. Checking Python environments..." -ForegroundColor Yellow

$hackmanPython = "D:\Dekha-Jayega\Hackman_agent-main\.venv\Scripts\python.exe"
$nanoPython = "D:\Dekha-Jayega\Nano banana\nano-banana-python\.venv\Scripts\python.exe"

if (Test-Path $hackmanPython) {
    Write-Host "✓ RenderPrepAgent Python found" -ForegroundColor Green
    & $hackmanPython --version
} else {
    Write-Host "✗ RenderPrepAgent Python NOT found at: $hackmanPython" -ForegroundColor Red
    Write-Host "  Please create virtual environment and install dependencies" -ForegroundColor Yellow
}

if (Test-Path $nanoPython) {
    Write-Host "✓ Nano Banana Python found" -ForegroundColor Green
    & $nanoPython --version
} else {
    Write-Host "✗ Nano Banana Python NOT found at: $nanoPython" -ForegroundColor Red
    Write-Host "  Please create virtual environment and install dependencies" -ForegroundColor Yellow
}

Write-Host ""

# Check run_render_prep.py exists
Write-Host "2. Checking Python wrapper script..." -ForegroundColor Yellow
$wrapperScript = "D:\Dekha-Jayega\Hackman_agent-main\run_render_prep.py"

if (Test-Path $wrapperScript) {
    Write-Host "✓ run_render_prep.py exists" -ForegroundColor Green
} else {
    Write-Host "✗ run_render_prep.py NOT found" -ForegroundColor Red
}

Write-Host ""

# Check backend files
Write-Host "3. Checking backend files..." -ForegroundColor Yellow

$controllerFile = "D:\Dekha-Jayega\Backend\src\controller\renderPrepAgentController.js"
$routeFile = "D:\Dekha-Jayega\Backend\src\routes\renderPrepAgent.js"

if (Test-Path $controllerFile) {
    Write-Host "✓ renderPrepAgentController.js exists" -ForegroundColor Green
} else {
    Write-Host "✗ renderPrepAgentController.js NOT found" -ForegroundColor Red
}

if (Test-Path $routeFile) {
    Write-Host "✓ renderPrepAgent.js routes exist" -ForegroundColor Green
} else {
    Write-Host "✗ renderPrepAgent.js routes NOT found" -ForegroundColor Red
}

Write-Host ""

# Check frontend file
Write-Host "4. Checking frontend files..." -ForegroundColor Yellow

$frontendFile = "D:\Dekha-Jayega\Frontend\src\pages\RenderPrepAgent.jsx"

if (Test-Path $frontendFile) {
    Write-Host "✓ RenderPrepAgent.jsx exists" -ForegroundColor Green
    $lineCount = (Get-Content $frontendFile).Count
    Write-Host "  File has $lineCount lines" -ForegroundColor Cyan
} else {
    Write-Host "✗ RenderPrepAgent.jsx NOT found" -ForegroundColor Red
}

Write-Host ""

# Check export directory
Write-Host "5. Checking export directories..." -ForegroundColor Yellow

$exportDir = "D:\Dekha-Jayega\Hackman_agent-main\exports\render_prep"

if (-not (Test-Path $exportDir)) {
    Write-Host "Creating export directory..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $exportDir -Force | Out-Null
    Write-Host "✓ Export directory created" -ForegroundColor Green
} else {
    Write-Host "✓ Export directory exists" -ForegroundColor Green
}

Write-Host ""
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Setup Check Complete!" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Start Backend: cd Backend; npm run dev" -ForegroundColor White
Write-Host "2. Start Frontend: cd Frontend; npm run dev" -ForegroundColor White
Write-Host "3. Navigate to: http://localhost:5173/render-prep-agent" -ForegroundColor White
Write-Host "4. Select a completed saga and generate prompts!" -ForegroundColor White
Write-Host ""
Write-Host "API Endpoints Available:" -ForegroundColor Yellow
Write-Host "  POST /api/render-prep/generate-prompts" -ForegroundColor Cyan
Write-Host "  POST /api/render-prep/generate-image/:assetId" -ForegroundColor Cyan
Write-Host "  POST /api/render-prep/batch-generate-images" -ForegroundColor Cyan
Write-Host "  GET  /api/render-prep/assets/:projectId" -ForegroundColor Cyan
Write-Host ""
