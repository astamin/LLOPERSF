import discord
from discord.ext import commands 
from discord.commands import application_command
import requests , httpx , uuid
import os
token =input('Enter Token : ')
from datetime import datetime

bot = commands.Bot(command_prefix='/')

@bot.application_command(name="start" , description="Start program")
async def start(ctx:discord.Interaction):
    await ctx.response.send_message("BOT IS STARTING AZBI !")

bot.run(token=token)
 
