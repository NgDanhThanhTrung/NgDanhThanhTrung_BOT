import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# --- CẤU HÌNH ---
TOKEN = os.getenv('BOT_TOKEN')
RAW_URL = "https://raw.githubusercontent.com/NgDanhThanhTrung/modules/main/LOCKET/Locket_NDTT.sgmodule"
CONTACT_URL = "https://t.me/NgDanhThanhTrung"
DONATE_URL = "https://ngdanhthanhtrung.github.io/Bank/"

# Thiết lập logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# --- CÁC HÀM XỬ LÝ LỆNH ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_text = (
        "👋 Chào mừng bạn đến với NgDanhThanhTrung_BOT!\n")

async def locket_handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý lệnh /locket với nút copy ẩn"""
    message_text = (
        f"✨ **HƯỚNG DẪN CÀI ĐẶT LOCKET GOLD** ✨\n\n"
        f"1️⃣ **Copy URL Module:**\n`{RAW_URL}`\n\n"
        f"2️⃣ **Thêm vào Shadowrocket:**\n"
        f"Mở Shadowrocket ➔ **Module** ➔ **Add Module** ➔ Dán URL.\n\n"
        f"3️⃣ **Cấu hình HTTPS Decryption:**\n"
        f"• Bật **HTTPS Decryption** trong Settings.\n"
        f"• Cài đặt & **Tin cậy chứng chỉ** (CA Certificate).\n\n"
        f"4️⃣ **Hoàn tất:**\n"
        f"Bật VPN Shadowrocket và mở lại app Locket."
    )
    
    # Chỉnh sửa nút Mở liên kết thành nút Copy ẩn (switch_inline_query_current_chat)
    keyboard = [
        [InlineKeyboardButton("📋 Sao chép Module (Bấm & Copy)", switch_inline_query_current_chat=RAW_URL)],
        [InlineKeyboardButton("🆘 Cần hỗ trợ kỹ thuật", url=CONTACT_URL)],
        [InlineKeyboardButton("☕ Donate ủng hộ", url=DONATE_URL)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        message_text, 
        reply_markup=reply_markup, 
        parse_mode=ParseMode.MARKDOWN
    )

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý lệnh /contact"""
    keyboard = [[InlineKeyboardButton("💬 Nhắn tin cho Admin", url=CONTACT_URL)]]
    await update.message.reply_text(
        "Bạn cần giúp đỡ? Nhấn nút bên dưới:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def donate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý lệnh /donate"""
    keyboard = [[InlineKeyboardButton("💳 Mở trang Donate", url=DONATE_URL)]]
    await update.message.reply_text(
        "Cảm ơn bạn đã ủng hộ duy trì dự án!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# --- KHỞI CHẠY ---

def main():
    if not TOKEN:
        logger.error("BOT_TOKEN không tìm thấy!")
        return

    app = ApplicationBuilder().token(TOKEN).build()

    # Đăng ký đầy đủ các Handler
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("locket", locket_handle))
    app.add_handler(CommandHandler("contact", contact))
    app.add_handler(CommandHandler("donate", donate))

    logger.info("Bot đã sẵn sàng và đang chờ lệnh...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()