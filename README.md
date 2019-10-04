# CalPal-hackNY
A diet tracker and recommend-er

# Installation

## Windows: 

- See what’s python version you have
```python
python --version
```

#### Make sure it’s python > 3

- Create virtual environment
```python
python -m venv venv3
```

- Activate the python environment

In Cmd : `venv3\Scripts\activate.bat`


- Install all the dependency:

`pip install -r requirements.txt`


- Run the code

`python app.py`

# Make a request 

- Request method  = POST

- http://192.168.1.163:5000/add

- Request param 
```json
{
	"image": "base64 string of an image"
}
```