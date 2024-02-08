import glfw
from OpenGL.GL import *

delta = 0.05
angle = 0.0
posx = -0.5
posy = -0.5
size = 0.0

def display(window):
    global angle
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glClearColor(0.0, 0.0, 0.0, 1.0) 
    glPushMatrix()
    glRotatef(angle, 0.45, 1, 0.90) 
    glBegin(GL_POLYGON)

    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(posx + 0 + size, posy + 0 + size)

    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(posx + 1 + size, posy + 0 - size)

    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(posx + 1 - size, posy + 1 - size)

    glColor3f(1.0, 1.0, 1.0)
    glVertex2f(posx + 0 - size, posy + 1 + size)

    glEnd()
    glPopMatrix()
    angle += delta
    glfw.swap_buffers(window)
    glfw.poll_events()

def key_callback(window, key, scancode, action, mods):
    global delta
    global angle
    global size
    if action == glfw.PRESS:
        if key == glfw.KEY_RIGHT:
            delta = -0.05
        if key == glfw.KEY_LEFT:
            delta = 0.05
        if key == glfw.KEY_ENTER:
            size = 0


def scroll_callback(window, xoffset, yoffset):
    global size
    if yoffset > 0:
        size -= xoffset / 10
    else:
        size += xoffset / 10


def main():
    if not glfw.init():
        return
    window = glfw.create_window(640, 640, "Laba1", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    while not glfw.window_should_close(window):
        display(window)
    glfw.destroy_window(window)
    glfw.terminate()

main()