#!/usr/bin/python3.4
#School Safe Discord Bot
#Created by Trevor L
#Last Modified 8/18/21
#Version 1.0
#---------------------------------------------------------------------------------
#This Discord bot is designed to help moderate and keep Discord servers designed for school safe
#This code may be used to help you learn how to make a bot or to make a bot for your own server
#Please do not distribute or profit from this code.
#---------------------------------------------------------------------------------
#For help go to https://realpython.com/how-to-make-a-discord-bot-python/
#https://betterprogramming.pub/how-to-make-discord-bot-commands-in-python-2cae39cbfd55
#---------------------------------------------------------------------------------

###########################################################################################################################
#############################################      Setup       ############################################################
###########################################################################################################################

import discord
import os
import time
import smtplib
import asyncio
import logging
import random
import json
import dbl
from dotenv import load_dotenv
from discord.ext import commands, tasks
from discord import Member
from discord import User
from discord.ext.commands import has_permissions, MissingPermissions
from discord.ext.commands import Bot, guild_only

from discord_slash import SlashCommand, SlashContext #Importing slash command library
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.model import SlashCommandOptionType

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN') #Grabs bot token from .env file
print("Logging in with Bot Token " + TOKEN)
BOT_UPDATE_CHANNEL = os.getenv('BOT_UPDATE_CHANNEL') #Grabs update channel .env file
print("Cam the Ram sends reconnect updates to " + BOT_UPDATE_CHANNEL)
dbl_token = os.getenv('dbl_token') #Grabs admin channel ID from .env file
print("Using DBL Token " + dbl_token)

bot = commands.Bot(command_prefix='$', intents=discord.Intents.all()) #declare intents for bot
slash = SlashCommand(bot, sync_commands=True) #Declares command prefix

with open('SwearWords.txt', 'r') as f:
    global badwords  # You want to be able to access this throughout the code
    words = f.read()
    badwords = words.split()

###########################################################################################################################
#############################################      TopGG       ############################################################
###########################################################################################################################

class TopGG(commands.Cog):
    """
    This example uses tasks provided by discord.ext to create a task that posts guild count to top.gg every 30 minutes.
    """

    def __init__(self, bot):
        self.bot = bot
        self.token = dbl_token  # set this to your DBL token
        self.dblpy = dbl.DBLClient(self.bot, self.token)
        self.update_stats.start()

    def cog_unload(self):
        self.update_stats.cancel()

    @tasks.loop(minutes=30)
    async def update_stats(self):
        """This function runs every 30 minutes to automatically update your server count."""
        await self.bot.wait_until_ready()
        try:
            server_count = len(self.bot.guilds)
            await self.dblpy.post_guild_count(server_count)
            logger.warning('Posted server count ({})'.format(server_count))
        except Exception as e:
            logger.warning('Failed to post server count\n{}: {}'.format(type(e).__name__, e))


def setup(bot):
    bot.add_cog(TopGG(bot))


global logger
logger = logging.getLogger('bot')

setup(bot)
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')


###########################################################################################################################
#############################################      Events      ############################################################
###########################################################################################################################

#############Adds server to json database on bot server join (working)##############################################################################
@bot.event
async def on_guild_join(guild):

#------------------ Set default update channel (working)------------------
    with open("welcomechannels.json", "r") as f:   #loads json file to dictionary
        guildInfo = json.load(f)

    guildInfo[guild.id] = guild.text_channels[0].id #sets key to guilds id and value to top textchannel
    
    #writes dictionary to json file
    with open("welcomechannels.json", "w") as f:
        json.dump(guildInfo, f)

#------------------ Set default admin channels (working)------------------
        
    #loads json file to dictionary
    with open("adminchannels.json", "r") as f:
        guildInfo = json.load(f)

    guildInfo[guild.id] = guild.text_channels[0].id #sets key to guilds id and value to top textchannel
    
    #writes dictionary to json file
    with open("adminchannels.json", "w") as f:
        json.dump(guildInfo, f)

#------------------ Sends join message (working) ------------------

    with open("welcomechannels.json", "r") as f:
        guildInfo = json.load(f)
    channel = bot.get_channel(guild.text_channels[0].id)
    embed = discord.Embed(colour=discord.Colour(0x788dee), url="https://discordapp.com", description=f" Hello **{guild}**! Thanks for inviting me to help keep your students safe!")

    embed.set_thumbnail(url="https://raw.githubusercontent.com/TrevorSLong/camtheram-discord/main/Screenshots/CSU-Logo.png")
    embed.set_author(name="Cam the Ram", url="https://top.gg/bot/827681932660965377", icon_url="https://raw.githubusercontent.com/TrevorSLong/camtheram-discord/main/Screenshots/CSU-Logo.png")

    embed.add_field(name="About me", value="Hi! I'm School Safe Bot, my goal is to help teachers and professors manage Discord servers intended for classroom settings.",inline=False)
    embed.add_field(name="Basic commands:", value="• Type the command ``/updatechannel`` and follow the onscreen help to set the update/welcome channel (this is where welcome messages will be sent).\n• Type the command ``/adminchannel`` and follow the onscreen help to set the admin update channel (this is where kicking, banning, and other admin announcements will be sent). \n• Typing / will show you all of the command other bots and I offer.",inline=False)
    embed.add_field(name="What I do:", value="• I attempt to delete all swear words posted in chat, the user who sent the message and the admin channel will be notified.\n• I delete messages where more then half the characters are capital letters.\n•I send a direct message to all new members laying out ground rules and expectations.\n• In the future I will be able to do more!",inline=False)
    embed.add_field(name="Help support my growth", value="I was made by two full time students, if you enjoy having me around please consider **supporting my development** by contributing code to me [here](https://github.com/TrevorSLong/School-Safe-Discord-Bot) or **donating** to help fund development and hosting costs [here](https://www.paypal.com/donate?hosted_button_id=RBYUJ5M6QSB52)",inline=False)

    await channel.send(embed=embed)

##############Changes bot status (working)###########################################################################################
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Math Class"))
    channel = bot.get_channel(int(BOT_UPDATE_CHANNEL))
    await channel.send(f'School Safe Bot has restarted and has successfully reconnected to Discord!')

##############Public Welcome (working)########################################################################################################
@bot.event
async def on_member_join(member):

###########Sends DM to member who joined############
    await member.create_dm()
    embed = discord.Embed(colour=discord.Colour(0x788dee), url="https://discordapp.com", description=f" Hello **{member.name}**! Welcome to {member.guild}! I'm School Safe Bot, I'm here to help keep the Discord server school appropriate and safe.")

    embed.set_thumbnail(url="https://raw.githubusercontent.com/TrevorSLong/camtheram-discord/main/Screenshots/CSU-Logo.png")
    embed.set_author(name="Cam the Ram", url="https://github.com/TrevorSLong/School-Safe-Discord-Bot", icon_url="https://raw.githubusercontent.com/TrevorSLong/camtheram-discord/main/Screenshots/CSU-Logo.png")

    embed.add_field(name=f"Welcome to **{member.guild}**! ", value=f"Please read through the servers specific rules and agree to them to start chatting, keep in mind that the server you're joining is for school and everything posted in it should be school appropriate.",inline=False)
    embed.add_field(name="A few notes:", value="• This message is **not** editable by your teacher, please read any rules they may have posted\n• Please change your username or nickname to your first and last name\n• Make sure that your profile picture is school appropriate.\n• Please contact your teacher or check the rules page to find any additional or corrections to these rules. This is an automated message sent by School Safe Bot.",inline=False)
    
    await member.dm_channel.send(embed=embed)

###########Sends welcome message in update channel###########
    with open("welcomechannels.json", "r") as f:
        guildInfo = json.load(f)
    channel = bot.get_channel(guildInfo[str(member.guild.id)])

 
    welcomemessages = [
        f'➡️ Welcome to class **{member.name}**!',
        f'➡️ Happy to have you **{member.name}**',
        f'➡️ So excited to have you in class **{member.name}**',
        ]
    randomwelcome = random.choice(welcomemessages)
    await channel.send(randomwelcome)
    
    with open("adminchannels.json", "r") as f:
        guildInfo = json.load(f)
    channel = bot.get_channel(guildInfo[str(member.guild.id)])
    
    await channel.send(f'School Safe Bot successfully welcomed **{member.name}** to class.')

##############Public Leave message (working)###########################################################################################
@bot.event
async def on_member_remove(member):
    
    with open("welcomechannels.json", "r") as f:
        guildInfo = json.load(f)
    channel = bot.get_channel(guildInfo[str(member.guild.id)])
    
    await channel.send(f'Goodbye **{member.name}** ☹️')
    
    with open("adminchannels.json", "r") as f:
        guildInfo = json.load(f)
    channel = bot.get_channel(guildInfo[str(member.guild.id)])
    
    await channel.send(f'School Safe Bot detected that **{member.name}** left **{member.guild}** and sent a goodbye message in the update channel.')

############# Detect role changes ##############################################################################
@bot.event
async def on_member_update(before, after):

    if len(before.roles) < len(after.roles):
        # The user has gained a new role, so lets find out which one
        newRole = next(role for role in after.roles if role not in before.roles)

        with open("adminchannels.json", "r") as f:
            guildInfo = json.load(f)
        channel = bot.get_channel(guildInfo[str(before.guild.id)])

        await channel.send(f'Member **{before.name}** has gained the role of **{newRole.name}**.')

    if len(after.roles) < len(before.roles):
        # The user has gained a new role, so lets find out which one
        newRole = next(role for role in before.roles if role not in after.roles)

        with open("adminchannels.json", "r") as f:
            guildInfo = json.load(f)
        channel = bot.get_channel(guildInfo[str(before.guild.id)])

        await channel.send(f'Member **{before.name}** has lost the role of **{newRole.name}**.')

############## On Message Event ###########################################################################################
@bot.event
async def on_message(message):

    if message.author == bot.user: return
    if message.author.bot: return
############## Delete mostly capital message #############################
    if len([l for l in message.clean_content if l.isupper()]) > len([l for l in message.clean_content if l.islower()]):

        await message.delete()
        await message.author.send(f"Hello **{message.author}**, the message you sent in **{message.guild}** was deleted because you used excessive capital letters. Please resend using normal capitalization.\nMessage:\n *`{message.clean_content}`*")

        with open("adminchannels.json", "r") as f:
            guildInfo = json.load(f)
        channel = bot.get_channel(guildInfo[str(message.guild.id)])
    
        await channel.send(f'School Safe Bot successfully deleted a message with excessive capital letters sent by **{message.author}** \nMessage:\n*`{message.clean_content}`*\nIf this should not have been filtered out please contact Cam the Rams developers or open an issue on GitHub.')

############## Respond to "cam" #############################
    if message.content == "hello":
        await message.channel.send("Hello!")

    await bot.process_commands(message) # INCLUDES THE COMMANDS FOR THE BOT. WITHOUT THIS LINE, YOU CANNOT TRIGGER YOUR COMMANDS.

############## Delete swear word #############################
    msg = message.content
    for word in badwords:
        if word in msg:
            await message.delete()
            await message.author.send(f"Hello **{message.author}**, the message you sent in **{message.guild}** was deleted because you used a swear word. Please resend using appropriate language if needed.\nMessage:\n *`{message.clean_content}`*")

            with open("adminchannels.json", "r") as f:
                guildInfo = json.load(f)
            channel = bot.get_channel(guildInfo[str(message.guild.id)])
    
            await channel.send(f'Cam the Ram successfully deleted a message with a swear word in it sent by **{message.author}** \nMessage:\n*`{message.clean_content}`*\nIf this should not have been filtered out please contact Cam the Rams developers or open an issue on GitHub.')

###########################################################################################################################
#############################################Slash Commands (/)############################################################
###########################################################################################################################

##############Reponds to /ping (working)########################################################################################################
@slash.slash(
	description="Responds with Pong and the bots server latency", 	# ADDS THIS VALUE TO THE $HELP PING MESSAGE.
)
async def ping(ctx:SlashContext):
	await ctx.send(f'🏓 Pong! {round(bot.latency * 1000)}ms') # SENDS A MESSAGE TO THE CHANNEL USING THE CONTEXT OBJECT.

##############Reponds to /donate (working)########################################################################################################
@slash.slash(
	description="Brings up information on how to donate towards School Safe Bots development", 	 
)
async def donate(ctx:SlashContext):
    embed = discord.Embed(colour=discord.Colour(0x788dee), url="https://discordapp.com", description=f" Hello **{ctx.author}**, Thank you for your interest in donating! Your donation will help with the cost of hosting and developing me for servers like **{ctx.guild}**!")

    embed.set_thumbnail(url="https://raw.githubusercontent.com/TrevorSLong/CamTheRam-Discord/main/Screenshots/DonateQRCode.png")
    embed.set_author(name="Cam the Ram", url="https://top.gg/bot/827681932660965377", icon_url="https://raw.githubusercontent.com/TrevorSLong/camtheram-discord/main/Screenshots/CSU-Logo.png")

    embed.add_field(name="Help support my growth", value="I was made by two full time students, if you enjoy having me around please consider **supporting my development** by contributing code to me [here](https://github.com/TrevorSLong/School-Safe-Bot) or **donating** to help fund development and hosting costs [here](https://www.paypal.com/donate?hosted_button_id=RBYUJ5M6QSB52)")

    await ctx.send(embed=embed)

##############Server count command (working)###########################################################################################
@slash.slash(
    description="Lists the number of servers Cam the Ram is active in",
)
async def servercount(ctx:SlashContext):
    await ctx.send("I'm currently active in " + str(len(bot.guilds)) + " servers!")

##############Anouncement command (working)###########################################################################################
@slash.slash(
    description="Sends an announcement to either the updates channel or to any channel ID.",
    options=[
        create_option(
            name="message",
            description="Type the message you want to send in the announcement",
            option_type=3,
            required=True
        ),
        create_option(
            name="channelid",
            description="Choose the channel the announcement will be sent to.",
            option_type=7,
            required=True,
        )
    ])
@has_permissions(manage_guild=True)
async def announce(ctx:SlashContext, message, channelid):

    embed = discord.Embed(title="Announcement",description=message,color=0x9208ea)
    embed.set_footer(text=f'-This message was sent by School Safe Bot on behalf of {ctx.author}.')
    channel = channelid
    await channel.send(embed=embed)
    await ctx.send(f"Announcement sent to {channelid}!")

    with open("adminchannels.json", "r") as f:
        guildInfo = json.load(f)
    channel = bot.get_channel(guildInfo[str(ctx.guild_id)])
    await channel.send(f"**{ctx.author}** sent an announcement to **{channelid}**!")

@announce.error
async def announce_error(ctx, error):
    if isinstance(error, MissingPermissions):
         await ctx.send(f'Sorry **{ctx.author}**, you need the permission `Manage Server` to make announcements.')

##############Kick command (working)###########################################################################################
@slash.slash(
            description="Kicks a member of the server.",
            options=[
        create_option(
            name="member",
            description="Select the member you would like to kick",
            option_type=6,
            required=True
        ),
        create_option(
            name="reason",
            description="Please type a reason for kicking the member (**they will be sent this reason**)",
            option_type=3,
            required=True,
        )
    ])
@has_permissions(kick_members=True)
async def kick(ctx:SlashContext, member, reason):

    with open("adminchannels.json", "r") as f:
        guildInfo = json.load(f)
    channel = bot.get_channel(guildInfo[str(ctx.guild_id)])

    await member.send(f'Hello **{member}**, you have been kicked from **{ctx.guild}** for **{reason}**. This message has been automatically sent by School Safe Bot. Please contact the teacher of **{ctx.guild}** for questions or concerns')
    await ctx.send(f"Success, **{member}** has been kicked from **{ctx.guild}**.")
    await channel.send(f"**{member}** has been kicked for **{reason}** by **{ctx.author}**.")
    await member.kick(reason=reason)

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send(f'Sorry **{ctx.author}**, you do not have permission to kick members.')

##############Ban command (working)###########################################################################################
@slash.slash(
            description="Bans a member of the server.",
            options=[
        create_option(
            name="member",
            description="Select the member you would like to ban",
            option_type=6,
            required=True
        ),
        create_option(
            name="reason",
            description="Please type a reason for banning the member (**they will be sent this reason**)",
            option_type=3,
            required=True,
        )
    ]
            )
@has_permissions(ban_members=True)
async def ban(ctx:SlashContext, member, reason):   
    
    with open("adminchannels.json", "r") as f:
        guildInfo = json.load(f)
    channel = bot.get_channel(guildInfo[str(ctx.guild_id)])

    await member.send(f'Hello **{member}**, you have been banned from **{ctx.guild}** for **{reason}**. This message has been automatically sent by School Safe Bot. Please contact the teacher of **{ctx.guild}** for questions or concerns')
    
    await channel.send(f"**{member}** has been banned for **{reason}** by **{ctx.author}**.")
    await ctx.send(f"Success, Banned **{member}** for **{reason}**.")
    await member.ban(reason=reason)

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send(f'Sorry **{ctx.author}**, you do not have permission to ban members.')

##############Unban command (working)###########################################################################################
@slash.slash(
    description="Unbans a member of the server.",
            options=[
        create_option(
            name="member1234",
            description="Select the member you would like to unban in the format member#1234.",
            option_type=3,
            required=True
        )
        ]
)
@has_permissions(ban_members=True)
@guild_only()
async def unban(ctx:SlashContext, member1234):
  user = member1234
  banned_users = await ctx.guild.bans()
  member_name, member_discriminator = user.split('#')
  for ban_entry in banned_users:
    user = ban_entry.user
  
  if (user.name, user.discriminator) == (member_name, member_discriminator):
    await ctx.guild.unban(user)

    with open("adminchannels.json", "r") as f:
        guildInfo = json.load(f)
    channel = bot.get_channel(guildInfo[str(ctx.guild_id)])
    
    await channel.send(f"**{user}** has been unbanned by **{ctx.author}**.")
    await ctx.send(f"**{user}** successfully unbanned!")
    await user.send(f'Hello **{user}**, you have been unbanned from **{ctx.guild}**. This message has been automatically sent by School Safe Bot. Please contact the teacher of **{ctx.guild}** for questions or concerns')

@unban.error
async def unban_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send(f'Sorry **{ctx.author}**, you do not have permission to unban members.')

##############Temporary Ban command (working)###########################################################################################               
@slash.slash(
            description="Bans a member of the server for a number of days.",
            options=[
        create_option(
            name="member",
            description="Select the member you would like to temporary ban",
            option_type=6,
            required=True
        ),
        create_option(
            name="reason",
            description="Please type a reason for temporary banning the member (**they will be sent this reason**)",
            option_type=3,
            required=True,
        ),
        create_option(
            name="duration",
            description="The number of days the user will be banned for",
            option_type=4,
            required=True
        )
    ]
            )
@has_permissions(ban_members=True)
async def tempban(ctx:SlashContext, member, reason, duration):   
    user = member
    with open("adminchannels.json", "r") as f:
        guildInfo = json.load(f)
    channel = bot.get_channel(guildInfo[str(ctx.guild_id)])

    await user.send(f'Hello **{user}**, you have been banned from **{ctx.guild}** for **{reason}** for **{duration}** days. This message has been automatically sent by School Safe Bot. Please contact the teacher of **{ctx.guild}** for questions or concerns')
    
    await channel.send(f"**{user}** has been banned for **{reason}** by **{ctx.author}** for **{duration}** days.")
    await user.ban(reason=reason)
    await ctx.send(f"Success, you have banned **{member}** for **{duration}** days.")
    #Unban process below
    await asyncio.sleep(duration*60*60*24)
    await ctx.guild.unban(user)

    await channel.send(f"**{user}** has been unbanned after **{duration}** days.")
    await user.send(f'Hello **{user}**, you have been unbanned from **{ctx.guild}** after **{duration}** days for **{reason}**. This message has been automatically sent by School Safe Bot. Please contact the teacher of **{ctx.guild}** for questions or concerns')
        
@tempban.error
async def tempban_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send(f'Sorry **{ctx.author}**, you do not have permission to ban members.')

##############Allows for the update channel to be changed (working)##############################################################################
@slash.slash(
            description="Changes the public announcements channel to the channel that you used the command in.",
            options=[
        create_option(
            name="channel",
            description="Select the channel updates will be sent in",
            option_type=7,
            required=True
        )
            ])
@has_permissions(manage_guild=True)
async def updatechannel(ctx:SlashContext, channel):

    with open("welcomechannels.json", "r") as f:
        guildInfo = json.load(f)

    guildInfo[ctx.guild_id] = channel.id #sets channel to send message to as the channel the command was sent to

    with open("welcomechannels.json", "w") as f:
        json.dump(guildInfo, f)
    await ctx.send(f'You have successfully changed the update channel to **{channel}**!')
    
@updatechannel.error
async def updatechannel_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send(f'Sorry **{ctx.author}**, you need the permission `Manage Server` to change the update channel.')

##############Allows for the update channel to be checked (working)##############################################################################
@slash.slash(
            description="Checks the public announcements channel.",
            )
@has_permissions(manage_guild=True)
async def checkupdatechannel(ctx:SlashContext):
    with open("welcomechannels.json", "r") as f:
        guildInfo = json.load(f)
    channel = bot.get_channel(guildInfo[str(ctx.guild_id)])
    await ctx.send(f'The update channel is set to **{channel.name}**')

@checkupdatechannel.error
async def checkupdatechannel_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send(f'Sorry **{ctx.author}**, you need the permission `Manage Server` to check the update channel.')
        
##############Allows for the admin channel to be changed (working)##############################################################################
@slash.slash(
            description="Changes the admin announcements channel to the channel that you used the command in.",
            options=[
        create_option(
            name="channel",
            description="Select the channel admin updates will be sent in",
            option_type=7,
            required=True
        )
            ]
            )
@has_permissions(manage_guild=True)
async def adminchannel(ctx:SlashContext, channel):
    with open("adminchannels.json", "r") as f:
        guildInfo = json.load(f)

    guildInfo[ctx.guild_id] = channel.id #sets channel to send message to as the channel the command was sent to

    with open("adminchannels.json", "w") as f:
        json.dump(guildInfo, f)
    await ctx.send(f'You have successfully changed the admin channel to **{channel}**!')

@adminchannel.error
async def adminchannel_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send(f'Sorry **{ctx.author}**, you need the permission `Manage Server` to change the admin channel.')

##############Allows for the admin channel to be checked (working)##############################################################################
@slash.slash(
            description="Checks the admin update channel.",
            )
@has_permissions(manage_guild=True)
async def checkadminchannel(ctx:SlashContext):
    with open("adminchannels.json", "r") as f:
        guildInfo = json.load(f)
    channel = bot.get_channel(guildInfo[str(ctx.guild_id)])
    await ctx.send(f'The admin channel is set to **{channel.name}**')

@checkadminchannel.error
async def checkadminchannel_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send(f'Sorry **{ctx.author}**, you need the permission `Manage Server` to check the admin channel.')

bot.run(TOKEN)