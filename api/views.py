from wsgiref.util import request_uri
from django.shortcuts import render

from rest_framework.viewsets import ViewSet,ModelViewSet
from rest_framework.response import Response
from api.models import Todos
from api.serializers import RegistrationSerializer, TodoSerializer

from rest_framework.decorators import action

from django.contrib.auth.models import User

from rest_framework import authentication,permissions

class TodosView(ViewSet):
    def list(self,request,*args,**kw):
        qs=Todos.objects.all()
        serializer=TodoSerializer(qs,many=True)
        return Response(data=serializer.data)

    def create(self,request,*args,**kw):
        seralizer=TodoSerializer(data=request.data)
        if seralizer.is_valid():
            seralizer.save()
            return Response(data=seralizer.data)
        else:
            return Response(data=seralizer.errors)


    def retrieve(self,request,*args,**kw):
        id=kw.get("pk")
        qs=Todos.objects.get(id=id)
        serializer=TodoSerializer(qs,many=False)
        return Response(data=serializer.data)


    def destroy(self,request,*args,**kw):
        id=kw.get("pk")
        Todos.objects.get(id=id).delete()
        return Response(data="Deleted")

    def update(self,request,*args,**kw):
        id=kw.get("pk")
        object=Todos.objects.get(id=id)
        serializer=TodoSerializer(data=request.data,instance=object)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)



class TodosModelViews(ModelViewSet):

    #Basic Authentication Implementation.....
    authentication_classes=[authentication.BasicAuthentication]
    permission_classes=[permissions.IsAuthenticated]


    serializer_class=TodoSerializer
    queryset=Todos.objects.all()

#custom method implementation in ModelViewSet
#localhost:8000/api/v1/todos/pending_todos/          get
#localhost:8000/api/v1/todos/completed_todos/          get
#localhost:8000/api/v1/todos/2/mark_as_done/             post


    def  get_queryset(self):
        return Todos.objects.filter(user=self.request.user)

    def create(self,request,*args,**kw):
        serializer=TodoSerializer(data=request.data,context={"user":request.user})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)

    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)
    
#overriding list method for fetching todos created by specific users....
    # def list(self,request,*args,**kw):
    #     qs=Todos.objects.filter(user=request.user)
    #     serializer=TodoSerializer(qs,many=True)
    #     return Response(data=serializer.data)

#overriding create method,request.data will contain the username of the user logged in
    # def create(self,request,*args,**kw):
    #     serializer=TodoSerializer(data=request.data)
    #     if serializer.is_valid():
    #         Todos.objects.create(**serializer.validated_data,user=request.user)
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors)

    

    @action(methods=["GET"],detail=False)
    def pending_todos(self,request,*args,**kw):
        qs=Todos.objects.filter(status=False)
        serializer=TodoSerializer(qs,many=True)
        return Response(data=serializer.data)

    @action(methods=["GET"],detail=False)
    def completed_todos(self,request,*args,**kw):
        qs=Todos.objects.filter(status=True)
        serializer=TodoSerializer(qs,many=True)
        return Response(data=serializer.data)

    @action(methods=["post"],detail=True)     #we are passing data in the url(eg:2),we can put post or get
    def mark_as_done(self,request,*args,**kw):
        id=kw.get("pk")
        object=Todos.objects.get(id=id)
        object.status=True
        object.save()
        serializer=TodoSerializer(object,many=False)
        return Response(data=serializer.data)



class UsersView(ModelViewSet):
    serializer_class=RegistrationSerializer
    queryset=User.objects.all()


    # #for password encryption,override the create method
    # def create(self,request,*args,**kw):
    #     serializer=RegistrationSerializer(data=request.data)
    #     if serializer.is_valid():
    #         usr=User.objects.create_user(**serializer.validated_data)
    #         return Response(data=serializer.data)
    #     else:
    #         return Response(data=serializer.errors)






    

    



