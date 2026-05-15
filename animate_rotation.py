from ursina import *
import random

app = Ursina(title="Premium 3D Bowling - 10 Pins", borderless=False)
window.fps_counter.enabled = False
window.exit_button.enabled = False

# Grafika va Atrof-muhit
Entity(model='quad', scale=100, texture='sky_vibrant', rotation_x=90, y=-5)
light = DirectionalLight(y=12, z=-10, shadows=True)
light.look_at(Vec3(0, 0, 15))

# Bowling yo'lagi
lane = Entity(
    model='cube', 
    scale=(5, 0.2, 35), 
    position=(0, 0, 17.5), 
    color=color.hex("e6b887"), # Premium yog'och foni
    texture='white_cube',
    collider='box'
)

# Yo'lak chetlari (Dizayn)
Entity(model='cube', scale=(0.15, 0.25, 35), position=(-2.5, 0, 17.5), color=color.dark_gray)
Entity(model='cube', scale=(0.15, 0.25, 35), position=(2.5, 0, 17.5), color=color.dark_gray)

# Bowling to'pi (Yaltiroq dizayn)
ball = Entity(
    model='sphere', 
    color=color.hex("ff1a1a"), 
    scale=0.8, 
    position=(0, 0.4, 2), 
    texture='white_cube'
)

# --- BARCHA 10 TA TOSH (PINS) KOORDINATALARI ---
# Matematik aniqlikda klassik 1-2-3-4 joylashuvi
pin_positions = [
    (0, 24),                              # 1-qator (1 ta tosh)
    (-0.4, 25.2), (0.4, 25.2),            # 2-qator (2 ta tosh)
    (-0.8, 26.4), (0, 26.4), (0.8, 26.4),  # 3-qator (3 ta tosh)
    (-1.2, 27.6), (-0.4, 27.6), (0.4, 27.6), (1.2, 27.6) # 4-qator (4 ta tosh)
]

pins = []
for i, pos in enumerate(pin_positions):
    # Har bir tosh (kegli) asosi
    pin = Entity(
        model='cylinder',
        color=color.white,
        scale=(0.35, 1.4, 0.35),
        position=(pos[0], 0.8, pos[1]),
        collider='box'
    )
    # Toshning o'rtasidagi qizil chiziq (Premium dizayn)
    Entity(parent=pin, model='cylinder', color=color.hex("cc0000"), scale=(1.05, 0.1, 1.05), y=0.2)
    pins.append(pin)

# O'yin mexanikasi
ball_speed = 28
ball_dx = 0
is_launched = False
score = 0

camera.position = (0, 6, -4)
camera.rotation_x = 22

score_text = Text(text=f'SCORE: {score}', position=(-0.1, 0.4), scale=2, color=color.gold)
instructions = Text(
    text="Boshqarish: [A/D] yoki [<- / ->]  |  [SPACE] - Otish", 
    position=(-0.35, -0.4), 
    scale=1.2, 
    color=color.white
)

def update():
    global is_launched, ball_dx, score
    
    if not is_launched:
        if held_keys['left arrow'] or held_keys['a']:
            ball.x -= 2.5 * time.dt
        if held_keys['right arrow'] or held_keys['d']:
            ball.x += 2.5 * time.dt
        ball.x = clamp(ball.x, -2.1, 2.1)
    else:
        ball.z += ball_speed * time.dt
        ball.x += ball_dx * time.dt
        
        # Kamera silliq kuzatib boradi
        camera.z = lerp(camera.z, ball.z - 7, 4 * time.dt)
        camera.x = lerp(camera.x, ball.x, 4 * time.dt)
        
        # To'p va 10 ta tosh to'qnashuvi
        for pin in pins:
            if pin.enabled and distance(ball, pin) < 0.9:
                # Realistik yiqilish va uchish effekti
                pin.animate_rotation((90, random.randint(-60, 60), random.randint(-30, 30)), duration=0.25)
                pin.animate_position((pin.x + random.uniform(-1.5, 1.5), 0.2, pin.z + 2), duration=0.35)
                
                score += 10
                score_text.text = f'SCORE: {score}'
                pin.enabled = False

        # Yo'lak tugagach restart
        if ball.z > 32:
            invoke(reset_game, delay=2)

def input(key):
    global is_launched, ball_dx
    if key == 'space' and not is_launched:
        is_launched = True
        ball_dx = random.uniform(-0.7, 0.7) # To'p to'g'ri ketmasdan biroz og'ishi uchun

def reset_game():
    global is_launched, ball_dx
    is_launched = False
    ball_dx = 0
    ball.position = (0, 0.4, 2)
    
    camera.animate_position((0, 6, -4), duration=1)
    camera.animate_rotation((22, 0, 0), duration=1)
    
    for i, pin in enumerate(pins):
        pin.enabled = True
        pin.position = (pin_positions[i][0], 0.8, pin_positions[i][1])
        pin.rotation = (0, 0, 0)

app.run()