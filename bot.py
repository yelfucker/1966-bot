import discord
from discord.ext import commands
import asyncio
import datetime
import random
import os

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

YETKILI_ROL_ID = 1539306482057875507  # 1 9 6 6 rolü
OZEL_KANAL_ID = 1539313789764374690  # !kaçcm kanalı

def yetkili_mi(ctx):
    rol = ctx.guild.get_role(YETKILI_ROL_ID)
    if rol and rol in ctx.author.roles:
        return True
    if ctx.author.guild_permissions.administrator:
        return True
    return False

def ozel_kanal_mi(ctx):
    return ctx.channel.id == OZEL_KANAL_ID

@bot.event
async def on_ready():
    print(f"{bot.user} aktif - {len(bot.guilds)} sunucu")
    await bot.change_presence(activity=discord.Game("!yardım | 7/24 | 1966"))

# SELAM KARŞILIĞI
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    selamlar = ["sa", "selam", "selamun aleyküm", "selamünaleyküm", "sea", "selamün aleyküm"]
    if any(message.content.lower().startswith(kelime) for kelime in selamlar):
        await message.channel.send(f"Aleyküm selam {message.author.mention}")

    await bot.process_commands(message)

OTOROL_ID = None

@bot.event
async def on_member_join(member):
    global OTOROL_ID
    if OTOROL_ID is None:
        return
    rol = member.guild.get_role(OTOROL_ID)
    if rol:
        await member.add_roles(rol)

# ROL VER
@bot.command(name="rolver")
async def rolver(ctx, member: discord.Member, role: discord.Role):
    if not yetkili_mi(ctx):
        await ctx.send("❌ Yetersiz yetki. Bu komutu kullanmak için `1 9 6 6` rolüne sahip olmalısın.")
        return
    if role >= ctx.guild.me.top_role:
        await ctx.send("❌ Bot bu rolden yüksek yetkide değil.")
        return
    await member.add_roles(role)
    embed = discord.Embed(title="✅ Rol Verildi", color=discord.Color.green())
    embed.add_field(name="Kullanıcı", value=member.mention)
    embed.add_field(name="Rol", value=role.mention)
    embed.add_field(name="Yetkili", value=ctx.author.mention)
    await ctx.send(embed=embed)

# ROL AL
@bot.command(name="rolal")
async def rolal(ctx, member: discord.Member, role: discord.Role):
    if not yetkili_mi(ctx):
        await ctx.send("❌ Yetersiz yetki. Bu komutu kullanmak için `1 9 6 6` rolüne sahip olmalısın.")
        return
    if role >= ctx.guild.me.top_role:
        await ctx.send("❌ Bot bu rolden yüksek yetkide değil.")
        return
    await member.remove_roles(role)
    embed = discord.Embed(title="✅ Rol Alındı", color=discord.Color.orange())
    embed.add_field(name="Kullanıcı", value=member.mention)
    embed.add_field(name="Rol", value=role.mention)
    embed.add_field(name="Yetkili", value=ctx.author.mention)
    await ctx.send(embed=embed)

# OTOROL AYARLA
@bot.command(name="otorol")
async def otorol(ctx, role: discord.Role):
    if not yetkili_mi(ctx):
        await ctx.send("❌ Yetersiz yetki. Bu komutu kullanmak için `1 9 6 6` rolüne sahip olmalısın.")
        return
    global OTOROL_ID
    OTOROL_ID = role.id
    embed = discord.Embed(title="✅ Otorol Ayarlandı", color=discord.Color.green())
    embed.add_field(name="Rol", value=role.mention)
    embed.add_field(name="Durum", value="Yeni katılan üyelere otomatik verilecek.")
    await ctx.send(embed=embed)

# OTOROL KAPAT
@bot.command(name="otorolkapat")
async def otorolkapat(ctx):
    if not yetkili_mi(ctx):
        await ctx.send("❌ Yetersiz yetki. Bu komutu kullanmak için `1 9 6 6` rolüne sahip olmalısın.")
        return
    global OTOROL_ID
    OTOROL_ID = None
    embed = discord.Embed(title="❌ Otorol Kapatıldı", color=discord.Color.red())
    embed.add_field(name="Durum", value="Yeni katılan üyelere artık rol verilmeyecek.")
    await ctx.send(embed=embed)

# BAN
@bot.command(name="ban")
async def ban(ctx, member: discord.Member, *, reason="Sebep belirtilmedi"):
    if not yetkili_mi(ctx):
        await ctx.send("❌ Yetersiz yetki. Bu komutu kullanmak için `1 9 6 6` rolüne sahip olmalısın.")
        return
    await member.ban(reason=reason)
    embed = discord.Embed(title="🔨 Ban", description=f"{member.mention} banlandı.", color=discord.Color.red())
    embed.add_field(name="Sebep", value=reason)
    embed.add_field(name="Yetkili", value=ctx.author.mention)
    await ctx.send(embed=embed)

# UNBAN
@bot.command(name="unban")
async def unban(ctx, user_id: int, *, reason="Sebep belirtilmedi"):
    if not yetkili_mi(ctx):
        await ctx.send("❌ Yetersiz yetki. Bu komutu kullanmak için `1 9 6 6` rolüne sahip olmalısın.")
        return
    user = await bot.fetch_user(user_id)
    await ctx.guild.unban(user, reason=reason)
    embed = discord.Embed(title="🔓 Unban", description=f"{user.mention} ({user_id}) banı kaldırıldı.", color=discord.Color.green())
    embed.add_field(name="Sebep", value=reason)
    embed.add_field(name="Yetkili", value=ctx.author.mention)
    await ctx.send(embed=embed)

# MUTE
@bot.command(name="mute")
async def mute(ctx, member: discord.Member, duration: int, *, reason="Sebep belirtilmedi"):
    if not yetkili_mi(ctx):
        await ctx.send("❌ Yetersiz yetki. Bu komutu kullanmak için `1 9 6 6` rolüne sahip olmalısın.")
        return
    timeout = datetime.timedelta(minutes=duration)
    await member.timeout(timeout, reason=reason)
    embed = discord.Embed(title="🤐 Mute", description=f"{member.mention} mute'lendi.", color=discord.Color.orange())
    embed.add_field(name="Süre", value=f"{duration} dakika")
    embed.add_field(name="Sebep", value=reason)
    embed.add_field(name="Yetkili", value=ctx.author.mention)
    await ctx.send(embed=embed)

# UNMUTE
@bot.command(name="unmute")
async def unmute(ctx, member: discord.Member):
    if not yetkili_mi(ctx):
        await ctx.send("❌ Yetersiz yetki. Bu komutu kullanmak için `1 9 6 6` rolüne sahip olmalısın.")
        return
    await member.timeout(None)
    embed = discord.Embed(title="🔊 Unmute", description=f"{member.mention} mute'i kaldırıldı.", color=discord.Color.green())
    embed.add_field(name="Yetkili", value=ctx.author.mention)
    await ctx.send(embed=embed)

# KICK
@bot.command(name="kick")
async def kick(ctx, member: discord.Member, *, reason="Sebep belirtilmedi"):
    if not yetkili_mi(ctx):
        await ctx.send("❌ Yetersiz yetki. Bu komutu kullanmak için `1 9 6 6` rolüne sahip olmalısın.")
        return
    await member.kick(reason=reason)
    embed = discord.Embed(title="👢 Kick", description=f"{member.mention} kicklendi.", color=discord.Color.orange())
    embed.add_field(name="Sebep", value=reason)
    embed.add_field(name="Yetkili", value=ctx.author.mention)
    await ctx.send(embed=embed)

# TEMİZLE
@bot.command(name="temizle")
async def temizle(ctx, amount: int):
    if not yetkili_mi(ctx):
        await ctx.send("❌ Yetersiz yetki. Bu komutu kullanmak için `1 9 6 6` rolüne sahip olmalısın.")
        return
    if amount > 100:
        amount = 100
    deleted = await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(f"{len(deleted)-1} mesaj silindi.")
    await asyncio.sleep(3)
    await msg.delete()

# KAÇ CM
@bot.command(name="kaçcm")
async def kaccm(ctx):
    if not ozel_kanal_mi(ctx):
        await ctx.send("❌ Bu komut sadece belirlenen kanalda kullanılabilir.")
        return
    uzunluk = random.randint(10, 50)
    embed = discord.Embed(
        title="📏 Kaç CM?",
        description=f"{ctx.author.mention}'in uzunluğu: **{uzunluk} cm**",
        color=discord.Color.purple()
    )
    embed.set_footer(text="Sonuçlar kesinlikle gerçekçidir.")
    await ctx.send(embed=embed)

# SUNUCU BİLGİSİ
@bot.command(name="sunucu")
async def sunucu(ctx):
    if not yetkili_mi(ctx):
        await ctx.send("❌ Yetersiz yetki. Bu komutu kullanmak için `1 9 6 6` rolüne sahip olmalısın.")
        return

    guild = ctx.guild
    embed = discord.Embed(title=f"📊 {guild.name} Sunucu Bilgisi", color=discord.Color.blue())
    embed.add_field(name="👥 Üye Sayısı", value=guild.member_count)
    embed.add_field(name="🚀 Boost Sayısı", value=guild.premium_subscription_count)
    embed.add_field(name="📅 Kuruluş", value=guild.created_at.strftime("%d.%m.%Y"))
    embed.add_field(name="👑 Sahip", value=guild.owner.mention)
    embed.add_field(name="📢 Kanal Sayısı", value=len(guild.channels))
    embed.add_field(name="🎭 Rol Sayısı", value=len(guild.roles))
    embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
    await ctx.send(embed=embed)

# YARDIM
@bot.command(name="yardım")
async def yardim(ctx):
    if not yetkili_mi(ctx):
        await ctx.send("❌ Yetersiz yetki. Bu komutu kullanmak için `1 9 6 6` rolüne sahip olmalısın.")
        return
    embed = discord.Embed(title="📋 Komut Listesi — 1 9 6 6", color=discord.Color.blue())
    embed.add_field(name="!ban @kullanıcı sebep", value="Kullanıcıyı banlar", inline=False)
    embed.add_field(name="!unban kullanıcı_id sebep", value="Banı kaldırır (ID ile)", inline=False)
    embed.add_field(name="!mute @kullanıcı dakika sebep", value="Kullanıcıyı mute'ler", inline=False)
    embed.add_field(name="!unmute @kullanıcı", value="Mute'i kaldırır", inline=False)
    embed.add_field(name="!kick @kullanıcı sebep", value="Kullanıcıyı kickler", inline=False)
    embed.add_field(name="!temizle sayı", value="Mesajları siler (max 100)", inline=False)
    embed.add_field(name="!kaçcm", value="Rastgele uzunluk gösterir (herkes kullanabilir, özel kanal)", inline=False)
    embed.add_field(name="!rolver @kullanıcı @rol", value="Kullanıcıya rol verir", inline=False)
    embed.add_field(name="!rolal @kullanıcı @rol", value="Kullanıcıdan rol alır", inline=False)
    embed.add_field(name="!otorol @rol", value="Yeni katılanlara otomatik rol verir", inline=False)
    embed.add_field(name="!otorolkapat", value="Otorolü kapatır", inline=False)
    embed.add_field(name="!sunucu", value="Sunucu bilgilerini gösterir", inline=False)
    embed.set_footer(text="Tüm komutlar için 1 9 6 6 rolü gerekir (kaçcm hariç)")
    await ctx.send(embed=embed)

# TEST KOMUTU
@bot.command(name="test")
async def test(ctx):
    embed = discord.Embed(title="✅ Bot Çalışıyor", color=discord.Color.green())
    embed.add_field(name="Sunucu", value=ctx.guild.name)
    embed.add_field(name="Kanal", value=ctx.channel.mention)
    embed.add_field(name="Kanal ID", value=ctx.channel.id)
    embed.add_field(name="Yetki", value="1 9 6 6" if yetkili_mi(ctx) else "Yok")
    await ctx.send(embed=embed)

# HATA YÖNETİMİ
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Yetersiz yetki.")
    elif isinstance(error, commands.MemberNotFound):
        await ctx.send("❌ Kullanıcı bulunamadı.")
    elif isinstance(error, commands.RoleNotFound):
        await ctx.send("❌ Rol bulunamadı.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("❌ Geçersiz argüman. Doğru kullanım: !yardım")
    else:
        await ctx.send(f"❌ Hata: {error}")

bot.run(os.getenv("TOKEN"))