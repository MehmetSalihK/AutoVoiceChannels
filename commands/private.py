import cfg
import discord
import utils
import functions as func
from commands.base import Cmd
from time import time

help_text = [
    [
        ("kullanım:", "<PREFIX><COMMAND>"),
        ("Açıklama:",
         "Ses kanalınızı gizli hale getirerek kimsenin size doğrudan ulaşmasını önleyin.\n\n"
         "İnsanların size katılmasını isteyebilmeleri için kendinizin üstünde bir \"⇩ Katıl (kullanıcı adı)\" kanalı oluşturun "
         "Birisi bu kanala katıldığında sana bir mesaj gönderirim"
         "kabul et/reddet/engelle."),
    ]
]


async def execute(ctx, params):
    guild = ctx['guild']
    settings = ctx['settings']
    author = ctx['message'].author
    vc = ctx['voice_channel']

    for p, pv in settings['auto_channels'].items():
        for s, sv in pv['secondaries'].items():
            if s == vc.id:
                if 'priv' in sv and sv['priv']:
                    return False, ("Kanalınız zaten özel."
                                   "kullanım `{}public` kanalı herkese açmak için.".format(ctx['print_prefix']))
                try:
                    await vc.set_permissions(author, connect=True)
                    await vc.set_permissions(guild.default_role, connect=False)
                except discord.errors.Forbidden:
                    return False, ("Bunu yapmak için iznim yok."
                                   "Lütfen bu sunucuda ve kategoride *Rolleri Yönet* iznine sahip olduğumdan emin olun.")
                settings['auto_channels'][p]['secondaries'][s]['priv'] = True
                settings['auto_channels'][p]['secondaries'][s]['msgs'] = ctx['channel'].id
                utils.set_serv_settings(guild, settings)
                cfg.PRIV_CHANNELS[s] = {
                    'creator': author,
                    'voice_channel': vc,
                    'primary_id': p,
                    'text_channel': ctx['channel'],
                    'guild_id': guild.id,
                    'request_time': time(),
                    'prefix': ctx['print_prefix'],
                }
                return True, ("Kanalınız artık özel!\n"
                              "Kısa bir süre kanalınızın üzerinde \"**⇩ Katıl {}**\" kanalı görünecektir. "
                              "Birisi size katılmasını istemek için bu kanala girdiğinde, "
                              "Buraya, isteğini onaylamanızı veya reddetmenizi isteyen bir mesaj göndereceğim.\n"
                              "kullanım `{}public` kanalı herkese açmak için.."
                              "".format(func.esc_md(author.display_name), ctx['print_prefix']))
    return False, "Artık bir ses kanalındaymışsınız gibi görünmüyor."


command = Cmd(
    execute=execute,
    help_text=help_text,
    params_required=0,
    admin_required=False,
    voice_required=True,
    creator_only=True,
)
