from django.shortcuts import get_object_or_404, render,  render_to_response
from django.http import HttpResponseRedirect, HttpResponse,HttpResponseBadRequest
from django.template import RequestContext, loader
from .models import Question, Choice,Post,videos
from django.http import Http404
from django.core.urlresolvers import reverse
from django.views import generic
from .forms import PostForm,LoginForm,RegisterForm
from django.core.context_processors import csrf
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.core import serializers
from comments.forms import CommentForm
from django.utils import timezone
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from comments.models import Comment

class IndexView(generic.ListView):
    template_name = 'principal/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pud_date')[:5]

class DetailView(generic.DetailView):
    model = Post
    template_name = 'principal/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'principal/results.html'


def vote(request, question_id):
    p = get_object_or_404(Post, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Post.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'principal/detail.html', {
            'question': p,
            'error_message': "No ha seleccionado ninguna opcion.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('encuesta:index', args=(p.id,)))

#pasos para el blog
def index(request):
    latest_question_list = Post.objects.all()
    
    query=request.GET.get("q")
    if query:
        latest_question_list= latest_question_list.filter(
                Q(titulo__icontains=query)|
                Q(autor__icontains=query)

            ).distinct()
    paginator = Paginator(latest_question_list, 6) # Show 25 contacts per page
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        contacts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        contacts = paginator.page(paginator.num_pages)

    return render(request,'principal/index.html', {"contacts": contacts})




def detail(request, post_id=None):
    instance=get_object_or_404(Post,pk=post_id)
  

    try:
        post = Post.objects.get(pk=post_id)
        cat=post.categoria.all() # Obteniendo las categorias del producto encontrado relacion many to many
        it=Post.objects.all()
        content_type=ContentType.objects.get_for_model(Post)
        #obj_id=instance.id
        initial_data ={
                "content_type": instance.get_content_type,
                "object_id": instance.id


        } 
        form=CommentForm(request.POST or None, initial=initial_data)
        if form.is_valid():
            c_type = form.cleaned_data.get("content_type")
            content_type = ContentType.objects.get(model=c_type)
            obj_id = form.cleaned_data.get('object_id')
            content_data = form.cleaned_data.get("content")
            parent_obj = None
            try:
                    parent_id = int(request.POST.get("parent_id"))
            except:
                    parent_id = None

            if parent_id:
                    parent_qs = Comment.objects.filter(id=parent_id)
                    if parent_qs.exists() and parent_qs.count() == 1:
                            parent_obj = parent_qs.first()

            new_comment, created = Comment.objects.get_or_create(
                            user = request.user,
                            content_type= content_type,
                            object_id = obj_id,
                            content = content_data,
                            parent = parent_obj
                        )


            return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

        comments=instance.comments
       
    except Post.DoesNotExist:
        raise Http404("Post does not exist")
    return render(request, 'principal/detail.html', {'post': post,'categoria':cat,'itera':it,'instance':instance,"comments":comments,"comment_form":form})

#creamos el formulario

def crear(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    if request.method=='POST':
        form=PostForm(request.POST or None, request.FILES or None)

        # verificamos si es valido
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')

    
    else:
        form=PostForm()

      


    return render(request,'principal/crear_post.html',{'form':form})    



def video(request):
   #latest_question_list =  videos.objects.order_by('-creation_date')[:6]
   latest_question_list =  videos.objects.all()
   template = loader.get_template('principal/video.html')
   context = RequestContext(request, {
   'latest_question_list': latest_question_list,
    })
   return HttpResponse(template.render(context))


def encuesta(request):
   template = loader.get_template('principal/encuesta.html')
   context = RequestContext(request)
   return HttpResponse(template.render(context))   


def videodeta(request, video_id):
    try:
        deta = videos.objects.get(pk=video_id)
    except videos.DoesNotExist:
        raise Http404("Videos does not exist")
    return render(request, 'principal/detalle_video.html', {'deta': deta})   


def login_view(request):
    mensaje = ""
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    else:
        if request.method == "POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                next = request.POST['next']
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                usuario = authenticate(username=username,password=password)
                if usuario is not None and usuario.is_active:
                    login(request,usuario)
                    return HttpResponseRedirect(next)
                else:
                    mensaje = "usuario y/o password incorrecto"
        next = request.REQUEST.get('next')
        form = LoginForm()
        ctx = {'form':form,'mensaje':mensaje,'next':next}
        return render_to_response('principal/login.html',ctx,context_instance=RequestContext(request))  
        

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')




#Modulo de busquedas

def search(request):

    # si no es una peticion ajax, devolvemos error 400
    if not request.is_ajax() or request.method != "POST":
        return HttpResponseBadRequest()

    # definimos el termino de busqueda
    q = request.POST['q']

    #verificamos si el termino de busqueda es un documento de identidad
    match = re.match(r'^(?P<titulo>[0-9]{2,})$', q)
    isCI = (False, True)[match != None]

    # generamos la query
    if isCI:
        poste = Post.objects.filter(titulo=match.groupdict()['titulo'])
    else:
        poste = Post.objects.filter(autor=q)

    # seleccionamos las columnas que deseamos obtener para el json
    user_fields = (
        'autor',
        'votes',
        'titulo'
    )

    # to json!
    data = serializers.serialize('json', poste, fields=user_fields)

    # eso es todo por hoy ^^
    return HttpResponse(data, content_type="application/json")


def register_view(request):
    form = RegisterForm()
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password_one = form.cleaned_data['password_one']
            password_two = form.cleaned_data['password_two']
            u = User.objects.create_user(username=usuario,email=email,password=password_one)
            u.save() # Guardar el objeto
            return render_to_response('principal/thanks_register.html',context_instance=RequestContext(request))
        else:
            ctx = {'form':form}
            return  render_to_response('principal/register.html',ctx,context_instance=RequestContext(request))
    ctx = {'form':form}
    return render_to_response('principal/register.html',ctx,context_instance=RequestContext(request))
