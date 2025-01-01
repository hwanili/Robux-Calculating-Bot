import nextcord
import asyncio
from nextcord.ext import commands
from nextcord.ui import Button, View, Modal, TextInput

intents = nextcord.Intents.default()
intents.message_content = True

intents = nextcord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

admin_id = #관리자 아이디
TOKEN = " " #봇토큰

@bot.event
async def on_ready():
    print(f'로그인 완료: {bot.user}')

def is_admin(user):
    return user.id == admin_id

robux_price_settings = {}

@bot.slash_command(name='로벅스가격설정', description='1만원당 로벅스 가격을 설정합니다.')
async def set_price(interaction: nextcord.Interaction, robux_price: int):
    if not is_admin(interaction.user):
        embed = nextcord.Embed(
            title="권한 없음",
            description="이 명령어는 관리자만 사용할 수 있습니다.",
            color=0xff0000
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return
    guild_id = interaction.guild_id
    robux_price_settings[guild_id] = robux_price
    embed = nextcord.Embed(
        title="가격 설정 완료",
        description=f"1만원당 로벅스 가격이 {robux_price} 로벅스로 설정되었습니다.",
        color=0x00ff00
    )
    await interaction.response.send_message(embed=embed)

class RobuxInputModal(Modal):
    def __init__(self, price_per_1_robox):
        super().__init__(title="로벅스 양 입력")
        self.price_per_1_robox = price_per_1_robox
        self.robox_amount = TextInput(
            label="원하는 로벅스 양을 입력하세요",
            placeholder="예: 1800",
            required=True
        )
        self.add_item(self.robox_amount)
    async def callback(self, interaction: nextcord.Interaction):
        try:
            robox_amount = int(self.robox_amount.value)
            price_per_robox = 10000 / self.price_per_1_robox
            total_price = robox_amount * price_per_robox
            total_price_int = int(total_price)
            embed = nextcord.Embed(
                title="로벅스 계산 결과",
                description=f"{robox_amount} 로벅스의 가격은 {total_price_int} 원입니다.",
                color=0x00ff00
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except ValueError:
            await interaction.response.send_message("유효한 숫자를 입력해주세요.", ephemeral=True)
class RobuxButtonView(View):
    def __init__(self, price_per_1_robox):
        super().__init__()
        self.price_per_1_robox = price_per_1_robox
    @nextcord.ui.button(label="로벅스 계산", style=nextcord.ButtonStyle.green)
    async def calculate_button(self, button: Button, interaction: nextcord.Interaction):
        modal = RobuxInputModal(self.price_per_1_robox)
        await interaction.response.send_modal(modal)

@bot.slash_command(name="로벅스계산", description="로벅스 가격을 계산합니다.")
async def robox_calculate(interaction: nextcord.Interaction):
    guild_id = interaction.guild_id
    if guild_id not in robux_price_settings:
        embed = nextcord.Embed(
            title="가격 미설정",
            description="관리자가 먼저 `/로벅스가격설정` 명령어로 가격을 설정해야 합니다.",
            color=0xff0000
        )
        await interaction.response.send_message(embed=embed)
        return
    price_per_1_robox = robux_price_settings[guild_id]
    view = RobuxButtonView(price_per_1_robox)
    embed = nextcord.Embed(
        title="로벅스 계산",
        description="버튼을 눌러 원하는 로벅스 양에 대한 가격을 계산하세요.",
        color=0x00ff00
    )
    await interaction.response.send_message(embed=embed, view=view)

bot.run(TOKEN)
