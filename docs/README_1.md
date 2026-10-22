# Meaning Intelligence × AI Bootloader

> 意义智能理论 + 刘慈欣AI开机程序论 - 图文并茂语音电子读物

**仓库:** https://github.com/sara-protocol/meaning-intelligence  
**在线阅读:** https://sara-protocol.github.io/meaning-intelligence/  
**海报 + 落地页 + 三合一下载包 + USDT支付**

## 真实USDT支付地址 (ERC20)
```
0x05761494aff51283651a470c53dd4954b5
```

## 定价 (最新)
- 月度会员: 9 USDT/月 - 全文阅读 + 三合一下载(PPTX+Word+PDF) + 语音
- 年度会员: 99 USDT/年 - 含L1-L6代码库 + 私有MCP Server + A2A配置
- 一次性订阅: 199 USDT - 终身三合一下载包 + 永久更新

## 一键部署
```bash
git clone https://github.com/sara-protocol/meaning-intelligence.git
cd meaning-intelligence
bash deploy.sh
# 或手动:
git remote add origin https://github.com/sara-protocol/meaning-intelligence.git
git branch -M main
git push -u origin main
# 然后 Settings -> Pages -> Source: GitHub Actions
```

## GitHub Actions 自动部署
已配置 `.github/workflows/deploy-pages.yml`，推送到 main 自动发布到 Pages

## 文件结构
```
docs/
  index.html - 落地页 (语音电子读物 + 会员制 + 二维码)
  *.png - 海报 + USDT二维码
  *.html - 20页双语讲座PPT
final_release/
  qrcode_usdt_real.png - 真实可扫支付
  qrcode_monthly_9_address.png
  qrcode_yearly_99_address.png
  qrcode_lifetime_199_address.png
  AGENT_Bootloader_最终发布包.zip
```

## 支付验证
扫码支付后，提交 TxHash 到 GitHub Issue，自动开通会员

## 技术
- L1-L6 Agent框架 v0.3.0 (PR-2)
- MCP/A2A架构
- web-MCP集成
- 中英繁三语切换 + 语音+字幕

MIT License
