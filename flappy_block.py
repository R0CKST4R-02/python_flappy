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
pipe_colors = []  # Lista para armazenar as cores dos canos
pipes_passed = []  # Lista para marcar os canos já contados na pontuação
score = 0  # Variável para armazenar a pontuação
font = pygame.font.Font(None, 36)  # Fonte para exibir a pontuação
game_won = False  # Variável para indicar se o jogo foi vencido

def create_pipe():
    """Cria um novo par de canos (superior e inferior)."""
    global score
    height = random.randint(50, HEIGHT - pipe_gap - 50)
    
    # Se for o 10º cano, ele será dourado
    color = (255, 255, 0) if score == 9 else (0, 255, 0)
    
    pipe_top = pygame.Rect(WIDTH, 0, pipe_width, height)
    pipe_bottom = pygame.Rect(WIDTH, height + pipe_gap, pipe_width, HEIGHT - height - pipe_gap)

    pipes.append(pipe_top)  
    pipes.append(pipe_bottom)  
    pipe_colors.append(color)  # Armazena a cor dos canos
    pipe_colors.append(color)  # Para ambos os canos (superior e inferior)
    pipes_passed.append(False)  # Marca que esse cano ainda não foi contado
    pipes_passed.append(False)  # Para o par de canos

# Criar os primeiros obstáculos
create_pipe()

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
    if pipes and pipes[-1].x < WIDTH - 200 and not game_won:  
        create_pipe()

    # Remover obstáculos fora da tela
    if pipes and pipes[0].x < -pipe_width:
        pipes.pop(0)  # Remove o cano de cima
        pipes.pop(0)  # Remove o cano de baixo
        pipe_colors.pop(0)  # Remove a cor correspondente
        pipe_colors.pop(0)  # Remove a cor correspondente
        pipes_passed.pop(0)  # Remove a marcação
        pipes_passed.pop(0)  # Remove a marcação

    # Verifica colisão com os canos
    for pipe in pipes:
        if block.colliderect(pipe):
            running = False  # Encerra o jogo se houver colisão

    # Verifica se o jogador passou por um cano e soma a pontuação
    for i in range(0, len(pipes), 2):  # Pega apenas os canos superiores
        if pipes[i].x + pipe_width < block.x and not pipes_passed[i]:
            score += 1
            pipes_passed[i] = True  # Marca que esse cano já foi contado
            pipes_passed[i + 1] = True  # Marca o par do cano também

            # Se o jogador passou pelo cano dourado (10º cano), ele vence o jogo
            if score == 10:
                game_won = True
                break

    # Desenha os obstáculos (canos) com suas cores corretas
    for i, pipe in enumerate(pipes):
        pygame.draw.rect(screen, pipe_colors[i], pipe)  

    # Desenha o jogador com imagem
    screen.blit(player_img, (block.x, block.y))  

    # Exibe a pontuação na tela
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # Verifica se o jogador caiu no chão ou saiu para cima
    if block.y > HEIGHT or block.y < 0:
        running = False  

    # Se o jogador venceu, exibe mensagem e pausa o jogo
    if game_won:
        win_text = font.render("VOCÊ VENCEU!", True, (255, 255, 0))
        screen.blit(win_text, (WIDTH // 2 - 80, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.delay(2000)  # Espera 2 segundos antes de fechar o jogo
        running = False

    pygame.display.flip()  
    clock.tick(30)  

pygame.quit()
