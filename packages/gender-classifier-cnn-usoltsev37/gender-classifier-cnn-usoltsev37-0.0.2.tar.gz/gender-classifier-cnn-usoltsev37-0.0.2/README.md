# hse-engineering-practices-ml

### HW02

#### Установка пакетного менеджера Pip (уже установленно, он дефолтный)

#### Развертывание окружения
```
python -m venv ./gender-classifier-cnn/env
```
#### Сборка пакета
```
python setup.py sdist bdist_wheel
twine upload --repository pypi dist/*
```
#### Ссылка на пакет в pypi-test

https://pypi.org/project/gender-classifier-cnn-usoltsev37/0.0.2/

#### Установка пакета из pypi-test
```
pip install gender-classifier-cnn-usoltsev37==0.0.2
```
#### P.S. 
Попробывал ```poetry```, возникли проблемы с установкой библиотеки torch на mac, это решение мне не помогло https://github.com/python-poetry/poetry/issues/6409?ysclid=lar7tjjma6220333470