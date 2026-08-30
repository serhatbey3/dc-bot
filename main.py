import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Basit bir hafıza tabanlı veri tabanı (Sözlükler)
# Gerçek projede veriler silinmesin diye json/sqlite kullanılır ama şimdilik anında çalışır!
bakiye_sistemi = {} 

# Senin Admin ID'n
ADMIN_ID = 991497628921634927

@bot.event
async def on_ready():
    print(f"{bot.user.name} olarak giriş yapıldı! Bot aktif.")

@bot.command()
async def kayit(ctx):
    user_id = str(ctx.author.id)
    if user_id in bakiye_sistemi:
        await ctx.send(f"⚠️ {ctx.author.mention}, zaten sistemde bir hesabın var kanka!")
    else:
        bakiye_sistemi[user_id] = {"para": 500, "isim": ctx.author.name}
        await ctx.send(f"🎉 Kayıt başarılı {ctx.author.mention}! Hesabına başlangıç hediyesi olarak **500 Para** yüklendi. `!cuzdan` yazarak bakiyeni görebilirsin.")

@bot.command(aliases=["cuzdan", "bakiye"])
async def profil(ctx):
    user_id = str(ctx.author.id)
    if user_id not in bakiye_sistemi:
        await ctx.send(f"❌ Henüz kayıt olmamışsın kanka! Kayıt olmak için `!kayit` yazmalısın.")
        return
    
    para = bakiye_sistemi[user_id]["para"]
    
    embed = discord.Embed(title=f"💼 {ctx.author.name} - Profil & Cüzdan", color=discord.Color.gold())
    embed.add_field(name="💰 Nakit Para", value=f"**{para}** Para", inline=True)
    embed.add_field(name="👑 Yetki Seviyesi", value="Sunucu Üyesi" if ctx.author.id != ADMIN_ID else "Sistem Kurucusu (Admin)", inline=True)
    embed.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def gonder(ctx, miktar: int, hedef: discord.Member):
    sender_id = str(ctx.author.id)
    target_id = str(hedef.id)

    if sender_id not in bakiye_sistemi:
        await ctx.send("❌ Önce `!kayit` komutuyla hesap oluşturmalısın kanka!")
        return
    
    if target_id not in bakiye_sistemi:
        await ctx.send(f"❌ {hedef.mention} isimli kullanıcının henüz sistemde hesabı yok!")
        return

    if miktar <= 0:
        await ctx.send("⚠️ Gönderilecek miktar 0'dan büyük olmalı kanka.")
        return

    if bakiye_sistemi[sender_id]["para"] < miktar:
        await ctx.send("❌ Cüzdanında o kadar para yok kanka!")
        return

    # Para transferi gerçekleşiyor
    bakiye_sistemi[sender_id]["para"] -= miktar
    bakiye_sistemi[target_id]["para"] += miktar

    await ctx.send(f"✅ Başarıyla {hedef.mention} kişisine **{miktar} Para** gönderdin kanka!")

# ================= 👑 SADECE SANA ÖZEL YÖNETİCİ PANELİ ================= #

@bot.command()
async def adminpanel(ctx):
    if ctx.author.id != ADMIN_ID:
        await ctx.send("🚨 Heyy! Bu komut sadece sistemin kurucusuna (Serhat'a) özel kanka, yetkin yok! 😎")
        return

    embed = discord.Embed(title="⚙️ SİSTEM YÖNETİCİ PANELİ", description="Hoş geldin patron! Sadece senin erişebildiğin özel komutlar:", color=discord.Color.red())
    embed.add_field(name="💰 Para Basma (Dağıtma)", value="`!admin_paraver @kullanici miktar`", inline=False)
    embed.add_field(name="💸 Para Silme / Çekme", value="`!admin_parasil @kullanici miktar`", inline=False)
    embed.add_field(name="👥 Toplam Üye Durumu", value="`!admin_istatistik`", inline=False)
    embed.set_footer(text="Bu panel gizlidir ve güvenlidir.")
    await ctx.send(embed=embed)

@bot.command()
async def admin_paraver(ctx, hedef: discord.Member, miktar: int):
    if ctx.author.id != ADMIN_ID:
        return
    
    target_id = str(hedef.id)
    if target_id not in bakiye_sistemi:
        bakiye_sistemi[target_id] = {"para": 0, "isim": hedef.name}
    
    bakiye_sistemi[target_id]["para"] += miktar
    await ctx.send(f"👑 [ADMİN] {hedef.mention} hesabına **{miktar} Para** eklendi patron!")

@bot.command()
async def admin_parasil(ctx, hedef: discord.Member, miktar: int):
    if ctx.author.id != ADMIN_ID:
        return
    
    target_id = str(hedef.id)
    if target_id in bakiye_sistemi:
        bakiye_sistemi[target_id]["para"] = max(0, bakiye_sistemi[target_id]["para"] - miktar)
        await ctx.send(f"👑 [ADMİN] {hedef.mention} hesabından **{miktar} Para** silindi patron!")
    else:
        await ctx.send("❌ Bu kullanıcının zaten hesabı yok.")

@bot.command()
async def admin_istatistik(ctx):
    if ctx.author.id != ADMIN_ID:
        return
    
    toplam_oyuncu = len(bakiye_sistemi)
    toplam_servet = sum(data["para"] for data in bakiye_sistemi.values())
    
    embed = discord.Embed(title="📊 Bot Ekonomi İstatistikleri", color=discord.Color.purple())
    embed.add_field(name="Kayıtlı Oyuncu Sayısı", value=toplam_oyuncu, inline=True)
    embed.add_field(name="Sistemdeki Toplam Para", value=toplam_servet, inline=True)
    await ctx.send(embed=embed)

# ======================================================================

bot.run(os.getenv("DISCORD_TOKEN"))
