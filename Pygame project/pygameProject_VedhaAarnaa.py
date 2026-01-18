import pygame

# Initialize pygame library
pygame.init()

# ============================================================
# SCREEN SETUP
# ============================================================
# Define the game window dimensions
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600
gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("RoadMaster")
clock = pygame.time.Clock()  # Used to control frame rate

# ============================================================
# COLOR PALETTE
# ============================================================
# Define RGB color values for consistent styling
ORANGE = (255, 165, 60)     
WHITE = (245, 245, 245)
GRAY = (160, 160, 160)   
DARK_GRAY = (40, 40, 40)
BLACK = (0, 0, 0) 
RED = (200, 50, 50) 
GREEN = (0, 200, 0) 

# ============================================================
# AUDIO SETUP
# ============================================================

pygame.mixer.music.load("Audio/pygameMusic.mp3")
pygame.mixer.music.set_volume(0.2)  # Set to 20% volume
pygame.mixer.music.play(-1, 0.0)    # Loop indefinitely

# ============================================================
# FONT SETUP
# ============================================================
# Create different font sizes for various UI elements
title_font = pygame.font.SysFont(None, 72)       # Large titles
button_font = pygame.font.SysFont(None, 36)      # Button text
subtitle_font = pygame.font.SysFont(None, 30)    # Subtitles
paragraph_font = pygame.font.SysFont(None, 25)   # Body text

# ============================================================
# BACKGROUND IMAGES
# ============================================================
# Menu background image
background = pygame.image.load("Images/backgroundIMG.png")
background = pygame.transform.scale(background, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

# Credits/exit screen background
credits_img = pygame.image.load("Images/exitScreen_background.png")
credits_img = pygame.transform.scale(credits_img, (DISPLAY_WIDTH, credits_img.get_height()))
credits_y = DISPLAY_HEIGHT  # Start position (off-screen bottom)
scroll_speed = 1.2           # Scrolling speed for credits

# ============================================================
# ROAD IMAGES
# ============================================================
# Load and scale all road map images to fit screen
straight_road = pygame.image.load("Images/straight_road.png")
straight_road = pygame.transform.scale(straight_road, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

intersection = pygame.image.load("Images/intersection.png")
intersection = pygame.transform.scale(intersection, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

crosswalk_road = pygame.image.load("Images/crosswalk_road.png")
crosswalk_road = pygame.transform.scale(crosswalk_road, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

parking_lot = pygame.image.load("Images/parking_lot.png")
parking_lot = pygame.transform.scale(parking_lot, (DISPLAY_WIDTH, DISPLAY_HEIGHT))

# ============================================================
# CAR IMAGES
# ============================================================
# Load player car and create rotated versions for steering animation
player_car_original = pygame.image.load("Images/player_car.png").convert_alpha()
player_car = pygame.transform.scale(player_car_original, (160, 170))
player_car_left = pygame.transform.rotate(player_car, 15)    # Left turn visual
player_car_right = pygame.transform.rotate(player_car, -15)  # Right turn visual

# ============================================================
# CHARACTER IMAGES
# ============================================================
# Instructor image for tutorial and decision popups
instructor = pygame.image.load("Images/instructor.png")
instructor = pygame.transform.scale(instructor, (80, 80))

# Pedestrian for crosswalk challenge
pedestrian_img = pygame.image.load("Images/pedestrian.png")
pedestrian_img = pygame.transform.scale(pedestrian_img, (40, 60))

# ============================================================
# LESSON SLIDES
# ============================================================
# Load all 11 lesson slides into a list
lesson_slides = []
for i in range(1, 12):
    img = pygame.image.load(f"Images/slide{i}.png")
    img = pygame.transform.scale(img, (DISPLAY_WIDTH, DISPLAY_HEIGHT))
    lesson_slides.append(img)
current_slide = 0  # Track which slide is currently displayed

# ============================================================
# QUIZ QUESTIONS
# ============================================================
# Each question has: question text, 4 choices, correct answer index, and explanation
quiz_questions = [
    {
        "question": "What does a broken white line represent?",
        "choices": [
            "Lane changes are discouraged",
            "Lane changes are prohibited",
            "Lane changes are permitted",
            "Lane changes are allowed as long as the area is clear"
        ],
        "correct": 2,
        "reason": "Broken white lines separate lanes moving in the same direction and allow lane changes."
    },
    {
        "question": "What does a construction zone sign mean?",
        "choices": [
            "It means stop before continuing",
            "A crosswalk is approaching",
            "You must stop immediately",
            "Construction may be happening and lanes may change"
        ],
        "correct": 3,
        "reason": "Construction signs warn drivers of road work and possible lane changes."
    },
    {
        "question": "How much over the speed limit can you go before getting a fine?",
        "choices": [
            "10–15 km over",
            "0–9 km over",
            "16–29 km over",
            "30–49 km over"
        ],
        "correct": 1,
        "reason": "Fines start at 10–15 km/h over the speed limit."
    },
    {
        "question": "Who has the right of way at a crosswalk?",
        "choices": [
            "The car",
            "The pedestrian",
            "Whoever arrives first",
            "The faster vehicle"
        ],
        "correct": 1,
        "reason": "Pedestrians always have the right of way at crosswalks."
    },
    {
        "question": "Is it okay to use a hand-held device when stopped at a red light?",
        "choices": [
            "True",
            "False",
            "Sometimes",
            "Depends on the situation"
        ],
        "correct": 1,
        "reason": "Using a hand-held device is illegal even when stopped at a red light."
    },
    {
        "question": "You are driving below the speed limit, but it starts raining heavily. What should you do?",
        "choices": [
            "Continue at the same speed",
            "Speed up to avoid traffic",
            "Slow down and increase following distance",
            "Pull over immediately"
        ],
        "correct": 2,
        "reason": "Drivers must adjust speed based on road and weather conditions."
    }
]

# ============================================================
# QUIZ STATE VARIABLES
# ============================================================
quiz_index = 0           # Current question number
selected_choice = None   # Which answer was selected (0-3)
show_result = False      # Whether to show correct/incorrect feedback
quiz_score = 0           # Number of correct answers
quiz_completed = False   # Whether all questions answered

# ============================================================
# BUTTON RECTANGLES - QUIZ
# ============================================================
# Define clickable areas for quiz navigation
quiz_menu_button = pygame.Rect(200, 300, 180, 60)
quiz_results_button = pygame.Rect(420, 300, 180, 60)
game_start_button = pygame.Rect(300, 480, 200, 60)
# Create 4 answer buttons in a vertical list
answer_buttons = [pygame.Rect(100, 200 + i * 60, 600, 50) for i in range(4)]
quiz_next_button = pygame.Rect(DISPLAY_WIDTH - 160, DISPLAY_HEIGHT - 65, 140, 45)

# ============================================================
# GAME STATE
# ============================================================
state = "title"  # Current screen: title, menu, lesson, quiz, game, etc.

# ============================================================
# CAR PHYSICS VARIABLES
# ============================================================
car_x = DISPLAY_WIDTH // 2 - 80  # Car horizontal position (centered)
car_y = DISPLAY_HEIGHT - 250     # Car vertical position (near bottom)
car_speed_x = 7                  # Left/right movement speed
car_speed_y = 0                  # Forward speed (0-12)
car_rotation = 0                 # Visual tilt: -1=right, 0=straight, 1=left
max_speed = 12                   # Maximum forward speed
acceleration = 0.5               # Speed increase per frame when accelerating
deceleration = 0.7               # Speed decrease per frame when braking

# ============================================================
# ROAD SCROLLING VARIABLES
# ============================================================
road_y = 0       # Vertical offset for scrolling effect
distance = 0     # Total distance traveled (triggers stage changes)

# ============================================================
# GAME PROGRESS VARIABLES
# ============================================================
current_stage = 0        # Which challenge: 0=start, 1=light, 4=crosswalk, 7=parking, 8=complete
show_instruction = True  # Whether to show instruction box at top
show_decision = False    # Whether to show speed decision popup
decision_made = False    # Whether player answered speed question

# ============================================================
# TRAFFIC LIGHT STATE
# ============================================================
at_stop_sign = False      # Whether car is in traffic light zone
stopped_at_sign = False   # Whether car came to complete stop
stop_wait_timer = 0       # Frames waited at red light (60 frames = 1 second)
can_proceed = False       # Whether light turned green

# ============================================================
# PEDESTRIAN STATE
# ============================================================
ped_x = -50         # Pedestrian horizontal position (starts off-screen)
ped_y = 280         # Pedestrian vertical position (crossing height)
ped_active = False  # Whether pedestrian is currently crossing
ped_warned = False  # Whether warning message was shown

# ============================================================
# DECISION POPUP BUTTONS
# ============================================================
decision_button_1 = pygame.Rect(150, 350, 500, 60)  # "Speed up" option
decision_button_2 = pygame.Rect(150, 430, 500, 60)  # "Stay within limit" option

# ============================================================
# VISUAL EFFECTS
# ============================================================
warning_alpha = 0        # Opacity of warning overlay (0-255)
warning_fade_in = False  # Whether warning is fading in

# ============================================================
# BUTTON RECTANGLES - MAIN MENU
# ============================================================
button_width = 140
button_height = 60
button_y = 350
spacing = 20
start_x = 10

# Five main menu buttons in a horizontal row
lesson_button = pygame.Rect(start_x, button_y, button_width, button_height)
quiz_button = pygame.Rect(start_x + (button_width + spacing), button_y, button_width, button_height)
results_button = pygame.Rect(start_x + (button_width + spacing) * 2, button_y, button_width, button_height)
game_button = pygame.Rect(start_x + (button_width + spacing) * 3, button_y, button_width, button_height)
quit_button = pygame.Rect(start_x + (button_width + spacing) * 4, button_y, button_width, button_height)

# ============================================================
# BUTTON RECTANGLES - NAVIGATION
# ============================================================
start_button = pygame.Rect((DISPLAY_WIDTH - button_width) // 2, 350, button_width, button_height)
back_button = pygame.Rect(DISPLAY_WIDTH - 140, 20, 120, 45)
next_button = pygame.Rect(DISPLAY_WIDTH - 160, DISPLAY_HEIGHT - 65, 140, 45)
prev_button = pygame.Rect(20, DISPLAY_HEIGHT - 65, 140, 45)

# ============================================================
# FUNCTIONS
# ============================================================

def draw_button(rect, text):
    """
    Draw a button with hover effect
    Changes color when mouse hovers over it
    """
    mouse_pos = pygame.mouse.get_pos()
    
    # Change colors based on hover state
    if rect.collidepoint(mouse_pos):
        color = ORANGE
        text_color = BLACK
    else:
        color = DARK_GRAY
        text_color = WHITE
    
    # Draw button rectangle and centered text
    pygame.draw.rect(gameDisplay, color, rect)
    text_surf = button_font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    gameDisplay.blit(text_surf, text_rect)

def draw_background():
    """
    Draw the menu background image with dark overlay
    Used for title, menu, quiz, and result screens
    """
    gameDisplay.blit(background, (0, 0))
    # Add semi-transparent dark overlay for better text readability
    overlay = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    overlay.set_alpha(120)
    overlay.fill(BLACK)
    gameDisplay.blit(overlay, (0, 0))

def draw_text_wrapped(text, font, color, x, y, max_width, line_spacing=5):
    """
    Draw text that automatically wraps to fit within max_width
    Splits text into multiple lines if needed
    """
    words = text.split(" ")
    lines = []
    current_line = ""
    
    # Build lines that fit within max_width
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)
    
    # Draw each line with spacing
    for i, line in enumerate(lines):
        line_surf = font.render(line, True, color)
        gameDisplay.blit(line_surf, (x, y + i * (font.get_height() + line_spacing)))

# ============================================================
# SCREEN DRAWING FUNCTIONS
# ============================================================

def draw_title_screen():
    """
    Draw the opening title screen
    Shows game title, tagline, and student info
    """
    draw_background()
    gameDisplay.blit(title_font.render("RoadMaster", True, WHITE), (260, 180))
    gameDisplay.blit(subtitle_font.render("A driving game built on precision, awareness, and real road rules.", True, GRAY), (80, 235))
    # Student information
    gameDisplay.blit(paragraph_font.render("Name: Vedha Golla & Aarnaa Sekhar", True, WHITE), (30, 515))
    gameDisplay.blit(paragraph_font.render("Class Code: TEJ207", True, WHITE), (30, 535))
    gameDisplay.blit(paragraph_font.render("Teacher Name: Ms.Xie", True, WHITE), (30, 555))
    draw_button(start_button, "START")

def draw_menu_screen():
    """
    Draw the main menu with 5 navigation options
    Lesson, Quiz, Results, Game, and Quit
    """
    draw_background()
    gameDisplay.blit(title_font.render("Main Menu", True, WHITE), (285, 160))
    draw_button(lesson_button, "LESSON")
    draw_button(quiz_button, "QUIZ")
    draw_button(results_button, "RESULTS")
    draw_button(game_button, "GAME")
    draw_button(quit_button, "QUIT")

def draw_lesson_screen():
    """
    Draw the lesson screen showing educational slides
    Users can navigate through 11 slides with prev/next buttons
    """
    gameDisplay.blit(lesson_slides[current_slide], (0, 0))
    # Add subtle dark overlay
    overlay = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    overlay.set_alpha(30)
    overlay.fill((0, 0, 0))
    gameDisplay.blit(overlay, (0, 0))
    
    # Show navigation buttons based on current position
    if current_slide > 0:
        draw_button(prev_button, "BACK")
    if current_slide < len(lesson_slides) - 1:
        draw_button(next_button, "NEXT")
    draw_button(back_button, "MENU")

def draw_quiz_screen():
    """
    Draw the quiz screen with question and 4 answer choices
    Shows feedback after selection and tracks score
    """
    draw_background()
    q = quiz_questions[quiz_index]
    
    # Question box at top
    pygame.draw.rect(gameDisplay, (20, 20, 20), (60, 60, 680, 100))
    draw_text_wrapped(q["question"], subtitle_font, WHITE, 80, 75, 640)
    
    mouse_pos = pygame.mouse.get_pos()
    
    # Draw 4 answer buttons with appropriate colors
    for i in range(4):
        rect = answer_buttons[i]
        
        # Color logic: green=correct, red=wrong, orange=hover, gray=default
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
    
    # Show feedback box after answer selected
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
    """
    Screen shown after completing all quiz questions
    Offers options to return to menu or view results
    """
    draw_background()
    title_text = title_font.render("Quiz Complete!", True, WHITE)
    gameDisplay.blit(title_text, (200, 150))
    draw_button(quiz_menu_button, "MENU")
    draw_button(quiz_results_button, "RESULTS")

def draw_results_screen():
    """
    Display quiz results with score percentage
    Shows pass/fail status and encouragement message
    """
    draw_background()
    total_questions = len(quiz_questions)
    percentage = int((quiz_score / total_questions) * 100)
    
    title_text = title_font.render("Quiz Results", True, WHITE)
    gameDisplay.blit(title_text, (220, 80))
    
    # Results box
    pygame.draw.rect(gameDisplay, (30, 30, 30), (150, 180, 500, 280))
    
    # Display percentage in large text
    percent_text = title_font.render(f"{percentage}%", True, ORANGE)
    percent_rect = percent_text.get_rect(center=(400, 235))
    gameDisplay.blit(percent_text, percent_rect)
    
    # Display fraction (e.g., "5 / 6")
    fraction_text = button_font.render(f"{quiz_score} / {total_questions}", True, WHITE)
    fraction_rect = fraction_text.get_rect(center=(400, 295))
    gameDisplay.blit(fraction_text, fraction_rect)
    
    # Pass/fail status and message
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
    """
    Tutorial screen explaining game controls and objectives
    Shown before starting the driving game
    """
    draw_background()
    title_text = title_font.render("How to Play", True, WHITE)
    gameDisplay.blit(title_text, (250, 60))
    
    # Tutorial box
    pygame.draw.rect(gameDisplay, (30, 30, 30), (80, 130, 680, 340))
    pygame.draw.rect(gameDisplay, ORANGE, (80, 130, 680, 340), 3)
    
    # Instructor image
    gameDisplay.blit(instructor, (650, 165))
    
    # Controls and objectives
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
    """
    Main driving game screen - the core gameplay
    Handles road scrolling, challenges, and all game mechanics
    """
    global road_y, distance, current_stage, car_x, car_y, car_speed_y, car_rotation
    global show_decision, decision_made, ped_x, ped_active, ped_warned
    global at_stop_sign, stopped_at_sign, stop_wait_timer, can_proceed
    global warning_alpha, warning_fade_in
    
    # ============================================================
    # STAGE DISTANCES 
    # ============================================================
    # Define when each challenge appears based on distance traveled
    STAGE_DECISION = 4200              # Speed decision popup
    STAGE_TRAFFIC_LIGHT = 6500         # Red light challenge starts
    STAGE_TRAFFIC_LIGHT_END = 6975     # Red light zone ends
    STAGE_PEDESTRIAN_WARNING = 9500    # Warning before crosswalk
    STAGE_CROSSWALK = 10000            # Crosswalk with pedestrian
    STAGE_CROSSWALK_END = 10500        # Crosswalk zone ends
    STAGE_PARKING_TRANSITION = 13500   # Start slowing for parking
    STAGE_PARKING = 14000              # Parking lot begins
    
    # ============================================================
    # ROAD SELECTION LOGIC
    # ============================================================
    # Choose which road image to display based on distance
    if distance < STAGE_DECISION:
        road = straight_road
    elif distance < 6000:
        road = straight_road
        # Trigger speed decision popup
        if not decision_made:
            show_decision = True
    elif distance < STAGE_TRAFFIC_LIGHT:
        road = straight_road
    elif distance < STAGE_TRAFFIC_LIGHT_END:
        # Show intersection with traffic light
        road = intersection
        current_stage = 1
        at_stop_sign = True
    elif distance < STAGE_PEDESTRIAN_WARNING:
        road = straight_road
        current_stage = 2
        at_stop_sign = False
        if not ped_warned:
            ped_warned = True
    elif distance < STAGE_CROSSWALK:
        road = straight_road
        current_stage = 3
    elif distance < STAGE_CROSSWALK_END:
        # Show crosswalk and activate pedestrian
        road = crosswalk_road
        if not ped_active:
            ped_active = True
            ped_x = -50
        current_stage = 4
    elif distance < 12500:
        road = straight_road
        ped_active = False  # Deactivate pedestrian after crosswalk
        current_stage = 5
    elif distance < STAGE_PARKING_TRANSITION:
        road = straight_road
        current_stage = 6
    elif distance < STAGE_PARKING:
        road = straight_road
        current_stage = 6
        # Gradually slow down car before parking lot
        if car_speed_y > 1:
            car_speed_y -= 0.05
    else:
        # Enter parking lot
        road = parking_lot
        current_stage = 7
        # Slow to stop in parking lot
        if car_speed_y > 0.1:
            car_speed_y -= 0.1
        else:
            car_speed_y = 0
    
    # ============================================================
    # DRAW SCROLLING ROAD
    # ============================================================
    # Draw road twice for seamless scrolling effect
    gameDisplay.blit(road, (0, road_y))
    gameDisplay.blit(road, (0, road_y - DISPLAY_HEIGHT))
    
    # ============================================================
    # DRAW TRAFFIC LIGHT
    # ============================================================
    if at_stop_sign and current_stage == 1:
        # Position traffic light on right side
        light_x = DISPLAY_WIDTH // 2 + 150
        light_y = 80
        
        # Draw pole
        pygame.draw.rect(gameDisplay, (60, 60, 60), (light_x + 35, light_y + 140, 10, 80))
        # Draw light housing
        pygame.draw.rect(gameDisplay, (40, 40, 40), (light_x, light_y, 80, 140))
        pygame.draw.rect(gameDisplay, (20, 20, 20), (light_x, light_y, 80, 140), 3)
        
        # Red light (top) - glows when active
        if not can_proceed:
            pygame.draw.circle(gameDisplay, RED, (light_x + 40, light_y + 30), 20)
            pygame.draw.circle(gameDisplay, (255, 100, 100), (light_x + 40, light_y + 30), 20, 3)
        else:
            pygame.draw.circle(gameDisplay, (80, 20, 20), (light_x + 40, light_y + 30), 20)
        
        # Yellow light (middle) - always dim
        pygame.draw.circle(gameDisplay, (80, 80, 20), (light_x + 40, light_y + 70), 20)
        
        # Green light (bottom) - glows when can proceed
        if can_proceed:
            pygame.draw.circle(gameDisplay, GREEN, (light_x + 40, light_y + 110), 20)
            pygame.draw.circle(gameDisplay, (100, 255, 100), (light_x + 40, light_y + 110), 20, 3)
        else:
            pygame.draw.circle(gameDisplay, (20, 80, 20), (light_x + 40, light_y + 110), 20)
    
    # ============================================================
    # ROAD SCROLLING LOGIC
    # ============================================================
    if not show_decision and current_stage < 7:
        # Special logic for traffic light stage
        if at_stop_sign and current_stage == 1:
            if not stopped_at_sign:
                # Car hasn't stopped yet - check if stopped
                if car_speed_y <= 0.5:
                    stopped_at_sign = True
                    stop_wait_timer = 0
                else:
                    # Still moving, continue scrolling
                    road_y += car_speed_y
                    distance += car_speed_y
            elif not can_proceed:
                # Stopped at red light - count wait time
                stop_wait_timer += 1
                if stop_wait_timer >= 120:  # 2 seconds at 60fps
                    can_proceed = True
            else:
                # Green light - can continue
                road_y += car_speed_y
                distance += car_speed_y
        else:
            # Normal scrolling for other stages
            road_y += car_speed_y
            distance += car_speed_y
        
        # Loop road position when it scrolls off screen
        if road_y >= DISPLAY_HEIGHT:
            road_y = 0
    
    # ============================================================
    # PEDESTRIAN ANIMATION
    # ============================================================
    if ped_active and current_stage == 4:
        # Move pedestrian left to right across screen
        ped_x += 2.5
        gameDisplay.blit(pedestrian_img, (int(ped_x), ped_y))
        
        # Check if car is going too fast near pedestrian
        if ped_x > 200 and ped_x < 600:
            if car_speed_y > 2:
                restart_game("You are going to hit the pedestrian!")
        
        # Reset pedestrian when it leaves screen
        if ped_x > DISPLAY_WIDTH:
            ped_active = False
    
    # ============================================================
    # DRAW CAR
    # ============================================================
    # Choose car sprite based on rotation state
    if car_rotation == 1:
        gameDisplay.blit(player_car_left, (car_x - 5, car_y - 5))
    elif car_rotation == -1:
        gameDisplay.blit(player_car_right, (car_x - 5, car_y - 5))
    else:
        gameDisplay.blit(player_car, (car_x, car_y))
    
    # ============================================================
    # BOUNDARY COLLISION CHECK
    # ============================================================
    # Check if car drove off the road (before parking lot)
    if current_stage < 7:
        if car_x < 150 or car_x > 490:
            restart_game("Drove off the road!")
    
    # ============================================================
    # TRAFFIC LIGHT VIOLATION CHECKS
    # ============================================================
    if at_stop_sign and current_stage == 1:
        # Check if player passed light without stopping
        if distance > STAGE_TRAFFIC_LIGHT + 800 and not stopped_at_sign:
            restart_game("Failed to stop at the red light!")
        # Check if player ran red light
        if distance > STAGE_TRAFFIC_LIGHT_END - 200 and not can_proceed and car_speed_y > 1:
            restart_game("You ran the red light!")
    
    # ============================================================
    # PARKING DETECTION
    # ============================================================
    if current_stage == 7:
        parked = False
        # Check if car is in any of the 4 parking spots at top of lot
        if 150 < car_x < 275 and 50 < car_y < 250:
            parked = True
        elif 275 < car_x < 400 and 50 < car_y < 250:
            parked = True
        elif 400 < car_x < 525 and 50 < car_y < 250:
            parked = True
        elif 525 < car_x < 650 and 50 < car_y < 250:
            parked = True
        
        if parked:
            current_stage = 8  # Move to completion stage
    
    # ============================================================
    # COMPLETION SCREEN
    # ============================================================
    if current_stage == 8:
        # Dark overlay
        overlay = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        gameDisplay.blit(overlay, (0, 0))
        
        # Completion box
        pygame.draw.rect(gameDisplay, (20, 80, 20), (80, 140, 680, 420))
        pygame.draw.rect(gameDisplay, ORANGE, (80, 140, 680, 420), 6)
        
        # Instructor image
        gameDisplay.blit(instructor, (650, 185))
        
        # Title
        title = title_font.render("COMPLETED!", True, ORANGE)
        gameDisplay.blit(title, (title.get_rect(center=(400, 220)).topleft))
        
        # Subtitle
        subtitle = subtitle_font.render("Congratulations on passing!", True, WHITE)
        gameDisplay.blit(subtitle, (subtitle.get_rect(center=(400, 280)).topleft))
        
        # List of achievements
        y_start = 330
        gameDisplay.blit(paragraph_font.render("You successfully completed:", True, WHITE), (140, y_start))
        
        achievements = [
            "Made the right speed decision",
            "Stopped at the red light and waited", 
            "Slowed down for pedestrians",
            "Parked in the correct spot"
        ]
        
        # Draw each achievement with checkmark
        for i, achievement in enumerate(achievements):
            y_pos = y_start + 35 + (i * 30)
            pygame.draw.circle(gameDisplay, GREEN, (160, y_pos + 8), 8)
            gameDisplay.blit(paragraph_font.render("✓", True, BLACK), (155, y_pos))
            gameDisplay.blit(paragraph_font.render(achievement, True, WHITE), (180, y_pos))
        
        # Back to menu button
        menu_btn = pygame.Rect(250, 480, 300, 60)
        draw_button(menu_btn, "BACK TO MENU")
        return
    
    # ============================================================
    # SPEED DECISION POPUP
    # ============================================================
    if show_decision and not decision_made:
        # Semi-transparent overlay
        overlay = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        gameDisplay.blit(overlay, (0, 0))
        
        # Decision box
        pygame.draw.rect(gameDisplay, (30, 30, 30), (100, 150, 600, 350))
        pygame.draw.rect(gameDisplay, ORANGE, (100, 150, 600, 350), 3)
        gameDisplay.blit(instructor, (120, 180))
        draw_text_wrapped("Speed limit is 50 km/h but we're late. What do you do?", subtitle_font, WHITE, 220, 190, 450, line_spacing=5)
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Option 1: Speed up (wrong choice)
        color1 = ORANGE if decision_button_1.collidepoint(mouse_pos) else DARK_GRAY
        text_color1 = BLACK if decision_button_1.collidepoint(mouse_pos) else WHITE
        pygame.draw.rect(gameDisplay, color1, decision_button_1)
        gameDisplay.blit(paragraph_font.render("Speed up", True, text_color1), (330, decision_button_1.y + 18))
        
        # Option 2: Stay within limit (correct choice)
        color2 = ORANGE if decision_button_2.collidepoint(mouse_pos) else DARK_GRAY
        text_color2 = BLACK if decision_button_2.collidepoint(mouse_pos) else WHITE
        pygame.draw.rect(gameDisplay, color2, decision_button_2)
        gameDisplay.blit(paragraph_font.render("Stay within limit", True, text_color2), (310, decision_button_2.y + 18))
    
    # ============================================================
    # INSTRUCTION BOX
    # ============================================================
    if show_instruction and not show_decision:
        inst = ""
        inst_color = WHITE
        
        # Choose instruction text based on current distance/stage
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
                wait_time = stop_wait_timer / 60
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
        elif distance < 12500:
            inst = "Watch for pedestrians - maintain safe speed"
            inst_color = ORANGE
        elif distance < STAGE_PARKING_TRANSITION:
            inst = "Almost there - parking lot ahead"
        elif distance < STAGE_PARKING:
            inst = "Slow down - parking lot entrance approaching"
        elif current_stage == 7:
            inst = "Park in any of the 4 spots at the TOP (use arrows to position)"
        
        # Draw instruction box if text exists
        if inst:
            pygame.draw.rect(gameDisplay, (20, 20, 30), (80, 25, 680, 100))
            pygame.draw.rect(gameDisplay, inst_color, (80, 25, 680, 100), 3)
            gameDisplay.blit(subtitle_font.render(inst, True, inst_color), (110, 60))
            gameDisplay.blit(instructor, (650, 40))

    # ============================================================
    # SPEED DISPLAY (BOTTOM LEFT)
    # ============================================================
    speed_pct = int((car_speed_y / max_speed) * 100)
    pygame.draw.rect(gameDisplay, (30, 30, 30), (10, DISPLAY_HEIGHT - 60, 150, 50))
    gameDisplay.blit(paragraph_font.render(f"Speed: {speed_pct}%", True, WHITE), (20, DISPLAY_HEIGHT - 50))
    
    # Color code speed bar based on stage
    if current_stage == 4:  # Stricter near pedestrian
        bar_color = GREEN if speed_pct < 40 else ORANGE if speed_pct < 60 else RED
    else:
        bar_color = GREEN if speed_pct < 70 else ORANGE if speed_pct < 90 else RED
    
    # Draw speed bar
    if speed_pct > 0:
        pygame.draw.rect(gameDisplay, bar_color, (20, DISPLAY_HEIGHT - 30, int(130 * speed_pct / 100), 15))
    pygame.draw.rect(gameDisplay, WHITE, (20, DISPLAY_HEIGHT - 30, 130, 15), 2)
    
    # ============================================================
    # PROGRESS DISPLAY (BOTTOM RIGHT)
    # ============================================================
    progress = min(100, int((distance / STAGE_PARKING) * 100))
    pygame.draw.rect(gameDisplay, (30, 30, 30), (DISPLAY_WIDTH - 170, DISPLAY_HEIGHT - 60, 150, 50))
    gameDisplay.blit(paragraph_font.render(f"Progress: {progress}%", True, WHITE), (DISPLAY_WIDTH - 160, DISPLAY_HEIGHT - 50))
    pygame.draw.rect(gameDisplay, GREEN, (DISPLAY_WIDTH - 160, DISPLAY_HEIGHT - 30, int(130 * progress / 100), 15))
    pygame.draw.rect(gameDisplay, WHITE, (DISPLAY_WIDTH - 160, DISPLAY_HEIGHT - 30, 130, 15), 2)
    
    draw_button(back_button, "MENU")

def restart_game(msg="WRONG CHOICE!"):
    """
    Reset all game variables and show error message
    Called when player fails a challenge or crashes
    """
    global distance, road_y, car_x, car_y, car_speed_y, car_rotation, current_stage
    global show_decision, decision_made, ped_x, ped_active, ped_warned
    global at_stop_sign, stopped_at_sign, stop_wait_timer, can_proceed
    global warning_alpha, warning_fade_in
    
    # Show error message if provided
    if msg:
        draw_background()
        pygame.draw.rect(gameDisplay, (200, 0, 0), (100, 225, 600, 150))
        pygame.draw.rect(gameDisplay, WHITE, (100, 225, 600, 150), 3)
        
        text_surf = subtitle_font.render(msg, True, WHITE)
        text_rect = text_surf.get_rect(center=(400, 300))
        gameDisplay.blit(text_surf, text_rect)
        pygame.display.update()
        pygame.time.wait(2000)  # Show for 2 seconds
    
    # Reset all game state variables
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
    """
    Draw scrolling credits screen
    Shows when player selects quit from menu
    """
    global credits_y
    gameDisplay.fill(BLACK)
    gameDisplay.blit(credits_img, (0, credits_y))
    credits_y -= scroll_speed  # Scroll upward

# ============================================================
# MAIN GAME LOOP
# ============================================================
def gameLoop():
    """
    Main game loop - handles all events, updates, and rendering
    Runs at 60 FPS until game is closed
    """
    global state, credits_y, current_slide
    global quiz_index, selected_choice, show_result, quiz_score, quiz_completed
    global car_x, car_y, car_speed_y, car_rotation, show_decision, decision_made

    running = True
    while running:
        # ============================================================
        # EVENT HANDLING
        # ============================================================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Title screen - start button
                if state == "title":
                    if start_button.collidepoint(event.pos):
                        state = "menu"
                
                # Main menu - 5 navigation buttons
                elif state == "menu":
                    if lesson_button.collidepoint(event.pos):
                        state = "lesson"
                    elif quiz_button.collidepoint(event.pos):
                        # Reset quiz state when starting
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
                
                # Lesson screen - navigation buttons
                elif state == "lesson":
                    if next_button.collidepoint(event.pos) and current_slide < len(lesson_slides) - 1:
                        current_slide += 1
                    elif prev_button.collidepoint(event.pos) and current_slide > 0:
                        current_slide -= 1
                    elif back_button.collidepoint(event.pos):
                        current_slide = 0
                        state = "menu"
                
                # Quiz screen - answer selection and navigation
                elif state == "quiz":
                    if not show_result:
                        # Check if any answer button clicked
                        for i in range(4):
                            if answer_buttons[i].collidepoint(event.pos):
                                selected_choice = i
                                show_result = True
                                if selected_choice == quiz_questions[quiz_index]["correct"]:
                                    quiz_score += 1
                    else:
                        # Next question button
                        if quiz_next_button.collidepoint(event.pos):
                            quiz_index += 1
                            selected_choice = None
                            show_result = False
                            if quiz_index >= len(quiz_questions):
                                quiz_completed = True
                                state = "quiz_end"
                    if back_button.collidepoint(event.pos):
                        state = "menu"
                
                # Quiz end screen
                elif state == "quiz_end":
                    if quiz_menu_button.collidepoint(event.pos):
                        state = "menu"
                    elif quiz_results_button.collidepoint(event.pos):
                        state = "results"
                
                # Game tutorial screen
                elif state == "game_tutorial":
                    if game_start_button.collidepoint(event.pos):
                        restart_game("")  # Initialize game without error message
                        state = "game"
                    elif back_button.collidepoint(event.pos):
                        state = "menu"
                
                # Results screen
                elif state == "results":
                    if back_button.collidepoint(event.pos):
                        state = "menu"
                
                # Game screen - decision popup and completion button
                elif state == "game":
                    if show_decision and not decision_made:
                        if decision_button_1.collidepoint(event.pos):
                            restart_game("Speeding is illegal!")
                        elif decision_button_2.collidepoint(event.pos):
                            show_decision = False
                            decision_made = True
                    
                    # Back button (except during completion)
                    if back_button.collidepoint(event.pos) and current_stage != 8:
                        state = "menu"
                    
                    # Completion screen button
                    if current_stage == 8:
                        completion_btn = pygame.Rect(250, 480, 300, 60)
                        if completion_btn.collidepoint(event.pos):
                            state = "menu"
                            restart_game("")
        
        # ============================================================
        # CAR CONTROLS (ONLY DURING GAME)
        # ============================================================
        if state == "game":
            keys = pygame.key.get_pressed()
            if not show_decision and current_stage < 8:
                # Parking lot controls (stage 7) - direct car movement
                if current_stage == 7:
                    if keys[pygame.K_UP]:
                        if car_y > 50:
                            car_y -= 3  # Move up
                    if keys[pygame.K_DOWN]:
                        if car_y < DISPLAY_HEIGHT - 180:
                            car_y += 3  # Move down
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
                # Normal driving controls (stages 0-6) - speed-based
                else:
                    if keys[pygame.K_UP]:
                        car_speed_y += acceleration
                        if car_speed_y > max_speed:
                            car_speed_y = max_speed
                    if keys[pygame.K_DOWN]:
                        car_speed_y -= deceleration
                        if car_speed_y < 0:
                            car_speed_y = 0
                    # Natural deceleration when no input
                    if not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
                        car_speed_y -= 0.15
                        if car_speed_y < 0:
                            car_speed_y = 0
                    # Steering
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

        # ============================================================
        # CONTROLL CURRENT SCREEN
        # ============================================================
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
            # Exit when credits scroll off screen
            if credits_y + credits_img.get_height() < 0:
                running = False

        # Update display and maintain 60 FPS
        pygame.display.update()
        clock.tick(60)

# ============================================================
# START THE GAME
# ============================================================
gameLoop()
pygame.quit()