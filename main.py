import pygame as pg
import random
import time
import json
# Инициализация pg
pg.init()

# Размеры окна
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 550
FPS=60

def load_image(file,width,height):
    image = pg.image.load(file).convert_alpha()
    image = pg.transform.scale(image, (width,height))
    return image
def text_render(text):
    return font.render(str(text),True,"black")


ICON_SIZE=80
PADDING=20
DOG_SIZE=(310,500)

BUTTON_WIDTH=200
BUTTON_HEIGHT=60

FOOD_SIZE=200

TOY_SIZE=100

BUTTON_NAV_XPAD=90
BUTTON_NAV_YPAD=130

MENU_NAV_XPAD=90
MENU_NAV_YPAD=130
font=pg.font.Font(None,40)
mini_font=pg.font.Font(None,15)
maxi_font=pg.font.Font(None,200)

class Item:
    def __init__(self,name,price,file,is_using,is_bought):
        self.name=name
        self.price=price
        self.is_using=is_using
        self.is_bought=is_bought
        self.file=file
        self.image=load_image(file,DOG_SIZE[0]//1.7,DOG_SIZE[1]//1.7)
        self.full_image=load_image(file,DOG_SIZE[0],DOG_SIZE[1])
class ClothesMenu:
    def __init__(self,game, data):
        self.game=game
        self.menu_page=load_image("images/menu/menu_page.png",SCREEN_WIDTH,SCREEN_HEIGHT)
        self.bottom_label_off=load_image("images/menu/bottom_label_off.png",SCREEN_WIDTH,SCREEN_HEIGHT)
        self.bottom_label_on=load_image("images/menu/bottom_label_on.png",SCREEN_WIDTH,SCREEN_HEIGHT)
        self.top_label_off=load_image("images/menu/top_label_off.png",SCREEN_WIDTH,SCREEN_HEIGHT)
        self.top_label_on=load_image("images/menu/top_label_on.png",SCREEN_WIDTH,SCREEN_HEIGHT)
        self.items=[]
        for item in data:
            self.items.append(Item(*item.values()))
        self.current_item=0
        self.item_rect=self.items[0].image.get_rect()
        self.item_rect.center=(SCREEN_WIDTH//2,SCREEN_HEIGHT//2)
        self.last_button=Button("Назад",BUTTON_NAV_XPAD+PADDING,SCREEN_HEIGHT-BUTTON_NAV_YPAD-BUTTON_HEIGHT,width=int(BUTTON_WIDTH//1.2),height=int(BUTTON_HEIGHT//1.2),func=self.to_last)
        self.next_button=Button("Вперёд",SCREEN_WIDTH-BUTTON_NAV_XPAD-BUTTON_WIDTH,SCREEN_HEIGHT-BUTTON_NAV_YPAD-BUTTON_HEIGHT,width=int(BUTTON_WIDTH//1.2),height=int(BUTTON_HEIGHT//1.2),func=self.to_next)
        self.buy_button=Button("Купить",SCREEN_WIDTH//2-BUTTON_WIDTH//2.4,SCREEN_HEIGHT-BUTTON_NAV_YPAD-BUTTON_HEIGHT,width=int(BUTTON_WIDTH//1.2),height=int(BUTTON_HEIGHT//1.2),func=self.buy)
        self.use_button=Button("Надеть",BUTTON_NAV_XPAD+PADDING,SCREEN_HEIGHT-BUTTON_NAV_YPAD*1.5-BUTTON_HEIGHT,width=int(BUTTON_WIDTH//1.2),height=int(BUTTON_HEIGHT//1.2),func=self.use_item)#,func=self.use_item
        self.price_text = text_render(self.items[self.current_item].price)
        self.price_text_rect = self.price_text.get_rect()
        self.price_text_rect.center = (SCREEN_WIDTH // 2, 180)
        self.name_text = text_render(self.items[self.current_item].name)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_rect.center = (SCREEN_WIDTH // 2, 120)
        self.use_text = text_render("Надето")
        self.use_text_rect = self.use_text.get_rect()
        self.use_text_rect.midright = (SCREEN_WIDTH-150, 130)
        self.buy_text = text_render("Куплено")
        self.buy_text_rect = self.buy_text.get_rect()
        self.buy_text_rect.midright = (SCREEN_WIDTH-140, 200)
    def to_last(self):
        if self.current_item!=0:
            self.current_item-=1
    def to_next(self):
        if self.current_item!=len(self.items)-1:
            self.current_item+=1
    def buy(self):
        if self.game.money >= self.items[self.current_item].price:
            self.game.money -= self.items[self.current_item].price
            self.items[self.current_item].is_bought = True
    def use_item(self):
        self.items[self.current_item].is_using = not self.items[self.current_item].is_using
    def update(self):
        self.next_button.update()
        self.last_button.update()
        self.buy_button.update()
        self.use_button.update()
    def is_clicked(self,event):
        self.next_button.is_clicked(event)
        self.last_button.is_clicked(event)
        self.buy_button.is_clicked(event)
        self.use_button.is_clicked(event)
    def draw(self,screen):
        screen.blit(self.menu_page,(0,0))
        screen.blit(self.items[self.current_item].image,self.item_rect)
        if self.items[self.current_item].is_bought:
            screen.blit(self.bottom_label_on,(0,0))
        else:
            screen.blit(self.bottom_label_off,(0,0))
        if self.items[self.current_item].is_using:
            screen.blit(self.top_label_on,(0,0))
        else:
            screen.blit(self.top_label_off,(0,0))
        self.next_button.draw(screen)
        self.last_button.draw(screen)
        self.buy_button.draw(screen)
        self.use_button.draw(screen)
        screen.blit(self.price_text, self.price_text_rect)
        screen.blit(self.name_text, self.name_text_rect)
        screen.blit(self.buy_text, self.buy_text_rect)
        screen.blit(self.use_text, self.use_text_rect)
class Food:
    def __init__(self, name, price, file, satiety, medicine_power=0):
        self.name = name
        self.price = price
        self.satiety = satiety
        self.medicine_power = medicine_power
        self.image=load_image(file,FOOD_SIZE,FOOD_SIZE)
class FoodMenu:
    def __init__(self,game):
        self.game=game
        self.menu_page=load_image("images/menu/menu_page.png",SCREEN_WIDTH,SCREEN_HEIGHT)
        self.bottom_label_off=load_image("images/menu/bottom_label_off.png",SCREEN_WIDTH,SCREEN_HEIGHT)
        self.bottom_label_on=load_image("images/menu/bottom_label_on.png",SCREEN_WIDTH,SCREEN_HEIGHT)
        self.top_label_off=load_image("images/menu/top_label_off.png",SCREEN_WIDTH,SCREEN_HEIGHT)
        self.top_label_on=load_image("images/menu/top_label_on.png",SCREEN_WIDTH,SCREEN_HEIGHT)
        self.items = [Food("Яблоко", 10, "images/food/apple.png", 5),
                      Food("Мясо", 30, "images/food/meat.png", 10), 
                      Food("Корм", 40, "images/food/dog food.png", 15), 
                      Food("Элитный корм", 100, "images/food/dog food elite.png", 25, medicine_power=2),
                      Food("Лекарство", 200, "images/food/medicine.png", 0, medicine_power=16)]
        self.current_item=0
        self.item_rect=self.items[0].image.get_rect()
        self.item_rect.center=(SCREEN_WIDTH//2,SCREEN_HEIGHT//2)
        self.last_button=Button("Назад",BUTTON_NAV_XPAD+PADDING,SCREEN_HEIGHT-BUTTON_NAV_YPAD-BUTTON_HEIGHT,width=int(BUTTON_WIDTH//1.2),height=int(BUTTON_HEIGHT//1.2),func=self.to_last)
        self.next_button=Button("Вперёд",SCREEN_WIDTH-BUTTON_NAV_XPAD-BUTTON_WIDTH,SCREEN_HEIGHT-BUTTON_NAV_YPAD-BUTTON_HEIGHT,width=int(BUTTON_WIDTH//1.2),height=int(BUTTON_HEIGHT//1.2),func=self.to_next)
        self.buy_button=Button("Сьесть",SCREEN_WIDTH//2-BUTTON_WIDTH//2.4,SCREEN_HEIGHT-BUTTON_NAV_YPAD-BUTTON_HEIGHT,width=int(BUTTON_WIDTH//1.2),height=int(BUTTON_HEIGHT//1.2),func=self.buy)
        self.price_text = text_render(self.items[self.current_item].price)
        self.price_text_rect = self.price_text.get_rect()
        self.price_text_rect.center = (SCREEN_WIDTH // 2, 180)
        self.name_text = text_render(self.items[self.current_item].name)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_rect.center = (SCREEN_WIDTH // 2, 120)
    def to_last(self):
        if self.current_item!=0:
            self.current_item-=1
    def to_next(self):
        if self.current_item!=len(self.items)-1:
            self.current_item+=1
    def buy(self):
        if self.game.money >= self.items[self.current_item].price:
            self.game.money -= self.items[self.current_item].price
            self.game.satiety+=self.items[self.current_item].satiety
            if self.game.satiety>100:
                self.game.satiety=100
            self.game.health+=self.items[self.current_item].medicine_power
            if self.game.health>100:
                self.game.health=100
    def update(self):
        self.next_button.update()
        self.last_button.update()
        self.buy_button.update()
    def is_clicked(self,event):
        self.next_button.is_clicked(event)
        self.last_button.is_clicked(event)
        self.buy_button.is_clicked(event)
    def draw(self,screen):
        screen.blit(self.menu_page,(0,0))
        screen.blit(self.items[self.current_item].image,self.item_rect)
        self.next_button.draw(screen)
        self.last_button.draw(screen)
        self.buy_button.draw(screen)
        screen.blit(self.price_text, self.price_text_rect)
        screen.blit(self.name_text, self.name_text_rect)
class Toy(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = load_image("images/toys/ball.png", TOY_SIZE, TOY_SIZE)
        self.rect=self.image.get_rect()
        self.rect.midtop=(MENU_NAV_XPAD+random.randint(0,700)+20,SCREEN_HEIGHT//8)
    def update(self):
        self.rect.top+=2
        if self.rect.top>=SCREEN_HEIGHT:
            self.rect.top=SCREEN_HEIGHT//20+random.randint(0,100)
            self.rect.centerx=MENU_NAV_XPAD+random.randint(0,300)+100
    def draw(self,screen):
        screen.blit(self.image,self.rect)
class Dog(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.width=DOG_SIZE[0]/2
        self.height=DOG_SIZE[1]/2
        self.image = load_image("images/dog.png", self.width, self.height)
        self.rect=self.image.get_rect()
        self.rect.midtop=(SCREEN_WIDTH//2,SCREEN_HEIGHT//2)
    def update(self):
        self.kd=pg.key.get_pressed()
        if self.kd[pg.K_a]:
            self.rect.left-=3
        if self.kd[pg.K_d]:
            self.rect.left+=3
    def draw(self,screen):
        screen.blit(self.image,self.rect)


    
class MiniGame:
    def __init__(self, game):
        self.game=game
        self.background =load_image("images/game_background.png", SCREEN_WIDTH, SCREEN_HEIGHT)
        self.dog=Dog()
        self.toys=pg.sprite.Group()
        self.score = 0
        self.start_time = pg.time.get_ticks()
        self.interval=5000
    def new_game(self):
        self.dog=Dog()
        self.toys=pg.sprite.Group(Toy())
        self.score = 0
        self.start_time = pg.time.get_ticks()
        self.interval=15000
        self.hp=True
    def update(self):
        self.dog.update()
        self.toys.update()
        if random.randint(0,100)>98 and len(self.toys)<10:
            self.toys.add(Toy())
        hits=pg.sprite.spritecollide(self.dog,self.toys,True,pg.sprite.collide_rect_ratio(0.6))
        self.score+=len(hits)
        if pg.time.get_ticks()-self.start_time>self.interval and self.hp:
            self.game.happiness+=int(self.score//2)
            if self.game.happiness>100:self.game.happiness=100
            self.game.mode="Main"
            self.hp=False
    def draw(self,screen):
        screen.blit(self.background,(0,0))
        screen.blit(text_render(self.score),(MENU_NAV_XPAD+20,80))
        self.dog.draw(screen)
        self.toys.draw(screen)
class Button:
    def __init__(self,text, x, y, width=BUTTON_WIDTH,height=BUTTON_HEIGHT,text_font=font,func=None):
        self.func=func
        self.idle_image = load_image("images/button.png", width, height)
        self.pressed_image = load_image("images/button_clicked.png", width, height)
        self.image = self.idle_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.text_font=text_font
        self.text=text_font.render(str(text),True,"black")
        self.text_rect=self.text.get_rect()
        self.text_rect.center=self.rect.center

        self.is_pressed = False

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)
    def update(self):
        mouse_pos=pg.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if self.is_pressed:
                self.image=self.pressed_image
            else:
                self.image=self.idle_image
    def is_clicked(self,event):
        if event.type==pg.MOUSEBUTTONDOWN and event.button==1:
            if self.rect.collidepoint(event.pos):
                self.is_pressed=True
                # try:

                self.func()
                # except:
                #     pass
        elif event.type==pg.MOUSEBUTTONUP and event.button==1:
            self.is_pressed=False
        

class Game:
    def __init__(self):

        # Создание окна
        self.screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pg.display.set_caption("Виртуальный питомец")

        self.background = pg.image.load("images/background.png")
        self.background = pg.transform.scale(self.background, (SCREEN_WIDTH,SCREEN_HEIGHT))

        self.happiness_image=load_image("images/happiness.png",ICON_SIZE,ICON_SIZE)
        self.satiety_image=load_image("images/satiety.png",ICON_SIZE,ICON_SIZE)
        self.health_image=load_image("images/health.png",ICON_SIZE,ICON_SIZE)
        self.money_image=load_image("images/money.png",ICON_SIZE,ICON_SIZE)
        self.dog_image=load_image("images/dog.png",DOG_SIZE[0],DOG_SIZE[1])

        with open("save.json",encoding="utf-8") as f:
            data=json.load(f)

        self.happiness=data["happiness"]
        self.satiety=data["satiety"]
        self.health=data["health"]
        self.money=data["money"]
        self.coins_per_second = data["coins_per_second"]
        self.cost_of_upgrade = {}
        for key, value in data["cost_of_upgrade"].items():
            self.cost_of_upgrade[int(key)]=value
        self.clock=pg.time.Clock()
        
        self.mode="Main"

        self.upgrade_button=Button("Улучшить",SCREEN_WIDTH-ICON_SIZE,0,width=BUTTON_WIDTH//3,height=BUTTON_HEIGHT//3,text_font=mini_font,func=self.increase_money)#

        button_x=SCREEN_WIDTH-BUTTON_WIDTH-PADDING
        self.eat_button=Button("Еда",button_x,PADDING+ICON_SIZE,func=self.food_menu_on)
        self.clothes_button=Button("Одежда",button_x,PADDING*2+ICON_SIZE+BUTTON_HEIGHT,func=self.clothes_menu_on)
        self.game_button=Button("Игры",button_x,PADDING*3+ICON_SIZE+BUTTON_HEIGHT*2,func=self.game_on)
        self.button=[self.eat_button,self.clothes_button,self.game_button,self.upgrade_button]
        
        self.clothes_menu=ClothesMenu(self, data["clothes"])

        self.INCREASE_COINS=pg.USEREVENT+1
        self.DECREASE=pg.USEREVENT+1
        pg.time.set_timer(self.INCREASE_COINS,1000)

        self.food_menu=FoodMenu(self)

        self.mini_game=MiniGame(self)

        self.run()
    def clothes_menu_on(self):
        self.mode="Clothes menu"
    def food_menu_on(self):
        self.mode="Food menu"
    def game_on(self):
        self.mode="Mini game"
        self.mini_game.new_game()
    def run(self):
        while True:
            self.event()
            self.update()
            self.draw()
            self.clock.tick(FPS)
    def increase_money(self):
    	for i in self.cost_of_upgrade.items():
            if self.money>=i[0] and not i[1]:
                self.money-=i[0]
                self.coins_per_second+=1
                self.cost_of_upgrade[i[0]]=True
    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                data={}
                if self.mode=="Game over":
                    data={
                        "happiness":100,
                        "satiety":100,
                        "health":100,
                        "money":0,
                        "coins_per_second":1,
                        "cost_of_upgrade":{
                            "100":False,
                            "1000":False,
                            "5000":False,
                            "10000":False
                        },
                        "clothes":[
                            {
                                "name":"Синяя футболка",
                                "price":10,
                                "image":"images/items/blue t-shirt.png",
                                "is_using":True,
                                "is_bought":True
                            },
                            {
                                "name":"Ботинки",
                                "price":50,
                                "image":"images/items/boots.png",
                                "is_using":False,
                                "is_bought":False
                            },
                            {
                                "name":"Шляпа",
                                "price":50,
                                "image":"images/items/hat.png",
                                "is_using":False,
                                "is_bought":False
                            }
                        ]
                    }
                else:
                    data={
                        "happiness":self.happiness,
                        "satiety":self.satiety,
                        "health":self.health,
                        "money":self.money,
                        "coins_per_second":self.coins_per_second,
                        "cost_of_upgrade":{
                            "100":self.cost_of_upgrade[100],
                            "1000":self.cost_of_upgrade[1000],
                            "5000":self.cost_of_upgrade[5000],
                            "10000":self.cost_of_upgrade[10000]
                        },
                        "clothes":[]
                    }
                    for item in self.clothes_menu.items:
                        data["clothes"].append({
                            "name":item.name,
                            "price":item.price,
                            "image":item.file,
                            "is_using":item.is_using,
                            "is_bought":item.is_bought
                        })
                with open("save.json","w",encoding="utf-8") as f:
                    json.dump(data,f,ensure_ascii=False)
                pg.quit()
                exit()
            if event.type==pg.KEYDOWN:
                if event.key==pg.K_ESCAPE:
                    self.mode="Main"
            if event.type==self.INCREASE_COINS:
                self.money+=self.coins_per_second
            if event.type==self.DECREASE:
                ch=random.randint(1,10)
                if ch<=5:
                    self.satiety-=1
                elif ch>5 and ch<=9:
                    self.happiness-=1
                else:
                    self.health-=1
            if event.type==pg.MOUSEBUTTONDOWN and event.button:
                self.money+=1+self.coins_per_second
            if self.mode=="Main":
                for i in self.button:
                    i.is_clicked(event)
            elif self.mode=="Clothes menu":
                self.clothes_menu.is_clicked(event)
            elif self.mode=="Food menu":
                self.food_menu.is_clicked(event)

    def update(self):
        for i in self.button:
            i.update()
        if self.mode=="Clothes menu":
            self.clothes_menu.update()
        elif self.mode=="Food menu":
            self.food_menu.update()
        elif self.mode=="Mini game":
            self.mini_game.update()
        if self.happiness<=0 or self.satiety<=0 or self.health<=0:
            self.mode="Game over"

    def draw(self):
        self.screen.blit(self.background,(0,0))

        self.screen.blit(self.happiness_image,(PADDING,PADDING))
        self.screen.blit(self.satiety_image,(PADDING,PADDING*2+ICON_SIZE))
        self.screen.blit(self.health_image,(PADDING,PADDING*3+ICON_SIZE*2))
        self.screen.blit(self.money_image,(SCREEN_WIDTH-PADDING-ICON_SIZE,PADDING))
        self.screen.blit(self.dog_image,(SCREEN_WIDTH//2-DOG_SIZE[0]//2,SCREEN_HEIGHT//2-DOG_SIZE[1]//2))

        self.screen.blit(text_render(self.happiness),(PADDING+ICON_SIZE,PADDING*2.3))
        self.screen.blit(text_render(self.satiety),(PADDING+ICON_SIZE,PADDING*3.3+ICON_SIZE))
        self.screen.blit(text_render(self.health),(PADDING+ICON_SIZE,PADDING*4.3+ICON_SIZE*2))
        self.screen.blit(text_render(self.money),(SCREEN_WIDTH-PADDING*2-ICON_SIZE,PADDING*2.3))
        for item in self.clothes_menu.items:
            if item.is_using:
                self.screen.blit(item.full_image, (SCREEN_WIDTH // 2-DOG_SIZE[0] // 2, SCREEN_HEIGHT//2-DOG_SIZE[1]//2))
        for i in self.button:
            i.draw(self.screen)
        if self.mode=="Clothes menu":
            self.clothes_menu.draw(self.screen)
        elif self.mode=="Food menu":
            self.food_menu.draw(self.screen)
        elif self.mode=="Mini game":
            self.mini_game.draw(self.screen)
        if self.mode=="Game over":
            text=maxi_font.render("ПРОИГРЫШ",True,"red")
            text_rect=text.get_rect(center=(SCREEN_WIDTH//2,SCREEN_HEIGHT//2))
            self.screen.blit(text,text_rect)
        pg.display.flip()


if __name__ == "__main__":
    Game()