import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Calculator")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

# Fonts
font = pygame.font.Font(None, 36)

# Calculator state
current_number = ""
stored_number = None
current_operation = None

# Button dimensions
BUTTON_WIDTH = 80
BUTTON_HEIGHT = 80
BUTTON_MARGIN = 10

# Define buttons
buttons = [
    '7', '8', '9', '/',
    '4', '5', '6', '*',
    '1', '2', '3', '-',
    '0', 'C', '=', '+'
]

# Create button rectangles
button_rects = []
for i, button in enumerate(buttons):
    row = i // 4
    col = i % 4
    x = col * (BUTTON_WIDTH + BUTTON_MARGIN) + BUTTON_MARGIN
    y = HEIGHT - (4 - row) * (BUTTON_HEIGHT + BUTTON_MARGIN) - BUTTON_MARGIN
    button_rects.append(pygame.Rect(x, y, BUTTON_WIDTH, BUTTON_HEIGHT))

def draw_buttons():
    for i, (button, rect) in enumerate(zip(buttons, button_rects)):
        pygame.draw.rect(screen, GRAY, rect)
        text = font.render(button, True, BLACK)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

def draw_display():
    display_rect = pygame.Rect(BUTTON_MARGIN, BUTTON_MARGIN, WIDTH - 2 * BUTTON_MARGIN, 100)
    pygame.draw.rect(screen, WHITE, display_rect)
    pygame.draw.rect(screen, BLACK, display_rect, 2)
    
    if stored_number is not None and current_operation:
        display_text = f"{stored_number} {current_operation} {current_number}"
    elif stored_number is not None:
        display_text = stored_number
    elif current_number:
        display_text = current_number
    else:
        display_text = "0"
    
    text = font.render(display_text, True, BLACK)
    text_rect = text.get_rect(midright=(WIDTH - 2 * BUTTON_MARGIN, 60))
    screen.blit(text, text_rect)

def calculate():
    global stored_number, current_number, current_operation
    if stored_number is not None and current_number and current_operation:
        a, b = int(stored_number), int(current_number)
        if current_operation == '+':
            result = a + b
        elif current_operation == '-':
            result = a - b
        elif current_operation == '*':
            result = a * b
        elif current_operation == '/':
            result = a // b if b != 0 else "Error"
        
        stored_number = str(result)
        current_number = ""
        current_operation = None
    return stored_number

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            for i, rect in enumerate(button_rects):
                if rect.collidepoint(pos):
                    if buttons[i] in '0123456789':
                        current_number += buttons[i]
                    elif buttons[i] in '+-*/':
                        if current_number:
                            if stored_number is not None:
                                calculate()
                            else:
                                stored_number = current_number
                                current_number = ""
                        current_operation = buttons[i]
                    elif buttons[i] == 'C':
                        current_number = ""
                        stored_number = None
                        current_operation = None
                    elif buttons[i] == '=':
                        stored_number = calculate()
    
    screen.fill(WHITE)
    draw_display()
    draw_buttons()
    pygame.display.flip()

pygame.quit()
sys.exit()