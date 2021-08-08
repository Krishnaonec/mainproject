from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib import messages
from webexteamssdk import WebexTeamsAPI
from decouple import config
from .models import UserOwnerSpace

def oauth(request):
    # if 'code' in request.GET and request.GET.get('state') == config('state'):
    #     code = request.GET.get('code')
    #     api  = WebexTeamsAPI.from_oauth_code(
    #         client_id     = config('client_id'),
    #         client_secret = config('client_secret'),
    #         code          = code,
    #         redirect_uri  = config('redirect_uri')
    #     )

    # request.session['access_token'] = api.access_token
    request.session['access_token'] = 'YmI5OTU3OGQtZmRmOC00NTljLWFhY2YtM2RkZjRmMGE3OGE3NGY2NjVkYzEtY2E3_P0A1_72fd5250-f4c5-4261-ba8d-0385199b4781'
    messages.success(request, f"You webex authentication is successful! Now you can contact onwers.")
    return redirect('cars_catalog')


def contact_owner(request, owner_id):
    owner = User.objects.get(id = owner_id)
    return render(request, 'webexmint/contact_owner.html',{'owner':owner})


def create_userowner_space(request, owner_id):
    existing_space = UserOwnerSpace.objects.filter(creator_id = request.user.id).first()

    # space already exists
    if existing_space:   
        return render(request, 'webexmint/space.html', {'spaceId': existing_space.roomId})

    # space not exists, create new space
    else:       
        try:         
            owner= User.objects.get(id = owner_id)
            owner_username = owner.username
            owner_email = owner.email
            space_title = f"{request.user.username} - {owner_username} (CarGear space)"
            api = WebexTeamsAPI(access_token= request.session.get('access_token'))
            space = api.rooms.create(title= space_title)
            UserOwnerSpace.objects.create(creator = request.user, title = space_title, roomId = space.id, owner = owner)
            api.memberships.create(roomId= space.id, personEmail= owner_email)
            api.messages.create(roomId = space.id, text=f"Hello {owner.first_name + owner.last_name}")
            messages.success(request, f"{space_title} space is created. Enjoy the interaction.")
            return render(request, 'webexmint/space.html', {'spaceId': space.id})
        except:
            messages.error(request, f'Something went wrong! Please retry again.')
            return redirect('cars_catalog', )

def delete_space(request):
    try:
        roomId = request.POST.get('roomId')
        api = WebexTeamsAPI(access_token= request.session.get('access_token'))
        api.rooms.delete(roomId= roomId)
        messages.success(request, f"We have deleted the space as you said :)")
        UserOwnerSpace.objects.get(roomId = roomId).delete()
        return redirect('home')
    except:
        messages.error(request, f"Something went wrong! Please try again.")
        return redirect('cars_catalog')


def my_spaces(request):
    try:
        spaceset = UserOwnerSpace.objects.filter(creator = request.user) | UserOwnerSpace.objects.filter(owner = request.user) 
        userownerspace = spaceset.first()
        webex_space = WebexTeamsAPI(access_token= request.session.get('access_token')).rooms.get(roomId= userownerspace.roomId)
        return render(request, 'webexmint/my_spaces.html',{'webex_space': webex_space, 'created_by' : userownerspace.creator.username})

    except UserOwnerSpace.DoesNotExist:
        messages.warning(request, f"No spaces available")
        return redirect('home')
    
    except:
        messages.error(request, f'Something went wrong! Please retry again.')
        return redirect('home')


def visit_space(request):
#     try:
#         roomId = request.POST.get('roomId')
#         api = WebexTeamsAPI(access_token = request.session.get('access_token'))
#         room = api.rooms.get(roomId = roomId)
#         return render(request, 'webexmint/space.html', {'spaceId' : room.id})
#     except:
#         messages.error(request, f"Something went wrong! Please retry again.")
#         return redirect('home')
    pass