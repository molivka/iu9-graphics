import glfw
from OpenGL.GL import *
from math import cos, sin, sqrt, asin, pi

alpha = 0.0
beta = 0.0
fill = False

def cube(sz):
    glBegin(GL_QUADS)
    #левая
    glColor3f(0.1, 0.0, 0.7)
    glVertex3f(-sz, -sz, -sz)
    glVertex3f(-sz, sz, -sz)
    glVertex3f(-sz, sz, sz)
    glVertex3f(-sz, -sz, sz)
    #правая
    glColor3f(0.4, 0.9, 0.0)
    glVertex3f(sz, -sz, -sz)
    glVertex3f(sz, -sz, sz)
    glVertex3f(sz, sz, sz)
    glVertex3f(sz, sz, -sz)
    #нижняя
    glColor3f(0.0, 1.0, 1.0)
    glVertex3f(-sz, -sz, -sz)
    glVertex3f(-sz, -sz, sz)
    glVertex3f(sz, -sz, sz)
    glVertex3f(sz, -sz, -sz)
    #верхняя
    glColor3f(0.0, 0.5, 0.8)
    glVertex3f(-sz, sz, -sz)
    glVertex3f(-sz, sz, sz)
    glVertex3f(sz, sz, sz)
    glVertex3f(sz, sz, -sz)
    #передняя
    glColor3f(0.5, 0.0, 0.8)
    glVertex3f(-sz, -sz, -sz)
    glVertex3f(sz, -sz, -sz)
    glVertex3f(sz, sz, -sz)
    glVertex3f(-sz, sz, -sz)
    #задняя
    glColor3f(1.0, 1.0, 1.0)
    glVertex3f(-sz, -sz, sz)
    glVertex3f(sz, -sz, sz)
    glVertex3f(sz, sz, sz)
    glVertex3f(-sz, sz, sz)

    glEnd()

def display(window):
    glEnable(GL_DEPTH_TEST) #отсечение заслонённых фигур
    glDepthFunc(GL_LESS) #обработка глубины(?)
    glClear(GL_COLOR_BUFFER_BIT)
    glClear(GL_DEPTH_BUFFER_BIT)

    glMatrixMode(GL_PROJECTION) #задаём видимое пространство 
    glLoadIdentity() #единичная матрица
    T = [1, 0, 0, 0,
         0, 1, 0, 0,
         0.5*cos(pi/4), 0.5*sin(pi/4), 1, 0,
         0, 0, 0, 1] #с какого ракурса видим объект 
    glMultMatrixf(T)

    glMatrixMode(GL_MODELVIEW) #матрица представления модели
    glLoadIdentity()
    Z = [cos(beta), 0, -sin(beta), 0,
         0, 1, 0, 0,
         sin(beta), 0, cos(beta), 0,
         0, 0, 0, 1] #вращение вокруг OZ
    Y = [1, 0, 0, 0,
         0, cos(alpha), -sin(alpha), 0,
         0, sin(alpha), cos(alpha), 0,
         0, 0, 0, 1] #вращение вокруг OY
    glMultMatrixf(Z)
    glMultMatrixf(Y)
    cube(0.3) #основной куб

    glLoadIdentity()
    T2 = [1, 0, 0, 0,
          0, 1, 0, 0,
          0, 0, 1, 0,
          0.7, 0.8, 0, 1] #координаты маленького кубика
    glMultMatrixf(T2)
    cube(0.1) #маленький кубик
    glfw.swap_buffers(window)
    glfw.poll_events()

def key_callback(window, key, scancode, action, mods):
    global alpha
    global beta
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_RIGHT:
            beta += 0.1
        elif key == glfw.KEY_LEFT:
            beta -= 0.1
        elif key == glfw.KEY_UP:
            alpha += 0.1
        elif key == glfw.KEY_DOWN:
            alpha -= 0.1
        elif key == glfw.KEY_F:
            global fill
            if fill :
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL) #твердотельное 
            else:
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE) #каркасное 
            fill = not fill

def main():
    if not glfw.init():
        return
    window = glfw.create_window(640, 640, "laba2", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    while not glfw.window_should_close(window):
        display(window)
    glfw.destroy_window(window)
    glfw.terminate()

main()