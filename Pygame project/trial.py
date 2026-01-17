import pygame

pygame.init()

# ---------------- SCREEN ----------------
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600
gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("RoadMaster")
clock = pygame.time.Clock()

# ---------------- COLORS ----------------
ORANGE = (255, 165, 60)
WHITE = (245, 245, 245)
GRAY = (160, 160, 160)
DARK_GRAY = (40, 40, 40)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
GREEN = (0, 200, 0)

# ---------------- MUSIC ----------------
pygame.mixer.music.load("Audio/pygameMusic.mp3")
pygame.mixer.music.set_volume(0.2) 
pygame.mixer.music.play(-1, 0.0)

# ---------------- FONTS ----------------
title_font = pygame.font.SysFont(None, 72)
button_font = pygame.font.SysFont(None, 36)
subtitle_font = pygame.font.SysFont(None, 30)
paragraph_font = pygame.font.SysFont(None, 25)

# ---------------- BACKGROUNDS ----------------
background = pygame.image.load("Images/backgroundIMG.png")
background = pygame.transform.scale(background, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

credits_img = pygame.image.load("Images/exitScreen_background.png")
credits_img = pygame.transform.scale(credits_img, (DISPLAY_WIDTH, credits_img.get_height()))
credits_y = DISPLAY_HEIGHT
scroll_speed = 1

# ---------------- GAME IMAGES ----------------
straight_road = pygame.image.load("Images/straight_road.png")
straight_road = pygame.transform.scale(straight_road, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

intersection = pygame.image.load("Images/intersection.png")
intersection = pygame.transform.scale(intersection, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

crosswalk_road = pygame.image.load("Images/crosswalk_road.png")
crosswalk_road = pygame.transform.scale(crosswalk_road, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

parking_lot = pygame.image.load("Images/parking_lot.png")
parking_lot = pygame.transform.scale(parking_lot, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

player_car_original = pygame.image.load("Images/player_car.png").convert_alpha()
player_car = pygame.transform.scale(player_car_original, (160, 170))

player_car_left = pygame.transform.rotate(player_car, 15)
player_car_right = pygame.transform.rotate(player_car, -15)

instructor = pygame.image.load("Images/instructor.png")
instructor = pygame.transform.scale(instructor, (80, 80))

pedestrian_img = pygame.image.load("Images/pedestrain.png")
pedestrian_img = pygame.transform.scale(pedestrian_img, (40, 60))

# ---------------- LESSON SLIDES ----------------
lesson_slides = []
for i in range(1, 12):
    img = pygame.image.load(f"Images/slide{i}.png")
    img = pygame.transform.scale(img, (DISPLAY_WIDTH, DISPLAY_HEIGHT))
    lesson_slides.append(img)

current_slide = 0

quiz_questions = [
    {"question": "What does a broken white line represent?", "choices": ["Lane changes are discouraged", "Lane changes are prohibited", "Lane changes are permitted", "Lane changes are allowed as long as the area is clear"], "correct": 2, "reason": "Broken white lines separate lanes moving in the same direction and allow lane changes."},
    {"question": "What does a construction zone sign mean?", "choices": ["It means stop before continuing", "A crosswalk is approaching", "You must stop immediately", "Construction may be happening and lanes may change"], "correct": 3, "reason": "Construction signs warn drivers of road work and possible lane changes."},
    {"question": "How much over the speed limit can you go before getting a fine?", "choices": ["10–15 km over", "0–9 km over", "16–29 km over", "30–49 km over"], "correct": 1, "reason": "Fines start at 10–15 km/h over the speed limit."},
    {"question": "Who has the right of way at a crosswalk?", "choices": ["The car", "The pedestrian", "Whoever arrives first", "The faster vehicle"], "correct": 1, "reason": "Pedestrians always have the right of way at crosswalks."},
    {"question": "Is it okay to use a hand-held device when stopped at a red light?", "choices": ["True", "False", "Sometimes", "Depends on the situation"], "correct": 1, "reason": "Using a hand-held device is illegal even when stopped at a red light."},
    {"question": "You are driving below the speed limit, but it starts raining heavily. What should you do?", "choices": ["Continue at the same speed", "Speed up to avoid traffic", "Slow down and increase following distance", "Pull over immediately"], "correct": 2, "reason": "Drivers must adjust speed based on road and weather conditions."}
]

quiz_index = 0
selected_choice = None
show_result = False
quiz_score = 0
quiz_completed = False

quiz_menu_button = pygame.Rect(200, 300, 180, 60)
quiz_results_button = pygame.Rect(420, 300, 180, 60)
game_start_button = pygame.Rect(300, 480, 200, 60)

answer_buttons = [pygame.Rect(100, 200 + i * 60, 600, 50) for i in range(4)]
quiz_next_button = pygame.Rect(DISPLAY_WIDTH - 160, DISPLAY_HEIGHT - 65, 140, 45)

# ---------------- GAME STATE ----------------
state = "title"

car_x = DISPLAY_WIDTH // 2 - 80
car_y = DISPLAY_HEIGHT - 250
car_speed_x = 7
car_speed_y = 0
car_rotation = 0
max_speed = 12
acceleration = 0.5
deceleration = 0.7

road_y = 0
distance = 0

current_stage = 0
show_instruction = True
show_decision = False
decision_made = False

# Stop sign stage variables
at_stop_sign = False
stopped_at_sign = False
stop_wait_timer = 0
can_proceed = False

# Pedestrian variables - FIXED
ped_x = -50
ped_y = 280  # Fixed Y position on screen
ped_active = False
ped_warned = False

decision_button_1 = pygame.Rect(150, 350, 500, 60)
decision_button_2 = pygame.Rect(150, 430, 500, 60)

warning_alpha = 0
warning_fade_in = False

# ---------------- BUTTON SETUP ----------------
button_width = 140
button_height = 60
button_y = 350
spacing = 20
start_x = 10

lesson_button = pygame.Rect(start_x, button_y, button_width, button_height)
quiz_button = pygame.Rect(start_x + (button_width + spacing), button_y, button_width, button_height)
results_button = pygame.Rect(start_x + (button_width + spacing) * 2, button_y, button_width, button_height)
game_button = pygame.Rect(start_x + (button_width + spacing) * 3, button_y, button_width, button_height)
quit_button = pygame.Rect(start_x + (button_width + spacing) * 4, button_y, button_width, button_height)

start_button = pygame.Rect((DISPLAY_WIDTH - button_width) // 2, 350, button_width, button_height)
back_button = pygame.Rect(DISPLAY_WIDTH - 140, 20, 120, 45)
next_button = pygame.Rect(DISPLAY_WIDTH - 160, DISPLAY_HEIGHT - 65, 140, 45)
prev_button = pygame.Rect(20, DISPLAY_HEIGHT - 65, 140, 45)

# ---------------- FUNCTIONS ----------------
def draw_button(rect, text):
    mouse_pos = pygame.mouse.get_pos()
    color = ORANGE if rect.collidepoint(mouse_pos) else DARK_GRAY
    text_color = BLACK if rect.collidepoint(mouse_pos) else WHITE
    pygame.draw.rect(gameDisplay, color, rect)
    text_surf = button_font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    gameDisplay.blit(text_surf, text_rect)

def draw_background():
    gameDisplay.blit(background, (0, 0))
    overlay = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    overlay.set_alpha(120)
    overlay.fill(BLACK)
    gameDisplay.blit(overlay, (0, 0))

def draw_text_wrapped(text, font, color, x, y, max_width, line_spacing=5):
    words = text.split(" ")
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)
    for i, line in enumerate(lines):
        line_surf = font.render(line, True, color)
        gameDisplay.blit(line_surf, (x, y + i * (font.get_height() + line_spacing)))

def draw_title_screen():
    draw_background()
    gameDisplay.blit(title_font.render("RoadMaster", True, WHITE), (260, 180))
    gameDisplay.blit(subtitle_font.render("A driving game built on precision, awareness, and real road rules.", True, GRAY), (80, 235))
    gameDisplay.blit(paragraph_font.render("Name: Vedha Golla & Aarnaa Sekhar", True, WHITE), (30, 515))
    gameDisplay.blit(paragraph_font.render("Class Code: TEJ207", True, WHITE), (30, 535))
    gameDisplay.blit(paragraph_font.render("Teacher Name: Ms.Xie", True, WHITE), (30, 555))
    draw_button(start_button, "START")

def draw_menu_screen():
    draw_background()
    gameDisplay.blit(title_font.render("Main Menu", True, WHITE), (285, 160))
    draw_button(lesson_button, "LESSON")
    draw_button(quiz_button, "QUIZ")
    draw_button(results_button, "RESULTS")
    draw_button(game_button, "GAME")
    draw_button(quit_button, "QUIT")

def draw_lesson_screen():
    gameDisplay.blit(lesson_slides[current_slide], (0, 0))
    overlay = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    overlay.set_alpha(30)
    overlay.fill((0, 0, 0))
    gameDisplay.blit(overlay, (0, 0))
    if current_slide > 0:
        draw_button(prev_button, "BACK")
    if current_slide < len(lesson_slides) - 1:
        draw_button(next_button, "NEXT")
    draw_button(back_button, "MENU")

def draw_quiz_screen():
    draw_background()
    q = quiz_questions[quiz_index]
    pygame.draw.rect(gameDisplay, (20, 20, 20), (60, 60, 680, 100))
    draw_text_wrapped(q["question"], subtitle_font, WHITE, 80, 75, 640)
    mouse_pos = pygame.mouse.get_pos()
    for i in range(4):
        rect = answer_buttons[i]
        if selected_choice is not None and i == selected_choice:
            button_color = (0, 200, 0) if selected_choice == q["correct"] else (200, 50, 50)
            text_color = WHITE
        elif selected_choice is not None and i == q["correct"]:
            button_color = (0, 150, 0)
            text_color = WHITE
        elif rect.collidepoint(mouse_pos):
            button_color = ORANGE
            text_color = BLACK
        else:
            button_color = (80, 80, 80)
            text_color = WHITE
        pygame.draw.rect(gameDisplay, button_color, rect)
        text_surf = button_font.render(q["choices"][i], True, text_color)
        text_rect = text_surf.get_rect(center=rect.center)
        gameDisplay.blit(text_surf, text_rect)
    if selected_choice is not None:
        box_y = 450
        pygame.draw.rect(gameDisplay, (30, 30, 30), (60, box_y, 680, 100))
        feedback_color = (0, 200, 0) if selected_choice == q["correct"] else (200, 60, 60)
        feedback_text = "Correct!" if selected_choice == q["correct"] else "Incorrect."
        gameDisplay.blit(button_font.render(feedback_text, True, feedback_color), (80, box_y + 10))
        draw_text_wrapped(q["reason"], subtitle_font, WHITE, 80, box_y + 50, 640, line_spacing=3)
        draw_button(quiz_next_button, "NEXT")
    draw_button(back_button, "MENU")

def draw_quiz_end_screen():
    draw_background()
    title_text = title_font.render("Quiz Complete!", True, WHITE)
    gameDisplay.blit(title_text, (200, 150))
    draw_button(quiz_menu_button, "MENU")
    draw_button(quiz_results_button, "RESULTS")

def draw_results_screen():
    draw_background()
    total_questions = len(quiz_questions)
    percentage = int((quiz_score / total_questions) * 100)
    title_text = title_font.render("Quiz Results", True, WHITE)
    gameDisplay.blit(title_text, (220, 80))
    pygame.draw.rect(gameDisplay, (30, 30, 30), (150, 180, 500, 280))
    percent_text = title_font.render(f"{percentage}%", True, ORANGE)
    percent_rect = percent_text.get_rect(center=(400, 235))
    gameDisplay.blit(percent_text, percent_rect)
    fraction_text = button_font.render(f"{quiz_score} / {total_questions}", True, WHITE)
    fraction_rect = fraction_text.get_rect(center=(400, 295))
    gameDisplay.blit(fraction_text, fraction_rect)
    if percentage >= 50:
        status_text = button_font.render("PASS", True, (0, 200, 0))
        status_rect = status_text.get_rect(center=(400, 345))
        gameDisplay.blit(status_text, status_rect)
        message = "Great job! Now practice your skills in the game mode."
        draw_text_wrapped(message, subtitle_font, WHITE, 180, 390, 440)
    else:
        status_text = button_font.render("FAIL", True, (200, 60, 60))
        status_rect = status_text.get_rect(center=(400, 345))
        gameDisplay.blit(status_text, status_rect)
        message = "Don't give up! Review the lesson and try again."
        draw_text_wrapped(message, subtitle_font, WHITE, 180, 390, 440)
    draw_button(back_button, "MENU")

def draw_game_tutorial():
    draw_background()
    title_text = title_font.render("How to Play", True, WHITE)
    gameDisplay.blit(title_text, (250, 60))
    pygame.draw.rect(gameDisplay, (30, 30, 30), (80, 130, 680, 340))
    pygame.draw.rect(gameDisplay, ORANGE, (80, 130, 680, 340), 3)
    
    gameDisplay.blit(instructor, (650, 165))
    y_pos = 180
    gameDisplay.blit(subtitle_font.render("CONTROLS:", True, ORANGE), (130, y_pos))
    y_pos += 40
    gameDisplay.blit(paragraph_font.render("UP = Gas, DOWN = Brake, LEFT/RIGHT = Steer", True, WHITE), (150, y_pos))
    y_pos += 50
    gameDisplay.blit(subtitle_font.render("GOAL:", True, ORANGE), (130, y_pos))
    y_pos += 40
    draw_text_wrapped("Navigate safely, follow rules, make smart decisions, STOP at the red light and wait, slow down for pedestrians, and park correctly. Crash or break the law = restart!", paragraph_font, WHITE, 150, y_pos, 500, line_spacing=3)
    draw_button(game_start_button, "START GAME")
    draw_button(back_button, "MENU")

def draw_game_screen():
    global road_y, distance, current_stage, car_x, car_y, car_speed_y, car_rotation
    global show_decision, decision_made, ped_x, ped_active, ped_warned
    global at_stop_sign, stopped_at_sign, stop_wait_timer, can_proceed
    global warning_alpha, warning_fade_in
    
    STAGE_STRAIGHT_1 = 4000
    STAGE_DECISION = 4200
    STAGE_STRAIGHT_2 = 6000
    STAGE_TRAFFIC_LIGHT = 6500  # Traffic light at intersection
    STAGE_TRAFFIC_LIGHT_END = 7500
    STAGE_STRAIGHT_3 = 9500
    STAGE_PEDESTRIAN_WARNING = 10000
    STAGE_CROSSWALK = 10500
    STAGE_CROSSWALK_END = 11000
    STAGE_STRAIGHT_4 = 13000
    STAGE_PARKING_TRANSITION = 14000
    STAGE_PARKING = 14500
    
    # Determine which road to show
    if distance < STAGE_DECISION:
        road = straight_road
    elif distance < STAGE_STRAIGHT_2:
        road = straight_road
        if not decision_made:
            show_decision = True
    elif distance < STAGE_TRAFFIC_LIGHT:
        road = straight_road
    elif distance < STAGE_TRAFFIC_LIGHT_END:
        road = intersection  # Show intersection with traffic light ONLY ONCE
        current_stage = 1
        at_stop_sign = True
    elif distance < STAGE_STRAIGHT_3:
        road = straight_road  # Back to straight road after intersection
        current_stage = 2
        at_stop_sign = False
    elif distance < STAGE_PEDESTRIAN_WARNING:
        road = straight_road
        if not ped_warned:
            ped_warned = True
        current_stage = 3
    elif distance < STAGE_CROSSWALK:
        road = straight_road
        current_stage = 3
    elif distance < STAGE_CROSSWALK_END:
        road = crosswalk_road
        if not ped_active:
            ped_active = True
            ped_x = -50
        current_stage = 4
    elif distance < STAGE_STRAIGHT_4:
        road = straight_road  # Back to straight road after crosswalk
        ped_active = False  # Stop showing pedestrian
        current_stage = 5
    elif distance < STAGE_PARKING_TRANSITION:
        road = straight_road
        current_stage = 6
    elif distance < STAGE_PARKING:
        road = straight_road
        current_stage = 6
        # Gradually slow down the scrolling for smooth transition
        if car_speed_y > 1:
            car_speed_y -= 0.05
    else:
        road = parking_lot
        current_stage = 7
        # Gradually stop scrolling
        if car_speed_y > 0.1:
            car_speed_y -= 0.1
        else:
            car_speed_y = 0
    
    # Draw road
    gameDisplay.blit(road, (0, road_y))
    gameDisplay.blit(road, (0, road_y - DISPLAY_HEIGHT))
    
    # Draw traffic light during intersection stage
    if at_stop_sign and current_stage == 1:
        # Draw traffic light pole
        light_x = DISPLAY_WIDTH // 2 + 150
        light_y = 80
        
        # Pole
        pygame.draw.rect(gameDisplay, (60, 60, 60), (light_x + 35, light_y + 140, 10, 80))
        
        # Traffic light box
        pygame.draw.rect(gameDisplay, (40, 40, 40), (light_x, light_y, 80, 140))
        pygame.draw.rect(gameDisplay, (20, 20, 20), (light_x, light_y, 80, 140), 3)
        
        # Red light (lit)
        if not can_proceed:
            pygame.draw.circle(gameDisplay, RED, (light_x + 40, light_y + 30), 20)
            pygame.draw.circle(gameDisplay, (255, 100, 100), (light_x + 40, light_y + 30), 20, 3)
        else:
            pygame.draw.circle(gameDisplay, (80, 20, 20), (light_x + 40, light_y + 30), 20)
        
        # Yellow light (off)
        pygame.draw.circle(gameDisplay, (80, 80, 20), (light_x + 40, light_y + 70), 20)
        
        # Green light (lit when can proceed)
        if can_proceed:
            pygame.draw.circle(gameDisplay, GREEN, (light_x + 40, light_y + 110), 20)
            pygame.draw.circle(gameDisplay, (100, 255, 100), (light_x + 40, light_y + 110), 20, 3)
        else:
            pygame.draw.circle(gameDisplay, (20, 80, 20), (light_x + 40, light_y + 110), 20)
    
    # Handle scrolling
    if not show_decision and current_stage < 7:
        # DON'T stop scrolling for pedestrian - let player decide to slow down or not
        if at_stop_sign and current_stage == 1:
            if not stopped_at_sign:
                # Check if car has stopped
                if car_speed_y <= 0.5:
                    stopped_at_sign = True
                    stop_wait_timer = 0
                else:
                    # Continue scrolling if still moving
                    road_y += car_speed_y
                    distance += car_speed_y
            elif not can_proceed:
                # Car is stopped, count wait time
                stop_wait_timer += 1
                if stop_wait_timer >= 120:  # Wait for 2 seconds (60 fps * 2)
                    can_proceed = True
            else:
                # Can proceed, resume scrolling
                road_y += car_speed_y
                distance += car_speed_y
        else:
            # Normal scrolling for all other stages including pedestrian crossing
            road_y += car_speed_y
            distance += car_speed_y
        
        if road_y >= DISPLAY_HEIGHT:
            road_y = 0
    
    # Draw pedestrian - only once and only when active
    if ped_active and current_stage == 4:
        ped_x += 2.5  # Pedestrian moves at constant speed regardless of car
        gameDisplay.blit(pedestrian_img, (int(ped_x), ped_y))
        
        # Check if pedestrian is crossing (in the middle of the road)
        # If player tries to accelerate while pedestrian is crossing, restart game
        if ped_x > 200 and ped_x < 600:
            # If player is accelerating (speed increasing), they're trying to hit the pedestrian
            if car_speed_y > 2:
                restart_game("You are going to hit the pedestrian!")
        
        # Don't reset pedestrian - let them cross once and disappear
        if ped_x > DISPLAY_WIDTH:
            ped_active = False
    
    # Draw car
    if car_rotation == 1:
        gameDisplay.blit(player_car_left, (car_x - 5, car_y - 5))
    elif car_rotation == -1:
        gameDisplay.blit(player_car_right, (car_x - 5, car_y - 5))
    else:
        gameDisplay.blit(player_car, (car_x, car_y))
    
    # Boundary checks
    if current_stage == 1 and at_stop_sign:
        if car_x < 150 or car_x > 490:
            restart_game("Drove off the road!")
    elif current_stage < 7:
        if car_x < 150 or car_x > 490:
            restart_game("Drove off the road!")
    
    # Check if player failed to stop at red light
    if at_stop_sign and current_stage == 1:
        # Check if player is past the intersection without stopping
        if distance > STAGE_TRAFFIC_LIGHT + 800 and not stopped_at_sign:
            restart_game("Failed to stop at the red light!")
        # Also check if they drove through while still at red light
        if distance > STAGE_TRAFFIC_LIGHT_END - 200 and not can_proceed and car_speed_y > 1:
            restart_game("You ran the red light!")
    
    # Parking completion check
    if current_stage == 7:
        parked = False
        if 150 < car_x < 275 and 50 < car_y < 250:
            parked = True
        elif 275 < car_x < 400 and 50 < car_y < 250:
            parked = True
        elif 400 < car_x < 525 and 50 < car_y < 250:
            parked = True
        elif 525 < car_x < 650 and 50 < car_y < 250:
            parked = True
        
        if parked:
            current_stage = 8
    
    # Completion screen
    if current_stage == 8:
        overlay = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        gameDisplay.blit(overlay, (0, 0))
        
        pygame.draw.rect(gameDisplay, (20, 80, 20), (80, 140, 680, 420))
        pygame.draw.rect(gameDisplay, ORANGE, (80, 140, 680, 420), 6)
        
        gameDisplay.blit(instructor, (650, 185))
        
        title = title_font.render("COMPLETED!", True, ORANGE)
        gameDisplay.blit(title, (title.get_rect(center=(400, 220)).topleft))
        
        subtitle = subtitle_font.render("Congratulations on passing!", True, WHITE)
        gameDisplay.blit(subtitle, (subtitle.get_rect(center=(400, 280)).topleft))
        
        y_start = 330
        gameDisplay.blit(paragraph_font.render("You successfully completed:", True, WHITE), (140, y_start))
        
        achievements = [
            "Made the right speed decision",
            "Stopped at the red light and waited", 
            "Slowed down for pedestrians",
            "Parked in the correct spot"
        ]
        
        for i, achievement in enumerate(achievements):
            y_pos = y_start + 35 + (i * 30)
            pygame.draw.circle(gameDisplay, GREEN, (160, y_pos + 8), 8)
            gameDisplay.blit(paragraph_font.render("✓", True, BLACK), (155, y_pos))
            gameDisplay.blit(paragraph_font.render(achievement, True, WHITE), (180, y_pos))
        
        menu_btn = pygame.Rect(250, 480, 300, 60)
        draw_button(menu_btn, "BACK TO MENU")
        return
    
    # Decision popup
    if show_decision and not decision_made:
        overlay = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        gameDisplay.blit(overlay, (0, 0))
        pygame.draw.rect(gameDisplay, (30, 30, 30), (100, 150, 600, 350))
        pygame.draw.rect(gameDisplay, ORANGE, (100, 150, 600, 350), 3)
        gameDisplay.blit(instructor, (120, 180))
        draw_text_wrapped("Speed limit is 50 km/h but we're late. What do you do?", subtitle_font, WHITE, 220, 190, 450, line_spacing=5)
        mouse_pos = pygame.mouse.get_pos()
        color1 = ORANGE if decision_button_1.collidepoint(mouse_pos) else DARK_GRAY
        text_color1 = BLACK if decision_button_1.collidepoint(mouse_pos) else WHITE
        pygame.draw.rect(gameDisplay, color1, decision_button_1)
        gameDisplay.blit(paragraph_font.render("Speed up", True, text_color1), (330, decision_button_1.y + 18))
        color2 = ORANGE if decision_button_2.collidepoint(mouse_pos) else DARK_GRAY
        text_color2 = BLACK if decision_button_2.collidepoint(mouse_pos) else WHITE
        pygame.draw.rect(gameDisplay, color2, decision_button_2)
        gameDisplay.blit(paragraph_font.render("Stay within limit", True, text_color2), (310, decision_button_2.y + 18))
    
    # Instructions
    if show_instruction and not show_decision:
        inst = ""
        inst_color = WHITE
        
        if distance < 2000:
            inst = "Press UP to accelerate, DOWN to brake"
        elif distance < STAGE_DECISION:
            inst = "Keep a steady speed"
        elif distance < STAGE_TRAFFIC_LIGHT:
            inst = "Intersection with traffic light approaching - prepare to stop"
            inst_color = ORANGE
        elif at_stop_sign and current_stage == 1:
            if not stopped_at_sign:
                inst = "RED LIGHT! You must come to a COMPLETE STOP (speed = 0)"
                inst_color = RED
            elif not can_proceed:
                wait_time = stop_wait_timer / 60  # Convert frames to seconds
                inst = f"Good! Wait at the red light... ({wait_time:.1f}s / 2.0s)"
                inst_color = ORANGE
            else:
                inst = "GREEN LIGHT! You may now proceed - press UP to accelerate"
                inst_color = GREEN
        elif distance < STAGE_PEDESTRIAN_WARNING:
            inst = "Good! Continue forward"
        elif distance < STAGE_CROSSWALK:
            inst = "WARNING: Pedestrian crosswalk ahead - SLOW DOWN!"
            inst_color = ORANGE
        elif distance < STAGE_STRAIGHT_4:
            inst = "Watch for pedestrians - maintain safe speed"
            inst_color = ORANGE
        elif distance < STAGE_PARKING_TRANSITION:
            inst = "Almost there - parking lot ahead"
        elif distance < STAGE_PARKING:
            inst = "Slow down - parking lot entrance approaching"
        elif current_stage == 7:
            inst = "Park in any of the 4 spots at the TOP (use arrows to position)"
        
        if inst:
            pygame.draw.rect(gameDisplay, (20, 20, 30), (80, 25, 680, 100))
            pygame.draw.rect(gameDisplay, inst_color, (80, 25, 680, 100), 3)
            
            gameDisplay.blit(subtitle_font.render(inst, True, inst_color), (110, 60))
            gameDisplay.blit(instructor, (650, 40))

    # Speed and progress displays
    speed_pct = int((car_speed_y / max_speed) * 100)
    pygame.draw.rect(gameDisplay, (30, 30, 30), (10, DISPLAY_HEIGHT - 60, 150, 50))
    gameDisplay.blit(paragraph_font.render(f"Speed: {speed_pct}%", True, WHITE), (20, DISPLAY_HEIGHT - 50))
    
    if current_stage == 4:
        bar_color = GREEN if speed_pct < 40 else ORANGE if speed_pct < 60 else RED
    else:
        bar_color = GREEN if speed_pct < 70 else ORANGE if speed_pct < 90 else RED
    
    if speed_pct > 0:
        pygame.draw.rect(gameDisplay, bar_color, (20, DISPLAY_HEIGHT - 30, int(130 * speed_pct / 100), 15))
    pygame.draw.rect(gameDisplay, WHITE, (20, DISPLAY_HEIGHT - 30, 130, 15), 2)
    
    progress = min(100, int((distance / STAGE_PARKING) * 100))
    pygame.draw.rect(gameDisplay, (30, 30, 30), (DISPLAY_WIDTH - 170, DISPLAY_HEIGHT - 60, 150, 50))
    gameDisplay.blit(paragraph_font.render(f"Progress: {progress}%", True, WHITE), (DISPLAY_WIDTH - 160, DISPLAY_HEIGHT - 50))
    pygame.draw.rect(gameDisplay, GREEN, (DISPLAY_WIDTH - 160, DISPLAY_HEIGHT - 30, int(130 * progress / 100), 15))
    pygame.draw.rect(gameDisplay, WHITE, (DISPLAY_WIDTH - 160, DISPLAY_HEIGHT - 30, 130, 15), 2)
    
    draw_button(back_button, "MENU")

def restart_game(msg="WRONG CHOICE!"):
    global distance, road_y, car_x, car_y, car_speed_y, car_rotation, current_stage
    global show_decision, decision_made, ped_x, ped_active, ped_warned
    global at_stop_sign, stopped_at_sign, stop_wait_timer, can_proceed
    global warning_alpha, warning_fade_in
    
    if msg:
        draw_background()
        pygame.draw.rect(gameDisplay, (200, 0, 0), (100, 225, 600, 150))
        pygame.draw.rect(gameDisplay, WHITE, (100, 225, 600, 150), 3)
        
        # Use subtitle_font instead of title_font for smaller text
        text_surf = subtitle_font.render(msg, True, WHITE)
        text_rect = text_surf.get_rect(center=(400, 300))
        gameDisplay.blit(text_surf, text_rect)
        pygame.display.update()
        pygame.time.wait(2000)
    
    distance = 0
    road_y = 0
    car_x = DISPLAY_WIDTH // 2 - 80
    car_y = DISPLAY_HEIGHT - 250
    car_speed_y = 0
    car_rotation = 0
    current_stage = 0
    show_decision = False
    decision_made = False
    ped_x = -50
    ped_active = False
    ped_warned = False
    at_stop_sign = False
    stopped_at_sign = False
    stop_wait_timer = 0
    can_proceed = False
    warning_alpha = 0
    warning_fade_in = False

def draw_quit_screen():
    global credits_y
    gameDisplay.fill(BLACK)
    gameDisplay.blit(credits_img, (0, credits_y))
    credits_y -= scroll_speed

def gameLoop():
    global state, credits_y, current_slide
    global quiz_index, selected_choice, show_result, quiz_score, quiz_completed
    global car_x, car_y, car_speed_y, car_rotation, show_decision, decision_made

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if state == "title":
                    if start_button.collidepoint(event.pos):
                        state = "menu"
                elif state == "menu":
                    if lesson_button.collidepoint(event.pos):
                        state = "lesson"
                    elif quiz_button.collidepoint(event.pos):
                        quiz_index = 0
                        quiz_score = 0
                        selected_choice = None
                        show_result = False
                        quiz_completed = False
                        state = "quiz"
                    elif results_button.collidepoint(event.pos):
                        state = "results"
                    elif game_button.collidepoint(event.pos):
                        state = "game_tutorial"
                    elif quit_button.collidepoint(event.pos):
                        credits_y = DISPLAY_HEIGHT
                        state = "quit"
                elif state == "lesson":
                    if next_button.collidepoint(event.pos) and current_slide < len(lesson_slides) - 1:
                        current_slide += 1
                    elif prev_button.collidepoint(event.pos) and current_slide > 0:
                        current_slide -= 1
                    elif back_button.collidepoint(event.pos):
                        current_slide = 0
                        state = "menu"
                elif state == "quiz":
                    if not show_result:
                        for i in range(4):
                            if answer_buttons[i].collidepoint(event.pos):
                                selected_choice = i
                                show_result = True
                                if selected_choice == quiz_questions[quiz_index]["correct"]:
                                    quiz_score += 1
                    else:
                        if quiz_next_button.collidepoint(event.pos):
                            quiz_index += 1
                            selected_choice = None
                            show_result = False
                            if quiz_index >= len(quiz_questions):
                                quiz_completed = True
                                state = "quiz_end"
                    if back_button.collidepoint(event.pos):
                        state = "menu"
                elif state == "quiz_end":
                    if quiz_menu_button.collidepoint(event.pos):
                        state = "menu"
                    elif quiz_results_button.collidepoint(event.pos):
                        state = "results"
                elif state == "game_tutorial":
                    if game_start_button.collidepoint(event.pos):
                        restart_game("")
                        state = "game"
                    elif back_button.collidepoint(event.pos):
                        state = "menu"
                elif state == "results":
                    if back_button.collidepoint(event.pos):
                        state = "menu"
                elif state == "game":
                    if show_decision and not decision_made:
                        if decision_button_1.collidepoint(event.pos):
                            restart_game("Speeding is illegal!")
                        elif decision_button_2.collidepoint(event.pos):
                            show_decision = False
                            decision_made = True
                    if back_button.collidepoint(event.pos) and current_stage != 8:
                        state = "menu"
                    if current_stage == 8:
                        completion_btn = pygame.Rect(250, 480, 300, 60)
                        if completion_btn.collidepoint(event.pos):
                            state = "menu"
                            restart_game("")
        
        if state == "game":
            keys = pygame.key.get_pressed()
            if not show_decision and current_stage < 8:
                if current_stage == 7:
                    if keys[pygame.K_UP]:
                        if car_y > 50:
                            car_y -= 3
                    if keys[pygame.K_DOWN]:
                        if car_y < DISPLAY_HEIGHT - 180:
                            car_y += 3
                    if keys[pygame.K_LEFT]:
                        if car_x > 0:
                            car_x -= car_speed_x
                        car_rotation = 1
                    elif keys[pygame.K_RIGHT]:
                        if car_x < DISPLAY_WIDTH - 160:
                            car_x += car_speed_x
                        car_rotation = -1
                    else:
                        car_rotation = 0
                else:
                    if keys[pygame.K_UP]:
                        car_speed_y += acceleration
                        if car_speed_y > max_speed:
                            car_speed_y = max_speed
                    if keys[pygame.K_DOWN]:
                        car_speed_y -= deceleration
                        if car_speed_y < 0:
                            car_speed_y = 0
                    if not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
                        car_speed_y -= 0.15
                        if car_speed_y < 0:
                            car_speed_y = 0
                    if keys[pygame.K_LEFT]:
                        if car_x > 0:
                            car_x -= car_speed_x
                        car_rotation = 1
                    elif keys[pygame.K_RIGHT]:
                        if car_x < DISPLAY_WIDTH - 160:
                            car_x += car_speed_x
                        car_rotation = -1
                    else:
                        car_rotation = 0

        if state == "title":
            draw_title_screen()
        elif state == "menu":
            draw_menu_screen()
        elif state == "lesson":
            draw_lesson_screen()
        elif state == "quiz":
            draw_quiz_screen()
        elif state == "quiz_end":
            draw_quiz_end_screen()
        elif state == "results":
            draw_results_screen()
        elif state == "game_tutorial":
            draw_game_tutorial()
        elif state == "game":
            draw_game_screen()
        elif state == "quit":
            draw_quit_screen()
            if credits_y + credits_img.get_height() < 0:
                running = False

        pygame.display.update()
        clock.tick(60)

gameLoop()
pygame.quit()