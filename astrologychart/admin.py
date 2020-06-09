from django.contrib import admin
from .models import AstrologyInfo, SunSign, MOONSign, MERCURYSign, VENUSSign, MARSSign, JUPITERSign, SATURNSign, URANUSSign, NEPTUNESign, PLUTOSign, CHIRONSign, AscSign, DesSign, MCSign, ICSign, NNodeSign, SNodeSign
from .models import HOUSE1, HOUSE2, HOUSE3, HOUSE4, HOUSE5, HOUSE6, HOUSE7, HOUSE8, HOUSE9, HOUSE10, HOUSE11, HOUSE12
from .models import ConstellationIntroduction, PlanetIntroduction, HouseIntroduction, AnglesIntroduction, NodeIntroduction

# Register your models here.


class AstrologyInfoAdmin(admin.ModelAdmin):
    list_display = ('user', 'latitude', 'longitude', 'date', 'time', 'accuracy', 'feedback')
    list_filter = ('user', 'latitude', 'longitude', 'date', 'time', 'accuracy')


admin.site.register(AstrologyInfo, AstrologyInfoAdmin)


class ConstellationIntroductionAdmin(admin.ModelAdmin):
    list_display = ('constellation', 'introduction')
    list_filter = ('constellation',)


admin.site.register(ConstellationIntroduction, ConstellationIntroductionAdmin)


class PlanetIntroductionAdmin(admin.ModelAdmin):
    list_display = ('planet', 'introduction')
    list_filter = ('planet', )


admin.site.register(PlanetIntroduction, PlanetIntroductionAdmin)


class HouseIntroductionAdmin(admin.ModelAdmin):
    list_display = ('house', 'introduction')
    list_filter = ('house', )


admin.site.register(HouseIntroduction, HouseIntroductionAdmin)


class AnglesIntroductionAdmin(admin.ModelAdmin):
    list_display = ('angle', 'introduction')
    list_filter = ('angle', )


admin.site.register(AnglesIntroduction, AnglesIntroductionAdmin)


class NodeIntroductionAdmin(admin.ModelAdmin):
    list_display = ('node', 'introduction')
    list_filter = ('node', )


admin.site.register(NodeIntroduction, NodeIntroductionAdmin)


class SunSignAdmin(admin.ModelAdmin):
    list_display = ('sign', 'meaning', 'house_meaning')
    list_filter = ('sign',)


admin.site.register(SunSign, SunSignAdmin)


class MOONSignAdmin(admin.ModelAdmin):
    list_display = ('sign', 'meaning', 'house_meaning')
    list_filter = ('sign',)


admin.site.register(MOONSign, MOONSignAdmin)


class MERCURYSignAdmin(admin.ModelAdmin):
    list_display = ('sign', 'meaning', 'house_meaning')
    list_filter = ('sign',)


admin.site.register(MERCURYSign,  MERCURYSignAdmin)


class VENUSSignAdmin(admin.ModelAdmin):
    list_display = ('sign', 'meaning', 'house_meaning')
    list_filter = ('sign',)


admin.site.register(VENUSSign,  VENUSSignAdmin)


class MARSSignAdmin(admin.ModelAdmin):
    list_display = ('sign', 'meaning', 'house_meaning')
    list_filter = ('sign',)


admin.site.register(MARSSign,  MARSSignAdmin)


class JUPITERSignAdmin(admin.ModelAdmin):
    list_display = ('sign', 'meaning', 'house_meaning')
    list_filter = ('sign',)


admin.site.register(JUPITERSign,  JUPITERSignAdmin)


class SATURNSignAdmin(admin.ModelAdmin):
    list_display = ('sign', 'meaning', 'house_meaning')
    list_filter = ('sign',)


admin.site.register(SATURNSign,  SATURNSignAdmin)


class URANUSSignAdmin(admin.ModelAdmin):
    list_display = ('sign', 'meaning', 'house_meaning')
    list_filter = ('sign',)


admin.site.register(URANUSSign,  URANUSSignAdmin)


class NEPTUNESignAdmin(admin.ModelAdmin):
    list_display = ('sign', 'meaning', 'house_meaning')
    list_filter = ('sign',)


admin.site.register(NEPTUNESign, NEPTUNESignAdmin)


class PLUTOSignAdmin(admin.ModelAdmin):
    list_display = ('sign', 'meaning', 'house_meaning')
    list_filter = ('sign',)


admin.site.register(PLUTOSign,  PLUTOSignAdmin)


class CHIRONSignAdmin(admin.ModelAdmin):
    list_display = ('sign', 'meaning')
    list_filter = ('sign',)


admin.site.register(CHIRONSign, CHIRONSignAdmin)


class AscSignAdmin(admin.ModelAdmin):
    list_display = ('sign',  'meaning')
    list_filter = ('sign',)


admin.site.register(AscSign, AscSignAdmin)


class DesSignAdmin(admin.ModelAdmin):
    list_display = ('sign',  'meaning')
    list_filter = ('sign',)


admin.site.register(DesSign, DesSignAdmin)


class MCSignAdmin(admin.ModelAdmin):
    list_display = ('sign',  'meaning')
    list_filter = ('sign',)


admin.site.register(MCSign, MCSignAdmin)


class ICSignAdmin(admin.ModelAdmin):
    list_display = ('sign',  'meaning')
    list_filter = ('sign',)


admin.site.register(ICSign, ICSignAdmin)


class NNodeSignAdmin(admin.ModelAdmin):
    list_display = ('sign',  'meaning')
    list_filter = ('sign',)


admin.site.register(NNodeSign, NNodeSignAdmin)


class SNodeSignAdmin(admin.ModelAdmin):
    list_display = ('sign',  'meaning')
    list_filter = ('sign',)


admin.site.register(SNodeSign, SNodeSignAdmin)


# class HOUSE1Admin(admin.ModelAdmin):
#     list_display = ('sign',  'meaning')
#     list_filter = ('sign',)
#
#
# admin.site.register(HOUSE1, HOUSE1Admin)
#
#
# class HOUSE2Admin(admin.ModelAdmin):
#     list_display = ('sign',  'meaning')
#     list_filter = ('sign',)
#
#
# admin.site.register(HOUSE2, HOUSE2Admin)
#
#
# class HOUSE3Admin(admin.ModelAdmin):
#     list_display = ('sign',  'meaning')
#     list_filter = ('sign',)
#
#
# admin.site.register(HOUSE3, HOUSE3Admin)
#
#
# class HOUSE4Admin(admin.ModelAdmin):
#     list_display = ('sign',  'meaning')
#     list_filter = ('sign',)
#
#
# admin.site.register(HOUSE4, HOUSE4Admin)
#
#
# class HOUSE5Admin(admin.ModelAdmin):
#     list_display = ('sign', 'meaning')
#     list_filter = ('sign',)
#
#
# admin.site.register(HOUSE5, HOUSE5Admin)
#
#
# class HOUSE6Admin(admin.ModelAdmin):
#     list_display = ('sign',  'meaning')
#     list_filter = ('sign',)
#
#
# admin.site.register(HOUSE6, HOUSE6Admin)
#
#
# class HOUSE7Admin(admin.ModelAdmin):
#     list_display = ('sign',  'meaning')
#     list_filter = ('sign',)
#
#
# admin.site.register(HOUSE7, HOUSE7Admin)
#
#
# class HOUSE8Admin(admin.ModelAdmin):
#     list_display = ('sign',  'meaning')
#     list_filter = ('sign',)
#
#
# admin.site.register(HOUSE8, HOUSE8Admin)
#
#
# class HOUSE9Admin(admin.ModelAdmin):
#     list_display = ('sign',  'meaning')
#     list_filter = ('sign',)
#
#
# admin.site.register(HOUSE9, HOUSE9Admin)
#
#
# class HOUSE10Admin(admin.ModelAdmin):
#     list_display = ('sign', 'meaning')
#     list_filter = ('sign',)
#
#
# admin.site.register(HOUSE10, HOUSE10Admin)
#
#
# class HOUSE11Admin(admin.ModelAdmin):
#     list_display = ('sign', 'meaning')
#     list_filter = ('sign',)
#
#
# admin.site.register(HOUSE11, HOUSE11Admin)
#
#
# class HOUSE12Admin(admin.ModelAdmin):
#     list_display = ('sign',  'meaning')
#     list_filter = ('sign',)
#
#
# admin.site.register(HOUSE12, HOUSE12Admin)

