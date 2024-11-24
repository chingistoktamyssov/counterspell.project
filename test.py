import pygame
import sys
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Fighter Game with Animations")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Animation frame rate
ANIMATION_SPEED = 100  # Milliseconds per frame

# Player attributes
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 100
player1 = pygame.Rect(200, 170, PLAYER_WIDTH, PLAYER_HEIGHT)
player2 = pygame.Rect(550, 170, PLAYER_WIDTH, PLAYER_HEIGHT)

# Player speeds and gravity
player_speed = 5
gravity = 0.5
jump_strength = -10

# Player vertical velocities
player1_velocity_y = 0
player2_velocity_y = 0

# Player states
player1_on_ground = True
player2_on_ground = True
player1_state = "idle"  # States: "idle", "walk", "jump", "punch"
player2_state = "idle"

# Health
player1_health, player2_health = 100, 100

# Ground level
GROUND_LEVEL = HEIGHT - PLAYER_HEIGHT - 10


platform = pygame.Rect(0, 270, 1000, 10)  # A rectangular platform at (x, y) with width and height

# Load animation frames
def load_frames(folder):
    frames = []
    for file in sorted(os.listdir(folder)):
        if file.endswith(".png"):
            frame = pygame.image.load(os.path.join(folder, file))
            frame = pygame.transform.scale(frame, (PLAYER_WIDTH, PLAYER_HEIGHT))
            frames.append(frame)
    return frames

# Load all animations for both players
player1_animations = {
    "walk": load_frames("player1/walk"),
    "idle": load_frames("player1/idle"),
    "jump": load_frames("player1/jump"),
    "punch": load_frames("player1/punch"),  # Add punch animation
}

player2_animations = {
    "walk": load_frames("player2/walk"),
    "idle": load_frames("player2/idle"),
    "jump": load_frames("player2/jump"),
    "gun": load_frames("player2/gun"),  # Add gun animation
}

# Debug output: Ensure frames are loaded correctly
print("Player 1 Animations:", {state: len(frames) for state, frames in player1_animations.items()})
print("Player 2 Animations:", {state: len(frames) for state, frames in player2_animations.items()})

# Frame indices and timers
player1_frame_index = 0
player2_frame_index = 0
player1_last_update = 0
player2_last_update = 0

# Direction flags
player1_facing_right = True
player2_facing_right = True


class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((10, 5))  # Simple rectangle as projectile
        self.image.fill((255, 0, 0))  # Red projectile
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        if self.direction == "right":
            self.rect.x += 10  # Move right
        else:
            self.rect.x -= 10  # Move left

        # **Remove the projectile if it goes off-screen**
        if self.rect.x < 0 or self.rect.x > WIDTH:
            self.kill()

# Punch collision box
punch_box = pygame.Rect(0, 0, 50, 30)  # Define a rectangular area for punch hitbox
projectiles = pygame.sprite.Group()

background = pygame.image.load("background.jpg")  # Replace with your image file
background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # Scale to fit the screen

def reset_game():
    global player1, player2
    global player1_velocity_y, player2_velocity_y
    global player1_on_ground, player2_on_ground
    global player1_health, player2_health
    global projectiles
    player1 = pygame.Rect(100, HEIGHT - PLAYER_HEIGHT - 10, PLAYER_WIDTH, PLAYER_HEIGHT)
    player2 = pygame.Rect(WIDTH - 150, HEIGHT - PLAYER_HEIGHT - 10, PLAYER_WIDTH, PLAYER_HEIGHT)
    player1_velocity_y = 0
    player2_velocity_y = 0
    player1_on_ground = True
    player2_on_ground = True
    player1_health = 100
    player2_health = 100
    projectiles.empty()  # Clear all projectiles

def display_game_over():
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", True, BLACK)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 4))

    play_again_text = font.render("Play Again?", True, BLACK)
    play_again_rect = play_again_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(play_again_text, play_again_rect)

    # Create a play again button area (simple rectangle)
    play_again_button = pygame.Rect(WIDTH // 2, HEIGHT // 2 + 50, 200, 50)
    pygame.draw.rect(screen, (0, 255, 0), play_again_button)
    # Check for mouse clicks on the Play Again button
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()
    if play_again_button.collidepoint(mouse_pos) and mouse_pressed[0]:
        return True  # Button clicked, return True to reset game

    return False

# Game loop
def main():
    global player1_velocity_y, player2_velocity_y
    global player1_on_ground, player2_on_ground
    global player1_health, player2_health
    global player1_frame_index, player2_frame_index
    global player1_last_update, player2_last_update
    global player1_facing_right, player2_facing_right
    global player1_state, player2_state
    global punch_box
    global projectiles

    # Flag to track punch key press
    punch_pressed = False
    game_over = False

    punch_cooldown = 300
    last_punch_time = 0
    projectile_cooldown = 300  # 500ms cooldown
    last_shot_time = 0  # The last time a projectile was shot



    running = True
    while running:
        screen.fill(WHITE)

        # **Blit (draw) the background image** at the start of each frame
        screen.blit(background, (0, 0))  # Draw the background at position (0, 0)
        pygame.draw.rect(screen, (255, 255, 255), platform)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Get keys
        keys = pygame.key.get_pressed()

        # Player 1 movement (WASD)
        moving1 = False
        if keys[pygame.K_a] and player1.left > 0:
            player1.x -= player_speed
            moving1 = True
            player1_facing_right = False
        if keys[pygame.K_d] and player1.right < WIDTH:
            player1.x += player_speed
            moving1 = True
            player1_facing_right = True
        if keys[pygame.K_w] and player1_on_ground:
            player1_velocity_y = jump_strength
            player1_on_ground = False

        # Player 2 movement (Arrow Keys)
        moving2 = False
        if keys[pygame.K_LEFT] and player2.left > 0:
            player2.x -= 6
            moving2 = True
            player2_facing_right = False
        if keys[pygame.K_RIGHT] and player2.right < WIDTH:
            player2.x += 6
            moving2 = True
            player2_facing_right = True
        if keys[pygame.K_UP] and player2_on_ground:
            player2_velocity_y = -13
            player2_on_ground = False

        # Player 1 punch (E key) — only trigger when 'E' is pressed
        if keys[pygame.K_e] and not punch_pressed:
            current_time1 = pygame.time.get_ticks()
            if current_time1 - last_punch_time >= punch_cooldown:  # Check if cooldown passed
                last_punch_time = current_time1  # Update the last shot time
            player1_state = "punch"
            player1_frame_index = 0  # Reset to the first punch framedddd
            punch_pressed = True  # Prevent multiple punches

        if not keys[pygame.K_e]:  # Reset punch flag when key is released
            punch_pressed = False
            player1_state = "walk"

        if keys[pygame.K_RETURN]:
            current_time = pygame.time.get_ticks()  # Get current time in milliseconds
            if current_time - last_shot_time >= projectile_cooldown:  # Check if cooldown passed
                if player2_facing_right:
                    projectile = Projectile(player2.x + PLAYER_WIDTH, player2.y + PLAYER_HEIGHT // 2, "right")
                else:
                    projectile = Projectile(player2.x, player2.y + PLAYER_HEIGHT // 2, "left")
                projectiles.add(projectile)
                last_shot_time = current_time  # Update the last shot time

        # Apply gravity
        if not player1_on_ground:
            player1_velocity_y += gravity
            player1.y += player1_velocity_y
            if player1.colliderect(platform) and player1_velocity_y > 0:  # Check for collision with platform
                player1.y = platform.top - PLAYER_HEIGHT  # Place player on platform
                player1_velocity_y = 0
                player1_on_ground = True
            elif player1.bottom >= HEIGHT:
                player1.y = GROUND_LEVEL
                player1_velocity_y = 0
                player1_on_ground = True

        if not player2_on_ground:
            player2_velocity_y += gravity
            player2.y += player2_velocity_y
            if player2.colliderect(platform) and player2_velocity_y > 0:  # Check for collision with platform
                player2.y = platform.top - PLAYER_HEIGHT  # Place player on platform
                player2_velocity_y = 0
                player2_on_ground = True
            elif player2.bottom >= HEIGHT:
                player2.y = GROUND_LEVEL
                player2_velocity_y = 0
                player2_on_ground = True

        # Update player states and reset frame indices
        new_player1_state = "jump" if not player1_on_ground else "walk" if moving1 else "idle"
        if player1_state != "punch":
            if new_player1_state != player1_state:
                player1_state = new_player1_state
                player1_frame_index = 0  # Reset frame index

        new_player2_state = "jump" if not player2_on_ground else "walk" if moving2 else "idle"

        if new_player2_state != player2_state:
            player2_state = new_player2_state
            player2_frame_index = 0  # Reset frame index

        # Update animations
        current_time = pygame.time.get_ticks()
        if current_time - player1_last_update > ANIMATION_SPEED:
            player1_frame_index = (player1_frame_index + 1) % len(player1_animations[player1_state])
            player1_last_update = current_time

        if current_time - player2_last_update > ANIMATION_SPEED:
            player2_frame_index = (player2_frame_index + 1) % len(player2_animations[player2_state])
            player2_last_update = current_time

        # Safely assign frames
        if player1_animations[player1_state]:
            player1_frame = player1_animations[player1_state][player1_frame_index]
        else:
            print(f"No frames for Player 1 state: {player1_state}")
            player1_frame = None

        if player2_animations[player2_state]:
            player2_frame = player2_animations[player2_state][player2_frame_index]
        else:
            print(f"No frames for Player 2 state: {player2_state}")
            player2_frame = None

        # Punch hit detection
        if player1_state == "punch" and player1_facing_right:
            punch_box = pygame.Rect(player1.x + PLAYER_WIDTH, player1.y + 20, 50, 30)  # Right-facing punch
        elif player1_state == "punch" and not player1_facing_right:
            punch_box = pygame.Rect(player1.x - 50, player1.y + 20, 50, 30)  # Left-facing punch

        # Check if punch collides with player2
        if punch_box.colliderect(player2):
            player2_health -= 1  # Decrease health by 1 on collision

        # Draw players using animation frames, flipped if necessary
        if player1_frame:
            if not player1_facing_right:
                player1_frame = pygame.transform.flip(player1_frame, True, False)
            screen.blit(player1_frame, (player1.x, player1.y))

        if player2_frame:
            if not player2_facing_right:
                player2_frame = pygame.transform.flip(player2_frame, True, False)
            screen.blit(player2_frame, (player2.x, player2.y))

        projectiles.update()

        # **Check for collisions between projectiles and Player 1**
        for projectile in projectiles:
            if projectile.rect.colliderect(player1):
                player1_health -= 9  # Damage Player 1
                projectile.kill()  # Remove the projectile after collision

        # Draw projectiles
        projectiles.draw(screen)
        # Draw health bars
        pygame.draw.rect(screen, (255, 0, 0), (10, 10, player1_health * 2, 20))
        pygame.draw.rect(screen, (0, 0, 255), (WIDTH - 210, 10, player2_health * 2, 20))

        # Check for game over
        if player1_health <= 0 or player2_health <= 0:
            winner = "Jake Paul" if player2_health <= 0 else "Hawk Tuah girl"
            font = pygame.font.Font(None, 74)
            text = font.render(f"{winner} Wins!", True, BLACK)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
            pygame.display.flip()
            pygame.time.wait(3000)  # Wait for 3 seconds before quitting
            running = False




        # Update the display
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
