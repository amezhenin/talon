from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from talon.models import Todo

from rest_framework import viewsets, serializers, permissions, filters

import logging
log = logging.getLogger(__name__)


def ping(request):
    '''
    Diagnostic request.
    '''
    log.info('ping')
    return HttpResponse("pong")


@login_required
def dashboard(request):
    """
    User can view and edit his Todos in dashboard. Login screen leads to this
    view.
    """
    return render(request, 'dashboard.html')


def index(request):
    """
    Index page for application
    """

    if request.user.is_authenticated() and request.user.is_active:
        return HttpResponseRedirect('/dashboard')

    return render(request, 'index.html')


#===============================================================================
# API
#===============================================================================

class TodoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Todo
        fields = ('id',
                  'url',
                  'completed',
                  'priority',
                  'created',
                  'due_date',
                  'text')


class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `user` attribute.
    """

    def has_object_permission(self, request, view, obj):
        """
        Use foreign key to determine authorship
        """
        return obj.user == request.user


class TodoViewSet(viewsets.ModelViewSet):
    """
    Main API view for Todos
    """
    model = Todo
    serializer_class = TodoSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    filter_backends = (filters.OrderingFilter, filters.DjangoFilterBackend)
    filter_fields = ('completed',)

    def get_queryset(self):
        """
        Filter Todos when listing all avaliable posts
        """
        return Todo.objects.filter(user=self.request.user)

    def pre_save(self, obj):
        """
        Ensure that Todo will be saved with correct author. We don't fill this
        field when calling API functions
        """
        obj.user = self.request.user
