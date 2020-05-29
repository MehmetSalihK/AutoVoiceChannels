import cfg
import discord
import utils
import functions as func
from math import floor
from commands.base import Cmd
from time import time

help_text = [
    [
        ("Usage:",
         "```<PREFIX><COMMAND> @USER```"
         "```<PREFIX><COMMAND> @USER\nREASON```"),
        ("Description:",
         "Initiate a votekick to remove a user from your channel and prevent them from joining again. "
         "**More than half** of the remaining users must vote yes in order for the member to be kicked.\n\n"
         "If you wish to allow a kicked user to return to the channel, you will all have to leave and create a new "
         "channel instead, or if you are a server admin, manually edit the channel permissions.\n\n"
         "The person who initially created the channel cannot be kicked (unless they leave voluntarily and later "
         "return, in which case the \"creator\" of the channel is reassigned to the person who was at the top of the "
         "channel when they left.)"),
        ("Examples:",
         "```<PREFIX><COMMAND> @pixaal```"
         "```<PREFIX><COMMAND> pixaal#1234\nBeing mean :(```"
         "```<PREFIX><COMMAND> pixaal\nSound board abuse```"),
    ]
]


async def execute(ctx, params):
    params_str = ' '.join(params).strip()
    guild = ctx['guild']
    settings = ctx['settings']
    author = ctx['message'].author
    vc = ctx['voice_channel']
    parts = params_str.split('\n', 1)
    name = parts[0]
    reason = parts[1] if len(parts) > 1 else None

    user = utils.get_user_in_channel(name, vc)

    if not user:
        return False, "Kanalınızda \"{}\" adında herhangi bir kullanıcı bulunamıyor.".format(name)
    if user.id == utils.get_creator_id(settings, vc):
        return False, "Bu kanalın yaratıcısını tekmeleyemezsiniz."
    if user == author:
        return False, "Lütfen kendini tekmeleme :frowning:"

    participants = [m for m in vc.members if m not in [author, user] and not m.bot]
    required_votes = floor((len(participants) + 1) / 2) + 1
    try:
        text = (
            "‼ **Votekick** ‼\n"
            "{initiator} karşı bir oylama başlattı {offender}.{reason}\n\n"
            "{participants}:\n{offender} atmak için ✅ ile tepki vererek oy verin, "
            "veya oy vermek için bu mesajı dikkate almayın **Hayır**.\n\n"
            "Oy vermek için **2 dakikanız** var. Çoğunluk oyu ({req}/{tot}) gereklidir.\n"
            "{initiator} oyunuz otomatik olarak sayılır. Kanalınızda olmayan kullanıcıların oyları yok sayılır."
            "".format(
                initiator=author.mention,
                offender=user.mention,
                reason=(" Sebep: **{}**".format(reason) if reason else ""),
                participants=' '.join([m.mention for m in participants]),
                req=required_votes,
                tot=len(participants) + 1
            )
        )
        if not participants:
            text = "..."
        m = await ctx['message'].channel.send(text)
    except discord.errors.Forbidden:
        return False, "Kick komutuna cevap verme iznim yok."
    cfg.VOTEKICKS[m.id] = {
        "initiator": author,
        "participants": participants,
        "required_votes": required_votes,
        "offender": user,
        "reason": reason,
        "in_favor": [author],
        "voice_channel": vc,
        "message": m,
        "end_time": time() + 120
    }
    try:
        if participants:
            await m.add_reaction('✅')
    except discord.errors.Forbidden:
        pass
    await func.server_log(
        guild,
        "👢 {} (`{}`), \"**{}**\" da **{}** (`{}`) karşısında bir oylama başlattı. Sebep: *{}*.".format(
            func.user_hash(author), author.id, func.user_hash(user), user.id, vc.name, reason
        ), 1, settings)
    return True, "NO RESPONSE"


command = Cmd(
    execute=execute,
    help_text=help_text,
    params_required=1,
    admin_required=False,
    voice_required=True,
)
