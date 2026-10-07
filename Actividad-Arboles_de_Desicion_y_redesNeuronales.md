# Actividad - Arbol de Decision y Red Neuronal Multicapa

# Parte I. Conceptos y definiciones
## Pregunta 1
### ¿Que es un arbol de decision y cual es su objetivo?

Un arbol de decision es un modelo que toma decisiones haciendo preguntas sobre los datos y siguiendo diferentes caminos hasta llegar a una respuesta.
Su objetivo principal en clasificacion es separar los datos en diferentes grupos o clases, por ejemplo, para saber si un alumno tiene riesgo de reprobar, el arbol podria preguntar primero por la asistencia, despues por el promedio y asi seguir hasta llegar a una clase como:
- Riesgo bajo
- Riesgo medio
- Riesgo alto

## Pregunta 2
### Nodo raiz
Es el primer nodo del arbol y es donde empieza la decision y normalmente contiene la variable que el modelo considera mas importante para hacer la primera separacion.
### Nodo interno
Es un nodo que hace otra pregunta o division sobre los datos.
Por ejemplo:
`¿La asistencia es menor a 70%?`
### Rama
Es el camino que se sigue dependiendo de la respuesta de una pregunta.
Por ejemplo:
`Si asistencia < 70%`
o
`Si asistencia >= 70%`
### Hoja
Es el punto final del arbol.Aqui ya se da la respuesta o clase que predice el modelo.
Por ejemplo:
`Riesgo alto`

## Pregunta 3
### ¿Que es una red neuronal multicapa?
Una red neuronal multicapa es una red que tiene varias capas de neuronas y que puede aprender relaciones mas complejas que un perceptron simple. Las principales capas son:

### Capa de entrada
Es donde entran las variables del problema.
Por ejemplo, para un alumno:
- asistencia
- calificaciones
- tareas
- participacion

### Capa oculta

Es donde la red combina las entradas usando pesos, bias y funciones de activacion. Puede haber una o varias capas ocultas , esta parte ayuda a encontrar relaciones entre los datos.

### Capa de salida
Es donde la red entrega el resultado final.
Por ejemplo:
`0 = no abandona`
`1 = abandona`
o varias salidas si tenemos varias clases.

## Pregunta 4
### ¿Que representan los pesos y los sesgos?
Los pesos representan que tanto influye cada entrada en una neurona.
Por ejemplo, una variable puede tener un peso alto porque tiene mucha influencia en el resultado.
El sesgo o bias es un valor adicional que se suma a la entrada de la neurona y ayuda a ajustar la salida.
Los pesos y los sesgos cambian durante el entrenamiento porque la red compara su resultado con el resultado correcto y trata de reducir el error
Con cada ejemplo puede modificar sus pesos para obtener una mejor respuesta.

## Pregunta 5
### Diferencia entre como aprende un arbol y una red neuronal
Un arbol de decision aprende buscando divisiones de los datos.
Por ejemplo:
`¿Asistencia < 70?`
`¿Promedio < 6?`

Y con esas divisiones va formando ramas hasta llegar a una decision.
En cambio, una red neuronal aprende ajustando los pesos y los bias de sus neuronas.
La red hace una prediccion, calcula el error y despues modifica sus pesos para intentar reducir ese error.

Entonces:
**Arbol de decision:**
Aprende reglas y divisiones de los datos.

**Red neuronal:**
Aprende pesos y bias para encontrar relaciones entre las variables.


# Parte II. Analisis y aplicacion

## Pregunta 6
### Deteccion de compras fraudulentas
 Una institución bancaria desea desarrollar un sistema que detecte posibles compras fraudulentas.

El sistema dispone de información como:

    Monto de la compra
    Hora de la operación
    Ciudad donde se realizó
    Tipo de establecimiento
    Número de compras realizadas durante el día
    Historial de compras del cliente
Analice las ventajas y desventajas de utilizar un árbol de decisión y una red neuronal multicapa.

¿Cuál utilizaría y por qué?:
Yo consideraria Arbol de decision

### Arbol de decision
#### Ventajas
- Es facil de entender
- Se pueden ver las reglas que usa para tomar la decision
- Es mas sencillo explicar por que una compra fue marcada como fraude
- Puede ser util si el banco necesita explicar sus decisiones
#### Desventajas
- Puede crecer demasiado y volverse complicadp
- Puede aprender demasiado los datos de entrenamiento
- Si las relaciones entre las variables son muy complicadas, puede no funcionar tan bien

Yo empezaria con un arbol de decision como primera opcion si el objetivo es tener un modelo que se pueda explicar facilmente , si tenemos muchos datos y el arbol no tiene suficiente precision, probaria una red neuronal.


# Pregunta 7
### Riesgo de reprobar en una escuela
Si los dos modelos tienen practicamente la misma precision, no elegiria solamente por precision.

Tambien tomaria en cuenta:
- Que tan facil es explicar el modelo.
- Cuantos datos necesita.
- Que tan rapido funciona.
- Que tan facil es actualizarlo.
- Que tan facil es detectar errores.
- Que tan importante es entender por que tomo una decision.

En este caso probablemente elegiria el **arbol de decision** si las dos opciones tienen resultados parecidos,  la razon es que un maestro o directivo puede entender reglas como: `Si asistencia < 70% y promedio < 6 entonces riesgo alto.` Con una red neuronal seria mas dificil explicar exactamente por que el alumno fue clasificado de esa manera.


# Pregunta 8
### Sistema hospitalario
No creo que una mayor precision sea suficiente para elegir la red neuronal. En un hospital una decision puede tener consecuencias importantes.Ya que  si el modelo se equivoca y clasifica a un paciente grave como paciente de baja prioridad, podria retrasarse su atencion. La red neuronal puede tener mayor precision, pero si es muy dificil explicar su decision tambien existe un problema. Un arbol de decision podria ser menos preciso pero mas facil de revisar y explicar.

En este caso yo compararia:
- Precision.
- Recall.
- Cantidad de falsos negativos.
- Cantidad de falsos positivos.
- Facilidad para explicar la decision.
- Consecuencias de cometer un error.

Para un hospital me enfocaria especialmente por los casos en los que el modelo no detecta a un paciente que realmente necesita atencion urgente.
Por eso no elegiria a la red neuronal solo porque tenga mayor precision.

# Pregunta 9
### Pedido que puede llegar tarde
Tenemos dos modelos:

**Arbol:**
`Llegara a tiempo`

**Red neuronal:**
`Probablemente llegara tarde`

No podria decir cual tiene razon solamente viendo este pedido.
Primero necesitaria conocer el resultado real.

Por ejemplo: `Resultado real = llego tarde` Entonces la red neuronal habria acertado. Pero si: `Resultado real = llego a tiempo` , entonces el arbol habria acertado. Tambien se puede revisar el comportamiento general de los modelos con un conjunto de datos de prueba y  tambien revisaria en que tipo de pedidos se equivoca cada modelo. No basta con saber que uno acerto este caso. Hay que revisar como funcionan los dos modelos en muchos casos.


# Pregunta 10
### Sistema para decidir si una persona recibe credito
En este caso yo elegiria dependiendo de lo que sea mas importante para la empresa. El arbol de decision tiene como ventaja principal que es mas facil de explicar , Por ejemplo, se puede mostrar algo como: `Ingresos bajos -> historial negativo -> credito rechazado` Esto permite explicar la decision al cliente.
La red neuronal tiene la ventaja de que puede obtener mejores resultados de prediccion si tiene suficientes datos y encuentra relaciones que el arbol no encuentra facilmente.

### ¿Cual utilizaria?
Yo probablemente empezaria con el **arbol de decision** si la diferencia de precision no es demasiado grande.
La razon es que en un credito es importante poder explicar por que se rechazo una solicitud.

### Ventajas de elegir el arbol
- Es mas facil de interpretar.
- Es mas facil detectar errores.
- Es mas facil explicar las decisiones.
- Puede ayudar a generar reglas de negocio.

### Riesgos
El arbol puede ser menos preciso.
Tambien puede crecer demasiado y aprender demasiado los datos de entrenamiento.

### ¿Y si la red neuronal es mucho mas precisa?
En ese caso consideraria usar la red neuronal, pero buscaria alguna forma de revisar y explicar mejor sus resultados.
Tambien compararia los errores de los dos modelos y no solamente su precision general.

### ¿Se pueden utilizar los dos?
Si. Podrian utilizarse los dos dentro del mismo sistema , por ejemplo, la red neuronal podria utilizarse para hacer la prediccion principal y el arbol podria servir como una segunda revision o como apoyo para explicar algunos casos.

## A partir de los ejercicios anteriores, explique brevemente la siguiente afirmacion:
> "No existe un algoritmo de Inteligencia Artificial que sea el mejor para todos los problemas."

Esta afirmacion es verdadera porque cada problema tiene diferentes datos, objetivos y consecuencias. Un modelo puede funcionar muy bien en un problema y no ser la mejor opcion en otro. Por ejemplo, un arbol de decision puede ser una buena opcion cuando necesitamos que las decisiones sean faciles de entender y explicar. Una red neuronal multicapa puede ser una mejor opcion cuando el problema es mas complejo y existen relaciones mas dificiles de encontrar entre las variables. Tambien se debe tomar en cuenta la **precision**, ya que un modelo puede tener mejores resultados que otro. Sin embargo, la precision no es lo unico importante. Tambien importa la **interpretabilidad**, es decir, que tan facil es entender por que el modelo tomo una decision. La **cantidad de datos** tambien puede influir en la eleccion, ya que algunos modelos pueden necesitar mas datos para aprender correctamente. Ademas, la **complejidad del problema** puede hacer que un modelo sencillo no sea suficiente y sea necesario utilizar uno con mayor capacidad.
Por ultimo, se deben considerar las **consecuencias de una decision incorrecta**. Por ejemplo, equivocarse al recomendar una pelicula no tiene la misma importancia que equivocarse al detectar un paciente que necesita atencion prioritaria o al decidir si una persona puede recibir un credito.

Por estas razones, no existe un unico algoritmo que sea el mejor para todos los problemas. La eleccion depende de los datos, del problema que queremos resolver, de la precision que necesitamos, de que tan importante sea poder explicar las decisiones y de las consecuencias que pueda tener un error.