from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.views.decorators.http import require_POST
import os
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from .models import Categoria, Dibujos,MisSolicitudesUsuario 
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.text import slugify
from datetime import datetime
from django.http import JsonResponse
def inicio(request):
    return render(request, 'draw_app/inicio.html')

def contacto(request):
    return render(request, 'draw_app/contacto.html')

def sobre_mi(request):  
    return render(request, 'draw_app/sobre_mi.html')

def terminos(request):
    print(os.getcwd())  
    return render(request, 'draw_app/terminos.html')
IMAGE_UPLOAD_PATH1 = r"C:\Users\Shent\Escritorio\P_draw\draw_app\static\formulario"
IMAGE_UPLOAD_PATH = r"C:\Users\Shent\Escritorio\P_draw\draw_app\static\img"
def portafolio(request):
    categorias = Categoria.objects.all()  # Obtener todas las categorías
    dibujos = Dibujos.objects.all()
    # Lógica para obtener dibujos o cualquier otra información necesaria
    return render(request, 'draw_app/portafolio.html', {'categorias': categorias, 'dibujos': dibujos})
def portafolio_simple(request):
    categorias = Categoria.objects.all()  # Obtener todas las categorías
    dibujos = Dibujos.objects.all()  # Obtener todos los dibujos
    return render(request, 'draw_app/portafolio_images.html', {'categorias': categorias, 'dibujos': dibujos})

def precios(request):
    categorias = Categoria.objects.all()  # Obtener todas las categorías
    dibujos = Dibujos.objects.all()
    return render(request, 'draw_app/precios.html', {'categorias': categorias, 'dibujos': dibujos})

def precios_simple(request):
    categorias = Categoria.objects.all()  # Obtener todas las categorías
    dibujos = Dibujos.objects.all()  # Obtener todos los dibujos
    return render(request, 'draw_app/precios_images.html', {'categorias': categorias, 'dibujos': dibujos})


User = get_user_model()  # Obtener el modelo de usuario actual

User = get_user_model()  # Obtener el modelo de usuario actual

def registro(request):
    if request.method == 'POST':
        username = request.POST.get('username')  # Obtener el nombre de usuario del formulario
        email = request.POST.get('email')
        password = request.POST.get('password')
        repeat_password = request.POST.get('repeat-password')

        # Validar que las contraseñas coincidan
        if password != repeat_password:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, 'draw_app/registro.html', {})

        # Verificar si el nombre de usuario ya está registrado
        if User.objects.filter(username=username).exists():
            messages.error(request, "Este nombre de usuario ya está en uso.")
            return render(request, 'draw_app/registro.html', {})

        # Verificar si el correo electrónico ya está registrado
        if User.objects.filter(email=email).exists():
            messages.error(request, "Este correo electrónico ya está registrado.")
            return render(request, 'draw_app/registro.html', {})

        # Crear el nuevo usuario usando el nombre de usuario y correo electrónico proporcionados
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Usuario creado exitosamente. Ahora puedes iniciar sesión.")
            return redirect('login')  # Cambia 'login' a la URL de inicio de sesión
        except Exception as e:
            messages.error(request, f"Error al crear el usuario: {str(e)}")
            return render(request, 'draw_app/registro.html', {})

    return render(request, 'draw_app/registro.html', {})
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Obtener el modelo de usuario
        User = get_user_model()
        
        # Intentar encontrar el usuario usando el correo electrónico
        try:
            user = User.objects.get(email=email)
            # Autenticar usando el nombre de usuario interno (pero invisible para el usuario) y la contraseña
            user = authenticate(request, username=user.username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Has iniciado sesión exitosamente.")
                return redirect('inicio')
            else:
                messages.error(request, "Credenciales inválidas. Intenta nuevamente.")
        except User.DoesNotExist:
            messages.error(request, "No se encontró ningún usuario con ese correo electrónico.")

    return render(request, 'draw_app/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "Has cerrado sesión exitosamente.")
    return redirect('login')  # Redirigir a la página de inicio de sesión

@csrf_exempt  # Solo si no estás usando CSRF en esta vista
def opciones_categorias(request):
    categorias = Categoria.objects.all()
    if request.method == 'POST':
        nombre_categoria = request.POST.get('nombre_categoria')
        descripcion_categoria = request.POST.get('descripcion_categoria')
        action = request.POST.get('action')
        categoria_id = request.POST.get('categoria_id')

        if action == 'add':
            if Categoria.objects.filter(nombre_categoria=nombre_categoria).exists():
                error_message = "Ya existe una categoría con ese nombre."
                return render(request, 'draw_app/opciones_categorias.html', {'error': error_message, 'categorias': categorias})
            try:
                categoria = Categoria(
                    nombre_categoria=nombre_categoria,
                    descripcion_categoria=descripcion_categoria
                )
                categoria.save()
                return redirect('opciones_categorias')

            except ValueError:
                error_message = "El precio debe ser un número válido."
                return render(request, 'draw_app/opciones_categorias.html', {'error': error_message, 'categorias': categorias})
    

        elif action == 'modify':
            try:
                categoria = Categoria.objects.get(id=categoria_id)
                
                # Actualizar solo si hay nuevos valores
                if nombre_categoria:
                    categoria.nombre_categoria = nombre_categoria
                if descripcion_categoria:
                    categoria.descripcion_categoria = descripcion_categoria
                
                categoria.save()
                return redirect('opciones_categorias')

            except Categoria.DoesNotExist:
                error_message = "La categoría no existe."
                return render(request, 'draw_app/opciones_categorias.html', {'error': error_message, 'categorias': categorias})


        elif action == 'delete':
                    try:
                        categoria = Categoria.objects.get(id=categoria_id)
                        
                        # Obtener todos los dibujos relacionados con la categoría
                        dibujos = Dibujos.objects.filter(categoria=categoria)
                        
                        # Eliminar cada dibujo y su imagen del sistema de archivos
                        for dibujo in dibujos:
                            # Obtener el nombre del archivo de imagen y quitar el prefijo 'img/'
                            image_name = dibujo.imagen.name.replace('img/', '')  # Eliminar 'img/' del nombre
                            image_path = os.path.join(IMAGE_UPLOAD_PATH, image_name)  # Ruta completa
                            
                            if os.path.isfile(image_path):
                                os.unlink(image_path)  # Eliminar el archivo de imagen
                            dibujo.delete()  # Eliminar el dibujo de la base de datos
                        
                        # Finalmente, eliminar la categoría
                        categoria.delete()
                        
                        return redirect('opciones_categorias')

                    except Categoria.DoesNotExist:
                        error_message = "La categoría no existe."
                        return render(request, 'draw_app/opciones_categorias.html', {'error': error_message, 'categorias': categorias})

    return render(request, 'draw_app/opciones_categorias.html', {'categorias': categorias})
def get_categoria(request, categoria_id):
    try:
        categoria = Categoria.objects.get(id=categoria_id)
        data = {
            'nombre_categoria': categoria.nombre_categoria,
            'descripcion_categoria': categoria.descripcion_categoria,
        }
        return JsonResponse(data)
    except Categoria.DoesNotExist:
        return JsonResponse({'error': 'Categoría no encontrada'}, status=404)

def agregar_categoria(request):
    # Aquí puedes añadir la lógica de la vista, si es necesario
    return render(request, 'agregar_categoria.html')

def modificar_categoria(request):
    # Aquí va la lógica de la vista
    return render(request, 'modificar_categoria.html')


@login_required
def opcionessolicitudes(request):
    usuarios = User.objects.all()  # Cargar usuarios
    solicitudes = MisSolicitudesUsuario.objects.all()  # Cargar todas las solicitudes
    return render(request, 'draw_app/opcionessolicitudes.html', {
        'usuarios': usuarios,
        'solicitudes': solicitudes,
    })



@login_required
def actualizar_solicitud(request):
    if request.method == 'POST':
        solicitud_id = request.POST.get('solicitud_id')
        solicitud = get_object_or_404(MisSolicitudesUsuario, id=solicitud_id)

        # Comprobación si se presionó el botón de eliminar
        if 'delete' in request.POST:
            # Verificar y eliminar el archivo de referencia si existe
            if solicitud.referencia:
                image_name = solicitud.referencia.name.replace('img/', '')
                image_path = os.path.join(IMAGE_UPLOAD_PATH1, image_name)
                if os.path.isfile(image_path):
                    os.remove(image_path)
                    messages.info(request, f"Documento '{image_name}' eliminado con éxito.")

            # Eliminar la solicitud
            solicitud.delete()
            messages.success(request, "La solicitud ha sido eliminada.")
            return redirect('opcionessolicitudes')
        
        # Código para actualizar la solicitud si se presionó el botón "Aceptar"
        else:
            estado = request.POST.get('estado')
            precio = request.POST.get('precio')
            
            # Actualizar los campos de la solicitud
            solicitud.estado = estado
            solicitud.precio_total = precio
            solicitud.save()
            
            messages.success(request, "La solicitud ha sido actualizada.")
            return redirect('opcionessolicitudes')

    # Mensaje de error si no es una solicitud POST válida
    messages.error(request, "No se pudieron realizar los cambios.")
    return redirect('opcionessolicitudes')
def solicitudes(request):
    # lógica para la vista de solicitudes
    return render(request, 'draw_app/solicitudes.html')


def administrar_dibujos(request):
    categorias = Categoria.objects.all()  # Obtener todas las categorías
    dibujos = Dibujos.objects.all()  # Obtener todos los dibujos

    if request.method == 'POST':
        nombre_dibujo = request.POST.get('nombre_dibujo')
        categoria_id = request.POST.get('categoria_id')
        imagen = request.FILES.get('imagen')  # Obtener el archivo de imagen

        # Validar si la categoría existe
        if not Categoria.objects.filter(id=categoria_id).exists():
            error_message = "La categoría seleccionada no existe."
            return render(request, 'draw_app/administrar_dibujos.html', {'error': error_message, 'categorias': categorias, 'dibujos': dibujos})

        # Cambiar el nombre del archivo a nombre_dibujo.extensión
        file_extension = os.path.splitext(imagen.name)[1]  # Obtener la extensión del archivo (ej. .jpg)
        new_image_name = f"{nombre_dibujo}{file_extension}"  # Crear un nuevo nombre para la imagen
        
        # Guardar la imagen en la ruta deseada con el nuevo nombre
        image_path = os.path.join(IMAGE_UPLOAD_PATH, new_image_name)  # Ruta completa donde se guardará la imagen
        
        with open(image_path, 'wb+') as destination:
            for chunk in imagen.chunks():
                destination.write(chunk)

        # Guardar el nuevo dibujo usando el campo relacionado correctamente
        dibujo = Dibujos(nombre_dibujo=nombre_dibujo, categoria_id=categoria_id)
        dibujo.imagen.name = f'img/{new_image_name}'  # Asignar el nuevo nombre al campo imagen del modelo
        dibujo.save()
        
        return redirect('administrar_dibujos')  # Redirigir a la misma página después de guardar

    return render(request, 'draw_app/administrar_dibujos.html', {'categorias': categorias, 'dibujos': dibujos})


@csrf_exempt  # Solo si no estás usando CSRF en esta vista
def eliminar_categoria(request, categoria_id):
    try:
        # Obtener la categoría a eliminar
        categoria = get_object_or_404(Categoria, id=categoria_id)

        # Obtener todos los dibujos relacionados con la categoría
        dibujos = Dibujos.objects.filter(categoria=categoria)

        # Eliminar cada dibujo y su imagen del sistema de archivos
        for dibujo in dibujos:
            # Obtener el nombre del archivo de imagen usando nombre_dibujo
            image_name = f"{dibujo.nombre_dibujo}.png"  # Cambia esto según la extensión real de tus imágenes
            image_path = os.path.join(IMAGE_UPLOAD_PATH, image_name)
            print(f"Intentando eliminar la imagen: {image_path}")  # Mensaje de depuración
            # Eliminar el archivo de imagen si existe
            if os.path.isfile(image_path):
                try:
                    os.unlink(image_path)  # Usar unlink para eliminar la imagen del sistema de archivos
                    print(f"Imagen eliminada: {image_path}")  # Mensaje de éxito
                except Exception as e:
                    print(f"Error al eliminar la imagen {image_path}: {e}")  # Manejo de errores si falla la eliminación
            else:
                print(f"La imagen no existe: {image_path}")  # Mensaje si el archivo no se encuentra

            # Eliminar el dibujo de la base de datos
            dibujo.delete()

        # Finalmente, eliminar la categoría
        categoria.delete()

        return JsonResponse({'success': True})
    except Categoria.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Categoría no encontrada.'}, status=404)
def opciones_estilos(request):
    return render(request, 'draw_app/opciones_estilos.html')
@login_required
def formulario(request):
    if request.method == 'POST':
        categoria_id = request.POST.get('categoria')
        tipo_comision = request.POST.get('tipo_comision')
        descripcion = request.POST.get('descripcion')
        referencia = request.FILES.get('referencia')  # Obtener la imagen subida

        # Validar que la categoría exista
        try:
            categoria = Categoria.objects.get(id=categoria_id)
        except Categoria.DoesNotExist:
            messages.error(request, "La categoría seleccionada no es válida.")
            return redirect('formulario')
        referencia_path = ""
        if referencia:

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            file_extension = os.path.splitext(referencia.name)[1]
            new_image_name = f"{slugify(tipo_comision)}_{timestamp}{file_extension}"
            image_path = os.path.join(IMAGE_UPLOAD_PATH1, new_image_name)
            

            with open(image_path, 'wb+') as destination:
                for chunk in referencia.chunks():
                    destination.write(chunk)


            referencia_path = f'img/{new_image_name}'


        solicitud = MisSolicitudesUsuario(
            usuario=request.user,
            categoria=categoria,
            estado='en_espera',
            descripcion=descripcion,
            referencia=referencia_path  # Guardar la ruta relativa de la imagen en la base de datos
        )
        solicitud.save()

        messages.success(request, "Tu solicitud ha sido enviada exitosamente.")
        return redirect('mi_perfil')

    # Obtener y enviar las categorías al template
    categorias = Categoria.objects.all()
    return render(request, 'draw_app/formulario.html', {'categorias': categorias})

def eliminar_dibujo(request, dibujo_id):
    if request.method == 'DELETE':
        try:
            dibujo = get_object_or_404(Dibujos, id=dibujo_id)

            # Obtener solo el nombre del archivo de imagen
            image_name = os.path.basename(dibujo.imagen.name)  # Extrae solo el nombre del archivo
            image_path = os.path.join(IMAGE_UPLOAD_PATH, image_name)  # Construir la ruta completa

            # Eliminar el archivo de imagen si existe
            if os.path.isfile(image_path):
                os.unlink(image_path)

            # Eliminar el dibujo de la base de datos
            dibujo.delete()

            return JsonResponse({'success': True})
        except Exception as e:
            print(f"Error: {str(e)}")  # Imprimir el error en la consola del servidor para depuración
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)
@login_required
def mi_perfil(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # Obtener datos del formulario
            username = request.POST.get('username')
            email = request.POST.get('email')

            # Validar que el nombre de usuario y el correo no estén vacíos
            if username and email:
                request.user.username = username
                request.user.email = email
                request.user.save()
                messages.success(request, 'Perfil actualizado correctamente.')
            else:
                messages.error(request, 'Por favor, completa ambos campos.')

            return redirect('mi_perfil')  # Redirige a la misma vista después de actualizar

        # Renderiza la página de perfil con los datos del usuario
        return render(request, 'draw_app/mi_perfil.html')

    # Redirige a la página de login si el usuario no está autenticado
    return redirect('login')

@login_required
def mis_solicitudes(request):
    solicitudes = MisSolicitudesUsuario.objects.filter(usuario=request.user)
    return render(request, 'draw_app/mis_solicitudes.html', {'solicitudes': solicitudes})



@login_required
def eliminar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(MisSolicitudesUsuario, id=solicitud_id, usuario=request.user)
    if solicitud.estado in ['en_espera', 'rechazado']:
        # Verificar si la solicitud tiene una referencia y si el archivo existe
        if solicitud.referencia:
            # Extraer solo el nombre del archivo sin el prefijo 'img/'
            image_name = solicitud.referencia.name.replace('img/', '')
            image_path = os.path.join(IMAGE_UPLOAD_PATH1, image_name)  # Construir la ruta completa

            if os.path.isfile(image_path):  # Verificar si el archivo existe en el sistema
                os.remove(image_path)  # Eliminar el archivo

        solicitud.delete()
        messages.success(request, "La solicitud ha sido eliminada exitosamente.")
    else:
        messages.error(request, "No puedes eliminar una solicitud que está en proceso o finalizada.")
    
    return redirect('mis_solicitudes')


def eliminar_solicitud1(request, solicitud_id):
    solicitud = get_object_or_404(MisSolicitudesUsuario, id=solicitud_id, usuario=request.user)
    
    if solicitud.referencia:
        image_name = solicitud.referencia.name.replace('img/', '')
        image_path = os.path.join(IMAGE_UPLOAD_PATH1, image_name)
        
        if os.path.isfile(image_path):
            os.remove(image_path)
    
    solicitud.delete()
    messages.success(request, "La solicitud ha sido eliminada exitosamente.")
    
    return redirect('mis_solicitudes')
@login_required
def obtener_correo_usuario(request):
    usuario_id = request.GET.get('usuario_id')
    try:
        usuario = User.objects.get(id=usuario_id)
        return JsonResponse({'correo': usuario.email})
    except User.DoesNotExist:
        return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
@login_required
def descargar_referencia(request, solicitud_id):
    # Obtener la solicitud por ID
    solicitud = get_object_or_404(MisSolicitudesUsuario, id=solicitud_id)

    # Verificar si existe una referencia de archivo
    if solicitud.referencia:
        # Construir la ruta completa del archivo
        image_name = solicitud.referencia.name.replace('img/', '')
        image_path = os.path.join(IMAGE_UPLOAD_PATH1, image_name)

        # Verificar si el archivo existe
        if os.path.isfile(image_path):
            with open(image_path, 'rb') as file:
                response = HttpResponse(file.read(), content_type="application/octet-stream")
                response['Content-Disposition'] = f'attachment; filename="{image_name}"'
                return response
        else:
            raise Http404("El archivo de referencia no existe.")
    else:
        raise Http404("No hay archivo de referencia para esta solicitud.")