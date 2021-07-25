from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.permissions import IsAuthenticatedOrReadOnly
from News.models import NewsItem, Story, Job
from .serializers import NewsItemSerializer, StorySerializer, JobSerializer


class NewsItemApiView(ModelViewSet):
    http_method_names = ['get', 'head']
    serializer_class = NewsItemSerializer
    queryset = NewsItem.objects.all()


class StoryApiView(ModelViewSet):
    # permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = StorySerializer
    queryset = Story.objects.all()
    http_method_names = ['get', 'post', 'head', 'put', 'delete']

    def update(self, request, pk=None, *args, **kwargs):
        """
        Checks if Story was created manually before updating
        :param request:
        :param pk:
        :param args:
        :param kwargs:
        :return:
        """
        item = self.get_object()
        if item.fetched:
            return Response({"message": "Data Was Fetched"}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

    def destroy(self, request, pk=None, *args, **kwargs):
        """
        Checks if Story was created manually before deleting
        :param request:
        :param pk:
        :param args:
        :param kwargs:
        :return:
        """
        item = self.get_object()
        if item.fetched:
            return Response({"message": "Data Was Fetched"}, status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(item)
        return Response(status=status.HTTP_204_NO_CONTENT)


class JobApiView(ModelViewSet):
    # permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = JobSerializer
    queryset = Job.objects.all()
    http_method_names = ['get', 'post', 'head', 'put', 'delete']

    def update(self, request, pk=None, *args, **kwargs):
        """
            Checks if Job was created manually before updating
            :param request:
            :param pk:
            :param args:
            :param kwargs:
            :return:
            """
        item = self.get_object()
        if item.fetched:
            return Response({"message": "Data Was Fetched"}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

    def destroy(self, request, pk=None, *args, **kwargs):
        """
            Checks if Job was created manually before deleting
            :param request:
            :param pk:
            :param args:
            :param kwargs:
            :return:
            """
        item = self.get_object()
        if item.fetched:
            return Response({"message": "Data Was Fetched"}, status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(item)
        return Response(status=status.HTTP_204_NO_CONTENT)
