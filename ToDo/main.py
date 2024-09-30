import pygame
import sys

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Enhanced To-Do List")

font = pygame.font.Font(None, 32)
small_font = pygame.font.Font(None, 24)

class Button:
    def __init__(self, x, y, width, height, text, color, text_size='normal'):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.font = small_font if text_size == 'small' else font

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surf = self.font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class TodoItem:
    def __init__(self, text):
        self.text = text
        self.completed = False
        self.rect = pygame.Rect(50, 0, WIDTH - 115, 40)
        self.checkbox = pygame.Rect(10, 0, 30, 30)
        self.remove_button = Button(WIDTH - 60, 0, 40, 40, "X", RED, 'small')

class TodoList:
    def __init__(self):
        self.items = []
        self.completed_items = []
        self.scroll_y = 0
        self.max_visible_items = 8

    def add_item(self, text):
        self.items.append(TodoItem(text))

    def remove_item(self, index):
        if 0 <= index < len(self.items):
            del self.items[index]

    def toggle_complete(self, index):
        if 0 <= index < len(self.items):
            item = self.items[index]
            item.completed = not item.completed
            if item.completed:
                self.completed_items.append(item)
                del self.items[index]
            else:
                self.items.append(item)
                self.completed_items.remove(item)

    def clear_completed(self):
        self.completed_items.clear()

todo_list = TodoList()

def draw_items(items, start_y, completed=False):
    for i, item in enumerate(items):
        item_y = start_y + i * 50 - todo_list.scroll_y
        if 0 <= item_y < HEIGHT - 100:
            item.rect.y = item_y
            item.checkbox.y = item_y + 5
            item.remove_button.rect.y = item_y
            
            pygame.draw.rect(screen, GRAY, item.rect, 2)
            pygame.draw.rect(screen, GRAY, item.checkbox, 2)
            item.remove_button.draw(screen)
            
            if completed or item.completed:
                pygame.draw.line(screen, GREEN, (item.checkbox.left, item.checkbox.centery),
                                 (item.checkbox.right, item.checkbox.centery), 2)
                pygame.draw.line(screen, GREEN, (item.checkbox.centerx, item.checkbox.top),
                                 (item.checkbox.centerx, item.checkbox.bottom), 2)
            
            text_surf = font.render(item.text, True, BLACK)
            screen.blit(text_surf, (item.rect.x + 10, item.rect.y + 10))

def main():
    clock = pygame.time.Clock()
    input_box = pygame.Rect(50, HEIGHT - 50, WIDTH - 100, 40)
    input_text = ""
    input_active = False

    clear_completed_button = Button(WIDTH - 200, 10, 180, 40, "Clear Completed", BLACK)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    input_active = True
                else:
                    input_active = False
                
                if event.button in (4, 5):  # Mouse wheel
                    todo_list.scroll_y += 30 if event.button == 4 else -30
                    todo_list.scroll_y = max(0, min(todo_list.scroll_y, max(0, len(todo_list.items) * 50 - HEIGHT + 100)))
                
                for i, item in enumerate(todo_list.items):
                    if item.checkbox.collidepoint(event.pos):
                        todo_list.toggle_complete(i)
                        break
                    if item.remove_button.is_clicked(event.pos):
                        todo_list.remove_item(i)
                        break

                if clear_completed_button.is_clicked(event.pos):
                    todo_list.clear_completed()
            
            if event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_RETURN:
                        todo_list.add_item(input_text)
                        input_text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        input_text += event.unicode

        screen.fill(WHITE)

        # Draw title
        title_text = font.render("My To-Do List", True, BLACK)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 10))

        # Draw to-do items
        draw_items(todo_list.items, 70)

        # Draw completed items
        if todo_list.completed_items:
            completed_text = font.render("Completed:", True, BLACK)
            screen.blit(completed_text, (50, HEIGHT // 2))
            draw_items(todo_list.completed_items, HEIGHT // 2 + 40, completed=True)

        # Draw input box and label
        pygame.draw.rect(screen, GRAY if input_active else BLACK, input_box, 2)
        input_label = font.render("Add new task:", True, BLACK)
        screen.blit(input_label, (input_box.x, input_box.y - 30))
        text_surface = font.render(input_text, True, BLACK)
        screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))

        # Draw clear completed button
        clear_completed_button.draw(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()