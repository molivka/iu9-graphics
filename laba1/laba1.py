import glfw
from OpenGL.GL import *

delta = 0.05
angle = 0.0
posx = -0.2
posy = -0.2
koef = 1.5

def display(window):
    global angle
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glClearColor(0.0, 0.0, 0.0, 1.0) 
    glPushMatrix()
    glRotatef(angle, 0.45, 1, 0.90) 
    glBegin(GL_POLYGON)

    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(posx + 0*koef, posy + 0*koef)

    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(posx + 0.2*koef, posy + 0.2*koef)

    glColor3f(0.0, 0.0, 0.1)
    glVertex2f(posx + 0.4*koef, posy + 0.2*koef)

    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(posx + 0.6*koef, posy + 0*koef)

    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(posx + 0.4*koef, posy - 0.2*koef)

    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(posx + 0.2*koef, posy - 0.2*koef)

    glColor3f(0.5, 0.5, 0.5)
    glVertex2f(posx + 0*koef, posy + 0*koef)

    glEnd()
    glPopMatrix()
    angle += delta
    glfw.swap_buffers(window)
    glfw.poll_events()

def key_callback(window, key, scancode, action, mods):
    global delta
    global angle
    if action == glfw.PRESS:
        if key == glfw.KEY_RIGHT:
            delta = -0.5
        if key == glfw.KEY_LEFT:
            delta = 0.5
        if key == glfw.KEY_ENTER:
            delta = 0

def main():
    if not glfw.init():
        return
    window = glfw.create_window(640, 640, "laba1", None, None)
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