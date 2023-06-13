import discord, discofunc, discosculk, json, os
from discord import app_commands
from discord.ui import button, TextInput



class CodeArg(discord.ui.Modal, title="Кодим"):
    def __init__(self, name, run, public, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name, self.run=name, run
        if public=="доступ всем":
            self.public="all"
        elif public=="только с моим разрешением":
            self.public=[user]
        self.add_item(TextInput(label="Код", required=True, placeholder='print(this.channel, "Hello, World!")', style=discord.TextStyle.paragraph))
    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message("код удачно изменен")
        with open("\\".join(str(os.path.abspath(__file__)).split("\\")[:-2])+f"\\data\\discofiles\\{self.name}.txt", "w") as f:
            f.write(self.children[0].value)
        if self.run=="сохранить и запустить":
            discofunc.get_pos(interaction.guild, interaction.channel.category, interaction.channel, interaction.user)
            await discosculk.DiscoSculk(self.name)
        load=json.load(open("\\".join(str(os.path.abspath(__file__)).split("\\")[:-2])+"\\data\\discofiles\\files.json", "r", encoding="utf-8"))
        load.update({self.name: self.public})
        json.dump(load, open("\\".join(str(os.path.abspath(__file__)).split("\\")[:-2])+"\\data\\discofiles\\files.json", "w", encoding="utf-8"))


class Code(discord.ui.Modal, title="Кодим"):
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name=name
        self.add_item(TextInput(label="Код", required=True, placeholder='print(this.channel, "Hello, World!")', style=discord.TextStyle.paragraph, default=open("\\".join(str(os.path.abspath(__file__)).split("\\")[:-2])+f"\\data\\discofiles\\{self.name}.txt", "r").read()))
    async def on_submit(self, interaction: discord.Interaction):
        with open("\\".join(str(os.path.abspath(__file__)).split("\\")[:-2])+f"\\data\\discofiles\\{self.name}.txt", "w") as f:
            f.write(self.children[0].value)

class Edit(app_commands.Group):
    @app_commands.command(name="имя")
    async def n(self, interaction: discord.Interaction, файл: str, новое_имя: str):
      load=json.load(open("\\".join(str(os.path.abspath(__file__)).split("\\")[:-2])+"\\data\\discofiles\\files.json", "r", encoding="utf-8"))
      if load[файл]=="all" or interaction.user.id in load[файл]:
        os.rename("\\".join(str(os.path.abspath(__file__)).split("\\")[:-2])+f"\\data\\discofiles\\{файл}.txt", "\\".join(str(os.path.abspath(__file__)).split("\\")[:-2])+f"\\data\\discofiles\\{новое_имя}.txt")
        load[новое_имя] = load.pop(файл)
        json.dump(load, open("\\".join(str(os.path.abspath(__file__)).split("\\")[:-2])+"\\data\\discofiles\\files.json", "w", encoding="utf-8"))
        await interaction.response.send_message("имя удачно изменено")
      else: await interaction.response.send_message("файла не существует или у вас к нему нету доступа")
    
    @app_commands.choices(доступ=[app_commands.Choice(name=x, value=x) for x in ["доступ всем", "только с моим разрешением"]])
    @app_commands.command(name="доступ")
    async def public(self, interaction: discord.Interaction, файл: str, доступ: str):
      load=json.load(open("\\".join(str(os.path.abspath(__file__)).split("\\")[:-2])+"\\data\\discofiles\\files.json", "r", encoding="utf-8"))
      if load[файл]=="all" or interaction.user.id in load[файл]:
        if доступ=="доступ всем": load[файл]="all"
        else: load[файл]=[interaction.user.id]
        json.dump(load, open("\\".join(str(os.path.abspath(__file__)).split("\\")[:-2])+"\\data\\discofiles\\files.json", "w", encoding="utf-8"))
        await interaction.response.send_message("доступ удачно изменен")
      else:
        await interaction.response.send_message("файла не существует или у вас к нему нету доступа")
    
    @app_commands.command(name="код")
    async def code(self, interaction: discord.Interaction, файл: str):
        await interaction.response.send_modal(Code(файл))