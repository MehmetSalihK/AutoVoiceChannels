import discord
import traceback
from functions import echo, dm_user, esc_md
from utils import log
from commands.base import Cmd

help_text = [
    [
        ("Usage:", "<PREFIX><COMMAND>\n"
                   "<PREFIX><COMMAND> `COMMAND`"),
        ("Description:", "Get help using this bot, or more information about a particular command."),
        ("Example:", "<PREFIX><COMMAND> template"),
    ]
]


async def execute(ctx, params):
    channel = ctx['channel']
    author = ctx['message'].author
    if not params:
        support_server_id = 601015720200896512
        if not ctx['admin'] and ctx['guild'].id != support_server_id:
            e = discord.Embed(color=discord.Color.from_rgb(205, 220, 57))
            e.title = "Otomatik Ses Kanalları"
            e.description = (
                "Sesli olarak istediğiniz kadar dinamik ve sonsuz ses kanalı oluşturmanızı sağlayan bir botum, "
                "ve artık kullanılmadıkları anda otomatik olarak silebilirler.\n\n"
                "Sadece bir ses kanalına katılın, ben de sizin için yeni bir kanal oluşturacağım ve sizi buna taşıyacağım."
            )
            text = (
                " ·  **<PREFIX>kilit** - "
                "Daha fazla kişinin katılamayacağı şekilde ses kanalınızın kullanıcı sınırını kilitleyin. "
                "Sınırı kaldırmak için **<PREFIX>unlock** kullanın.\n\n"
                " ·  **<PREFIX>sınır `N`** - "
                "Kanalınızın kullanıcı sınırını belirli bir sayıya ayarlayın. "
                "Sınırı kaldırmak için **<PREFIX>unlock** kullanın.\n\n"
                " ·  **<PREFIX>özel** - "
                "Ses kanalınızı gizli hale getirerek kimsenin size doğrudan katılmasını önleyin. "
                "Birileri sana katılmak için, üstünde bir \"⇩ Katıl {}\" kanalı oluşturur.\n\n"
                " ·  **<PREFIX>kick `@USER`** - "
                "Birini kanalınızdan atmak için bir oy kullanma başlatın.\n\n"
                " ·  **<PREFIX>aktar `@USER`** - "
                "Kanalınızın sahipliğini başka birine aktarın.\n\n".format(
                    esc_md(author.display_name)
                )
            )
            if ctx['gold']:
                text += (
                    " ·  **<PREFIX>isim** - Ses kanalınızın adını değiştirme.\n\n"
                    " ·  **<PREFIX>nick** - İçerik oluşturucunun adını gösteren kanalların sizi arayacağını belirleyin.\n\n"
                 #   " ·  **<PREFIX>bithızı** - Kendiniz için sunucu genelinde özel bir bit hızı (kbps cinsinden) ayarlayın. katıldığınız tüm "
                 #  "kanallar için kullanılır.\n\n"
                )
            text += (
                " ·  **<PREFIX>davet** - Beni başka bir sunucuya davet et!\n\n"
                " ·  **<PREFIX>help `komut`** - Belirli bir komut hakkında daha fazla bilgi edinin."
            )
            text = text.replace('<PREFIX>', ctx['print_prefix'])
            e.add_field(name="Komutlar:", value=text)
            try:
                await channel.send(embed=e)
            except discord.errors.Forbidden:
                log("Forbidden to echo", channel.guild)
                await dm_user(
                    author,
                    "I don't have permission to send messages in the "
                    "`#{}` channel of **{}**.".format(channel.name, channel.guild.name)
                )
                return False, "NO RESPONSE"
            return True, "NO RESPONSE"
        can_embed = channel.permissions_for(ctx['guild'].me).embed_links
        with open("docs.md", 'r', encoding='utf8') as f:
            docs = f.read()
        sections = docs.split('** **')
        for i, s in enumerate(sections):
            s = s.replace("@Auto Voice Channels ", "@{} ".format(ctx['message'].guild.me.display_name))
            s = s.replace("vc/", esc_md(ctx['prefix_p']))
            s = s.replace("@pixaal", author.mention)
            s = s.replace(" :)", " :slight_smile:")
            s = s.replace("**Gold Patron**", ":credit_card: **Gold Patron**")
            s = s.replace("Change the prefix of the bot (default is", "Change the prefix of the bot (currently")
           # s = s.replace("<https://www.patreon.com/pixaal>", "https://www.patreon.com/pixaal")  # Always embed
            if s.startswith("\n**-- Commands --**\n") and can_embed:
                lines = [l for l in s.split('\n') if l != ""]
                parts = []
                title = []
                end_of_title = False
                cmds = []
                for l in lines:
                    if not l.startswith('`'):
                        if end_of_title:
                            parts.append(["** **\n" + '\n'.join(title), cmds])
                            title = []
                            cmds = []
                            end_of_title = False
                        title.append(l)
                    else:
                        end_of_title = True
                        cmds.append(l)
                parts.append(["** **\n" + '\n'.join(title), cmds])

                for j, p in enumerate(parts):
                    embed = discord.Embed(color=discord.Color.from_rgb(205, 220, 57))
                    for c in p[1]:
                        cmd_name, cmd_desc = c.split(" - ", 1)
                        embed.add_field(name=" ·  " + cmd_name, value=cmd_desc)
                    try:
                        await channel.send(content=p[0].replace("Komutlar --**", "Komutlar --**\n"), embed=embed)
                    except discord.errors.Forbidden:
                        log("Forbidden to echo", channel.guild)
                        await dm_user(
                            author,
                            "I don't have permission to send messages in the "
                            "`#{}` channel of **{}**.".format(channel.name, channel.guild.name)
                        )
                        return False, "NO RESPONSE"
                continue
            if i == 0:
                s = '\n'.join(s.strip('\n').split('\n')[:-1])  # Remove last line of first section (gfycat embed)
               # s += "\nhttps://gfycat.com/latemealyhoneyeater"
            else:
                s = '** **' + s
            echo_success = await echo(s, channel, author)
            if not echo_success:
                return False, "NO RESPONSE"
        return True, "NO RESPONSE"
    else:
        from commands import commands
        c = params[0]
        if c in commands:
            replacements = {
                "<PREFIX>": ctx['print_prefix'],
                "<COMMAND>": c,
                "<USER>": author.mention,
            }
            help_text = commands[c].help_text
            for part in help_text:
                e = discord.Embed(color=discord.Color.from_rgb(205, 220, 57))
                content = None
                if 'incorrect_command_usage' in ctx and part == help_text[0]:
                    content = " ".format(c)
                if part == help_text[-1]:
                    e.set_footer(text="Daha fazla yardım: discord.io/TurkServerSunucusu",
                                 icon_url=ctx['guild'].me.avatar_url_as(size=32))
                for i, p in enumerate(part):
                    t = ("⠀\n" + p[0]) if i != 0 and not p[0].startswith(" ·  ") else p[0]
                    d = (p[1] + "\n⠀") if i == len(part) - 1 and part == help_text[-1] else p[1]
                    if t == 'title':
                        e.title = d
                    else:
                        for r, rv in replacements.items():
                            t = t.replace(r, rv)
                            d = d.replace(r, rv)
                        e.add_field(name=t, value=d, inline=False)
                try:
                    await channel.send(content=content, embed=e)
                except discord.errors.Forbidden:
                    log("Forbidden to echo", channel.guild)
                    await dm_user(
                        author,
                        "I don't have permission to send messages in the "
                        "`#{}` channel of **{}**.".format(channel.name, channel.guild.name)
                    )
                    return False, "NO RESPONSE"
                except Exception:
                    log("Failed to echo", channel.guild)
                    print(traceback.format_exc())
                    return False, "NO RESPONSE"

          #  if commands[c].sapphire_required and not ctx['sapphire']:
          #      await channel.send(
          #          "**Note:** This command is restricted to :gem: **Sapphire Patron** servers.\n"
          #          "Become a Sapphire Patron to support the development of this bot and unlock more ~~useless~~ "
          #          "amazing features: <https://www.patreon.com/pixaal>"
          #      )
          #  elif commands[c].gold_required and not ctx['gold']:
          #      await channel.send(
          #          "**Note:** This command is restricted to :credit_card: **Gold Patron** servers.\n"
          #          "Become a Gold Patron to support the development of this bot and unlock more ~~useless~~ "
          #          "amazing features: <https://www.patreon.com/pixaal>"
          #      )
          #  return True, "NO RESPONSE"
        elif c == 'expressions':
            e = discord.Embed(color=discord.Color.from_rgb(205, 220, 57))
            e.title = "Template Expressions"
            e.description = (
                "Expressions are a powerful way to set the channel name based on certain conditions, such as whether "
                "or not the creator has a particular role, what game is being played, and the party size.\n\n"
                "Expressions must be in the following form:\n"
                "```"
                "{{CONDITION ?? TRUE // FALSE}}"
                "```\n"
                "If the `CONDITION` part is met, whatever you wrote in the `TRUE` part will be added to the channel "
                "name, otherwise the `FALSE` part will be used instead. The `FALSE` part is optional and can be "
                "left out (e.g. `{{CONDITION ?? TRUE}}`).\n\n"
                "Anything at all can be written inside the `TRUE`/`FALSE` parts, including other template variables "
                "like `@@num@@` or `@@game_name@@`, or even other nested expressions, "
                "however only a certain things may be used as the `CONDITION`:\n\n"
            )
            e.add_field(
                name=" ·  `ROLE:role id`",
                value="Check whether or not the creator has a particular role.\n\n"
            )
            e.add_field(
                name=" ·  `GAME=game name`",
                value="Check if the game that users in the channel are playing (the same one that "
                "`@@game_name@@` returns, including aliases) matches **exactly** the text provided.\n"
                "You can also use `!=` instead of `=` to match anything **other** than exactly the text provided, "
                "or `:` to match anything that **contains** the text provided. "
                "E.g. `GAME:Call of Duty` will match with *\"Call of Duty: Modern Warfare\"*, "
                "but `GAME=Call of Duty` will not.\n\n"
            )
            e.add_field(
                name=" ·  `LIVE`",
                value="Whether or not the creator of the channel is streaming. Use `LIVE_DISCORD` to only detect "
                "discord's \"Go Live\" streams, or `LIVE_EXTERNAL` for Twitch. `LIVE` will include both.\n\n"
            )
            e.add_field(
                name=" ·  `PLAYERS>number`",
                value="💎 [*patrons only.*](https://patreon.com/pixaal) Check if the number of players in your game "
                "(determined either by Discord Rich Presence or the game activity statuses of members in the channel) "
                "is greater than the number provided. You can also use `<`, `<=`, `>=`, `=` and `!=`.\n\n"
            )
            e.add_field(
                name=" ·  `MAX>number`",
                value="💎 [*patrons only.*](https://patreon.com/pixaal) Check if the maximum number of players "
                "allowed in your game (determined by Discord Rich Presence or the channel limit) is greater than the "
                "number provided. You can also use `<`, `<=`, `>=`, `=` and `!=`.\n\n"
            )
            e.add_field(
                name=" ·  `RICH`",
                value="💎 [*patrons only.*](https://patreon.com/pixaal) Whether or not the current game uses "
                      "Discord Rich Presence, which means `@@num_playing@@`, `@@party_size@@`, `@@party_state@@`, and "
                      "`@@party_details@@` should have reliable values.\n\n"
            )
            try:
                await channel.send(embed=e)
            except discord.errors.Forbidden:
                log("Forbidden to echo", channel.guild)
                await dm_user(
                    author,
                    "I don't have permission to send messages in the "
                    "`#{}` channel of **{}**.".format(channel.name, channel.guild.name)
                )
                return False, "NO RESPONSE"
            e = discord.Embed(color=discord.Color.from_rgb(205, 220, 57))
            e.title = "Örnekler"
            e.description = (
                "```{{GAME:Left 4 Dead ?? [@@num_playing@@/4]}}```"
                "```{{LIVE??🔴 @@stream_name@@}}```"
                "```{{PLAYERS=1 ?? LFG}}```"
                "```{{PLAYERS<=20 ?? ## [@@game_name@@] // It's a party!}}```"
                "```{{MAX=@@num_playing@@ ?? (Full) // (@@num_playing@@)}}```"
                "```{{RICH??@@party_details@@{{MAX>1?? (@@num_playing@@/@@party_size@@)}}}}```"
                "```{{ROLE:601025860614750229 ?? {{ROLE:615086491235909643??[UK] // {{ROLE:607913610139664444??[DE] // "
                "[EU]}}}}}}```\n"
                "`??` ve `//` etrafındaki boşluklar okunabilirliği artırır, ancak istemiyorsanız istenmeyebilir "
                "sonucun çevresindeki boşluklar.\n\n"
                "Bir sorunuz varsa veya ifade ayarlamak için yardıma ihtiyacınız varsa, "
                "lütfen bana [destek sunucusunda sor](https://discord.io/TurkServerSunucusu). "
                "İhtiyacınız olan ekstra değişkenleri eklemekten memnuniyet duyarım."
            )
            await channel.send(embed=e)
            return True, "NO RESPONSE"
        else:
            if 'dcnf' not in ctx['settings'] or ctx['settings']['dcnf'] is False:
                return False, ("`{}` is not a recognized command. Run '**{}help**' "
                               "to get a list of commands".format(c, ctx['print_prefix']))
            else:
                return False, "NO RESPONSE"


command = Cmd(
    execute=execute,
    help_text=help_text,
    params_required=0,
    admin_required=False,
)
