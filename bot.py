import discord
from discord.ext import commands
import random
import os

TOKEN = os.environ.get("TOKEN")

GUILD_ID = 1465477542919016625
CALL_CHANNEL_ID = 1465657430292697151  # ✅┃escolha-e-pagamentos
ENTREGADOR_ROLE_NAME = "Entregador"

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print("Call Ticket Bot online!")

@bot.event
async def on_interaction(interaction: discord.Interaction):
    # só slash commands
    if interaction.type != discord.InteractionType.application_command:
        return

    # só quando o nome do comando for "call"
    if interaction.data.get("name") != "call":
        return

    # só no canal correto
    if interaction.channel_id != CALL_CHANNEL_ID:
        return

    guild = bot.get_guild(GUILD_ID)
    member = interaction.user

    role = discord.utils.get(guild.roles, name=ENTREGADOR_ROLE_NAME)
    entregadores = [m for m in guild.members if role in m.roles and not m.bot]

    if not entregadores:
        await interaction.response.send_message(
            "❌ Nenhum entregador disponível no momento.",
            ephemeral=True
        )
        return

    entregador = random.choice(entregadores)

    # cria o canal privado
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        member: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        entregador: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        guild.me: discord.PermissionOverwrite(view_channel=True)
    }

    channel = await guild.create_text_channel(
        name=f"ticket-{member.name}".lower(),
        overwrites=overwrites
    )

    await interaction.response.send_message(
        "✅ Veja os chats",
        ephemeral=True
    )

    await channel.send(
        f"🎟️ **Ticket aberto**\n\n"
        f"👤 Cliente: {member.mention}\n"
        f"📦 Entregador: {entregador.mention}\n\n"
        f"Conversem aqui."
    )

bot.run(TOKEN)
