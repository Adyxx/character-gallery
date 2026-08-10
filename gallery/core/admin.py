from django.contrib import admin

from .models import (
	Affiliation,
	Character,
	Domain,
	GalleryImage,
	Race,
	StoryFragment,
	Region,
	TriviaEntry,
    Submerge,
    SubmergeCategory,
    Creature,
    Flora,
    FloraPropertyTag
)


admin.site.register(Affiliation)
admin.site.register(Character)
admin.site.register(Domain)
admin.site.register(GalleryImage)
admin.site.register(Race)
admin.site.register(StoryFragment)
admin.site.register(Region)
admin.site.register(TriviaEntry)
admin.site.register(Submerge)
admin.site.register(SubmergeCategory)
admin.site.register(Creature)
admin.site.register(Flora)
admin.site.register(FloraPropertyTag)
