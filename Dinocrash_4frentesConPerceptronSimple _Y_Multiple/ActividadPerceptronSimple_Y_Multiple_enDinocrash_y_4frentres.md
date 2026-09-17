# Seleccion de Red Neuronal 

**Nombre:** irving garica 


# Operacion Dino Crash

## P1 - Morira en el siguiente frame?

### Resultado del EDA

Ya vimos que la salida es binaria:

- 0 = no muere
- 1 = muere

Tambien vimos que variables como:

* `dist_obstacle`
* `speed`
* `jump`
* `obstacle_type`

pueden influir en la muerte.

Otro problema importante es que hay muy pocos casos de muerte comparados con los frames donde no muere.

### Modelo propuesto

**Red neuronal multicapa**

### Por que?

Aunque la salida es binaria, la muerte puede depender de varias variables al mismo tiempo.

Por ejemplo, una distancia de 20 pixeles puede ser peligrosa si el juego va rapido, pero tal vez no lo sea si va lento y el dinosaurio ya esta saltando.

Un perceptron simple podria funcionar si los datos fueran separables con una sola linea, pero por la forma del problema parece mas razonable usar una red multicapa.

### Se puede resolver?

Si, pero primero hay que tomar en cuenta el desbalance del dataset y asegurarse de que las variables tengan suficiente informacion.


## P2 - Cuantos puntos alcanzara al morir?

### Resultado del EDA

La salida es un valor numerico:

`final_score`

Una fila representaria una partida completa.

### Modelo propuesto

**Red neuronal multicapa**

### Por que?

Aqui no queremos decidir entre 0 o 1.

Queremos obtener un numero, por ejemplo:

`final_score = 120`

El perceptron simple  trabaja mejor con problemas de clasificacion binaria.

Una red multicapa puede trabajar con varias variables para intentar estimar el score final.

### Se puede resolver?

Si, siempre que podamos obtener suficientes partidas completas y variables que realmente tengan relacion con el score.


## P3 - Que tipo de obstaculo viene despues?

### Resultado del EDA

La salida tiene varias posibles clases:

- cactus pequeno
- cactus grande
- pajaro

### Modelo propuesto

**Red neuronal multicapa**

### Por que?

Un perceptron simple con una sola salida funciona mejor cuando tenemos dos clases.

Aqui tenemos varias categorias diferentes.

Por eso una red multicapa tiene mas sentido.

### Se puede resolver?

Si, siempre que tengamos suficientes ejemplos de cada tipo de obstaculo.

Si casi todos los datos fueran de cactus y hubiera pocos ejemplos de pajaro, el modelo podria aprender mal.


# Operacion Cuatro Frentes

## Mision 1 - Semaforo Academico

### Resultado del EDA

La variable objetivo es:

`riesgo`

Y tiene tres clases:

- verde
- amarillo
- rojo

Tambien vimos que el riesgo tiene relacion con variables como:

- asistencia
- promedio de parciales
- tareas entregadas
- materias reprobadas

### Modelo propuesto

**Red neuronal multicapa**

### Por que?

Tenemos tres clases diferentes.

Ademas, varias variables pueden influir al mismo tiempo en el riesgo de un alumno.

Un perceptron simple con una sola salida no seria suficiente para manejar directamente las tres categorias.

### Se puede resolver?

Si.

El EDA muestra que existen patrones entre las variables y el nivel de riesgo.



## Mision 2 - Alerta de Churn Estudiantil


La salida es:

- 0 = permanece
- 1 = abandona

Tambien vimos que:

- muchos dias sin login se relacionan con abandono
- poco avance se relaciona con abandono
- el dataset esta desbalanceado

### Modelo propuesto

**Perceptron simple como primera prueba**

### Por que?

Este problema solamente tiene dos posibles salidas.

Por eso primero se podria intentar con un perceptron simple.

Si los datos se pueden separar de forma lineal, podria funcionar.

### Cuando usaria multicapa?

Si el perceptron simple no logra separar bien a los alumnos que abandonan de los que permanecen.

Eso indicaria que las relaciones entre las variables son mas complejas.

### Se puede resolver?

Si.

Pero hay que tomar en cuenta que hay muchos mas alumnos que permanecen que alumnos que abandonan.


## Mision 3 - Pronostico de Puntaje Final


La salida es:

`calificacion_final`

Es un valor numerico entre 0 y 100.

Tambien vimos que:

- `examen_1`
- `examen_2`

tienen una relacion fuerte con la calificacion final.

### Modelo propuesto

**Red neuronal multicapa**

### Por que?

No queremos solamente saber si el alumno aprueba o reprueba.

Queremos obtener un numero.

Por ejemplo:

`calificacion_final = 82`

Las entradas podrian ser:

- promedio de tareas
- examen 1
- examen 2
- asistencia
- horas de estudio

Una red multicapa podria aprender la relacion entre esas variables y la calificacion final.

### Se puede resolver?

Si.

Ademas, el EDA ya muestra que algunas variables tienen relacion clara con la salida.


## Mision 4 - Estimacion de Tiempo de Estudio

La salida es:

`horas_adicionales`

Por ejemplo:

- 2 horas
- 10 horas
- 18 horas
- 35 horas

Tambien vimos que mientras aumenta la dificultad del tema, normalmente aumentan las horas necesarias.

### Modelo propuesto

**Red neuronal multicapa**

### Por que?

Queremos predecir una cantidad de horas.

Las entradas pueden ser:

- `pretest_score`
- `tema_dificultad`
- `videos_vistos`
- `ejercicios_correctos_pct`
- `dispositivo`

El perceptron simple binario no seria suficiente porque la salida no es solamente 0 o 1.

### Se puede resolver?

Si.

El EDA muestra que ya existen patrones entre la dificultad, el rendimiento inicial y las horas necesarias.



# Resumen General

| Problema | Tipo de salida | Modelo 
|---|------------------------|----------- |
| Dino P1 - muerte | Binaria | Multicapa  |
| Dino P2 - score final | Numerica       |     Multicapa                                 |
| Dino P3 - obstaculo | Multiclase        |  Multicapa                                 |
| Frente 1 -riesgo academico | Multiclase | Multicapa                                 |
| Frente 2 - abandono |Binaria|Perceptron simple primero                            |
| Frente 3 - calificacion final | Numerica| Multicapa                                 |
| Frente 4 - horas adicionales | Numerica | Multicapa                                 |



# Conclusion

El EDA que se hizo anteriormente sirve para decidir que modelo tiene mas sentido usar.

No todos los problemas necesitan una red multicapa.

Si tenemos una salida binaria y los datos se pueden separar de forma lineal, un perceptron simple puede ser suficiente.

Si tenemos varias clases, una salida numerica o relaciones mas complicadas entre las variables, una red multicapa puede ser una mejor opcion.

En el caso de Alerta de Churn Estudiantil, primero se podria probar con un perceptron simple porque la salida es binaria.

En los demas problemas, por la forma de la salida o por la cantidad de variables involucradas, una red multicapa parece una opcion mas adecuada.

La idea principal es usar primero lo que encontramos en el EDA y despues justificar por que usamos un perceptron simple o una red multicapa.

# diagramas 
