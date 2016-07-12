from rest_framework.serializers import  ModelSerializer


from principal.models import Post

class PostSerializer(ModelSerializer):
	class Meta:
		model=Post
		fields=[
             'autor',
             'titulo',
             'body',
             'publish',
             'updated',

		]



class PostDetailSerializer(ModelSerializer):
	class Meta:
		model=Post
		fields=[
			 'id',
             'autor',
             'titulo',
             'body',
             'publish',
             'updated',

		]
