class GramaticaASD:
    def __init__(self, reglas, simbolo_inicial, vacio='vacio'):
        self.reglas = reglas
        self.simbolo_inicial = simbolo_inicial
        self.vacio = vacio
        self.no_terminales = set(reglas.keys())
        self.terminales = set()

        for nt, producciones in reglas.items(): # Determinamos los terminales 
            for prod in producciones:
                for simbolo in prod:
                    if simbolo not in self.no_terminales and simbolo != self.vacio:
                        self.terminales.add(simbolo)

        self.primeros = {nt: set() for nt in self.no_terminales}
        self.siguientes = {nt: set() for nt in self.no_terminales}
        self.prediccion = {}


    def primeros_de_cadena(self, cadena, primeros):
        if not cadena:
            return {self.vacio}
        if len(cadena) == 1 and cadena[0] == self.vacio:
            return {self.vacio}
        
        resultado = set()
        
        for simbolo in cadena:
            if simbolo == self.vacio:
                resultado.add(self.vacio)
                break
            if simbolo in self.terminales:
                resultado.add(simbolo)
                return resultado
            if simbolo in self.no_terminales:
                resultado |= (primeros[simbolo] - {self.vacio})

                if self.vacio not in primeros[simbolo]:
                    return resultado
            else:
                resultado.add(simbolo)
                return resultado
        resultado.add(self.vacio)
        return resultado

    
    def calcular_primeros(self): #Aca aplicamos las reglas para calcular los primeros
        cambio = True
        while cambio:
            cambio = False
            for A, producciones in self.reglas.items():
                for alpha in producciones:
                    first_alpha = self.primeros_de_cadena(alpha, self.primeros)
                    antes = len(self.primeros[A])
                    self.primeros[A] |= first_alpha
                    if len(self.primeros[A]) != antes:
                        cambio = True

    
    def calcular_siguientes(self): #Reglas para calcular los siguientes
        self.siguientes[self.simbolo_inicial].add('$')
        cambio = True
        while cambio:
            cambio = False

            for B, producciones in self.reglas.items():
                for alpha in producciones:
                    for i, A in enumerate(alpha):
                        if A not in self.no_terminales:
                            continue
                        beta = alpha[i + 1:]  
                        first_beta = self.primeros_de_cadena(beta, self.primeros)
                        antes = len(self.siguientes[A])
                        self.siguientes[A] |= (first_beta - {self.vacio})

                        if (not beta) or (self.vacio in first_beta):
                            self.siguientes[A] |= self.siguientes[B]
                        if len(self.siguientes[A]) != antes:
                            cambio = True

    
    def calcular_prediccion(self): #Reglas para determinar los conjuntos de prediccion
        for A, producciones in self.reglas.items():
            for alpha in producciones:
                first_alpha = self.primeros_de_cadena(alpha, self.primeros)
                if self.vacio in first_alpha:
                    pred = (first_alpha - {self.vacio}) | self.siguientes[A]
                else:
                    pred = set(first_alpha)

                self.prediccion[(A, tuple(alpha))] = pred

    def analizar_gramatica(self):
        self.calcular_primeros()
        self.calcular_siguientes()
        self.calcular_prediccion()


if __name__ == "__main__":
    print("=> Conjuntos del primer ejercicio:")
    reglas1 = {
        'S': [['A', 'uno', 'B', 'C'], ['S', 'dos']],
        'A': [['B', 'C', 'D'], ['A', 'tres'], ['vacio']],
        'B': [['D', 'cuatro', 'C', 'tres'], ['vacio']],
        'C': [['cinco', 'D', 'B'], ['vacio']],
        'D': [['seis'], ['vacio']]
    }
    analisis1 = GramaticaASD(reglas1, simbolo_inicial='S', vacio='vacio')
    analisis1.analizar_gramatica()

    print(" Conjunto de Primeros ")
    for nt in sorted(analisis1.primeros.keys()):
        print(f"Primeros({nt}) = {analisis1.primeros[nt]}")

    print(" Conjunto de Siguientes")
    for nt in sorted(analisis1.siguientes.keys()):
        print(f"Siguientes({nt}) = {analisis1.siguientes[nt]}")

    print(" Conjuntos de prediccion")
    for (nt, prod), pred in analisis1.prediccion.items():
        produccion_str = f"{nt} -> {' '.join(prod)}"
        print(f"Pred({produccion_str:<20}) = {pred}")



    print("")
    print("=> Conjuntos del segundo ejercicio:")
    reglas2 = {
        'S': [['A', 'B', 'uno']],
        'A': [['dos', 'B'], ['vacio']],
        'B': [['C', 'D'], ['tres'], ['vacio']],
        'C': [['cuatro', 'A', 'B'], ['cinco']],
        'D': [['seis'], ['vacio']]
    }
    analisis2 = GramaticaASD(reglas2, simbolo_inicial='S', vacio='vacio')
    analisis2.analizar_gramatica()

    print(" Conjunto de Primeros ")
    for nt in sorted(analisis2.primeros.keys()):
        print(f"Primeros({nt}) = {analisis2.primeros[nt]}")

    print(" Conjunto de Siguientes")
    for nt in sorted(analisis2.siguientes.keys()):
        print(f"Siguientes({nt}) = {analisis2.siguientes[nt]}")

    print(" Conjuntos de prediccion")
    for (nt, prod), pred in analisis2.prediccion.items():
        produccion_str = f"{nt} -> {' '.join(prod)}"
        print(f"Pred({produccion_str:<20}) = {pred}")


    