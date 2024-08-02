from polling_dispatcher import main_polling
from webhook_dispatcher import main_webhooks
from settings import WEBHOOK_BOT


if __name__ == "__main__":
    if WEBHOOK_BOT:
        main_webhooks()
    else:
        main_polling()