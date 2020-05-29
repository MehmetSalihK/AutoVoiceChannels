import cfg
import discord
import utils
from commands.base import Cmd

help_text = [
    [
        ("Usage:", "<PREFIX><COMMAND>"),
        ("Description:",
         "Make your private channel public again, so anyone can join."),
    ]
]


async def execute(ctx, params):
    guild = ctx['guild']
    settings = ctx['settings']
    vc = ctx['voice_channel']

    for p, pv in settings['auto_channels'].items():
        for s, sv in pv['secondaries'].items():
            if s == vc.id:
                if 'priv' not in sv or not sv['priv']:
                    return False, ("Kanalınız zaten herkese açık. "
                                   "Bunun yerine özel yapmak için `{}özel` kullanın.".format(ctx['print_prefix']))
                try:
                    await vc.set_permissions(guild.default_role, connect=True)
                except discord.errors.Forbidden:
                    return False, ("Bunu yapmak için iznim yok."
                                   "Lütfen bu sunucuda ve kategoride *Rolleri Yönet* iznine sahip olduğumdan emin olun.")
                settings['auto_channels'][p]['secondaries'][s]['priv'] = False
                try:
                    jcid = settings['auto_channels'][p]['secondaries'][s]['jc']
                    del settings['auto_channels'][p]['secondaries'][s]['jc']
                except KeyError:
                    jcid = 0
                utils.set_serv_settings(guild, settings)
                if s in cfg.PRIV_CHANNELS:
                    del cfg.PRIV_CHANNELS[s]
                try:
                    jc = guild.get_channel(jcid)
                    if jc:
                        await jc.delete()
                except discord.errors.Forbidden:
                    return False, "Kanalınız artık herkese açık, ancak **⇩ Katıl** kanalınızı silme iznim yok."
                return True, "Kanalınız artık herkese açık!"
    return False, "Artık bir ses kanalındaymışsınız gibi görünmüyor."


command = Cmd(
    execute=execute,
    help_text=help_text,
    params_required=0,
    admin_required=False,
    voice_required=True,
    creator_only=True,
)
