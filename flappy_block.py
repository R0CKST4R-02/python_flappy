import pygame
import random  

# Inicializa o pygame
pygame.init()

# Definir largura e altura da tela
WIDTH, HEIGHT = 400, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Python")

# Carregar a imagem do jogador
player_img = pygame.image.load("game/player.png")  # Substitua pelo caminho correto da sua imagem
player_img = pygame.transform.scale(player_img, (30, 30))  # Redimensiona a imagem para 30x30

# Criando o bloco (jogador)
block = pygame.Rect(50, 200, 30, 30)
velocity = 0
gravity = 0.5

# Criando os obstáculos (canos)
pipe_width = 50
pipe_gap = 150
pipes = []

def create_pipe():
    height = random.randint(50, HEIGHT - pipe_gap - 50)
    pipes.append(pygame.Rect(WIDTH, 0, pipe_width, height))  
    pipes.append(pygame.Rect(WIDTH, height + pipe_gap, pipe_width, HEIGHT - height - pipe_gap))  

# Criar os primeiros obstáculos
create_pipe()

# Loop principal do jogo
running = True
clock = pygame.time.Clock()  
while running:
    screen.fill((0, 0, 0))  

    # Captura eventos (teclas e saída)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            velocity = -7  

    # Movimento do jogador
    velocity += gravity
    block.y += velocity

    # Movimento dos obstáculos
    for pipe in pipes:
        pipe.x -= 3  

    # Criar novos obstáculos
    if pipes and pipes[-1].x < WIDTH - 200:  
        create_pipe()

    # Remover obstáculos fora da tela
    pipes = [pipe for pipe in pipes if pipe.x > -pipe_width]

    # Desenha os obstáculos (canos)
    for pipe in pipes:
        pygame.draw.rect(screen, (0, 255, 0), pipe)  

    # Desenha o jogador com imagem
    screen.blit(player_img, (block.x, block.y))  

    pygame.display.flip()  
    clock.tick(30)  

pygame.quit()
