#!/bin/bash
# 一键初始化GitHub仓库并部署到Pages - 意义智能×AI开机程序论
set -e
REPO_NAME="agent-bootloader"
GITHUB_USER="your-org"
PAGES_URL="https://your-org.github.io/agent-bootloader/"

echo "=== Agent Bootloader - 一键部署 ==="
echo "USDT地址: 0x05761494aff51283651a470c53dd4954b5"
echo "定价: 月度9U / 年度99U / 终身199U"

git init
git add .
git commit -m "release: v1.0 语音电子读物 + 真实USDT支付 9/99/199"

echo "请创建GitHub仓库并执行:"
echo "git remote add origin https://github.com/$GITHUB_USER/$REPO_NAME.git"
echo "git branch -M main"
echo "git push -u origin main"
echo ""
echo "然后在GitHub Settings -> Pages -> Source: main /docs -> Save"
echo "访问: $PAGES_URL"
echo ""
echo "支付验证:"
echo "扫码 qrcode_usdt_real.png 支付后，请在GitHub Issue提交TxHash开通会员"
ls -lh qrcode_*.png pricing.json
