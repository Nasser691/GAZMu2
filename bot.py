from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# تشغيل سيرفر وهمي حتى يتجنب Render مشكلة Port Scan Timeout
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'Bot is running!')

def run_fake_web_server():
    server = HTTPServer(('0.0.0.0', 10000), SimpleHandler)
    server.serve_forever()

threading.Thread(target=run_fake_web_server).start()

# تحميل المتغيرات من ملف .env
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# أيدي الملكين الذين يمكنهم تغيير اسم وصورة البوت
KING_IDS = ["361039024288432138", "691265105878319195"]

@bot.event
async def on_ready():
    print(f'✅ Logged in as {bot.user}')

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"🎶 Joined {channel}")
    else:
        await ctx.send("❌ لازم تكون في روم صوتي")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("📤 Left the voice channel")
    else:
        await ctx.send("❌ البوت مو في أي روم صوتي")

@bot.command()
async def set_name(ctx, *, new_name: str):
    if str(ctx.author.id) in KING_IDS:
        await bot.user.edit(username=new_name)
        await ctx.send(f"✅ تم تغيير اسم البوت إلى: {new_name}")
    else:
        await ctx.send("❌ فقط الملكين يمكنهم تغيير اسم البوت")

@bot.command()
async def set_avatar(ctx):
    if str(ctx.author.id) in KING_IDS:
        await bot.user.edit(avatar=open("new_avatar.png", "rb").read())
        await ctx.send("✅ تم تغيير صورة البوت")
    else:
        await ctx.send("❌ فقط الملكين يمكنهم تغيير صورة البوت")

# تشغيل البوت باستخدام التوكن من ملف .env
bot.run(os.getenv("DISCORD_TOKEN"))
