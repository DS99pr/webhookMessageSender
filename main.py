# punctuactionReplacer Copyright (c) 2024, Pard. All rights reserved.

import discord
import aiohttp
import flet as ft


def main(page: ft.Page):
    async def connect(*args, **kwargs):
        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(url=webhook_url_input.value, session=session)
            await webhook.send(content=(webhook_content_input.value if webhook_content_input.value else "Blank message."), username=(webhook_name_input.value if webhook_name_input.value else "Foo"))
    page.title = "Webhook Message Sender"
    page.theme_mode = ft.ThemeMode.DARK
    webhook_label = ft.Text("Webhook Message Sender", size=32)
    webhook_url_input = ft.TextField(label="Webhook URL", hint_text="https://discord.com/...")
    webhook_content_input = ft.TextField(label="Message Content", hint_text="hi there...")
    webhook_name_input = ft.TextField(label="Webhook NAME", hint_text="foo...")
    webhook_button = ft.Button(text="Submit", icon=ft.Icons.SAVE, on_click=connect)
    page.add(webhook_label, webhook_url_input, webhook_content_input, webhook_name_input, webhook_button)

ft.app(main)   
