# randseal
Simple package that produces a seal image. The image is then output as a `discord.File` for Pycord.

### Usage example
```py
from discord.ext import seal
import discord

bot = discord.Bot(intents=discord.Intents.default())

@bot.slash_command(description="Gets a random seal image")
async def seal(ctx):
	await ctx.respond(file=seal( # You can optionally specify a number between 1 and 82 here
	))

bot.run("token")
```