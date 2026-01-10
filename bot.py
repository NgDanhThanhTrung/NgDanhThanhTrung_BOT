import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# --- CẤU HÌNH ---
LOCKET_WEB_URL = "https://ngdanhthanhtrung.github.io/locket/"
TOKEN = os.getenv('BOT_TOKEN')
RAW_URL = "https://raw.githubusercontent.com/NgDanhThanhTrung/modules/main/LOCKET/Locket_NDTT.sgmodule"
CONTACT_URL = "https://t.me/NgDanhThanhTrung"
DONATE_URL = "https://ngdanhthanhtrung.github.io/Bank/"

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- CÁC HÀM XỬ LÝ ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"👋 Chào mừng bạn đến với NgDanhThanhTrung_BOT!\n"
        "Gõ /hdsd để xem các lệnh ."
    )

async def hdsd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("✨ Hướng dẫn Locket Gold", url=LOCKET_WEB_URL)],
        [InlineKeyboardButton("💬 Liên hệ", url=CONTACT_URL), 
         InlineKeyboardButton("☕ Donate", url=DONATE_URL)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"/locket - Hướng Dẫn Up LocketGold\n"
        "/contact - Liên Hệ Để Được Hỗ Trợ\n"
        "/donate - Ủng Hộ NgDanhThanhTrung Cho Những Dự Án Trong Tương Lai .",
        reply_markup=reply_markup
    )

async def locket(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🔗 Sao chép URL Module (Nhấn giữ)", url=RAW_URL)]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
            f"✨ **HƯỚNG DẪN CÀI ĐẶT LOCKET GOLD** ✨\n\n"
            f"Vui lòng thực hiện theo đúng trình tự để Module hoạt động ổn định:\n\n"
            f"1️⃣ **Chuẩn bị URL Module:**\n"
            f"Nhấn nút **Sao chép URL** ở phía dưới. Đây là liên kết chứa các tập lệnh (Script) cần thiết.\n\n"
            f"2️⃣ **Thêm vào Shadowrocket:**\n"
            f"Mở app Shadowrocket ➔ Chọn tab **Module** (hình hộp) ➔ Nhấn **Add Module** ➔ Dán URL và nhấn **OK**.\n\n"
            f"3️⃣ **Cấu hình HTTPS Decryption (Quan trọng):**\n"
            f"• Vào tab **Settings** ➔ **HTTPS Decryption**.\n"
            f"• Bật công tắc **HTTPS Decryption**.\n"
            f"• Chọn **Generate New CA Certificate** ➔ **Install Certificate**.\n"
            f"• Vào **Cài đặt máy** ➔ **Đã tải về hồ sơ** ➔ **Cài đặt**.\n"
            f"• Vào **Cài đặt máy** ➔ **Cài đặt chung** ➔ **Giới thiệu** ➔ **Tin cậy chứng chỉ** ➔ **Bật tin cậy** cho Shadowrocket.\n\n"
            f"4️⃣ **Hoàn tất & Kiểm tra:**\n"
            f"Quay lại tab **Home**, nhấn **Connect**. Mở Locket và kiểm tra trạng thái **Gold**.\n\n"
            f"⚠️ *Lưu ý: Nếu không hiện Gold, hãy vuốt đóng Locket và mở lại.*",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("💬 Nhắn tin ngay", url=CONTACT_URL)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f"💬 Liên hệ Admin: {CONTACT_URL}", reply_markup=reply_markup)

async def donate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("☕ Mở trang Donate", url=DONATE_URL)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(f"☕ Donate ủng hộ tại: {DONATE_URL}", reply_markup=reply_markup)

# --- KHỞI CHẠY ---

def main():
    if not TOKEN:
        print("❌ Lỗi: Không tìm thấy BOT_TOKEN!")
        return

    app = ApplicationBuilder().token(TOKEN).build()

    # Đăng ký các lệnh
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("locket", locket))
    app.add_handler(CommandHandler("contact", contact))
    app.add_handler(CommandHandler("donate", donate))
    app.add_handler(CommandHandler("hdsd", hdsd))
    
    print("--- 🤖 NgDanhThanhTrung_BOT Ready ---")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
