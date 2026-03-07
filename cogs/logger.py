import discord
from discord.ext import commands
from utils.embed_handler import info, runtime_join_embed
from constants import system_log_channel_id


class BotLogger(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def _send(self, content=None, embed=None):
        channel = self.bot.get_channel(system_log_channel_id)
        if channel:
            await channel.send(content=content, embed=embed)

    async def _resolve_invite(self, guild: discord.Guild):
        inviter = None
        invite_url = None

        try:
            invites = await guild.invites()
            if invites:
                invite = max(invites, key=lambda i: i.uses or 0)
                inviter = invite.inviter
                invite_url = f"https://discord.gg/{invite.code}"
        except Exception:
            pass

        if not invite_url:
            try:
                for channel in guild.text_channels:
                    invite = await channel.create_invite(max_age=0, max_uses=0)
                    invite_url = invite.url
                    break
            except Exception:
                pass

        return inviter, invite_url

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        inviter, invite = await self._resolve_invite(guild)

        inviter_text = f"{inviter}" if inviter else "Unknown"
        invite_text = invite if invite else "None"

        text = f"{inviter_text} added bot to **{guild.name}** : {invite_text}"

        embed = info(text, None, "Bot Added")

        await self._send(embed=embed)

        target_channel = None

        if guild.system_channel and guild.system_channel.permissions_for(guild.me).send_messages:
            target_channel = guild.system_channel
        else:
            for channel in guild.text_channels:
                perms = channel.permissions_for(guild.me)
                if perms.send_messages and perms.embed_links:
                    target_channel = channel
                    break

        if target_channel:
            try:
                await target_channel.send(embed=runtime_join_embed())
            except discord.HTTPException:
                pass

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        text = f"Bot removed from **{guild.name}** (`{guild.id}`)"
        embed = info(text, None, "Bot Removed")
        await self._send(embed=embed)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        await self._send(content=f"```py\nCommand Error:\n{repr(error)}\n```")

    @commands.Cog.listener()
    async def on_app_command_error(self, interaction: discord.Interaction, error):
        await self._send(content=f"```py\nSlash Command Error:\n{repr(error)}\n```")

    @commands.Cog.listener()
    async def on_error(self, event, *args, **kwargs):
        await self._send(content=f"```py\nEvent Error in {event}\n```")


async def setup(bot: commands.Bot):
    await bot.add_cog(BotLogger(bot))