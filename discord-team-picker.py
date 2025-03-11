import discord
from discord.ext import commands
import random

# Create intents and enable necessary ones
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

call_members = []  # Global list of players
last_game_mode = None  # Store last game mode

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def start_game(ctx):
    global call_members, last_game_mode
    channel_id = YOUR_VOICE_CHANNEL_ID  # Replace with your actual voice channel ID
    channel = bot.get_channel(channel_id)

    if channel and isinstance(channel, discord.VoiceChannel):
        call_members = [member.display_name for member in channel.members if member != bot.user]

        await ctx.send("Which game are we playing? Type 'ARAM' or 'Arena'.")

        def check(message):
            return message.author == ctx.author and message.content.lower() in ["aram", "arena"]

        game_choice = await bot.wait_for('message', check=check)
        last_game_mode = game_choice.content.lower()

        while True:
            await ctx.send(f"Current members: {', '.join(call_members)}")
            await ctx.send("Would you like to add or remove members? Type 'add', 'remove', or 'done'.")

            def action_check(message):
                return message.author == ctx.author and message.content.lower() in ["add", "remove", "done"]

            action_choice = await bot.wait_for('message', check=action_check)
            action_choice = action_choice.content.lower()

            if action_choice == "add":
                await ctx.send("Enter names to add (separate by spaces).")
                member_to_add = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
                members_to_add = member_to_add.content.split()

                for name in members_to_add:
                    if name not in call_members:
                        call_members.append(name)

                await ctx.send(f"Added: {', '.join(members_to_add)}")

            elif action_choice == "remove":
                if not call_members:
                    await ctx.send("No members to remove.")
                    continue

                await ctx.send(f"Current members: {', '.join(call_members)}\nEnter names to remove (separate by spaces).")
                member_to_remove = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
                members_to_remove = member_to_remove.content.split()

                removed_members = [name for name in members_to_remove if name in call_members]
                call_members = [name for name in call_members if name not in members_to_remove]

                if removed_members:
                    await ctx.send(f"Removed: {', '.join(removed_members)}")
                else:
                    await ctx.send("None of those names were in the list.")

            elif action_choice == "done":
                await ctx.send("Finalizing teams...")
                break

        await generate_teams(ctx, last_game_mode)

@bot.command()
async def rematch(ctx):
    global call_members, last_game_mode
    if not call_members or last_game_mode is None:
        await ctx.send("No previous game found. Start a new game with !start_game.")
        return

    await ctx.send("Shuffling teams for a rematch...")
    await generate_teams(ctx, last_game_mode)

async def generate_teams(ctx, game_mode):
    def split_into_teams(members, game_mode):
        random.shuffle(members)

        if game_mode == "aram":
            num_teams = max(2, len(members) // 5 + (1 if len(members) % 5 != 0 else 0))
            teams = [[] for _ in range(num_teams)]

            for i, member in enumerate(members):
                teams[i % num_teams].append(member)

            return teams

        elif game_mode == "arena":
            return [members[i:i+2] for i in range(0, len(members), 2)]

    teams = split_into_teams(call_members, game_mode)

    if game_mode == "aram":
        for idx, team in enumerate(teams, 1):
            await ctx.send(f"Team {idx}: {', '.join(team)}")
    elif game_mode == "arena":
        await ctx.send("Arena Teams:")
        for idx, team in enumerate(teams, 1):
            await ctx.send(f"Team {idx}: {', '.join(team)}")

    await ctx.send("Good luck and have fun!")

@bot.command()
async def list(ctx):
    global call_members
    if call_members:
        await ctx.send("Current members: " + ", ".join(call_members))
    else:
        await ctx.send("No members in the list.")

bot.run("YOUR_BOT_TOKEN")  # Replace with your bot token
