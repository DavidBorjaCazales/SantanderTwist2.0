# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import status
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from BuscadorSantaderTwist2 import Buscador


# Create your views here.

class Busqueda(APIView):
    """
    Metodos permitidos GET
    Lista todas las busquedas segun las necesidades de Santander Twist 2.0
    """

    def get(self, request, busqueda, latitud, amplitud ,format=None):
        a=Buscador()
        PrefijosLista=a.Buscar(busqueda)
        a={"Busquedas":PrefijosLista}
        return Response(a)
