# MercadoPago Value Props Prediction Pipeline

## Introducción

Este proyecto aborda la construcción de una ETL robusta, diseñada para organizar y estructurar datos que eventualmente alimentarán un modelo de Machine Learning. La elección de un procesamiento por lotes se alinea con la necesidad de procesar grandes volúmenes de información histórica de las interacciones de los usuarios con las Propuestas de Valor en MercadoPago.

## Características Principales del Proyecto

- **CI Pipeline para Chequeo de Código Estático:** Utilizamos una pipeline de CI que emplea herramientas de análisis estático como Flake8, isort, y Black para mantener el código limpio y bien estructurado.

- **Precommit para Contribuciones Consistentes:** Para facilitar las contribuciones y mantener la calidad del código, se implementaron hooks de precommit que automatizan la verificación de estilo y calidad antes de cada commit.

- **Monitor de Drift en los Datos de Entrada:** Un sistema integrado para monitorear cualquier desviación en los datos de entrada, permitiendo ajustes proactivos para mantener la precisión del modelo.

- **Validador de Contratos de Datos en la Entrada:** Implementación de validaciones de contrato para asegurar que los datos ingresados sigan el esquema y se encuentren de el rango correctos.

- **Logger Centralizado y Extensible:** Un sistema de logging diseñado para ser intuitivo y expansible.

- **ETL Robusta:** Una ETL construida para procesar grandes cantidades de datos de forma eficiente, con mecanismos de manejo de errores para asegurar su fiabilidad y disponibilidad continua.

Estas características componen la columna vertebral de un proyecto diseñado no solo para el rendimiento a corto plazo, sino también para la adaptabilidad y facilidad de mantenimiento a largo plazo.

## Racionalización del Procesamiento por Lotes

La decisión de adoptar el procesamiento por lotes se justifica por:

- **Volumen de Datos:** La capacidad de procesar y manejar grandes conjuntos de datos acumulativos de manera eficiente.
- **Actualizaciones Periódicas:** La naturaleza de los datos no requiere actualizaciones en tiempo real, lo que permite un procesamiento programado y optimizado.
- **Eficiencia de Recursos:** Mejor utilización de los recursos, concentrando el procesamiento de datos durante periodos de menor demanda operativa.

## Comparación con Otros Paradigmas

La etapa ETL del proyecto se compara con otros paradigmas de la siguiente manera:

- **Procesamiento en Tiempo Real:** Aunque ofrece la ventaja de la inmediatez, en nuestro caso, no proporciona beneficios significativos debido a que los patrones y tendencias se evalúan sobre periodos más largos y no requieren acciones instantáneas.
- **Procesamiento Basado en Eventos:** Este paradigma se centra en reaccionar ante eventos específicos cuando ocurren. Para el propósito de construir un dataset estructurado, la naturaleza continua de los datos hace que este enfoque sea menos eficiente y más costoso que el procesamiento por lotes.
- **Procesamiento Federado:** La federación de datos es útil cuando los datos deben permanecer en sus sistemas nativos por razones de privacidad o logística. Sin embargo, nuestro proyecto beneficia de la centralización de datos para el análisis histórico y la construcción de un dataset unificado.
- **Procesamiento Paralelo:** Aunque el procesamiento paralelo se puede aplicar dentro de una estrategia de procesamiento por lotes para acelerar las operaciones, no define nuestra estrategia de procesamiento principal. La paralelización se utilizará como una táctica dentro del procesamiento por lotes más amplio para manejar grandes volúmenes de datos de manera eficiente.

En conclusión, el procesamiento por lotes es la estrategia más alineada con los objetivos de esta etapa del proyecto, que se centra en la construcción y preparación de datos para análisis futuros.

## Perspectivas del Modelo

El modelo se puede enfocar en comprender y predecir la interacción del usuario con el carrusel de Propuestas de Valor. Las features disponibles permitirán explorar diversas aproximaciones al modelado del problema, tales como:

- **Modelos Basados en Clasificación:** Identificar si un usuario hará clic en una propuesta en función de sus acciones pasadas.
- **Modelos de Regresión:** Predecir la cantidad de interacción o el valor de los pagos de un usuario para una Propuesta de Valor específica.
- **Modelos de Series Temporales:** Examinar tendencias a lo largo del tiempo para prever la popularidad de las Propuestas de Valor.
