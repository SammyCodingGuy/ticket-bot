import discord
from discord.ext import commands

# Configuration
TOKEN = 'YOUR_BOT_TOKEN'  # Replace with your bot's token
GUILD_ID = YOUR_GUILD_ID  # Replace with your server's ID
CATEGORY_ID = YOUR_CATEGORY_ID  # Replace with the category ID for tickets
SUPPORT_ROLE_ID = YOUR_SUPPORT_ROLE_ID  # Replace with the ID of the support role
TICKET_PREFIX = 'ticket-'  # Prefix for ticket channel names

# Initialize bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Bot ready event
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    if GUILD_ID:
        guild = bot.get_guild(GUILD_ID)
        if guild:
            print(f'Connected to server: {guild.name}')
    await bot.change_presence(activity=discord.Game(name="!ticket for help"))

# Command to create a ticket
@bot.command(name='ticket')
async def ticket(ctx):
    guild = bot.get_guild(GUILD_ID)
    if not guild:
        await ctx.send("I am not connected to a server.")
        return

    category = guild.get_channel(CATEGORY_ID)
    if not category or not isinstance(category, discord.CategoryChannel):
        await ctx.send("Ticket category not found or invalid.")
        return

    # Check if user already has an open ticket
    for channel in category.channels:
        if channel.name.startswith(TICKET_PREFIX) and str(ctx.author.id) in channel.name:
            await ctx.send("You already have an open ticket.")
            return

    # Create ticket channel
    ticket_channel = await guild.create_text_channel(
        f'{TICKET_PREFIX}{ctx.author.name}-{ctx.author.discriminator}',
        category=category,
        overwrites={
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.author: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.get_role(SUPPORT_ROLE_ID): discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }
    )

    await ticket_channel.send(f'{ctx.author.mention}, Your ticket has been created! Please describe what your applying for and someone will take this ticket.')
    await ctx.send(f'Your ticket has been created: {ticket_channel.mention}')

# Command to close a ticket
@bot.command(name='close')
async def close(ctx):
    if not ctx.channel.name.startswith(TICKET_PREFIX):
        await ctx.send("This command can only be used in a ticket channel.")
        return

    await ctx.channel.delete()
    print(f'Ticket closed: {ctx.channel.name}')

# Run the bot
bot.run(TOKEN)
