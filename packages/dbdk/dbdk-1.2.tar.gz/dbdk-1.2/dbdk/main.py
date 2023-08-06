import os
from dotenv import load_dotenv
from kit import *

def get_prefix(bot, message) -> List[str]:
    return commands.when_mentioned_or(".")(bot, message)

bot = Bot(
    prefix=get_prefix, 
    intents=discord.Intents.all()
) 

@bot.command(name="test")
async def test(ctx: discord.ApplicationContext):
    
    root: Root = await create_root(ctx)
    
    embed = Embed(
        timestamp=datetime.datetime.today(),
        author=ctx.author
    )
    
    await root.embeds.add_items(embed)
    
    async def on_submit(modal: Modal, interaction: discord.Interaction):
        await embed.edit( **modal.as_dict(skip_null=True), fields=[EmbedField(name="Fuck", value="This fucking shirt")] )
        await interaction.response.send_message("El Embed ha sido editado.", ephemeral=True, delete_after=5)
    
    modal = Modal(
        title="Edita el Embed",
        on_submit=on_submit,
        items = [
            InputText(label="Color", style=InputTextType.singleline, required=False, custom_id="color"),
            InputText(label="Titulo", style=InputTextType.singleline, custom_id="title"),   
            InputText(label="Descripcion", style=InputTextType.long, custom_id="description"), 
            InputText(label="Image (URL)", style=InputTextType.singleline, required=False, custom_id="image"), 
            InputText(label="URL", style=InputTextType.singleline, required=False, custom_id="url")                      
        ]
    )
    
    @only_owner(ctx.author)
    async def on_button_click(btn : Button, interaction: discord.Interaction):
        await modal.open(interaction)
        
    await root.view.add_items(Button(
        on_button_click, "Edit"
    ))

    
load_dotenv()
bot.run(os.environ.get("TOKEN"))
