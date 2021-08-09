from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from webexteamssdk import WebexTeamsAPI
from decouple import config
from .models import UserOwnerSpace
from accounts.models import Profile

def oauth(request):
    if 'code' in request.GET and request.GET.get('state') == config('state'):
        code = request.GET.get('code')
        try:
            api  = WebexTeamsAPI.from_oauth_code(
                client_id     = config('CLIENT_ID'),
                client_secret = config('CLIENT_SECRET'),
                code          = code,
                redirect_uri  = config('REDIRECT_URI')
            )

            request.session['access_token'] = api.access_token
            current_user = Profile.objects.filter(user = request.user).first()
            current_user_webex_emails = api.people.me().emails

            if current_user_webex_emails:
                current_user.webex_email = current_user_webex_emails[0]
                current_user.save()

            messages.success(request, f"You Webex authentication is successful! Webex magic unlocked :)")
            return redirect('home')

        except:
            messages.error(request, f"Something went wrong! Please try again")
            return redirect('home')
            
    else:
        messages.error(request, f"Something went wrong! Please try again")
        return redirect('home')
    pass


def contact_owner(request, owner_id):
    owner = User.objects.get(id = owner_id)
    return render(request, 'webexmint/contact_owner.html',{'owner':owner})


def create_userowner_space(request, owner_id):
    existing_space = UserOwnerSpace.objects.filter(creator_id = request.user.id).first()

    # space already exists
    if existing_space:   
        messages.info(request, f"You already have an open space. Please delete existing space to create new one.")
        return render(request, 'webexmint/space.html', {'spaceId': existing_space.roomId})

    # space not exists, create new space
    else:       
        try:         
            owner= User.objects.get(id = owner_id)
            owner_username = owner.username
            owner_webex_email = owner.webex_email
            space_title = f"{request.user.username} - {owner_username} (CarGear space)"
            api = WebexTeamsAPI(access_token= request.session.get('access_token'))
            space = api.rooms.create(title= space_title)
            UserOwnerSpace.objects.create(creator = request.user, title = space_title, roomId = space.id, owner = owner)
            api.memberships.create(roomId= space.id, personEmail= owner_webex_email)
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
        return redirect('home')


def my_spaces(request):
    if request.session.get('access_token'):
        try:
            spaceset = UserOwnerSpace.objects.filter(creator = request.user) | UserOwnerSpace.objects.filter(owner = request.user) 
            if spaceset:
                userownerspace = spaceset.first()
                webex_space = WebexTeamsAPI(access_token= request.session.get('access_token')).rooms.get(roomId= userownerspace.roomId)
                return render(request, 'webexmint/my_spaces.html',{'webex_space': webex_space, 'created_by' : userownerspace.creator.username})
            else:
                messages.info(request, f"No spaces available")
                return redirect('home')
        
        except:
            messages.error(request, f'Something went wrong! Please retry again.')
            return redirect('home')

    else:
        return redirect('oauth')


def visit_space(request):
    roomId = request.POST.get('roomId')
    return render(request, 'webexmint/space.html', {'spaceId' : roomId})