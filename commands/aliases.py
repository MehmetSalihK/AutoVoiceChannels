import discord
import traceback
import functions as func
from commands.base import Cmd
from utils import log

help_text = [
    [
        ("kullanım:", "<PREFIX><COMMAND>"),
        ("Açıklama:",
         "Bu sunucudaki oyun adları için tüm diğer adları listeleyin."),
    ]
]


async def execute(ctx, params):
    settings = ctx['settings']
    channel = ctx['channel']
    author = ctx['message'].author

    if not settings['aliases']:
        return True, "Henüz takma ad belirlemediniz."

    e = discord.Embed(color=discord.Color.from_rgb(205, 220, 57))
    e.title = "Bu sunucu aşağıdaki takma adlara sahip:"
    e.set_footer(
        text="Bir takma adı silmek için \"{0}removealias ORİJİNAL ADI\" kullanın, "
        "veya \"{0}alias ORİJİNAL ADI >> YENİ AD\" oluşturmak veya değiştirmek için.".format(ctx['print_prefix']))

    keys = sorted(settings['aliases'].keys(), key=lambda x: x.lower())
    for a in keys:
        av = settings['aliases'][a]
        e.add_field(name=a, value=av, inline=True)
    try:
        await channel.send(embed=e)
    except discord.errors.Forbidden:
        log("Yankılamak yasak", channel.guild)
        await func.dm_user(
            author,
            "İçinde mesaj gönderme iznim yok "
            "**{}** kanalının `#{}` kanalı.".format(channel.name, channel.guild.name)
        )
        return False, "NO RESPONSE"
    except Exception:
        log("Yankılamadı", channel.guild)
        print(traceback.format_exc())
        return False, "NO RESPONSE"

    return True, "NO RESPONSE"


command = Cmd(
    execute=execute,
    help_text=help_text,
    params_required=0,
    admin_required=True,
)
