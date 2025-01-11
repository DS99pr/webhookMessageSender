# PunctuactionReplacer Copyright (c) 2024, Pard. All rights reserved.

import discord
import re
import aiohttp
import flet as ft

foo = 'Foo'
blank_message = 'Blank message.'

def check_if_discord_thing(value) -> bool:
    if isinstance(value, discord.embeds.Embed):
       return True
    elif isinstance(value, discord.file.File):
       return 2
    else:
       return False

def process_string(string) -> discord.Embed | str:
    embed_regex = r'EMBED\[title=\"(.*)\", description=\"(.*)\"\]' # EMBED[title="[arg1]", description="[arg2]"]
    embed_match = re.match(embed_regex, string)
    file_regex = r'FILE\[path=\"(.*)\"\]' # FILE[path="[arg1]"]
    file_match = re.match(file_regex, string)
    if embed_match:
       title, description = embed_match.groups()
       return discord.Embed(title=title, description=description)
    elif file_match:
       try:
        path = file_match.groups()
        return discord.File(fp=f"{path}")
       except FileNotFoundError:
        return "Error occured while using me: file does not exists" 
    else:
        return string     

def main(page: ft.Page):
    async def connect(*args, **kwargs):
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(url=webhook_url_input.value, session=session)
            class default:
                name = webhook.name
                avatar = webhook.avatar
            content = webhook_content_input.value
            name = webhook_name_input.value
            avatar = webhook_avatar_input.value
            compressed = process_string(content)
            try:
             if check_if_discord_thing(compressed):
              if check_if_discord_thing(compressed) != 2:
               await webhook.send(embed=compressed, username=(name if name else default.name), avatar_url=(avatar if avatar else default.avatar))
              else:
               await webhook.send(file=compressed, username=(name if name else default.name), avatar_url=(avatar if avatar else default.avatar))       
             else:
              await webhook.send(content=(compressed if compressed else blank_message), username=(name if name else default.name), avatar_url=(avatar if avatar else default.avatar))   
            except discord.errors.HTTPException as err:
             await webhook.send(f"Error occured while using me: {err.text}")     

    page.title = "Webhook Message Sender"
    page.theme_mode = ft.ThemeMode.DARK
    webhook_label = ft.Text("Webhook Message Sender", size=32)
    webhook_url_input = ft.TextField(label="Webhook URL", hint_text="https://discord.com/...")
    webhook_content_input = ft.TextField(label="Message Content", hint_text="hi there...")
    webhook_name_input = ft.TextField(label="Webhook NAME", hint_text="foo...")
    webhook_avatar_input = ft.TextField(label="Webhook AVATAR (url)", hint_text="https://.../something.png")
    webhook_button = ft.Button(text="Submit", icon=ft.Icons.SAVE, on_click=connect)
    
    # HELP

    first_question = ft.Text("How can I create webhook?", size=32)
    first_answer = ft.Text("Go to your guild, then edit your channel, click \"Integrations\", then go into \"Webhooks\" and click \"Create Webhook\", if you need to copy webhook url, click \"Copy Webhook URL\".")
    second_question = ft.Text("How can I send embed?", size=32)
    second_answer = ft.Text("In \"Message Content\" label (in WMS) type \"EMBED[title=\"(title)\", description=\"(description)\"].")
    third_question = ft.Text("How can I send file?", size=32)
    third_answer = ft.Text("In \"Message Content\" label (In WMS) type \"FILE[path=\"(path)\"]. (file must exists)")

    # HELP

    page.add(webhook_label, webhook_url_input, webhook_content_input, webhook_name_input, webhook_avatar_input, webhook_button, first_question, first_answer, second_question, second_answer, third_question, third_answer)

ft.app(main)   
