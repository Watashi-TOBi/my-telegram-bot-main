import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ChatType

from config import SUPPORT_URL, OWNER_URL, SOURCE_URL

_ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
_BANNER = os.path.join(_ASSETS_DIR, "start_banner.jpg")


def _build_keyboard(bot_username: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(
            "📤 ADD ME TO YOUR GROUP",
            url=f"https://t.me/{bot_username}?startgroup=true",
        )],
        [
            InlineKeyboardButton("💫 Support", url=SUPPORT_URL),
            InlineKeyboardButton("▶️ Owner",   url=OWNER_URL),
        ],
        [
            InlineKeyboardButton("❓ Help", callback_data="show_help"),
            InlineKeyboardButton("🔗 Join", url="https://t.me/Graveyard_of_S0UL"),
        ],
    ])


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    bot  = context.bot
    chat = update.effective_chat

    # ── Group: quick inline message, no banner ────────────────────────────────
    if chat.type in (ChatType.GROUP, ChatType.SUPERGROUP):
        await update.message.reply_text(
            f"👋 Hey <b>{user.first_name}</b>!\n\n"
            f"I'm <b>{bot.first_name}</b> 🖤 — your group's all-in-one bot.\n\n"
            f"⚙️ Moderation  •  💰 Economy  •  🎭 Mafia  •  🎮 Games\n"
            f"🔫 Duels  •  🏪 Shop  •  🤖 AI Chat  •  and more!\n\n"
            f"Use /help to see every command.",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("❓ Help", callback_data="show_help"),
                InlineKeyboardButton("🔗 Community", url="https://t.me/Graveyard_of_S0UL"),
            ]]),
        )
        return

    # ── DM: full banner welcome ───────────────────────────────────────────────
    caption = (
        f"👋 Hey, <b>{user.first_name}</b> 🐻\n\n"
        f"<i>\"Your group's guardian\"</i>\n\n"
        f"🖤 I'm <b>{bot.first_name}</b> — a versatile Telegram management bot "
        f"built to help you take full control of your groups with ease.\n\n"
        f"💎 <b>What I Can Do:</b>\n\n"
        f"• 🛡️  Powerful group moderation\n"
        f"• 💰  Full economy system — coins, shop, duels\n"
        f"• 🎭  Mafia party game with roles & voting\n"
        f"• 🎮  Betting games — football, slots, darts & more\n"
        f"• 🤖  AI chat — just mention me or DM me\n"
        f"• ✨  Truth/Dare, Love Calculator, @all tag & more\n\n"
        f"⭐ <b>Need Help?</b>\n"
        f"Hit the Help button below for all commands."
    )

    keyboard = _build_keyboard(bot.username)

    try:
        with open(_BANNER, "rb") as photo:
            await update.message.reply_photo(
                photo=photo,
                caption=caption,
                parse_mode="HTML",
                reply_markup=keyboard,
            )
    except FileNotFoundError:
        await update.message.reply_text(
            caption,
            parse_mode="HTML",
            reply_markup=keyboard,
        )


async def commands_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    commands_text = (
        "📋 <b>Quick Command Reference</b>\n\n"
        "🎭 <b>Mafia Game</b>\n"
        "• /startgame /join /flee /startmafia\n"
        "• /players /skip /endgame /stats /gamerules\n\n"
        "⚙️ <b>Moderation</b>\n"
        "• /ban /kick /tban /mute /unmute /tmute\n"
        "• /warn /unwarn /warns /resetwarns\n"
        "• /promote /demote /purge /pin /unpin\n"
        "• /lock /unlock /locks\n\n"
        "💰 <b>Economy</b>\n"
        "• /bal /daily /weekly /monthly\n"
        "• /kill /rob /duel /shop /leaderboard\n\n"
        "🎮 <b>Games</b>\n"
        "• /bet /football /basket /bowling /dart /slot\n\n"
        "🎉 <b>Fun</b>\n"
        "• /love /crush /truth /dare /tagall\n"
        "• /hug /kiss /slap /pat /poke /punch\n\n"
        "🤖 <b>AI Chat</b>\n"
        "• DM me · @mention me · reply to my message\n\n"
        "📖 Use /help for the full detailed guide!"
    )

    await query.edit_message_caption(
        caption=commands_text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back", callback_data="show_start")],
        ]),
    )


async def back_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if not query.message.photo:
        await query.message.delete()
        return

    user = query.from_user
    bot  = context.bot

    caption = (
        f"👋 Hey, <b>{user.first_name}</b> 🐻\n\n"
        f"<i>\"Your group's guardian\"</i>\n\n"
        f"🖤 I'm <b>{bot.first_name}</b> — a versatile Telegram management bot "
        f"built to help you take full control of your groups with ease.\n\n"
        f"💎 <b>What I Can Do:</b>\n\n"
        f"• 🛡️  Powerful group moderation\n"
        f"• 💰  Full economy system — coins, shop, duels\n"
        f"• 🎭  Mafia party game with roles & voting\n"
        f"• 🎮  Betting games — football, slots, darts & more\n"
        f"• 🤖  AI chat — just mention me or DM me\n"
        f"• ✨  Truth/Dare, Love Calculator, @all tag & more\n\n"
        f"⭐ <b>Need Help?</b>\n"
        f"Hit the Help button below for all commands."
    )

    await query.edit_message_caption(
        caption=caption,
        parse_mode="HTML",
        reply_markup=_build_keyboard(bot.username),
    )
