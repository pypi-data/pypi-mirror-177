from codificador.cifraCesar.alphabet import *

def decode_word(palavra):
    palavra = palavra.upper()
    letras = []
    
    for letra in palavra:
        letras.append(CIFRA_CESAR_2[letra])
    nova_palavra = ''.join(letras)
    return nova_palavra

def decode_phrase(frase):
    frase = frase.upper()
    palavras = frase.split()

    for palavra in palavras:
        indice = palavras.index(palavra)
        nova_palavra = decode_word(palavra)
     
        palavras.pop(indice)
        palavras.insert(indice,nova_palavra)

    nova_frase = ' '.join(palavras)
    return nova_frase