import discord
import functions as func
from commands.base import Cmd

help_text = [
    [
        ("kullanım:", "<PREFIX><COMMAND>"),
        ("Açıklama:",
         "Yeni bir ana ses kanalı oluşturun. Kullanıcılar bu kanala katıldıklarında, yeni bir kanal oluşturur ve onları taşırım "
         "içinde. Varsayılan olarak, ana kanallar \"+\" olarak adlandırılır ve sunucunuzun en üstüne yerleştirilir, ancak "
         "güvenle yeniden adlandırabilir, taşıyabilir ve izinlerini değiştirebilirsiniz.\n\n"
         "İstediğiniz kadar ana kanal oluşturabilir ve bunları sunucunuzun farklı alanlarına yerleştirebilirsiniz. "
         "Onlar (ve onlar için oluşturduğum ikincil kanallar) izinlerini bulundukları kategoriden devralacak "
         "varsayılan olarak.\n\n"
         "Bir ana kanalı özel/kısıtlanmış bir kategoriye taşırsanız, ** oluşturma iznim olduğundan emin olun "
         "ve orada ses kanallarını düzenleyin**.\n\n"
         "İkincil kanallar, birincil kanallarının çevresini, bit hızını ve kullanıcı sınırını kopyalar.\n\n"
         "Varsayılan olarak, ikincil kanallar birincil kanallarının üzerine yerleştirilir. Kullanım *<PREFIX>toggleposition* "
         "onları aşağıya yerleştirmek için."),
    ]
]


async def execute(ctx, params):
    guild = ctx['guild']
    default_name = "➕ Oda Oluştur"

    try:
        await func.create_primary(guild, default_name, ctx['message'].author)
    except discord.errors.Forbidden:
        return False, "Kanal oluşturma iznim yok."
    except discord.errors.HTTPException as e:
        return False, "Bir HTTPException oluştu: {}".format(e.text)

    response = ("\"{}\" Adlı yeni bir ses kanalı oluşturuldu. "
                "Şimdi taşıyabilir, yeniden adlandırabilirsiniz, vb.\n\n"
                "Kullanıcı bu ses kanalına her girdiğinde, üstünde yeni bir ses kanalı oluşturulur. "
                "onlar için otomatik olarak taşınır.\n"
                "Bu dize boş olduğunda, otomatik olarak silinecektir.\n\n"
                "Yeni kanalların adlandırma şemasını değiştirmek için `{}template` kullanın".format(default_name,
                                                                                           ctx['print_prefix']))
    return True, response


command = Cmd(
    execute=execute,
    help_text=help_text,
    params_required=0,
    admin_required=True,
)
