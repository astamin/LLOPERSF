try : 
    import discord
    import os
    import asyncio
    from discord.ext import commands
    from dotenv import load_dotenv
except :
    import os
    os.system('pip install -r requirements.txt')
    import discord
    import os
    import asyncio
    from discord.ext import commands
    from dotenv import load_dotenv
load_dotenv()
TOKEN = input('Enter Token : ')
class MyHelpCommand(commands.DefaultHelpCommand):
    async def send_bot_help(self, mapping):
        pass
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all() , help_command=MyHelpCommand())
async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') :
            cog_name = filename[:-3]
            try:
                await bot.load_extension(f'cogs.{cog_name}')
                print(f'Loaded {cog_name} cog')
            except Exception as e:
                print(f'Failed to load {cog_name} cog. Error: {e}')

@bot.event
async def on_ready():
    print("BOT IS ONLINE NOW {}".format(bot.user.display_name))
def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(load())
    loop.run_until_complete(bot.run(TOKEN))

main()
