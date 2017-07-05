@echo off

python -m pip install --upgrade pip wheel setuptools
pip install numpy
pip install pyyaml
python -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew
python -m pip install kivy

echo DONE
pause