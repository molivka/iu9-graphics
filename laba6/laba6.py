import glfw
from OpenGL.GL import *
from math import cos, sin, sqrt, asin, pi
from PIL import Image

alpha, beta = 0.0, 0.0 #углы поворота
vector_speed, speed = 0.009, 0.0
fill = False
is_move, is_light = 0, 0

def load_tex(): #генерация текстуры
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, glGenTextures(1))
    image = Image.open('/Users/molivka/vs/iu9-graphics/laba6/ruby.jpeg')
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = image.convert("RGBA").tobytes()
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

def compute_norm(a, b, c): #вычисление нормали
    x0, y0, z0 = a
    x1, y1, z1 = b
    x2, y2, z2 = c
    ux, uy, uz = [x1 - x0, y1 - y0, z1 - z0]
    vx, vy, vz = [x2 - x0, y2 - y0, z2 - z0]
    normal = [uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx]
    l = sqrt(normal[0] * normal[0] + normal[1] * normal[1] + normal[2] * normal[2])
    normal[0] /= l
    normal[1] /= l
    normal[2] /= l
    return normal

def prizma():
    glBegin(GL_POLYGON)
    #верхняя
    glTexCoord2f(0, 0)
    glVertex3f(1/2, 1/2, 8**(1/4)/4)#A
    glTexCoord2f(0, 1)
    glVertex3f(-1/2, 1/2, 8**(1/4)/4)#B
    glTexCoord2f(1, 0)
    glVertex3f(-1/2, -1/2, 8**(1/4)/4)#D
    glTexCoord2f(1, 1)
    glVertex3f(1/2, -1/2, 8**(1/4)/4)#C
    normal = compute_norm((1/2, 1/2, 8**(1/4)/4), (-1/2, 1/2, 8**(1/4)/4), (-1/2, -1/2, 8**(1/4)/4))
    glNormal3f(normal[0], normal[1], normal[2])
    glEnd()
    glBegin(GL_TRIANGLES)
    #1
    glTexCoord2f(0, 0)
    glVertex3f(1/2, 1/2, 8**(1/4)/4)#A
    glTexCoord2f(0, 1)
    glVertex3f(0, sqrt(2)/2, -8**(1/4)/4)#E
    glTexCoord2f(1, 0)
    glVertex3f(-1/2, 1/2, 8**(1/4)/4)#B
    glTexCoord2f(1, 1)
    normal = compute_norm((1/2, 1/2, 8**(1/4)/4), (0, sqrt(2)/2, -8**(1/4)/4), (-1/2, 1/2, 8**(1/4)/4))
    glNormal3f(normal[0], normal[1], normal[2])
    #2
    glTexCoord2f(0, 0)
    glVertex3f(0, sqrt(2)/2, -8**(1/4)/4)#E
    glTexCoord2f(0, 1)
    glVertex3f(-1/2, 1/2, 8**(1/4)/4)#B
    glTexCoord2f(1, 0)
    glVertex3f(-sqrt(2)/2, 0, -8**(1/4)/4)#H
    glTexCoord2f(1, 1)
    normal = compute_norm((0, sqrt(2)/2, -8**(1/4)/4), (-1/2, 1/2, 8**(1/4)/4), (-sqrt(2)/2, 0, -8**(1/4)/4))
    glNormal3f(normal[0], normal[1], normal[2])
    #3
    glTexCoord2f(0, 0)
    glVertex3f(-1/2, 1/2, 8**(1/4)/4)#B
    glTexCoord2f(0, 1)
    glVertex3f(-sqrt(2)/2, 0, -8**(1/4)/4)#H
    glTexCoord2f(1, 0)
    glVertex3f(-1/2, -1/2, 8**(1/4)/4)#D
    glTexCoord2f(1, 1)
    normal = compute_norm((-1/2, 1/2, 8**(1/4)/4), (-sqrt(2)/2, 0, -8**(1/4)/4), (-1/2, -1/2, 8**(1/4)/4))
    glNormal3f(normal[0], normal[1], normal[2])
    #4
    glTexCoord2f(0, 0)
    glVertex3f(-sqrt(2)/2, 0, -8**(1/4)/4)#H
    glTexCoord2f(0, 1)
    glVertex3f(-1/2, -1/2, 8**(1/4)/4)#D
    glTexCoord2f(1, 0)
    glVertex3f(0, -sqrt(2)/2, -8**(1/4)/4)#F
    glTexCoord2f(1, 1)
    normal = compute_norm((-sqrt(2)/2, 0, -8**(1/4)/4), (-1/2, -1/2, 8**(1/4)/4), (0, -sqrt(2)/2, -8**(1/4)/4))
    glNormal3f(normal[0], normal[1], normal[2])
    #5
    glTexCoord2f(0, 0)
    glVertex3f(-1/2, -1/2, 8**(1/4)/4)#D
    glTexCoord2f(0, 1)
    glVertex3f(0, -sqrt(2)/2, -8**(1/4)/4)#F
    glTexCoord2f(1, 0)
    glVertex3f(1/2, -1/2, 8**(1/4)/4)#C
    glTexCoord2f(1, 1)
    normal = compute_norm((-1/2, -1/2, 8**(1/4)/4), (0, -sqrt(2)/2, -8**(1/4)/4), (1/2, -1/2, 8**(1/4)/4))
    glNormal3f(normal[0], normal[1], normal[2])
    #6
    glTexCoord2f(0, 0)
    glVertex3f(0, -sqrt(2)/2, -8**(1/4)/4)#F
    glTexCoord2f(0, 1)
    glVertex3f(1/2, -1/2, 8**(1/4)/4)#C
    glTexCoord2f(1, 0)
    glVertex3f(sqrt(2)/2, 0, -8**(1/4)/4)#G
    glTexCoord2f(1, 1)
    normal = compute_norm((0, -sqrt(2)/2, -8**(1/4)/4), (1/2, -1/2, 8**(1/4)/4), (sqrt(2)/2, 0, -8**(1/4)/4))
    glNormal3f(normal[0], normal[1], normal[2])
    #7
    glTexCoord2f(0, 0)
    glVertex3f(1/2, -1/2, 8**(1/4)/4)#C
    glTexCoord2f(0, 1)
    glVertex3f(sqrt(2)/2, 0, -8**(1/4)/4)#G
    glTexCoord2f(1, 0)
    glVertex3f(1/2, 1/2, 8**(1/4)/4)#A
    glTexCoord2f(1, 1)
    normal = compute_norm((1/2, -1/2, 8**(1/4)/4), (sqrt(2)/2, 0, -8**(1/4)/4), (1/2, 1/2, 8**(1/4)/4))
    glNormal3f(normal[0], normal[1], normal[2])
    #8
    glTexCoord2f(0, 0)
    glVertex3f(sqrt(2)/2, 0, -8**(1/4)/4)#G
    glTexCoord2f(0, 1)
    glVertex3f(1/2, 1/2, 8**(1/4)/4)#A
    glTexCoord2f(1, 0)
    glVertex3f(0, sqrt(2)/2, -8**(1/4)/4)#E
    glTexCoord2f(1, 1)
    normal = compute_norm((sqrt(2)/2, 0, -8**(1/4)/4), (1/2, 1/2, 8**(1/4)/4), (0, sqrt(2)/2, -8**(1/4)/4))
    glNormal3f(normal[0], normal[1], normal[2])
    glEnd()
    #нижняя
    glBegin(GL_POLYGON)
    glTexCoord2f(0, 0)
    glVertex3f(sqrt(2)/2, 0, -8**(1/4)/4)#G
    glTexCoord2f(0, 1)
    glVertex3f(0, sqrt(2)/2, -8**(1/4)/4)#E
    glTexCoord2f(1, 0)
    glVertex3f(-sqrt(2)/2, 0, -8**(1/4)/4)#H
    glTexCoord2f(1, 1)
    glVertex3f(0, -sqrt(2)/2, -8**(1/4)/4)#F
    normal = compute_norm((sqrt(2)/2, 0, -8**(1/4)/4), (0, sqrt(2)/2, -8**(1/4)/4), (-sqrt(2)/2, 0, -8**(1/4)/4))
    glNormal3f(normal[0], normal[1], normal[2])
    glEnd()
    

def light(): #освещение
    glShadeModel(GL_SMOOTH) #режим интерполяции цветов между вершинами
    glLightModelf(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE) #установка глобальной модели освещения
    glEnable(GL_NORMALIZE) #нормировка нормалей

    glLightfv(GL_LIGHT0, GL_POSITION, [0, 0, 0, 1]) #позиция источника света
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0, 0, 0, 1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1, 1, 1, 1])

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.5)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.05)
    
    ambient = [0.0, 0.0, 0.0, 0.0] 
    diffuse = [90.0, 90.8, 90.8, 1.0] 
    specular = [100.0, 100.0, 100.0, 1.0] 
    shininess = [1] 
    emission = [0.0, 0.0, 0.0, 0.0] 

    glMaterialfv(GL_FRONT, GL_AMBIENT, ambient) #цвет фонового отражения материала
    glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse) #цвет рассеянного отражения материала
    glMaterialfv(GL_FRONT, GL_SPECULAR, specular) #цвет зеркального отражения материала
    glMaterialfv(GL_FRONT, GL_SHININESS, shininess) #степень в формуле зеркального отражения
    glMaterialfv(GL_FRONT, GL_EMISSION, emission)


def move(): #движение
    global vector_speed, speed
    speed -= vector_speed
    if speed < -1 or speed > 1:
        vector_speed = -vector_speed

def display(window):
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glLoadIdentity()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    if is_move == 1:
        move()
    glTranslatef(speed, 0, 0) #движение по оси 
    glTranslatef(0, speed, 0)
    glRotatef(alpha, 1, 0, 0)
    glRotatef(beta, 0, 1, 0)
    prizma()
    glfw.swap_buffers(window)
    glfw.poll_events()

def key_callback(window, key, scancode, action, mods):
    global alpha, beta, is_move, is_light
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_RIGHT:
            beta += 1
        elif key == glfw.KEY_LEFT:
            beta -= 1
        elif key == glfw.KEY_UP:
            alpha += 1
        elif key == glfw.KEY_DOWN:
            alpha -= 1
        elif key == glfw.KEY_F:
            global fill
            if fill :
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL) #твердотельное 
            else:
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE) #каркасное 
            fill = not fill
        elif key == glfw.KEY_L:
            if is_light:
                glEnable(GL_LIGHTING)
                glEnable(GL_LIGHT0)
                light()
            else:
                glDisable(GL_LIGHTING)
            is_light = 1 - is_light
        elif key == glfw.KEY_M:
            is_move = 1 - is_move

def main():
    if not glfw.init():
        return
    window = glfw.create_window(640, 640, "laba6", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    load_tex()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    light()
    while not glfw.window_should_close(window):
        display(window)
    glfw.destroy_window(window)
    glfw.terminate()

main()