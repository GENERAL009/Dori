import os
import asyncio
import logging
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters,
    ContextTypes,
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy import select, and_, text

from db import engine, AsyncSessionLocal
from models import Base, TelegramUser, TelegramRole, SentReminder

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8838868114:AAEZ2FMxmgfOBkMh3PSStRjFdMHYbBr8bu8")

PHONE, ROLE = range(2)

TZ = ZoneInfo("Asia/Tashkent")


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_or_create_user(telegram_id: int, first_name: str = None, last_name: str = None, username: str = None):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(TelegramUser).where(TelegramUser.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()
        if not user:
            user = TelegramUser(
                telegram_id=telegram_id,
                first_name=first_name,
                last_name=last_name,
                username=username,
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
        return user


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    tg_user = await get_or_create_user(user.id, user.first_name, user.last_name, user.username)

    if tg_user.phone and tg_user.role:
        await update.message.reply_text(
            f"Salom, {user.first_name}! 👋\n"
            f"Siz allaqachon ro'yxatdan o'tgansiz.\n"
            f"📱 Raqam: {tg_user.phone}\n"
            f"👤 Rol: {_role_label(tg_user.role)}\n\n"
            f"Dori eslatmalari avtomatik yuboriladi.\n"
            f"Qayta sozlash uchun /reset buyrug'ini yuboring.",
            reply_markup=ReplyKeyboardRemove(),
        )
        return ConversationHandler.END

    contact_button = KeyboardButton("📱 Raqamni yuborish", request_contact=True)
    reply_markup = ReplyKeyboardMarkup([[contact_button]], one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text(
        f"Salom, {user.first_name}! 👋\n\n"
        "🏥 *Dori — Oilaviy Dori Tracker* botiga xush kelibsiz!\n\n"
        "Ro'yxatdan o'tish uchun telefon raqamingizni yuboring:",
        reply_markup=reply_markup,
        parse_mode="Markdown",
    )
    return PHONE


async def receive_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    if not contact:
        await update.message.reply_text("Iltimos, telefon raqamingizni yuboring (tugmani bosing).")
        return PHONE

    phone = contact.phone_number
    telegram_id = update.effective_user.id

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(TelegramUser).where(TelegramUser.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()
        if user:
            user.phone = phone
            user.first_name = contact.first_name
            user.last_name = contact.last_name
            await session.commit()

    context.user_data["phone"] = phone

    role_keyboard = ReplyKeyboardMarkup(
        [["👨 Erkak", "👩 Ayol"], ["👨‍👩‍👧 Ota-Ona"]],
        one_time_keyboard=True,
        resize_keyboard=True,
    )

    await update.message.reply_text(
        f"✅ Raqam qabul qilindi: {phone}\n\n"
        "Endi rolingizni tanlang:\n"
        "• 👨 *Erkak* — faqat erkak dorilari haqida eslatma\n"
        "• 👩 *Ayol* — faqat ayol dorilari haqida eslatma\n"
        "• 👨‍👩‍👧 *Ota-Ona* — barcha dorilar haqida eslatma",
        reply_markup=role_keyboard,
        parse_mode="Markdown",
    )
    return ROLE


async def receive_role(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_msg = update.message.text
    telegram_id = update.effective_user.id

    role_map = {
        "👨 Erkak": TelegramRole.MALE,
        "👩 Ayol": TelegramRole.FEMALE,
        "👨‍👩‍👧 Ota-Ona": TelegramRole.PARENT,
    }

    role = role_map.get(text_msg)
    if not role:
        await update.message.reply_text("Iltimos, quyidagi tugmalardan birini tanlang.")
        return ROLE

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(TelegramUser).where(TelegramUser.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()
        if user:
            user.role = role
            await session.commit()

    await update.message.reply_text(
        f"✅ Ro'yxatdan o'tish yakunlandi!\n\n"
        f"📱 Raqam: {context.user_data.get('phone', '—')}\n"
        f"👤 Rol: {_role_label(role)}\n\n"
        f"Endi dori eslatmalari avtomatik keladi 💊\n"
        f"Buyruqlar:\n"
        f"/status — bugungi dorilar\n"
        f"/reset — qayta sozlash",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(TelegramUser).where(TelegramUser.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()
        if user:
            user.phone = None
            user.role = None
            await session.commit()

    await update.message.reply_text(
        "🔄 Sozlamalar tozalandi. Qaytadan boshlash uchun /start buyrug'ini yuboring.",
        reply_markup=ReplyKeyboardRemove(),
    )
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Bekor qilindi.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


async def status_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.effective_user.id
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(TelegramUser).where(TelegramUser.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()

    if not user or not user.role:
        await update.message.reply_text("Siz hali ro'yxatdan o'tmagansiz. /start bosing.")
        return

    now = datetime.now(TZ)
    meds = await _get_today_medications(user.role)

    if not meds:
        await update.message.reply_text("Bugun dori yo'q ✅")
        return

    lines = [f"📋 *Bugungi dorilar* ({now.strftime('%d.%m.%Y')}):\n"]
    for m in meds:
        times_str = ", ".join(t[:5] for t in m["times"])
        role_prefix = ""
        if user.role == TelegramRole.PARENT:
            role_emoji = "👨" if m["user_role"] == "male" else "👩"
            role_prefix = f"{role_emoji} "
        lines.append(f"💊 {role_prefix}*{m['name']}* — {m['dosage']}\n   ⏰ {times_str}")

    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")


def _role_label(role: TelegramRole) -> str:
    labels = {
        TelegramRole.MALE: "👨 Erkak",
        TelegramRole.FEMALE: "👩 Ayol",
        TelegramRole.PARENT: "👨‍👩‍👧 Ota-Ona",
    }
    return labels.get(role, str(role))


async def _get_today_medications(role: TelegramRole) -> list[dict]:
    today = datetime.now(TZ).date()
    async with AsyncSessionLocal() as session:
        if role == TelegramRole.PARENT:
            query = text("""
                SELECT m.name, m.dosage, m.times, m.instruction, u.role as user_role
                FROM medications m
                JOIN users u ON m.user_id = u.id
                WHERE m.status = 'active'
                  AND m.start_date <= :today
                  AND (m.end_date >= :today OR m.end_date IS NULL)
                ORDER BY u.role, m.name
            """)
            result = await session.execute(query, {"today": today})
        else:
            db_role = "male" if role == TelegramRole.MALE else "female"
            query = text("""
                SELECT m.name, m.dosage, m.times, m.instruction, u.role as user_role
                FROM medications m
                JOIN users u ON m.user_id = u.id
                WHERE m.status = 'active'
                  AND m.start_date <= :today
                  AND (m.end_date >= :today OR m.end_date IS NULL)
                  AND u.role = :role
                ORDER BY m.name
            """)
            result = await session.execute(query, {"today": today, "role": db_role})

        rows = result.fetchall()
        meds = []
        for row in rows:
            times = row.times if isinstance(row.times, list) else []
            meds.append({
                "name": row.name,
                "dosage": row.dosage,
                "times": times,
                "instruction": row.instruction,
                "user_role": row.user_role,
            })
        return meds


async def _check_already_sent(session, telegram_id: int, med_name: str, time_str: str, date_str: str) -> bool:
    result = await session.execute(
        select(SentReminder).where(
            and_(
                SentReminder.telegram_id == telegram_id,
                SentReminder.medication_name == med_name,
                SentReminder.scheduled_time == time_str,
                SentReminder.sent_date == date_str,
            )
        )
    )
    return result.scalar_one_or_none() is not None


async def send_reminders(app: Application):
    now = datetime.now(TZ)
    today = now.date()
    today_str = today.isoformat()
    current_time = now.time()
    window_start = (now - timedelta(minutes=2)).time()

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(TelegramUser).where(
                and_(TelegramUser.is_active == True, TelegramUser.role.isnot(None))
            )
        )
        users = result.scalars().all()

    for user in users:
        try:
            meds = await _get_today_medications(user.role)
            if not meds:
                continue

            to_notify = []
            for med in meds:
                for t in med["times"]:
                    parts = t.split(":")
                    med_time = time(int(parts[0]), int(parts[1]))
                    if window_start <= med_time <= current_time:
                        async with AsyncSessionLocal() as session:
                            already = await _check_already_sent(
                                session, user.telegram_id, med["name"], t[:5], today_str
                            )
                        if not already:
                            to_notify.append({
                                "name": med["name"],
                                "dosage": med["dosage"],
                                "time": t[:5],
                                "instruction": med["instruction"],
                                "user_role": med["user_role"],
                            })

            if not to_notify:
                continue

            lines = ["⏰ *Dori vaqti keldi!*\n"]
            for med in to_notify:
                role_prefix = ""
                if user.role == TelegramRole.PARENT:
                    role_emoji = "👨" if med["user_role"] == "male" else "👩"
                    role_prefix = f"{role_emoji} "
                lines.append(f"💊 {role_prefix}*{med['name']}* — {med['dosage']}")
                lines.append(f"   ⏰ {med['time']}")
                if med["instruction"]:
                    lines.append(f"   📝 {med['instruction']}")
                lines.append("")

            await app.bot.send_message(
                chat_id=user.telegram_id,
                text="\n".join(lines),
                parse_mode="Markdown",
            )

            async with AsyncSessionLocal() as session:
                for med in to_notify:
                    reminder = SentReminder(
                        telegram_id=user.telegram_id,
                        medication_name=med["name"],
                        scheduled_time=med["time"],
                        sent_date=today_str,
                    )
                    session.add(reminder)
                await session.commit()

            logger.info(f"Sent {len(to_notify)} reminders to {user.telegram_id} ({user.role})")
        except Exception as e:
            logger.error(f"Failed to send reminder to {user.telegram_id}: {e}")


async def post_init(app: Application):
    await init_db()

    scheduler = AsyncIOScheduler(timezone=TZ)
    scheduler.add_job(
        send_reminders,
        IntervalTrigger(minutes=1),
        args=[app],
        id="send_telegram_reminders",
        replace_existing=True,
    )
    scheduler.start()
    logger.info("Scheduler started!")


def main():
    app = Application.builder().token(BOT_TOKEN).post_init(post_init).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            PHONE: [MessageHandler(filters.CONTACT, receive_phone)],
            ROLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_role)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(CommandHandler("status", status_cmd))

    logger.info("Dori Bot starting...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
