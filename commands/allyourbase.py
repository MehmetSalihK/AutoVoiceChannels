import utils
import functions as func
from commands.base import Cmd

help_text = [
    [
        ("kullanım:", "<PREFIX><COMMAND>"),
        ("Açıklama:",
         "Bulunduğunuz kanalın sahipliğini varsayalım.\n"
         "Yönetici olarak, aslında içerik oluşturucu olmasanız bile yalnızca içerik oluşturucuya ait tüm komutları kullanabilirsiniz, "
         "ancak bu sizi diğer herkesin yaratıcısı olarak gösterecektir.\n\n"
         "Yaratıcı olarak başka birini atamak istiyorsanız `<PREFIX>aktar @KULLANICI` kullanın."),
    ]
]


async def execute(ctx, params):
    guild = ctx['guild']
    author = ctx['message'].author
    vc = ctx['voice_channel']

    creator_id = utils.get_creator_id(ctx['settings'], vc)

    if author.id == creator_id:
        return False, "Sen zaten yaratıcısın."

    result = await func.set_creator(guild, vc.id, author)
    return result, None


command = Cmd(
    execute=execute,
    help_text=help_text,
    params_required=0,
    admin_required=True,
    voice_required=True,
)
