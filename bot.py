import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# --- CẤU HÌNH ---
TOKEN = os.getenv('BOT_TOKEN')
RAW_URL = "https://raw.githubusercontent.com/NgDanhThanhTrung/modules/main/LOCKET/Locket_NDTT.sgmodule"
CONTACT_URL = "https://t.me/NgDanhThanhTrung"
DONATE_URL = "https://ngdanhthanhtrung.github.io/Bank/"

# Thiết lập Logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- CÁC HÀM XỬ LÝ ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý lệnh /start"""
    await update.message.reply_text("👋 Chào mừng bạn đến với NgDanhThanhTrung_BOT!\nSử dụng lệnh /locket để lấy cấu hình giả lập.")

async def send_locket_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý khi người dùng dùng lệnh /locket hoặc nhắn chữ 'locket'"""
    response = (
        "<b>⭐ LOCKET NDTT MODULE - 2026 ⭐</b>\n"
        "────────────────\n"
        "Hướng dẫn giả lập <b>Locket Gold</b> vĩnh viễn:\n\n"
        "1️⃣ <b>Copy URL Module:</b>\n"
        f"<code>{RAW_URL}</code>\n\n"
        "2️⃣ <b>Shadowrocket:</b> Tab Module > Add Module > Dán link.\n\n"
        "3️⃣ <b>HTTPS Decryption:</b> Cài chứng chỉ CA và <b>Bật tin cậy</b>.\n\n"
        "4️⃣ <b>Hoàn tất:</b> Bật VPN và mở Locket hưởng thụ."
    )
    
    keyboard = [
        [InlineKeyboardButton("🚀 Cài nhanh (Shadowrocket)", url=f"shadowrocket://config/add/{RAW_URL}")],
        [InlineKeyboardButton("💬 Liên hệ Admin", url=CONTACT_URL)],
        [InlineKeyboardButton("☕ Donate", url=DONATE_URL)]
    ]
    
    await update.message.reply_text(
        text=response,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
    )

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý lệnh /contact"""
    await update.message.reply_text(f"💬 Liên hệ Admin tại đây: {CONTACT_URL}")

async def donate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý lệnh /donate"""
    await update.message.reply_text(f"☕ Donate ủng hộ tác giả: {DONATE_URL}")

# --- HÀM CHÍNH ---

def main():
    if not TOKEN:
        print("❌ Lỗi: Không tìm thấy BOT_TOKEN trong biến môi trường!")
        return

    # Khởi tạo Application
    app = ApplicationBuilder().token(TOKEN).build()

    # Thêm các Handler cho lệnh (Commands)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("locket", send_locket_info))
    app.add_handler(CommandHandler("contact", contact))
    app.add_handler(CommandHandler("donate", donate))

    # Xử lý tin nhắn văn bản bình thường (Nếu chứa từ 'locket' thì cũng gửi hướng dẫn)
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND) & filters.Regex(r"(?i)locket"), send_locket_info))

    print("--- 🤖 NgDanhThanhTrung_BOT 2026 Ready ---")
    
    # Chạy bot và loại bỏ các tin nhắn tồn đọng cũ
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
