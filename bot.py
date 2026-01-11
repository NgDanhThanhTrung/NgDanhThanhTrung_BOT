import os
import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand, ReplyKeyboardMarkup, KeyboardButton
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

# --- 1. CẤU HÌNH (CONFIG) ---
TOKEN = os.getenv('BOT_TOKEN') or "YOUR_TOKEN_HERE"
ADMIN_ID = 7346983056 
USER_LIST_FILE = "users.txt"

# URLs
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
    if not os.path.exists(USER_LIST_FILE): open(USER_LIST_FILE, "w").close()
    with open(USER_LIST_FILE, "r") as f:
        users = f.read().splitlines()
    if str(user_id) not in users:
        with open(USER_LIST_FILE, "a") as f: f.write(f"{user_id}\n")

# --- 3. GIAO DIỆN NÚT BẤM (KEYBOARDS) ---
def main_menu_keyboard():
    """Tạo bàn phím nút bấm cố định dưới thanh nhập liệu"""
    keyboard = [
        [KeyboardButton("✨ Hướng Dẫn ✨")],
        [KeyboardButton("💛 Locket Gold"), KeyboardButton("🎵 Spotify")],
        [KeyboardButton("🔴 YouTube"), KeyboardButton("💎 Combo Tất Cả")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# --- 4. HANDLERS ---
async def post_init(application):
    await application.bot.set_my_commands([
        BotCommand("start", "Khởi động"), BotCommand("hdsd", "Menu lệnh"),
        BotCommand("backup", "Backup (Admin)"), BotCommand("stats", "Thống kê (Admin)")
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    save_user(user.id)
    await update.message.reply_text(
        f"👋 Chào mừng <b>{user.first_name}</b>!\nChọn một dịch vụ bên dưới để bắt đầu.",
        reply_markup=main_menu_keyboard(), parse_mode=ParseMode.HTML
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Xử lý khi người dùng nhấn vào các nút ở bàn phím ReplyKeyboard"""
    text = update.message.text
    if text == "✨ Hướng Dẫn ✨": await hdsd(update, context)
    elif text == "💛 Locket Gold": await locket(update, context)
    elif text == "🎵 Spotify": await spotify(update, context)
    elif text == "🔴 YouTube": await youtube(update, context)
    elif text == "💎 Combo Tất Cả": await combo3(update, context)

async def hdsd(u, c):
    save_user(u.effective_user.id)
    keyboard = [[InlineKeyboardButton("✨ Web Tài Liệu", url=WEB_URL)], 
                [InlineKeyboardButton("💬 Admin", url=CONTACT_URL), InlineKeyboardButton("☕ Donate", url=DONATE_URL)]]
    await u.message.reply_text("<b>📚 MENU DỊCH VỤ:</b>\nChọn dịch vụ bạn muốn cài đặt bên dưới.", 
                              reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.HTML)

async def send_guide(update, title, url, note=""):
    keyboard = [[InlineKeyboardButton(f"🔗 Link {title}", url=url)]]
    guide_text = (
        f"✨ <b>{title.upper()}</b> ✨\n\n"
        f"1️⃣ <b>Copy URL:</b> <code>{url}</code>\n\n"
        f"2️⃣ <b>Shadowrocket:</b> Module ➔ Add Module ➔ Dán URL.\n{note}\n"
        f"3️⃣ <b>HTTPS:</b> Bật <b>HTTPS Decryption</b> và Tin cậy CA.\n\n"
        f"📥 Support: {CONTACT_URL}"
    )
    await update.message.reply_text(guide_text, parse_mode=ParseMode.HTML, reply_markup=InlineKeyboardMarkup(keyboard))

async def locket(u, c): await send_guide(u, "Locket Gold", LOCKET_RAW_URL)
async def spotify(u, c): await send_guide(u, "Spotify Premium", SPOTIFY_RAW_URL)
async def youtube(u, c): await send_guide(u, "YouTube Premium", YOUTUBE_RAW_URL)
async def combo3(u, c): await send_guide(u, "Siêu Combo 3-in-1", SPOTIFY_YOUTUBE_LOCKET_RAW_URL, "<i>(Sử dụng file .conf)</i>\n")

# --- 5. ADMIN HANDLERS ---
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    with open(USER_LIST_FILE, "r") as f: count = len(f.read().splitlines())
    await update.message.reply_text(f"📊 Tổng: <code>{count}</code> người dùng.", parse_mode=ParseMode.HTML)

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID or not context.args: return
    msg = " ".join(context.args)
    with open(USER_LIST_FILE, "r") as f: users = f.read().splitlines()
    sent = 0
    m = await update.message.reply_text(f"🚀 Đang gửi đến {len(users)} người...")
    for uid in users:
        try:
            await context.bot.send_message(chat_id=uid, text=f"📢 <b>THÔNG BÁO:</b>\n\n{msg}", parse_mode=ParseMode.HTML)
            sent += 1
            await asyncio.sleep(0.05)
        except: continue
    await m.edit_text(f"✅ Đã gửi thành công {sent} tin nhắn.")

async def backup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID:
        await update.message.reply_document(document=open(USER_LIST_FILE, 'rb'))

# --- 6. MAIN ---
def main():
    if not TOKEN or TOKEN == "YOUR_TOKEN_HERE": return
    app = ApplicationBuilder().token(TOKEN).post_init(post_init).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("hdsd", hdsd))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("backup", backup))
    app.add_handler(CommandHandler("broadcast", broadcast))
    
    # Xử lý các nút bấm văn bản từ ReplyKeyboardMarkup
    from telegram.ext import MessageHandler, filters
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__": main()
