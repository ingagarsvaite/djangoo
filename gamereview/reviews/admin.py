from django.contrib import admin
from .models import Publisher, Game, Genre, GameReview
from .forms import GameReviewForm

class GameReviewAdmin(admin.ModelAdmin):
    list_display = ('game', 'reviewer', 'content', 'date_created')
    list_editable = ('reviewer',)


admin.site.register(Publisher)
admin.site.register(Game)
admin.site.register(Genre)
admin.site.register(GameReview, GameReviewAdmin)



