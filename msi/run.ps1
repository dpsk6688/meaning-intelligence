# run.ps1 —— 一键渲染 + 构建（Windows / PowerShell）
#
# 注意：本文件必须以 **UTF-8 with BOM** 保存。
# Windows PowerShell 5.1 在没有 BOM 时会按系统 ANSI 代码页（简体中文为 GBK）解析 .ps1，
# 中文注释会被解码成乱码并导致 "The string is missing the terminator" 之类的解析错误。
# 仓库的 .gitattributes 已把 *.ps1 标记为 text eol=crlf。
$ErrorActionPreference = 'Stop'

$here = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $here
Write-Host "工作目录 / working dir: $here" -ForegroundColor Cyan

# --- 1. 定位 manim ---
$manim = (Get-Command manim -ErrorAction SilentlyContinue).Source
if (-not $manim) {
    $candidates = @(
        "$env:USERPROFILE\miniconda3\Scripts\manim.exe",
        "$env:LOCALAPPDATA\miniconda3\Scripts\manim.exe",
        "$env:USERPROFILE\anaconda3\Scripts\manim.exe"
    )
    $manim = $candidates | Where-Object { Test-Path $_ } | Select-Object -First 1
}
if (-not $manim) { throw "未找到 manim，请先 pip install manim" }
Write-Host "manim: $manim" -ForegroundColor Cyan
& $manim --version 2>&1 | Select-Object -First 1

# --- 2. 渲染六幕场景（-ql = 480p15 快速预览；正式出片用 -qh）---
& $manim -ql scenes/meaning_intelligence.py MeaningIntelligenceScene
if ($LASTEXITCODE -ne 0) { throw "Manim 渲染失败，退出码 $LASTEXITCODE" }

# --- 3. 把 mp4 复制到 HTML 同级目录 ---
# Manim 的产物在 media\videos\<module>\480p15\ 下，而 HTML 引用的是同级目录的文件名。
# 少了这一步，<video> 永远黑屏 —— 这是原版脚本最常见的坑。
$mp4 = Get-ChildItem -Path (Join-Path $here 'media') -Recurse -Filter 'MeaningIntelligenceScene.mp4' `
       -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if ($mp4) {
    Copy-Item $mp4.FullName -Destination (Join-Path $here 'MeaningIntelligenceScene.mp4') -Force
    Write-Host "已复制视频 -> MeaningIntelligenceScene.mp4" -ForegroundColor Green
} else {
    Write-Warning "未找到渲染出的 MP4，HTML 中的动画区将为空。"
}

# --- 4. 构建 HTML（此时会读到刚生成的实测 timeline.json）---
$py = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $py) { $py = 'python' }
& $py build.py
if ($LASTEXITCODE -ne 0) { throw "构建失败，退出码 $LASTEXITCODE" }

Write-Host "`n完成。用浏览器打开 / open in browser:" -ForegroundColor Green
Write-Host "  $here\meaning_intelligence.html"
