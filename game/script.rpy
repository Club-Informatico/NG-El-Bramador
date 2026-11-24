## ============================================================================
##  EL BRAMADOR · Una leyenda de Copiapó
##  Guion principal (cuatro finales)
## ============================================================================

label start:
    scene negro
    stop music

    menu:
        "{b}Antes de empezar: ¿cómo quieres escuchar el cerro?{/b}\nEl bramido es un sonido muy grave. Con audífonos o a volumen alto puede cansar."

        "Bramido completo, como suena el cerro de verdad.":
            $ persistent.bramido_suave = False

        "Bramido suave (recomendado con audífonos).":
            $ persistent.bramido_suave = True

    centered "Puedes cambiarlo en cualquier momento con la tecla {b}B{/b}." with dissolve

    play ambiente viento fadein 3.0
    pause 1.0
    show cg titulo with fundido_muy_lento
    play cerro cerro_snd("bramido_lejano")
    pause 4.0
    scene negro with fundido_lento
    jump prologo


## ----------------------------------------------------------------------------
##  PRÓLOGO · Lo que dicen en Copiapó
## ----------------------------------------------------------------------------

label prologo:
    scene bg cerro_noche with fundido_muy_lento
    play music tension fadein 4.0

    nvl clear
    leyenda "Dicen en Copiapó que el Cerro Bramador tiene oro adentro."
    leyenda "No una veta: una ciudad entera de oro macizo, con calles, campanarios y puertas que nadie ha abierto dos veces."
    leyenda "Dicen que el dueño de ese oro es el Diablo. El Coludo. Mandinga. El Caballero. Tiene muchos nombres, porque nadie quiere decir el verdadero."
    nvl clear
    leyenda "Dicen que el oro se puede sacar. Pero se paga: con el alma de un compañero o de alguien que uno quiera."
    leyenda "Y dicen que el que lo saca sin pagar no vuelve a dormir en paz. Que el cerro se le cierra encima, o que el Caballero lo sigue hasta que se le va el juicio."
    leyenda "Por eso, cuando un minero bajaba solo del Bramador y amanecía rico, en Copiapó se murmuraba una sola cosa:"
    leyenda "{i}«Ese entregó a alguien.»{/i}"
    nvl clear

    play cerro cerro_snd("bramido")
    show bg cerro_noche at temblor_cerro

    leyenda "Y el cerro, cuando la arena se desliza por sus faldas, brama."
    leyenda "Los arrieros dicen que es el Diablo gruñendo para espantar a los intrusos. Las viejas dicen que son las almas que se quedaron adentro."
    leyenda "Hace unos años pasó por Copiapó un naturalista inglés, de esos que andan juntando piedras y bichos. Le contaron del cerro y dijo que era la arena nomás, los granos frotándose unos con otros."
    leyenda "Puede ser."
    leyenda "Pero el inglés nunca subió."
    nvl clear

    stop music fadeout 3.0
    scene negro with fundido_lento
    centered "{size=+10}Copiapó{/size}\n\nInvierno de 1839" with dissolve
    jump chingana


## ----------------------------------------------------------------------------
##  CAPÍTULO 1 · La chingana
## ----------------------------------------------------------------------------

label chingana:
    scene bg chingana with fade
    stop ambiente fadeout 2.0
    play music cueca fadein 2.0

    "Me llamo Matías Ardiles. Tengo veintiséis años, una mujer que se merece algo mejor que yo y una deuda de ciento veinte pesos con don Fermín Cisternas."
    "Hace siete años encontraron plata en Chañarcillo, y desde entonces medio Chile vino a Copiapó a hacerse rico. Algunos lo consiguieron. Los demás nos quedamos en la chingana."
    "Mi pique se agotó en marzo. La veta se cortó de un día para otro, limpia, como si alguien la hubiera cortado con tijeras."

    show celestino neutral with dissolve

    "Celestino Aracena tiene cuarenta y tantos años y ha cateado todo el despoblado, de la cordillera al mar. Fue el que me enseñó a leer la piedra. También me enseñó a perder plata en las carreras de caballos."

    c "Matías, mijo. Te traigo el remedio para todas tus penas."
    m "La última vez que me dijo eso pasamos tres días sin agua en el despoblado."

    show celestino risa

    c "¡Y volvimos! ¿O no volvimos? Mira esto."

    show cg derrotero with dissolve

    "Es un papel amarillo, blando de tanto doblarlo, con un dibujo hecho a pluma: un cerro, una quebrada, una cruz. Y unas líneas de letra torcida."

    nvl clear
    papel "Del Bramador, la falda que mira al poniente."
    papel "Donde la arena no canta, ahí está la puerta."
    papel "Entrar con la luna nueva. No decir el nombre. No recibir nada."
    nvl clear

    hide cg derrotero with dissolve
    show celestino neutral

    c "Un derrotero. Se lo compré a la viuda de un arriero de Toledo: dos reales y una gallina."
    m "Celestino. Es el Bramador. Usted sabe lo que dicen."
    c "Dicen muchas cosas, mijo. También decían que en Chañarcillo no había nada, y mira cómo anda Copiapó."

    stop music fadeout 1.5

    "Entonces la guitarra se calla."
    "En la puerta de la chingana hay un hombre parado. Nadie sabe su edad. Tiene la barba larga y llena de tierra, y cuando le da la luz de la vela, brilla como si la tuviera espolvoreada de oro."

    show celestino neutral at right with move
    show ulises neutral at left with dissolve

    "El Loco Ulises."

    u "¿Quién dijo Bramador?"

    "Nadie contesta. El dueño de la chingana ya viene saliendo de detrás del mesón, con cara de echarlo a la calle."

    menu:
        "Invitarlo a la mesa y escucharlo.":
            $ escucho_ulises = True
            "Me paro antes de que llegue el dueño y le acerco un banco."
            m "Siéntese, don Ulises. ¿Le traigo algo?"
            u "Agua. Agua nomás. El aguardiente se me hace oro en la boca."
            "Se toma el jarro entero sin respirar. Después nos mira, primero a Celestino, después a mí. Tiene los ojos de un niño que se perdió en una feria."
            u "Éramos dos. Dos socios. Fermín y Ulises. Ulises y Fermín."
            u "Subimos con la luna nueva, como dice el papel. Y abajo estaba él, esperando, bien vestido."
            u "Fermín le dijo mi nombre. Mi nombre completo, como en el bautizo: Ulises Rojas Campillay."
            u "Y el Caballero me sacó lo de adentro con dos dedos. Así. Como quien saca una moneda de un bolsillo."
            "Junta el índice y el pulgar delante de mi cara. Le tiemblan."
            u "El cerro tiene mi alma en la garganta. Por eso brama."
            u "No le reciban nada. Ni agua, ni fuego, ni un trago. El que recibe, debe."
            "Se levanta y se va sin despedirse, arrastrando los pies."
            "Fermín."
            "Hay un solo Fermín en Copiapó que pasó de pobre a rico de un día para otro. Hace diez años."
            "Y yo le debo ciento veinte pesos."

        "Dejar que el dueño lo eche.":
            "No me muevo. El dueño lo agarra del brazo y lo saca a la calle sin mucho esfuerzo; pesa lo que pesa un poncho vacío."
            u "¡El cerro tiene hambre! ¡Hambre! ¡Y ustedes van a ir a darle de comer!"
            "La puerta se cierra. Alguien se ríe. La guitarra vuelve a sonar, pero más bajito."

    hide ulises with dissolve
    show celestino neutral at center with move
    play music cueca fadein 2.0

    c "Pobre diablo."
    c "Mañana vamos donde don Fermín. Necesitamos un habilitador que ponga las mulas y los víveres. Y tú le debes plata: mejor ir de socio que de deudor."

    "Esa noche no duermo. A lo lejos, hacia el poniente, el viento trae un ruido grave que podría ser un carretón en la quebrada."

    play cerro cerro_snd("bramido_lejano")

    "O podría no serlo."

    stop music fadeout 3.0
    jump oficina


## ----------------------------------------------------------------------------
##  CAPÍTULO 2 · El habilitador
## ----------------------------------------------------------------------------

label oficina:
    scene bg oficina with fade
    play ambiente viento fadein 2.0

    "La casa de don Fermín Cisternas es la única de la calle con ventanas de vidrio. Adentro huele a tabaco, a cera y a algo dulzón que no reconozco."
    "En el escritorio hay una balanza de cobre, un tintero de plata y un libro de cuentas tan gordo como un misal."

    show fermin neutral with dissolve

    "Don Fermín tiene sesenta años, patillas grises y un anillo de oro en cada mano. Sonríe con la boca. Con los ojos, cuenta."

    f "Matías Ardiles. Ciento veinte pesos, más los intereses de agosto."
    m "Vengo a proponerle un negocio, don Fermín."

    "Celestino le muestra el derrotero. Don Fermín no se sorprende. Lo mira como quien mira una carta que ya leyó."

    f "El Bramador. Hay derroteros de ese cerro desde el tiempo de los españoles. Casi todos son mentira."
    f "Casi todos."

    show fermin sonrisa

    f "Les propongo esto: yo pongo dos mulas, víveres para una semana, barretas y pólvora. Le perdono la deuda, Ardiles. Y de lo que traigan, un tercio para cada uno."
    c "Muy generoso, patrón."
    f "Con una condición: que firmen como socios de mi compañía. Todo en regla, ante escribano."

    "Saca un pliego de un cajón. Ya está escrito. Con nuestros nombres."
    "Celestino firma primero, con una cruz grande y contenta."

    show fermin neutral

    menu:
        "Leer el contrato completo antes de firmar.":
            $ contrato = True
            "Mi madre me enseñó a leer con el catecismo, y desde entonces leo todo lo que me ponen delante. Don Fermín tamborilea los dedos sobre la mesa."

            show cg contrato with dissolve

            "Compañía minera {i}La Fortuna del Poniente{/i}. Socios: don Fermín Cisternas, Matías Ardiles, Celestino Aracena."
            "Las cláusulas de siempre: el reparto, los plazos, las multas. Y la cuarta:"
            "{i}Cuarta. Cada socio responde ante las deudas de la compañía con lo suyo y con los suyos.{/i}"
            "Con los suyos."

            hide cg contrato with dissolve

            m "¿Qué quiere decir «con los suyos», don Fermín?"
            f "Fórmula de escribano, mijo. Así se escriben estas cosas desde Felipe Segundo."
            m "Entonces no le importará darme una copia."

            "Por un segundo, don Fermín deja de sonreír. Después sonríe más."

            f "Por supuesto. Un socio tiene derecho a sus papeles."

            "Firmo. Doblo mi copia en cuatro y la guardo en el forro del poncho, junto al pecho."

        "Firmar sin leer: Celestino ya firmó.":
            "Celestino ya firmó, y Celestino lleva veinte años en esto. Firmo debajo de su cruz."
            "Don Fermín sopla la tinta y guarda el pliego en el cajón, con llave."

    if escucho_ulises:
        "Antes de irme, me acuerdo de los dedos temblorosos del Loco."
        m "Don Fermín. ¿Usted conoció a Ulises Rojas?"

        show fermin neutral

        "La pluma se le queda quieta en el aire."

        f "Fue mi socio, hace mucho. Se le fue la cabeza en el desierto, pobre hombre. Le pago la comida en la chingana, por caridad."
        f "Cosas que pasan en el despoblado, Ardiles. Por eso hay que ir bien acompañado."

    show fermin sonrisa

    f "Salgan pasado mañana, con la luna nueva. Y usted, Aracena, cuídeme al muchacho."

    "Lo dice mirando a Celestino. Celestino se ríe. Yo no."

    hide fermin with dissolve
    stop ambiente fadeout 2.0
    jump rancho


label rancho:
    scene bg rancho with fade
    play music tema fadein 3.0

    "Rosario está sentada junto al brasero, remendando una camisa que no es mía. Lava ropa ajena para las señoras de la calle Atacama desde que se secó el pique."

    show rosario neutral with dissolve

    ro "Llegaste tarde y oliendo a tabaco fino. O le pagaste a don Fermín, o le debes más."
    m "Ninguna de las dos. Me voy de cateo con Celestino. Pasado mañana."
    ro "¿Para dónde?"

    menu:
        "Contarle la verdad: el Bramador.":
            $ conto_rosario = True
            m "Al Bramador."

            show rosario triste

            "Rosario deja la aguja clavada en la camisa."

            ro "¿Tú sabes lo que dicen de ese cerro?"
            m "Que tiene oro."
            ro "Que el oro tiene dueño, Matías. Y que el dueño cobra."
            ro "Mi abuela decía que el que sube al Bramador baja con las manos llenas o con la cabeza vacía, y que las dos cosas son lo mismo."
            m "Si no vamos, en un mes no tenemos ni para el pan. Don Fermín me perdonó la deuda."
            ro "Don Fermín no perdona nada. Don Fermín presta."

            "Se queda callada un rato largo. Después saca de debajo de la cama una hebra de lana roja y me la cose al forro del poncho."

            ro "Si vas a ir, anda antes donde ña Tránsito. Ella sabe tratar con esas cosas."

        "Decirle que es un cateo cerca de Chañarcillo.":
            m "Para el lado de Chañarcillo. Una quebrada que nadie ha mirado bien."

            "Rosario me mira un rato largo. Tiene la costumbre de mirar así, como si la cara de uno fuera una carta escrita en otro idioma."

            show rosario triste

            ro "Mientes mal, Matías. Siempre has mentido mal."
            ro "No te voy a preguntar más. Pero antes de irte, anda donde ña Tránsito. Hazme ese favor."

            "Saca de debajo de la cama una hebra de lana roja y me la cose al forro del poncho, sin decir nada."

    menu:
        "Ir donde doña Tránsito esa misma noche.":
            jump transito

        "No perder tiempo con supersticiones.":
            "No voy. Tengo que conseguir pólvora, revisar las barretas, dormir algo."
            "Rosario no me lo vuelve a pedir. Esa noche reza el rosario entero en voz baja, y yo me hago el dormido."
            stop music fadeout 3.0
            jump viaje


label transito:
    scene bg transito with fade
    play ambiente fogata fadein 2.0

    "Doña Tránsito vive al final de la calle, donde Copiapó se acaba y empieza el pedregal. Dicen que tiene más de ochenta años; ella dice que dejó de contarlos después del terremoto."
    "Su rancho huele a ruda, a sebo y a humo de pimiento. Hay santos en todas las paredes, y todos tienen las caras gastadas de tanto besarlos."

    show transito neutral with dissolve

    tr "Pasa, Matías Ardiles. Traes olor a arena del poniente."
    m "Todavía no he ido."
    tr "Ya vas yendo. Siéntate."

    $ consejo = True

    tr "Tres cosas. Grábatelas como el padrenuestro."
    tr "Una: no le digas tu nombre de bautizo. El nombre completo es una llave, y él colecciona llaves."
    tr "Dos: no le recibas nada. Ni agua, ni fuego, ni un trago. El que recibe, debe."
    tr "Tres: el Coludo cumple la letra de los tratos, no lo que uno quiso decir. Si vas a tratar con él, trata como escribano, no como cristiano."
    m "¿Y si no quiero tratar con él?"
    tr "Entonces no subas. Pero vas a subir."

    "Echa unas hojas al fuego. El humo sube derecho, sin moverse, aunque por las rendijas entra el viento."

    tr "Te voy a decir algo que en Copiapó todos saben y nadie dice."
    tr "Fermín Cisternas y Ulises Rojas subieron juntos al Bramador el año veintinueve. Fermín bajó con tres alforjas llenas. Ulises bajó vacío."
    tr "Vacío por dentro, ¿me entiendes? El cuerpo camina, come, duerme. Lo de adentro se quedó en el cerro."
    tr "Un rico así nunca termina de pagar, mijo. El oro del Bramador cobra intereses."

    if escucho_ulises:
        "Pienso en los dedos de Ulises, juntos delante de mi cara. Como quien saca una moneda de un bolsillo."

    tr "Anda. Y si llegas a estar delante de él, acuérdate de lo que firmaste."
    m "¿Cómo sabe que firmé algo?"
    tr "Porque a Fermín le gustan los papeles. Igual que al otro."

    hide transito with dissolve
    stop ambiente fadeout 2.0
    stop music fadeout 3.0
    jump viaje


## ----------------------------------------------------------------------------
##  CAPÍTULO 3 · Las faldas del Bramador
## ----------------------------------------------------------------------------

label viaje:
    scene bg cerro_tarde with fundido_lento
    play ambiente viento fadein 2.0
    play music tema fadein 4.0

    "Salimos de Copiapó antes del alba, con las dos mulas de don Fermín, valle abajo por el camino de Toledo."
    "El Bramador se ve desde lejos. Es un cerro como cualquier otro, de roca parda y pelada, pero con una falda entera cubierta de arena clara, como si alguien le hubiera echado un mantel encima."
    "De lejos parece manso. De cerca, también. Eso es lo peor."

    show celestino risa with dissolve

    c "¿Sabes lo que dijo el gringo ese, el del barco inglés? Que era la arena nomás. Que los granos se frotan y suenan, como cuando uno camina por la playa."
    c "¡Arena! ¿Y por qué se queja como gente, entonces?"
    m "¿Usted lo ha oído de cerca?"
    c "Una vez. Hace años. No me gustó."

    "Subimos un trecho por la falda. La arena es fina y se escurre bajo las ojotas. Celestino se detiene arriba, me guiña un ojo y se deja caer sentado, ladera abajo."

    play sound arena
    show cg avalancha with dissolve
    play cerro cerro_snd("bramido")
    show cg avalancha at temblor_cerro

    "Y el cerro brama."
    "No es un ruido. Es un temblor que entra por los pies y sube por los huesos. Una nota grave y larga, como un órgano de iglesia tocado debajo de la tierra."
    "La arena corre en lenguas alrededor de Celestino, y cada lengua suma su voz a las otras, hasta que todo el cerro está cantando la misma nota."
    "Después, despacio, se calla."

    hide cg avalancha with dissolve
    show celestino miedo with dissolve

    "Celestino está sentado al pie de la ladera, blanco de polvo. Ya no se ríe."

    c "Eso no es la arena, Matías."
    m "Usted mismo dijo..."
    c "Yo sé lo que dije."

    stop music fadeout 3.0
    jump campamento


label campamento:
    scene bg campamento with fundido_lento
    stop ambiente fadeout 2.0
    play ambiente fogata fadein 2.0

    "Acampamos al pie de la falda que mira al poniente, con la fogata entre nosotros y el cerro. Las mulas no quieren echarse. Miran la oscuridad con las orejas paradas."
    "No hay luna. Tal como dice el papel."

    show celestino neutral with dissolve

    c "Mañana buscamos la arena que no canta. Si la hay, la hay. Si no, nos volvemos y le decimos a Fermín que el derrotero era de gallina."

    play sound cascos

    "Entonces se oyen cascos. Lentos, sobre piedra. Viene alguien por la quebrada, sin farol."

    show celestino neutral at right with move
    play music caballero_tema fadein 3.0

    show caballero neutral at aparece(0.25)

    "Es un caballero. Levita negra, sombrero de ala ancha, una cadena de reloj que brilla aunque no hay de dónde sacar luz. Viene en una mula negra que no hace ruido al respirar."
    "Tiene la cara pálida y fina, la barba recortada como la de un notario. Y unos ojos claros que reflejan el fuego como dos monedas recién acuñadas."
    "La arena no se mueve bajo sus botas."

    cab "Buenas noches, señores. ¿Me permiten calentarme las manos? En el despoblado las noches son largas."
    c "Pase nomás, patrón. Fuego hay para todos."
    cab "Muy amable. ¿Con quién tengo el gusto?"

    c "Celestino Aracena Pastén, para servirle a usted y a Dios."

    "Lo dice antes de que alguien pueda detenerlo. El caballero inclina la cabeza, como quien recibe una moneda y la guarda."

    cab "¿Y usted, joven?"

    menu:
        "Decirle mi nombre completo.":
            $ dijo_nombre = True
            m "Matías Ardiles Contreras."

            show caballero sonrisa

            cab "Matías Ardiles Contreras. Un nombre completo es un regalo, y yo los regalos los guardo."

        "Decirle solo «Matías».":
            if consejo:
                "{i}No le digas tu nombre de bautizo.{/i} La voz de ña Tránsito, clarita, como si estuviera sentada al lado del fuego."
            m "Matías, nomás."

            show caballero sonrisa

            cab "Matías a secas. Prudente. La prudencia es una virtud muy poco rentable."

    show caballero neutral

    cab "Ustedes vienen buscando una puerta."
    c "¿Cómo sabe?"
    cab "Porque yo soy el que la cuida."

    "Celestino se ríe, como se ríe uno cuando no sabe qué otra cosa hacer. El caballero no se ríe."

    show cg caballero with dissolve

    "Saca de la levita una petaca de plata labrada. La destapa, y el olor del aguardiente llena la noche: uva, fuego, y por debajo algo metálico."

    cab "Para el frío, señores. Es de una cosecha muy antigua."

    "Celestino estira la mano y bebe un trago largo. Se le iluminan los ojos."
    "Después el caballero me ofrece la petaca a mí."

    menu:
        "Aceptar el trago.":
            $ bebio = True
            "Bebo. Es el mejor aguardiente que he tomado en mi vida. Me calienta el pecho, la guata, las manos."
            "Al final me queda en la lengua un sabor a moneda chupada."
            cab "Ahora sí que somos conocidos."

        "Rechazarlo.":
            if consejo:
                "{i}Ni agua, ni fuego, ni un trago. El que recibe, debe.{/i}"
            elif escucho_ulises:
                "{i}No le reciban nada.{/i} Los dedos del Loco, temblando delante de mi cara."
            m "Gracias, patrón. No tomo."
            cab "Lástima. Uno se pierde tantas cosas por no aceptar un convite."

    hide cg caballero with dissolve
    show caballero sonrisa

    cab "Saludos a don Fermín, cuando lo vean."
    cab "Si lo ven."

    "Se levanta. La mula negra ya está a su lado, aunque nadie la vio moverse."

    cab "Mañana, donde la arena no canta. Los espero. Con la luna nueva las puertas pesan menos."

    hide caballero with dissolve
    stop music fadeout 3.0

    "Se va por la quebrada, sin farol, sin ruido."
    "A la mañana siguiente buscamos las huellas de la mula. No hay ninguna."

    show celestino miedo

    "Y las nuestras se fueron también: a medianoche las dos mulas cortaron las amarras y huyeron hacia Copiapó."
    "Esa noche, a las tres de la mañana, el cerro bramó solo. Sin viento. Sin que nadie pisara la arena."

    play cerro cerro_snd("bramido_lejano")

    "En el bramido, juraría, alguien dijo mi nombre."

    hide celestino with dissolve
    jump puerta


## ----------------------------------------------------------------------------
##  CAPÍTULO 4 · Donde la arena no canta
## ----------------------------------------------------------------------------

label puerta:
    scene bg ladera with fundido_lento
    stop ambiente fadeout 2.0
    play ambiente viento fadein 2.0
    play music tension fadein 3.0

    "Pasamos el día entero en la falda del poniente. Cada paso hace cantar la arena, y el cerro nos sigue con su nota grave, como un perro grande que gruñe sin levantarse."

    show celestino neutral with dissolve

    c "Escucha, Matías. Escucha cuando pisas."

    "A media tarde, Celestino se mete en una hondonada y la arena se le viene encima. Una lengua blanca y lenta que lo agarra hasta la cintura y sigue subiendo."

    play sound arena
    play cerro cerro_snd("bramido_furioso")
    show bg ladera at temblor_cerro
    show celestino miedo

    c "¡Matías!"

    "Me tiro de guata y le alcanzo la barreta. Tiro. La arena brama tan fuerte que no oigo mis propios gritos. Tiro otra vez, y otra, hasta que la arena lo suelta con un ruido de algo que se rinde."
    "Nos quedamos tirados, jadeando, cubiertos de polvo."
    "Entonces me doy cuenta: la arena donde estoy acostado no suena."

    stop music fadeout 2.0
    scene bg puerta with fundido_lento

    "Es un manchón del tamaño de un rancho, en medio de la falda. Pisas y la arena calla. Como una iglesia en la que se acabó la misa."
    "Cavamos con las manos, con las barretas, con los platos de lata. A un metro aparece la piedra: un dintel labrado, liso, con unas letras que no son de ningún idioma que yo conozca."
    "Abajo hay una puerta. Y la puerta está entreabierta."

    play sound piedra

    show celestino neutral with dissolve

    c "La luna nueva. Las puertas pesan menos."
    m "Todavía podemos volvernos."
    c "¿A qué, mijo? ¿A la chingana? ¿A la deuda?"

    "Celestino enciende el chonchón y entra primero. Yo lo sigo, porque siempre lo he seguido."

    hide celestino
    stop ambiente fadeout 3.0
    play cerro cerro_snd("bramido_entrada")
    show bg puerta at temblor_cerro

    "Apenas cruzamos el dintel, el cerro empieza a bramar."
    "No afuera, en la arena. Adentro. Alrededor. En todas partes a la vez, como si nos hubiéramos metido en el pecho de un animal que respira."

    jump caverna


label caverna:
    scene bg caverna with sangre_oro
    play music coro fadein 8.0

    "El túnel baja, y baja, y de repente se abre."
    "Hay una ciudad."
    "No sé de qué otra manera decirlo. Calles, y casas, y torres de iglesia, todo de oro macizo, todo brillando con una luz que no viene de ninguna parte. Un oro amarillo y tibio, como la carne de un durazno."
    "Y en las paredes, mirándonos, hay caras."
    "Caras de mineros, de arrieros, de niñas, de viejos, fundidas en el oro como monedas mal acuñadas. Tienen los ojos abiertos. Algunas mueven los labios."
    "El bramido aquí adentro no es una nota. Son voces. Muchas voces cantando encima del cerro, sin poder parar."

    show celestino risa with dissolve
    play sound oro

    "Celestino ya tiene los bolsillos llenos. Se ríe con una risa que no le conozco, una risa de niño y de borracho."

    c "¡Mira, Matías! ¡Mira! ¡Se despega con la mano, como queso!"
    m "Celestino. Las caras."
    c "¿Qué caras?"

    play music caballero_tema fadein 2.0
    show celestino miedo at right with move
    show caballero neutral at aparece(0.3)

    "Al fondo de la plaza de oro hay un sillón de cuarzo. Y en el sillón, con las piernas cruzadas, está el caballero de anoche."

    $ nombre_caballero = "El Caballero"

    cab "Bienvenidos a mi casa. ¿Les gusta? Todo esto lo hicieron otros, con sus manos y con sus nombres."
    cab "Les voy a hablar con franqueza, porque soy un comerciante honrado. El más honrado de este valle, aunque eso no es mucho decir."

    show caballero sonrisa

    cab "Don Fermín Cisternas me debe."
    cab "Hace diez años me pagó con su socio Ulises y se llevó tres alforjas. Pero el oro cobra intereses, y los intereses del oro se pagan en almas."
    cab "Don Fermín me prometió otro pago para esta luna nueva. Y me mandó a ustedes dos."

    "Lo dice como quien lee una factura."
    "Me acuerdo de don Fermín diciéndole a Celestino: {i}cuídeme al muchacho{/i}. Y de que lo dijo mirándolo a él."

    show caballero neutral

    cab "Así que tengo derecho a uno de ustedes. Pero soy generoso, y me aburren los trámites: todo este oro es para el primero que diga un nombre."

    "Celestino me mira. Yo lo miro a él. Celestino abre la boca."
    "Y la cierra."

    cab "O, don Matías, podría usted ofrecerme a alguien que lo espera en Copiapó. Una lavandera de manos ásperas que remienda camisas ajenas junto al brasero. Vale más que este viejo, se lo aseguro."
    m "Ni la nombre."

    show caballero sonrisa

    cab "Como guste. Entonces, un nombre. El que usted quiera."

    if dijo_nombre:
        cab "Y apúrese, Matías Ardiles Contreras. Las puertas no se quedan abiertas para siempre."
        "Cuando dice mi nombre completo siento que algo me tira de adentro, suavecito, como un anzuelo."

    if bebio:
        "El trago de anoche me arde todavía en el estómago. Siento que el caballero sabe exactamente dónde está."

    menu:
        "Decir: «Celestino Aracena».":
            jump final_precio

        "Llenar las alforjas de oro y correr hacia la salida.":
            jump final_loco

        "«No hay trato.» Agarrar a Celestino y salir sin nada.":
            jump final_arena

        "Sacar el contrato: «Mi socio es don Fermín Cisternas»." if contrato and (escucho_ulises or consejo) and not bebio:
            jump final_letra


## ----------------------------------------------------------------------------
##  FINAL I · El precio
## ----------------------------------------------------------------------------

label final_precio:
    m "Celestino Aracena."

    "No lo digo fuerte. No hace falta."

    show celestino miedo

    "Celestino me mira. No hay rabia en su cara. Hay algo peor: entiende. Me entiende perfectamente."

    c "Ay, mijo."

    play cerro cerro_snd("bramido_furioso")
    show bg caverna at temblor_cerro
    hide celestino with fundido_lento

    "Y ya no está."
    "En el suelo de oro queda su chupalla, todavía dando vueltas. El coro de las paredes sube medio tono. Hay una voz nueva cantando."

    show caballero sonrisa

    cab "Cuentas claras, socio. Llévese lo que pueda cargar. Lo demás se lo guardo para la próxima."

    stop music fadeout 3.0
    scene bg calle_noche with fundido_muy_lento
    play music oscuro fadein 3.0

    "Bajé del Bramador solo, con tres alforjas llenas. Las llevé al hombro dos días por el desierto. No me pesaban."
    "En Copiapó, al día siguiente, todo el mundo sabía. Nadie dijo nada. Solo lo murmuraban cuando yo pasaba."
    "{i}Ese entregó a alguien.{/i}"

    if conto_rosario:
        "Rosario no me preguntó nada. Sabía adónde había ido, y vio que volví solo. Esa misma tarde juntó sus dos vestidos y se fue a La Serena, donde su hermana."
    else:
        "Rosario me preguntó por Celestino. Le dije que se había quedado cateando en la cordillera. Me miró con esa mirada de carta en otro idioma, y esa misma tarde juntó sus dos vestidos y se fue a La Serena, donde su hermana."

    "Don Fermín me mandó un recado: me felicitaba por el éxito de la compañía. Nunca le contesté."

    scene bg mansion with fundido_lento

    "Hoy tengo la casa más grande de Copiapó. Ventanas de vidrio, piano de cola, alfombras traídas de Valparaíso."
    "Cada mañana, la sirvienta barre arena del suelo del salón. Arena clara, fina, del poniente. Nadie sabe por dónde entra."
    "Y cada noche, cuando el viento viene de Toledo, el cerro brama."

    play cerro cerro_snd("bramido_lejano")

    "Yo conozco esa voz. Es la que cantaba la nota más baja del coro. Es la de Celestino."

    stop music fadeout 4.0

    "Esta noche alguien golpeó la puerta. Tres veces, despacito."

    play sound golpes

    cab "Buenas noches, don Matías. Vengo por los intereses."

    scene negro with fundido_muy_lento
    $ fin_num = 1
    $ fin_nombre = "El precio"
    jump fin


## ----------------------------------------------------------------------------
##  FINAL II · El loco del Bramador
## ----------------------------------------------------------------------------

label final_loco:
    "No digo ningún nombre. Agarro las alforjas y las lleno de oro a manotazos. Celestino hace lo mismo."

    play sound oro
    show caballero neutral

    cab "Señores. Eso no se hace."

    "No lo dice enojado. Lo dice como un profesor que ve a un niño copiando en la prueba."

    play cerro cerro_snd("bramido_furioso")
    show bg caverna at temblor_cerro
    hide caballero with dissolve

    "Corremos. El túnel brama, las paredes braman, las caras de oro abren la boca y braman con nosotros. La arena empieza a llover del techo, primero un hilo, después una cortina."
    "Yo voy adelante. Celestino viene atrás, cargando más que yo."

    scene bg puerta with relampago

    "Salgo de la puerta de cabeza, rodando por la arena muda. Me doy vuelta."
    "La puerta se está cerrando. No de golpe: despacio, con un ruido de piedra contra piedra, como una boca que mastica."

    play sound piedra

    "Del otro lado, la voz de Celestino gritando mi nombre."
    "Después, solo el bramido."

    stop music fadeout 3.0
    scene bg calle_noche with fundido_muy_lento
    play music oscuro fadein 3.0

    "Llegué a Copiapó con las alforjas llenas y le pagué a don Fermín sus ciento veinte pesos en oro. Él contó las monedas sin levantar la vista."
    "Esa misma noche empezó."
    "Cada vez que alguien arrastraba una silla, yo oía el bramido. Cada vez que el viento movía la arena de la calle, el bramido. El agua al hervir. La lluvia, las dos veces que llovió."
    "Y en cada esquina, de reojo, una mula negra que no hacía ruido al respirar."
    "El oro se me fue como agua: en médicos, en curas, en candados, en velas. En aguardiente, que no me hacía dormir."

    if conto_rosario:
        "Rosario no se fue. Me trae agua todos los días a la chingana. A veces la reconozco. Cuando la reconozco, lloro, y ella me limpia la cara con el delantal sin decir nada."
    else:
        "Rosario se fue un día, o puede que yo me haya ido. No me acuerdo bien. A veces una mujer me trae agua a la chingana y me limpia la cara con el delantal. Creo que la conozco."

    scene bg chingana with fundido_lento
    show ulises neutral at left with dissolve

    "Ahora me siento en la chingana con Ulises. No hablamos. No hace falta. Cuando el cerro brama, los dos levantamos la cabeza al mismo tiempo, como perros que oyen a su amo."
    "Hay muchachos nuevos en Copiapó, con derroteros nuevos. Cada tanto, alguno nombra el cerro en voz alta."
    "Y yo me paro en la puerta."

    play cerro cerro_snd("bramido_lejano")

    m "¿Quién dijo Bramador?"

    scene negro with fundido_muy_lento
    $ fin_num = 2
    $ fin_nombre = "El loco del Bramador"
    jump fin


## ----------------------------------------------------------------------------
##  FINAL III · Arena
## ----------------------------------------------------------------------------

label final_arena:
    m "No hay trato."

    "Agarro a Celestino del poncho."

    m "Bote todo, Celestino. Todo. Hasta la última pepita."
    c "Matías, mijo, mira lo que..."
    m "¡Bótelo!"

    play sound oro

    "Celestino da vuelta los bolsillos, llorando como un niño. El oro cae al suelo de oro sin hacer ruido, y se hunde en él como en agua."

    show caballero neutral

    cab "Así que no se llevan nada."
    cab "Entonces nada me deben. Yo no cobro lo que no se lleva. Soy el Diablo, pero no soy un ladrón."

    if bebio:
        show caballero sonrisa
        cab "Bueno. Casi nada. Ese trago de anoche corre por su cuenta, don Matías. Se lo voy a ir cobrando de a poquito."

    if dijo_nombre:
        "Doy un paso hacia la salida y el caballero dice mi nombre completo, despacio, como quien lee una lista."
        "Las piernas se me quedan pegadas al oro. Celestino me agarra del brazo y tira, tira, como yo tiré de él en la arena."

    hide caballero with dissolve
    play cerro cerro_snd("bramido")
    stop music fadeout 3.0

    scene bg desierto_alba with fundido_muy_lento
    play music luz fadein 4.0

    "Salimos al amanecer. La puerta se cerró detrás de nosotros con un suspiro de piedra, y la arena muda se puso a cantar otra vez, como si nunca hubiera callado."
    "Volvimos a Copiapó a pie. Dos días, sin mulas, con medio chuspe de agua. No hablamos casi nada."

    scene bg calle_alba with fundido_lento

    "Llegando, nos enteramos."
    "Don Fermín Cisternas había desaparecido la noche de la luna nueva. Su casa estaba llena de arena hasta las ventanas. Arena clara y fina, del poniente."
    "Cuando abrieron su caja fuerte, adentro no había onzas ni barras. Había arena."
    "El Coludo cobró lo que le debían. Y no fuimos nosotros."

    show rosario sonrisa at right with dissolve

    if conto_rosario:
        "Rosario me esperaba en la puerta del rancho. No me preguntó por el oro. Me sacó la hebra de lana roja del poncho y la guardó en su cajita, como quien guarda una cosa que ya cumplió."
    else:
        "Rosario me esperaba en la puerta del rancho. Le conté todo, la verdad completa, por primera vez. Me escuchó sin interrumpir, y al final me sacó la hebra de lana roja del poncho y la guardó en su cajita."

    "Celestino dejó el cateo. Ahora es arriero entre Copiapó y el puerto, y dice que es el oficio más honrado del mundo porque las mulas no saben mentir."

    if bebio:
        "Yo sigo pobre. Y cada vez que hay silencio, en la misa, en la noche, en el momento antes de dormirme, oigo una nota grave y lejana. Es el trago. Lo sigo pagando, de a poquito."
    else:
        "Yo sigo pobre. Pero duermo de un tirón, y en Copiapó, en estos tiempos, eso vale más que una veta."

    "A veces, cuando el viento viene de Toledo, el cerro brama. Rosario y yo nos quedamos callados, escuchando."
    "Arena, dijo el inglés. Puede ser."

    scene negro with fundido_muy_lento
    $ fin_num = 3
    $ fin_nombre = "Arena"
    jump fin


## ----------------------------------------------------------------------------
##  FINAL IV · La letra del trato
## ----------------------------------------------------------------------------

label final_letra:
    "Me meto la mano al forro del poncho, junto a la hebra roja de Rosario, y saco el papel doblado en cuatro."
    "{i}Trata como escribano, no como cristiano.{/i}"

    m "Usted quiere el pago de don Fermín Cisternas."

    show caballero neutral

    cab "Lo quiero, y lo tendré."
    m "Entonces cóbreselo a él."

    "Desdoblo el contrato y lo levanto a la luz del oro."

    m "Compañía minera {i}La Fortuna del Poniente{/i}. Socios: Fermín Cisternas, Celestino Aracena, Matías Ardiles. Firmado ante escribano."
    m "Cláusula cuarta: cada socio responde ante las deudas de la compañía con lo suyo y con los suyos."
    m "La deuda es de don Fermín, que la contrajo. Don Fermín es nuestro socio. Esta compañía le debe a usted un alma: que la pague el socio que firmó primero."

    "Por primera vez, el Caballero se queda callado."
    "Estira una mano enguantada. Le paso el papel. Lo lee entero, despacio, moviendo los labios en las palabras difíciles, como hacía mi madre con el catecismo."

    show caballero sonrisa

    cab "«Con lo suyo y con los suyos.» Qué hermosa fórmula. Debí haberla inventado yo."
    cab "La letra es la letra, don Matías. Acepto el pago."
    m "Una cosa más."
    cab "Siempre hay una cosa más con ustedes."
    m "No quiero oro. Ni una pepita. Quiero que le devuelva a Ulises Rojas lo que le sacó con dos dedos."

    "El Caballero me mira largo. En sus ojos de moneda veo mi cara chiquitita, dos veces."

    cab "Un alma por un alma. La contabilidad cuadra. Me gusta la gente que lleva bien las cuentas."

    show caballero revelado
    play cerro cerro_snd("bramido_furioso")
    show bg caverna at temblor_cerro

    "Se para. Por un segundo, su sombra en la pared de oro no tiene la forma de un hombre. Tiene cuernos, y una cola que barre las caras fundidas."
    "Mete la mano en la pared, entre dos caras, y saca algo chiquito y tibio, que alumbra como una luciérnaga. Lo sopla."
    "La lucecita sube por el túnel, hacia afuera, hacia Copiapó."

    show caballero neutral

    cab "Váyanse. Y don Matías: no vuelva nunca. A los escribanos no los quiero de clientes."

    hide caballero with fundido_lento
    stop music fadeout 3.0

    scene bg desierto_alba with fundido_muy_lento
    play music luz fadein 4.0

    "Salimos con las manos vacías. Celestino había vaciado sus bolsillos sin que nadie se lo pidiera."
    "Cuando la puerta se cerró detrás de nosotros, el cerro bramó. Pero sonaba distinto. Como si en el coro cantara una voz menos."

    scene bg calle_alba with fundido_lento
    play sound campana

    "Llegamos a Copiapó al tercer día, muertos de sed."
    "La casa de don Fermín estaba llena de arena hasta las ventanas de vidrio. Del dueño no quedaba ni el anillo."
    "Y en la plaza, sentado en la pila, con la barba recién lavada, había un hombre mirando cómo salía el sol sobre los cerros del oriente."

    show ulises lucido with dissolve

    "Tenía los ojos claros. Los ojos de un hombre que acaba de despertar de una siesta muy larga."

    u "Disculpe, joven. ¿Usted sabe qué año es?"
    m "Mil ochocientos treinta y nueve, don Ulises."
    u "Diez años."
    u "Tengo mucha sed. Y diez años que contar."

    show ulises lucido at left with move
    show rosario sonrisa at right with dissolve

    "Rosario vino corriendo desde la calle Atacama, con el delantal todavía mojado. No me preguntó nada. Solo me sacó la hebra roja del poncho y me la amarró en la muñeca."

    "Nunca volví al Bramador. Pero cada vez que paso por el camino de Toledo y el cerro brama, me saco el sombrero."
    "Arena, dijo el inglés."
    "Yo sé lo que oí."

    scene negro with fundido_muy_lento
    $ fin_num = 4
    $ fin_nombre = "La letra del trato"
    jump fin


## ----------------------------------------------------------------------------
##  Cierre común de los finales
## ----------------------------------------------------------------------------

label fin:
    stop music fadeout 3.0
    stop ambiente fadeout 3.0
    $ persistent.finales.add(fin_num)
    $ vistos = len(persistent.finales)

    centered "{size=+14}FINAL [fin_num] · [fin_nombre]{/size}\n\nHas visto [vistos] de 4 finales." with dissolve

    if vistos < 4:
        if 4 not in persistent.finales:
            if not contrato:
                centered "{i}Pista: el Coludo cumple la letra de los tratos. Lee bien lo que firmas.{/i}" with dissolve
            elif not (escucho_ulises or consejo):
                centered "{i}Pista: en Copiapó alguien sabe con quién subió don Fermín al cerro, hace diez años.{/i}" with dissolve
            elif bebio:
                centered "{i}Pista: ni agua, ni fuego, ni un trago. El que recibe, debe.{/i}" with dissolve
            else:
                centered "{i}Pista: en la ciudad de oro, el contrato puede decir más que una súplica.{/i}" with dissolve
        else:
            centered "{i}Todavía quedan caminos por recorrer en el cerro.{/i}" with dissolve
    else:
        centered "{i}Has recorrido todos los caminos del Bramador.\nGracias por escuchar al cerro.{/i}" with dissolve

    centered "{size=-4}El Bramador · Una leyenda de Copiapó{/size}" with dissolve
    return
