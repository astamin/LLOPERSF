import discord
from discord.ext import commands, tasks
import psutil
import asyncio

class BotStatusCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.status_message = None
        self.status_update.start()

    def cog_unload(self):
        self.status_update.cancel()

    async def send_status_message(self, channel):
        cpu_percent = psutil.cpu_percent()
        cpu_count = psutil.cpu_count()

        virtual_memory = psutil.virtual_memory()
        swap_memory = psutil.swap_memory()

        disk_usage = psutil.disk_usage('/')

        bot_latency = round(self.bot.latency * 1000, 2)  # Bot latency in milliseconds

        servers_count = len(self.bot.guilds)  # Number of servers the bot is in

        status_content = (
            f"```\n"
            f"CPU Usage: {cpu_percent}%\n"
            f"CPU Count: {cpu_count}\n\n"
            f"Virtual Memory: {virtual_memory.percent}%\n"
            f"Swap Memory: {swap_memory.percent}%\n\n"
            f"Disk Usage: {disk_usage.percent}%\n\n"
            f"Bot Latency: {bot_latency} ms\n"
            f"Servers Count: {servers_count}\n"
            f"```"
        )

        self.status_message = await channel.send(status_content)

    @tasks.loop(seconds=1)
    async def status_update(self):
        if self.status_message:
            cpu_percent = psutil.cpu_percent()
            cpu_count = psutil.cpu_count()

            virtual_memory = psutil.virtual_memory()
            swap_memory = psutil.swap_memory()

            disk_usage = psutil.disk_usage('/')

            bot_latency = round(self.bot.latency * 1000, 2)  # Bot latency in milliseconds

            servers_count = len(self.bot.guilds)  # Number of servers the bot is in

            status_content = (
                f"```\n"
                f"CPU Usage: {cpu_percent}%\n"
                f"CPU Count: {cpu_count}\n\n"
                f"Virtual Memory: {virtual_memory.percent}%\n"
                f"Swap Memory: {swap_memory.percent}%\n\n"
                f"Disk Usage: {disk_usage.percent}%\n\n"
                f"Bot Latency: {bot_latency} ms\n"
                f"Servers Count: {servers_count}\n"
                f"```"
            )

            await self.status_message.edit(content=status_content)

    @status_update.before_loop
    async def before_status_update(self):
        await self.bot.wait_until_ready()

    @commands.command(name='stats')
    async def show_stats(self, ctx):
        await self.send_status_message(ctx.channel)

def setup(bot):
    bot.add_cog(BotStatusCog(bot))
