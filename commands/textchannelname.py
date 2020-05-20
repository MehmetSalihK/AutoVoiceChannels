import discord
import utils
import functions as func
from commands.base import Cmd

help_text = [
    [
        ("Usage:", "<PREFIX><COMMAND> `NEW NAME`"),
        ("Description:",
         "Modifiez le nom des canaux de texte privés temporaires créés pour chaque conversation vocale si `textchannels` est activé."
         "\nLa valeur par défaut est `voice context`."),
        ("Example:", "<PREFIX><COMMAND> typing/tts/bot commands"),
    ]
]


async def execute(ctx, params):
    params_str = ' '.join(params)
    guild = ctx['guild']
    settings = ctx['settings']
    author = ctx['message'].author
    new_word = params_str.replace('\n', ' ')  # Can't have newlines in channel name.
    new_word = utils.strip_quotes(new_word)
    previous_word = ("text" if 'text_channel_name' not in settings else
                     func.esc_md(settings['text_channel_name']))
    if not new_word:
        return False, ("You need to define a new name, e.g. `{}textchannelname links` to make "
                       "**links** shown instead of **{}**.".format(ctx['print_prefix'], previous_word))
    settings['text_channel_name'] = new_word
    utils.set_serv_settings(guild, settings)
    e_new_word = func.esc_md(new_word)
    await func.server_log(
        guild,
        "💬 {} (`{}`) définissez le nom \"text\" du serveur sur **{}**".format(
            func.user_hash(author), author.id, e_new_word
        ), 2, settings)

    for p, pv in settings['auto_channels'].items():
        for s, sv in pv['secondaries'].items():
            if 'tc' in sv:
                tc = guild.get_channel(sv['tc'])
                try:
                    await tc.edit(name=utils.nice_cname(new_word))
                except discord.errors.Forbidden:
                    pass

    return True, ("Done! From now on I'll use **{}** instead of **{}**.".format(e_new_word, previous_word))


command = Cmd(
    execute=execute,
    help_text=help_text,
    params_required=1,
    gold_required=True,
    admin_required=True,
)
