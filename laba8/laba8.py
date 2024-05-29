import glfw
from OpenGL.GL import *
from math import cos, sin, sqrt, asin, pi
from PIL import Image
import random
import time
import numpy as np


alpha, beta = 0.0, 0.0 
vector_speed, speed = 0.009, 0.0
fill = False
is_move, is_light, is_tek = 0, 0, 1
R, G, B = 155, 456, 89


sides = [
    (1/2, 1/2, 8**(1/4)/4),#A
    (0, sqrt(2)/2, -8**(1/4)/4),#E
    (-1/2, 1/2, 8**(1/4)/4),#B
    (-sqrt(2)/2, 0, -8**(1/4)/4),#H
    (-1/2, -1/2, 8**(1/4)/4),#D
    (0, -sqrt(2)/2, -8**(1/4)/4),#F
    (1/2, -1/2, 8**(1/4)/4),#C
    (sqrt(2)/2, 0, -8**(1/4)/4)#G
]
root1 = [
    (1/2, 1/2, 8**(1/4)/4),#A
    (-1/2, 1/2, 8**(1/4)/4),#B
    (-1/2, -1/2, 8**(1/4)/4),#D
    (1/2, -1/2, 8**(1/4)/4)#C
]
root2 = [
    (sqrt(2)/2, 0, -8**(1/4)/4),#G
    (0, sqrt(2)/2, -8**(1/4)/4),#E
    (-sqrt(2)/2, 0, -8**(1/4)/4),#H
    (0, -sqrt(2)/2, -8**(1/4)/4),#F
]
tek_list = [
    (0, 0), 
    (0, 1), 
    (1, 0), 
    (1, 1)
]


def compute_norm(a, b, c):
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


def move(): 
    global vector_speed, speed
    speed -= vector_speed
    if speed < -1 or speed > 1:
        vector_speed = -vector_speed


def load_tex(): 
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, glGenTextures(1))

    image = Image.open('/Users/molivka/vs/iu9-graphics/laba8/ruby.jpeg')
    image = image.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = image.convert("RGBA").tobytes()

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)


def light():
    glShadeModel(GL_SMOOTH) 
    glLightModelf(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE) 
    glEnable(GL_NORMALIZE)

    light_pos = [10.0, 10.0, 10.0, 0.0]  
    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)

    glLightfv(GL_LIGHT0, GL_AMBIENT, [0, 0, 0, 1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [1, 1, 1, 1])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [1, 1, 1, 1])

    glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, 180.0)
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.5)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.05)
    glLightfv(GL_LIGHT0, GL_SPOT_EXPONENT, 0)
    
    ambient = [0.0, 0.0, 0.0, 0.0] 
    diffuse = [0.4, 0.7, 0.2]
    specular = [1.0, 1.0, 1.0, 1.0] 
    shininess = [1] 
    emission = [0.0, 0.0, 0.0, 0.0] 

    glMaterialfv(GL_FRONT, GL_AMBIENT, ambient) 
    glMaterialfv(GL_FRONT, GL_DIFFUSE, diffuse) 
    glMaterialfv(GL_FRONT, GL_SPECULAR, specular) 
    glMaterialfv(GL_FRONT, GL_SHININESS, shininess) 
    glMaterialfv(GL_FRONT, GL_EMISSION, emission) 


def prizma():
    global R, G, B

    glBegin(GL_POLYGON)
    #верхняя
    if (1 - is_tek):
        glColor3f(R / 255, G / 255, B / 255) 
    for i in range(len(root1)):
        if is_tek:
            glTexCoord2f(tek_list[i][0], tek_list[i][1])
        glVertex3f(root1[i][0], root1[i][1], root1[i][2])
    normal = compute_norm(root1[0], root1[1], root1[2])
    glNormal3f(normal[0], normal[1], normal[2])
    glEnd()
    #стороны
    glBegin(GL_TRIANGLES)
    for i in range(8):
        if is_tek:
            glTexCoord2f(tek_list[0][0], tek_list[0][1])
        else:
            glColor3f(R / 255, G / 255, B / 255) 
        a, b, c = sides[i]
        glVertex3f(a, b, c)
        if is_tek:
            glTexCoord2f(tek_list[1][0], tek_list[1][1])
        a, b, c = sides[(i + 1) % 8]
        glVertex3f(a, b, c)
        if is_tek:
            glTexCoord2f(tek_list[2][0], tek_list[2][1])
        a, b, c = sides[(i + 2) % 8]
        glVertex3f(a, b, c)
        if is_tek:
            glTexCoord2f(tek_list[3][0], tek_list[3][1])
        normal = compute_norm(sides[i], sides[(i + 1) % 8], sides[(i + 2) % 8])
        glNormal3f(normal[0], normal[1], normal[2])
    glEnd()
    #нижняя
    glBegin(GL_POLYGON)
    if (1 - is_tek):
        glColor3f(R / 255, G / 255, B / 255) 
    for i in range(len(root2)):
        if is_tek:
            glTexCoord2f(tek_list[i][0], tek_list[i][1])
        glVertex3f(root2[i][0], root2[i][1], root2[i][2])
    normal = compute_norm(root2[0], root2[1], root2[2])
    glNormal3f(normal[0], normal[1], normal[2])
    glEnd()


def create_shader(shader_type, source):
    #контейнер для шейдера
    shader = glCreateShader(shader_type)
    #код шейдера 
    glShaderSource(shader, source)
    #компиляция 
    glCompileShader(shader)
    return shader


def display(window):
    global is_tek

    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    if is_move == 1:
        move()
    glTranslatef(speed, 0, 0)
    glTranslatef(0, speed, 0)
    glRotatef(alpha, 1, 0, 0)
    glRotatef(beta, 0, 1, 0)

    prizma()
    glShadeModel(GL_FLAT)

    glfw.swap_buffers(window)
    glfw.poll_events()


def key_callback(window, key, scancode, action, mods):
    global alpha, beta, is_move, is_light, is_tek
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
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            else:
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            fill = not fill
        elif key == glfw.KEY_L:
            if is_light:
                glEnable(GL_LIGHTING)
                glEnable(GL_LIGHT0)
            else:
                glDisable(GL_LIGHTING)
            is_light = 1 - is_light
        elif key == glfw.KEY_M:
            is_move = 1 - is_move
        elif key == glfw.KEY_T:
            is_tek = 1 - is_tek


def main():
    global R, G, B
    if not glfw.init():
        return
    window = glfw.create_window(640, 640, "laba8", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    #создание вершинного шейдера
    vertex = create_shader(GL_VERTEX_SHADER, """
            attribute vec3 aVert; //3D вектор
            varying vec3 n; //нормаль
            varying vec3 v; //вектор к камере
            varying vec2 uv; //текстурные координаты
            
            void main() {   
                uv = gl_MultiTexCoord0.xy;
                v = vec3(gl_ModelViewMatrix * gl_Vertex);
                n = normalize(gl_NormalMatrix * gl_Normal);
                gl_TexCoord[0] = gl_TextureMatrix[0]  * gl_MultiTexCoord0;
                //позиция вершины в пространстве
                gl_Position = gl_ModelViewProjectionMatrix * vec4(gl_Vertex.x, gl_Vertex.y, gl_Vertex.z, 1); 
            }
            """)
    #создание фрагментного шейдера
    fragment = create_shader(GL_FRAGMENT_SHADER, """
            varying vec3 n;
            varying vec3 v; 
                             
            uniform sampler2D tex; //текстура
            void main () {  
                //вектор от поверхности к источнику света
                vec3 L = normalize(gl_LightSource[0].position.xyz - v); 
                //вектор к наблюдателю
                vec3 E = normalize(-v);
                //отражённый относительно нормали вектор света 
                vec3 R = normalize(-reflect(L,n));  
                //амбидентная часть освещения
                vec4 Iamb = gl_FrontLightProduct[0].ambient; 
                //диффузная часть освещения
                vec4 Idiff = gl_FrontLightProduct[0].diffuse * max(dot(n,L), 1.0);
                Idiff = clamp(Idiff, 2.0, 0.6);     
                //спекулярная часть освещения
                vec4 Ispec = gl_LightSource[0].specular * pow(max(dot(R,E),0.0),0.7); 
                Ispec = clamp(Ispec, 0.0, 1.0); 
                //цвет текстуры
                vec4 texColor = texture2D(tex, gl_TexCoord[0].st); 
                gl_FragColor = (Idiff + Iamb + Ispec) * texColor;
            }
            """)
    
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    load_tex()
    #создание и линковка шейдеров
    program = glCreateProgram()
    glAttachShader(program, vertex)
    glAttachShader(program, fragment)
    glLinkProgram(program)

    #использование массивов вершин, нормалей и цветов
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glEnableClientState(GL_COLOR_ARRAY)
    #включение текстуры
    if is_tek:
        glEnableClientState(GL_TEXTURE_COORD_ARRAY) 

    prizma()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    #установка шейдерной программы в качестве основной
    glUseProgram(program)

    while not glfw.window_should_close(window):
        display(window)
    glfw.destroy_window(window)
    glfw.terminate()

main()