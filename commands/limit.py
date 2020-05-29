import utils
import functions as func
from commands.base import Cmd

help_text = [
    [
        ("kullanım:", "<PREFIX><COMMAND>\n"
                   "<PREFIX><COMMAND> `N`"),
        ("Açıklama:",
         "Zaten bir kanaldayken kullan - Kanalınızda izin verilen kullanıcı sayısını mevcut kanalla sınırlandırın "
         "kullanıcı sayısı veya belirtilen sayı.\n\n"
         "Sınırı kaldırmak için *<PREFIX>un<COMMAND>* kullanın."),
        ("Misal:", "<PREFIX><COMMAND> 4"),
    ]
]


async def execute(ctx, params):
    params_str = ' '.join(params)
    guild = ctx['guild']
    settings = ctx['settings']
    sınır = utils.strip_quotes(params_str)
    author = ctx['message'].author
    vc = ctx['voice_channel']

    if sınır:
        try:
            sınır = abs(int(sınır))
        except ValueError:
            return False, "`{}` bir sayı değil.".format(sınır)
    else:
        sınır = len(vc.members)

    if sınır > 99:
        return False, "Kullanıcı limiti 99'dan fazla olamaz."

    await vc.edit(user_limit=sınır)
    if sınır != 0:
        log_msg = "👪 {} (`{}`) set the user limit of \"**{}**\" (`{}`) to {}".format(
            func.user_hash(author), author.id, func.esc_md(vc.name), vc.id, sınır
        )
    else:
        log_msg = "👨‍👩‍👧‍👦 {} (`{}`) removed the user limit of \"**{}**\" (`{}`)".format(
            func.user_hash(author), author.id, func.esc_md(vc.name), vc.id
        )
    await func.server_log(guild, log_msg, 2, settings)
    return True, None


command = Cmd(
    execute=execute,
    help_text=help_text,
    params_required=0,
    admin_required=False,
    voice_required=True,
    creator_only=True,
)
