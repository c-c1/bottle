import requests
from bs4 import BeautifulSoup
import re
import random
import telebot
from telebot import types

def extract_image_urls(page_url):
    response = requests.get(page_url)
    
    if response.status_code != 200:
        print(f"فشل في جلب الصفحة. الرمز الاستجابة: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')

    image_urls = []
    for img_tag in img_tags:
        src = img_tag.get('src')
        if src and re.search(r'_low\.webp$', src):
            image_urls.append(src)
    
    return image_urls

def download_image(url, save_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=128):
                file.write(chunk)
        print(f"تم تحميل الصورة بنجاح إلى {save_path}")
    else:
        print(f"فشل في تحميل الصورة. الرمز الاستجابة: {response.status_code}")

def save_user_info(user_id, username):
    with open('usersphoto.txt', 'a') as file:
        file.write(f'User ID: {user_id}, Username: @{username}\n')

def is_user_info_saved(user_id):
    with open('usersphoto.txt', 'r') as file:
        return f'User ID: {user_id}' in file.read()

def is_user_in_channel(user_id):
    try:
        chat_member = bot.get_chat_member('@KINGROBOTTEL', user_id)
        return chat_member.status in [types.ChatMember.MEMBER, types.ChatMember.ADMINISTRATOR, types.ChatMember.CREATOR]
    except Exception as e:
        print(f"Error checking channel membership: {e}")
        return False

bot = telebot.TeleBot("6853009728:AAH3paDZC3sJtAow0hGQFW5YAy1MJCVUPy4")
# def msg(message):

#     bot.send_message(message.chat.id,'تم تحديث البوت اضغط /help')
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    username = message.from_user.username
    print(f"User ID: {user_id}, Username: @{username}")
    
    if not is_user_info_saved(user_id):
        save_user_info(user_id, username)

        if is_user_in_channel(user_id):
            bot.send_message(message.chat.id, "مرحبا بك في بوت انشاء صور بلذكاء الاصطناعي\n لمعرفة المزيد اضغط /help \n\n\tتم البرمجة بواسطة \n TELEGRAM: @msms1o\n INSTAGRAM: 0c0cg")
            bot.send_message(message.chat.id, "ارسل كلمة تلميحية")

            bot.register_next_step_handler(message, photo)
        else:
            # قم بتعديل الرابط هنا إذا كانت القناة تغيرت
            channel_link = "https://t.me/KINGROBOTTEL"
            bot.send_message(message.chat.id, f"يجب أن تنضم أولاً إلى القناة {channel_link} لاستخدام البوت.")
    else:
        bot.reply_to(message, "مرحبا بك مجددا في بوت انشاء صور بالذكاء الاصطناعي\nاضغط /help \n تم البرمجة بواسطة \nTELEGRAM: @msms1o\n INSTAGRAM: 0c0cg")

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "اكتب كلمة تلميحية عن أي شيء تريد وصفه\n\nبالعربي أو الإنجليزي مثل car أو green car و أي شيء تقوم بكتابته\n\n او اضغظ /random لأنتاج الصور العشوائية")


@bot.message_handler(commands=['random'])
def help(message):

    animal_names = ["Red", "Blue", "Green", "Yellow", "Orange", "Purple", "Pink", "Violet"]
    animal_names1 = ["Lion", "Elephant", "Giraffe", "Tiger", "Kangaroo", "dog","cat", "Zebra", "Monkey","Toyota", "Honda", "Ford", "Chevrolet", "Mercedes-Benz", "BMW", "Audi", "Tesla"]
    chosen_name = random.choice(animal_names)
    chosen_name1 = random.choice(animal_names1)
    allrand = f'{chosen_name}%20{chosen_name1}'
    print(allrand)
    page_url = f'https://www.seaart.ai/ar/searchView?keyword=art%20{allrand }'
    image_urls = extract_image_urls(page_url)
    bot.send_message(message.chat.id, "جار المعالجة")

    selected_image_url = random.choice(image_urls)

    save_path = "downloaded_image.jpg"
    download_image(selected_image_url, save_path)

    bot.send_photo(message.chat.id, photo=open(save_path, 'rb'))
    #bot.send_message(message.chat.id, allrand)

@bot.message_handler(func=lambda message: True)
def photo(message):
    try:
        user = message.text.split()
        page_url = f'https://www.seaart.ai/ar/searchView?keyword=art%20{user}'
        image_urls = extract_image_urls(page_url)
        bot.send_message(message.chat.id, "جار المعالجة")

        selected_image_url = random.choice(image_urls)

        save_path = "downloaded_image.jpg"
        download_image(selected_image_url, save_path)
        bot.send_photo(message.chat.id, photo=open(save_path, 'rb'))

        print(f"تم تنزيل صورة عشوائية بنجاح: {selected_image_url}")
    except:
        bot.send_message(message.chat.id, "فشل المعالجة")

max_retries = 3
retries = 0

while retries < max_retries:
    try:
        bot.polling(timeout=60)
    except requests.exceptions.ReadTimeout:
        print("Timeout occurred. Retrying...")
        retries += 1
        continue
    break
else:
    print("Max retries reached. Unable to establish connection.")
