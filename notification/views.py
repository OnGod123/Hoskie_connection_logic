from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification

@csrf_exempt
@login_required
def send_connection_request(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        recipient_username = data.get('recipient_username')

        if recipient_username:
            try:
                sender = request.user
                recipient = User.objects.get(username=recipient_username)

                # Create a notification record
                Notification.objects.create(
                    sender=sender,
                    recipient=recipient,
                    message=f"You have a new connection request from {sender.username}"
                )

                # Send WebSocket message to recipient
                channel_layer = get_channel_layer()
                room_name = f"{sender.username}_{recipient_username}"
                room_group_name = f"chat_{room_name}"

                async_to_sync(channel_layer.group_send)(
                    room_group_name,
                    {
                        'type': 'chat_message',
                        'message': f"You have a new connection request from {sender.username}"
                    }
                )

                return JsonResponse({'success': True})
            except User.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Recipient not found'}, status=404)
            except IntegrityError:
                return JsonResponse({'success': False, 'error': 'Notification could not be created'}, status=500)
        return JsonResponse({'success': False, 'error': 'Recipient username not provided'}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)
