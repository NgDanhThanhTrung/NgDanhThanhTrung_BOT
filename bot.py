import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# --- CẤU HÌNH ---
# Đảm bảo bạn đã set môi trường BOT_TOKEN hoặc thay trực tiếp token vào đây
TOKEN = os.getenv('BOT_TOKEN') 
RAW_URL = "https://raw.githubusercontent.com/NgDanhThanhTrung/modules/main/LOCKET/Locket_NDTT.sgmodule"
CONTACT_URL = "https://t.me/NgDanhThanhTrung"
DONATE_URL = "https://ngdanhthanhtrung.github.io/Bank/"

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- CÁC HÀM XỬ LÝ ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Chào mừng bạn đến với **NgDanhThanhTrung_BOT**!\n"
        "Gõ /locket để xem hướng dẫn hoặc /filters để xem các lệnh khác.",
        parse_mode='Markdown'
    )

async def locket_handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Tạo nút bấm để giao diện chuyên nghiệp hơn
    keyboard = [
        [InlineKeyboardButton("🔗 Copy Link Module", url=RAW_URL)],
        [InlineKeyboardButton("💬 Liên hệ Admin", url=CONTACT_URL),
         InlineKeyboardButton("☕ Donate", url=DONATE_URL)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = (
        "✨ **HƯỚNG DẪN CÀI ĐẶT LOCKET GOLD** ✨\n\n"
        "1️⃣ **Chuẩn bị:** Copy URL Module bằng nút bên dưới.\n\n"
        "2️⃣ **Thêm vào Shadowrocket:**\n"
        "Mở app ➔ **Module** ➔ **Add Module** ➔ Dán URL ➔ **OK**.\n\n"
        "3️⃣ **Cấu hình HTTPS Decryption (Bắt buộc):**\n"
        "• Vào **Settings** ➔ **HTTPS Decryption** ➔ Bật công tắc.\n"
        "• Chọn **Generate New CA Certificate** ➔ **Install Certificate**.\n"
        "• Vào **Cài đặt máy** ➔ **Đã tải về hồ sơ** ➔ **Cài đặt**.\n"
        "• Vào **Cài đặt máy** ➔ **Cài đặt chung** ➔ **Giới thiệu** ➔ **Tin cậy chứng chỉ** ➔ Bật tin cậy cho Shadowrocket.\n\n"
        "4️⃣ **Kiểm tra:** Quay lại tab Home, nhấn **Connect**. Sau đó mở Locket."
    )
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"💬 Liên hệ Admin tại đây: {CONTACT_URL}")

async def donate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"☕ Donate ủng hộ mình tại: {DONATE_URL}")

async def filters_handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Trả lời danh sách lệnh theo yêu cầu của bạn
    text = (
        "• `/start`\n"
        "• `/locket`\n"
        "• `/contact`\n"
        "• `/donate`\n"
        "• `/filters`"
    )
    await update.message.reply_text(text, parse_mode='Markdown')

# --- KHỞI CHẠY ---

def main():
    if not TOKEN:
        print("❌ Lỗi: Không tìm thấy BOT_TOKEN trong biến môi trường!")
        return

    # Khởi tạo Application
    app = ApplicationBuilder().token(TOKEN).build()

    # Đăng ký các lệnh (Commands)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("locket", locket_handle))
    app.add_handler(CommandHandler("contact", contact))
    app.add_handler(CommandHandler("donate", donate))
    app.add_handler(CommandHandler("filters", filters_handle))

    # Tự động trả lời khi tin nhắn chứa từ "locket" (không phân biệt hoa thường)
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND) & filters.Regex(r"(?i)locket"), locket_handle))

    print("--- 🤖 NgDanhThanhTrung_BOT is Running ---")
    
    # Bắt đầu nhận tin nhắn
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
