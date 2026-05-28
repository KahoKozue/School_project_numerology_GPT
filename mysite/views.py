import os
import json
from django.shortcuts import render
from django.http import HttpResponse
from mysite.ai_mod import GPT_response,GPT3_5_response,GPT_response4o
from . import models
from .models import Daily
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.http import StreamingHttpResponse
import time
from openai import OpenAI
import datetime
from cnlunar.lunar import *


def book2(request):
    return render(request, 'book2.html')
def book3(request):
    return render(request, 'book3.html')
def book4(request):
    return render(request, 'book4.html')
def book5(request):
    return render(request, 'book5.html')
def aboutme(request):
    return render(request, 'aboutme.html')
def we(request):
    return render(request, 'we.html')
def dragon(request):
    return render(request, 'dragon.html')
def disclaimer(request):
    return render(request, 'disclaimer.html')

#---------------------------------------------------------------------------------------------------------------------
#命盤
# 十神表
relationship_table = {
    '甲': {'甲': '比肩', '乙': '劫財', '丙': '偏印', '丁': '正印', '戊': '七殺', '己': '正官', '庚': '偏財', '辛': '正財', '壬': '食神', '癸': '傷官'},
    '乙': {'甲': '劫財', '乙': '比肩', '丙': '正印', '丁': '偏印', '戊': '正官', '己': '七殺', '庚': '正財', '辛': '偏財', '壬': '傷官', '癸': '食神'},
    '丙': {'甲': '食神', '乙': '傷官', '丙': '比肩', '丁': '劫財', '戊': '偏印', '己': '正印', '庚': '七殺', '辛': '正官', '壬': '偏財', '癸': '正財'},
    '丁': {'甲': '傷官', '乙': '食神', '丙': '劫財', '丁': '比肩', '戊': '正印', '己': '偏印', '庚': '正官', '辛': '七殺', '壬': '正財', '癸': '偏財'},
    '戊': {'甲': '偏財', '乙': '正財', '丙': '食神', '丁': '傷官', '戊': '比肩', '己': '劫財', '庚': '偏印', '辛': '正印', '壬': '七殺', '癸': '正官'},
    '己': {'甲': '正財', '乙': '偏財', '丙': '傷官', '丁': '食神', '戊': '劫財', '己': '比肩', '庚': '正印', '辛': '偏印', '壬': '正官', '癸': '七殺'},
    '庚': {'甲': '七殺', '乙': '正官', '丙': '偏財', '丁': '正財', '戊': '食神', '己': '傷官', '庚': '比肩', '辛': '劫財', '壬': '偏印', '癸': '正印'},
    '辛': {'甲': '正官', '乙': '七殺', '丙': '正財', '丁': '偏財', '戊': '傷官', '己': '食神', '庚': '劫財', '辛': '比肩', '壬': '正印', '癸': '偏印'},
    '壬': {'甲': '偏印', '乙': '正印', '丙': '七殺', '丁': '正官', '戊': '偏財', '己': '正財', '庚': '食神', '辛': '傷官', '壬': '比肩', '癸': '劫財'},
    '癸': {'甲': '正印', '乙': '偏印', '丙': '正官', '丁': '七殺', '戊': '正財', '己': '偏財', '庚': '傷官', '辛': '食神', '壬': '劫財', '癸': '比肩'},       
    '子': {'甲': '正印', '乙': '偏印', '丙': '正官', '丁': '七殺', '戊': '正財', '己': '偏財', '庚': '傷官', '辛': '食神', '壬': '劫財', '癸': '比肩'},
    '丑': {'甲': '正財', '乙': '偏財', '丙': '傷官', '丁': '食神', '戊': '劫財', '己': '比肩', '庚': '正印', '辛': '偏印', '壬': '正官', '癸': '七殺'},
    '寅': {'甲': '比肩', '乙': '劫財', '丙': '偏印', '丁': '正印', '戊': '七殺', '己': '正官', '庚': '偏財', '辛': '正財', '壬': '食神', '癸': '傷官'},
    '卯': {'甲': '劫財', '乙': '比肩', '丙': '正印', '丁': '偏印', '戊': '正官', '己': '七殺', '庚': '正財', '辛': '偏財', '壬': '傷官', '癸': '食神'},
    '辰': {'甲': '偏財', '乙': '正財', '丙': '食神', '丁': '傷官', '戊': '比肩', '己': '劫財', '庚': '偏印', '辛': '正印', '壬': '七殺', '癸': '正官'},
    '巳': {'甲': '傷官', '乙': '食神', '丙': '劫財', '丁': '比肩', '戊': '正印', '己': '偏印', '庚': '正官', '辛': '七殺', '壬': '正財', '癸': '偏財'},
    '午': {'甲': '食神', '乙': '傷官', '丙': '比肩', '丁': '劫財', '戊': '偏印', '己': '正印', '庚': '七殺', '辛': '正官', '壬': '偏財', '癸': '正財'},
    '未': {'甲': '正財', '乙': '偏財', '丙': '傷官', '丁': '食神', '戊': '劫財', '己': '比肩', '庚': '正印', '辛': '偏印', '壬': '正官', '癸': '七殺'},
    '申': {'甲': '七殺', '乙': '正官', '丙': '偏財', '丁': '正財', '戊': '食神', '己': '傷官', '庚': '比肩', '辛': '劫財', '壬': '偏印', '癸': '正印'},
    '酉': {'甲': '正官', '乙': '七殺', '丙': '正財', '丁': '偏財', '戊': '傷官', '己': '食神', '庚': '劫財', '辛': '比肩', '壬': '正印', '癸': '偏印'},
    '戌': {'甲': '偏財', '乙': '正財', '丙': '食神', '丁': '傷官', '戊': '比肩', '己': '劫財', '庚': '偏印', '辛': '正印', '壬': '七殺', '癸': '正官'},
    '亥': {'甲': '偏印', '乙': '正印', '丙': '七殺', '丁': '正官', '戊': '偏財', '己': '正財', '庚': '食神', '辛': '傷官', '壬': '比肩', '癸': '劫財'}
}

#月份表
M1,M2,M3,M4,M5,M6,M7,M8,M9,M10,M11,M12 = "丁丑月","戊寅月","己卯月","庚辰月","辛巳月","壬午月","癸未月","甲申月","乙酉月","丙戌月","丁亥月","戊子月"

#找十神
def find_relationship(first_char, second_char):
    return relationship_table[first_char][second_char]

#計算八字 w是八字，s是納音 g是十神
def bazs(user_date,user_time):
    #先分割日期和時間
    date_parts = list(map(int, user_date.split('-')))
    #print("date_parts:",date_parts)
    time_parts = list(map(int, user_time.split(':')))
    #print("time_parts:",time_parts)
    #轉換日期格式
    a = Lunar(datetime(date_parts[0], date_parts[1], date_parts[2], time_parts[0], time_parts[1]), godType='8char')
    #print(a)
    w1,w2,w3,w4 = a.year8Char, a.month8Char, a.day8Char, a.twohour8Char
    #print(a.get_nayin())
    #納音
    s1 = a.get_nayin()
    #八字
    g1,g2= w1[0],w1[1]
    g3,g4= w2[0],w2[1]
    g5,g6= w3[0],w3[1]
    g7,g8= w4[0],w4[1]
    #十神
    graphs = [g1, g2, g3, g4, g6, g7, g8]  
    g1, g2, g3, g4, g6, g7, g8 = [find_relationship(graph, g5) for graph in graphs]   
    return w1,w2,w3,w4,s1,g1,g2,g3,g4,g6,g7,g8
#計算今天八字
def now_bazs():
    now = datetime.now()
    user_date = now.strftime("%Y-%m-%d")
    user_time = now.strftime("%H:%M")
    #先分割日期和時間
    date_parts = list(map(int, user_date.split('-')))
    #print("date_parts:",date_parts)
    time_parts = list(map(int, user_time.split(':')))
    #print("time_parts:",time_parts)
    #轉換日期格式
    a = Lunar(datetime(date_parts[0], date_parts[1], date_parts[2], time_parts[0], time_parts[1]), godType='8char')
    #print(a)
    w1,w2,w3,w4 = a.year8Char, a.month8Char, a.day8Char, a.twohour8Char
    return w1,w2,w3,w4

#2025年 月干支
M1,M2,M3,M4,M5,M6,M7,M8,M9,M10,M11,M12 = "丁丑月","戊寅月","己卯月","庚辰月","辛巳月","壬午月","癸未月","甲申月","乙酉月","丙戌月","丁亥月","戊子月"
M =["","丁丑月","戊寅月","己卯月","庚辰月","辛巳月","壬午月","癸未月","甲申月","乙酉月","丙戌月","丁亥月","戊子月"]
#年網頁
@login_required
def year(request):
    user = request.user
    user_date = str(Customer.objects.get(user=user).birthday)
    user_time = str(Customer.objects.get(user=user).birthday_time) 
    user_time = user_time[:-3]

    return render(request, 'year.html',locals())
@login_required
def yearfinal(request):
    return render(request, 'yearfinal.html')

def GPTyear(text):
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.chat.completions.create(
        model="ft:gpt-3.5-turbo-1106:kitaikuyokitaaan:0429explain3:9JESHblh",
        messages=[
            {"role": "system", "content": "這是一個基於四柱八字的聊天機器人，旨在提供洞察力強的讀數與事實信息相結合，不要說到生肖，請用繁體中文回答。"},
            {"role": "user", "content": text}
        ],
        temperature=1,
        max_tokens=4096,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    answer = response.choices[0].message.content
    return answer

from .models import Yearly
import re
#計算年月
@login_required
def year12(request):
    month = request.GET.get('m')
    year = datetime.now().year
    x = int(month)
    M = [
        'dummy', '甲子', '乙丑', '丙寅', '丁卯', '戊辰', '己巳', '庚午', '辛未', '壬申', '癸酉', '甲戌', '乙亥'
    ]
    m = M[x]
    #print("m:", m)
    user = request.user
    user_date = str(Customer.objects.get(user=user).birthday)
    user_time = str(Customer.objects.get(user=user).birthday_time)
    user_data = bazs(user_date,user_time)
    #print(user_data)
    d5 = user_data[2][0]
    dg1, dg2 = find_relationship(m[0], d5), find_relationship(m[1], d5)
    #print("dg1, dg2:", dg1, dg2)
    
    horoscope, created = Yearly.objects.get_or_create(user=request.user, year=year)
    month_field = [
            'january', 'february', 'march', 'april', 'may', 'june',
            'july', 'august', 'september', 'october', 'november', 'december'
        ][x-1]   
    if not created:
        # 如果資料已存在，直接返回資料庫中的結果
        A = getattr(horoscope, month_field)
        if A:
            # 使用關鍵字拆分字串
            health_key = "健康運勢："
            finance_key = "財務運勢："
            love_key = "愛情運勢："
            career_key = "工作運勢："

            # 找出每段運勢的開始位置
            health_start = A.find(health_key)
            finance_start = A.find(finance_key)
            love_start = A.find(love_key)
            career_start = A.find(career_key)

            # 提取每段運勢
            health = A[health_start:finance_start].strip()
            finance = A[finance_start:love_start].strip()
            love = A[love_start:career_start].strip()
            career = A[career_start:].strip()
            #print(career)
            
            response = str(str(health) + "@" + str(finance) + "@" + str(love) + "@" + str(career) + "@")
            return StreamingHttpResponse(response, content_type='text/event-stream')


    def month_H(user_data, m, dg1, dg2, month):
        prompt = '我的命盤是%s，這個月是%s月遇到%s和%s，說明這個月健康運的勢是好還是壞?要注意甚麼?' % (user_data, m, dg1, dg2)
        return GPTyear(prompt)

    def month_M(user_data, m, dg1, dg2, month):
        prompt = '我的命盤是%s，這個月是%s月遇到%s和%s，說明這個月財務的運勢是好還是壞?要注意甚麼?' % (user_data, m, dg1, dg2)
        return GPTyear(prompt)

    def month_L(user_data, m, dg1, dg2, month):
        prompt = '我的命盤是%s，這個月是%s月遇到%s和%s，說明這個月愛情的運勢是好還是壞?要注意甚麼?' % (user_data, m, dg1, dg2)
        return GPTyear(prompt)

    def month_W(user_data, m, dg1, dg2, month):
        prompt = '我的命盤是%s，這個月是%s月遇到%s和%s，說明這個月工作的運勢是好還是壞?要注意甚麼?' % (user_data, m, dg1, dg2)
        return GPTyear(prompt)

    def combined_year_stream(user_data, m, month):
        health = month_H(user_data, m, dg1, dg2, month)
        finance = month_M(user_data, m, dg1, dg2, month)
        love = month_L(user_data, m, dg1, dg2, month)
        work = month_W(user_data, m, dg1, dg2, month)

        combined_result = f"健康運勢：{health}\n財務運勢：{finance}\n愛情運勢：{love}\n工作運勢：{work}"

        # 檢查資料庫中是否已有該年份的資料
        horoscope, created = Yearly.objects.get_or_create(user=request.user, year=year)

        month_field = [
            'january', 'february', 'march', 'april', 'may', 'june',
            'july', 'august', 'september', 'october', 'november', 'december'
        ][x-1]

        setattr(horoscope, month_field, combined_result)
        horoscope.save()

        parts = combined_result.split('\n')
        for part in parts:
            yield part + "@"

    response = StreamingHttpResponse(combined_year_stream(user_data, m, month), content_type='text/event-stream')
    return response

#每日網頁
"""
@login_required
def day(request):
    return render(request, 'day.html')
"""
from .models import Daily
import threading
#計算每日
@login_required
def day12(request):
    user = request.user
    birthday = Customer.objects.get(user=user)
    birthday = str(birthday.birthday)
    user_time = '00:00'
    w1,w2,w3,w4,s1,r1,r2,r3,r4,r6,r7,r8 =bazs(birthday,user_time)
    d5= w3[0]
    user_data = "%s年 %s月 %s日 %s時，十神分別是:年干為%s、年支為%s、月干為%s、月支為%s、日干%s為本元、日支為%s、時干為%s、時支為%s。"%(w1,w2,w3,w4,r1,r2,r3,r4,d5,r6,r7,r8)
    
    d1,d2,d3,d4 =now_bazs()
    dg1,dg2 =find_relationship(d3[0],d5),find_relationship(d3[1],d5)
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")

    
    def GPTday(prompt):
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        stream = client.chat.completions.create(
            model="ft:gpt-3.5-turbo-1106:kitaikuyokitaaan:0429explain3:9JESHblh",
            messages=[
                {"role": "system", "content": "這是一個基於四柱八字的聊天機器人，旨在提供洞察力強的讀數與事實信息相結合，請用繁體中文回答。"},
                {"role": "user", "content": prompt}
            ],
            stream=True,
            temperature=1,
            max_tokens=4096,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        for chunk in stream:
            content = chunk.choices[0].delta.content
            if content:
                yield content
    if request.method == 'GET':
        prompt = request.GET.get('prompt')
        if prompt == 'H':
            user_prompt = '我的命盤是%s，今天是%s日遇到%s和%s，一句話說明今天健康運勢是好還是壞?要注意甚麼?' % (user_data, d3, dg1, dg2)
            field = 'health'
        elif prompt == 'L':
            user_prompt = '我的命盤是%s，今天是%s日遇到%s和%s，一句話說明今天感情的運勢是好還是壞?要注意甚麼?' % (user_data, d3, dg1, dg2)
            field = 'love'
        elif prompt == 'W':
            user_prompt = '我的命盤是%s，今天是%s日遇到%s和%s，一句話說明今天工作的運勢是好還是壞?要注意甚麼?' % (user_data, d3, dg1, dg2)
            field = 'work'
        else:
            user_prompt = '我的命盤是%s，今天是%s日遇到%s和%s，一句話說明今天財務的運勢是好還是壞?要注意甚麼?' % (user_data, d3, dg1, dg2)
            field = 'finance'
        # 檢查資料庫中是否已有今天的資料
        try:
            horoscope = Daily.objects.get(user=user, date=today)
            response_text = getattr(horoscope, field)
            return HttpResponse(response_text, content_type='text/plain; charset=utf-8')
        except Daily.DoesNotExist:
            # 初始化緩存
            response_text = []

            def stream_and_save():
                for content in GPTday(user_prompt):
                    response_text.append(content)
                    yield content

                # 保存到資料庫
                result_text = ''.join(response_text)
                horoscope, created = Daily.objects.get_or_create(user=user, date=today)
                setattr(horoscope, field, result_text)
                horoscope.save()

            # 返回流逝的生成器
            response = StreamingHttpResponse(stream_and_save(), content_type='text/event-stream')
            return response

#登入系統
def forget(request):
    return render(request, 'forget.html')

def test(request):
    return render(request, 'generated_text.html')

def test2(request):
    return render(request, 'input_form.html')

def user_authentication(request):
    if request.method == 'POST':
        # 如果表单提交的数据中包含 'register' 参数，则执行注册操作
        if 'register' in request.POST:
            return user_register(request)
        # 否则执行登录操作
        elif 'login' in request.POST:
            return loginpage(request)
    # 如果是 GET 请求，或者表单提交的数据中既没有 'register' 也没有 'login' 参数，就渲染登录页面
    error = 'Passwords do not match.'
    return render(request, 'login.html')

#登入
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render  # 導入 render 函數
from django.contrib import messages
from django.contrib.auth import  login, logout

def loginpage(request): 
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=password)  # 使用正確的字段名稱
        if user is not None:
            login(request, user) 
            return HttpResponseRedirect('/index/')  # 登入成功後重定向到首頁
        else:
            error = '帳號密碼錯誤'
            return render(request, 'login.html', {'error': error})
    context = {}
    return render(request, 'login.html', context)

def index(request):
    return render(request, 'index.html')
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/index')

#註冊
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login

def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        birthday = request.POST.get('date')
        birthday_time = request.POST.get('time')
        sex = request.POST.get('sex')  # 取得性別

        # 檢查電子郵件是否已存在
        if User.objects.filter(email=email).exists():
            error = 'Email 已被註冊'
            return render(request, 'login.html', {'error': error})

        # 檢查用戶名是否已存在
        if User.objects.filter(username=username).exists():
            error = 'Username 已被註冊'
            return render(request, 'login.html', {'error': error})

        elif password1 == password2:
            user = User.objects.create_user(username=username, password=password1, email=email)
            user = User.objects.get(username=username)
            Customer.objects.create(user=user, birthday=birthday, birthday_time=birthday_time, sex=sex)  # 將性別加入 Customer 物件
            login(request, user)
            return redirect('/index/')
        else:
            error = 'Passwords do not match.'
            return render(request, 'login.html', {'error': error})
    else:
        error = None
        return render(request, 'login.html', {'error': error})



#聊天室..................................................................................................................
from .models import Chatroom2, Conversation


#進入AI聊天畫面
@login_required
def aichat2(request):
    user = request.user
    chat_messages = user.Conversation_history.all()
    #計算八字
    user_date0 = Customer.objects.get(user=user).birthday
    user_date0 = str(user_date0)
    user_time = '01:30:00'
    all = bazs(user_date0,user_time) 

    # 檢查是否存在預設聊天室
    default_chatroom_exists = Chatroom2.objects.filter(owner=user).exists()
    # 如果不存在，則創建一個新的聊天室
    if not default_chatroom_exists:
        chatroom = Chatroom2.objects.create(name="Default Chatroom", owner=user)
        selected_chatroom = chatroom # 設置為預選聊天室
        chatrooms = Chatroom2.objects.filter(owner=user)
        return render(request, 'aichat2.html', {'all':all,'chatrooms': chatrooms,'selected_chatroom': selected_chatroom.id})
    else:
        # 如果存在，檢查是否有新增內容，如果沒有，則刪除聊天室
        chatrooms = Chatroom2.objects.filter(owner=user).order_by('-updated_at')
        if chatrooms.count() == 1:
            chatroom = chatrooms.first()
        else:
            # 找到多個聊天室，選擇最新的聊天室            
            for chatroom in chatrooms:
                if (Chatroom2.objects.filter(owner=user).order_by('-updated_at')).count() > 1:
                    if chatroom.conversation_set.count() == 0:
                        chatroom.delete()
            chatroom = chatrooms.order_by('-updated_at').first()
        selected_chatroom = chatroom
        # 獲取該聊天室的最新對話
        chatrooms = Chatroom2.objects.filter(owner=user)
        #命盤訊息    
        return render(request, 'aichat2.html', {'chat_messages': chat_messages ,'chatrooms': chatrooms,'all':all,'selected_chatroom': selected_chatroom.id})


#取得聊天室訊息
@login_required
def get_chat_messages(request, chatroom_id):
    # 獲取該聊天室的所有聊天記錄
    messages = Conversation.objects.filter(chatroom_id=chatroom_id,user=request.user)   
    # 將聊天記錄轉換為 JSON 格式
    data = [{'user_question': message.user_question, 'ai_answer': message.ai_answer} for message in messages]   
    return JsonResponse(data, safe=False)

#訊息丟入AI跟資料庫
def send_message(request):
    if request.method == 'GET':
        message = request.GET.get('message')
        chatroomId = request.GET.get('chatroomId')
        modeltype = request.GET.get('modeltype')
        user = request.user
        user_date0 = Customer.objects.get(user=user).birthday
        user_date0 = str(user_date0)
        user_date = user_date0
        user_time = '01:30:00'
        w1,w2,w3,w4,s1,r1,r2,r3,r4,r6,r7,r8 = bazs(user_date,user_time) 
        d5 = w3[0]
        user_data = "%s年 %s月 %s日 %s時，十神分別是:年干為%s、年支為%s、月干為%s、月支為%s、日干%s為本元、日支為%s、時干為%s、時支為%s。"%(w1,w2,w3,w4,r1,r2,r3,r4,d5,r6,r7,r8)
        print(user_data)
        #print(modeltype)
        # 查詢對應的聊天室
        chatroom = Chatroom2.objects.get(id=chatroomId)
        print(chatroom)
        Conversation_history = Conversation.objects.filter(user=user, chatroom=chatroom).order_by('timestamp')
        conversation = ""
        for msg in Conversation_history:
            if msg.user_question:
                conversation += f"User: {msg.user_question}\n"
            if msg.ai_answer:
                conversation += f"Assistant: {msg.ai_answer}\n"   
        # 將之前的聊天記錄和當前用戶的問題組合成 prompt
        historical_record = f"{conversation}User: {message}\nAssistant:"
        prompt = "我的資訊：" + user_data+"對話:" + historical_record 
        #prompt =historical_record 
        #print(prompt)

        if modeltype == "1":
            # 使用GPT-3生成回復
            assistant_message = GPT_response4o(prompt)
            read_text = "Q:"+message+"\n"+"A:"+assistant_message

            #print("read_text"+"\n"+read_text)
            #print(read_text )
            # 使用生成器函數生成流式回覆
            def chat_stream(prompt, user, chatroom):
                client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
                stream = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "你是一個命理諮詢師，用引導的方式，我會給你一個對話，幫我把回答的內容豐富點、更有趣，你要扮演回答的位置，將原本的A不改語意方式改寫，用你的對話來取代A，不要重複Q以及直接回答不要有A"},
                        {"role": "user", "content": prompt}
                    ],
                    stream=True,
                    temperature=1,
                    max_tokens=4096,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0,
                )
                global x 
                x =""
                for chunk in stream:
                    content = chunk.choices[0].delta.content
                    x +=  str(content)
                    #print(x)
                    if x.endswith("None"):
                        assistant_message = x.replace("None","")
                        #print(assistant_message)                  
                    if content:
                        yield content
                Conversation.objects.create(
                    user=user,
                    chatroom=chatroom, 
                    user_question=message, 
                    ai_answer=assistant_message
                )
            response = StreamingHttpResponse(chat_stream(read_text, user, chatroom), content_type='text/event-stream')
            #response = HttpResponse(assistant_message)
        else:
            def breeze(prompt):
                # Point to the local server
                client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

                completion = client.chat.completions.create(
                model="Breeze FT/breeze ft",
                messages=[
                    {"role": "system", "content": "這是一個基於四柱八字的聊天機器人，旨在提供洞察力強的讀數與事實信息相結合。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                )
                # 给定字符串
                string = str(completion.choices[0].message)
                # 使用 split() 函数分割字符串
                content_start = string.find("content=")
                content_end = string.find(", role=")
                content = string[content_start + len("content=\""):content_end - 1]              
                # 打印提取的内容
                return content
            assistant_message = breeze(prompt)           
            Conversation.objects.create(
                user=user,
                chatroom=chatroom, 
                user_question=message, 
                ai_answer=assistant_message
            )

            response = StreamingHttpResponse(breeze(prompt), content_type='text/event-stream')
            #print(breeze)
            #response = HttpResponse(assistant_message)        
        # 保存用戶消息和AI生成的回復       
    return response

from django.views.decorators.http import require_POST

# 創建新的聊天室
@login_required
@require_POST
def create_chatroom(request):
    user = request.user
    #chatroom_name = request.POST.get('name', 'New Chat')
    chatroom_number = Chatroom2.objects.filter(owner=user).count()
    chatroom_name = f"New Chat {chatroom_number+1}"
    print(chatroom_number)

    # 創建新的聊天室
    chatroom = Chatroom2.objects.create(
        name=chatroom_name,
        owner=user
    )

    return JsonResponse({'success': True, 'id': chatroom.id, 'name': chatroom.name})

# 重新命名
@require_POST
def rename_chatroom(request, chatroom_id):
    user = request.user
    try:
        # 获取 POST 数据中的新名称
        data = json.loads(request.body)
        new_name = data.get('newName')
        # 根据 chatroom_id 获取相应的聊天室对象
        chatroom = Chatroom2.objects.get(id=chatroom_id , owner=user)
        # 更新聊天室名称
        chatroom.name = new_name
        chatroom.save()
        # 返回成功响应
        return JsonResponse({'success': True})
    except Exception as e:
        # 如果出现异常，返回错误响应
        return JsonResponse({'success': False, 'error': str(e)})

# 刪除聊天室
@login_required
@require_POST
def delete_chatroom(request):
    user = request.user

    data = json.loads(request.body)
    chatroom_id = data.get('chatroomId')
    print(chatroom_id)

    # 刪除聊天室
    chatroom = Chatroom2.objects.get(id=chatroom_id, owner=user)
    chatroom.delete()
    return JsonResponse({'success': True})



#..................................................................................................................
#書籍處理

 
def bookpage(request):
    books = models.book.objects.all().order_by('bookID')
    #for booke in books:
        #print(booke.bookID)

    return render(request, 'book.html',{'books': books})



def book_detail(request, book_id):
    #print(book_id)
    book_obj = models.book.objects.get(bookID=book_id)
    #print(book_obj)
    chapters = models.chapter.objects.filter(book=book_obj).order_by('chapterID')
    #print(chapters)
    context = {
        'book': book_obj,
        'chapters': chapters,
    }
    return render(request, 'book1.html', context)

def book1(request):
    return render(request, 'book1.html')


#歷史紀錄
from django.shortcuts import render  # 導入 render 函數

from django.contrib.auth.models import User
from django.contrib.auth import login
from mysite.models import Customer


def aboutme(request):
    username = request.POST.get('username')
    
    birthday = Customer.objects.get(user=request.user)

    return render(request, 'aboutme.html', { 'birthday': birthday, 'birthday_time': birthday.birthday_time,'sex': birthday.sex})

#--------------------------------------------------------------------------------------------
# 改個人的資料
from django.shortcuts import render, redirect
from .models import Customer

@login_required
def update_birthday(request):
    if request.method == 'POST':
        # 获取提交的新生日
        new_birthday = request.POST.get('Bth')

        # 获取当前用户的生日记录
        birthday = Customer.objects.get(user=request.user)

        # 更新生日记录
        birthday.birthday = new_birthday
        birthday.save()

        # 重定向到其他页面或返回成功消息
        return redirect('aboutme')  

    # 如果不是POST请求,重定向到其他页面
    return redirect('aboutme')


from django.contrib.auth.decorators import login_required
from .models import Customer

@login_required
def update_birthday_time(request):
    if request.method == 'POST':
        # 获取提交的新生日时间
        new_birthday_time = request.POST.get('Bth_tm')

        try:
            
            birthday = Customer.objects.get(user=request.user)
        except Customer.DoesNotExist:
            
            birthday = Customer(user=request.user)

        # 更新生日时间
        birthday.birthday_time = new_birthday_time
        birthday.save()

        # 重定向到其他页面或返回成功消息
        return redirect('aboutme')

    # 如果不是 POST 请求，重定向到其他页面
    return redirect('aboutme')

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Customer

@login_required
def update_sex(request):
    if request.method == 'POST':
        # 获取提交的新性别
        new_sex = request.POST.get('Bth_sex')

        try:
           
            birthday = Customer.objects.get(user=request.user)
        except Customer.DoesNotExist:
           
            birthday = Customer(user=request.user)

        # 更新性别
        birthday.sex = new_sex
        birthday.save()

        # 重定向到其他页面或返回成功消息
        return redirect('aboutme')

    # 如果不是 POST 请求，重定向到其他页面
    return redirect('aboutme')



#登入之後抓這個人的紀錄#
#from django.shortcuts import render
#from mysite.models import TestRecord  # 假设你的测试记录模型是TestRecord

##from django.contrib.auth import login

#每日如果有登入
from django.shortcuts import render, redirect
from mysite.models import Customer
@login_required
def day(request):
    if request.user.is_authenticated:
        # 用户已登录
        if request.method == 'POST':
            birthday = request.POST.get('birthday')
            user_birthday, created = Customer.objects.get_or_create(user=request.user)
            user_birthday.birthday = birthday
            user_birthday.save()
            return redirect('day')
        else:
            try:
                birthday_obj = Customer.objects.get(user=request.user)
                birthday = birthday_obj.birthday
            except Customer.DoesNotExist:
                birthday = None
    else:
        # 用户未登录
        if request.method == 'POST':
            birthday = request.POST.get('birthday')
            # 可以在这里处理未登录用户的生日数据,例如保存在session中
        else:
            birthday = None

    context = {'birthday': {'birthday': birthday}}
    return render(request, 'day.html', context)




from mysite.models import Customer
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required



