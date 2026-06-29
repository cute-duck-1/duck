coins = 0
level = 1
attack = 1
luck = 0
skillLevel = 1
monsterHp = 10
monsterMaxHp = 10
shopOpen = False
skillReady = True
hero: Sprite = None
monster: Sprite = None
scene.set_background_color(7)
info.set_score(0)
info.set_life(3)
hero = sprites.create(img("""
        . . . . . . . .
        . . 9 9 9 9 . .
        . 9 9 9 9 9 9 .
        . 9 f 9 9 f 9 .
        . 9 9 9 9 9 9 .
        . . 9 9 9 9 . .
        . . 9 . . 9 . .
        """),
    SpriteKind.player)
hero.set_position(35, 60)
monster = sprites.create(img("""
        . . . . . . . .
        . . 2 2 2 2 . .
        . 2 2 f 2 f 2 .
        . 2 2 2 2 2 2 .
        . . 2 2 2 2 . .
        . . . 2 2 . . .
        """),
    SpriteKind.enemy)
monster.set_position(120, 60)
def updateText():
    info.set_score(coins)
    monster.say_text("HP: " + str(monsterHp) + "/" + str(monsterMaxHp), 500)
def newMonster():
    global level, monsterMaxHp, monsterHp
    level += 1
    monsterMaxHp = 10 + level * 8
    monsterHp = monsterMaxHp
    monster.set_position(120, 60)
    monster.say_text("레벨 " + str(level) + " 몬스터!", 1000)
    updateText()
def attackMonster():
    global monsterHp, coins
    monsterHp -= attack
    monster.start_effect(effects.disintegrate, 100)
    hero.start_effect(effects.fire, 100)
    if monsterHp <= 0:
        reward = 10 + level * 5 + luck
        coins += reward
        monster.say_text("+" + str(reward) + " 코인!", 1000)
        newMonster()
    else:
        updateText()
# A: 공격 또는 상점 구매

def on_a_pressed():
    global coins, attack, shopOpen
    if shopOpen:
        if attack < 20 and coins >= attack * 30:
            coins -= attack * 30
            attack += 1
            game.show_long_text("공격력 업! 공격력: " + str(attack), DialogLayout.BOTTOM)
        else:
            game.show_long_text("코인이 부족하거나 최대 레벨이야.", DialogLayout.BOTTOM)
        shopOpen = False
        updateText()
    else:
        attackMonster()
controller.A.on_event(ControllerButtonEvent.PRESSED, on_a_pressed)

# B: 상점 열기

def on_b_pressed():
    global shopOpen
    shopOpen = True
    game.show_long_text("상점!\nA: 공격력 +1\n가격: " + str((attack * 30)) + " 코인",
        DialogLayout.BOTTOM)
controller.B.on_event(ControllerButtonEvent.PRESSED, on_b_pressed)

# 스킬: A+B 같이 누르기

def my_function():
    global shopOpen, skillReady, monsterHp, coins
    if skillReady and not shopOpen:
        skillReady = False
        skillDamage = attack * (2 + skillLevel)
        monsterHp -= skillDamage
        monster.start_effect(effects.ashes, 500)
        game.show_long_text("파워 스킬! " + str(skillDamage) + " 데미지!", DialogLayout.BOTTOM)
        if monsterHp <= 0:
            reward2 = 10 + level * 5 + luck
            coins += reward2
            newMonster()
        else:
            updateText()
        pause(3000)
        skillReady = True
        game.show_long_text("스킬 준비 완료!", DialogLayout.BOTTOM)
controller.AB.onEvent(ControllerButtonEvent.PRESSED, my_function)

game.splash("성장형 몬스터 게임")
game.show_long_text("A: 공)