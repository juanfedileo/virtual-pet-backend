from django.db import migrations
from decimal import Decimal

# Usaremos los mismos datos de tus mocks de React.
# ¡Asegúrate de que los campos coincidan con tu 'products/models.py'!
# (Ej. si tu modelo tiene 'title', 'price' y 'description', esto funcionará)
MOCK_PRODUCTS = [
    {
        "id":1,
        "title":"Alimento Royal Canin Maxi Adulto Perro",
        "price":52340,
        "description":"Alimento royal canin para perros grandes de 26 a 44 kilos. La mejor calidad para tu peludo",
        "category":"comida",
        "image":"https://i.ibb.co/XrM0Yzqz/01-Alimento-Royal-Canin-Maxi-Adulto-Perro.png"
    },
    {
        "id":2,
        "title":"Alimento Purina One Cat Adulto",
        "price":14800,
        "description":"Alimento sabor pollo y salmon de 7,5Kg. Lo ves y el lo siente",
        "category":"comida",
        "image":"https://i.ibb.co/N2z52J8c/02-Alimento-Purina-One-Cat-Adulto.png"
    },
    {
        "id":3,
        "title":"Alimento Eukanuba Puppy Large Breed",
        "price":71000,
        "description":"Alimento eukanuba para cachorros de hasta 24 meses. Razas grandes. Sabor Pollo.",
        "category":"comida",
        "image":"https://i.ibb.co/9mzq0CJj/03-Alimento-Eukanuba-Puppy-Large-Breed.webp"
    },
    {
        "id":4,
        "title":"Alimento Vital Can Premium Cachorro",
        "price":46600,
        "description":"Alimento vital can 15kg para cachorros. Lo mejor para tu perrito a un precio accesible.",
        "category":"comida",
        "image":"https://i.ibb.co/s9SgqVZP/04-Alimento-Vital-Can-Premium-Cachorro.png"
    },
    {
        "id":5,
        "title":"Alimento Pedigree Adulto Mediano Perro",
        "price":27500,
        "description":"Alimento pedigree de 21 Kg sabor carne, pollo y cereales",
        "category":"comida",
        "image":"https://i.ibb.co/xK7qth9k/05-Alimento-Pedigree-Adulto-Mediano-Perro.png"
    },
    {
        "id":6,
        "title":"Alimento Whiskas Pollo Gato",
        "price":13200,
        "description":"Pack de 2 Sobrecitos whiskas sabor pollo para gatitos consentidos.",
        "category":"comida",
        "image":"https://i.ibb.co/TBzDv3sg/06-Alimento-Whiskas-Pollo-Gato.png"
    },
    {
        "id":7,
        "title":"Alimento Royal Canin Vet Gastrointestinal Gato",
        "price":64700,
        "description":"Alimento gastrointestinal para gatitos delicados. Lo mejor para tu peludito",
        "category":"comida",
        "image":"https://i.ibb.co/jXr7pgV/07-Alimento-Royal-Canin-Vet-Gastrointestinal-Gato.png"
    },
    {
        "id":8,
        "title":"Alimento Purina Dog Chow Adulto",
        "price":22100,
        "description":"Alimento dogchow extra life para perros adultos, razas medianas y grandes",
        "category":"comida",
        "image":"https://i.ibb.co/PvdXyZgY/08-Alimento-Purina-Dog-Chow-Adulto.webp"
    },
    {
        "id":9,
        "title":"Alimento Purina Excellent Senior Gato",
        "price":19800,
        "description":"Alimento purina excellent para gatitos adultos. Cuida siempre a tu gatito",
        "category":"comida",
        "image":"https://i.ibb.co/6cx2PRRh/09-Alimento-Purina-Excellent-Senior-Gato.jpg"
    },
    {
        "id":10,
        "title":"Alimento Royal Canin Size Mini Adulto Perro",
        "price":43800,
        "description":"Alimento royal canin para perros adultos de raza pequeña de hasta 10kg de peso",
        "category":"comida",
        "image":"https://i.ibb.co/ynDLG8P1/10-Alimento-Royal-Canin-Size-Mini-Adulto-Perro.png"
    },
    {
        "id":11,
        "title":"Alimento Eukanuba Adult Performance Perro",
        "price":80500,
        "description":"Alimento eukanuba de 20 Kilos para perros adultos muy activos. La mejor nutricion para tu perrito",
        "category":"comida",
        "image":"https://i.ibb.co/ZzCdXfL2/11-Alimento-Eukanuba-Adult-Performance-Perro.png"
    },
    {
        "id":12,
        "title":"Alimento Vital Can Complete Gato Adulto",
        "price":24400,
        "description":"Bolsa de 105kg de alimento vital can complete para gatitos adultos. Recomendado para gatitos de 12 meses a 7 años",
        "category":"comida",
        "image":"https://i.ibb.co/yF7Sn5vr/12-Alimento-Vital-Can-Complete-Gato-Adulto.png"
    },
    {
        "id":13,
        "title":"Alimento Pedigree Cachorro Pollo",
        "price":29300,
        "description":"Pack de 4 Sobrecitos de bifecitos en salsa para tu cachorrito. Ideal para complementar su alimentación diaria y verlos crecer de forma sana",
        "category":"comida",
        "image":"https://i.ibb.co/7NtnTDVP/13-Alimento-Pedigree-Cachorro-Pollo.png"
    },
    {
        "id":14,
        "title":"Alimento Whiskas Pouch Atún Gato",
        "price":11500,
        "description":"1 sobrecito de whiskas sabor atun para darle un mimo bien merecido a tu gatito.",
        "category":"comida",
        "image":"https://i.ibb.co/27ScKt5k/14-Alimento-Whiskas-Pouch-At-n-Gato.png"
    },
    {
        "id":15,
        "title":"Alimento Purina Pro Plan Sensitive Digestión",
        "price":99200,
        "description":"Alimento para perros con sensibilidad estomacal y de la piel. Sabor cordero. Con un toque de avena.",
        "category":"comida",
        "image":"https://i.ibb.co/ccPtH7Pt/15-Alimento-Purina-Pro-Plan-Sensitive-Digesti-n.png "
    },
    {
        "id":16,
        "title":"Alimento Royal Canin Maxi Puppy Perro",
        "price":68800,
        "description":"Alimento Royal Canin para cachorros grandotes. Cuidalos en esta etapa para que crezcan sanos y fuertes",
        "category":"comida",
        "image":"https://i.ibb.co/5xM0WtxT/16-Alimento-Royal-Canin-Maxi-Puppy-Perro.png"
    },
    {
        "id":17,
        "title":"Alimento Purina One Senior Perro",
        "price":20500,
        "description":"Alimento purina one senior para razas pequeñas.  Nutrición especial para tu pequeño gigante",
        "category":"comida",
        "image":"https://i.ibb.co/mVL9TmcY/17-Alimento-Purina-One-Senior-Perro.png"
    },
    {
        "id":18,
        "title":"Alimento Eukanuba Adulto Raza Pequeña",
        "price":73000,
        "description":"Alimento eukanuba sabor pollo para perritos adultos de raza pequeñas.",
        "category":"comida",
        "image":"https://i.ibb.co/FLQ7y5fG/18-Alimento-Eukanuba-Adulto-Raza-Peque-a.png"
    },
    {
        "id":19,
        "title":"Alimento Vital Can Balanced Senior Mediano",
        "price":31200,
        "description":"Alimento vital can de 3kg Balanced para razas medianas. Excelente calidad precio",
        "category":"comida",
        "image":"https://i.ibb.co/G3dP3MgZ/19-Alimento-Vital-Can-Balanced-Senior-Mediano.png "
    },
    {
        "id":20,
        "title":"Alimento Pedigree Pollo Verduras Perro raza pequeña",
        "price":28000,
        "description":"Bolsa de alimento pedigree de 3kg para razas pequeñas y minis. Sabor carne y vegetales",
        "category":"comida",
        "image":"https://i.ibb.co/Tq75vnhQ/20-Alimento-Pedigree-Pollo-Verduras-Perro-raza-peque-a.png"
    },
    {
        "id":21,
        "title":"Cucha Perro Mediano suave",
        "price":132000,
        "description":"Cucha super mullida y acolchonada para tu perrito. Disponible unicamente en color gris. Especial para perros medianos",
        "category":"camas",
        "image":"https://i.ibb.co/WvrStN4T/21-Cucha-Perro-Mediano-suave.jpg"
    },
    {
        "id":22,
        "title":"Cama Plush Perro Pequeño",
        "price":115000,
        "description":"Camitas de plush super comodas para perritos de raza pequeña",
        "category":"camas",
        "image":"https://i.ibb.co/99Z1G3s2/22-Cama-Plush-Perro-Peque-o.png"
    },
    {
        "id":23,
        "title":"Ropa Abrigo Perro Mediano",
        "price":37850,
        "description":"Queres que tu perro esté calentito y se vea super canchero? este abrigo es ideal para lograr ambas cosas",
        "category":"ropa",
        "image":"https://i.ibb.co/cXCSWRJ9/23-Ropa-Abrigo-Perro-Mediano.png"
    },
    {
        "id":24,
        "title":"Ropa Chaqueta Gato Catdidas",
        "price":26900,
        "description":"Tu gatito va a despertar la envidia del barrio con esta campera super canchera de catdidas",
        "category":"ropa",
        "image":"https://i.ibb.co/5WJHHy6L/24-Ropa-Chaqueta-Gato-Catdidas.png"
    },
    {
        "id":25,
        "title":"Ropa Sudadera Perro",
        "price":31400,
        "description":"Tu perrito siempre tiene frio? queres ser la envidia del barrio? este es el hoodie ideal para el.",
        "category":"ropa",
        "image":"https://i.ibb.co/ZpDRwjwz/25-Ropa-Sudadera-Perro.png"
    },
    {
        "id":26,
        "title":"Kit Limpieza Bandeja Gato + Palita",
        "price":11000,
        "description":"Bandejita con palita para gatos o perritos muy educados.",
        "category":"limpieza",
        "image":"https://i.ibb.co/KzQMqpDx/26-Kit-Limpieza-Bandeja-Gato-Palita.png"
    },
    {
        "id":27,
        "title":"Shampoo Hypoalergénico Perro",
        "price":19500,
        "description":"Shampoo para dejar el pelo de tu amigo peludo muy suave y sedoso.",
        "category":"limpieza",
        "image":"https://i.ibb.co/3ytZ1mFg/27-Shampoo-Hypoalerg-nico-Perro.png"
    },
    {
        "id":28,
        "title":"Toallitas Húmedas Gato",
        "price":9500,
        "description":"Toallitas humedas ideal para limpiar las orejitas de tu gatito",
        "category":"limpieza",
        "image":"https://i.ibb.co/1tQxNLwW/28-Toallitas-H-medas-Gato.png"
    },
    {
        "id":29,
        "title":"Cepillo Perro Furminator",
        "price":42000,
        "description":"El mejor cepillo cortador de pelo llego. Ideal para razas muy peludas como pugs",
        "category":"varios",
        "image":"https://i.ibb.co/Jj0CPs9Q/29-Cepillo-Perro-Furminator.png"
    },
    {
        "id":30,
        "title":"Juguete Perro Pollo",
        "price":18000,
        "description":"Juguete de pollo ideal para que tu perrito juegue durante horas",
        "category":"varios",
        "image":"https://i.ibb.co/XkYgXDVb/30-Juguete-Perro-Pollo.png"
    }
]


def create_initial_products(apps, schema_editor):
    # Obtenemos el modelo 'Product' de la app 'products'
    Product = apps.get_model('products', 'Product')
    
    # Evitamos crear duplicados si la migración se corre de nuevo
    existing_titles = list(Product.objects.values_list('title', flat=True))

    print("\n  Populating initial products...") # Mensaje para la consola
    
    products_to_create = []
    for p in MOCK_PRODUCTS:
        if p['title'] not in existing_titles:
            # Creamos la instancia del producto
            # NOTA: Ajusta los campos ('title', 'price', 'description')
            #       para que coincidan 100% con tu 'products/models.py'
            products_to_create.append(
                Product(
                    title=p['title'],
                    price=Decimal(p['price']),
                    description=p['description'],
                    # Si tienes los campos 'category' e 'image' en tu modelo,
                    # puedes descomentar y añadirlos aquí también.
                    category=p['category'], 
                    image=p['image'],
                )
            )
    
    if products_to_create:
        Product.objects.bulk_create(products_to_create)
        print(f"  Created {len(products_to_create)} new products.")
    else:
        print("  Products already exist.")


class Migration(migrations.Migration):

    # Esta migración depende de la anterior (la que creó la tabla Product)
    dependencies = [
        ('products', '0001_initial'), 
    ]

    operations = [
        # Aquí le decimos a Django que ejecute nuestra función
        migrations.RunPython(create_initial_products),
    ]