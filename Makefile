.PHONEY: install, build, run

install:
	pip install -r requirements.txt

build:

run:
	python Raytracer.py $(file)