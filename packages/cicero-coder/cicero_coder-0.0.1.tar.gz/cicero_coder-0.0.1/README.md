# package_name

Description. 
The package cifra_cesar is used to:
	- Crypt words and phrases by Caesar's Cipher
	- Decrypt words and phrases written in Caesar's Cipher.
 
## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install package_name

```bash
pip install package_name
```

## Usage

```python

from codificador.cifraCesar.encode import encode_phrase
phrase = 'Hello World'

# This function crypt the phrase 'Hello World'
crypt_phrase = encode_phrase(phrase)
print(crypt_phrase)
```
It'll return:
```
KHOOR ZRUOG
```
```python

from codificador.cifraCesar.encode import decode_phrase
#The inverse occours when we use the funcion decode_phrase
```

## Author
Cícero Hitzschky, @cicero.hitzschky

## License
[MIT](https://choosealicense.com/licenses/mit/)