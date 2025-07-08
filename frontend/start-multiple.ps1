# 启动多个前端实例的PowerShell脚本
# 用于测试多人聊天功能

Write-Host "🚀 启动多个前端实例用于测试多人聊天功能" -ForegroundColor Green

# 启动第一个实例 (端口 3001)
Write-Host "启动实例 1 - 端口 3001" -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-Command", "cd '$PWD'; npm run dev -- --port 3001 --host 0.0.0.0"

# 等待2秒
Start-Sleep -Seconds 2

# 启动第二个实例 (端口 3002)
Write-Host "启动实例 2 - 端口 3002" -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-Command", "cd '$PWD'; npm run dev -- --port 3002 --host 0.0.0.0"

# 等待2秒
Start-Sleep -Seconds 2

# 启动第三个实例 (端口 3003)
Write-Host "启动实例 3 - 端口 3003" -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-Command", "cd '$PWD'; npm run dev -- --port 3003 --host 0.0.0.0"

Write-Host ""
Write-Host "✅ 所有实例启动完成！" -ForegroundColor Green
Write-Host "📱 实例 1: http://localhost:3001" -ForegroundColor Cyan
Write-Host "📱 实例 2: http://localhost:3002" -ForegroundColor Cyan
Write-Host "📱 实例 3: http://localhost:3003" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 提示：" -ForegroundColor Magenta
Write-Host "- 在每个实例中创建不同的玩家角色" -ForegroundColor White
Write-Host "- 测试实时聊天功能" -ForegroundColor White
Write-Host "- 观察消息在不同窗口间的同步" -ForegroundColor White
Write-Host ""
Write-Host "按任意键退出..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
