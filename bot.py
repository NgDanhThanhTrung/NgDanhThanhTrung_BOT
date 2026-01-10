import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# --- CẤU HÌNH ---
TOKEN = os.getenv('BOT_TOKEN') or "YOUR_TOKEN_HERE"
WEB_URL = "https://ngdanhthanhtrung.github.io/Modules-NDTT-Premium/"
LOCKET_RAW_URL = "https://raw.githubusercontent.com/NgDanhThanhTrung/modules/main/LOCKET/Locket_NDTT.sgmodule"
SPOTIFY_RAW_URL = "https://raw.githubusercontent.com/NgDanhThanhTrung/modules/main/SPOTIFY/SPOTIFY.sgmodule"
CONTACT_URL = "https://t.me/NgDanhThanhTrung"
DONATE_URL = "https://ngdanhthanhtrung.github.io/Bank/"

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- CÁC HÀM XỬ LÝ ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    await update.message.reply_text(
        f"👋 Chào mừng <b>{user_name}</b> đến với NgDanhThanhTrung_BOT!\n\n"
        "Gõ /hdsd để xem danh sách lệnh hỗ trợ.",
        parse_mode=ParseMode.HTML
    )

async def hdsd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("✨ Hướng dẫn Cài Modules", url=WEB_URL)],
        [InlineKeyboardButton("💬 Liên hệ", url=CONTACT_URL), 
         InlineKeyboardButton("☕ Donate", url=DONATE_URL)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = (
        "<b>📚 DANH SÁCH LỆNH:</b>\n\n"
        "💛 /locket - Hướng dẫn cài đặt Locket Gold\n"
        "🎵 /spotify - Hướng dẫn cài đặt Spotify Premium\n"
        "💬 /contact - Liên hệ hỗ trợ trực tiếp\n"
        "☕ /donate - Ủng hộ duy trì dự án"
    )
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)

async def locket(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🔗 Sao chép URL Locket Module", url=LOCKET_RAW_URL)]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    guide_text = (
        "✨ <b>HƯỚNG DẪN CÀI ĐẶT LOCKET GOLD</b> ✨\n\n"
        "1️⃣ <b>Copy URL:</b> Nhấn nút bên dưới để lấy link Module.\n\n"
        "2️⃣ <b>Shadowrocket:</b> Tab <b>Module</b> ➔ <b>Add Module</b> ➔ Dán URL ➔ OK.\n\n"
        "3️⃣ <b>HTTPS Decryption:</b>\n"
        "• Bật <b>HTTPS Decryption</b> trong Settings.\n"
        "• Chọn <b>Generate New CA</b> ➔ Install.\n"
        "• Vào Cài đặt máy ➔ Đã tải về hồ sơ ➔ Tin cậy chứng chỉ.\n\n"
        "4️⃣ <b>Kết nối:</b> Bật VPN và tận hưởng!"
    )
    await update.message.reply_text(guide_text, parse_mode=ParseMode.HTML, reply_markup=reply_markup)

async def spotify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🔗 Sao chép URL Spotify Module", url=SPOTIFY_RAW_URL)]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    guide_text = (
        "🎵 <b>HƯỚNG DẪN CÀI ĐẶT SPOTIFY PREMIUM</b> 🎵\n\n"
        "1️⃣ <b>Copy URL:</b> Nhấn nút bên dưới để lấy link Module.\n\n"
        "2️⃣ <b>Shadowrocket:</b> Tab <b>Module</b> ➔ <b>Add Module</b> ➔ Dán URL ➔ OK.\n\n"
        "3️⃣ <b>HTTPS Decryption:</b>\n"
        "• Bật <b>HTTPS Decryption</b> trong Settings.\n"
        "• Chọn <b>Generate New CA</b> ➔ Install.\n"
        "• Vào Cài đặt máy ➔ Đã tải về hồ sơ ➔ Tin cậy chứng chỉ.\n\n"
        "4️⃣ <b>Kết nối:</b> Bật VPN và tận hưởng âm nhạc!"
    )
    await update.message.reply_text(guide_text, parse_mode=ParseMode.HTML, reply_markup=reply_markup)

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("💬 Nhắn tin cho Admin", url=CONTACT_URL)]]
    await update.message.reply_text("Nếu gặp lỗi trong quá trình cài đặt, hãy liên hệ:", reply_markup=InlineKeyboardMarkup(keyboard))

async def donate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("☕ Mở trang Donate", url=DONATE_URL)]]
    await update.message.reply_text("Cảm ơn bạn đã có lòng ủng hộ dự án! ❤️", reply_markup=InlineKeyboardMarkup(keyboard))

# --- KHỞI CHẠY ---

def main():
    if not TOKEN or TOKEN == "YOUR_TOKEN_HERE":
        print("❌ Lỗi: Bạn chưa cấu hình BOT_TOKEN!")
        return

    app = ApplicationBuilder().token(TOKEN).build()

    # Đăng ký các lệnh
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("locket", locket))
    app.add_handler(CommandHandler("spotify", spotify))
    app.add_handler(CommandHandler("contact", contact))
    app.add_handler(CommandHandler("donate", donate))
    app.add_handler(CommandHandler("hdsd", hdsd))
    app.add_handler(CommandHandler("help", hdsd))
    
    print("--- 🤖 Bot đang chạy đầy đủ tính năng ---")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
