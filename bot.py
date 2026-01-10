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

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- CÁC HÀM XỬ LÝ ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Chào mừng bạn đến với NgDanhThanhTrung_BOT!\nGõ /locket để xem hướng dẫn cài đặt.")

async def locket_handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        f"✨ **HƯỚNG DẪN CÀI ĐẶT LOCKET GOLD** ✨\n\n"
        f"1️⃣ **Chuẩn bị URL Module:**\n`{RAW_URL}`\n\n"
        f"2️⃣ **Thêm vào Shadowrocket:**\n"
        f"Mở app ➔ **Module** ➔ **Add Module** ➔ Dán URL và nhấn **OK**.\n\n"
        f"3️⃣ **Cấu hình HTTPS Decryption:**\n"
        f"• Bật **HTTPS Decryption** trong Settings.\n"
        f"• **Generate New CA Certificate** ➔ **Install**.\n"
        f"• Vào **Cài đặt máy** ➔ **Tin cậy chứng chỉ** cho Shadowrocket.\n\n"
        f"4️⃣ **Hoàn tất:** Mở Locket và tận hưởng Gold."
    )
    await update.message.reply_text(text, parse_mode='Markdown')

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"💬 Liên hệ Admin: {CONTACT_URL}")

async def donate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"☕ Donate ủng hộ tại: {DONATE_URL}")

async def filters_handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Trả lời đúng danh sách lệnh khi có /filters
    text = (
        "• \"/start\"\n"
        "• \"/locket\"\n"
        "• \"/contact\"\n"
        "• \"/donate\"\n"
        "• \"/filters\""
    )
    await update.message.reply_text(text)

# --- KHỞI CHẠY ---

def main():
    if not TOKEN:
        print("❌ Lỗi: Không tìm thấy BOT_TOKEN!")
        return

    app = ApplicationBuilder().token(TOKEN).build()

    # Đăng ký các CommandHandler (Chỉ phản hồi khi có dấu /)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("locket", locket_handle))
    app.add_handler(CommandHandler("contact", contact))
    app.add_handler(CommandHandler("donate", donate))
    app.add_handler(CommandHandler("filters", filters_handle))

    # Giữ lại tính năng tự động phản hồi khi người dùng gõ chữ "locket" không có dấu /
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND) & filters.Regex(r"(?i)locket"), locket_handle))

    print("--- 🤖 NgDanhThanhTrung_BOT Ready ---")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
