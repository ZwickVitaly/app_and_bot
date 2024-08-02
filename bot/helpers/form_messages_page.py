async def form_page(messages: list[dict], user_id: int):
    message_string = ""
    for message in messages:
        message_string += (
            f"Автор: {'Вы' if message.get('telegram_id') == user_id else message.get('author_username')}\n"
            f"Сообщение:\n'{message.get('message_text')}'\n"
            f"Отправлено: {message.get('created_at')}\n\n"
        )
    return message_string
