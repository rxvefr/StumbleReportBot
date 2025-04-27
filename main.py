import os
import discord
import re
import datetime
# import tasks
from keep_alive import keep_alive 
# from os import system

from discord.ext import commands

from replit import db


#await bot.change_presence(activity=discord.Game("DM to report a bug"))

client = discord.Client()
yes_word = ["yes"]

client = commands.Bot(case_insensitive=True, command_prefix =  '/')

regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)



@client.event
async def on_ready():
  await client.change_presence(activity=discord.Game('Dm me to report a bug!'))
  print('We have logged in as {0.user}'.format(client))

#@tasks.loop(seconds=10)
#async def change_status():
 # await client.change_presence(activity=discord.Game('Dm me to report a bug!'))



  @client.event
  async def on_message(message):
    if message.content.startswith('/report'):
      
      if message.author == client.user or not isinstance(message.channel, discord.channel.DMChannel):
        return

      channel = message.channel

      def isCorrectUser(m):
        return m.author == message.author and m.channel == channel

      await channel.send('Do you want to report a bug? (Respond with **YES** to start the bug report). \n To cancel report at any point type /cancel. \n Remember to check <#875653341034741760> Since the solution might be there \nFalse reports might result in a ban')

      report_bug_answer = await client.wait_for('message', check=isCorrectUser)

      if report_bug_answer.content.lower() != 'yes':
        await channel.send('OK. You do not want to report a bug this time. Aborting!')
        return;
      
      await channel.send('First tell me your username in Stumble Guys')

      username = await client.wait_for('message', check=isCorrectUser)

      if await check_for_abort(username.content, channel):
        return;

      await channel.send('What device are you using? (iPhone 8, iPhone X, Galaxy S9, OnePlus 8T etc..)')

      device = await client.wait_for('message', check=isCorrectUser)

      if await check_for_abort(device.content, channel):
        return;

      await channel.send('What OS version are you running on your device? (iOS 11, Nougat, Android 10, etc...)')

      deviceos = await client.wait_for('message', check=isCorrectUser)

      if await check_for_abort(deviceos.content, channel):
        return;

      await channel.send('Thanks! Next describe the problem for me')

      problem = await client.wait_for('message', check=isCorrectUser)

      if await check_for_abort(problem.content, channel):
        return;

      await channel.send("Additional info URL or text eg. Screenshot of Unity debugger, video or screenshot that could help us. If it's a video upload the video to YouTube first then paste link here. If you don't have just reply no")

      additionalinfo = await client.wait_for('message', check=isCorrectUser)

      if await check_for_abort(additionalinfo.content, channel):
        return;

      was_proper_url = True

      has_attachment = True

      if re.match(regex, additionalinfo.content) is None:
        was_proper_url = False

      if not additionalinfo.attachments:
        has_attachment = False

      #if additionalinfo.startswith('http')

      await channel.send('Thank you, I will now forward your bug-report! You might get an answer in your DM by our moderators on direcly on the <#766696275721846815> -channel')

      bug_report_channel = client.get_channel(766696275721846815) #channel id?

      await testEmbed(bug_report_channel, username, problem, device, deviceos, additionalinfo, was_proper_url, has_attachment)
      
async def check_for_abort(message_content, channel):
  if message_content.startswith('/cancel'):
    await channel.send('Aborting!')
    return True
  elif message_content.startswith('/report'):
    return True
  else:
    return False

@client.command()
async def testEmbed(channel, username, problem, device, deviceos, additionalinfo, was_proper_url, has_attachment):
    embed = discord.Embed(title="Bug report") 
    embed.set_thumbnail(url=username.author.avatar)
    embed.set_author(name=username.author.display_name + ' (' + str(username.author.id) + ')'), icon_url=str(username.author.avatar))
    embed.add_field(name="**Stumble name**", value=username.content, inline=False)
    embed.add_field(name="**Bug Description**", value=problem.content, inline=False)
    embed.add_field(name="**Device**", value=device.content, inline=False)
    embed.add_field(name="**Device OS**", value=deviceos.content, inline=False)
    
    #if was_proper_url:
    #  embed.set_image(url=additionalinfo.content)
    #else:
    #  embed.add_field(name="**Additional info**", value=additionalinfo.content, #inline=False)

    if has_attachment:
      embed.set_image(url=additionalinfo.attachments[0])
    elif was_proper_url:
      embed.set_image(url=additionalinfo.content)
    else:
      embed.add_field(name="**Additional info**", value=additionalinfo.content,inline=False)

    embed.set_footer(text="React with  👍  or  👎  if you have or have not encountered this") #Antti added
    embed.timestamp = datetime.datetime.utcnow()  
    message = await channel.send(embed=embed)
    await message.add_reaction("👍") #Antti added
    await message.add_reaction("👎") #Antti added
    #await channel.send(embed=embed)   

@client.event
async def on_message(message):
    channel_id = 766696275721846815
    if message.channel.id == channel_id:
        await message.publish()
    await client.process_commands(message)

keep_alive() #Antti added
try:
    client.run(os.getenv('TOKEN'))
except discord.errors.HTTPException:
    print("\n\n\nBLOCKED BY RATE LIMITS\nRESTARTING NOW\n\n\n")
    system("python restarter.py")
    system('kill 1')  
