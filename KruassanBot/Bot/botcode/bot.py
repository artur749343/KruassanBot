import discord, discosculk, json, os, typing, discofunc
from discord import app_commands
from discord.ext import commands
from classes import *
intent = discord.Intents.all()
intent.message_content = True
discord.member = True
client = discord.Client(intents=intent)
tree = app_commands.CommandTree(client)
discofunc.get_client(client)
botinfo=json.load(open("\\".join(str(os.path.abspath(__file__)).split("\\")[:-3])+"\\botinfo.json", "r", encoding="utf-8"))
TESTGUILD=botinfo["Guild"] #guild where bot working

@client.event
async def on_ready():
    tree.add_command(Edit(name="редактировать", description="редактировать файл"))
    tree.copy_global_to(guild=discord.Object(id=TESTGUILD))
    await tree.sync(guild=discord.Object(id=TESTGUILD))


@app_commands.choices(доступ=[app_commands.Choice(name=x, value=x) for x in ["доступ всем", "только с моим разрешением"]], запуск=[app_commands.Choice(name=x, value=x) for x in ["сохранить", "сохранить и запустить"]])
@tree.command(name="создать", description="создай код и стань программистом", guild=discord.Object(id=TESTGUILD))
async def self(interaction: discord.Interaction, имя:str, доступ: str, запуск: str):
  await interaction.response.send_modal(CodeArg(имя, запуск, доступ, interaction.user.id))


@tree.command(name="запуск", description="запустить код написаный кем то", guild=discord.Object(id=TESTGUILD))
async def self(interaction: discord.Interaction, файл:str):
  файлы=json.load(open("\\".join(str(os.path.abspath(__file__)).split("\\")[:-2])+"\\data\\discofiles\\files.json", "r", encoding="utf-8"))[файл]
  if файлы=="all" or interaction.user.id in файлы:
    discofunc.get_pos(interaction.guild, interaction.channel.category, interaction.channel, interaction.user)
    await discosculk.DiscoSculk(файл)
  else:
    await interaction.response.send_message("файла не существует или у вас к нему нету доступа")

@tree.command(name="добавить", description="добавить другу возможность смотреть ваш файл", guild=discord.Object(id=TESTGUILD))
async def self(interaction: discord.Interaction, файл: str,друг:discord.Member):
  load=json.load(open("\\".join(str(os.path.abspath(__file__)).split("\\")[:-2])+"\\data\\discofiles\\files.json", "r", encoding="utf-8"))
  if load[файл]!="all":
    load[файл].append(друг.id)
    
    json.dump(load, open("\\".join(str(os.path.abspath(__file__)).split("\\")[:-2])+"\\data\\discofiles\\files.json", "w", encoding="utf-8"))
  else: await interaction.response.send_message("этот файл являеться публичным")
  

@tree.command(name="просмотреть", description="просмотреть доступные вам файлы", guild=discord.Object(id=TESTGUILD))
async def self(interaction: discord.Interaction):
  load=json.load(open("\\".join(str(os.path.abspath(__file__)).split("\\")[:-2])+"\\data\\discofiles\\files.json", "r", encoding="utf-8"))
  embed=discord.Embed(title="Все вами доступные файлы")
  [embed.add_field(name=n, value=" ".join([client.get_guild(TESTGUILD).get_member(x).name for x in load[n]]) if load[n]!="all" else "Публичный", inline=False) for n in load]
  await interaction.response.send_message(embed=embed)

client.run(botinfo["token"])