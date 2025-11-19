<div dir="rtl">

# 🧙‍♂️ راهنمای کامل Multi Wizard

**طراحی شده توسط: 👽 Anonymous**

---

## 📋 فهرست مطالب

1. [معرفی](#-معرفی)
2. [پیش‌نیازها](#-پیشنیازها)
3. [نصب](#-نصب)
   - [Linux](#-نصب-در-linux)
   - [macOS](#-نصب-در-macos)
   - [Termux (Android)](#-نصب-در-termux-android)
   - [Windows](#-نصب-در-windows)
4. [اجرای دستی](#-اجرای-دستی)
5. [مدیریت سیستم](#-مدیریت-سیستم)
6. [استفاده از کانفیگ‌ها](#-استفاده-از-کانفیگها)
7. [به‌روزرسانی](#-بهروزرسانی)
8. [عیب‌یابی](#-عیبیابی)
9. [حذف کامل](#-حذف-کامل)

---

## 🎯 معرفی

**Multi Wizard** یک نصب‌کننده خودکار و کامل برای سیستم مدیریت پروکسی است که:

✅ تمام ابزارهای مورد نیاز را نصب می‌کند  
✅ محیط کار را به طور کامل راه‌اندازی می‌کند  
✅ اجرای خودکار هر 12 ساعت را تنظیم می‌کند  
✅ ابزارهای مدیریتی ساده ارائه می‌دهد  

### چه چیزهایی نصب می‌شود؟
- **Git** - برای دریافت کدها
- **Python 3.7+** - زبان برنامه‌نویسی
- **Xray-core** - موتور تست پروکسی (مرحله اول)
- **Sing-box** - موتور تست پروکسی (مرحله دوم)
- **وابستگی‌های Python** - کتابخانه‌های مورد نیاز
- **Cron/LaunchAgent** - برای اجرای خودکار

---

## 📦 پیش‌نیازها

### برای همه پلتفرم‌ها:
- ✅ اتصال به اینترنت (پایدار)
- ✅ حداقل 500MB فضای خالی
- ✅ دسترسی به ترمینال/Terminal

### Termux (Android):
- ✅ نصب [Termux از F-Droid](https://f-droid.org/packages/com.termux/)
- ⚠️ نسخه Google Play پشتیبانی نمی‌شود!
- ✅ توصیه می‌شود: نصب [Termux:Boot](https://f-droid.org/packages/com.termux.boot/)

### Linux:
- ✅ توزیع‌های پشتیبانی شده: Ubuntu, Debian, Arch, Fedora, CentOS
- ✅ دسترسی sudo (برای نصب پکیج‌ها)

### macOS:
- ✅ macOS 10.15+ (Catalina یا جدیدتر)
- ✅ Homebrew (نصب خودکار انجام می‌شود)

### Windows:
- ✅ WSL2 (Windows Subsystem for Linux)
- یا Git Bash

---

## 🚀 نصب

### 🐧 نصب در Linux

#### روش 1: نصب با یک دستور (توصیه می‌شود)
```bash
curl -fsSL https://raw.githubusercontent.com/4n0nymou3/multi-proxy-config-fetcher/main/install.sh | bash
```

یا:
```bash
wget -qO- https://raw.githubusercontent.com/4n0nymou3/multi-proxy-config-fetcher/main/install.sh | bash
```

#### روش 2: نصب دستی
```bash
# نصب Git (در صورت نیاز)
sudo apt install git -y          # Ubuntu/Debian
sudo pacman -S git               # Arch
sudo yum install git -y          # CentOS/RHEL

# دانلود و نصب
git clone https://github.com/4n0nymou3/multi-proxy-config-fetcher.git
cd multi-proxy-config-fetcher
bash install.sh
```

#### زمان تقریبی نصب:
⏱️ **5-10 دقیقه** (بسته به سرعت اینترنت)

---

### 🍎 نصب در macOS

#### روش 1: نصب با یک دستور
```bash
curl -fsSL https://raw.githubusercontent.com/4n0nymou3/multi-proxy-config-fetcher/main/install.sh | bash
```

#### روش 2: نصب دستی
```bash
# نصب Homebrew (در صورت نیاز)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# نصب Git
brew install git

# دانلود و نصب
git clone https://github.com/4n0nymou3/multi-proxy-config-fetcher.git
cd multi-proxy-config-fetcher
bash install.sh
```

#### زمان تقریبی نصب:
⏱️ **8-15 دقیقه**

---

### 📱 نصب در Termux (Android)

#### مرحله 1: نصب Termux از F-Droid
1. دانلود [F-Droid](https://f-droid.org/)
2. نصب **Termux** از F-Droid
3. باز کردن Termux

⚠️ **هشدار**: نسخه Google Play کار نمی‌کند!

#### مرحله 2: به‌روزرسانی پکیج‌ها
```bash
pkg update
pkg upgrade -y
```

#### مرحله 3: نصب Multi Wizard
```bash
pkg install curl git -y
curl -fsSL https://raw.githubusercontent.com/4n0nymou3/multi-proxy-config-fetcher/main/install.sh | bash
```

یا نصب دستی:
```bash
pkg install curl git -y
git clone https://github.com/4n0nymou3/multi-proxy-config-fetcher.git
cd multi-proxy-config-fetcher
bash install.sh
```

#### زمان تقریبی نصب:
⏱️ **10-20 دقیقه** (بسته به گوشی و اینترنت)

#### نکات مهم برای Termux:
1. **Termux را باز نگه دارید** - در حین نصب Termux را نبندید
2. **Wake Lock فعال کنید**:
   ```bash
   termux-wake-lock
   ```
3. **Battery Optimization را غیرفعال کنید**:
   - Settings → Apps → Termux → Battery → Unrestricted

---

### 🪟 نصب در Windows

Windows به صورت مستقیم پشتیبانی نمی‌شود. از یکی از روش‌های زیر استفاده کنید:

#### روش 1: WSL2 (توصیه می‌شود)

##### مرحله 1: نصب WSL2
```powershell
# در PowerShell به عنوان Administrator اجرا کنید
wsl --install
```

##### مرحله 2: راه‌اندازی مجدد
کامپیوتر را Restart کنید

##### مرحله 3: نصب Ubuntu
1. باز کردن Microsoft Store
2. جستجوی "Ubuntu"
3. نصب Ubuntu
4. باز کردن Ubuntu از Start Menu

##### مرحله 4: نصب Multi Wizard
```bash
# در Ubuntu Terminal
curl -fsSL https://raw.githubusercontent.com/4n0nymou3/multi-proxy-config-fetcher/main/install.sh | bash
```

#### روش 2: Git Bash
1. دانلود و نصب [Git for Windows](https://git-scm.com/download/win)
2. باز کردن Git Bash
3. اجرای دستور نصب:
```bash
bash <(curl -fsSL https://raw.githubusercontent.com/4n0nymou3/multi-proxy-config-fetcher/main/install.sh)
```

---

## ▶️ اجرای دستی

بعد از نصب، Multi Wizard به صورت خودکار اجرا نمی‌شود. برای اجرای دستی:

### روش 1: استفاده از اسکریپت اجرا
```bash
cd ~/multi-proxy-config-fetcher
bash run.sh
```

### روش 2: استفاده از Management Script
```bash
cd ~/multi-proxy-config-fetcher
bash manage.sh start
```

### زمان تقریبی اجرا:
⏱️ **5-15 دقیقه** (بسته به تعداد کانفیگ‌ها)

### مراحل اجرا:
```
➤ Fetch Configs         ✓ دریافت از منابع
➤ Enrich Configs        ✓ شناسایی موقعیت جغرافیایی
➤ Rename Configs        ✓ تغییر نام با جزئیات
➤ Test with Xray        ✓ تست سلامت مرحله 1
➤ Convert to Sing-box   ✓ تبدیل فرمت
➤ Test with Sing-box    ✓ تست سلامت مرحله 2
➤ Security Filter       ✓ فیلتر امنیتی
➤ Generate Balanced     ✓ ساخت لودبالانس
➤ Generate Charts       ✓ ساخت نمودارها
```

---

## 🔧 مدیریت سیستم

بعد از نصب، یک اسکریپت مدیریتی به نام `manage.sh` ایجاد می‌شود.

### دستورات موجود:

#### 1️⃣ اجرای Pipeline
```bash
bash manage.sh start
```
**کاربرد**: اجرای کامل دریافت و پردازش کانفیگ‌ها

---

#### 2️⃣ بررسی وضعیت
```bash
bash manage.sh status
```

**خروجی نمونه**:
```
📊 System Status:

✓ Xray: Xray 1.8.9 (Xray, Penetrates Everything.)
✓ Sing-box: sing-box version 1.8.0

📁 Output files:
   configs/proxy_configs.txt - 45K
   configs/proxy_configs_tested.txt - 38K
   configs/singbox_configs_tested.json - 156K

📝 Recent logs:
   logs/run_2024-11-19_07-14-01.log
```

---

#### 3️⃣ مشاهده لاگ‌ها
```bash
bash manage.sh logs
```

**کاربرد**: نمایش 50 خط آخر لاگ اجرای خودکار

---

#### 4️⃣ پاکسازی لاگ‌های قدیمی
```bash
bash manage.sh clean
```

**کاربرد**: حذف لاگ‌های قدیمی‌تر از 7 روز

---

#### 5️⃣ به‌روزرسانی از GitHub
```bash
bash manage.sh update
```

**کاربرد**: دریافت آخرین نسخه کدها از GitHub

---

#### 6️⃣ راهنما
```bash
bash manage.sh help
```

---

## 📁 استفاده از کانفیگ‌ها

بعد از اجرای موفق Pipeline، فایل‌های زیر ایجاد می‌شوند:

### انواع فایل‌های خروجی:

| فایل | توضیحات | کاربرد |
|------|---------|--------|
| `proxy_configs.txt` | کانفیگ‌های خام دریافت شده | v2rayNG, v2rayN |
| `proxy_configs_tested.txt` | کانفیگ‌های تست شده با Xray | v2rayNG, v2rayN ⭐ |
| `singbox_configs_all.json` | همه کانفیگ‌ها در فرمت Sing-box | SFA, Hiddify, NekoBox |
| `singbox_configs_tested.json` | کانفیگ‌های تست شده با Sing-box | SFA, Hiddify, NekoBox ⭐ |
| `singbox_configs_secure.json` | کانفیگ‌های تست شده و امن Sing-box | SFA, Hiddify, NekoBox 🛡️⭐ |
| `xray_loadbalanced_config.json` | لودبالانس Xray (تست شده) | v2rayNG, v2rayN ⭐ |
| `xray_secure_loadbalanced_config.json` | لودبالانس Xray (تست شده و امن) | v2rayNG, v2rayN 🛡️⭐ |

⭐ = توصیه می‌شود  
🛡️ = امنیت بالا

---

### 📱 استفاده در v2rayNG (Android)

#### روش 1: Import از فایل محلی (ساده‌ترین)

##### مرحله 1: کپی فایل به حافظه گوشی
```bash
# در Termux
termux-setup-storage

# کپی فایل به Downloads
cp ~/multi-proxy-config-fetcher/configs/xray_secure_loadbalanced_config.json ~/storage/downloads/
```

##### مرحله 2: Import در v2rayNG
1. باز کردن **v2rayNG**
2. کلیک روی **منوی ☰** (بالا سمت راست)
3. انتخاب **Import config from file**
4. رفتن به پوشه **Downloads**
5. انتخاب فایل `xray_secure_loadbalanced_config.json`
6. کلیک روی **Import**

✅ تمام! حالا تمام کانفیگ‌های امن در v2rayNG شماست.

---

#### روش 2: استفاده از Share (سریع‌تر)

##### مرحله 1: نصب Termux API
```bash
pkg install termux-api
```

##### مرحله 2: اشتراک‌گذاری فایل
```bash
termux-share ~/multi-proxy-config-fetcher/configs/xray_secure_loadbalanced_config.json
```

##### مرحله 3: انتخاب v2rayNG
از لیست برنامه‌ها، **v2rayNG** را انتخاب کنید.

---

#### روش 3: HTTP Server (پیشرفته)

این روش برای دسترسی از چند دستگاه یا به‌روزرسانی خودکار مناسب است.

##### مرحله 1: راه‌اندازی HTTP Server
```bash
cd ~/multi-proxy-config-fetcher/configs
python -m http.server 8080
```

⚠️ **مهم**: این Terminal را باز نگه دارید!

##### مرحله 2: پیدا کردن IP محلی

###### در Termux:
```bash
# در یک Terminal جدید (New Session)
ifconfig | grep "inet "
```

مثال خروجی:
```
inet 192.168.1.105 netmask 0xffffff00 broadcast 192.168.1.255
```

IP شما: `192.168.1.105`

##### مرحله 3: Import در v2rayNG

**گزینه A: Import یکباره**
1. باز کردن **v2rayNG**
2. منو ☰ → **Import config from URL**
3. وارد کردن:
   ```
   http://192.168.1.105:8080/xray_secure_loadbalanced_config.json
   ```
4. کلیک **OK**

**گزینه B: Subscription (به‌روزرسانی خودکار)**
1. باز کردن **v2rayNG**
2. منو ☰ → **Subscription setting**
3. کلیک روی **+** (پایین سمت راست)
4. وارد کردن:
   - **Remarks**: `کانفیگ‌های محلی من`
   - **URL**: `http://192.168.1.105:8080/proxy_configs_tested.txt`
5. ذخیره
6. برگشت به صفحه اصلی
7. منو ☰ → **Update subscription**

✅ حالا هر وقت بخواهید به‌روزرسانی کنید:
- منو ☰ → **Update subscription**

---

### 💻 استفاده در v2rayN (Windows)

#### مرحله 1: کپی فایل
اگر از WSL2 استفاده می‌کنید:
```bash
# در WSL2
cp ~/multi-proxy-config-fetcher/configs/xray_secure_loadbalanced_config.json /mnt/c/Users/YOUR_USERNAME/Downloads/
```

#### مرحله 2: Import
1. باز کردن **v2rayN**
2. منو → **Import** → **Import from file**
3. انتخاب فایل از Downloads
4. کلیک **Import**

---

### 📦 استفاده در Sing-box Apps

برای استفاده در برنامه‌های مبتنی بر Sing-box مثل:
- **SFA** (Sing-box for Android)
- **Hiddify**
- **NekoBox**

#### استفاده از فایل‌های JSON:
```bash
# کپی به حافظه گوشی
cp ~/multi-proxy-config-fetcher/configs/singbox_configs_secure.json ~/storage/downloads/

# سپس در برنامه:
Import → Select file → singbox_configs_secure.json
```

---

### 🌐 استفاده از GitHub (دسترسی از همه جا)

اگر می‌خواهید از هر جا به کانفیگ‌هایتان دسترسی داشته باشید:

#### ⚠️ هشدار امنیتی:
این روش فقط برای **ریپازیتوری‌های Private** توصیه می‌شود!

#### مرحله 1: Fork کردن ریپازیتوری
1. رفتن به https://github.com/4n0nymou3/multi-proxy-config-fetcher
2. کلیک روی **Fork**
3. ایجاد Fork

#### مرحله 2: تبدیل به Private
1. رفتن به **Settings** ریپازیتوری فورک شده
2. پایین صفحه → **Danger Zone**
3. **Change visibility** → **Make private**

#### مرحله 3: فعال کردن GitHub Actions
1. **Actions** tab
2. **I understand my workflows, go ahead and enable them**

#### مرحله 4: دریافت Raw URL
بعد از اجرای Action و بروزرسانی فایل‌ها:
```
https://raw.githubusercontent.com/YOUR_USERNAME/multi-proxy-config-fetcher/main/configs/proxy_configs_tested.txt
```

#### مرحله 5: استفاده در v2rayNG
1. منو → **Subscription setting**
2. **+** (اضافه کردن)
3. وارد کردن Raw URL
4. ذخیره
5. **Update subscription**

---

## 🔄 به‌روزرسانی

### به‌روزرسانی خودکار
سیستم به صورت خودکار هر 12 ساعت یکبار اجرا می‌شود:
- **Linux/Termux**: از طریق Cron
- **macOS**: از طریق LaunchAgent

برای بررسی:

#### Linux/Termux:
```bash
crontab -l
```

#### macOS:
```bash
launchctl list | grep multiproxy
```

---

### به‌روزرسانی دستی

#### روش 1: استفاده از Management Script
```bash
cd ~/multi-proxy-config-fetcher
bash manage.sh update
```

#### روش 2: دستی
```bash
cd ~/multi-proxy-config-fetcher
git pull origin main
pip install -r requirements.txt
```

---

### تغییر زمان اجرای خودکار

#### Linux/Termux (Cron):
```bash
# ویرایش Crontab
crontab -e

# تغییر خط زیر:
0 */12 * * * cd ~/multi-proxy-config-fetcher && bash run.sh

# به (مثلاً هر 6 ساعت):
0 */6 * * * cd ~/multi-proxy-config-fetcher && bash run.sh
```

#### macOS (LaunchAgent):
```bash
# ویرایش فایل plist
nano ~/Library/LaunchAgents/com.anonymous.multiproxy.plist

# تغییر بخش StartCalendarInterval
# سپس:
launchctl unload ~/Library/LaunchAgents/com.anonymous.multiproxy.plist
launchctl load ~/Library/LaunchAgents/com.anonymous.multiproxy.plist
```

---

## 🐛 عیب‌یابی

### مشکل 1: Xray یا Sing-box نصب نشده

#### علائم:
```
✗ Xray: Not installed
✗ Sing-box: Not installed
```

#### راه حل:
```bash
cd ~/multi-proxy-config-fetcher

# نصب مجدد
bash install.sh

# یا نصب دستی Xray
bash -c "$(curl -L https://github.com/XTLS/Xray-install/raw/main/install-release.sh)" @ install

# نصب دستی Sing-box
# Termux:
pkg install sing-box

# Linux:
bash <(curl -fsSL https://sing-box.app/install.sh)

# macOS:
brew install sing-box
```

---

### مشکل 2: خطای Python Dependencies

#### علائم:
```
ModuleNotFoundError: No module named 'requests'
```

#### راه حل:
```bash
cd ~/multi-proxy-config-fetcher

# فعال کردن virtual environment
source venv/bin/activate

# نصب مجدد
pip install --upgrade pip
pip install -r requirements.txt
```

---

### مشکل 3: Cron اجرا نمی‌شود

#### بررسی وضعیت:

**Termux:**
```bash
# بررسی crond
pgrep crond

# اگر خروجی ندادcrond را اجرا کنید
crond

# بررسی cron jobs
crontab -l
```

**Linux:**
```bash
# بررسی سرویس cron
sudo systemctl status cron

# فعال کردن
sudo systemctl enable cron
sudo systemctl start cron
```

**macOS:**
```bash
# بررسی LaunchAgent
launchctl list | grep multiproxy

# Load کردن مجدد
launchctl unload ~/Library/LaunchAgents/com.anonymous.multiproxy.plist
launchctl load ~/Library/LaunchAgents/com.anonymous.multiproxy.plist
```

---

### مشکل 4: خطای Permission Denied

#### راه حل:
```bash
cd ~/multi-proxy-config-fetcher

# اعطای مجوز اجرا
chmod +x run.sh
chmod +x manage.sh
chmod +x install.sh
```

---

### مشکل 5: فضای دیسک کم

#### بررسی فضا:
```bash
df -h

# حجم پوشه پروژه
du -sh ~/multi-proxy-config-fetcher
```

#### راه حل:
```bash
cd ~/multi-proxy-config-fetcher

# پاکسازی لاگ‌های قدیمی
bash manage.sh clean

# یا پاکسازی دستی
find logs -name "*.log" -mtime +3 -delete

# حذف cache Python
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
```

---

### مشکل 6: Termux بسته می‌شود

#### راه حل:
```bash
# فعال کردن Wake Lock
termux-wake-lock

# غیرفعال کردن Battery Optimization
# Settings → Apps → Termux → Battery → Unrestricted
```

#### نصب Termux:Boot (اختیاری):
1. دانلود [Termux:Boot از F-Droid](https://f-droid.org/packages/com.termux.boot/)
2. ایجاد اسکریپت startup:
```bash
mkdir -p ~/.termux/boot
cat > ~/.termux/boot/start-wizard.sh << 'EOF'
#!/data/data/com.termux/files/usr/bin/sh
termux-wake-lock
crond
EOF
chmod +x ~/.termux/boot/start-wizard.sh
```

---

### مشکل 7: دانلود Xray فیل می‌شود

#### راه حل Termux:
```bash
# نصب دستی با معماری صحیح
# بررسی معماری
uname -m

# ARM64:
curl -L https://github.com/XTLS/Xray-core/releases/latest/download/Xray-linux-arm64-v8a.zip -o /data/data/com.termux/files/usr/tmp/xray.zip

# ARM32:
curl -L https://github.com/XTLS/Xray-core/releases/latest/download/Xray-linux-arm32-v7a.zip -o /data/data/com.termux/files/usr/tmp/xray.zip

# استخراج و نصب
unzip /data/data/com.termux/files/usr/tmp/xray.zip -d /data/data/com.termux/files/usr/bin/
chmod +x /data/data/com.termux/files/usr/bin/xray
rm /data/data/com.termux/files/usr/tmp/xray.zip
```

---

## 📊 نظارت و لاگ‌ها

### مشاهده لاگ به صورت زنده:
```bash
# لاگ اجرای خودکار
tail -f ~/multi-proxy-config-fetcher/logs/cron.log

# آخرین اجرای دستی
tail -f ~/multi-proxy-config-fetcher/logs/run_*.log
```

### بررسی آخرین اجرا:
```bash
cd ~/multi-proxy-config-fetcher

# آخرین فایل لاگ
ls -lt logs/run_*.log | head -1

# مشاهده محتوا
cat $(ls -t logs/run_*.log | head -1)
```

### بررسی حجم فایل‌های خروجی:
```bash
du -h ~/multi-proxy-config-fetcher/configs/*
```

---

## 🗑️ حذف کامل

اگر می‌خواهید Multi Wizard را کاملاً حذف کنید:

### مرحله 1: حذف Cron Job
```bash
# Linux/Termux
crontab -l | grep -v "multi-proxy-config-fetcher" | crontab -

# macOS
launchctl unload ~/Library/LaunchAgents/com.anonymous.multiproxy.plist
rm ~/Library/LaunchAgents/com.anonymous.multiproxy.plist
```

### مرحله 2: حذف فایل‌ها
```bash
rm -rf ~/multi-proxy-config-fetcher
```

### مرحله 3: حذف Xray و Sing-box (اختیاری)
```bash
# Xray
sudo rm /usr/local/bin/xray     # Linux/macOS
rm $PREFIX/bin/xray              # Termux

# Sing-box
sudo apt remove sing-box -y      # Ubuntu/Debian
pkg uninstall sing-box -y        # Termux
brew uninstall sing-box          # macOS
```

---

## 💡 نکات کاربردی

### 1. سفارشی‌سازی منابع
```bash
# ویرایش فایل تنظیمات
nano ~/multi-proxy-config-fetcher/src/user_settings.py

# تغییر SOURCE_URLS
SOURCE_URLS = [
    "https://t.me/s/your_channel",
    "https://raw.githubusercontent.com/user/repo/main/configs.txt",
]

# ذخیره: Ctrl+O ثم Enter
# خروج: Ctrl+X
```

---

### 2. تنظیم پروتکل‌های فعال
```bash
nano ~/multi-proxy-config-fetcher/src/user_settings.py

# فعال/غیرفعال کردن پروتکل‌ها
ENABLED_PROTOCOLS = {
    "wireguard://": False,
    "hysteria2://": True,
    "vless://": True,
    "vmess://": True,
    "ss://": True,
    "trojan://": True,
    "tuic://": False,
}
```

---

### 3. تغییر تعداد Worker ها
برای افزایش سرعت (سیستم‌های قدرتمند):
```python
SINGBOX_TESTER_MAX_WORKERS = 16
XRAY_TESTER_MAX_WORKERS = 16
```

برای کاهش مصرف منابع (Termux یا سیستم‌های ضعیف):
```python
SINGBOX_TESTER_MAX_WORKERS = 4
XRAY_TESTER_MAX_WORKERS = 4
```

---

### 4. رمزنگاری فایل‌های حساس
```bash
# نصب GPG
pkg install gnupg           # Termux
sudo apt install gnupg -y   # Linux

# رمزنگاری فایل
gpg -c ~/multi-proxy-config-fetcher/configs/xray_secure_loadbalanced_config.json

# رمزگشایی
gpg ~/multi-proxy-config-fetcher/configs/xray_secure_loadbalanced_config.json.gpg
```

---

### 5. Backup خودکار
```bash
# ایجاد اسکریپت backup
cat > ~/multi-proxy-config-fetcher/backup.sh << 'EOF'
#!/usr/bin/env bash
DATE=$(date +%Y-%m-%d)
BACKUP_DIR=~/multi-proxy-backups/$DATE
mkdir -p $BACKUP_DIR
cp -r ~/multi-proxy-config-fetcher/configs $BACKUP_DIR/
echo "Backup created: $BACKUP_DIR"
EOF

chmod +x ~/multi-proxy-config-fetcher/backup.sh

# اضافه کردن به Cron (بعد از هر اجرا)
crontab -e

# اضافه کردن این خط:
0 */12 * * * cd ~/multi-proxy-config-fetcher && bash run.sh && bash backup.sh
```

---

### 6. نوتیفیکیشن Termux
```bash
# نصب Termux API
pkg install termux-api

# ویرایش run.sh برای اضافه کردن نوتیفیکیشن
nano ~/multi-proxy-config-fetcher/run.sh

# اضافه کردن در انتهای فایل قبل از EOF:
termux-notification --title "Multi Wizard" --content "Pipeline completed successfully!" --priority high
```

---

### 7. مانیتورینگ با Gotify/Telegram Bot (پیشرفته)
```bash
# مثال: ارسال به Telegram Bot
TELEGRAM_BOT_TOKEN="YOUR_BOT_TOKEN"
TELEGRAM_CHAT_ID="YOUR_CHAT_ID"

curl -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  -d "chat_id=${TELEGRAM_CHAT_ID}" \
  -d "text=✅ Multi Wizard: Pipeline completed successfully!"
```

---

## 🎓 آموزش گام به گام برای مبتدیان

### 🆕 کاربران تازه‌کار Termux:

#### قدم 1: نصب F-Droid و Termux
1. گوگل کنید: `F-Droid download`
2. دانلود و نصب F-Droid
3. باز کردن F-Droid
4. جستجوی `Termux`
5. نصب Termux
6. باز کردن Termux

#### قدم 2: به‌روزرسانی
```bash
pkg update
pkg upgrade -y
```
**صبر کنید تا تمام شود** (1-3 دقیقه)

#### قدم 3: نصب Multi Wizard
```bash
pkg install curl git -y
```
**صبر کنید** (30 ثانیه - 1 دقیقه)

```bash
curl -fsSL https://raw.githubusercontent.com/4n0nymou3/multi-proxy-config-fetcher/main/install.sh | bash
```
**صبر کنید** (10-20 دقیقه)

⚠️ **مهم**: در حین نصب Termux را نبندید!

#### قدم 4: اجرای اولین Pipeline
```bash
cd ~/multi-proxy-config-fetcher
bash run.sh
```
**صبر کنید** (5-15 دقیقه)

#### قدم 5: کپی کانفیگ‌ها
```bash
termux-setup-storage
```
**دسترسی به حافظه را بدهید**

```bash
cp ~/multi-proxy-config-fetcher/configs/xray_secure_loadbalanced_config.json ~/storage/downloads/
```

#### قدم 6: استفاده در v2rayNG
1. باز کردن v2rayNG
2. منو ☰ → Import config from file
3. رفتن به Downloads
4. انتخاب فایل JSON
5. Import

✅ **تمام! حالا می‌توانید اتصال برقرار کنید.**

---

## 📞 دریافت کمک و پشتیبانی

### قبل از درخواست کمک:

1. **بررسی لاگ‌ها:**
```bash
cd ~/multi-proxy-config-fetcher
bash manage.sh logs
```

2. **بررسی وضعیت:**
```bash
bash manage.sh status
```

3. **تست اجرای دستی:**
```bash
bash run.sh
```

---

### راه‌های دریافت کمک:

#### 1. GitHub Issues
- آدرس: https://github.com/4n0nymou3/multi-proxy-config-fetcher/issues
- کلیک روی **New Issue**
- توضیح مشکل + کپی لاگ خطا

#### 2. شبکه‌های اجتماعی
- **Twitter/X**: [@4n0nymou3](https://x.com/4n0nymou3)
- **GitHub**: [@4n0nymou3](https://github.com/4n0nymou3)

---

## ❓ سوالات متداول (FAQ)

### ❓ چقدر طول می‌کشد تا نصب کامل شود؟
**پاسخ**: 
- Linux/macOS: 5-10 دقیقه
- Termux: 10-20 دقیقه
- بستگی به سرعت اینترنت دارد

---

### ❓ چقدر فضا نیاز است؟
**پاسخ**: حداقل 500MB فضای خالی

---

### ❓ آیا باید همیشه Termux باز باشد؟
**پاسخ**: 
- برای اجرای دستی: بله
- برای اجرای خودکار: خیر، ولی باید crond فعال باشد

---

### ❓ کانفیگ‌ها هر چند وقت به‌روز می‌شوند؟
**پاسخ**: هر 12 ساعت یکبار (قابل تغییر)

---

### ❓ آیا می‌توانم منابع خودم را اضافه کنم؟
**پاسخ**: بله، فایل `src/user_settings.py` را ویرایش کنید

---

### ❓ کدام فایل برای v2rayNG بهتر است؟
**پاسخ**: `xray_secure_loadbalanced_config.json` (امن + لودبالانس)

---

### ❓ چگونه از GitHub به‌روزرسانی کنم؟
**پاسخ**:
```bash
cd ~/multi-proxy-config-fetcher
bash manage.sh update
```

---

### ❓ Xray و Sing-box چیست؟
**پاسخ**: 
- **Xray**: موتور تست پروکسی (مرحله 1)
- **Sing-box**: موتور تست پروکسی (مرحله 2)
- دو مرحله تست = کیفیت بالاتر

---

### ❓ آیا امن است؟
**پاسخ**: 
- ✅ کد Open Source است
- ✅ فقط از منابع عمومی دریافت می‌کند
- ✅ Security Filter اعمال می‌شود
- ⚠️ همیشه از `xray_secure_loadbalanced_config.json` استفاده کنید

---

### ❓ چگونه لاگ‌ها را پاک کنم؟
**پاسخ**:
```bash
bash manage.sh clean
```

---

### ❓ چگونه کاملاً حذف کنم؟
**پاسخ**: بخش [حذف کامل](#-حذف-کامل) را ببینید

---

## 🎯 خلاصه دستورات مهم

### نصب:
```bash
curl -fsSL https://raw.githubusercontent.com/4n0nymou3/multi-proxy-config-fetcher/main/install.sh | bash
```

### اجرای دستی:
```bash
cd ~/multi-proxy-config-fetcher && bash run.sh
```

### بررسی وضعیت:
```bash
bash manage.sh status
```

### مشاهده لاگ‌ها:
```bash
bash manage.sh logs
```

### به‌روزرسانی:
```bash
bash manage.sh update
```

### پاکسازی:
```bash
bash manage.sh clean
```

### کپی کانفیگ به گوشی (Termux):
```bash
cp ~/multi-proxy-config-fetcher/configs/xray_secure_loadbalanced_config.json ~/storage/downloads/
```

---

## 📚 منابع بیشتر

- **ریپازیتوری اصلی**: https://github.com/4n0nymou3/multi-proxy-config-fetcher
- **صفحه وب کانفیگ‌ها**: https://4n0nymou3.github.io/Anonymous-Proxy-Hub/
- **Xray-core**: https://github.com/XTLS/Xray-core
- **Sing-box**: https://sing-box.sagernet.org
- **v2rayNG**: https://github.com/2dust/v2rayNG
- **Termux**: https://termux.dev

---

## 📜 مجوز و سلب مسئولیت

این پروژه تحت مجوز **MIT License** منتشر شده است.

### ⚠️ سلب مسئولیت:
- این ابزار فقط برای اهداف **آموزشی و تحقیقاتی** ارائه شده است
- توسعه‌دهنده مسئولیتی در قبال استفاده نادرست ندارد
- کاربران موظفند قوانین محلی خود را رعایت کنند
- استفاده از کانفیگ‌های عمومی ممکن است ریسک امنیتی داشته باشد

---

## 🙏 تشکر و قدردانی

این پروژه با ❤️ توسط **👽 Anonymous** توسعه یافته است.

### سهم‌گذاران:
- **Xray-core Team** - موتور پروکسی قدرتمند
- **Sing-box Team** - موتور پروکسی جامع

### حمایت از پروژه:
- ⭐ **Star** کردن در GitHub

---

<div align="center">

## 🚀 آماده شروع هستید؟

```bash
curl -fsSL https://raw.githubusercontent.com/4n0nymou3/multi-proxy-config-fetcher/main/install.sh | bash
```

**ساخته شده با 💚 توسط Anonymous**

[⬆ بازگشت به بالا](#-راهنمای-کامل-multi-wizard)

</div>

</div>
