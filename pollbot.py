import discord
from discord.ext import commands
from discord.ext.commands import CommandOnCooldown, BucketType

client = commands.Bot(command_prefix='--')

emoji_reactions = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

client.remove_command('help')


@client.event
async def on_command_error(ctx, exc):

    if isinstance(exc, CommandOnCooldown):

        time_embed = discord.Embed(title="Cooldown", description="You'll need to wait until \n you can use this command again!", color=0x8c0e0e)
        time_embed.add_field(name="Time left", value=f"{exc.retry_after: ,.0f} seconds")

        await ctx.send(embed=time_embed)

    raise exc


@client.command(name="help")
async def help(context):

    help_embed = discord.Embed(title="📊Poll Bot Usage:", description="**Yes/No poll:**\n--poll title/descripti"
                                                                      "on\n\n**Multiple choice poll(up to 10 choices/):"
                                                                      "**\n--poll title/descpription/choice1/choice2/ch"
                                                                      "oice3/etc...\n\n**Custom reaction poll**\n--"
                                                                      "custompoll title;descpription;choice1/choice2"
                                                                      "/etc...;emojis1/emoji2/etc...\n\n[Add PollBot to "
                                                                      "your server](https://discord.com/api/oauth2/aut"
                                                                      "horize?client_id=822315210672308284&permissions="
                                                                      "3221748800&scope=bot)"
                               , color=0x5daac1)

    help_embed.set_footer(text="Developed by GO#6275")

    await context.message.channel.send(embed=help_embed)


@client.event
async def on_ready():

    await client.change_presence(status=discord.Status.online, activity=discord.Game(" --help"))

    guilds = client.guilds

    for Guild in guilds:
        print(Guild.name + " GUILD")

    print("I'm online!")


@client.command(name="poll")
@commands.cooldown(1, 10, BucketType.user)
async def poll(context, *args):

    # returns if no args
    if not args:
        return

    # joins args into single item
    poll_input = " ".join(args)

    # seperates poll_input by splits, and stores into args_list
    args_list = poll_input.split("/")

    # gets poll question from args_list
    poll_title = args_list[0]

    # gets the poll description from args_list
    poll_description = args_list[1]

    # runs if is args_list only contains 1 item(poll_question)
    if len(args_list) == 2:
        # creates embed with title of poll question
        poll_embed = discord.Embed(title=str("📊  " + poll_title), description=poll_description, color=0x5daac1)

        # sends and stores poll_embed
        embed = await context.message.channel.send(embed=poll_embed)

        # reacts to poll with thumbs up and down reaction
        await embed.add_reaction("👍")
        await embed.add_reaction("👎")
        return()

    # gets the poll choices
    poll_reactions = args_list[2:]

    poll_description += "\n\n"

    # create empty reactions list
    reactions = []

    # tells user if there are too many options(more than 10)
    if len(poll_reactions) > 10:
        await context.message.channel.send("You have too many choices!")
        return

    # runs for each item in poll_reactions
    for i in range(len(poll_reactions)):

        # sets emoji according to corresponding index of number emoji list
        emoji = emoji_reactions[i]

        # adds emoji to list of reactions
        reactions.append(emoji_reactions[i])

        # adds to desc, with emoji and corresponding choice/reactions
        poll_description += str(emoji + poll_reactions[i] + ", ")

    # creates embed
    poll_embed = discord.Embed(title=str("📊" + poll_title), description=str(poll_description), color=0x5daac1)

    # send embed and store message to use for future reference
    embed = await context.message.channel.send(embed=poll_embed)

    # adds reaction to message, for each item in reactions list
    for i in reactions:
        await embed.add_reaction(i)


@client.command(name="custompoll")
@commands.cooldown(1, 10, BucketType.user)
async def complexpoll(context, *args):

    # returns if no args
    if not args:
        return

    # joins args into single item
    poll_input = " ".join(args)

    # seperates poll_input by splitting, and stores into args_list
    args_list = poll_input.split(";")

    # gets poll question from args_list
    poll_title = args_list[0]


    # gets poll description from args_list
    poll_description = str(args_list[1]+"\n\n")

    # gets poll reactions from args_list
    poll_raw_reactions = args_list[2]
    poll_reactions = poll_raw_reactions.split("/")

    # gets poll emojis from args_list
    poll_raw_emojis = args_list[3]
    poll_emojis = poll_raw_emojis.split("/")

    # create empty reactions list
    reactions = []

    # runs for each item in poll_reactions
    for i in range(len(poll_reactions)):

        # sets emoji according to corresponding index of number emoji list
        emoji = poll_emojis[i]

        # adds emoji to list of reactions
        reactions.append(poll_emojis[i])

        # adds to desc, with emoji and corresponding choice/reactions
        poll_description += str(emoji + poll_reactions[i] + ", ")

    # creates embed
    poll_embed = discord.Embed(title=str("📊" + poll_title), description=str("\n" + poll_description), color=0x5daac1)

    # send embed and store message to use for future reference
    embed = await context.message.channel.send(embed=poll_embed)

    # adds emoji to message, for each emoji in reactions list
    for i in reactions:
        # clears extra spaces
        emote = i.replace(" ", "")
        await embed.add_reaction(emote)


# Runs the client on the server
client.run('ODIyMzE1MjEwNjcyMzA4Mjg0.YFQeuA.ZvxN7gyM9mPSNcny8Iv9H-ngYNk')
