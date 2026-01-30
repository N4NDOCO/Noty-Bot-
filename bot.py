import discord
from discord.ext import commands
import random
from config import (
    TOKEN,
    GUILD_ID,
    CALL_CHANNEL_ID,
    ROLE_ENTREGADOR_NAME,
    CATEGORY_NAME
)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print("Call Listener Bot online!")

@bot.event
async def on_message(message):

    if message.author.bot:
        return

    if message.content.strip().lower() != "/call":
        return

    if message.channel.id != CALL_CHANNEL_ID:
        return

    guild = message.guild
    user = message.author

    role = discord.utils.get(guild.roles, name=ROLE_ENTREGADOR_NAME)
    if not role:
        await message.channel.send("❌ Cargo Entregador não encontrado.")
        return

    entregadores = [
        m for m in guild.members
        if role in m.roles and not m.bot
    ]

    if not entregadores:
        await message.channel.send("❌ Nenhum entregador disponível.")
        return

    entregador = random.choice(entregadores)

    category = discord.utils.get(guild.categories, name=CATEGORY_NAME)
    if not category:
        category = await guild.create_category(CATEGORY_NAME)

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        entregador: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True),
    }

    channel = await guild.create_text_channel(
        name=f"ticket-{user.name}",
        category=category,
        overwrites=overwrites
    )

    await channel.send(
        f"👋 {user.mention} | {entregador.mention}\n"
        "**Chat privado aberto.**"
    )

bot.run(TOKEN)
