from math import radians
import random
import segno
from khayyam import JalaliDatetime
from gtts import gTTS
import qrcode
import telebot
from telebot.types import Message


bot=telebot.TeleBot('2139317891:AAHIEMoQb8xR2cdrpEol-e2AqAT7oitjFe0')


@bot.message_handler(commands=['start'])
def salam(message):
    bot.reply_to(message,'خوش اومدی' + message.from_user.first_name)



@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message,
                 """
                 /start=به کاربر خوش امد میگوید 
                 /game=بازی حدس عدد اجرا میشود کاربر یک عدد حدس میزد و بات راهنمایی میکند 
                 /age=تاریخ تولد را دریافت میکند و سن را محاسبه میکند 
                 /voice=یک جمله به صورت انگلیسی از کاربر دریافت نماید و به صورت ویس ارسال کند 
                 /max=یک ارایه به صورت 1و2و3و4 از کاربر دریافت نماید و بزرگ ترین عدد را نمایش دهد
                 /argmax=یک ارایه به صورت 1و2و3و4 از کاربر بگیرد و بزرگ ترین اندیس را مشخص کند
                 /qrcode=  ان را تولید کندqrcode یک رشته از کاربر دریافت نماید و  """)
    
    
    
@bot.message_handler(commands=['age'])
def age(message):
    birth=bot.send_message(message.chat.id, 'تاریخ تولدت را وارد کن مثلا: 1379/7/19')
    bot.register_next_step_handler(birth,age_calculate)
def age_calculate(birth) :
    a=birth.text.split('/')
    b=JalaliDatetime.now()-JalaliDatetime(a[0],a[1],a[2])
    y=b//365
    bot.send_message(birth.chat.id,y)
    
    
@bot.message_handler(commands=['max'])  
def max_aray(message):
    aray=bot.send_message(message.chat.id,'وارد کن اعدادی مثل: 14و7و78و15و8و19و20 ')
    bot.register_next_step_handler(aray,maxing)

def maxing(aray):
    a=list(map(float,aray.text.split(',')))   
    b=max(a)
    bot.send_message(aray.chat.id,b)



@bot.message_handler(commands=['argmax'])  
def argmax(message):
     aray=bot.send_message(message.chat.id,'وارد کن اعدادی مثل: 14و7و78و15و8و19و20 ')
     bot.register_next_step_handler(aray,maxing_index)
def maxing_index(aray):
    a=list(map(float,aray.text.split(',')))   
    b=a.index(max(a))+1
    bot.send_message(aray.chat.id,b)
    
    
    
@bot.message_handler(commands=['qrcode'])
def qrcode(message):
    text=bot.send_message(message.chat.id,'متنی راوارد کنید ')
    bot.register_next_step_handler(text,qrc)
def qrc(message):
    text=message.text
    img=segno.make(text)
    img.save('qrcode.png')
    qr=open('qrcode.png','rb')
    bot.send_photo(message.chat.id,qr)
    
    
@bot.message_handler(commands=['voice'])
def voice(message):
    text=bot.send_message(message.chat.id,'متنی راوارد کنید ')
    bot.register_next_step_handler(text,make_voice)
def make_voice(message):
    t=message.text
    language='en'
    myobj=gTTS(text=t,lang=language,slow=False)
    myobj.save('voice.mp3')
    v=open('voice.mp3','rb')
    bot.send_voice(message.chat.id,v)
    

@bot.message_handler(commands=['game'])
def game(message):
    global r
    r=random.randint(1,20)
    g=bot.send_message(message.chat.id,'یک عدد بین 1 تا 20 وارد کن')
    bot.register_next_step_handler(g,gaming)
def gaming(g):
    global r
    markub=telebot.types.ReplyKeyboardMarkup(row_width=1)
    Button=telebot.types.KeyboardButton('new game')
    markub.add(Button)
    if  g.text=='new game':
        g=bot.send_message(g.chat.id,'بازی دوباره شروع شداز بین 1 تا 20 انتخاب کن') 
        r=random.randint(1,20)
        bot.register_next_step_handler(g,gaming)
    
    else:    
       
       if int (g.text)>r:
        g=bot.send_message(g.chat.id,'بیا پایین ',reply_markup=markub)
        bot.register_next_step_handler(g,gaming)
       elif int(g.text)<r:
        g=bot.send_message(g.chat.id,'برو بالا',reply_markup=markub)
        bot.register_next_step_handler(g,gaming)
       else:
        markub=telebot.types.ReplyKeyboardRemove(selective=True)
        bot.send_message(g.chat.id,'تبریک شما برنده شدی',reply_markup=markub)
        
bot.infinity_polling()



