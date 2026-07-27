from nicegui import ui,app
import asyncio
import random
import time
import os

from nicegui import ui
async def delay():
    await asyncio.sleep(5)
def refresh_page():
    ui.run_javascript('location.reload()')
ui.add_head_html('<script src="https://unpkg.com/@lottiefiles/lottie-player@latest/dist/lottie-player.js"></script>')

with ui.dialog() as win_dialog, ui.card().classes('items-center text-center p-6'):
    ui.label('🏆 CHAMPION! 🏆').classes('text-h4 text-bold text-amber-8')
    ui.html('''
        <lottie-player 
            src="https://assets10.lottiefiles.com/packages/lf20_tou_5x.json" 
            background="transparent" 
            speed="1" 
            style="width: 250px; height: 250px;" 
            autoplay>
        </lottie-player>
    ''')
    ui.label("YOU FINISHED GAME").classes('tex-4xl')
    timewin=ui.label("")

    

with ui.dialog() as lose_dialog, ui.card().classes('items-center text-center p-6 bg-grey-10 text-white'):
    ui.label('💔 GAME OVER 💔').classes('text-h4 text-bold text-negative')
    ui.html('''
        <lottie-player 
            src="https://lottie.host/7e0b5710-1845-48b0-8a16-d446973167df/V0Dq1i8j7L.json" 
            background="transparent" 
            speed="1" 
            style="width: 250px; height: 250px;" 
            autoplay>
        </lottie-player>
    ''')
    ui.label("Don't give up! Give it another shot.").classes('text-subtitle1 text-grey-5 mb-4')



async def show_game_result(status: str):
    global end_time
    if status == 'win':
        end_time=time.time()
        win_dialog.open()
        timewin.set_text(f"in {int((end_time-start_time)//60)} minutes and {int((end_time-start_time)%60)} seconds")
        sound_url = "https://cdn.pixabay.com/download/audio/2025/11/24/audio_a78d073adb.mp3?filename=mrstokes302-you-win-sfx-mrstokes302-442128.mp3"
        ui.run_javascript(f"new Audio('{sound_url}').play();")
        await delay()
        refresh_page()
    elif status == 'lose':
        lose_dialog.open()
        sound_url = "https://cdn.pixabay.com/download/audio/2026/05/03/audio_3bc60193a4.mp3?filename=mrstokes302-you-lose-sfx-mrstokes302-528744.mp3"
        ui.run_javascript(f"new Audio('{sound_url}').play();")
        await delay()
        refresh_page()





# دالة الآلة الكاتبة الصحيحة لـ NiceGUI
async def typewriter(label_element, text: str, delay: float = 0.03):
    current_text = ""
    writing="https://www.soundjay.com/communication_c2026/sounds/computer-keyboard-1.mp3"
    ui.html(f'<audio id="type_sound" src="{writing}" loop></audio>')
    ui.run_javascript('document.getElementById("type_sound").play();')
    
    for char in text:
        current_text += char
        label_element.set_text(current_text) # تحديث عنصر النص الموجود بالفعل
        await asyncio.sleep(delay)   
    ui.run_javascript('document.getElementById("type_sound").pause();')         # انتظر بدون تجميد الواجهة
    
# دالة المقدمة
async def intro(name: str):
    # ننشئ Label واحد للتأثير
    story_label = ui.label().classes('text-base text-slate-300 italic pl-4 border-l-2 border-cyan-500/50')
    
    text = (
        f"Darkness fades... Your suit's AI glitched:\n"
        f"[ WARNING: Critical pressure drop.. Oxygen depleting ]\n"
        f"You open your eyes on the cold, red dust of Mars. Behind you, your ship is a burning wreck. "
        f"In front of you, the dark, silent ruins of the 'Lost Mars Colony' loom in the shadows.\n\n"
        f"Comms are dead. A magnetic storm fried everything. You are entirely alone, and the shadows of corrupted droids are starting to move around the crash site.\n\n"
        f"You have only two choices: scavenge, fight, and build the distress beacon... or let the red dust cover your bones forever.\n\n"
        f"Survival protocol initiated.. Good luck, Astronaut {name}."
    )
    
    # تشغيل تأثير الكتابة
    await typewriter(story_label, text, delay=0.03)

start=ui.card()
with start.classes('w-full bg-slate-900/90 border border-cyan-500/30 rounded-2xl p-6 shadow-2xl backdrop-blur-md relative overflow-hidden'):
    ui.label("START GAME OF SPACE").classes("font-bold text-green-300 text-9xl")
    ui.label("By:Mahmoud Nasr").classes('text-sl')
    name=ui.input("Enter your name:")
    ui.button("START",color='red',on_click=lambda: game()).classes('text-3xl')
game_state = {
    'health': 100,     
    'oxygen': 100,
    'iron': 0,
    'crystal': 0,
    'credits': 0,
    'Tools': [],
    'beacon_parts':0,
    'XP_level': 1.0,
    'y':"",
    'x':"START"
}
Gatekeeper_Alien = ["Gatekeeper_Alien", 30, 200, 10, 5]
Mutant_Explorer = ["Mutant_Explorer", 15, 80, 2, 0]
Broken_Droid = ["Broken_Droid", 5, 20, 0, 0]
enemses = ["none", Broken_Droid, Mutant_Explorer, Gatekeeper_Alien]
e_name = "None"
e_health = 0
e_xp = 0
e_defense = 0
e_thorns = 0
e_xpd = 0
x=4

async def start_cooldown(duration: float = 3.0):
    # Disable button so user can't click multiple times
    global collecting_iron
    collecting_iron.disable()
    exit.disable()
    audio_url = "https://cdn.pixabay.com/download/audio/2026/04/04/audio_09bf283489.mp3?filename=herrparadox-mining_pickaxe_hit_crystal_rock_sharp-514333.mp3"
    ui.html(f'<audio id="type_soun" src="{audio_url}" loop></audio>')
    ui.run_javascript('document.getElementById("type_soun").play();')
    # Show progress bar and status text
    progress_bar.visible = True
    progress_bar.set_value(0.0)

    # 100 steps for smooth animation
    steps = 100
    step_delay = duration / steps

    for step in range(1, steps + 1):
        progress_bar.set_value(step / steps)
        await asyncio.sleep(step_delay)  # Non-blocking delay
    ui.run_javascript('document.getElementById("type_soun").pause();')
    # Reset UI when finished
    
    progress_bar.visible = False
    collecting_iron.enable()
    exit.enable()


dark = ui.dark_mode(True)
async def game():
    global start,b,game_state,lab,progress_bar,status_label,z,v

    start.clear()
    with ui.card().classes('w-full bg-slate-800 text-white p-4 shadow-lg gap-4'):
        
        # شريط الموارد (Iron, Crystal, Credits, Tools)
        with ui.row().classes('w-full items-center justify-between text-base'):
            ui.label('📊 INVENTORY').classes('text-lg font-bold text-cyan-400')
            
            with ui.row().classes('items-center gap-6'):

                with ui.row().classes('items-center gap-1'):
                    ui.label('📡beacon_parts:')
                    ui.label().bind_text_from(game_state, 'beacon_parts', backward=str).classes('font-bold text-red-400')
                with ui.row().classes('items-center gap-1'):
                    ui.label('✨XP:')
                    ui.label().bind_text_from(game_state, 'XP_level', backward=lambda x: f'{x:.2f}').classes('font-bold text-green-300')
                with ui.row().classes('items-center gap-1'):
                    ui.label('⚙️ Iron:')
                    # ربط نص الـ Label بمفتاح 'iron' داخل القاموس تلقائياً
                    ui.label().bind_text_from(game_state, 'iron', backward=str).classes('font-bold text-yellow-400')
                    
                with ui.row().classes('items-center gap-1'):
                    ui.label('💎 Crystal:')
                    ui.label().bind_text_from(game_state, 'crystal', backward=str).classes('font-bold text-cyan-300')
                    
                with ui.row().classes('items-center gap-1'):
                    ui.label('👛 Credits:')
                    ui.label().bind_text_from(game_state, 'credits', backward=lambda c: f"{c:.1f}").classes('font-bold text-green-400')
                    
                with ui.row().classes('items-center gap-1'):
                    ui.label('🛠️ Tools:')
                    ui.label().bind_text_from(game_state, 'tools', backward=lambda t: ", ".join(t)).classes('font-bold text-purple-300')

        # أشرطة التقدم (Health & Oxygen)
        with ui.row().classes('w-full items-center justify-between gap-6 mt-2'):
            
            # ❤️ Health Bar
            with ui.row().classes('items-center gap-2 flex-1'):
                ui.label('❤️ Health:').classes('font-bold text-red-400 min-w-16')
                # ربط شريط التقدم بقيمة الصحة (نقسم على 10 لأن شريط التقدم يقبل من 0.0 إلى 1.0)
                ui.linear_progress(show_value=False)\
                    .bind_value_from(game_state, 'health', backward=lambda h: h / 100)\
                    .props('color=red-6 size=20px stripe rounded').classes('flex-1')
                ui.label().bind_text_from(game_state, 'health', backward=lambda h: f"{h}/100").classes('text-sm font-bold')

            # 🫧 Oxygen Bar
            with ui.row().classes('items-center gap-2 flex-1'):
                ui.label('🫧 Oxygen:').classes('font-bold text-cyan-400 min-w-16')
                ui.linear_progress(show_value=False)\
                    .bind_value_from(game_state, 'oxygen', backward=lambda o: o / 100)\
                    .props('color=cyan-5 size=20px stripe rounded').classes('flex-1')
                ui.label().bind_text_from(game_state, 'oxygen', backward=lambda o:f"{o} / 100").classes('text-sm font-bold')
    with ui.card().classes('w-full bg-slate-900/90 border border-cyan-500/30 rounded-2xl p-6 shadow-2xl backdrop-blur-md relative overflow-hidden'):
        
        # Optional glowing accent bar on top
        ui.element('div').classes('absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-cyan-500 via-purple-500 to-amber-400')

        # Card Header / Speaker Title
        with ui.row().classes('w-full items-center justify-between mb-4 pb-2 border-b border-slate-800'):
            with ui.row().classes('items-center gap-2'):
                ui.icon('auto_awesome', size='sm').classes('text-amber-400')
                lab=ui.label(game_state['x']).classes('text-xl font-bold tracking-widest text-amber-400 uppercase')#############################################------>X text
            
            # Chapter / Scene Tag
            

        # Main Story Text Content
        with ui.column().classes('w-full gap-3 text-slate-200 leading-relaxed'):
          
           
           z=ui.label(await intro(name.value) ).classes('text-base text-slate-300 italic pl-4 border-l-2 border-cyan-500/50')#   y text
           v=ui.label("").classes('text-base text-slate-300 italic pl-8 border-l-2 border-cyan-500/50').style('white-space: pre-wrap')
        
        progress_bar = (
            ui.linear_progress(value=0.0)
            .props('color=black size=20px stripe rounded')
            .classes('w-64 text-4xl'))
        progress_bar.visible = False

    
        b=ui.button("sart game",color='red',on_click=clearboard).style('font-size: 1.5rem; '
            'color: #fafafa; '
            'text-transform: uppercase; '
            'padding: 10px 20px; '
            'border-radius: 10px; '
            'border: 2px solid #fafafa; '
            'background: #252525; '
            'box-shadow: 3px 3px #fafafa; '
            'cursor: pointer; '
            'transition: transform 0.05s, box-shadow 0.05s;'
            'box-shadow: none; transform: translate(3px, 3px);').classes('w-full justify-center')
def clear():
    global printx,b,game_state,lab,scavenge,crystals,craft,scavenges,exit,collecting_iron,mining,becon,scavenge_Laser,plasma_drill,plasma_sword,hp,o,go,stay,attack,start_time
    b.delete()
    start_time=time.time()
    with ui.row().classes('w-full justify-center gap-8'):

        mining=ui.button("MINING",color='green',on_click=collectcrystal).classes('text-2xl')

        collecting_iron=ui.button("START COLLECTING",color='green',on_click=collectiron).classes('text-2xl')

        becon=ui.button("BUY BECON PART 📡",on_click=beconpart,color='green').classes('text-2xl')

        scavenge_Laser=ui.button('BUY Scavenge Laser🔫',color='gray',on_click=laser).classes('text-2xl')

        plasma_drill=ui.button('BUY PLASMA DRILL⛏️',on_click=drill).classes('text-2xl')

        plasma_sword=ui.button('BUY PLASMA SWORD⚔️',color='black',on_click=sword).classes('text-2xl')

        hp=ui.button('💨 Oxygen Tank (+30)',color='yellow',on_click=oxygen).classes('text-2xl')

        o=ui.button('❤️ MedKit (+40 HP)',color='green',on_click=health).classes('text-2xl')
        go=ui.button('GO AWAY',color='green',on_click=away).classes('text-2xl')
        stay=ui.button('STAY AND FIGHT',color='red',on_click=here).classes('text-2xl')
        exit=ui.button("BACK TO DASHBOARD",color='red',on_click=dashboard).classes('text-2xl')
        scavenge=ui.button('scavenge iron',color='red',on_click=scavenges).classes('text-2xl')
        crystals=ui.button('crystals',color='blue',on_click=crystal).classes('text-2xl')
        attack=ui.button('ATTACK',color='black',on_click=fight).classes('text-2xl')
        craft=ui.button('craft',color='green',on_click=crafts).classes('text-2xl')

def dashboard():
    global printx,b,game_state,lab,scavenge,crystals,craft,scavenges,exit,collecting_iron,mining,becon,scavenge_Laser,plasma_drill,plasma_sword,hp,o,v,go,stay
    sound_url = "https://assets.mixkit.co/active_storage/sfx/900/900.wav"
    ui.run_javascript(f"new Audio('{sound_url}').play();")
    lab.set_text("DASHBOARD")
    v.set_text("")
    mining.set_visibility(False)
    collecting_iron.set_visibility(False)
    becon.set_visibility(False)
    scavenge_Laser.set_visibility(False)
    plasma_sword.set_visibility(False)
    plasma_drill.set_visibility(False)
    hp.set_visibility(False)
    o.set_visibility(False)
    exit.set_visibility(False)
    scavenge.set_visibility(True)
    crystals.set_visibility(True)
    craft.set_visibility(True)
    stay.set_visibility(False)
    go.set_visibility(False)
    attack.set_visibility(False)



def clearboard():
    clear()
    dashboard()
def matter(x):
    if x == 0:
        x += 1
    m = random.choice(range(1,x+1))
    return m
def scavenges():
    global printx,b,game_state,lab,scavenge,crystals,craft,scavenges,exit,collecting_iron,mining,becon,scavenge_Laser,plasma_drill,plasma_sword,hp,o
    sound_url = "https://assets.mixkit.co/active_storage/sfx/900/900.wav"
    ui.run_javascript(f"new Audio('{sound_url}').play();")
    lab.set_text("scavenges")
    collecting_iron.set_visibility(True)
    scavenge.set_visibility(False)
    crystals.set_visibility(False)
    craft.set_visibility(False)
    exit.set_visibility(True)
async def collectiron():
    
    global x,game_state
    await start_cooldown(x)
    if "Scavenge Laser" not in game_state['Tools']:
        x=5
        game_state['oxygen'] -= matter(5)

        amount = matter(4)
        game_state['iron']+= amount
        game_state['XP_level']+= 0.1
        if game_state['health']<=0 or game_state['oxygen']<=0:
            await show_game_result('lose')


        
    elif "Scavenge Laser" in game_state['Tools']:
        x=3
        game_state['oxygen'] -= matter(3)
        if game_state['health']<=0 or game_state['oxygen']<=0:
            await show_game_result('lose')
        amount = matter(6)
        game_state['iron']+= amount
        game_state['XP_level']+= 0.15
    enemy()
def crystal():
    global printx,b,game_state,lab,scavenge,crystals,craft,scavenges,exit,collecting_iron,mining,becon,scavenge_Laser,plasma_drill,plasma_sword,hp,o
    sound_url = "https://assets.mixkit.co/active_storage/sfx/900/900.wav"
    ui.run_javascript(f"new Audio('{sound_url}').play();")
    lab.set_text('crystal')
    mining.set_visibility(True)
    scavenge.set_visibility(False)
    crystals.set_visibility(False)
    craft.set_visibility(False)
    exit.set_visibility(True)
async def collectcrystal():
    global x,sound,game_state
    
    
    
    if "Plasma Drill" not in game_state['Tools'] and "Plasma Sword" not in game_state['Tools']:
        ui.notify("YOU NEED PLASMA DRILL OR PLASMA SWORD GO TO CRAFT",color='red',timeout=None,type='negative')
        sound_url = "https://www.soundjay.com/buttons_c2026/sounds/beep-03.mp3"
        ui.run_javascript(f"new Audio('{sound_url}').play();")
    elif"Plasma Sword" in game_state['Tools']:
        x=5
        await start_cooldown(x)
        
        game_state['oxygen'] -= matter(3)

        amount = matter(6)
        game_state['crystal']+= amount
        game_state['XP_level']+= 0.3
        if game_state['health']<=0 or game_state['oxygen']<=0:
            await show_game_result('lose')
        enemy()
    elif"Plasma Drill" in game_state['Tools']:
        x=7
        await start_cooldown(x)
        game_state['oxygen'] -= matter(4)

        amount = matter(4)
        game_state['crystal']+= amount
        game_state['XP_level']+= 0.2
        if game_state['health']<=0 or game_state['oxygen']<=0:
            await show_game_result('lose')
        enemy()
def crafts():
    global z
    sound_url = "https://assets.mixkit.co/active_storage/sfx/900/900.wav"
    ui.run_javascript(f"new Audio('{sound_url}').play();")
    lab.set_text('CRAFT')
    b="="*60
    v.set_text(f"{b}\n"
    f"🔫 Scavenge Laser     | ⚙️ 50  | 💎 0  | 👛 0\n"
    f"⛏️ Plasma Drill       | ⚙️ 100 | 💎 0  | 👛 0\n"
    f"⚔️ Plasma Sword       | ⚙️ 100 | 💎 50  | 👛 10.0\n"
    f"💨 Oxygen Tank (+30)  | ⚙️ 25 | 💎 0  | 👛 1.5\n"
    f"❤️ MedKit (+40 HP)    | ⚙️ 0  | 💎 30  | 👛 0\n"
    f"📡 Beacon Part        | ⚙️ 300 | 💎 100 | 👛 20.0\n"""
    f"{b}")
    scavenge.set_visibility(False)
    crystals.set_visibility(False)
    craft.set_visibility(False)
    exit.set_visibility(True)
    becon.set_visibility(True)
    scavenge_Laser.set_visibility(True)
    plasma_drill.set_visibility(True)
    plasma_sword.set_visibility(True)
    hp.set_visibility(True)
    o.set_visibility(True)
def laser():
    global game_state,scavenge_Laser
    if "Scavenge Laser" in game_state['Tools']:
        ui.notify("YOU ALREADY HAVE Scavenge Laser",type='warning')
    elif game_state['iron']>=50 and game_state['credits']>=2:
        sound_url = "https://www.myinstants.com/media/sounds/cash-register-sound-fx.mp3"
        ui.run_javascript(f"new Audio('{sound_url}').play();")
        game_state['iron']-=50
        
        game_state['Tools'].append("Scavenge Laser")
        ui.notify("DONE!",type='positive')
    elif game_state['iron']<50:
        ui.notify("NO enought iron",type='warning')
 
def drill():
    global game_state,scavenge_Laser
    if "Plasma Drill" in game_state['Tools']:
        ui.notify("YOU ALREADY HAVE Plasma Drill",type='warning')
    elif game_state['iron']>=100 and game_state['credits']>=5:
        game_state['iron']-=100
        sound_url = "https://www.myinstants.com/media/sounds/cash-register-sound-fx.mp3"
        ui.run_javascript(f"new Audio('{sound_url}').play();")
        game_state['Tools'].append("Plasma Drill")
        ui.notify("DONE!",type='positive')
    elif game_state['iron']<100:
        ui.notify("NO enought iron",type='warning')

def sword():
    global game_state,scavenge_Laser
    if "Plasma Sword" in game_state['Tools']:
        ui.notify("YOU ALREADY HAVE Scavenge Laser",type='warning')
    elif game_state['iron']>=100 and game_state['credits']>=10 and game_state['crystal']>=5:
        game_state['iron']-=100
        game_state['credits']-=10
        game_state['crystal']-=50
        game_state['Tools'].append("Plasma Sword")
        sound_url = "https://www.myinstants.com/media/sounds/cash-register-sound-fx.mp3"
        ui.run_javascript(f"new Audio('{sound_url}').play();")
        ui.notify("DONE!",type='positive')
    elif game_state['iron']<100:
        ui.notify("NO enought iron",type='warning')
    elif game_state['crystal']<50:
        ui.notify("NO enought crystal",type='warning')
    else:
        ui.notify("NO enought credit",type='warning') 
def oxygen():
    if game_state['oxygen']==100:
        ui.notify("YOUR OXYGEN COMPLETED",type='warning')
    elif game_state['iron']<25:
        ui.notify("NO enought iron",type='warning')
    elif game_state['credits'] <1.5:
        ui.notify("NO enought credits",type='warning')
    else:
        sound_url = "https://assets.mixkit.co/active_storage/sfx/2232/2232.wav"
        ui.run_javascript(f"new Audio('{sound_url}').play();")
        game_state['iron']-=25
        game_state['credits']-=1.5
        game_state['oxygen']=min(100,game_state['oxygen']+30)
        ui.notify("DONE!",type='positive')
def health():
    if game_state['health']==100:
        ui.notify("YOUR HEALTH COMPLETED",type='warning')

    elif game_state['crystal'] <20:
        ui.notify("NO enought crystal",type='warning')
    else:
        sound_url = "https://assets.mixkit.co/active_storage/sfx/2831/2831.wav"
        ui.run_javascript(f"new Audio('{sound_url}').play();")
        game_state['crystal']-=20
        game_state['health']=min(100,game_state['health'])
        ui.notify("DONE!",type='positive')

async def beconpart():
    if game_state['iron']<300:
        ui.notify("NO enought iron",type='warning')
    elif game_state['credits']<20:
        ui.notify("NO enought credits",type='warning')
    elif game_state['crystal']<100:
        ui.notify("NO enought crystal",type='warning')
    else:
        game_state['iron']-=300
        game_state['credits']-=20
        game_state['crystal']-=100
        game_state['beacon_parts']+=1
        ui.notify(f"YOU HAVE {game_state['beacon_parts']} PART/S FROM BECON, YOU NEED 3 TO END GAME")
        if game_state['beacon_parts']==3:
            await show_game_result('win')

            
def enemy():
    global e_defense,e_health,e_name,e_thorns,e_xp,e_xpd,stay,go,enem

    if game_state['XP_level']>=3:
        ratio = [60, 35, 5, 0]
        enem=random.choices(enemses,ratio,k=1)[0]
        if enem!="none":
            sound_url = "https://assets.mixkit.co/active_storage/sfx/1777/1777.wav"
            ui.run_javascript(f"new Audio('{sound_url}').play();")
            lab.set_text(enem[0])
            e_xp = enem[1]
            e_health = enem[2]
            e_defense = enem[3]
            e_thorns = enem[4]
            e_name = enem[0]
            e_xpd = enem[1]
            ui.notify(f"{e_name} ATTACKS YOU",type='warning')
            sound_url1 = "https://www.soundjay.com/buttons_c2026/sounds/beep-03.mp3"
            ui.run_javascript(f"new Audio('{sound_url1}').play();")
            v.set_text(f"YOU WILL FIGHT {e_name}\n"
                    f"ITS HEALTH {e_health}\n"
                    f"ITS DEFENSE {e_defense}\n"
                    f"THORNS {e_thorns}\n"
                    "IF YOU CHOOSE GO AWAY\n"
                    "YOU WILL LOSE 10 HEALTH and all of your iron").classes('text-3xl')
            stay.set_visibility(True)
            go.set_visibility(True)
            exit.set_visibility(False)    
            mining.set_visibility(False)
            collecting_iron.set_visibility(False)
        else:
            ui.notify('YOU ARE SAFE',type='positive')
def away():
    sound_url = "https://cdn.pixabay.com/download/audio/2025/08/22/audio_b288bf5180.mp3?filename=spinopel-run-fast-on-asphalt-393096.mp3"
    ui.run_javascript(f"new Audio('{sound_url}').play();")
    lab.set_text('DASHBOARD')
    dashboard()
    game_state['iron']=0
    game_state['health']-=10
    v.set_text("")
def here():
    stay.set_visibility(False)
    go.set_visibility(False)
    exit.set_visibility(False)    
    mining.set_visibility(False)
    collecting_iron.set_visibility(False)
    attack.set_visibility(True)
async def fight():
    global e_health

    if "Plasma Sword" not in game_state['Tools'] and "Plasma Drill" in game_state['Tools']:
        damge = random.choice(range(11, 21))
        o_ = random.choice(range(5))
    elif "Plasma Sword" in game_state['Tools']:
        damge = random.choice(range(21, 31))
        o_ = random.choice(range(2))   
    elif "Scavenge Laser" in game_state['Tools'] and len(game_state['Tools']) == 1:
        damge = random.choice(range(5, 10))
        o_ = random.choice(range(7))
    elif len(game_state['Tools']) == 0:
        damge = random.choice(range(5))-e_defense
        o_ = random.choice(range(10))
    attack.disable()
    e_health-=damge
    sound_url = "https://cdn.pixabay.com/download/audio/2025/08/23/audio_ccf247ea0a.mp3?filename=dragon-studio-violent-sword-slice-2-393841.mp3"
    ui.run_javascript(f"new Audio('{sound_url}').play();")
    if e_health<=0:
        if enem==Broken_Droid:
            cr=0.5
        elif enem==Mutant_Explorer:
            cr=1
        else:
            cr=2
        
        ui.notify(f"YOU WIN credit + {cr}",type='positive')
        game_state['credits']+=cr

        dashboard()
        attack.enable()
    else:
        game_state['oxygen']-=o_
        if game_state['health']<=0 or game_state['oxygen']<=0:
            await show_game_result('lose')
        game_state['health']-=e_thorns
        if game_state['health']<=0 or game_state['oxygen']<=0:
            await show_game_result('lose')
        ui.notify(f"YOU CAUSE DAMAGE={damge}",type='positive')
        await asyncio.sleep(2.0)
        ond=random.choice(range(e_xp))
        game_state['health']-=ond
        if game_state['health']<=0 or game_state['oxygen']<=0:
            await show_game_result('lose')
        if game_state['health']<=0 or game_state['oxygen']<=0:
            show_game_result('lose')
        ui.notify(f"YOUR HEALTH DECREASED BY {ond}",type='positive')
        attack.enable()





port = int(os.environ.get('PORT', 8080))
ui.run(host='0.0.0.0', port=port, reload=False)
