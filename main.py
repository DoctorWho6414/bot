import asyncio
import asyncpraw
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from mtranslate import translate


TOKEN_API = '6169019962:AAEIMzzio9u1BdGm7tOmDhMNrPes2jxM19o'
GROUP_ID = -1001698692995

bot = Bot(token=TOKEN_API)
dp = Dispatcher(bot, storage=MemoryStorage())

reddit = asyncpraw.Reddit(
    client_id='cA27X1AB2w9t0Gti5n1CaA',
    client_secret='YvJdtC_1ZntT_gF7DUFdVMKMmrDQoQ',
    user_agent='Budget_Bid5845'
)

async def send_message_to_group(message):
    await bot.send_message(chat_id=GROUP_ID, text=message)

async def fetch_posts(subreddit_name, limit):
    subreddit = await reddit.subreddit(subreddit_name)
    new_posts = []
    async for post in subreddit.new(limit=limit):
        new_posts.append(post)
    return new_posts

async def process_posts():
    subreddit1 = 'FetishWantAds'
    subreddit2 = 'realonlyfansrequests'
    processed_posts = []

    while True:
        new_posts1 = await fetch_posts(subreddit1, limit=5)
        new_posts2 = await fetch_posts(subreddit2, limit=5)

        for post in new_posts1:
            if post.id not in processed_posts:
                translated_title = translate(post.title, 'ru', 'en')
                translated_content = translate(post.selftext, 'ru', 'en')

                message = f"New Post from r/FetishWantAds:\nTitle: {translated_title}\nURL: {post.url}\nText: {translated_content}"
                await send_message_to_group(message)

                processed_posts.append(post.id)

        for post in new_posts2:
            if post.id not in processed_posts:
                translated_title = translate(post.title, 'ru', 'en')
                translated_content = translate(post.selftext, 'ru', 'en')

                message = f"New Post from r/realonlyfansrequests:\nTitle: {translated_title}\nURL: {post.url}\nText: {translated_content}"
                await send_message_to_group(message)

                processed_posts.append(post.id)

        await asyncio.sleep(60)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(process_posts())
    loop.create_task(dp.skip_updates())
    try:
        loop.run_until_complete(dp.start_polling())
    finally:
        loop.run_until_complete(dp.storage.close())
        loop.run_until_complete(dp.storage.wait_closed())
        loop.close()