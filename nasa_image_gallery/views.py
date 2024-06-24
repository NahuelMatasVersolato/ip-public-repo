# capa de vista/presentación
# si se necesita algún dato (lista, valor, etc), esta capa SIEMPRE se comunica con services_nasa_image_gallery.py

from django.shortcuts import redirect, render
from .layers.services import services_nasa_image_gallery 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# función que invoca al template del índice de la aplicación.
def index_page(request):
    return render(request, 'index.html')

# auxiliar: retorna 2 listados -> uno de las imágenes de la API y otro de los favoritos del usuario.
def getAllImagesAndFavouriteList(request, page_number=1, images_per_page=3):
    images = services_nasa_image_gallery.getAllImages()
    favourite_list = []
    
    if request.user.is_authenticated:
        favourite_list = services_nasa_image_gallery.getAllFavouritesByUser(request)
    
    # Implementa la paginación para las imágenes
    paginator = Paginator(images, images_per_page)
    
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)  # Si el número de página no es un entero, muestra la primera página
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)  # Si la página está fuera de rango, muestra la última página
    
    return page_obj, favourite_list


def home(request):
    page_number = request.GET.get('page', 1)  # Por defecto muestra la primera página
    images_per_page = 3  # Cantidad de imágenes por página, puedes ajustarla según tus necesidades
    
    images_page, favourite_list = getAllImagesAndFavouriteList(request, page_number, images_per_page)
    
    return render(request, 'home.html', {
        'images': images_page,
        'favourite_list': favourite_list
    })

# función utilizada en el buscador.
def search(request):
    if request.method == 'POST':
        search_msg = request.POST.get('query', '')

        if search_msg.strip():  # Verifica que haya texto de búsqueda
            images = services_nasa_image_gallery.getAllImages(input=search_msg)
            favourite_list = []
            if request.user.is_authenticated:
                favourite_list = list(request.user.favourite_images.all())
            return render(request, 'home.html', {'images': images})
        else:
            # Si no se ingresa ningún texto, podrías redirigir o manejar el caso de otra manera
            return render(request, 'home.html', {'images': [], 'favourite_list': []})

    # Maneja el caso de otro método HTTP (GET) si es necesario
    return render(request, 'home.html', {'images': [], 'favourite_list': []})

# las siguientes funciones se utilizan para implementar la sección de favoritos: traer los favoritos de un usuario, guardarlos, eliminarlos y desloguearse de la app.
@login_required
def getAllFavouritesByUser(request):
    favourite_list = []
    return render(request, 'favourites.html', {'favourite_list': favourite_list})


@login_required
def saveFavourite(request):
    pass


@login_required
def deleteFavourite(request):
    pass


@login_required
def exit(request):
    pass
