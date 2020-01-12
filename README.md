# Wallet-Platform

En este documento me dispongo a explicar ciertos detalles de la implementación del código 

## Planteamiento

Antes de ponerme a picar código realicé una fase de análisis. Lo primero que hice fue leer unas cuantas veces el problema y de aquí obtuve el primer documento que está en la carpeta doc: el análisis de requisitos.
Mi segundo paso fue establecer los cimientos de la aplicación de una forma inicial, es decir, el modelo de datos. De esta forma, desde el principio podría tener de un vistazo una imagen de como conectan todos los conceptos dentro de la aplicación.
Finalmente definí los endpoints que el proyecto requería en el documento de definición de la API REST.

## Docker-Compose

He utilizado Docker Compose para realizar el proyecto y así desplegar varios servicios de forma fácil.

Antes de usar el docker-compose en local se necesitarán inicializar varias variables de entorno:

```export WEB_ENVIRONMENT='LOCAL'
export DJANGO_SETTINGS_MODULE='event_platform.settings.local'
export SECRET_KEY='eHv60Lp4t&HM7NKwuAaUx%C30nUUtgbE)FOi4u0A7dw'
export DATABASE_NAME='postgres'
export DATABASE_USER='postgres'
export DATABASE_PASSWORD=''
export DATABASE_HOST='db'
```

Para usarlo tenemos un archivo Makefile con varios comandos, comentaré los más necesarios.

- make up: inicializa la aplicación levantando todo lo necesario y haciendo el build y coloca en http://localhost el desarrollo.
- make up-non-daemon: lo mismo que `make up` pero mostrando por pantalla el log.
- make run-tests: Corre la batería de tests completa realizada para esta aplicación.

En producción lo tenemos ya todo preparado para acceder a la ip y que este funcionando en el puerto 80.

## Modelo de datos

Al plantear el modelo de datos, por una parte, los usuarios los divido en dos: Customers y Commerces. Al final los dos van a tener Wallets, la diferencia es que el Commerce solo tendrá una y los Customers pueden tener varias, pero el funcionamiento general de la Wallet es el mismo, por esta razón los dos tipos de Wallet hereden de un Wallet general. Para las Operations habría realizado una relación de herencia entre Operations y operaciones de entrada de dinero and operaciones de salida de dinero pero al ser una prueba y ya haber hecho otras dos relaciones de herencia no le quería meter más complejidad, pero me parecería más adecuado para poder escalar mejor en el futuro.

## Detalles

 - Los token que se han utilizado para identificar inequívocamente los elementos del modelo de datos son los uuid.
 - He supuesto que cualquier User puede cargar un Wallet aunque no sea suyo, de esta forma los comercios con esta misma petición podrían incluso hacer una devolución o se podría utilizar tipo bizum, para pasar dinero entre Customers. Aunque para que esto fuera más correcto se deberían generar otros endpoints y deberían ser otro tipo de operación.
 - No testeo `get_operation_by_wallet_uuid` porque implicitamente está testado con los tests de integración en este momento.
 - Para asegurarme que las transacciones sean atómicas he utilizado el decorador `transaction.atomic` sobre el sevice que realiza la transacción.

1.​ Desplegar el proyecto en la instancia proporcionada.

Lo he dejado desplegado en la instancia con el docker compose, mi idea era haberlo automatizado con github actions, pero nunca lo había hecho, ni me ha dado tiempo.
Tengo experiencia automatizando despliegues con Bitbucket Pipelines, podría mostrároslo, y ya hace unos años, en la empresa donde trabajaba antes lo teníamos con Jenkins.

2.​ Indica cómo se puede optimizar el rendimiento del servicio de listado de operaciones.

Cachearía las operaciones en Memcached o en Redis, posiblemente directamente los JSON y cuando hubiera una nueva o invalidaría la caché o lo incluiría en lo ya cacheado.
También se me puede ocurrir utilizar alguna herramienta tipo ElasticSearch para realizar las búsquedas más rápidas.

3​ . ¿Qué alternativas planteas en el caso que la base de datos relacional de la aplicación se convierta en un cuello de botella por saturación en las operaciones de lectura? ¿Y para las de escritura?

Caching, caching, caching. Para los temas de lectura cachearía todo lo que pudiese en memcached o Redis como expliqué en la pregunta anterior para los JSON, pero después los típicos cálculos que requiran lógica los mantendría cacheados y los iría actualizando cuando fuese necesario. En este caso, en ApetEat desarrolle dos capas de caché con estas dos teorías que acabo de describir y que me resultan interesantes y me gustaría poder explicároslo. La caché es la mejor amiga del desarrollador backend :)
Otra opción es montar una solución marter-slave en la capa de datos para de esta forma guardarnos las espaldas y que si hay un cuello de botella se pueda recurrir a la otra.
Otra opción más radical, que solucionaría los os problemas (lectura y escritura) sería partir la base de datos por zonas y que cada zona ataque a su db, de esta forma no se sobrecargaría una misma db. Y después si se quisiera trabajar sobre todos los datos se podría hacer sharding.

4​ . Dicen que las bases de datos relacionales no escalan bien, se me ocurre montar el proyecto con alguna NoSQL, ¿qué me recomiendas?

La verdad es que nunca me he enfrentado a un problema en el que haya que utilizar una NoSQL en vez de una SQL. Si me tuviera que meter a recomendar algo necesitaría analizar tu problema para saber que solución aplica mejor, ya que hay diferentes tipos de db NoSQL: orientada a documentos (mongoDB), grafos (Neo4j)...
De hecho, hasta Redis es una db NoSQL.

5.​ ¿Qué tipo de métricas y servicios nos pueden ayudar a comprobar que la API y el servidor funcionan correctamente?

Yo he trabajado con diferentes herramientas de monitoriación de servidores y detección de errores que nos hacen la vida mucho más fácil a los desarrolladores: Data Dog, Cloudwatch, Sentry...