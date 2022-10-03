import pygame as pg
from OpenGL.GL import *
import numpy as np
import ctypes
from OpenGL.GL.shaders import compileShader, compileProgram


class App:
    def __init__(self):
        # initial pygame
        pg.init()
        pg.display.set_mode((640, 480), pg.OPENGL | pg.DOUBLEBUF)
        self.clock = pg.time.Clock()

        # initial opengl
        glClearColor(0.1, 0.2, 0.2, 1)

        # 创建 shader （vertex shader、fragment shader）
        self.shader = self.create_shader("./shaders/vertex.txt", "./shaders/fragment.txt")
        # 将 shader 绑定到 OpenGL 上下文（在创建 Mesh 前绑定 shader 是一个好习惯）
        glUseProgram(self.shader)

        self.triangle = Triangle()
        self.main_loop()

    def create_shader(self, vertex_filepath, fragment_filepath):
        with open(vertex_filepath, "r", encoding="utf-8") as f:
            vertex_src = f.read()

        with open(fragment_filepath, "r", encoding="utf-8") as f:
            fragment_src = f.read()

        shader = compileProgram(
            compileShader(vertex_src, GL_VERTEX_SHADER),
            compileShader(fragment_src, GL_FRAGMENT_SHADER)
        )

        return shader

    def main_loop(self):
        running = True

        while running:
            # check events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False

            # refresh screen
            glClear(GL_COLOR_BUFFER_BIT)

            glUseProgram(self.shader)
            glBindVertexArray(self.triangle.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.triangle.vertex_count)

            pg.display.flip()

            # timing
            self.clock.tick(60)
        self.quit()

    def quit(self):
        self.triangle.destroy()
        glDeleteProgram(self.shader)
        pg.quit()


class Triangle:
    def __init__(self):
        # x, y, z, r, g ,b
        self.vertices = (
            -0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
            0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
            0.0, 0.5, 0.0, 0.0, 0.0, 1.0
        )

        self.vertices = np.array(self.vertices, dtype=np.float32)
        self.vertex_count = 3
        # 创建 VAO
        self.vao = glGenVertexArrays(1)
        # 在 OpenGL 上下文中绑定 VAO
        glBindVertexArray(self.vao)
        # 创建 VBO
        self.vbo = glGenBuffers(1)
        # 将创建的 VBO 绑定到 OpenGL 的上下文
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        # 定义 VBO 的存储方式（是静态存储还是动态存储）
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        # 启用 VAO 中的一个属性
        glEnableVertexAttribArray(0)
        # 定义该属性含义 ——
        # * 属性 index 为 0
        # * 属性 size 为 3
        # * 属性 type 为 GL_FLOAT (float32)
        # * 是否对该属性进行归一化
        # * VAO 每组属性的步长
        # * 该属性在 VBO 中的偏移量
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        # 启用 VAO 中的另一个属性
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))

    def destroy(self):
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.vbo,))


if __name__ == '__main__':
    app = App()
