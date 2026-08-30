import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"{bot.user.name} olarak giriş yapıldı! Bot aktif.")

@bot.command()
async def selam(ctx):
    await ctx.send(f"Aleykümselam {ctx.author.mention}! 🚀")

@bot.command()
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f"Pong! 🏓 Gecikme süresi: **{latency}ms**")

@bot.command()
async def id(ctx, user_id: int):
    try:
        # Sunucuda olmasa bile ID ile kullanıcıyı Discord API'sinden çekiyoruz
        kullanici = await bot.fetch_user(user_id)
        
        # Hesap açılış tarihini Discord ID'sinden hesaplıyoruz
        kurulus_tarihi = kullanici.created_at.strftime("%d.%m.%Y %H:%M:%S")
        
        # Bilgileri şık bir Embed (kutulu mesaj) içinde hazırlıyoruz
        embed = discord.Embed(
            title="🔍 Kullanıcı Bilgi Sistemi",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=kullanici.avatar.url if kullanici.avatar else kullanici.default_avatar.url)
        embed.add_field(name="Kullanıcı Adı", value=f"{kullanici} (`{kullanici.id}`)", inline=False)
        embed.add_field(name="Discord'a Başlama Tarihi", value=kurulus_tarihi, inline=False)
        embed.add_field(name="Bot mu?", value="Evet" if kullanici.bot else "Hayır", inline=True)
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f"❌ Böyle bir kullanıcı bulunamadı veya ID yanlış girildi! Hata: `{e}`")

bot.run(os.getenv("DISCORD_TOKEN"))
