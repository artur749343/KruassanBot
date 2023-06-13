import discord
from discord.guild import Guild
from discord.channel import CategoryChannel, VoiceChannel, TextChannel
from discord.message import Message
def get_client(myclient: discord.Client): #get discord client
   global client
   client=myclient

######## Button class
class MyButton(discord.ui.Button):
  def __init__(self, *arg):
    if arg[1]=="blue": color=discord.ButtonStyle.blurple
    elif arg[1]=="red": color=discord.ButtonStyle.red
    elif arg[1]=="green": color=discord.ButtonStyle.green
    else: color=discord.ButtonStyle.gray
    self.send=arg[2]
    super().__init__(style=color,label=arg[0])
  async def callback(self, interaction: discord.Interaction):
      await interaction.response.send_message(self.send)

class View(discord.ui.View):
  def __init__(self, *arg, timeout=180):
    super().__init__(timeout=timeout)
    self.add_item(MyButton(*arg))
########

dir_fun={"print": lambda x, y: x.send(str(y)),
         "button": lambda x, name, color, send: x.send(view=View(str(name), color, str(send))),
         "clear": lambda x, n: x.purge(limit=n),
         "newfunc": lambda x, a, b: x.send(str(a+b))
}


def get_pos(tguild, tcategory, tchannel, tmember): #get chat id
   global guild, channel, category, member
   guild, channel, category, member=tguild, tchannel, tcategory, tmember


def this(t:tuple): #this like in C
   t=t[1:]
   if t[0]=="guild": n=guild
   elif t[0]=="channel": n=channel
   elif t[0]=="categore": n=category
   elif t[0]=="user": n=member
   for x in t[1:]:
      if x=="parent":
         if type(n)==Guild:
            return "Guilds havn`t parents"
         elif type(n)==CategoryChannel:
            n=n.guild
         elif type(n)==TextChannel:
            n=n.category
         elif type(n)==discord.Member:
            n=n.guild
      elif x[:8]=="channels" and type(n)==CategoryChannel:
         n=n.text_channels[int(x[8:])]
      elif x[:10]=="categories" and type(n)==Guild:
         n=n.categories[int(x[10:])]
      elif x[:7]=="members" and type(n)==Guild:
         n=n.members[int(x[7:])]
   if type(n) in [CategoryChannel, TextChannel, discord.Member, Guild]:
      return n