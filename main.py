import os
import random
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Hafıza tabanlı ekonomi ve süre takip sözlükleri
bakiye_sistemi = {} 
gunluk_cooldown = {}

# Senin Admin ID'n
ADMIN_ID = 991497628921634927

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
        kullanici = await bot.fetch_user(user_id)
        kurulus_tarihi = kullanici.created_at.strftime("%d.%m.%Y %H:%M:%S")
        
        embed = discord.Embed(title="🔍 Kullanıcı Bilgi Sistemi", color=discord.Color.blue())
        embed.set_thumbnail(url=kullanici.avatar.url if kullanici.avatar else kullanici.default_avatar.url)
        embed.add_field(name="Kullanıcı Adı", value=f"{kullanici} (`{kullanici.id}`)", inline=False)
        embed.add_field(name="Discord'a Başlama Tarihi", value=kurulus_tarihi, inline=False)
        embed.add_field(name="Bot mu?", value="Evet" if kullanici.bot else "Hayır", inline=True)
        
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(f"❌ Kullanıcı bulunamadı veya ID hatalı! Hata: `{e}`")

@bot.command()
async def sil(ctx, miktar: int):
    if not ctx.author.guild_permissions.manage_messages:
        await ctx.send("❌ Bu komut için **Mesajları Yönet** yetkin olmalı kanka!")
        return

    if miktar <= 0:
        await ctx.send("⚠️ Lütfen 0'dan büyük bir sayı gir kanka!")
        return

    try:
        silinen = await ctx.channel.purge(limit=miktar + 1)
        bilgi = await ctx.send(f"🧹 Başarıyla **{len(silinen) - 1}** adet mesaj silindi kanka!")
        await bilgi.delete(delay=3)
    except Exception as e:
        await ctx.send(f"❌ Hata oluştu: `{e}`")

@bot.command()
async def kayit(ctx):
    user_id = str(ctx.author.id)
    if user_id in bakiye_sistemi:
        await ctx.send(f"⚠️ {ctx.author.mention}, zaten sistemde bir hesabın var kanka!")
    else:
        bakiye_sistemi[user_id] = {"para": 500, "isim": ctx.author.name}
        await ctx.send(f"🎉 Kayıt başarılı {ctx.author.mention}! Hesabına başlangıç hediyesi **500 Para** yüklendi. `!cuzdan` yazarak bakiyeni görebilirsin.")

@bot.command(aliases=["cuzdan", "bakiye"])
async def profil(ctx):
    user_id = str(ctx.author.id)
    if user_id not in bakiye_sistemi:
        await ctx.send(f"❌ Henüz kayıt olmamışsın kanka! `!kayit` yazmalısın.")
        return
    
    para = bakiye_sistemi[user_id]["para"]
    embed = discord.Embed(title=f"💼 {ctx.author.name} - Cüzdan", color=discord.Color.gold())
    embed.add_field(name="💰 Nakit Para", value=f"**{para}** Para", inline=True)
    embed.add_field(name="👑 Yetki", value="Üye" if ctx.author.id != ADMIN_ID else "Sistem Kurucusu", inline=True)
    embed.set_thumbnail(url=ctx.author.avatar.url if ctx.author.avatar else ctx.author.default_avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def gonder(ctx, miktar: int, hedef: discord.Member):
    sender_id = str(ctx.author.id)
    target_id = str(hedef.id)

    if sender_id not in bakiye_sistemi:
        await ctx.send("❌ Önce `!kayit` olmalısın kanka!")
        return
    if target_id not in bakiye_sistemi:
        await ctx.send(f"❌ {hedef.mention} isimli kişinin sistemde hesabı yok!")
        return
    if miktar <= 0 or bakiye_sistemi[sender_id]["para"] < miktar:
        await ctx.send("❌ Yetersiz bakiye veya geçersiz miktar!")
        return

    bakiye_sistemi[sender_id]["para"] -= miktar
    bakiye_sistemi[target_id]["para"] += miktar
    await ctx.send(f"✅ Başarıyla {hedef.mention} kişisine **{miktar} Para** gönderdin kanka!")

# ================= 🎮 OWO TARZI OYUN SİSTEMLERİ ================= #

@bot.command()
async def gunluk(ctx):
    user_id = str(ctx.author.id)
    if user_id not in bakiye_sistemi:
        await ctx.send("❌ Önce `!kayit` olmalısın kanka!")
        return
    
    # Basit bir günlük ödül simülasyonu (Herkes alabilir)
    odul = 1000
    bakiye_sistemi[user_id]["para"] += odul
    await ctx.send(f"🎁 Günlük ödülün toplandı {ctx.author.mention}! Cüzdanına **{odul} Para** eklendi.")

@bot.command()
async def yazitura(ctx, miktar: int, secim: str):
    user_id = str(ctx.author.id)
    if user_id not in bakiye_sistemi:
        await ctx.send("❌ Önce `!kayit` olmalısın kanka!")
        return
    
    secim = secim.lower()
    if secim not in ["yazi", "tura"]:
        await ctx.send("⚠️ Seçimini `yazi` veya `tura` olarak yapmalısın kanka!")
        return
    
    if miktar <= 0 or bakiye_sistemi[user_id]["para"] < miktar:
        await ctx.send("❌ Geçersiz miktar veya yetersiz bakiye!")
        return

    sonuc = random.choice(["yazi", "tura"])
    
    if secim == sonuc:
        bakiye_sistemi[user_id]["para"] += miktar
        await ctx.send(f"🎉 Para **{sonuc.upper()}** geldi! Kazandın ve cüzdanına **+{miktar} Para** eklendi kanka!")
    else:
        bakiye_sistemi[user_id]["para"] -= miktar
        await ctx.send(f"😢 Para **{sonuc.upper()}** geldi, kaybettin! Cüzdanından **-{miktar} Para** gitti.")

@bot.command()
async def avlan(ctx):
    user_id = str(ctx.author.id)
    if user_id not in bakiye_sistemi:
        await ctx.send("❌ Önce `!kayit` olmalısın kanka!")
        return
    
    bulunan_para = random.randint(50, 300)
    bakiye_sistemi[user_id]["para"] += bulunan_para
    
    canavarlar = ["Vahşi Ejderha 🐉", "Zombi 🧟", "Uzaylı 👽", "Kocaayak 🦍"]
    av = random.choice(canavarlar)
    
    await ctx.send(f"🏹 Ormanda **{av}** ile karşılaştın ve yendin! Ödül olarak cüzdanına **+{bulunan_para} Para** düştü kanka!")

@bot.command()
async def slots(ctx, miktar: int):
    user_id = str(ctx.author.id)
    if user_id not in bakiye_sistemi:
        await ctx.send("❌ Önce `!kayit` olmalısın kanka!")
        return
    
    if miktar <= 0 or bakiye_sistemi[user_id]["para"] < miktar:
        await ctx.send("❌ Geçersiz miktar veya yetersiz bakiye!")
        return

    semboller = ["🍒", "🍋", "🍊", "🍇", "💎", " 7️⃣ "]
    sonuc1 = random.choice(semboller)
    sonuc2 = random.choice(semboller)
    sonuc3 = random.choice(semboller)

    slot_goruntu = f"[ {sonuc1} | {sonuc2} | {sonuc3} ]"

    if sonuc1 == sonuc2 == sonuc3:
        kazanc = miktar * 5
        bakiye_sistemi[user_id]["para"] += kazanc
        await ctx.send(f"🎰 **SLOTS** 🎰\n{slot_goruntu}\n\n🔥 MÜKEMMEL! Üçlü tutturdun ve **+{kazanc} Para** kazandın kanka!")
    elif sonuc1 == sonuc2 or sonuc2 == sonuc3 or sonuc1 == sonuc3:
        kazanc = miktar * 2
        bakiye_sistemi[user_id]["para"] += kazanc
        await ctx.send(f"🎰 **SLOTS** 🎰\n{slot_goruntu}\n\n✨ İkili tutturdun! Cüzdanına **+{kazanc} Para** eklendi kanka.")
    else:
        bakiye_sistemi[user_id]["para"] -= miktar
        await ctx.send(f"🎰 **SLOTS** 🎰\n{slot_goruntu}\n\n❌ Maalesef eşleşmedi, **-{miktar} Para** kaybettin kanka.")

# ================= ==============================================

# ================= 👑 SADECE SANA ÖZEL YÖNETİCİ PANELİ ================= #

@bot.command()
async def adminpanel(ctx):
    if ctx.author.id != ADMIN_ID:
        await ctx.send("🚨 Burası sadece kurucuya (Serhat'a) özel kanka, yetkin yok! 😎")
        return

    embed = discord.Embed(title="⚙️ SİSTEM YÖNETİCİ PANELİ", color=discord.Color.red())
    embed.add_field(name="💰 Para Ver", value="`!admin_paraver @kullanici miktar`", inline=False)
    embed.add_field(name="💸 Para Sil", value="`!admin_parasil @kullanici miktar`", inline=False)
    embed.add_field(name="📊 İstatistik", value="`!admin_istatistik`", inline=False)
    await ctx.send(embed=embed)

@bot.command()
async def admin_paraver(ctx, hedef: discord.Member, miktar: int):
    if ctx.author.id != ADMIN_ID: return
    target_id = str(hedef.id)
    if target_id not in bakiye_sistemi:
        bakiye_sistemi[target_id] = {"para": 0, "isim": hedef.name}
    bakiye_sistemi[target_id]["para"] += miktar
    await ctx.send(f"👑 [ADMİN] {hedef.mention} hesabına **{miktar} Para** eklendi patron!")

@bot.command()
async def admin_parasil(ctx, hedef: discord.Member, miktar: int):
    if ctx.author.id != ADMIN_ID: return
    target_id = str(hedef.id)
    if target_id in bakiye_sistemi:
        bakiye_sistemi[target_id]["para"] = max(0, bakiye_sistemi[target_id]["para"] - miktar)
        await ctx.send(f"👑 [ADMİN] {hedef.mention} hesabından **{miktar} Para** silindi patron!")

@bot.command()
async def admin_istatistik(ctx):
    if ctx.author.id != ADMIN_ID: return
    toplam_oyuncu = len(bakiye_sistemi)
    toplam_servet = sum(data["para"] for data in bakiye_sistemi.values())
    embed = discord.Embed(title="📊 Bot İstatistikleri", color=discord.Color.purple())
    embed.add_field(name="Kayıtlı Oyuncu", value=toplam_oyuncu, inline=True)
    embed.add_field(name="Toplam Servet", value=toplam_servet, inline=True)
    await ctx.send(embed=embed)

# ======================================================================

@bot.command()
async def dm_yaz(ctx, *, mesaj: str):
    if ctx.author.id != ADMIN_ID:
        await ctx.send("🚨 Bu komut sadece kurucuya (sana) özel kanka!")
        return

    basarili = 0
    basarisiz = 0

    await ctx.send("🚀 Duyuru mesajları üyelerin DM kutularına gönderilmeye başlandı...")

    for uye in ctx.guild.members:
        if uye.bot:
            continue
        try:
            await uye.send(f"📢 **Duyuru ({ctx.guild.name})**:\n\n{mesaj}")
            basarili += 1
        except Exception:
            basarisiz += 1

    await ctx.send(f"✅ Duyuru tamamlandı!\n📨 Gönderilen: **{basarili}**\n❌ Ulaşılamayan: **{basarisiz}**")

import asyncio
from datetime import datetime, timedelta

# Silinen mesajları saklamak için sözlük (mesaj_id: veri)
silinen_mesajlar_hafizasi = {}

@bot.event
async def on_message_delete(message):
    if message.author.bot:
        return
    
    # Mesaj bilgilerini hafızaya alıyoruz
    mesaj_verisi = {
        "yazan": message.author,
        icerik: message.content,
        "kanal": message.channel,
        "zaman": datetime.now()
    }
    silinen_mesajlar_hafizasi[message.id] = mesaj_verisi

    # 10 dakika (600 saniye) boyunca hafızada tut, sonra sil
    await asyncio.sleep(600)
    silinen_mesajlar_hafizasi.pop(message.id, None)

@bot.command()
async def snipe(ctx):
    # Son 10 dakika içinde bu kanalda silinmiş mesaj var mı diye bakıyoruz
    kanal_silinenleri = [
        veri for veri in silinen_mesajlar_hafizasi.values() 
        if veri["kanal"].id == ctx.channel.id and datetime.now() - veri["zaman"] <= timedelta(minutes=10)
    ]

    if not kanal_silinenleri:
        await ctx.send("❌ Bu kanalda son 10 dakika içinde silinen bir mesaj bulunamadı kanka!")
        return

    # En son silinen mesajı al
    en_son = kanal_silinenleri[-1]
    
    embed = discord.Embed(title="👻 Son Silinen Mesaj (Snipe)", color=discord.Color.orange())
    embed.add_field(name="Yazan Kişi", value=en_son["yazan"].mention, inline=False)
    embed.add_field(name="Silinen Mesaj", value=en_son["icerik"] if en_son["icerik"] else "*İçerik yok (Fotoğraf veya boş mesaj)*", inline=False)
    embed.set_footer(text=f"Silinme üzerinden 10 dakika geçmeden yakalandı.")
    
    await ctx.send(embed=embed)

bot.run(os.getenv("DISCORD_TOKEN"))
