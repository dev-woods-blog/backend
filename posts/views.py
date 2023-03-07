from django.shortcuts import get_list_or_404, get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import Post, Category
from .serializers import PostSerializer, CategoryListSerializer

@api_view(['GET'])
def post_list(request):
    currentPage = request.GET.get('currentPage', None)
    pageSize = request.GET.get('pageSize', None)

    currentPage = 0 if currentPage == None else int(currentPage)
    pageSize = 0 if pageSize == None else int(pageSize)

    posts = get_list_or_404(Post)
    if currentPage > 0 and pageSize > 0:
       
        start = (currentPage - 1) * pageSize
        end = currentPage * pageSize
        filteredPosts = posts[start:end]
        serializer = PostSerializer(filteredPosts, many=True)
    else:
        serializer = PostSerializer(posts, many=True)

    response = {
            'list': serializer.data,
            'currentPage': currentPage,
            'pageSize': pageSize,
            'totalPages': 1 if currentPage <= 0 or pageSize <= 0 else len(posts) // pageSize
        }
    return Response(response)

@api_view(['GET'])
def post_list_by_category(request, categoryId):
    currentPage = request.GET.get('currentPage', None)
    pageSize = request.GET.get('pageSize', None)

    currentPage = 0 if currentPage == None else int(currentPage)
    pageSize = 0 if pageSize == None else int(pageSize)

    posts = Post.objects.filter(categoryId=categoryId)

    if currentPage > 0 and pageSize > 0:
       
        start = (currentPage - 1) * pageSize
        end = currentPage * pageSize
        filteredPosts = posts[start:end]
        serializer = PostSerializer(filteredPosts, many=True)
    else:
        serializer = PostSerializer(posts, many=True)

    response = {
            'list': serializer.data,
            'currentPage': currentPage,
            'pageSize': pageSize,
            'totalPages': 1 if currentPage <= 0 or pageSize <= 0 else len(posts) // pageSize
        }
    return Response(response)

@api_view(['GET'])
def detail_post(request, postId):

    post = get_object_or_404(Post, pk=postId)

    serializer = PostSerializer(post)
    return Response(serializer.data)

@api_view(['GET'])
def category_list(request):
    categories = get_list_or_404(Category)
    serializer = CategoryListSerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_category(request):
    serializer = CategoryListSerializer(data=request.data)
    
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def update_delete_category(request, categoryId):
    category = get_object_or_404(Category, pk=categoryId)

    if request.method == 'PUT':
        serializer = CategoryListSerializer(category, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        category.delete()
        childCategories = Category.objects.filter(parentId=categoryId)
        for category in childCategories:
            category.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_post(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

@api_view(['PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def update_delete_post(request, postId):
    post = get_object_or_404(Post, pk=postId)

    if request.method == 'PUT':
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        post.delete()
        return Response(status=status.HTTP_200_OK)