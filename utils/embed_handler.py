from typing import Union
import constants
from discord import Embed, Color, Member, User

def get_top_role_color(member: Union[Member, User], *, fallback_color) -> Color:
    """
    Tries to get member top role color and if fails returns fallback_color - This makes it work in DMs.
    Also if the top role has default role color then returns fallback_color.
    :param member: Member to get top role color from. If it's a User then default discord color will be returned.
    :param fallback_color: Color to use if the top role of param member is default color or if param member is
                           discord.User (DMs)
    :return: discord.Color
    """
    try:
        color = member.top_role.color
    except AttributeError:
        # Fix for DMs
        return fallback_color

    if color == Color.default():
        return fallback_color
    else:
        return color



def simple_embed(message: str, title: str, color: Color) -> Embed:
    embed = Embed(title=title, description=message, color=color)
    return embed


def info(message: str, member: Union[Member, User], title: str = "Info") -> Embed:
    """
    Constructs success embed with custom title and description.
    Color depends on passed member top role color.
    :param message: embed description
    :param member: member object to get the color of it's top role from
    :param title: title of embed, defaults to "Info"
    :return: Embed object
    """
    return Embed(title=title, description=message, color=get_top_role_color(member, fallback_color=Color.green()))


def success(message: str, member: Union[Member, User] = None) -> Embed:
    """
    Constructs success embed with fixed title 'Success' and color depending
    on passed member top role color.
    If member is not passed or if it's a User (DMs) green color will be used.
    :param message: embed description
    :param member: member object to get the color of it's top role from,
                   usually our bot member object from the specific guild.
    :return: Embed object
    """
    return simple_embed(f"{constants.success_emoji}︱{message}", "",
                        get_top_role_color(member, fallback_color=Color.green()))


def warning(message: str) -> Embed:
    """
    Constructs warning embed with fixed title 'Warning' and color gold.
    :param message: embed description
    :return: Embed object
    """
    return simple_embed(f":warning:︱{message}", "", Color.dark_gold())


def failure(message: str) -> Embed:
    """
    Constructs failure embed with fixed title 'Failure' and color red
    :param message: embed description
    :return: Embed object
    """
    return simple_embed(f"{constants.failure_emoji}︱{message}", "", Color.red())


def code_eval_embed(language: str, output: str, *, edited: bool = False, exit_code: int = -1, disable_extras=False) -> Embed:
    title = "Execution Result (edited)" if edited else "Execution Result"
    if language == "java":
        title += "〖beta〗"
    color = (Color.dark_red() if exit_code != 0 else Color.green() if edited else Color.dark_green())

    if not output:
        output = "(no output)"

    if len(output) > 4000:
        output = output[:4000] + "\n... (truncated)"

    output = output.rstrip("\n")
    lines = output.split("\n")
    last_line = lines[-1] if lines else ""
    space_req = max(0, 49 - len(last_line))
    spacer = "\u2800" * space_req
    embed = Embed(title=title, description=f"```ex\n{output}{spacer}```", color=color)

    if not disable_extras:
        embed.add_field(name="Language", value=f"```ex\n{language.capitalize()}```", inline=True)
        embed.add_field(name="Exit code", value=f"```ex\n{exit_code}```", inline=True)
    return embed

def runtime_join_embed() -> Embed:
    embed = Embed(
        title="Thank you for using Runtime",
        description=(
            "Use `/run_help` to get started.\n"
            "Execution is enabled by default, administrators can enable or disable it using bot commands.\n\n"
            "This bot runs on the [Hermes Engine](https://github.com/Ryuga/Hermes), which is currently in beta, so occasional performance issues may occur.\n\n"
            "[GitHub](https://github.com/Tortoise-Community/Runtime-BOT)  •  "
            "[Website](https://runtime-bot.tortoisecommunity.org)  •  "
            "[Status](https://runtime-bot.tortoisecommunity.org/health)  •  "
            f"[Support]({constants.discord_invite_link})"
        ),
        color=Color.dark_green()
    )
    embed.set_footer(text=f"Tortoise Programming Community", icon_url="https://avatars.githubusercontent.com/u/54438042")
    return embed
