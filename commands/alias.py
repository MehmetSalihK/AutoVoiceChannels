import utils
from commands.base import Cmd

help_text = [
    [
        ("kullanım:", "<PREFIX><COMMAND> `GAME NAME` >> `ALIAS`"),
        ("Açıklama:",
         "Örneğin kanal kenar çubuğuna sığmayacak kadar uzunsa, belirli bir oyun için görüntülenen adı değiştirin.\n\n"
         "**Uyarı:** Takma adlar büyük/küçük harfe duyarlıdır. Oyunun adını tam olarak eşleştirdiğinizden emin olun, "
         "yoksa değiştirilmeyecektir.\n\n"
         "Mevcut tüm diğer adları listelemek için `<PREFIX>aliases` ve silmek için `<PREFIX>removealias` kullanın."),
        ("Misal:", "<PREFIX><COMMAND> The Elder Scrolls V: Skyrim >> Skyrim"),
    ]
]


async def execute(ctx, params):
    params_str = ' '.join(params)
    guild = ctx['guild']
    settings = ctx['settings']
    gsplit = params_str.split('>>')
    if len(gsplit) != 2 or not gsplit[0] or not gsplit[-1]:
        return False, ("Takma ad komutu için yanlış sözdizimi. Olması gereken: `{}alias [Gerçek oyun adı] >> "
                       "[Yeni isim]` (köşeli ayraç olmadan).".format(ctx['print_prefix']))
    else:
        gname = utils.strip_quotes(gsplit[0])
        aname = utils.strip_quotes(gsplit[1])
        if gname in settings['aliases']:
            oaname = settings['aliases'][gname]
            response = "'{}' zaten bir takma ada sahip ('{}'), '{}' ile değiştirilecek.".format(gname, oaname, aname)
        else:
            response = "'{} 'şimdi' {} 'olarak gösterilecek.".format(gname, aname)
        settings['aliases'][gname] = aname
        utils.set_serv_settings(guild, settings)
        return True, response


command = Cmd(
    execute=execute,
    help_text=help_text,
    params_required=1,
    admin_required=True,
)
