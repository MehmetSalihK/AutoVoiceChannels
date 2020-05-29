import utils
import functions as func
from commands.base import Cmd

help_text = [
    [
        ("kullanım:", "<PREFIX><COMMAND> `@USER`"),
        ("Açıklama:",
         "Kanalınızın sahipliğini kanaldaki başka birine aktarın; "
         "içerik oluşturucu olmalarını zorunlu kılar (ör. `özel`, `limit`, 'ad`...)."),
        ("Örnekler:",
         "```<PREFIX><COMMAND> @MehmetSalihK```"),
    ]
]


async def execute(ctx, params):
    name = ' '.join(params).strip()
    guild = ctx['guild']
    author = ctx['message'].author
    vc = ctx['voice_channel']

    user = utils.get_user_in_channel(name, vc)

    if not user:
        return False, "Kanalınızda \"{}\" adında herhangi bir kullanıcı bulunamıyor.".format(name)
    if user.id == ctx['creator_id']:
        if user == author:
            return False, "Sen zaten yaratıcısın."
        else:
            return False, "{} zaten yaratıcı.".format(func.user_hash(user))

    result = await func.set_creator(guild, vc.id, user)
    return result, None


command = Cmd(
    execute=execute,
    help_text=help_text,
    params_required=1,
    admin_required=False,
    voice_required=True,
    creator_only=True,
)
