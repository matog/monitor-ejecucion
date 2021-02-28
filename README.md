# Dashboard de la ejecución presupuestaria de un SAF de la APN

Esta app tiene como objetivo generar un dashboard para analizar la ejecución presupuestaria de un SAF (sistema adminsitravio financiero) de un organismo de la APN (Administración Pública Nacional) de Argentina

Está desarrollado 100% en python, utilizando el framework _Dash_, con un diseño _responsive_, para poder ser accesible de un dispositivo móvil,. 

Una versión demo está alojada en [Heroku](https://monitor-ejecucion.herokuapp.com/)

## Requisitos

### Paquetes
Los requisitos en términos de paquetes se encuentran en el archivo _requirements.txt_.

### Información presupuestaria
Para que la app tenga un funcionamiento correcto, es necesario tener un tabla "base.csv" ubicada en el directorio de la app, donde se tenga la ejecución mensual a nivel programa-inciso.

Esta información está disponible en [Presupuesto Abierto](https://www.presupuestoabierto.gob.ar/sici/datos-abiertos#). Por ejemplo, para ver la ejecución del ejercicio 2020, seleccionamos el "Año:2020", en Temas elegimos "Presupuesto de gastos y su ejecución" y en "Resultados encontrados" descargamos "Presupuesto de gastos y su ejecución detallada - agrupación mensual 2020"  
![image](https://user-images.githubusercontent.com/660448/109428493-165ba880-79d6-11eb-8a6e-7a4bb7358eda.png)

#### Seleccionar SAF

El archivo _saf_selector.ipynb_ es una notebook que al correrla en el mismo directorio que la base.csv, arroja un cuadro con el total de crédito vigente por SAF.

En la misma nota, está indicado donde cambiar el SAF para exportar una nueva base para poder correrla en el dashboard.

### Screenshot

![image](https://user-images.githubusercontent.com/660448/109428624-9aae2b80-79d6-11eb-9483-8a5ebb980af5.png)
