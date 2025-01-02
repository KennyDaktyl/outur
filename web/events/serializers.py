from rest_framework import serializers
from web.models import Event

class EventSerializer(serializers.ModelSerializer):
    users_count = serializers.IntegerField()
    likes_count = serializers.IntegerField()
    
    class Meta:
        model = Event
        fields = [
            'id',
            'name',
            'slug',
            'location',
            'one_day_date',
            'is_multi_day',
            'start_date',
            'end_date',
            'is_recurring',
            'day_of_week',
            'participants_count',
            'likes_count',
            'users_count',
            'date_info',
            'formatted_one_day_date'
        ]
