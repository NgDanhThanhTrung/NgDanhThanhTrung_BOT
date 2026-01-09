Import os
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
    await update.message.reply_text("👋 Chào mừng bạn đến với NgDanhThanhTrung_BOT!\nGõ /locket để xem hướng dẫn.")

async def locket_handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
            f"✨ **HƯỚNG DẪN CÀI ĐẶT LOCKET GOLD** ✨\n\n"
            f"1️⃣ **URL Module:**\n"
            f"{RAW_URL}\n\n"
            f"2️⃣ **Thêm vào Shadowrocket:**\n"
            f"Tab **Module** ➔ **Add Module** ➔ Dán URL ➔ **OK**.\n\n"
            f"3️⃣ **HTTPS Decryption:**\n"
            f"• **Settings** ➔ **HTTPS Decryption** ➔ Bật công tắc.\n"
            f"• **Generate New CA Certificate** ➔ **Install Certificate**.\n"
            f"• **Cài đặt máy** ➔ **Đã tải về hồ sơ** ➔ **Cài đặt**.\n"
            f"• **Cài đặt chung** ➔ **Giới thiệu** ➔ **Tin cậy chứng chỉ** ➔ **Bật tin cậy**.\n\n"
            f"4️⃣ **Hoàn tất:**\n"
            f"Bật **Connect**. Mở Locket kiểm tra.\n\n"
            f"⚠️ *Lưu ý: Nếu không hiện Gold, hãy đóng Locket và mở lại. Có thể vào trang web sau https://ngdanhthanhtrung.github.io/locket/*",
            parse_mode='Markdown'
        )

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"💬 Liên hệ Admin: {CONTACT_URL}")

async def donate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"☕ Donate tại: {DONATE_URL}")

# --- KHỞI CHẠY ---

def main():
    if not TOKEN:
        print("❌ Lỗi: Không tìm thấy BOT_TOKEN!")
        return

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("locket", locket_handle))
    app.add_handler(CommandHandler("contact", contact))
    app.add_handler(CommandHandler("donate", donate))

    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND) & filters.Regex(r"(?i)locket"), locket_handle))

    print("--- 🤖 NgDanhThanhTrung_BOT Ready ---")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
