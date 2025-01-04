# 🌀 3D Fractal Explorer

An interactive 3D visualization tool for exploring Mandelbrot and Julia sets, built with Python, OpenGL, and PyQt5.

![License](https://img.shields.io/github/license/melihcanndemir/3d-fractal-explorer)
![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![OpenGL](https://img.shields.io/badge/OpenGL-3.3+-green.svg)

## ✨ Features

- 🎨 Real-time 3D visualization of fractals
- 🔄 Interactive rotation and zoom capabilities
- 🌈 Dynamic color animation
- 🔲 Support for both Mandelbrot and Julia sets
- 🎮 Intuitive GUI controls
- 🖱️ Mouse-based navigation
- ⚡ Optimized performance with OpenGL

## 🚀 Getting Started

### Prerequisites

```bash
python 3.7+
PyQt5
PyOpenGL
numpy
```

### Installation

1. Clone the repository:
```bash
git clone https://github.com/melihcanndemir/3d-fractal-explorer.git
cd 3d-fractal-explorer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python fractal_explorer.pyw
```

## 📖 Educational Content

### What are Fractals?

Fractals are complex geometric patterns that repeat infinitely at different scales. They're created by repeating a simple mathematical process over and over.

### The Mathematics Behind It

#### Mandelbrot Set
The Mandelbrot set is defined by the function:
```
z₍ₙ₊₁₎ = zₙ² + c
```
where z₀ = 0 and c is a complex number. A point c is in the Mandelbrot set if the sequence remains bounded.

#### Julia Set
Julia sets use the same function as the Mandelbrot set:
```
z₍ₙ₊₁₎ = zₙ² + c
```
but here, c is fixed and z₀ varies. Each different value of c creates a different Julia set.

## 🎮 How to Use

1. **Basic Navigation**:
   - 🖱️ Left-click and drag to move around
   - 🖲️ Mouse wheel to zoom in/out
   - 🔄 Watch the automatic rotation

2. **Controls**:
   - Switch between Mandelbrot and Julia sets
   - Adjust iteration count for detail
   - Modify Julia set parameters
   - Control color animation speed

## 🔧 Technical Implementation

The project demonstrates several advanced programming concepts:

- 3D Graphics Programming with OpenGL
- Complex Number Mathematics
- Real-time Animation
- Event-driven Programming
- GUI Development with Qt
- Performance Optimization

### Key Components

```python
# Example of the core fractal calculation
def calculate_fractal(z, c, max_iter):
    n = 0
    while abs(z) <= 2 and n < max_iter:
        z = z*z + c
        n += 1
    return n
```

## 🤝 Contributing

Contributions are welcome! Here are ways you can contribute:

- 🐛 Report bugs
- ✨ Propose new features
- 📝 Improve documentation
- 🔍 Submit pull requests

## 📚 Learning Resources

To learn more about the concepts used in this project:

- [Fractal Mathematics](https://en.wikipedia.org/wiki/Fractal)
- [OpenGL Tutorial](https://learnopengl.com/)
- [PyQt5 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt5/)
- [Complex Numbers in Python](https://docs.python.org/3/library/cmath.html)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🌟 Acknowledgments

- Thanks to Benoit B. Mandelbrot for his groundbreaking work on fractals
- PyQt and OpenGL communities for their excellent documentation
- All contributors and users of this project

---

Made with ❤️ by Melih Can Demir

*"The beauty of fractals shows that simple rules can create infinite complexity."*
