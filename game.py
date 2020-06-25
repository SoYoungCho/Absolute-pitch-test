from tkinter import*
from tkinter import messagebox
import tkinter.simpledialog
import pygame
from playsound import playsound
import random
import time
import sqlite3

NUM = 2
level = 'easy'
correct_cnt, wrong_cnt, total_cnt= 0, 0, 0
input_array = []
rand_seed = []
con, cur = None, None
sql = ""
nickname = "player"
window = Tk()
listNameEasy = [None]*5
listNameNormal = [None]*5
listNameHard = [None]*5

listScoreEasy = [None]*5
listScoreNormal = [None]*5
listScoreHard = [None]*5


listLevelEasy = [None]*5
listLevelNormal = [None]*5
listLevelHard = [None]*5

con = sqlite3.connect("gameDB")
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS userTABLE (userName char(15), userLevel char(10), userScore int)")
#DB 없을시 새로 생성. 사용자 이름, 난이도, 최종점수를 저장하는 userTable생성 
#window.geometry("1800x1000")
window.title("절대음감 게임")
window.resizable(width=FALSE, height = FALSE) #사이즈 조절 불가

windowWidth = window.winfo_reqwidth()
windowHeight = window.winfo_reqheight()

# Gets both half the screen width/height and window width/height
x = int((window.winfo_screenwidth()/2 - windowWidth/2)/2)
y = int((window.winfo_screenheight()/2 - windowHeight/2)/2)

class FullScreenApp(object):#전체화면 모드 클래스
    def __init__(self, master, **kwargs):
        self.master=master
        pad=3
        self._geom='200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(
            master.winfo_screenwidth()-pad, master.winfo_screenheight()-pad))
        master.bind('<Escape>',self.toggle_geom)            
    def toggle_geom(self,event):
        geom=self.master.winfo_geometry()
        print(geom,self._geom)
        self.master.geometry(self._geom)
        self._geom=geom

class CreateAccount(tkinter.simpledialog.Dialog):#계정 생성 클래스     
    def body(self, window):
        app = FullScreenApp(self)
        tkinter.Label(window, image = mainphoto).pack(side = TOP, padx=10, pady=30, ipady=30)
        tkinter.Label(window, text="플레이어 이름을 입력해주세요", font=("",25)).pack(side = TOP, padx=10, pady=5, ipady=10)
        self.user_id = tkinter.Entry(window)
        self.user_id.pack(side = TOP, padx=10, pady=10)

    def apply(self): #OK button click event
        global nickname
        nickname =""
        nickname = self.user_id.get()
        play=StartGame()
        play.choose_difficulty()#StartGame 클래스 내 난이도 선택 함수 호출 

class Guide(tkinter.simpledialog.Dialog):#가이드 클래스
    global x
    global y
    
    def body(self, window):
        
        piano_button(window)#연습용 피아노 UI 구현
        tkinter.Label(window, text="위의 건반은 연습용으로 Play버튼을 누르면 랜덤으로 음이 출력됩니다!", font=("",25)).grid(row=7, columnspan =25)
        tkinter.Label(window, text="##절대음감 게임 플레이 방법##", font=("",25)).grid(row=8, columnspan =25)
        tkinter.Label(window, text="난이도별 총 10회의 게임이 진행됩니다.", font=("",15)).grid(row=9, columnspan =25)
        tkinter.Label(window, text="들려주는 피아노의 음을 듣고 어떤 음인지 맞춰보세요!", font=("",15)).grid(row=10, columnspan =25)
        tkinter.Label(window, text="Replay버튼을 누르면 원하는 음을 딱 한 번 더 들을 수 있습니다.", font=("",15)).grid(row=11, columnspan =25)
        tkinter.Label(window, text="----------------------난이도 설명----------------------", font=("",15)).grid(row=12, columnspan =25)
        tkinter.Label(window, text="EASY : 흰색 건반에서 한 음정", font=("",15)).grid(row=13, columnspan =25)
        tkinter.Label(window, text="NORMAL : 흰색 건반에서 두 음정", font=("",15)).grid(row=14, columnspan =25)
        tkinter.Label(window, text="HARD : 흰/검 건반에서 두 음정", font=("",15)).grid(row=15, columnspan =25)
        tkinter.Label(window, text="------------------------------------------------------", font=("",15)).grid(row=16, columnspan =25)
        #게임 방법 설명
    def apply(self):
        quit
        
class Ranking(tkinter.simpledialog.Dialog): #랭킹 확인용 Dialog
    global listNameEasy
    global listNameNormal
    global listNameHard
    global listLevelEasy
    global listLevelNormal
    global listLevelHard
    global listScoreEasy
    global listScoreNormal
    global listScoreHard
    global x
    global y
    i = 0
    j = 0
    
    
    def body(self, window):
        tkinter.Label(window, text="Easy 랭킹", font=("",40)).grid(row=0, columnspan = 3)
        tkinter.Label(window, text="-----------------------------------", font=("",30)).grid(row=1, columnspan=3)
        for i in range(5):  #점수에 따라 상위 5명의 정보만 가져옴
            tkinter.Label(window, text=str(i+1)+"위    " + listNameEasy[i], font=("",20)).grid(row=i+2, column = 0, sticky="w")
            tkinter.Label(window, text="    난이도 " + listLevelEasy[i]+ "    ", font=("",20)).grid(row=i+2, column = 1, sticky="w")
            tkinter.Label(window, text=str(listScoreEasy[i])+"점/10개", font=("",20)).grid(row=i+2, column = 2, sticky="e")
        

        tkinter.Label(window, text="-----------------------------------", font=("",30)).grid(row=7, columnspan=3)
        i = 0
        j = 0
        tkinter.Label(window, text="Normal 랭킹", font=("",40)).grid(row=8, columnspan = 3)
        tkinter.Label(window, text="-----------------------------------", font=("",30)).grid(row=9, columnspan=3)
        for i in range(5):  #점수에 따라 상위 5명의 정보만 가져옴
            tkinter.Label(window, text=str(i+1)+"위    " + listNameNormal[i], font=("",20)).grid(row=i+10, column = 0, sticky="w")
            tkinter.Label(window, text="    난이도 " + listLevelNormal[i]+ "    ", font=("",20)).grid(row=i+10, column = 1, sticky="w")
            tkinter.Label(window, text=str(listScoreNormal[i])+"점/10개", font=("",20)).grid(row=i+10, column = 2, sticky="e")

        tkinter.Label(window, text="-----------------------------------", font=("",30)).grid(row=15, columnspan=3)
        i = 0
        j = 0
        tkinter.Label(window, text="Hard 랭킹", font=("",40)).grid(row=16, columnspan = 3)
        tkinter.Label(window, text="-----------------------------------", font=("",30)).grid(row=17, columnspan=3)
        for i in range(5):  #점수에 따라 상위 5명의 정보만 가져옴
            tkinter.Label(window, text=str(i+1)+"위    " + listNameHard[i], font=("",20)).grid(row=i+18, column = 0, sticky="w")
            tkinter.Label(window, text="    난이도 " + listLevelHard[i]+ "    ", font=("",20)).grid(row=i+18, column = 1, sticky="w")
            tkinter.Label(window, text=str(listScoreHard[i])+"점/10개", font=("",20)).grid(row=i+18, column = 2, sticky="e")

        tkinter.Label(window, text="-----------------------------------", font=("",30)).grid(row=23, columnspan=3)
        
    def apply(self):
        quit

class round_over(tkinter.simpledialog.Dialog):#가이드 클래스
    global level
    global nickname
    global sql
    global correct_cnt
    
    def body(self, window):
        tkinter.Label(window, text="------------------------------------------", font=("",20)).grid(row=0, columnspan=2)
        tkinter.Label(window, text="난이도 " + str(level) +" 게임 종료!", font=("",25)).grid(row=1,columnspan=2)
        tkinter.Label(window, text= nickname +"님 최종점수: 10개 중 "+ str(correct_cnt) + "개 맞추셨습니다.", font=("", 25)).grid(row=2, columnspan=2)
        tkinter.Label(window, text="------------------------------------------", font=("",20)).grid(row=3, columnspan=2)
    def apply(self):# OK button click event
        sql = "INSERT INTO userTable VALUES('"+nickname+"','"+level+"',"+str(correct_cnt)+")" #사용자의 닉네임,난이도, 점수를 DB에 추가
        cur.execute(sql)
        con.commit()
        con.execute("SELECT * FROM userTable")
        print(nickname, level, correct_cnt)        
        quit


class StartGame():
    global x
    global y
    def choose_difficulty(self):#난이도 선택 함수
        self.choose=Toplevel()
        app = FullScreenApp(self.choose)
        #window.resizable(width=FALSE, height = FALSE)
        self.label = Label(self.choose, image = mainphoto).pack(side = TOP, padx=10, pady=30, ipady=30)
        self.easy_button = Button(self.choose, text="EASY", font = ("",25), width=40, command = self.startEasy).pack(side = TOP, padx = 30, pady=30, ipady=30)
        self.normal_button = Button(self.choose, text="NORMAL", font=("", 25), width=40, command = self.startNormal).pack(side = TOP, padx = 30, pady=30, ipady=30)
        self.hard_button = Button(self.choose, text="HARD", font=("", 25), width=40, command = self.startHard).pack(side = TOP, padx = 30, pady=30, ipady=30)
        
    def startEasy(self):#easy_button 클릭시
        global level
        level = "easy"
        self.ingame = Toplevel()
        self.choose.destroy()
        self.ingame.geometry("1040x550")
        self.ingame.geometry("+{}+{}".format(x, y))
        piano_button(self.ingame)
        

    def startNormal(self):#normal_button 클릭시
        global level 
        level = "normal"
        self.ingame=Toplevel()
        self.choose.destroy()
        self.ingame.geometry("1040x550")
        self.ingame.geometry("+{}+{}".format(x, y))
        piano_button(self.ingame)
    
    def startHard(self):#hard_button 클릭시
        global level 
        level = "hard"
        self.choose.destroy()
        self.ingame=Toplevel()
        self.ingame.geometry("1040x550")
        self.ingame.geometry("+{}+{}".format(x, y))
        piano_button(self.ingame)

def clickStart():#btnStart버튼 click시 실행
    total_cnt = 0
    correct_cnt = 0
    wrong_cnt = 0
    CreateAccount(window)

def clickHowtoplay():#btnHowtoplay click시 실행
    Guide(window)

def clickRank():#btnRank click시 실행
    global listNameEasy
    global listNameNormal
    global listNameHard
    global listLevelEasy
    global listLevelNormal
    global listLevelHard
    global listScoreEasy
    global listScoreNormal
    global listScoreHard
    i=0
    j=0
    k=0
    
    sql = "SELECT * FROM userTable WHERE userLevel = 'easy'" #level easy인 사용자 DB조회
    cur.execute(sql)
    rank = cur.fetchall()
    rank.sort(key=lambda x:-x[2])
    for i in range (5):
        listNameEasy[i] = rank[i][0]
        listLevelEasy[i] = rank[i][1]
        listScoreEasy[i] = rank[i][2]

    sql = "SELECT * FROM userTable WHERE userLevel = 'normal'" #level normal인 사용자 DB조회
    cur.execute(sql)
    rank = cur.fetchall()
    rank.sort(key=lambda x:-x[2])
    for j in range(5):
        listNameNormal[j] = rank[j][0]
        listLevelNormal[j] = rank[j][1]
        listScoreNormal[j] = rank[j][2]

    sql = "SELECT * FROM userTable WHERE userLevel = 'hard'" #level normal인 사용자 DB조회
    cur.execute(sql)
    rank = cur.fetchall()
    rank.sort(key=lambda x:-x[2])
    for k in range (5):
        listNameHard[k] = rank[k][0]
        listLevelHard[k] = rank[k][1]
        listScoreHard[k] = rank[k][2]
    
    Ranking(window)

#메인화면 UI
btnStart = Button(window, text = "게임시작", font = ("", 25), width=40, command = clickStart)#게임시작 버튼
btnHowtoplay = Button(window, text = "게임방법", font = ("", 25), width = 40, command = clickHowtoplay)#게임방법 버튼 
btnRank = Button(window, text="랭킹", font=("", 25), width = 40, command = clickRank)#랭킹 버튼
btnQuit = Button(window, text="게임종료", font=("", 25), width = 40, command=window.destroy)#종료 버튼
space = Label(window, text="", width=40)

mainphoto = PhotoImage(file = "image/main.png")#메인화면의 이미지
pLabel = Label(window, image=mainphoto)
pLabel.configure(image = mainphoto)
pLabel.image = mainphoto

#라벨과 버튼들을 위에서부터 pack으로 위치 지정
pLabel.pack(side = TOP, pady=15, ipady=15)
btnStart.pack(side = TOP, padx=10, pady=30, ipady=30)
btnHowtoplay.pack(side = TOP, padx=10, pady=30, ipady=30)
btnRank.pack(side = TOP, padx=10, pady=30, ipady=30)
btnQuit.pack(side = TOP, padx=10, pady=30, ipady=30)
space.pack(side=TOP)
app = FullScreenApp(window)#전체모드로 화면 설정

##################################피아노#######################################

pygame.init()
count = 0
click_num = 0
max_click = 2
rand_seed = []


# 난이도별 랜덤음 생성
def randSound():
    global sound_list
    global rand_seed
    
    sound_list_only_white = ['c3','d3','e3','f3','g3','a3','b3',
                             'c4','d4','e4','f4','g4','a4','b4',
                             'c5','d5','e5','f5','g5','a5','b5']
    sound_list = ['c3','c3s','d3','d3s','e3','f3','f3s','g3','g3s','a3','a3s','b3',
                  'c4','c4s','d4','d4s','e4','f4','f4s','g4','g4s','a4','a4s','b4',
                  'c5','c5s','d5','d5s','e5','f5','f5s','g5','g5s','a5','a5s','b5']
    

    # 난이도 - 하 : 흰건반/단음  
    if level == 'easy':
        global sound
        sound = random.choice(sound_list_only_white)
        rand_seed.append(sound)

    # 난이도 - 중 : 흰건반/여러음    
    elif level == 'normal':
        a = random.sample(range(1,21),2)
        for i in a:
            rand_seed.append(sound_list_only_white[i])
        
    # 난이도 - 상 : 흰건반/검은건반/여러음
    elif level == 'hard':
        a = random.sample(range(1,36),2)
        for i in a:
            rand_seed.append(sound_list[i])

            
# PLAY 버튼 실행 함수            
def click():
    
    global click_num
    global rand_seed
    
    click_num += 1
    
    if click_num <= max_click:

        # 소리 재생
        for i in rand_seed:
            if i in sound_list:
                playsound("wav/" + str(i) + ".wav")
                print("play ", rand_seed)
                
    # 다음 단계 이동 및 초기화
    else:
        rand_seed = []
        click_num = 0     
        randSound()
        click()
        
        
# 정답인지 확인 함수             
def check(음표): # sound 는 계이름
    global correct_cnt
    global wrong_cnt
    global total_cnt
    global rand_seed
    global input_array

    print("function sound is ", rand_seed)
    
    if level == 'easy': # 난이도 - easy
        if sound == note: # 정답을 맞춤
            correct_cnt += 1
            total_cnt += 1
            print("correct count is ", correct_cnt) 
            messagebox.showinfo("Correct","정답은 " + sound + "\n당신이 고른 건반은 " + note +  "\n정답입니다!\n" + str(10-total_cnt) +"회 남았습니다.")
            rand_seed = []
            randSound()
            click_num = 0

        elif sound != note: # 틀림
            total_cnt += 1
            print("total_cnt is ", total_cnt)
            messagebox.showinfo("Wrong", "정답은 " + sound + "\n당신이 고른 건반은 " + note + "\n틀렸습니다!\n"+ str(10-total_cnt)+ "회 남았습니다.")
            rand_seed = []
            randSound()
            click_num = 0
            

            
            
    elif level == 'normal': # 난이도 - normal
        input_array.append(음표) # 입력한 계이름을 배열에 추가
        
        for i in range(len(input_array)):
            print("input array는 ", input_array, "고 rand_seed는 ", rand_seed)
            
            if rand_seed[i] == input_array[i]: # 정답을 맞춤
                if len(input_array) == 1:
                    pass
                
                elif len(input_array) == 2 and rand_seed[1] == input_array[1]:
                    correct_cnt += 1
                    total_cnt += 1
                    messagebox.showinfo("Correct","정답은 " + sound + "\n당신이 고른 건반은 " + note +  "\n정답입니다!\n" + str(10-total_cnt) +"회 남았습니다.")
                    rand_seed = []
                    input_array = []
                    randSound()
                    click_num = 0
                    print("correct count is ", correct_cnt)
                    print("total_cnt is ", total_cnt)
                    break

            else: # 틀림
                print("wrong, input array is ", input_array)
                total_cnt += 1
                print("total_cnt is ", total_cnt)
                messagebox.showinfo("Wrong", "정답은 " + sound + "\n당신이 고른 건반은 " + note + "\n틀렸습니다!\n"+ str(10-total_cnt)+ "회 남았습니다.")
                rand_seed = []
                input_array = []
                randSound()
                click_num = 0
                print("total_cnt is ", total_cnt)
                break

            
    elif level == 'hard': # 난이도 - hard
        input_array.append(음표) # 입력한 계이름을 배열에 추가
        
        for i in range(len(input_array)):
            print("input array는 ", input_array,"고 rand_seed는 ",rand_seed)
            if rand_seed[i] == input_array[i]: # 정답을 맞춤
                if len(input_array) == 1:
                    pass
                elif len(input_array) == 2 and rand_seed[1] == input_array[1]:
                    correct_cnt += 1
                    total_cnt += 1
                    messagebox.showinfo("Correct","정답은 " + sound + "\n당신이 고른 건반은 " + note +  "\n정답입니다!\n" + str(10-total_cnt) +"회 남았습니다.")
                    rand_seed = []
                    input_array = []
                    randSound()
                    click_num = 0
                    print("correct count is ", correct_cnt)
                    print("total_cnt is ", total_cnt)
                    break

            else: # 틀림
                print("wrong, input array is ", input_array)
                total_cnt += 1
                print("total_cnt is ", total_cnt)
                messagebox.showinfo("Wrong", "정답은 " + sound + "\n당신이 고른 건반은 " + note + "\n틀렸습니다!\n"+ str(10-total_cnt)+ "회 남았습니다.")
                rand_seed = []
                rand_seed = []
                input_array = []
                randSound()
                click_num = 0
                print("total_cnt is ", total_cnt)
                break

    if total_cnt == 10: 
        total_cnt = 0
        correct_cnt = 0
        print("끝났음")
        round_over(window)
        

        
# 건반 사운드 출력 함수 - 옥타브 3
def note_C3():
    sound = pygame.mixer.Sound("wav/c3.wav")
    sound.play()
    check("c3")

def note_CC3():
    sound = pygame.mixer.Sound("wav/c3s.wav")
    sound.play()
    check("c3s")

def note_D3():
    sound = pygame.mixer.Sound("wav/d3.wav")
    sound.play()
    check("d3")

def note_DD3():
    sound = pygame.mixer.Sound("wav/d3s.wav")
    sound.play()
    check("d3s")
    
def note_E3():
    sound = pygame.mixer.Sound("wav/e3.wav")
    sound.play()
    check("e3")

def note_F3():
    sound = pygame.mixer.Sound("wav/f3.wav")
    sound.play()
    check("f3")

def note_FF3():
    sound = pygame.mixer.Sound("wav/f3s.wav")
    sound.play()
    check("f3s")

def note_G3():
    sound = pygame.mixer.Sound("wav/g3.wav")
    sound.play()
    check("g3")
    
def note_GG3():
    sound = pygame.mixer.Sound("wav/g3s.wav")
    sound.play()
    check("g3s")    

def note_A3():
    sound = pygame.mixer.Sound("wav/a3.wav")
    sound.play()
    check("a3")

def note_AA3():
    sound = pygame.mixer.Sound("wav/a3s.wav")
    sound.play()
    check("a3s")

def note_B3():
    sound = pygame.mixer.Sound("wav/b3.wav")
    sound.play()
    check("b3") 

    
#건반 사운드 출력 함수 - 옥타브 4
def note_C4():
    sound = pygame.mixer.Sound("wav/c4.wav")
    sound.play()
    check("c4")

def note_CC4():
    sound = pygame.mixer.Sound("wav/c4s.wav")
    sound.play()
    check("c4s")

def note_D4():
    sound = pygame.mixer.Sound("wav/d4.wav")
    sound.play()
    check("d4")

def note_DD4():
    sound = pygame.mixer.Sound("wav/d4s.wav")
    sound.play()
    check("d4s")
    
def note_E4():
    sound = pygame.mixer.Sound("wav/e4.wav")
    sound.play()
    check("e4")

def note_F4():
    sound = pygame.mixer.Sound("wav/f4.wav")
    sound.play()
    check("f4")

def note_FF4():
    sound = pygame.mixer.Sound("wav/f4s.wav")
    sound.play()
    check("f4s")

def note_G4():
    sound = pygame.mixer.Sound("wav/g4.wav")
    sound.play()
    check("g4")
    
def note_GG4():
    sound = pygame.mixer.Sound("wav/g4s.wav")
    sound.play()
    check("g4s")    

def note_A4():
    sound = pygame.mixer.Sound("wav/a4.wav")
    sound.play()
    check("a4")

def note_AA4():
    sound = pygame.mixer.Sound("wav/a4s.wav")
    sound.play()
    check("a4s")

def note_B4():
    sound = pygame.mixer.Sound("wav/b4.wav")
    sound.play()
    check("b4")    


# 건반 사운드 출력 함수 - 옥타브 5
def note_C5():
    sound = pygame.mixer.Sound("wav/c5.wav")
    sound.play()
    check("c5")

def note_CC5():
    sound = pygame.mixer.Sound("wav/c5s.wav")
    sound.play()
    check("c5s")

def note_D5():
    sound = pygame.mixer.Sound("wav/d5.wav")
    sound.play()
    check("d5")

def note_DD5():
    sound = pygame.mixer.Sound("wav/d5s.wav")
    sound.play()
    check("d5s")
    
def note_E5():
    sound = pygame.mixer.Sound("wav/e5.wav")
    sound.play()
    check("e5")

def note_F5():
    sound = pygame.mixer.Sound("wav/f5.wav")
    sound.play()
    check("f5")

def note_FF5():
    sound = pygame.mixer.Sound("wav/f5s.wav")
    sound.play()
    check("f5s")

def note_G5():
    sound = pygame.mixer.Sound("wav/g5.wav")
    sound.play()
    check("g5")
    
def note_GG5():
    sound = pygame.mixer.Sound("wav/g5s.wav")
    sound.play()
    check("g5s")    

def note_A5():
    sound = pygame.mixer.Sound("wav/a5.wav")
    sound.play()
    check("a5")

def note_AA5():
    sound = pygame.mixer.Sound("wav/a5s.wav")
    sound.play()
    check("a5s")

def note_B5():
    sound = pygame.mixer.Sound("wav/b5.wav")
    sound.play()
    check("b5")    


# 피아노 건반 출력
def piano_button(self):
    global level
    randSound()

    #Positions the window in the center of the page.
    
    
    #Play Sound
    self.play_button = Button(self, text="PLAY", command=click, height=2 , width=117)
    self.play_button.grid(row=0 , columnspan=55)  


    #Buttons for keyboard         
    self.C_3_button = Button(self, bg="white", command=note_C3, height=10, width=5)
    self.C_3_button.grid(row=5,column=0)

    self.CC_3_button = Button(self ,bg="black", fg="white",command=note_CC3 ,height=10 ,width=4)
    self.CC_3_button.grid(row=1,columnspan=2)

    self.DD_3_button = Button(self ,bg="black", fg="white" ,command=note_DD3,height=10 ,width=4)
    self.DD_3_button.grid(row=1,columnspan=4)

    self.D_3_button = Button(self, bg="white", command=note_D3,height=10 , width=5)
    self.D_3_button.grid(row=5 , column=1)

    self.E_3_button = Button(self, bg="white", command=note_E3,height=10 , width=5)
    self.E_3_button.grid(row=5 , column=2)

    self.F_3_button = Button(self, bg="white", command=note_F3,height=10 , width=5)
    self.F_3_button.grid(row=5 , column=3)

    self.FF_3_button = Button(self , bg="black", fg="white", command=note_FF3, height=10 ,width=4)
    self.FF_3_button.grid(row=1,column=3 ,columnspan=2)

    self.G_3_button = Button(self, bg="white" ,command=note_G3, height=10 , width=5)
    self.G_3_button.grid(row=5 , column=4)

    self.GG_3_button = Button(self,bg="black" ,fg="white", command=note_GG3,height=10 ,width=4)
    self.GG_3_button.grid(row=1, column = 4 , columnspan=2)

    self.A_3_button = Button(self, bg="white" ,command=note_A3,height=10 , width=5)
    self.A_3_button.grid(row=5 , column=5)

    self.AA_3_button = Button(self,bg="black" ,fg="white", command=note_AA3, height=10 ,width=4)
    self.AA_3_button.grid(row=1, column = 5 , columnspan=2)

    self.B_3_button = Button(self, bg="white",command=note_B3, height=10 , width=5)
    self.B_3_button.grid(row=5 , column=6)



    #Buttons for keyboard 2nd Octave   
    self.C_4_button = Button(self, bg="white",command=note_C4, height=10, width=5)
    self.C_4_button.grid(row=5,column=7)

    self.CC_4_button = Button(self ,bg="black" , fg="white",command=note_CC4 ,height=10 ,width=4)
    self.CC_4_button.grid(row=1, column = 6 , columnspan=4)

    self.DD_4_button = Button(self ,bg="black" , fg="white",command=note_DD4,height=10 ,width=4)
    self.DD_4_button.grid(row=1, column = 7, columnspan=4)

    self.D_4_button = Button(self, bg="white",command=note_D4,height=10 , width=5)
    self.D_4_button.grid(row=5 , column=8)

    self.E_4_button = Button(self, bg="white", command=note_E4,height=10 , width=5)
    self.E_4_button.grid(row=5 , column=9)

    self.F_4_button = Button(self, bg="white",command=note_F4,height=10 , width=5)
    self.F_4_button.grid(row=5 , column=10)

    self.FF_4_button = Button(self , bg="black", fg="white", command=note_FF4,height=10 ,width=4)
    self.FF_4_button.grid(row=1, column = 8, columnspan=6)

    self.G_4_button = Button(self, bg="white",command=note_G4,height=10 , width=5)
    self.G_4_button.grid(row=5 , column=11)

    self.GG_4_button = Button(self,bg="black" ,fg="white", command=note_GG4,height=10 ,width=4)
    self.GG_4_button.grid(row=1, column = 9, columnspan=6)

    self.A_4_button = Button(self, bg="white",command=note_A4,height=10 , width=5)
    self.A_4_button.grid(row=5 , column=12)

    self.AA_4_button = Button(self,bg="black" ,fg="white", command=note_AA4,height=10 ,width=4)
    self.AA_4_button.grid(row=1, column = 10, columnspan=6)

    self.B_4_button = Button(self, bg="white" ,command=note_B4,height=10 , width=5)
    self.B_4_button.grid(row=5 , column=13)

    
    #Buttons for keyboard 3rd Octave   
    self.C_5_button = Button(self, bg="white",command=note_C5 ,height=10, width=5)
    self.C_5_button.grid(row=5,column=14)

    self.CC_5_button = Button(self ,bg="black" , fg="white",command=note_CC5 ,height=10 ,width=4)
    self.CC_5_button.grid(row=1, column = 11 , columnspan=8)

    self.DD_5_button = Button(self ,bg="black" , fg="white",command=note_DD5,height=10 ,width=4)
    self.DD_5_button.grid(row=1, column = 12, columnspan=8)

    self.D_5_button = Button(self, bg="white",command=note_D5,height=10 , width=5)
    self.D_5_button.grid(row=5 , column=15)

    self.E_5_button = Button(self, bg="white", command=note_E5,height=10 , width=5)
    self.E_5_button.grid(row=5 , column=16)

    self.F_5_button = Button(self, bg="white",command=note_F5,height=10 , width=5)
    self.F_5_button.grid(row=5 , column=17)

    self.FF_5_button = Button(self , bg="black", fg="white", command=note_FF5,height=10 ,width=4)
    self.FF_5_button.grid(row=1, column = 15, columnspan=10)

    self.G_5_button = Button(self, bg="white",command=note_G5,height=10 , width=5)
    self.G_5_button.grid(row=5 , column=18)

    self.GG_5_button = Button(self,bg="black" ,fg="white", command=note_GG5,height=10 ,width=4)
    self.GG_5_button.grid(row=1, column = 17, columnspan=10)

    self.A_5_button = Button(self, bg="white",command=note_A5,height=10 , width=5)
    self.A_5_button.grid(row=5 , column=19)

    self.AA_5_button = Button(self,bg="black" ,fg="white", command=note_AA5,height=10 ,width=4)
    self.AA_5_button.grid(row=1, column = 19, columnspan=10)
    
    self.B_5_button = Button(self, bg="white",command=note_B5 ,height=10, width=5)
    self.B_5_button.grid(row=5 , column=20)

    self.Label1 = Label(self)
    self.Label1.grid(row=6, columnspan = 25)
    self.Label2=Label(self, text="play버튼을 누르면 피아노 소리가 재생됩니다.", font=("",15))
    self.Label2.grid(row=7, columnspan =25)
    self.Label3=Label(self, text="최대 2번까지 들을 수 있습니다.", font=("",15))
    self.Label3.grid(row=8, columnspan =25)
    self.Label4=Label(self, text="총 10회 진행됩니다.", font=("",15))
    self.Label4.grid(row=9, columnspan =25)
    self.Label5=Label(self, text=level, font=("",20))
    self.Label5.grid(row=10, columnspan =25)
window.mainloop()
