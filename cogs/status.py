import itertools
import discord
from discord.ext import commands, tasks
from discord import app_commands

from utils.checks import tortoise_bot_developer_only
from constants import tortoise_guild_id

class StatusCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        self.statuses = [
            "/run to execute code",
        ]

        self.status_cycle = itertools.cycle(self.statuses)

    async def cog_load(self):
        self.change_status.start()

    async def cog_unload(self):
        self.change_status.cancel()


    @tasks.loop(seconds=50)
    async def change_status(self):
        if not self.statuses:
            return

        await self.bot.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(
                type=discord.ActivityType.competing,
                name=next(self.status_cycle),
                # url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            ),
        )

    @change_status.before_loop
    async def before_change_status(self):
        await self.bot.wait_until_ready()


    status_group = app_commands.Group(
        name="status",
        description="Manage bot statuses",
        guild_ids=[tortoise_guild_id]
    )

    @status_group.command(name="add", description="Add a rotating status")
    @app_commands.check(tortoise_bot_developer_only)
    async def add(self, interaction: discord.Interaction, status: str):
        self.statuses.append(status)
        self.status_cycle = itertools.cycle(self.statuses)

        await interaction.response.send_message(
            f"✅ **Status added:**\n`{status}`",
            ephemeral=True,
        )

    @status_group.command(name="remove", description="Remove a rotating status")
    @app_commands.check(tortoise_bot_developer_only)
    async def remove(self, interaction: discord.Interaction, status: str):
        if status not in self.statuses:
            await interaction.response.send_message(
                "❌ That status does not exist.",
                ephemeral=True,
            )
            return

        self.statuses.remove(status)
        self.status_cycle = itertools.cycle(self.statuses)

        await interaction.response.send_message(
            f"🗑️ **Status removed:**\n`{status}`",
            ephemeral=True,
        )

    @status_group.command(name="list", description="List all rotating statuses")
    @app_commands.check(tortoise_bot_developer_only)
    async def list(self, interaction: discord.Interaction):
        formatted = "\n".join(
            f"{i + 1}. {s}" for i, s in enumerate(self.statuses)
        )

        await interaction.response.send_message(
            f"📊 **Current Statuses:**\n{formatted}",
            ephemeral=True,
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(StatusCog(bot))
