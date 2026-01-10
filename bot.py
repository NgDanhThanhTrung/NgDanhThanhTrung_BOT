import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# --- 1. CẤU HÌNH (CONFIG) ---
TOKEN = os.getenv('BOT_TOKEN') or "YOUR_TOKEN_HERE"

# URLs đơn lẻ
LOCKET_RAW_URL = "https://raw.githubusercontent.com/NgDanhThanhTrung/modules/main/LOCKET/Locket_NDTT.sgmodule"
SPOTIFY_RAW_URL = "https://raw.githubusercontent.com/NgDanhThanhTrung/modules/main/SPOTIFY/SPOTIFY.sgmodule"
YOUTUBE_RAW_URL = "https://raw.githubusercontent.com/NgDanhThanhTrung/modules/main/YOUTUBE/YOUTUBE.sgmodule"

# URLs Combo
SPOTIFY_LOCKETGOLD_RAW_URL = "https://raw.githubusercontent.com/NgDanhThanhTrung/modules/main/Test_modules/Tong_hop/Spotify_LocketGold.sgmodule"
SPOTIFY_YOUTUBE_LOCKET_RAW_URL = "https://raw.githubusercontent.com/NgDanhThanhTrung/modules/main/tonghopv2/Spotity_Youtube_Locket%20.conf"

# Thông tin hỗ trợ
WEB_URL = "https://ngdanhthanhtrung.github.io/Modules-NDTT-Premium/"
CONTACT_URL = "https://t.me/NgDanhThanhTrung"
DONATE_URL = "https://ngdanhthanhtrung.github.io/Bank/"

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- 2. CÁC HÀM XỬ LÝ (HANDLERS) ---

async def post_init(application):
    """Tự động cài đặt nút Menu lệnh cho Bot"""
    commands = [
        BotCommand("start", "Khởi động bot"),
        BotCommand("hdsd", "Danh sách lệnh hỗ trợ"),
        BotCommand("locket", "Cài Locket Gold"),
        BotCommand("spotify", "Cài Spotify Premium"),
        BotCommand("youtube", "Cài YouTube Premium"),
        BotCommand("spotify_locketgold", "Combo Spotify & Locket"),
        BotCommand("spotify_youtube_locket", "Combo 3-trong-1 (Tất cả)"),
    ]
    await application.bot.set_my_commands(commands)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    await update.message.reply_text(
        f"👋 Chào mừng <b>{user_name}</b> đến với NgDanhThanhTrung_BOT!\n\n"
        "Gõ /hdsd để xem tất cả các hướng dẫn cài đặt Module.",
        parse_mode=ParseMode.HTML
    )

async def hdsd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("✨ Web Hướng Dẫn", url=WEB_URL)],
        [InlineKeyboardButton("💬 Liên hệ Admin", url=CONTACT_URL), 
         InlineKeyboardButton("☕ Donate", url=DONATE_URL)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = (
        "<b>📚 DANH SÁCH LỆNH CÀI ĐẶT:</b>\n\n"
        "💛 /locket - Locket Gold\n"
        "🎵 /spotify - Spotify Premium\n"
        "🔴 /youtube - YouTube Premium\n\n"
        "<b>🎁 CÁC BẢN COMBO:</b>\n"
        "✌️ /spotify_locketgold - Combo 2-trong-1\n"
        "💎 /spotify_youtube_locket - Siêu Combo 3-trong-1\n\n"
        "<i>Hãy chọn lệnh tương ứng để lấy link Module!</i>"
    )
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)

async def send_guide(update, title, url, note=""):
    """Hàm mẫu chung gửi hướng dẫn kèm lưu ý và quảng cáo mới"""
    keyboard = [[InlineKeyboardButton(f"🔗 Sao chép URL {title}", url=url)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    guide_text = (
        f"✨ <b>HƯỚNG DẪN CÀI ĐẶT {title.upper()}</b> ✨\n\n"
        f"1️⃣ <b>Copy URL:</b> Nhấn nút bên dưới để lấy link Module.\n\n"
        f"2️⃣ <b>Shadowrocket:</b> Tab <b>Module</b> ➔ <b>Add Module</b> ➔ Dán URL ➔ OK.\n"
        f"{note}\n"
        f"3️⃣ <b>HTTPS Decryption:</b>\n"
        f"• Bật <b>HTTPS Decryption</b> trong Settings.\n"
        f"• Chọn <b>Generate New CA</b> ➔ Install.\n"
        f"• Vào Cài đặt máy ➔ Đã tải về hồ sơ ➔ Tin cậy chứng chỉ.\n\n"
        f"4️⃣ <b>Kết nối:</b> Bật VPN và tận hưởng!\n\n"
        f"⚠️ <b>LƯU Ý: NẾU TẮT VPN SẼ MẤT, INBOX AD ĐỂ ĐƯỢC HỖ TRỢ DÙNG LÂU DÀI</b>\n\n"
        f"💰 <b>Giá rẻ \"giật mình\" – Chỉ bằng vài ly trà sữa là có Combo trọn đời!</b>\n"
        f"📥 <b>Inbox ngay để nhận báo giá \"Học sinh - Sinh viên\" nhất thị trường!</b>\n"
        f"👉 Nhắn tin tại đây: {CONTACT_URL}"
    )
    await update.message.reply_text(guide_text, parse_mode=ParseMode.HTML, reply_markup=reply_markup)

# --- Điều hướng lệnh ---
async def locket(update, context): await send_guide(update, "Locket Gold", LOCKET_RAW_URL)
async def spotify(update, context): await send_guide(update, "Spotify Premium", SPOTIFY_RAW_URL)
async def youtube(update, context): await send_guide(update, "YouTube Premium", YOUTUBE_RAW_URL)
async def spotify_locketgold(update, context): await send_guide(update, "Combo Spotify & Locket", SPOTIFY_LOCKETGOLD_RAW_URL)
async def spotify_youtube_locket(update, context): 
    note = "<i>(Lưu ý: File .conf này hoạt động tương tự Module)</i>\n"
    await send_guide(update, "Siêu Combo 3-trong-1", SPOTIFY_YOUTUBE_LOCKET_RAW_URL, note)

async def contact(update, context):
    keyboard = [[InlineKeyboardButton("💬 Nhắn tin cho Admin", url=CONTACT_URL)]]
    text = (
        "💰 <b>Giá rẻ \"giật mình\" – Chỉ bằng vài ly trà sữa là có Combo trọn đời!</b>\n"
        "📥 <b>Inbox ngay để nhận báo giá \"Học sinh - Sinh viên\" nhất thị trường!</b>"
    )
    await update.message.reply_text(text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))

async def donate(update, context):
    keyboard = [[InlineKeyboardButton("☕ Mở trang Donate", url=DONATE_URL)]]
    await update.message.reply_text("Cảm ơn bạn đã ủng hộ duy trì dự án! ❤️", reply_markup=InlineKeyboardMarkup(keyboard))

# --- 3. KHỞI CHẠY (MAIN) ---

def main():
    if not TOKEN or TOKEN == "YOUR_TOKEN_HERE":
        print("❌ Lỗi: Bạn chưa cấu hình BOT_TOKEN!")
        return

    app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("hdsd", hdsd))
    app.add_handler(CommandHandler("help", hdsd))
    app.add_handler(CommandHandler("locket", locket))
    app.add_handler(CommandHandler("spotify", spotify))
    app.add_handler(CommandHandler("youtube", youtube))
    app.add_handler(CommandHandler("spotify_locketgold", spotify_locketgold))
    app.add_handler(CommandHandler("spotify_youtube_locket", spotify_youtube_locket))
    app.add_handler(CommandHandler("contact", contact))
    app.add_handler(CommandHandler("donate", donate))
    
    print("--- 🤖 Bot đã cập nhật nội dung mới và sẵn sàng ---")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
