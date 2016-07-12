from django.db import models
from comments.models import Comment
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse



class userProfile(models.Model):
	user 		=	models.OneToOneField(User)
	photo 		=	models.ImageField(upload_to="MultimediaData/Proyecto/",null=True,blank=True)
	telefono	=	models.CharField(max_length=30)
	correo= models.CharField(max_length=50)
	

	def __unicode__(self):
		return self.user.username



class Question(models.Model):
	question_text= models.CharField(max_length=200)
	pud_date = models.DateField('date published')

	def __unicode__(self):
		return self.question_text

	def was_published_recently(self):
		return self.pud_date >=timezone.now() - datetime.timedelta(days=1)
		
class Choice(models.Model):
	question=models.ForeignKey(Question)
	choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)

	def __unicode__(self):
		return self.choice_text

class Category(models.Model):
	name=models.CharField(max_length=200)

	def __unicode__(self):
		return self.name

class Post(models.Model):
	user=models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	autor=models.CharField(max_length=30)
	titulo=models.CharField(max_length=200)
	body=models.TextField()
	categoria=models.ManyToManyField(Category)
	imagen 		= models.ImageField(upload_to="MultimediaData/Proyecto/",null=True,blank=True)
	votes = models.IntegerField(default=0)
	draft = models.BooleanField(default=False)
	publish = models.DateField(auto_now=False, auto_now_add=False)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)


 

	

	def __unicode__(self):
		return self.titulo


	def  get_absolute_url(self):
		#return reverse("encuesta:detail")
		return "/djpython/%s/"%(self.id)



	@property 
	def comments(self):
		instance = self
		qs = Comment.objects.filter_by_instance(instance)
		return qs

	
	@property 
	def get_content_type(self):
	    instance=self
	    content_type = ContentType.objects.get_for_model(instance.__class__)
	    return content_type    	


    

class Comentario(models.Model):
	nombre = models.CharField(max_length=200)
	cuerpo = models.TextField()
	fecha_pub = models.DateTimeField('fecha publicacion')
	post=models.ForeignKey(Post)


	def __unicode__(self):
		return self.nombre

class videos(models.Model):
	
    
	titulo=models.CharField(max_length=200)
	url=models.CharField(max_length=200)
	categoria=models.ForeignKey(Category)
	creation_date=models.DateTimeField(auto_now_add=True)
	votes = models.IntegerField(default=0)
	
    
	def __unicode__(self):
		return self.titulo		


    	  


                    
    






	
	  
	    	

   
