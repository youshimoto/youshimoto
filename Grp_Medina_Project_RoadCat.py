import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
width, height = 1280, 800
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simple Pygame Example")

# Load images
player_image = pygame.image.load('cat_icon.png')  # Load your human icon image
enemy_image = pygame.image.load('car_icon.png')  # Load your car icon image
background_image = pygame.image.load('road.jpg')  # Load the background image

# Scale the background image to fit the window
background_image = pygame.transform.scale(background_image, (width, height))

# Resize images if necessary
player_image = pygame.transform.scale(player_image, (80, 50))  # Resize player image
enemy_image = pygame.transform.scale(enemy_image, (220, 120))  # Resize enemy image

# Load sound effects
death_sound = pygame.mixer.Sound('Meow.mp3')  # Death sound effect
pass_sound = pygame.mixer.Sound('car_pass.mp3')  # Car passing sound effect
win_sound = pygame.mixer.Sound('Victory.mp3')  # Winning sound effect (make sure this file exists)

# Function to display the score and options
def display_game_over(final_score, level):
    font = pygame.font.SysFont("Arial", 50)
    text = font.render(f"Game Over! Score: {final_score} Level: {level}", True, (255, 255, 255))
    window.blit(text, (width // 2 - text.get_width() // 2, height // 2 - text.get_height() // 2))

    # Play Again and Quit options
    font_small = pygame.font.SysFont("Arial", 30)
    play_again_text = font_small.render("Press R to Play Again or Q to Quit", True, (255, 255, 255))
    window.blit(play_again_text, (width // 2 - play_again_text.get_width() // 2, height // 2 + 50))

# Game loop
def game_loop():
    player_pos = [width // 2, height - 50]
    enemy_pos = [random.randint(0, width - 50), 0]
    enemy_speed = 25  # Initial speed of the enemy
    player_speed = 18  # Slower player speed
    score = 0
    level = 1  # Start at level 1

    # Set the frame rate
    clock = pygame.time.Clock()
    FPS = 30  # Frames per second

    # Game loop
    running = True
    game_over = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not game_over:
            # Player movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_pos[0] > 0:
                player_pos[0] -= player_speed  # Move left
            if keys[pygame.K_RIGHT] and player_pos[0] < width - 50:
                player_pos[0] += player_speed  # Move right

            # Update enemy position
            enemy_pos[1] += enemy_speed
            if enemy_pos[1] > height:
                enemy_pos[1] = 0  # Reset position to top
                enemy_pos[0] = random.randint(0, width - 50)  # Random new X position
                score += 1
                pass_sound.play()  # Play the car passing sound effect when the enemy resets

                # Increase level every 10 points
                if score % 10 == 0:
                    level += 1
                    enemy_speed += 5  # Increase enemy speed by 5 for each level

            # Collision detection (update this part)
            player_rect = pygame.Rect(player_pos[0], player_pos[1], 80, 50)
            enemy_rect = pygame.Rect(enemy_pos[0], enemy_pos[1], 180, 120)
            if player_rect.colliderect(enemy_rect):  # Check for collision
                pygame.mixer.music.stop()  # Stop the background music
                death_sound.play()  # Play the death sound effect
                game_over = True  # Set game over flag

            # Check if player reached level 5 (win condition)
            if level >= 5:
                win_sound.play()  # Play the winning sound effect
                font = pygame.font.SysFont("Arial", 50)
                win_text = font.render(f"YOU WIN! Final Score: {score}", True, (255, 255, 255))
                window.blit(win_text, (width // 2 - win_text.get_width() // 2, height // 2 - win_text.get_height() // 2))
                pygame.display.update()
                pygame.time.delay(3000)  # Wait for 3 seconds before closing the game
                running = False

        else:
            # Check for restart or quit
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:  # Restart the game
                game_loop()  # Call the game loop again
            if keys[pygame.K_q]:  # Quit the game
                running = False

        # Drawing
        window.blit(background_image, (0, 0))  # Draw the scaled background image
        if not game_over:
            window.blit(player_image, (player_pos[0], player_pos[1]))  # Draw player icon
            window.blit(enemy_image, (enemy_pos[0], enemy_pos[1]))  # Draw enemy icon

            # Display score and level during the game with the correct colors
            font = pygame.font.SysFont("Arial", 30)
            score_text = font.render(f"Score: {score}", True, (0, 0, 255))  # Blue color for score
            level_text = font.render(f"Level: {level}", True, (255, 0, 0))  # Red color for level
            window.blit(score_text, (10, 10))
            window.blit(level_text, (width - level_text.get_width() - 10, 10))
        else:
            display_game_over(score, level)  # Display game over screen

        pygame.display.update()

        # Control the frame rate
        clock.tick(FPS)

# Start the game
game_loop()

# Stop the music and quit Pygame
pygame.quit()
