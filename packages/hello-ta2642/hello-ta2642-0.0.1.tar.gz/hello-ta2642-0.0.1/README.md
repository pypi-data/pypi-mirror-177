
# Hello World


## Installation
Run the following to install:
```python
pip install hello
```

## Usage

```python
from helloworld import say_hello
# Generate "Hello, World!"
say_hello

#Generate hello, name
say_hello("name")
```

Tutorial from: https://www.youtube.com/watch?v=GIF3LaRqgXo&ab_channel=CodingTech

1. create src folder
2. put code .py under src folder
3. create init file within src folder

4. create setup.py outside of src folder

5. go on terminal and run
```python
python setup.py bdist_wheel
```
 -- this creates build and dist library

6. terminal and run 
```bash
pip install -e .
```
this installs package locally.
run it if you add new library so it installs all the library dependencies

7. source distribution- builds a wheel file
```bash
python setup.py bdist_wheel
```
8. check files under dist tar
```bash
tar tzf dist/hello-0.0.1.tar.gz
```

9. build it to publish
```bash
python setup.py bdist_wheel sdist
```
- it should have wheel file and source dist
