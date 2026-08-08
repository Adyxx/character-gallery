from django.contrib import admin

from .models import (
	Affiliation,
	Character,
	Domain,
	GalleryImage,
	Race,
	StoryFragment,
	Territory,
	TriviaEntry,
)


admin.site.register(Affiliation)
admin.site.register(Character)
admin.site.register(Domain)
admin.site.register(GalleryImage)
admin.site.register(Race)
admin.site.register(StoryFragment)
admin.site.register(Territory)
admin.site.register(TriviaEntry)