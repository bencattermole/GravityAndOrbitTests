import pygame
import Mover
import Vector
import random
import math
import time
import NeuralNetwork

Screen_Size = 1024
block_size = 4
WHITE = (200, 200, 200)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((Screen_Size, Screen_Size))
pygame.display.set_caption("Orbitals")

block_scale = int(Screen_Size/block_size)

clock = pygame.time.Clock()

pygame.init()

myfont = pygame.font.SysFont("monospace", 15)

label_y = myfont.render("I.", 1, (0, 0, 0))
label_x = myfont.render("Time", 1, (0, 0, 0))

'''
KNOWN GLITCH
 - shapiro delay will still be counted even if it influences the beam that is facing away from the observer at the
   time of crossing
   - i have implemented a fix, it worked in one case but then happened again, just a matter of fine tuning but a more
     proper fix would be to look at the vectors of it js

variables below are for the setup of the orbit between the two 'movers'
    - note these values are not the best as they ARE NOT based on simply keplers laws calculations but I am keeping them
      as the shape of orbit they produce is in my opinion nicer, if I ever add orbital decay and gravitational waves 
      emission I should change this as it will be easier maths to work with perfect circles(?)
'''

pos2 = Vector.Vector(620, 620)
pos = Vector.Vector(420, 420)
vel = Vector.Vector(1, -1)
vel2 = Vector.Vector(-1, 1)
accel = Vector.Vector(0, 0)
accel2 = Vector.Vector(0, 0)

mover = Mover.Pulsar(pos, vel, accel, 4, 20, 0)
mover2 = Mover.Mover(pos2, vel2, accel2, 4)

running = True

# tic = time.perf_counter()
# toc = time.perf_counter()
# print(f"ran two diffuse in {toc - tic:0.4f} seconds")

scroll = 0.5

line_draw_x = [22]
line_draw_y = [929]

pulses_info = [[0, 0, 0]]

num_of_reset = [0]
previous_prediction = [0]
current_prediction = [0]

n_one = NeuralNetwork.Neuron(2)
n_two = NeuralNetwork.Neuron(2)
n_three = NeuralNetwork.Neuron(2)

neurons = [n_one, n_two, n_three]

p = NeuralNetwork.Predictor(3)

network = NeuralNetwork.Network(neurons, p)


def graph_draw(detection, line_to_draw_y, line_to_draw_x, intensity, e_delay, s_delay):
    offset = -22 + 950 * num_of_reset[0]

    if line_to_draw_x[-1] == 1004:
        line_to_draw_x.clear()
        line_to_draw_x.append(22)
        line_to_draw_y.clear()
        line_to_draw_y.append(929)
        pulses_info.clear()
        pulses_info.append([0, 0, 0])
        num_of_reset[0] = num_of_reset[0] + 1

    if detection:
        # print(intensity)
        line_to_draw_y.append(929 - intensity*2)
        if not network.last_four_pulses:
            network.alert_pulse((line_draw_x[-1] + offset))
        elif abs(network.last_four_pulses[-1] - (line_draw_x[-1] + offset)) < 30:
            pass
        else:
            network.alert_pulse((line_draw_x[-1] + offset))

    else:
        line_to_draw_y.append(929)

    line_to_draw_x.append(line_to_draw_x[-1] + 1)

    for n in range(len(line_to_draw_x)):
        draw_circle = True

        if line_to_draw_y[n] != 929 and n != 2:
            pygame.draw.line(screen, (0, 0, 0), (line_to_draw_x[n], line_to_draw_y[n]), (line_to_draw_x[n-1], line_to_draw_y[n-1]), 1)
            draw_circle = False

        if n != 0:
            if line_to_draw_y[n-1] != 929:
                pygame.draw.line(screen, (0, 0, 0), (line_to_draw_x[n], line_to_draw_y[n]), (line_to_draw_x[n - 1], line_to_draw_y[n - 1]), 1)
                draw_circle = False

        if detection:
            if line_to_draw_y[n] != 929 and line_to_draw_y[n-1] == 929:
                if line_to_draw_x[n] != pulses_info[-1][2]:
                    e_delay = int(e_delay*100)/100
                    s_delay = int(s_delay * 100) / 100
                    new_pulse = [e_delay, s_delay, line_to_draw_x[n]]
                    pulses_info.append(new_pulse)

        if draw_circle:
            pygame.draw.circle(screen, (0, 0, 0), (line_to_draw_x[n], line_to_draw_y[n]), 1, 1)


def graph_pulse(x1, x2, y1, y2, radius, x_cor, y_cor, e_delay, s_delay):

    if x2 - x1 == 0:
        x2 += 0.000001

    m = (y2-y1)/(x2-x1)
    c = y1 - m*x1

    A = c - y_cor

    quada = (1 + m*m)
    quadb = (-2*x_cor + 2*A*m)
    quadc = (x_cor*x_cor + A*A - radius*radius)

    discrim = quadb*quadb - 4*quada*quadc

    if discrim <= 0:
        graph_draw(False, line_draw_y, line_draw_x, 1, e_delay, s_delay)
        pass
    else:

        xpos = (-1*quadb + math.sqrt(discrim))/(2*quada)
        ypos = m*xpos + c

        xneg = (-1*quadb - math.sqrt(discrim))/(2*quada)
        yneg = m*xneg + c

        distance = math.sqrt((xpos - xneg)**2 + (ypos - yneg)**2)
        graph_draw(True, line_draw_y, line_draw_x, distance, e_delay, s_delay)


def shapiro_delay(x1, x2, y1, y2, radius, x_cor, y_cor):

    if x2 - x1 == 0:
        x2 += 0.000001

    m = (y2-y1)/(x2-x1)
    c = y1 - m*x1

    A = c - y_cor

    quada = (1 + m*m)
    quadb = (-2*x_cor + 2*A*m)
    quadc = (x_cor*x_cor + A*A - radius*radius)

    discrim = quadb*quadb - 4*quada*quadc

    if discrim <= 0:
        return 0
    else:

        xpos = (-1*quadb + math.sqrt(discrim))/(2*quada)
        ypos = m*xpos + c

        xneg = (-1*quadb - math.sqrt(discrim))/(2*quada)
        yneg = m*xneg + c

        if yneg > 600 or ypos > 600:
            distance = 0
        else:
            distance = math.sqrt((xpos - xneg) ** 2 + (ypos - yneg) ** 2)
        pygame.draw.line(screen, (252, 215, 3), (xpos, ypos), (xneg, yneg), 5)
        return distance


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                up_vel = Vector.Vector(0, -1)
                mover.vel.add(up_vel)
            if event.key == pygame.K_a:
                left_vel = Vector.Vector(-1, 0)
                mover.vel.add(left_vel)
            if event.key == pygame.K_s:
                down_vel = Vector.Vector(0, 1)
                mover.vel.add(down_vel)
            if event.key == pygame.K_d:
                right_vel = Vector.Vector(1, 0)
                mover.vel.add(right_vel)
            if event.key == pygame.K_x:
                x, y = mover.vel.x, mover.vel.y
                cancel_vel = Vector.Vector(-x, -y)
                mover.vel.add(cancel_vel)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 5: scroll = max(scroll - 0.1, 0)
            if event.button == 4: scroll = min(scroll + 0.1, 5)

    pygame.display.update()
    screen.fill((0, 0, 0))

    mover.gravity(mover2.pos, mover2.mass)
    mover2.gravity(mover.pos, mover.mass)

    mover.update()
    mover.render(screen)

    mover2.update()
    mover2.render(screen)

    e_delay = mover.render_beam(screen)

    s_delay = shapiro_delay(mover.pos.x, (mover.pos.x + mover.rot_x), mover.pos.y, (mover.pos.y + mover.rot_y), 100, mover2.pos.x, mover2.pos.y)

    pygame.draw.rect(screen, (255, 252, 250), (0, 829, 1024, 1024), 128)
    pygame.draw.line(screen, (0, 0, 0), (20, 839), (20, 939), 2)
    pygame.draw.line(screen, (0, 0, 0), (20, 939), (1004, 939), 2)

    pygame.draw.circle(screen, (0, 255, 0), (80, 80), 15, 15)

    screen.blit(label_y, (1, 889))
    screen.blit(label_x, (492, 940))

    graph_pulse(mover.pos.x, (mover.pos.x + mover.rot_x), mover.pos.y, (mover.pos.y + mover.rot_y), 15, 80, 80, abs(e_delay), s_delay)


    pulse_id = []
    for pulse in pulses_info:
        if pulse == [0, 0, 0]:
            pass
        elif pulse[2] not in pulse_id:
            einstien_text_delay = myfont.render(f"E delay: {pulse[0]}", 1, (0, 0, 0))
            shapiro_text_delay = myfont.render(f"S delay: {pulse[1]}", 1, (0, 0, 0))
            screen.blit(einstien_text_delay, (pulse[2], 960))
            pygame.draw.rect(screen, (255, 0, 0), (pulse[2] - 16, 964, 8, 16), 4)
            pygame.draw.rect(screen, (0, 0, 255), (pulse[2] - 8, 964, 8, 16), 4)
            screen.blit(shapiro_text_delay, (pulse[2], 980))
            pygame.draw.rect(screen, (252, 215, 3), (pulse[2] - 16, 983, 16, 16), 8)
            pulse_id.append(pulse[2])

    if network.current_prediction != 0:
        has_changed = False
        dummy_val = 0
        pygame.draw.line(screen, (0, 0, 255), ((pulses_info[-1][2] + network.current_prediction), 939), ((pulses_info[-1][2] + network.current_prediction), 839), 2)
        if network.current_prediction != current_prediction[0]:
            if current_prediction[0] == 0 or pulses_info[-1][2] == 0:
                previous_prediction[0] = 0
            else:
                previous_prediction[0] = pulses_info[-2][2] + current_prediction[0]

            current_prediction[0] = network.current_prediction
            has_changed = True

        pygame.draw.line(screen, (64, 233, 255), ((previous_prediction[0]), 939),((previous_prediction[0]), 839), 2)



    clock.tick(30)
