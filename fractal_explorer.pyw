import sys
import time
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtOpenGL import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import colorsys
import math

class FractalWidget(QGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(800, 800)
        # Anti-aliasing disabled
        
        # Display parameters
        self.zoom = 1.0
        self.center_x = 0
        self.center_y = 0
        self.max_iter = 100
        self.fractal_type = "mandelbrot"  # or "julia"
        self.julia_c = complex(-0.4, 0.6)  # c parameter for Julia set
        self.color_offset = 0
        self.rotation = 0
        self.last_frame_time = time.time()
        
        # Timer for animation
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(16)  # ~60 FPS target
        
        # Arrays for vertex buffer
        self.vertex_array = []
        self.color_array = []
        
    def initializeGL(self):
        try:
            glEnable(GL_DEPTH_TEST)
            glEnable(GL_POINT_SMOOTH)  # Smooth points
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glPointSize(2.0)
            glClearColor(0.0, 0.0, 0.0, 1.0)
        except Exception as e:
            print(f"OpenGL Initialization Error: {e}")
        
    def resizeGL(self, w, h):
        try:
            glViewport(0, 0, w, h)
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            gluPerspective(45, w/h, 0.1, 100.0)
        except Exception as e:
            print(f"Resize Error: {e}")
        
    def paintGL(self):
        try:
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            glTranslatef(0, 0, -2.5)
            glRotatef(self.rotation, 0, 1, 0)
            
            # Fractal drawing
            if self.fractal_type == "mandelbrot":
                self.draw_mandelbrot()
            else:
                self.draw_julia()
        except Exception as e:
            print(f"Paint Error: {e}")
            
    def calculate_vertices(self):
        self.vertex_array = []
        self.color_array = []
        
        for i in range(-100, 100, 2):  # Increased step size for performance improvement
            for j in range(-100, 100, 2):
                x = i / 50 / self.zoom + self.center_x
                y = j / 50 / self.zoom + self.center_y
                
                if self.fractal_type == "mandelbrot":
                    c = complex(x, y)
                    z = 0
                else:
                    z = complex(x, y)
                    c = self.julia_c
                
                # Fractal iteration
                for n in range(self.max_iter):
                    if abs(z) > 2:
                        break
                    z = z*z + c
                
                if n < self.max_iter:
                    self.vertex_array.append((x, y, 0))
                    hue = (n + self.color_offset) % 360 / 360.0
                    r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
                    self.color_array.append((r, g, b))
            
    def draw_mandelbrot(self):
        self.calculate_vertices()
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        
        vertices = np.array(self.vertex_array, dtype=np.float32)
        colors = np.array(self.color_array, dtype=np.float32)
        
        glVertexPointer(3, GL_FLOAT, 0, vertices)
        glColorPointer(3, GL_FLOAT, 0, colors)
        glDrawArrays(GL_POINTS, 0, len(self.vertex_array))
        
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)
        
    def draw_julia(self):
        self.calculate_vertices()
        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        
        vertices = np.array(self.vertex_array, dtype=np.float32)
        colors = np.array(self.color_array, dtype=np.float32)
        
        glVertexPointer(3, GL_FLOAT, 0, vertices)
        glColorPointer(3, GL_FLOAT, 0, colors)
        glDrawArrays(GL_POINTS, 0, len(self.vertex_array))
        
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_COLOR_ARRAY)
        
    def animate(self):
        current_time = time.time()
        if hasattr(self, 'last_frame_time'):
            delta = current_time - self.last_frame_time
            if delta < 1/60:  # max 60 FPS
                return
                
        self.last_frame_time = current_time
        self.color_offset += 1
        self.rotation += 0.5
        self.update()
        
    def mousePressEvent(self, event):
        self.last_pos = event.pos()
        
    def mouseMoveEvent(self, event):
        try:
            dx = event.x() - self.last_pos.x()
            dy = event.y() - self.last_pos.y()
            
            if event.buttons() & Qt.LeftButton:
                self.center_x -= dx * 0.01 / self.zoom
                self.center_y += dy * 0.01 / self.zoom
                
            self.last_pos = event.pos()
            self.updateGL()
        except Exception as e:
            print(f"Mouse Move Error: {e}")
        
    def wheelEvent(self, event):
        try:
            if event.angleDelta().y() > 0:
                self.zoom *= 1.2
            else:
                self.zoom /= 1.2
            self.updateGL()
        except Exception as e:
            print(f"Wheel Event Error: {e}")

class FractalExplorer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('3D Fractal Explorer')
        self.init_ui()
        
    def init_ui(self):
        try:
            # Main widget
            main_widget = QWidget()
            self.setCentralWidget(main_widget)
            layout = QVBoxLayout(main_widget)
            
            # Fractal viewer
            self.fractal_widget = FractalWidget()
            layout.addWidget(self.fractal_widget)
            
            # Control panel
            controls = QHBoxLayout()
            
            # Fractal type selector
            fractal_combo = QComboBox()
            fractal_combo.addItems(['Mandelbrot', 'Julia'])
            fractal_combo.currentTextChanged.connect(self.change_fractal)
            controls.addWidget(QLabel('Fractal Type:'))
            controls.addWidget(fractal_combo)
            
            # Number of iterations
            iter_slider = QSlider(Qt.Horizontal)
            iter_slider.setRange(10, 500)
            iter_slider.setValue(100)
            iter_slider.valueChanged.connect(self.change_iterations)
            controls.addWidget(QLabel('Iteration:'))
            controls.addWidget(iter_slider)
            
            # Julia parameters
            self.julia_real = QDoubleSpinBox()
            self.julia_real.setRange(-2, 2)
            self.julia_real.setValue(-0.4)
            self.julia_real.setSingleStep(0.1)
            self.julia_real.valueChanged.connect(self.change_julia)
            
            self.julia_imag = QDoubleSpinBox()
            self.julia_imag.setRange(-2, 2)
            self.julia_imag.setValue(0.6)
            self.julia_imag.setSingleStep(0.1)
            self.julia_imag.valueChanged.connect(self.change_julia)
            
            controls.addWidget(QLabel('Julia c ='))
            controls.addWidget(self.julia_real)
            controls.addWidget(QLabel('+ i'))
            controls.addWidget(self.julia_imag)
            
            # Color speed control
            color_speed = QSlider(Qt.Horizontal)
            color_speed.setRange(0, 10)
            color_speed.setValue(1)
            color_speed.valueChanged.connect(self.change_color_speed)
            controls.addWidget(QLabel('Color Speed:'))
            controls.addWidget(color_speed)
            
            layout.addLayout(controls)
            
            # Status bar
            self.statusBar().showMessage('Ready')
            
            # Window size
            self.setMinimumSize(1000, 900)
            
        except Exception as e:
            print(f"UI Initialization Error: {e}")
        
    def change_fractal(self, fractal_type):
        try:
            self.fractal_widget.fractal_type = fractal_type.lower()
            self.fractal_widget.updateGL()
            self.statusBar().showMessage(f'{fractal_type} fractal selected')
        except Exception as e:
            print(f"Change Fractal Error: {e}")
        
    def change_iterations(self, value):
        try:
            self.fractal_widget.max_iter = value
            self.fractal_widget.updateGL()
            self.statusBar().showMessage(f'Number of iterations: {value}')
        except Exception as e:
            print(f"Change Iterations Error: {e}")
        
    def change_julia(self):
        try:
            real = self.julia_real.value()
            imag = self.julia_imag.value()
            self.fractal_widget.julia_c = complex(real, imag)
            self.fractal_widget.updateGL()
            self.statusBar().showMessage(f'Julia parameter: {real} + {imag}i')
        except Exception as e:
            print(f"Change Julia Error: {e}")
            
    def change_color_speed(self, value):
        try:
            self.fractal_widget.timer.setInterval(max(16, 100 - value * 8))
            self.statusBar().showMessage(f'Color change speed: {value}')
        except Exception as e:
            print(f"Change Color Speed Error: {e}")

def main():
    try:
        app = QApplication(sys.argv)
        window = FractalExplorer()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Application Error: {e}")

if __name__ == '__main__':
    main()