from codificador.cifraCesar.alphabet import *

def encode_word(palavra):
    palavra = palavra.upper()
    letras = []
    
    for letra in palavra:
        letras.append(CIFRA_CESAR[letra])
    nova_palavra = ''.join(letras)
    return nova_palavra

def encode_phrase(frase):

    frase = frase.upper()
    palavras = frase.split()

    for palavra in palavras:
        indice = palavras.index(palavra)
        nova_palavra = encode_word(palavra)
        palavras.pop(indice)
        palavras.insert(indice,nova_palavra)
    
    nova_frase = ' '.join(palavras)
    return nova_frase

