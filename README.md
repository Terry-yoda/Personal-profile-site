# 使用我的小米手機架設 自我介紹網站

## 目錄結構

```
profile-site/
├── app.py                  ← Flask 主程式
├── requirements.txt        ← 套件清單
├── profile_data.json       ← 自動產生，存放你的資料
└── templates/
    └── index.html          ← 前端頁面
```

---

## 第一步：安裝 Termux（安卓）

1. 從 **F-Droid** 下載安裝 Termux（不要用 Google Play 版，太舊）
   - 網址：https://f-droid.org/packages/com.termux/

2. 開啟 Termux，更新套件：
```bash
pkg update && pkg upgrade
```

3. 安裝 Python：
```bash
pkg install python
```

---

## 第二步：安裝專案

1. 把這個資料夾傳到手機（可用 USB、Google Drive、或直接在 Termux 建立）

2. 進入資料夾：
```bash
cd profile-site
```

3. 安裝 Flask：
```bash
pip install flask
```

---

## 第三步：啟動伺服器

```bash
python app.py
```

看到以下訊息表示成功：
```
 * Running on http://0.0.0.0:5000
```

用手機瀏覽器打開 **http://localhost:5000** 即可看到頁面！

---

## 第四步：讓外部可以連到你的網站（Cloudflare Tunnel）

### 方法 A：Cloudflare Tunnel（推薦，免費！）

不需要固定 IP，直接穿透防火牆。

1. 在 Termux 安裝 cloudflared：
```bash
pkg install wget
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64
chmod +x cloudflared-linux-arm64
mv cloudflared-linux-arm64 /data/data/com.termux/files/usr/bin/cloudflared
```

2. 登入 Cloudflare（會跳出瀏覽器授權）：
```bash
cloudflared tunnel login
```

3. 建立 Tunnel：
```bash
cloudflared tunnel create my-profile
```

4. 把 Flask 綁定到你的網域：
```bash
cloudflared tunnel route dns my-profile 你的子網域.你的網域.com
```

5. 啟動 Tunnel：
```bash
cloudflared tunnel run --url http://localhost:5000 my-profile
```

### 方法 B：快速測試（臨時網址）

不需要帳號，直接執行：
```bash
cloudflared tunnel --url http://localhost:5000
```
會產生一個 `https://xxxxx.trycloudflare.com` 臨時網址，重啟會變。

---

## 第五步：保持背景運行

Termux 關掉視窗後伺服器會停止，用以下方式保持運行：

```bash
# 安裝 tmux
pkg install tmux

# 建立新 session
tmux new -s server

# 啟動 Flask
python app.py

# 按 Ctrl+B 然後按 D 來分離（不會關掉）
# 之後要回來用：
tmux attach -t server
```

---

## 使用說明：前端編輯

1. 打開網頁後，點右上角 **「編輯模式」** 按鈕
2. 直接點擊名字、職稱、介紹等文字即可修改
3. 點擊頭像可輸入圖片網址更換
4. 點「**+ 新增社群連結**」新增平台
5. 每個連結右側有 ✏️ 編輯和 ✕ 刪除按鈕
6. 改完後按右下角 **「💾 儲存」**，資料會存到 `profile_data.json`

---

## 常見問題

**Q: 手機重開後要怎麼重新啟動？**
```bash
tmux attach -t server
# 如果 session 不見了：
cd profile-site && python app.py
```

**Q: 可以用 Wi-Fi 讓同網段其他人連嗎？**
查你手機的 Wi-Fi IP：
```bash
ifconfig | grep 192
```
然後用 `http://192.168.x.x:5000` 連線。

**Q: profile_data.json 在哪？**
在 `profile-site/` 資料夾下，可以直接備份這個檔案。
