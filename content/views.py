from user.views import *
from content.models import Page
from content.serializer import PageSerializer

@api_view(['PUT', 'GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
@transaction.atomic()
def update_content(request, page):
    authorization = request.headers['Authorization']
    authorization_split = authorization.split(' ')
    payload = jwt.decode(authorization_split[1], settings.SECRET_KEY)
    user = User.objects.get(id=payload['user_id'])
    if not user.is_active:
        return Response({"error": "user status invalid"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        page_search = Page.objects.get(name=page)
    except User.DoesNotExist:
        return Response({"error": "Page not found"}, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'PUT':
        serializer = PageSerializer(data=request.data)
        if serializer.is_valid():
            update = 0
            if "pr_1" in serializer.data:
                page_search.pr_1 = serializer.data['pr_1']
                update = 1
            if "pr_2" in serializer.data:
                page_search.pr_2 = serializer.data['pr_2']
                update = 1
            if "pr_3" in serializer.data:
                update = 1
                page_search.pr_3 = serializer.data['pr_3']
            if "img_1" in serializer.data:
                update = 1
                page_search.img_1 = serializer.data['img_1']
            if "img_2" in serializer.data:
                update = 1
                page_search.img_2 = serializer.data['img_2']
            if "img_3" in serializer.data:
                update = 1
                page_search.img_3 = serializer.data['img_3']
            if update != 0:
                page_search.save()
                page_again = Page.objects.get(name=page)
                simple_page = {
                    "name": page_again.name,
                    "pr_1": page_again.pr_1,
                    "pr_2": page_again.pr_2,
                    "pr_3": page_again.pr_3,
                    "img_1": page_again.img_1,
                    "img_2": page_again.img_2,
                    "img_3": page_again.img_3,
                }
                return Response(simple_page, status=status.HTTP_200_OK)
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        simple_page = {
            "name": page_search.name,
            "pr_1": page_search.pr_1,
            "pr_2": page_search.pr_2,
            "pr_3": page_search.pr_3,
            "img_1": page_search.img_1,
            "img_2": page_search.img_2,
            "img_3": page_search.img_3,
        }
        return Response(simple_page, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
@transaction.atomic()
def get_content(request):
    authorization = request.headers['Authorization']
    authorization_split = authorization.split(' ')
    payload = jwt.decode(authorization_split[1], settings.SECRET_KEY)
    user = User.objects.get(id=payload['user_id'])
    if not user.is_active:
        return Response({"error": "user status invalid"}, status=status.HTTP_400_BAD_REQUEST)
    pages = Page.objects.all()
    list_page = []
    for page in pages:
        simple_page = {
            "name": page.name,
            "pr_1": page.pr_1,
            "pr_2": page.pr_2,
            "pr_3": page.pr_3,
            "img_1": page.img_1,
            "img_2": page.img_2,
            "img_3": page.img_3,
        }
        list_page.append(simple_page)
    return Response(list_page, status=status.HTTP_200_OK)