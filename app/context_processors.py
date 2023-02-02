from app.forms import SubscribeForm


def subscribe_to_base(request):
    subscribe_form = SubscribeForm()
    subscribe_successful = None
    log_in = request.session.get('log_in', False)
    username = request.session.get('username', '')

    if request.POST:
            subscribe = SubscribeForm(request.POST)
            if subscribe.is_valid():
                subscribe.save()
                subscribe_successful = 'subscribe_successfully'
                subscribe_form = SubscribeForm() 
    
    return {'subscribe_form': subscribe_form, 'subscribe_successful': subscribe_successful, 'log_in':log_in, 'username': username}




