import re
import glob
import random 
import datetime


# Obtener lista de fotos para generar tageos de temáticast [Restaurante, hotel, gimnasio, etc]
# Apuntar a objetos en S3
pic_list = glob.glob('./pics/*.jpg')
# creacion de tags a partir de nombres de los objetos
r = re.compile(' Internet-[0-9]+.jpg')
tags = [re.sub(r, '', pic.split('/')[2]) for pic in pic_list]

# Archivos con templates y layout correspondientes 
templates = {
    'rackCard1' : ('./template_rackcard.pptx',2),
    'rackCard2' : ('./template_rackcard.pptx',3),
    'factSheet1' : ('./template_factsheet.pptx',1),
    'factSheet2' : ('./template_factsheet.pptx',2),
}


# Diccionario de posiciones de templates
position_dict = {
    'rackCard1' : {
        'text_explain' : [13],
        'text_dir' : [14],
        'text_hotel_name' : [15],
        'text_hotel_link' : [16],
        # 'pic_logo' : [17],
        'text_init' : [18],
        'pic_wide' : [19],
        'pic_1' : [20],
        'pic_2' : [21],
        'text_copy' : [22]
        },
    'rackCard2':{
        'pic_1': [10],
        'pic_2': [11],
        'text_copy' : [13],
        # 'text_copy_2' : [14],
        # 'pic_logo' : [15],
        'text_hotel_name' : [16],
        'text_dir' : [17],
        'text_hotel_link' : [18],
        'text_init' : [19] 
        },
    'factSheet1': {
        'pic_1' : [10],
        'pic_2' : [17],
        'pic_4' : [18],
        'pic_6' : [29],
        'pic_7' : [30],
        'pic_8' : [31],
        'text_title_amenidades' : [11],
        'text_amenidades_1' : [12],
        # 'text_amenidades_2' : [13],
        'text_cost' : [14],
        'text_nearus_title' : [15],
        'text_nearus' : [16],
        'text_hotel_name' : [20,27],
        'text_dir' : [21,26],
        'text_hotel_link' : [22,25],
        'text_choice_privileges' : [24],
        'text_explain' : [28],
        'text_init' : [32]
        },
    'factSheet2': {
        'pic_1' : [10],
        'pic_2' : [15],
        'pic_3' : [16],
        'pic_4' : [17],
        'text_title_1' : [11],
        'text_explain_1' : [12],
        'text_title_2' : [13],
        'text_explain_2' : [14],
        'text_title_3' : [18],
        'text_explain_4' : [19]
        }
}

text_rack1 = {
'text_explain' : 'Ya sea que viajes por trabajo o por placer, Comfort Inn® \n te ofrece una experiencia cálida y acogedora con los \n beneficios que te ayudarán a iniciar tu día.',
'text_dir' : 'Av. Hidalgo 3408-A. Flores, \n C.P. 89220 | Tampico, Tam. \n 800 36 (HOTEL) 46835',
'text_hotel_name' : 'Comfort Inn Tampico',
'text_init' : 'Despierta listo para iniciar tu día',
'text_copy' : 'Lo mejor de nosotros. Para lo mejor para ti.',
'text_hotel_link' : 'ChoiceHotels.com'
}

text_rack2 = {
'text_init' : 'Amenidades clave',
'text_copy' : '88 modernas habitaciones Centro de negocios \nDesayuno continental gratis \nInternet WiFi de cortesía \nPiscina al aire libre \nEstacionamiento sin costo techado \nRestaurante \n1 salón con capacidad max. de 50 p.',
'text_hotel_name' : 'Comfort Inn Tampico',
'text_dir' : 'Av. Hidalgo 3408-A. Flores, \n C.P. 89220 | Tampico, Tam. \n 800 36 (HOTEL) 46835',
'text_hotel_link' : 'ChoiceHotels.com'
}
text_fact1 = {
'text_title_amenidades' : 'Nuestras amenidades clave',
'text_amenidades_1' : "53 modernas habitaciones \nDesayuno americano tipo buffet de cortesía \nCentro de negocios \nPiscina al aire libre por temporada \nGimnasio \nLounge/Bar \nRestaurante \nEstacionamiento cubierto \nCafetería \nLavandería* \nServicio de alquiler de coches* \n3 salones con capacidad max. de 350 p.",
'text_cost' : '*Costo adicional',
'text_nearus_title' : 'Cerca de nosotros',
'text_nearus' : "McDonald’s \nCasa Los Campos \nBurger King \nPizza Hut \nLos Portales de Zevallos \nCatedral Inmaculada \nPlaza Crystal \nBarranca Metlac \nSanatorio Covadonga \nPalacio Municipal \nParque Industrial \nTec de Monterrey",
'text_hotel_name' : 'Comfort Inn Córdoba',
'text_dir' : "Av. 1 2623, Plaza Fundadores \nC.P. 94550 | Córdoba, Ver. \n800 36 (HOTEL) 46835",
'text_hotel_link' : 'ChoiceHotels.com',
'text_choice_privileges': 'Únase al programa de recompensas Choice Privileges®.\nEl camino más fácil para ganar una noche gratis. \nInscríbase hoy en el área del servicio del hotel o en ChoicePrivileges.com para obtener recompensas inmediatamente.',
'text_explain': 'En Comfort Inn® trabajamos arduamente para ayudarte a sentirte renovado, para que puedas estar listo para afrontar tu día. Contarás con ropa de cama de primera calidad para sentirte renovado por la mañana. Esto es solo la mitad de la batalla, también ofrecemos opciones de desayuno saludables que necesitas para iniciar el día. Y, como necesitas estar conectado, hay Wi-Fi rápido y gratuito en todas las habitaciones. \n \n Un mejor nosotros. Para lo mejor de ti.',
'text_init' : 'Cuando se trata de negocios, hablamos en serio.'
}

text_fact2 = {
'text_title_1' : 'Estamos listos para que usted esté listo.',
'text_explain_1' : 'Nos aseguramos de que se sienta bienvenido y relajado desde el momento en que llega y durante su estancia. Nuestro amable equipo siempre está para ayudarlo, desde proveerle recomendaciones de lugares locales hasta cuidar de los detalles para que disfrute de su estancia.',
'text_title_2' : 'Detrás de cada gran día hay una gran noche.',
'text_explain_2' : 'En Comfort Inn®, contamos con modernas y espaciosas habitaciones diseñadas para hacer su estadía renovadora. Encontrarás opciones de almohadas suaves y firmes, lujosa ropa de cama de primera calidad, estaciones de carga junto a la cama, artículos de tocador exclusivos y Wi-Fi gratis.',
'text_title_3' : 'El mejor camino para comenzar el día.',
'text_explain_4' : '¿Qué tal un desayuno abundante con opciones saludables? Complacerlo con un buen desayuno es sólo otro camino para asegurarnos que usted esté complacido mientras viaja por trabajo o placer.',
}

