# Reporte EDA - Operacion Dino Crash


## 1. Problema y dataset

### P1 - Morira en el siguiente frame?

La variable de salida seria `died_next_frame`.

Seria binaria porque solo puede tener dos valores:

- `0` = no muere
- `1` = si muere

Las variables que yo usaria serian:

1. `speed`  
   Porque si el juego va mas rapido, hay menos tiempo para reaccionar.

2. `dist_obstacle`  
   Porque indica que tan cerca esta el siguiente obstaculo.

3. `obstacle_type`  
   Porque no es lo mismo brincar un cactus que reaccionar a un pajaro.

4. `jump`  
   Para saber si el dinosaurio ya esta saltando.

5. `dino_height`  
   Para saber si esta en el piso o en el aire.

6. `duck`  
   Para saber si esta agachado.

En este caso una fila deberia representar un frame, porque queremos saber que pasa justo despues.

Yo creo que se necesitan muchas partidas y muchos frames para tener suficientes ejemplos de muerte y no muerte.

Un problema seria usar `died` como salida, porque esa variable dice que el dinosaurio ya murio. Eso no seria predecir, seria detectar algo que ya paso.

---

### P2 - Cuantos puntos alcanzara al morir?

La variable de salida seria `final_score`.

Esta variable seria numerica.

Las variables que usaria podrian ser:

- velocidad promedio
- cantidad de obstaculos
- cantidad de saltos
- duracion de la partida
- distancia promedio a los obstaculos
- cantidad de obstaculos de cada tipo

Aqui una fila deberia representar una partida completa.

Se necesitarian bastantes partidas para comparar partidas cortas con partidas largas.

Un problema seria usar informacion que solo conocemos al final de la partida, porque estariamos usando datos del futuro.

---

### P3 - Que tipo de obstaculo viene despues?

La salida seria `next_obstacle_type`.

Seria una variable de varias clases, por ejemplo:

- `cactus_small`
- `cactus_large`
- `bird`

Las entradas podrian ser:

- `speed`
- `score`
- `time_ms`
- ultimo tipo de obstaculo
- distancia desde el ultimo obstaculo
- frecuencia de obstaculos recientes

Aqui se podria usar una fila por frame o una fila por evento.

Un problema seria que un tipo de obstaculo aparezca mucho mas que los otros, porque el modelo podria aprender casi siempre la clase mas comun.



## 2. Diccionario y muestra

### Patron cuando `died = 1`

En el frame 82 se ve esto:

- `speed = 6.8`
- `obstacle_type = cactus_small`
- `dist_obstacle = 12`
- `jump = 0`
- `died = 1`

Lo que veo noto es que el dinosaurio estaba muy cerca del obstaculo y no estaba saltando.

Por eso creo que `dist_obstacle` y `jump` pueden ser variables importantes.

### Sirve `score` para predecir muerte en el siguiente frame?

No creo que sea de las mejores variables.

El `score` dice cuanto ha avanzado el jugador, pero no dice directamente si esta a punto de chocar.

Puede ayudar un poco porque con el tiempo aumenta la velocidad, pero la distancia al obstaculo y si esta saltando parecen mas importantes.

### Faltan columnas?

Si, yo agregaria algunas como:

- altura del dinosaurio
- si esta agachado
- velocidad vertical
- distancia vertical al obstaculo
- tiempo desde que empezo el salto
- tiempo de reaccion del jugador

Estas variables ayudarian a entender mejor lo que esta pasando antes de una muerte.

### Sirve `died` para P1?

Como esta definida, `died` solo dice que la partida ya termino.

Para P1 seria mejor usar algo como `died_next_frame`, para indicar si morira en el siguiente frame.

---

## 3. Checklist EDA

### Esta balanceada la clase?

No.

Hay aproximadamente 12,000 frames y solo 50 son de muerte.

Entonces:

`50 / 12000 x 100 = 0.42%`

Eso significa que casi todos los frames son de no muerte.

Por eso el dataset esta muy desbalanceado.

### Hay outliers?

Podria haberlos.

Ejemplos:

- distancias negativas
- velocidades demasiado altas
- tiempos imposibles
- valores diferentes de 0 y 1 en `jump`

Si aparecen datos asi, primero habria que revisar si son errores.

### Puede haber sesgo?

Si.

Por ejemplo, si todas las partidas fueran de jugadores expertos, los datos no representarian bien a jugadores principiantes.

Entonces el modelo podria funcionar bien con expertos y mal con otros jugadores.

### Por que no mezclar frames de una misma partida en Train y Test?

Porque los frames de una misma partida son muy parecidos.

Si algunos frames quedan en Train y otros de la misma partida en Test, el modelo practicamente ya vio informacion muy parecida.

Eso podria hacer que parezca mejor de lo que realmente es.

Por eso seria mejor separar las partidas usando `session_id`.

### Ejemplo de Data Leakage

Si queremos predecir si el dinosaurio morira y usamos el score final de la partida, estariamos usando informacion que todavia no deberiamos conocer.

Eso seria data leakage.

---

## 4. Interpretacion de los datos

P1 esta muy desbalanceado.

De 12,000 frames:

- 50 tienen `died = 1`
- aproximadamente 11,950 tienen `died = 0`

Eso da:

- 0.42% muerte
- 99.58% no muerte

Por eso usar solo accuracy seria enganoso.

Por ejemplo, un modelo que siempre diga `died = 0` tendria casi 99.58% de accuracy, pero no detectaria ninguna muerte.

Por eso conviene revisar tambien:

- Precision
- Recall
- F1-score

La variable `dist_obstacle` parece util porque se menciona que muchas muertes pasan cuando la distancia es menor a 20.

Ademas, en un ejemplo de muerte la distancia era 12.

Tambien vemos que el `score` tiene media de 28 y mediana de 18.

Eso indica que hay algunas partidas con scores altos que suben el promedio.

---

## 5. Eleccion de modelo

| Escenario | Tipo de problema | Modelo que podria servir |
|---|---|---|
| P1 | Clasificacion binaria | Regresion logistica o arbol |
| P2 | Regresion | Regresion lineal o arbol regresor |
| P3 | Clasificacion multiclase | Arbol o regresion logistica multinomial |

### P1

Como la salida es si o no, es clasificacion binaria.

Antes de entrenar habria que tomar en cuenta que hay muy pocas muertes comparadas con los frames normales.

### P2

Como queremos predecir un numero, seria regresion.

Se podria empezar con una regresion lineal para ver si funciona.

### P3

Como hay varios tipos de obstaculo, seria clasificacion multiclase.

---

## 6. Cuando no usar ciertos modelos

### Arbol muy profundo

Un arbol muy profundo podria aprender demasiado los datos de entrenamiento.

Luego podria fallar con datos nuevos.

A eso se le llama overfitting.

### Red neuronal

Una red neuronal podria tener sentido si tuvieramos muchisimos datos o informacion mas complicada, como imagenes o secuencias largas.

Si solo tenemos pocas columnas en una tabla, puede ser demasiado para lo que necesitamos.

### Regla fija

Tambien se podria hacer una regla sencilla:

`si dist_obstacle < 20 y jump = 0, entonces hay alto riesgo de muerte`

Ventajas:

- es facil de entender
- no necesita entrenamiento
- es rapida

Desventajas:

- el numero 20 puede no servir con todas las velocidades
- no toma en cuenta todos los obstaculos
- no toma en cuenta la altura del dinosaurio
- no aprende sola con nuevos datos

Un modelo de Machine Learning podria encontrar relaciones mas complicadas entre varias variables.

---

## Conclusion

El EDA sirve para revisar primero si los datos realmente tienen sentido antes de escoger un modelo.

En este problema parece que la distancia al obstaculo, la velocidad y si el dinosaurio esta saltando son datos importantes.

Tambien vimos que hay muy pocas muertes comparadas con los frames normales, asi que el dataset esta muy desbalanceado.

Antes de entrenar cualquier modelo habria que revisar los datos, evitar data leakage y separar bien las partidas entre Train y Test.

Despues de eso ya tendria sentido probar un modelo sencillo.