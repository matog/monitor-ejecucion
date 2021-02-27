# Dashboard de la ejecución presupuestaria de un SAF de la APN

Esta app tiene como objetivo generar un dashboard para analizar la ejecución presupuestaria de un SAF (sistema adminsitravio financiero) de un organismo de la APN (Administración Pública Nacional) de Argentina

Está programada 100% en python, utilizando el framework _Dash_. Está desarrollada con un diseño _responsive_, para poder ser accesible de un dispositivo móvil,. 

Los requisitos para la correcta visualización de la información es tener un tabla "Base_mes.xlsx", donde se tenga la ejecución mensual a nivel programa-inciso, con los siguientes campos:

- 'yyyymm': Fecha de registro en formato _yyyymm_.
- 'credito_inicial': Crédito presupuestario inicial.
- 'credito_vigente': Crédito presupuestario vigente.
- 'credito_devengado': Crédito presupuestario devengado.
- 'actualizacion': Fecha de ultima actualización de la base.
- 'programa_id': Id del programa presupuestario.
- 'programa_desc'': Descripción del programa presupuestario.
- 'inciso_id': Id del inciso
- 'fuente_de_financiamiento_desc': Descripción de la fuente de financiamiento.

Esta información está disponible en [Presupuesto Abierto](https://www.presupuestoabierto.gob.ar/sici/datos-abiertos#)



![image](https://user-images.githubusercontent.com/660448/109393371-fe195a00-78ff-11eb-8e37-bbbe6d824828.png)
