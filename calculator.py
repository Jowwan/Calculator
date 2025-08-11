import pygame
import sys

pygame.init()

# Screen setup
WIDTH, HEIGHT = 350, 520
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Calculator")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)

# Fonts
font = pygame.font.Font(None, 40)

# Calculator variables
current_input = ""
result = ""
just_calculated = False  # Tracks if last action was '='

# Button layout (first row has C and BACKSPACE)
buttons = [
    ["C", "BACK", "", ""],  # "BACK" will be drawn as a big button
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["0", ".", "=", "+"]
]

button_width = 70
button_height = 70
button_spacing = 5

# Calculate starting X so margins match
total_buttons_width = len(
    buttons[0]) * button_width + (len(buttons[0]) - 1) * button_spacing
start_x = (WIDTH - total_buttons_width) // 2
start_y = 120


def draw_buttons():
    for row_idx, row in enumerate(buttons):
        for col_idx, label in enumerate(row):
            if label == "":
                continue  # Skip unused slots

            # Special case: BACKSPACE button takes up 3 columns
            if label == "BACK":
                x = start_x + (button_width + button_spacing)  # after C
                y = start_y
                w = button_width * 3 + button_spacing * 2
                pygame.draw.rect(screen, GRAY, (x, y, w, button_height))
                text_surface = font.render("<----", True, BLACK)
                screen.blit(
                    text_surface,
                    (x + w // 2 - text_surface.get_width() // 2,
                     y + button_height // 2 - text_surface.get_height() // 2)
                )
                break  # Skip rest of the row for BACKSPACE

            else:
                x = start_x + col_idx * (button_width + button_spacing)
                y = start_y + row_idx * (button_height + button_spacing)
                pygame.draw.rect(
                    screen, GRAY, (x, y, button_width, button_height))
                text_surface = font.render(label, True, BLACK)
                screen.blit(
                    text_surface,
                    (x + button_width // 2 - text_surface.get_width() // 2,
                     y + button_height // 2 - text_surface.get_height() // 2)
                )


def get_button_clicked(pos):
    for row_idx, row in enumerate(buttons):
        for col_idx, label in enumerate(row):
            if label == "":
                continue

            if label == "BACK":
                # Big backspace hitbox
                x = start_x + (button_width + button_spacing)
                y = start_y
                w = button_width * 3 + button_spacing * 2
                rect = pygame.Rect(x, y, w, button_height)
                if rect.collidepoint(pos):
                    return "BACK"
                break
            else:
                x = start_x + col_idx * (button_width + button_spacing)
                y = start_y + row_idx * (button_height + button_spacing)
                rect = pygame.Rect(x, y, button_width, button_height)
                if rect.collidepoint(pos):
                    return label
    return None


# Main loop
clock = pygame.time.Clock()
running = True
while running:
    screen.fill(WHITE)

    # Draw display
    pygame.draw.rect(screen, DARK_GRAY, (10, 10, WIDTH - 20, 70))
    display_text = font.render(current_input or result, True, WHITE)
    screen.blit(display_text, (15, 20))

    draw_buttons()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            clicked = get_button_clicked(event.pos)
            if clicked:
                if clicked == "C":
                    current_input = ""
                    result = ""
                    just_calculated = False

                elif clicked == "BACK":
                    current_input = current_input[:-1]

                elif clicked == "=":
                    try:
                        result = str(eval(current_input))
                        current_input = result  # Keep result for next calculation
                        just_calculated = True
                    except:
                        result = "Error"
                        current_input = ""
                        just_calculated = False

                else:
                    if just_calculated and clicked.isdigit():
                        current_input = clicked
                    else:
                        current_input += clicked
                    just_calculated = False

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
