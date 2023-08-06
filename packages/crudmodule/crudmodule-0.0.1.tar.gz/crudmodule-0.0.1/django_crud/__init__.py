from rest_framework import serializers


from rest_framework.response import Response


from rest_framework.decorators import api_view
from uritemplate import partial


def crud(app_model, app_serializer):
    @api_view(['GET'])
    def CrudList(request):
        list = app_model.objects.all()
        serializer = app_serializer(list, many=True)
        return Response(serializer.data)
    return CrudList

def crud(app_model, app_serializer):
    @api_view(['GET'])
    def CrudDetail(request, pk):
        detail = app_model.objects.get(id=pk)
        serializer = app_serializer(detail, many=False)
        return Response(serializer.data)
    return CrudDetail

def crud(app_serializer):
    @api_view(['POST'])
    def CrudCreate(request):
        if request.method == "POST":

            serializer = app_serializer(data=request.data)
            
        if serializer.is_valid():
                
            serializer.save()

        return Response(serializer.data)
    return CrudCreate
def crud(app_model, app_serializer):
    @api_view(['PUT'])
    def CrudUpdate(request, pk):
        update = app_model.objects.get(id=pk)
        serializer = app_serializer(instance=update, data=request.data, many=False, partial="True")

        if serializer.is_valid():
            serializer.save()

        return Response(serializer.data)
        
    return CrudUpdate