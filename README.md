# Calculadora de conjuntos PRIMEROS, SIGUIENTES y PREDICCIÓN (ASD Predictivo)

Este programa en Python calcula:

- **PRIMEROS** de los no terminales y de cadenas de símbolos.
- **SIGUIENTES** de los no terminales.
- **Conjuntos de PREDICCIÓN** de cada producción de la gramática.

---

## ¿Qué problema resuelve?

Dada una gramática libre de contexto representada en Python como un diccionario, el programa:

1. Identifica automáticamente cuáles símbolos son no terminales con las claves del diccionario de python.
2. Identifica cuáles son **terminales** 
3. Calcula los conjuntos **PRIMEROS**, **SIGUIENTES** y **PREDICCIÓN** siguiendo exactamente las reglas teóricas del análisis descendente predictivo.

El resultado final se imprime en consola.

---

## Estructura general del código

Todo el cálculo se encapsula en la clase:

- **`GramaticaASD`**

Dentro de esta clase, el método principal que orquesta todo es:

- **`analizar_gramatica()`**
  - llama a `calcular_primeros()`
  - luego `calcular_siguientes()`
  - y al final `calcular_prediccion()`

Esto es importante porque:
- Para calcular **SIGUIENTES** necesitas poder consultar **PRIMEROS**.
- Para calcular **PREDICCIÓN** necesitas **PRIMEROS** y (a veces) **SIGUIENTES**.

---

## Explicación detallada de las funciones:

### 1) `primeros_de_cadena(self, cadena, primeros)`

Esta función implementa, en esencia, lo que dicen las reglas teóricas:

- Si la cadena es vacía o es exactamente `[vacio]`, entonces:
  - **PRIMEROS(α) = {vacio}**
- Si la cadena empieza por un terminal `t`, entonces:
  - **PRIMEROS(α) = {t}**
- Si empieza por un no terminal `A`, entonces:
  - se agregan **PRIMEROS(A) − {vacio}**
  - y si `A` puede derivar a `vacio`, hay que seguir mirando el siguiente símbolo de la cadena, porque el “inicio real” podría venir del siguiente símbolo.
- Si todos los símbolos de la cadena pueden desaparecer (derivar a vacío), entonces:
  - **vacio** también pertenece a PRIMEROS(α)

---

### 2) `calcular_primeros(self)`

Calcula **PRIMEROS(A)** para cada no terminal **A**.

- Repite el proceso mientras siga habiendo cambios.
- Para cada producción `A -> α`:
  - calcula `PRIMEROS(α)`
  - lo une con `PRIMEROS(A)`

---

### 3) `calcular_siguientes(self)`

Calcula **SIGUIENTES(A)** para cada no terminal **A** siguiendo las reglas clásicas:

1. Al símbolo inicial se le agrega `$` (fin de cadena):
   - `$ ∈ SIGUIENTES(SimboloInicial)`

2. Para cada producción de la forma:
   - `B -> α A β`

   se aplican dos reglas:

   **(a)** Todo lo que pueda empezar `β` (sin contar vacío) puede ir después de `A`:
   - `PRIMEROS(β) − {vacio} ⊆ SIGUIENTES(A)`

   **(b)** Si `β` puede desaparecer (derivar a vacío), entonces lo que siga a `B` también puede seguir a `A`:
   - si `vacio ∈ PRIMEROS(β)` (o β es vacío), entonces:
   - `SIGUIENTES(B) ⊆ SIGUIENTES(A)`


**Idea en palabras simples:**  
SIGUIENTES(A) responde a:  
> “En alguna derivación válida, ¿qué terminales podrían aparecer inmediatamente después de A?”

---

### 4) `calcular_prediccion(self)`

Calcula el conjunto de predicción por producción (la regla típica de los analizadores predictivos):

Para cada producción `A -> α`:

- Si `vacio ∈ PRIMEROS(α)` entonces:
  - **PRED(A->α) = (PRIMEROS(α) − {vacio}) ∪ SIGUIENTES(A)**
- En caso contrario:
  - **PRED(A->α) = PRIMEROS(α)**

**¿Por qué aparece SIGUIENTES(A) cuando hay vacío?**  
Porque si `α` puede desaparecer, entonces el parser no “vería” ningún terminal producido por `α`. En ese caso, la decisión de aplicar esa regla se basa en lo que puede venir después de `A` (o sea, SIGUIENTES(A)).

---

### Ejecucion del codigo:
### Ejecución del código

```text
=> Conjuntos del primer ejercicio:
 Conjunto de Primeros.
Primeros(A) = {'cinco', 'tres', 'cuatro', 'vacio', 'seis'}
Primeros(B) = {'cuatro', 'vacio', 'seis'}
Primeros(C) = {'cinco', 'vacio'}
Primeros(D) = {'seis', 'vacio'}
Primeros(S) = {'cinco', 'uno', 'tres', 'cuatro', 'seis'}
 Conjunto de Siguientes
Siguientes(A) = {'uno', 'tres'}
Siguientes(B) = {'cinco', 'uno', 'tres', '$', 'seis', 'dos'}
Siguientes(C) = {'$', 'uno', 'tres', 'seis', 'dos'}
Siguientes(D) = {'uno', 'tres', '$', 'cuatro', 'seis', 'dos'}
Siguientes(S) = {'$', 'dos'}
 Conjuntos de prediccion
Pred(S -> A uno B C      ) = {'cinco', 'cuatro', 'tres', 'uno', 'seis'}
Pred(S -> S dos          ) = {'cinco', 'cuatro', 'uno', 'tres', 'seis'}
Pred(A -> B C D          ) = {'cinco', 'cuatro', 'uno', 'tres', 'seis'}
Pred(A -> A tres         ) = {'cinco', 'seis', 'cuatro', 'tres'}
Pred(A -> vacio          ) = {'uno', 'tres'}
Pred(B -> D cuatro C tres) = {'seis', 'cuatro'}
Pred(B -> vacio          ) = {'cinco', '$', 'uno', 'tres', 'seis', 'dos'}
Pred(C -> cinco D B      ) = {'cinco'}
Pred(C -> vacio          ) = {'$', 'uno', 'tres', 'seis', 'dos'}
Pred(D -> seis           ) = {'seis'}
Pred(D -> vacio          ) = {'$', 'cuatro', 'uno', 'tres', 'seis', 'dos'}

=> Conjuntos del segundo ejercicio:
 Conjunto de Primeros 
Primeros(A) = {'vacio', 'dos'}
Primeros(B) = {'cinco', 'cuatro', 'vacio', 'tres'}
Primeros(C) = {'cinco', 'cuatro'}
Primeros(D) = {'seis', 'vacio'}
Primeros(S) = {'cinco', 'uno', 'tres', 'cuatro', 'dos'}
 Conjunto de Siguientes
Siguientes(A) = {'cinco', 'tres', 'uno', 'cuatro', 'seis'}
Siguientes(B) = {'cinco', 'uno', 'tres', 'cuatro', 'seis'}
Siguientes(C) = {'cinco', 'uno', 'tres', 'cuatro', 'seis'}
Siguientes(D) = {'cinco', 'uno', 'tres', 'cuatro', 'seis'}
Siguientes(S) = {'$'}
 Conjuntos de prediccion
Pred(S -> A B uno        ) = {'cinco', 'cuatro', 'uno', 'tres', 'dos'}
Pred(A -> dos B          ) = {'dos'}
Pred(A -> vacio          ) = {'cinco', 'cuatro', 'tres', 'uno', 'seis'}
Pred(B -> C D            ) = {'cinco', 'cuatro'}
Pred(B -> tres           ) = {'tres'}
Pred(B -> vacio          ) = {'cinco', 'cuatro', 'uno', 'tres', 'seis'}
Pred(C -> cuatro A B     ) = {'cuatro'}
Pred(C -> cinco          ) = {'cinco'}
Pred(D -> seis           ) = {'seis'}
Pred(D -> vacio          ) = {'cinco', 'cuatro', 'uno', 'tres', 'seis'}
```