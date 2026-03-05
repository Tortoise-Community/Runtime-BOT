from discord import Color

tortoise_guild_id = 577192344529404154
website_url = "https://www.tortoisecommunity.org/"
github_repo_link = "https://github.com/Ryuga/Hermes"
discord_invite = "https://discord.gg/WeUtJ7hqum/"

# Log Channel IDs
system_log_channel_id = 1461947577200148605
bot_log_channel_id = 693090079329091615
bot_dev_channel_id = 692851221223964822

# Roles
moderator_role = 577368219875278849
admin_role = 577196762691928065

# Emojis
success_emoji = "<a:success:1479072071064490069>"
failure_emoji = "<a:success:1479072071064490069>"

# Special
tortoise_developers = (197918569894379520, 612349409736392928)

# Embeds are not monospaced so we need to use spaces to make different lines "align"
# But discord doesn't like spaces and strips them down.
# Using a combination of zero width space + regular space solves stripping problem.
embed_space = "\u200b "

# After this is exceeded the link to tortoise paste service should be sent
max_message_length = 1000

rate_limit_minutes = 10