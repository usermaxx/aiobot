import asyncio
import aiogram
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import random
from datetime import datetime 
import sqlite3
import google.generativeai as genai

bot = Bot(token="6810377873:AAGtTn8CUrwtzqAXiMp9Q8uDJrjotOt9G7s")
dp = Dispatcher()

genai.configure(api_key="AIzaSyA-X1rDXanqHpoL3tJ96V7CCMK1rHJh7Mg")
model = genai.GenerativeModel("gemini-1.5-flash")
history = ["Chat history:",]
role = None
def gemini_send(g_input, message):
     history.append(f"{g_input}")
     response = model.generate_content(f"@{g_input}  {history}  {role} (максмум 150 слов). даю разрешение использовать нецензурные лексики в напряженных ситуациях")
     print(response.text)
     history.append("You responsed:" + response.text)
     return response.text

quotes = ['Обязательно дружите с теми, кто лучше вас. Будете мучиться, но расти.',
             'Ты — это то, что ты делаешь. Ты — это твой выбор. Тот, в кого себя превратишь.',
             'Кем бы ты ни был — будь лучше.',
             'Наверное, никого нельзя насильно заставить измениться, даже если он сам об этом просит. В конце концов, если ты созрел, то сможешь измениться и без посторонней помощи, сам.',
             'Умеющий управлять другими силен, но умеющий владеть собой ещё сильнее.',
             'Невозможно жить лучше, чем проводя жизнь в стремлении стать совершеннее.',
             'Человек начинает жить лишь тогда, когда ему удается превзойти самого себя.',
             'Единственный человек, стоящий на твоём пути, — это ты сама.',
             'Будьте внимательны к своим мыслям, они — начало поступков.',
             'Нужно быть лучше, чем вчера, а не лучше, чем другие. Хоть эта стратегия жизни и не самая легкая, зато самая беспроигрышная...',
             'Когда человек начинает войну с самим собой, он уже чего-то да стоит.',
             'Похоже, ты мечтаешь сбежать от обычной жизни, но жизнь в Токио примерно через полгода тоже станет обычной. Если хочешь новых ощущений, то лучше податься в другую страну или же влезть во что-нибудь незаконное. Но даже это станет обыденным дня через три. Если правда хочешь сбежать — продолжай развиваться. И неважно, где твоя цель, выше или ниже тебя. Просто наслаждайся повседневной жизнью.',
             'Одиночество никогда не пугало меня, ведь это личное время, а учитывая, что во мне живет мелкий эгоист, то я особо ценю это время, время самопознания и самосовершенствования.',
             'Единственный способ стать умнее — играть с более умным противником.',
             'Если Вы хотите изменить свою реальность, то Вы должны изменить своё мышление.',
             'Лучше находиться в обществе людей лучших, чем вы сами… Выберите знакомых, чье поведение лучше, чем ваше, и вы устремитесь в этом направлении.',
             'Совершенствоваться – значит меняться, быть совершенным – значит меняться часто.',
             'Жизнь — это риск. Только попадая в рискованные ситуации, мы продолжаем расти. И одна из самых рискованных ситуаций, на которые мы можем отважиться, — это риск полюбить, риск оказаться уязвимым, риск позволить себе открыться перед другим человеком, не боясь ни боли, ни обид.',
             'Даже разумный человек будет глупеть, если он не будет самосовершенствоваться.',
             'Каждый день надо делать дело, которое тебя пугает.',
             'Либо вы поднимитесь вверх на одну ступень сегодня, или соберитесь с силами, чтобы подняться на эту ступень завтра.',
             ]

@dp.message(Command('roles'))
async def airole(message: types.Message):
    await message.answer(f"Thinker Role: \n {role}")
@dp.message(lambda message: message.text.startswith('!role'))
async def setrole(message: types.Message):
    global history
    global role
    history = ["Chat History:"]
    role = message.text[5:]
    await message.answer(f'Role: \n {role} \n setted up ')
@dp.message(Command('quote', 'start', 'цитата'))
async def start(message: types.Message):
    quote = random.choice(quotes)
    response = model.generate_content(f" отвечай коротко и ясно")
    await message.reply(quote)
@dp.message(Command('help'))
async def quote(message: types.Message):
    await message.reply("_Комманды_ \n /start /quote /цитата - цитаты \n /news - новости предстоящих обновлений \n /info - информация о текущем боте", parse_mode="Markdown")


@dp.message(Command('cleanhistory'))
async def cleanchat(message: types.Message):
    global history
    history = ["Chat History:"]
    await message.answer("Chat history cleaned.")


@dp.message(lambda message: message.text.startswith(("!", "/")))
async def gemini_pull(message):
     userinfo = message.from_user.username
     print(userinfo)
     g_input = f"@{userinfo}: {message.text[1:]}"
     answer = gemini_send(g_input, message)
     await message.reply(answer)


@dp.message(Command('news'))
async def news(message: types.Message):
    await message.answer(""" 
    *Предстоящие Обновы*: \n 
    _version 0.5_
    1. *Улучшение интерфейса* 
    2. #empty 
    3. #empty
    
    """, parse_mode = "Markdown")


@dp.message(Command('ban'))
async def ban(message: types.Message):
    if message.reply_to_message:
        replyeduser = message.reply_to_message.from_user
        username = replyeduser.username
        await message.answer(f"Пользователь @{username} забанен")
    else:
        print('у чела нет юз')

@dp.message(Command('kiss'))
async def ban(message: types.Message):
    if message.reply_to_message:
        replyeduser = message.reply_to_message.from_user
        username = replyeduser.username
        ruser = message.from_user.username

        await message.answer(f"@{username} получил поцелуй💋 от @{ruser}")
    else:
        user = message.from_user
        uz = user.username
        await message.answer(f'@{uz} поцеловал тут всех!! @everyone')
        


@dp.message(Command('server')) 
async def ip(message: types.Message):
     await message.answer("DREIX.aternos.me:44838")



@dp.message(Command('shedule'))
async def sh(message: types.Message):
    at = message.from_user.username
    id = message.from_user.id
    # cur.execute("INSERT OR IGNORE ")
    await message.reply(f"тебя зовут {at}, id: {id}")

@dp.message(lambda message: message.chat.type == "private")
async def ls(message: types.Message):
    await bot.send_message(chat_id="6746608599", text=message.text)


    


async def sicle():
    while True:
        watch = datetime.now()
        if watch.hour == 23 and watch.minute == 24:
                   print('KABOOM')
                   a = '-1002339942344'
                   await bot.send_message(chat_id=a, text="Итоги дня: \nСултан 102 очка \nРизат 0 \nРафик 0")
                   await asyncio.sleep(60)
        await asyncio.sleep(2)



async def main():
     await asyncio.gather(
         sicle(),
         dp.start_polling(bot))

if __name__ == '__main__':
    asyncio.run(main())
