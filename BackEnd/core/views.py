from collections import OrderedDict
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from rest_framework.views import APIView

from core.models import Client
from core.serializers import ClientSerializer

class ClientApi(APIView):
    '''
    CRUD operations API on Client models.
    '''

    @staticmethod
    def search_client(id:int=None, name:str=None):
        '''
        search_client(id:int, name:str) -> OrderedDict OR empty QuerySet

        search for a client, if id is pass as an argument then the search will be performed based in this ID, even if the client name is also passed as an argument
        '''
    
        if id:
            search = Client.objects.filter(id=id)
        
        elif name:
            search = Client.objects.filter(name=name)

        else:
            search = Client.objects.none()

        return search

    @staticmethod
    def create_client(name:str):
        '''
        create_client(str) -> tuple[Client, str] 
        
        create a register for the Client model on the DB, if there's already a client with the given name then return a string indicating the error. Otherwise returns None as the element of the tuple
        '''
        client, error = None, None

        try:
            Client.objects.get(name=name)
            error = 'client name already exists'
        except Client.DoesNotExist:
            client = Client.objects.create(name= name)

        return client, error

    def update_client(id:int=None, name:str=None):
        '''
        update_client(id:int, name:str) -> tuple[Client, str]:

        Update the name of the client with the given ID
        '''
        client, error = None, None
        client = ClientApi.search_client(id=id, name=name)[0]
        
        if client:
            client.name = name
            client.save()
        else:
            error = 'Client not found'
        
        return client, error

    def get(self, request):
        response = dict()
        query_params = request.GET.copy()
        
        search = ClientApi.search_client(
            id = query_params.get('id'),
            name = query_params.get('name')
        )

        response['data'] = ClientSerializer(search, many=True).data
        return JsonResponse(response)

    def post(self, request) -> JsonResponse:
        json_data = dict()
        json_data['success'] = False
        json_data['error'] = None
        json_data['data'] = None

        error = None
        params = request.data
        if 'name' in params:
            client, error = ClientApi.create_client(name=params['name'])
        else:
            error = 'invalid parameters'
        

        if not error:
            json_data['data'] = ClientSerializer(client).data

        else:
            json_data['error'] = error

        json_data['success'] = bool(json_data['data'])

        return JsonResponse(json_data)

    def put(self, request) -> JsonResponse:
        json_data = dict()
        json_data['success'] = False
        json_data['error'] = None
        json_data['data'] = None

        error = None
        params = request.data
        if 'name' in params and 'id' in params:
            client, error = ClientApi.update_client(id=params.get('id'), name=params.get('name'))
        else:
            error = 'invalid parameters'
        

        if not error:
            json_data['data'] = ClientSerializer(client).data

        else:
            json_data['error'] = error

        json_data['success'] = bool(json_data['data'])

        return JsonResponse(json_data)