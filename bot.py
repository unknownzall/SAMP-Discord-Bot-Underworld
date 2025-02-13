
# Discord bot for SAMP servers with simple register etc.
# All open Source!
# Credits: Muhammad Putra/unknownzall
# Do not remove the credits!

# Note:
# Bot will work if you settings on your mysql.py depends on your gamemode.
# Maybe need some setup again for make it work on another gamemode like database etc.

# If you need anything or some help, contact me on discord : rakannn51

import discord, random
from discord.ext import commands
from discord import ui
from discord.ui import button
from handle.mysql import *

try:
  with open('config.json', 'r') as file:
    config = json.load(file)
except FileNotFoundError:
  config = {}
  
#------------------------------#
TOKEN = config['TOKEN']
PREFIX = config['PREFIX']
NAME = config['TAG']
ROLE_ID = config['ROLE_ID']
THUMBNAIL = config['THUMBNAIL']
IMAGE = config['IMAGE']
ICON = config['ICON']
KARCIS = config['KARCIS_IMAGE']
WARNA = 0xFFd000
#------------------------------#

intents = discord.Intents().all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents)
    
@bot.event
async def on_ready():
    bot.add_view(Buttons())
    bot.add_view(ButtonsAdmin())
    await bot.tree.sync()
    await bot.change_presence(activity=discord.Game("Underworld User Control Panel"))
    print(f'Bot Online Logged in as {bot.user.name}')
    is_connected = check_mysql_connection()
    if is_connected:
      print("MySQL has successfully connected")
    else:
      print("Mysql Tidak Connect")

def randomOTP():
    otp = random.randint(1000, 9999)
    return otp
    
class Buttons(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)

  @discord.ui.button(label="Register", custom_id="register_id", style=discord.ButtonStyle.red, emoji="📮")
  async def register(self, interaction: discord.Interaction, button: discord.Button):
    user_ucp = check_id(interaction.user.id)
    if user_ucp is not None:
      await interaction.response.send_message(f"Anda sudah mendaftar sebelumnya dengan nama UCP **{user_ucp['UCP']}**.", ephemeral=True)
    else:
      await interaction.response.send_modal(ModalApplicationForm(interaction.user.id))

  @discord.ui.button(label="Reverif", custom_id="reverif_id", style=discord.ButtonStyle.green, emoji="📬")
  async def reverif(self, interaction: discord.Interaction, button: discord.Button):
    user_ucpp = check_id(interaction.user.id)
    if user_ucpp is None:
      await interaction.response.send_message(f"Anda belum pernah membuat user control panel, silahkan buat terlebih dahulu!", ephemeral=True)
    else:
      await interaction.response.send_message(f"Kamu berhasil melakukan reverifikasi, selamat datang kembali!", ephemeral=True)
      roles = interaction.guild.get_role(ROLE_ID)
      interaction.user.edit(nick=f'{user_ucpp["UCP"]}')
      if roles:
        await interaction.user.add_roles(roles)
        
class ButtonsAdmin(discord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)

  @discord.ui.button(label="Character Story", custom_id="char_id", style=discord.ButtonStyle.grey, emoji="📮")
  async def adminpanel1(self, interaction: discord.Interaction, button: discord.Button):
      await interaction.response.send_modal(ModalNgentot(interaction.user.id))

  @discord.ui.button(label="Redeem Code", custom_id="redeem_id", style=discord.ButtonStyle.grey, emoji="📮")
  async def adminpanel2(self, interaction: discord.Interaction, button: discord.Button):
      await interaction.response.send_modal(ModalNgentot1(interaction.user.id))

class ModalNgentot1(discord.ui.Modal, title='Redeem Code'):
  def __init__(self, user_id, **kwargs):
    super().__init__(**kwargs)
    self.user_id = user_id

  CodeNya = ui.TextInput(label='Code', style=discord.TextStyle.short, placeholder="Example: 73821")
  VipType = ui.TextInput(label='Vip Type', style=discord.TextStyle.short, placeholder="Example: 1-4")
  VipTime = ui.TextInput(label='Vip Time', style=discord.TextStyle.short, placeholder="Example: 30-60 Days")
  Gold = ui.TextInput(label='Gold', style=discord.TextStyle.short, placeholder="Example: 100")
  async def on_submit(self, interaction: discord.Interaction):
    code = self.CodeNya.value
    vip = self.VipType.value
    viptime = self.VipTime.value
    gold = self.Gold.value
    vouchercode(code, vip, viptime, gold)
    await interaction.response.send_message(f"You successfully make redeem code with code {code} and gold amount {gold}", ephemeral=True)
    return

class ModalNgentot(discord.ui.Modal, title='Character Story'):
  def __init__(self, user_id, **kwargs):
    super().__init__(**kwargs)
    self.user_id = user_id

  NamaCharacter = ui.TextInput(label='Character Name', style=discord.TextStyle.short, placeholder="Example: Daevion_Bennet")
  async def on_submit(self, interaction: discord.Interaction):
    namayangdimasukin = self.NamaCharacter.value
    namayangdimasukin = self.NamaCharacter.value
    characterstory(namayangdimasukin)
    await interaction.response.send_message(f"You successfully actived character story for player with name `{namayangdimasukin}`", ephemeral=True)
    return

class ModalApplicationForm(discord.ui.Modal, title='Register'):
  def __init__(self, user_id, **kwargs):
    super().__init__(**kwargs)
    self.user_id = user_id

  NamaUcp = ui.TextInput(label='User Control Panel', style=discord.TextStyle.short, placeholder="Example: Reno")
  NamaGmail = ui.TextInput(label='Gmail ( must be valid gmail )', style=discord.TextStyle.short, placeholder="Example: test@gmail.com")
  NoWa = ui.TextInput(label='Whatsapp Number ( must be valid number )', style=discord.TextStyle.short, placeholder="Example: 081921129111")
  async def on_submit(self, interaction: discord.Interaction):
    nama = self.NamaUcp.value
    Gmail = self.NamaGmail.value
    Phone = self.NoWa.value
    discord_id = self.user_id

    global NAME, ROLE_ID
    
    checkUCP = ucp_check(nama)
    if checkUCP:
      await interaction.response.send_message(f"Nama UCP **{checkUCP['username']}** sudah digunakan. Silakan pilih nama UCP lain.", ephemeral=True)
    else:
      await interaction.user.edit(nick=f'{nama}')
      role = interaction.guild.get_role(ROLE_ID)
      if role:
        await interaction.user.add_roles(role)
        
      nama = self.NamaUcp.value
      Gmail = self.NamaGmail.value
      Phone = self.NoWa.value
      discord_id = self.user_id
      code = randomOTP()
      await interaction.response.send_message("Your User Control Panel successfully verified, please check the message from bot!", ephemeral=True)
      register_user(nama, code, discord_id, Gmail, Phone)
      try:
        user = await bot.fetch_user(discord_id)
        embed = discord.Embed(title="User Control Panel - Registration", color=WARNA, description=f"""
Selamat User Control Panel kamu di Validity Roleplay berhasil didaftarkan Gunakan User Control Panel untuk login dibawah untuk login ke dalam server!
        """)
        embed.add_field(name="", value=f"```User Control Panel: {nama}\nVerify Code: {code}\nEmail: {Gmail}\nWhatsapp Number: {Phone}```\nKamu tidak diperbolehkan untuk memberitahu data diatas ini kepada siapapun (bahkan staff sekalipun)")
        embed.set_footer(text="Validity Roleplay: User Control Panel", icon_url=ICON)
        await user.send(embed=embed)
      except discord.Forbidden:
        await interaction.response.send_message("Pastikan kamu sudah mengaktifkan dm anggota server.", ephemeral=True)
        return

@bot.tree.command(name="adminpanel")
@commands.has_permissions(administrator=True)
async def adminpanel(interaction: discord.Interaction):
  if not interaction.user.guild_permissions.administrator:
    return await interaction.response.send_message("Anda tidak bisa menggunakan command ini karena anda bukan administrator.", ephemeral=True)
    
  embed = discord.Embed(title='',color=WARNA, description="""### **__Administrator Panel__**
Channel ini merupakan channel untuk mengatur akun dari in game seseorang didalam server Validity Roleplay, sebelum mengatur akun dari in game seseorang pastikan kamu mengetahui kegunaan beberapa button yang tersedia.
  """)
  embed.add_field(name="Character Story Button", value="""
> Gunakan button ini apabila kamu ingin mengatur character story dari seseorang menjadi aktif!
  """)
  embed.add_field(name="Redeem Code Button", value="""
> Gunakan button ini apabila kamu ingin membuat redeem code untuk seseorang yang sudah donate atau booster ke server!
  """)
  embed.set_footer(text="Validity Roleplay: Admin Control Panel", icon_url=ICON)
  await interaction.response.send_message(embed=embed, view=ButtonsAdmin())

@bot.tree.command(name="setregister")
@commands.has_permissions(administrator=True)
async def setregister(interaction: discord.Interaction):
  if not interaction.user.guild_permissions.administrator:
    return await interaction.response.send_message("Anda tidak bisa menggunakan command ini karena anda bukan administrator.", ephemeral=True)
    
  embed = discord.Embed(title='',color=WARNA, description="""### **__Registration Panel__**
Channel ini merupakan channel yang digunakan untuk mengatur atau registrasi akun kamu agar bisa memasuki in game dari server Validity Roleplay, sebelum membuat User Control panel pastikan kamu mengetahui kegunaan beberapa button yang tersedia.
  """)
  embed.add_field(name="Register Button", value="""
> Gunakan button ini apabila kamu ingin melakukan registrasi akun in game kamu, pastikan kamu sudah melihat tutorial yang diberi Validity Roleplay dan rules-rules yang sudah diberikan server!
  """)
  embed.add_field(name="Reverif Button", value="""
> Gunakan button ini apabila kamu sudah registrasi ucp dan kamu keluar dari discord Validity Roleplay lalu ketika memasuki nya kamu tidak akan memiliki role gunakan button ini untuk mendapatkan role kembali!
  """)
  embed.set_image(url=KARCIS)
  embed.set_footer(text="Validity Roleplay: User Control Panel", icon_url=ICON)
  await interaction.response.send_message(embed=embed, view=Buttons())

@bot.command(name="ip")
async def ip(ctx):
     await ctx.send("gta-validity.my.id:3023\n45.139.226.53:3023\nKalian bisa menggunakan ip mana pun karena itu sama, apabila kalian merasa laging dalam in game kalian bisa menggunakan ip angka.", ephemeral=True)
    
bot.run(TOKEN)