
def AlfaNum(cNumero):
    nValor    = 0
    lSoNumero = True
    nAtual    = 0
    cAscii    = ""
    nPosIni   = 0
    cCaract   = ""
    nValAux   = 0
    cZeros    = ""
    cNumero = cNumero.upper()
     
    #Percorre os valores
    for nAtual in range(len(cNumero)):
        cCaract = cNumero[nAtual]
        
        # Se encontrar uma letra
        if cCaract.isalpha():
            if nPosIni == 0:
                nPosIni = nAtual
            lSoNumero = False
            break  # Interrompe o loop ao encontrar uma letra
     
    #Se tiver somente numero, converte com Val
    if lSoNumero:
        nValor = int(cNumero)
    else:
        nValor = 0
         
        #Percorre os valores
        for nAtual in range(len(cNumero)):
            cCaract = cNumero[nAtual]
            cZeros = "0" * (len(cNumero) - nAtual - 1)
        
            # Se tiver alguma letra no número
            if cCaract.isalpha():
                # Converte a letra para número
                cAscii = str(ord(cCaract) - 64 + 9)  # Converte letra para número
                
                # Se for a partir da segunda posição e não for a última
                if nAtual > nPosIni and nAtual != len(cNumero) - 1:
                    nValAux = int(cAscii + cZeros) + (ord(cCaract) - 64) * 26
                    nValAux *= int(cAscii)
                    nValAux += (26 + int(cAscii))
                    nValor += nValAux
                else:
                    nValor += int(cAscii + cZeros) + (ord(cCaract) - 64) * 26
            # Se for somente números
            else:
                # Se for a partir da segunda posição e não for a última
                if nAtual > nPosIni and nAtual != len(cNumero) - 1:
                    nValor += int(cCaract + cZeros) + (36 * 26) + (26 * int(cCaract))
                else:
                    nValor += int(cCaract + cZeros)
    return nValor