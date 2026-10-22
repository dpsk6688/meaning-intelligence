# 推送指南

## Windows
cd Desktop
unzip meaning-intelligence-push-ready.zip
cd meaning-intelligence-push-ready
git init
git add .
git commit -m "release: v1.0 docs/index.html + USDT 9/99/199"
git branch -M main
git remote add origin https://github.com/sara-protocol/meaning-intelligence.git
git push -u origin main --force

## Mac/Linux
cd ~/Desktop
unzip meaning-intelligence-push-ready.zip
cd meaning-intelligence-push-ready
git init
git add .
git commit -m "release: v1.0"
git branch -M main
git remote add origin https://github.com/sara-protocol/meaning-intelligence.git
git push -u origin main --force

## 已克隆的情况
git clone https://github.com/sara-protocol/meaning-intelligence.git
cd meaning-intelligence
cp -r ../meaning-intelligence-push-ready/docs ./
cp -r ../meaning-intelligence-push-ready/.github ./
git add .
git commit -m "release: v1.0"
git push
