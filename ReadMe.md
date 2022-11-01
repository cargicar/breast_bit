<h1> Breast BiT </h1>

We have use Big Data Transfer Learning (BiT) to train a network to detect maligns tumors in mammograms. This model is being deployed using Django



## Prerequisites

- Knowledge in Python
- Basic understanding of Django and the Web

## Resources

- [Keras BiT Example](https://keras.io/examples/vision/bit/)

## Tools

- [Python 3](https://www.python.org) : The Python Programming Language
- [Django](https://www.djangoproject.com) : The Web Framework for Python
- [TensorFlow](https://www.tensorflow.org) : The TensorFlow Machine Learning Library used to create the neural network

## Setup Instructions

```bash
# Clone the repository
git https://github.com/cargicar/breast_bit
# switch to it
cd breast_bit
```

- Create a virtual environment where all packages will be installed.

```bash
# Windows
py -3 -m venv env
# Linux and Mac
python3 -m venv env
# or use conda
conda create -n [my_env] python
```

- Activate the virtual environment.

```bash
# Windows
.\env\Scripts\activate
# Linux and Mac
source env/bin/activate
# or use conda
conda activate [my_env]
```

- Install all the required packages.

```bash
pip install -r requirements.txt
```

## Prepare Dataset



## Setup Django App

- Create new django project

```bash
# create new project in the current directory
django-admin startproject core .
# run web app
python manage.py runserver
# visit http://localhost:8000/ on your browser
```

- We will go ahead and update our settings.py file and then create a view that will perform the prediction and pass it to the frontend.


