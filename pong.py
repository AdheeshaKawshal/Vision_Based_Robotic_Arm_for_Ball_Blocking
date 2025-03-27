import math as mt
import pygame
import random



# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
balldir=[]
dir=1
# Paddle settings
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_RADIUS = 10

# Paddle positions
left_paddle = pygame.Rect(10, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 20, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2)

# Speeds
paddle_speed = 14
ball_speed_x = 9
ball_speed_y = 9

X = [] # Independent variable
Y = []  # Dependent variable
m=0
b=0
def linearRgression():
    # Compute means
    global m,b
    X_mean = sum(X) / len(X)
    y_mean = sum(Y) / len(Y)

    # Compute slope (m) using formula: m = Σ((xi - X_mean) * (yi - y_mean)) / Σ((xi - X_mean)^2)
    numerator = sum((X[i] - X_mean) * (Y[i] - y_mean) for i in range(len(X)))
    denominator = sum((X[i] - X_mean) ** 2 for i in range(len(X)))
    m = numerator / denominator

    # Compute intercept (b) using formula: b = y_mean - m * X_mean
    b = y_mean - m * X_mean

# Function to predict new values
def predict():
    yt=Y[len(Y)-1]
    xt=X[len(X)-1]
    s=mt.degrees(mt.atan(m))
    print(' s ',s)
    if m<10 and 0<m: return xt*m-yt
    elif m>-10 and 0>m: return 2*HEIGHT-xt*(-m)-yt
    else: return 0
    #return m * x + b

# Function to predict ball movement
def predict_ball_y(ball_x, ball_y, ball_speed_x, ball_speed_y):
    if ball_speed_x > 0:
        time_to_reach_paddle = (right_paddle.left - ball_x) / ball_speed_x
    else:
        time_to_reach_paddle = (left_paddle.right - ball_x) / abs(ball_speed_x)
    predicted_y = ball_y + ball_speed_y * time_to_reach_paddle
    while predicted_y < 0 or predicted_y > HEIGHT:
        if predicted_y < 0:
            predicted_y = -predicted_y
        elif predicted_y > HEIGHT:
            predicted_y = HEIGHT - (predicted_y - HEIGHT)
    return predicted_y

# Game loop
running = True
y_val=0
y=0
st=False;
prv_y=WIDTH/2
while running:
    
    pygame.time.delay(20)
    screen.fill(BLACK)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.y -= paddle_speed
    if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
        right_paddle.y += paddle_speed
    
    # Predict and move left paddle
    predicted_y = predict_ball_y(ball.x, ball.y, ball_speed_x, ball_speed_y)
    if left_paddle.centery < y:
        left_paddle.y += paddle_speed
    elif left_paddle.centery > y:
        left_paddle.y -= paddle_speed
    
    # Ball movement
    ball.x += ball_speed_x
    ball.y += ball_speed_y
    balldir.append(ball.x)
    if len(balldir)==5:
        if balldir[0]<balldir[4]:dir=-1
        else :dir=1
        balldir.clear()
        print(dir)
    # Ball collisions
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y *= -1
        st=False
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_speed_x *= -1
    if ball.x>300:st=True
    elif ball.x<50:st=False
    
    # Ball out of bounds
    if ball.left <= 0 or ball.right >= WIDTH:
        ball.x, ball.y = WIDTH // 2 - BALL_RADIUS, HEIGHT // 2 - BALL_RADIUS
        rn =random.uniform(-.5, .8)
        ball_speed_x *= -rn
    if len(X)==5 :
        linearRgression()
        if st and dir==1:y=predict()
        print('m',m)
        print('dr',dir)
        if y> HEIGHT:y=prv_y
        elif y<0:y=prv_y
        else: prv_y=y
        X=[]
        Y=[]
    print(st)
    # Draw paddles and ball
    pygame.draw.rect(screen, WHITE, left_paddle)
    pygame.draw.rect(screen, WHITE, right_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))
     # Draw ball path in a dotted way
    temp_x, temp_y = ball.x, ball.y
    temp_speed_x, temp_speed_y = ball_speed_x, ball_speed_y
    
    pygame.draw.circle(screen, (0,255,0), (20,y ), 10)  # Small    
    X.append(ball.x)
    Y.append(ball.y)
    for _ in range(140):  # Predict 20 steps ahead
        temp_x += temp_speed_x
        temp_y += temp_speed_y
        if temp_y <= 0 or temp_y >= HEIGHT:
            temp_speed_y *= -1
        if temp_x==10:
            y_val=temp_y;  # Small dots
            #pygame.draw.circle(screen, (0,255,0), (10, 10), 10)  # Small dots
        else :pygame.draw.circle(screen, WHITE, (temp_x, temp_y), 1)  # Small dots
    pygame.display.flip()
    
pygame.quit()
