import os
import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# --- 1. CẤU HÌNH (CONFIG) ---
TOKEN = os.getenv('BOT_TOKEN') or "YOUR_TOKEN_HERE"
ADMIN_ID = 7346983056 
USER_LIST_FILE = "users.txt"

# URLs Modules
LOCKET_RAW_URL = "https://raw.githubusercontent.com/NgDanhThanhTrung/modules/main/LOCKET/Locket_NDTT.sgmodule"
SPOTIFY_RAW_URL = "https://raw.githubusercontent.com/NgDanhThanhTrung/modules/main/SPOTIFY/SPOTIFY.sgmodule"
YOUTUBE_RAW_URL = "https://raw.githubusercontent.com/NgDanhThanhTrung/modules/main/YOUTUBE/YOUTUBE.sgmodule"
SPOTIFY_LOCKETGOLD_RAW_URL = "https://raw.githubusercontent.com/NgDanhThanhTrung/modules/main/Test_modules/Tong_hop/Spotify_LocketGold.sgmodule"
SPOTIFY_YOUTUBE_LOCKET_RAW_URL = "https://raw.githubusercontent.com/NgDanhThanhTrung/modules/main/tonghopv2/Spotity_Youtube_Locket%20.conf"

WEB_URL = "https://ngdanhthanhtrung.github.io/Modules-NDTT-Premium/"
CONTACT_URL = "https://t.me/NgDanhThanhTrung"
DONATE_URL = "https://ngdanhthanhtrung.github.io/Bank/"

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- 2. LOGIC HỆ THỐNG ---

def save_user(user_id):
    if not os.path.exists(USER_LIST_FILE):
        open(USER_LIST_FILE, "w").close()
    with open(USER_LIST_FILE, "r") as f:
        users = f.read().splitlines()
    if str(user_id) not in users:
        with open(USER_LIST_FILE, "a") as f:
            f.write(f"{user_id}\n")

# --- 3. HANDLERS ---

async def post_init(application):
    commands = [
        BotCommand("start", "Khởi động bot"),
        BotCommand("hdsd", "Danh sách lệnh hỗ trợ"),
        BotCommand("locket", "Cài Locket Gold"),
        BotCommand("spotify", "Cài Spotify Premium"),
        BotCommand("youtube", "Cài YouTube Premium"),
        BotCommand("broadcast", "Gửi thông báo (Admin)"),
    ]
    await application.bot.set_my_commands(commands)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    save_user(user.id)
    await update.message.reply_text(
        f"👋 Chào mừng <b>{user.first_name}</b> đến với NgDanhThanhTrung_BOT!\n\n"
        "Gõ /hdsd để xem tất cả các hướng dẫn cài đặt Module.",
        parse_mode=ParseMode.HTML
    )

async def hdsd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    save_user(update.effective_user.id)
    keyboard = [
        [InlineKeyboardButton("✨ Web Hướng Dẫn", url=WEB_URL)],
        [InlineKeyboardButton("💬 Liên hệ Admin", url=CONTACT_URL), 
         InlineKeyboardButton("☕ Donate", url=DONATE_URL)]
    ]
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
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.HTML)

async def send_guide(update, title, url, note=""):
    keyboard = [[InlineKeyboardButton(f"🔗 Sao chép URL {title}", url=url)]]
    guide_text = (
        f"✨ <b>HƯỚNG DẪN CÀI ĐẶT {title.upper()}</b> ✨\n\n"
        f"1️⃣ <b>Copy URL:</b> Chạm giữ link bên dưới để sao chép:\n<code>{url}</code>\n\n"
        f"2️⃣ <b>Shadowrocket:</b> Tab <b>Module</b> ➔ <b>Add Module</b> ➔ Dán URL ➔ OK.\n"
        f"{note}\n"
        f"3️⃣ <b>HTTPS Decryption:</b>\n"
        f"• Bật <b>HTTPS Decryption</b> trong Settings.\n"
        f"• Chọn <b>Generate New CA</b> ➔ Install.\n"
        f"• Vào Cài đặt máy ➔ Đã tải về hồ sơ ➔ Tin cậy chứng chỉ.\n\n"
        f"4️⃣ <b>Kết nối:</b> Bật VPN và tận hưởng!\n\n"
        f"⚠️ <b>LƯU Ý: NẾU TẮT VPN SẼ MẤT, INBOX AD ĐỂ ĐƯỢC HỖ TRỢ DÙNG LÂU DÀI</b>\n\n"
        f"💰 <b>Giá rẻ \"giật mình\" – Chỉ bằng vài ly trà sữa là có Combo trọn đời!</b>\n"
        f"👉 Nhắn tin tại đây: {CONTACT_URL}"
    )
    await update.message.reply_text(guide_text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    if not context.args:
        await update.message.reply_text("⚠️ Cú pháp: <code>/broadcast Nội dung</code>", parse_mode=ParseMode.HTML)
        return
    
    msg_text = " ".join(context.args)
    with open(USER_LIST_FILE, "r") as f:
        users = f.read().splitlines()

    sent, fail = 0, 0
    status_msg = await update.message.reply_text(f"🚀 Đang gửi thông báo đến {len(users)} người...")

    for user_id in users:
        try:
            await context.bot.send_message(
                chat_id=user_id, 
                text=f"📢 <b>THÔNG BÁO TỪ ADMIN:</b>\n\n{msg_text}", 
                parse_mode=ParseMode.HTML
            )
            sent += 1
            await asyncio.sleep(0.05)
        except: fail += 1

    await status_msg.edit_text(f"✅ Gửi xong!\n- Thành công: {sent}\n- Thất bại: {fail}", parse_mode=ParseMode.HTML)

async def locket(u, c): await send_guide(u, "Locket Gold", LOCKET_RAW_URL)
async def spotify(u, c): await send_guide(u, "Spotify Premium", SPOTIFY_RAW_URL)
async def youtube(u, c): await send_guide(u, "YouTube Premium", YOUTUBE_RAW_URL)
async def combo2(u, c): await send_guide(u, "Combo Spotify & Locket", SPOTIFY_LOCKETGOLD_RAW_URL)
async def combo3(u, c): 
    note = "<i>(Lưu ý: File .conf này hoạt động tương tự Module)</i>\n"
    await send_guide(u, "Siêu Combo 3-trong-1", SPOTIFY_YOUTUBE_LOCKET_RAW_URL, note)

# --- 4. KHỞI CHẠY ---
def main():
    if not TOKEN or TOKEN == "YOUR_TOKEN_HERE": return
    app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("hdsd", hdsd))
    app.add_handler(CommandHandler("locket", locket))
    app.add_handler(CommandHandler("spotify", spotify))
    app.add_handler(CommandHandler("youtube", youtube))
    app.add_handler(CommandHandler("spotify_locketgold", combo2))
    app.add_handler(CommandHandler("spotify_youtube_locket", combo3))
    app.add_handler(CommandHandler("broadcast", broadcast))
    
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
