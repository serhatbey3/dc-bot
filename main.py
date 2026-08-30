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

bot.run(os.getenv("DISCORD_TOKEN"))
