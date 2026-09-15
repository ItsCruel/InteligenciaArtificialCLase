# Reporte EDA - Operacion Cuatro Frentes


## Mision 1 - Semaforo Academico

### Pregunta de negocio

La escuela quiere saber que nivel de riesgo tiene cada alumno de reprobar:

- verde
- amarillo
- rojo

### Tipo de problema

Yo lo manejaria como **clasificacion multiclase**, porque la variable que queremos obtener es `riesgo` y tiene tres posibles categorias.

### Variable objetivo Y

`riesgo`

### Variables X

- `asistencia_pct`: porque si un alumno falta mucho podria tener mas riesgo.
- `tareas_entregadas`: porque entregar pocas tareas puede afectar su rendimiento.
- `promedio_parciales`: porque muestra como le esta yendo en los examenes.
- `horas_plataforma`: porque puede mostrar cuanto usa el material de la materia.
- `reprobadas_previas`: porque si ya ha reprobado materias antes podria existir mas riesgo.
- `turno`: para revisar si hay diferencias entre matutino y vespertino.

No usaria `alumno_id` como variable para aprender, porque solo sirve para identificar al alumno.

### Hallazgos del EDA

Un patron claro es que los alumnos con riesgo verde tienen una asistencia promedio mas alta.

Por ejemplo:

- verde: 91%
- amarillo: 76%
- rojo: 52%

Tambien pasa algo parecido con el promedio de parciales:

- verde: 8.4
- amarillo: 6.8
- rojo: 5.0

Entonces parece que cuando baja la asistencia y el promedio, aumenta el riesgo.

Tambien se ve que los alumnos con riesgo rojo tienen mas materias reprobadas anteriormente.

### Distribucion de Y

La distribucion es:

- verde: 40%
- amarillo: 35%
- rojo: 25%

No esta totalmente balanceada, pero tampoco hay una clase demasiado pequena.

Aun asi no usaria solamente accuracy.

Tambien revisaria:

- Precision
- Recall
- F1

### Calidad de datos

Un problema podria ser encontrar asistencias mayores a 100%.

Por ejemplo:

`asistencia_pct = 140`

Eso no tendria sentido.

Lo detectaria revisando los valores minimos y maximos.

Si fuera un error, habria que corregirlo o quitar ese registro.

### Data Leakage

No usaria la calificacion final como variable X.

La razon es que queremos saber el riesgo antes de que termine el curso.

Si usamos la calificacion final, estariamos usando informacion que todavia no deberiamos conocer.

Eso seria data leakage.

### Modelo propuesto

Despues del EDA se podria probar un **arbol de decision**.

Antes tendria que revisar que existan suficientes ejemplos de alumnos verdes, amarillos y rojos.



## Mision 2 - Alerta de Churn Estudiantil

### Pregunta de negocio

La universidad quiere saber si un alumno va a abandonar o va a seguir en la materia.

### Tipo de problema

Es un problema de **clasificacion binaria** porque `abandona` solo tiene dos valores:

- 0 = permanece
- 1 = abandona

### Variable objetivo Y

`abandona`

### Variables X

- `dias_sin_login`
- `foros_participados`
- `avance_contenido_pct`
- `calif_actividad_1`
- `beca`
- `trabaja`

### Distribucion de Y

El dataset tiene 500 alumnos.

El 14% abandona.

Entonces:

`500 x 0.14 = 70`

Por lo tanto:

- 430 permanecen
- 70 abandonan

El dataset esta desbalanceado.

Si alguien dijera que su modelo tiene 86% de accuracy, eso no seria suficiente.

Un modelo podria decir siempre "no abandona" y ya tendria 86% de aciertos.

Por eso hay que usar otras metricas.

### Valores faltantes

`calif_actividad_1` tiene valores NA.

Una posibilidad es que el alumno no haya entregado la actividad.

Eso mismo podria ser informacion importante.

Yo podria crear una variable como:

`tiene_calif`

Con valores:

- 1 = tiene calificacion
- 0 = no tiene calificacion

Despues revisaria si conviene llenar el dato faltante con algun valor.

No borraria esas filas directamente.

### Data Leakage

No usaria datos como:

- fecha de baja definitiva
- nota final

Porque esos datos aparecen cuando probablemente ya sabemos que el alumno abandono.

Eso seria usar informacion del futuro.

### Hallazgos EDA

La variable que parece tener mas relacion con abandono es `dias_sin_login`.

Tambien parece que los alumnos con poco `avance_contenido_pct` abandonan mas.

Por ejemplo, varios alumnos que abandonan tienen muchos dias sin entrar y poco avance.

### Metricas

Usaria principalmente:

- Recall
- F1-score

El recall seria importante porque nos interesa detectar a los alumnos que realmente estan en riesgo de abandonar.

### Modelo propuesto

Despues del EDA podria probar:

- regresion logistica
- arbol de decision



## Mision 3 - Pronostico de Puntaje Final

### Pregunta de negocio

Queremos saber que calificacion final va a obtener un alumno entre 0 y 100.

### Tipo de problema

Yo lo considero un problema de **regresion**, porque la variable `calificacion_final` es un numero.

### Variable objetivo Y

`calificacion_final`

### Variables X

- `promedio_tareas`
- `examen_1`
- `examen_2`
- `asistencia_pct`
- `horas_estudio_sem`

### Variable mas relacionada con Y

Segun los datos, `examen_1` y `examen_2` tienen una correlacion aproximada de 0.85 con `calificacion_final`.

Entonces parecen ser las variables mas relacionadas con la calificacion final.

### Que pasa si cambiamos la nota a aprobado/reprobado?

Una ventaja seria que el problema seria mas sencillo.

Solo tendriamos:

- aprobado
- reprobado

Pero perderiamos informacion.

Por ejemplo:

- alumno A = 61
- alumno B = 95

Los dos aparecerian como aprobados, aunque sus calificaciones son muy diferentes.

### Horas de estudio

La media es 5.5 horas.

La mediana es 5 horas.

No hay mucha diferencia entre las dos.

Pero el valor maximo es 25 horas.

Eso podria indicar que hay algunos datos bastante altos.

Habria que revisar si esos alumnos realmente estudian 20 o 25 horas por semana o si fue un error al capturar los datos.

### Calificaciones mayores a 100

Hay tres registros con:

`calificacion_final > 100`

Eso no tiene sentido porque la escala llega hasta 100.

Primero revisaria si fue un error.

Si sabemos cual era el valor correcto, se puede corregir.

Si no se puede saber, podria ser mejor quitar esos registros.

### Metricas

Usaria:

**MAE**

Sirve para saber cuanto se equivoca el modelo en promedio.

Por ejemplo:

`MAE = 4`

Significaria que normalmente el modelo se equivoca alrededor de 4 puntos.

**RMSE**

Tambien mide el error, pero castiga mas cuando el modelo se equivoca por mucho.

### Modelo propuesto

Si al comparar `examen_1` con `calificacion_final` los puntos forman algo parecido a una linea, usaria una **regresion lineal**.

Si los datos se ven mas separados por grupos o por escalones, podria probar un **arbol regresor**.

---

## Mision 4 - Estimacion de Tiempo de Estudio

### Pregunta de negocio

Tutorias quiere saber cuantas horas adicionales necesita un alumno para dominar un tema.

### Tipo de problema

Yo lo manejaria como **regresion**, porque `horas_adicionales` es un numero.

### Variable objetivo Y

`horas_adicionales`

### Variables X

- `pretest_score`
- `tema_dificultad`
- `videos_vistos`
- `ejercicios_correctos_pct`
- `dispositivo`

### Hipotesis EDA

Las medias son:

- dificultad baja: 3.2 horas
- dificultad media: 7.8 horas
- dificultad alta: 16.5 horas

Entonces mi idea seria:

**Entre mas dificil sea el tema, mas horas adicionales necesita el alumno.**

### Variables categoricas

Para `tema_dificultad` revisaria cuantos casos hay de:

- baja
- media
- alta

Para `dispositivo` revisaria:

- pc
- movil
- tablet

Tambien compararia cuantas horas adicionales necesita cada grupo.

### Outliers

El 3% necesita mas de 40 horas.

Yo no los borraria directamente.

Primero revisaria si son errores o si son casos reales.

Por ejemplo, puede existir un alumno que saco muy poco en el pretest y aparte esta estudiando un tema dificil.

En ese caso si podria necesitar muchas horas.

Si el dato es real, no conviene borrarlo.

### Posible redundancia

`pretest_score` y `ejercicios_correctos_pct` podrian estar diciendo algo parecido.

Para revisarlo podria ver la correlacion entre las dos variables.

Si casi siempre suben y bajan juntas, puede haber informacion repetida.

### Convertir Y a tutoria intensiva si/no

Tambien se podria cambiar el problema a:

- menos de 15 horas = no necesita tutoria intensiva
- 15 horas o mas = si necesita tutoria intensiva

Eso serviria si la escuela solo quiere decidir quien necesita apoyo extra.

Pero perderiamos informacion.

Ya no sabriamos si un alumno necesita:

- 16 horas
- 25 horas
- 40 horas

Solo sabriamos si necesita tutoria intensiva o no.

### Metricas

Usaria:

- MAE
- RMSE

Porque estamos tratando de predecir una cantidad de horas.

### Modelo propuesto

Despues del EDA podria comenzar con una **regresion lineal**.

Antes de entrenar revisaria dos cosas:

1. si existen outliers en `horas_adicionales`
2. si algunas variables estan dando informacion muy parecida



# Sintesis

| Mision | Tipo de problema | Variable Y |
|---|---|---|
| Semaforo academico | Clasificacion multiclase | riesgo |
| Churn estudiantil | Clasificacion binaria | abandona |
| Puntaje final | Regresion | calificacion_final |
| Tiempo de estudio | Regresion | horas_adicionales |

conclusion

La forma mas facil que use para decidir el tipo de problema fue ver la variable Y.

Si Y tiene categorias, normalmente es clasificacion.

Si Y es un numero que queremos calcular, normalmente es regresion.

Por eso primero hay que saber que queremos obtener, luego hacer el EDA y al final pensar que modelo podria servir.