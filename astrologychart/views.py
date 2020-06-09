from django.shortcuts import render
from .forms import AstrologyInfoForm, FeedbackForm
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib.chart import Chart
from flatlib import const
import json
from django.contrib.auth.models import AnonymousUser
from .models import SunSign, MOONSign, MERCURYSign, VENUSSign, MARSSign, JUPITERSign, SATURNSign, URANUSSign, NEPTUNESign, PLUTOSign, CHIRONSign
from .models import AscSign, DesSign, MCSign, ICSign
from .models import PlanetIntroduction, HouseIntroduction, AnglesIntroduction
from .models import NNodeSign, NodeIntroduction, SNodeSign

# Create your views here.


def astrologychart(request):
    # return render(request, "astrologychart/astrologychart-astro.html")
    return render(request, "astrologychart/astrologychart.html")

@csrf_exempt
def feedback_astrology(request):
    if request.method == "POST":
        feedback_form = FeedbackForm(data=request.POST)
        if feedback_form.is_valid():
            cd = feedback_form.cleaned_data
            try:
                new_astrology = feedback_form.save(commit=False)
                if isinstance(request.user, AnonymousUser):
                    print('游客')
                else:
                    new_astrology.user = request.user
                new_astrology.save()
                return HttpResponse("1")
            except:
                return HttpResponse("2")
        else:
            return HttpResponse("3")
    else:
        astrologyinfo_form = AstrologyInfoForm()
        astrologyinfo_form['date'].field.widget.attrs['style'] = 'width:600px'
        return render(request, "astrologychart/astrologychart.html", {"article_post_form": astrologyinfo_form})



@csrf_exempt
def calculate_astrology(request):
    if request.method == "POST":
        data = request.POST
        date = Datetime(data['date'], data['time'], '+08:00')
        pos = GeoPos(data['latitude'], data['longitude'])
        chart = Chart(date, pos, IDs=[const.SUN, const.MOON, const.MERCURY, const.VENUS, const.MARS, const.JUPITER, const.SATURN, const.URANUS, const.NEPTUNE, const.PLUTO, const.CHIRON, const.NORTH_NODE, const.SOUTH_NODE ])
        print(data['latitude']+ data['longitude'])
        print(data['date']+ data['time'])
        cusp = []
        lsthouse = chart.houses
        for house in lsthouse:
            print(str(house))
            # print(str(house.sign)+': '+str(house.lon))
            cusp.append(round(house.lon, 6))
        cusps = {'cusps': cusp}
        print(cusps)

        planets = {}

        lstplanet = chart.objects
        for obj in lstplanet:
            print(str(obj))
            temp1 = obj.lon
            temp2 = obj.id
            print(temp2+':  ' + str(temp1)+' '+str(obj.signlon))
            tem = []
            tem.append(round(temp1, 6))
            if temp2 == 'North Node':
                planets['NNode'] = tem
            else:
                planets[temp2] = tem
        print(planets)

        angles = {}
        lstangle = chart.angles
        for angle in lstangle:
            print(str(angle))
            print(str(angle.lon))
            angles[angle.id] = round(angle.lon, 6)
        coordinate = data['latitude'] +'&nbsp&nbsp&nbsp'+ data['longitude']
        time = data['date'] + '&nbsp&nbsp&nbsp' + data['time']
        data = {}
        data['planets'] = planets
        data['cusps'] = cusps['cusps']
        data['angles'] = angles


        print(data)

        data['coordinate'] = coordinate
        data['time'] = time
        sunsign = {}
        sun_obj = chart.get(const.SUN)
        print('太阳星座'+sun_obj.sign)
        sign_sun = findsign(SunSign, sun_obj.sign)
        print(sign_sun.sign)
        print(sign_sun.meaning)
        sunsign['signlon'] = conv(sun_obj.signlon)
        sunsign['planetmeaning'] = PlanetIntroduction.objects.filter(planet='太阳')[0].introduction
        sunsign['chinesesign'] = sign_sun.sign
        sunsign['englishsign'] = sun_obj.sign
        sunsign['meaning'] = sign_sun.meaning
        data['SunSign'] = sunsign


        moonsign = {}
        moon_obj = chart.get(const.MOON)
        print('月亮星座'+moon_obj.sign)
        sign_moon = findsign(MOONSign, moon_obj.sign)
        print(sign_moon.sign)
        print(sign_moon.meaning)
        moonsign['signlon'] = conv(moon_obj.signlon)
        moonsign['planetmeaning'] = PlanetIntroduction.objects.filter(planet='月亮')[0].introduction
        moonsign['chinesesign'] = sign_moon.sign
        moonsign['englishsign'] = moon_obj.sign
        moonsign['meaning'] = sign_moon.meaning
        data['MoonSign'] = moonsign

        mercurysign = {}
        mercury_obj = chart.get(const.MERCURY)
        print('水星星座'+mercury_obj.sign)
        sign_mercury = findsign(MERCURYSign, mercury_obj.sign)
        print(sign_mercury.sign)
        print(sign_mercury.meaning)
        mercurysign['signlon'] = conv(mercury_obj.signlon)
        mercurysign['planetmeaning'] = PlanetIntroduction.objects.filter(planet='水星')[0].introduction
        mercurysign['chinesesign'] = sign_mercury.sign
        mercurysign['englishsign'] = mercury_obj.sign
        mercurysign['meaning'] = sign_mercury.meaning
        data['MercurySign'] = mercurysign

        venussign = {}
        venus_obj = chart.get(const.VENUS)
        print('金星星座'+venus_obj.sign)
        sign_venus = findsign(VENUSSign, venus_obj.sign)
        print(sign_venus.sign)
        print(sign_venus.meaning)
        venussign['signlon'] = conv(venus_obj.signlon)
        venussign['planetmeaning'] = PlanetIntroduction.objects.filter(planet='金星')[0].introduction
        venussign['chinesesign'] = sign_venus.sign
        venussign['englishsign'] = venus_obj.sign
        venussign['meaning'] = sign_venus.meaning
        data['VenusSign'] = venussign

        marssign = {}
        mars_obj = chart.get(const.MARS)
        print('火星星座'+mars_obj.sign)
        sign_mars = findsign(MARSSign, mars_obj.sign)
        print(sign_mars.sign)
        print(sign_mars.meaning)
        marssign['signlon'] = conv(mars_obj.signlon)
        marssign['planetmeaning'] = PlanetIntroduction.objects.filter(planet='火星')[0].introduction
        marssign['chinesesign'] = sign_mars.sign
        marssign['englishsign'] = mars_obj.sign
        marssign['meaning'] = sign_mars.meaning
        data['MarsSign'] = marssign

        jupitersign = {}
        jupiter_obj = chart.get(const.JUPITER)
        print('木星星座'+jupiter_obj.sign)
        sign_jupiter = findsign(JUPITERSign, jupiter_obj.sign)
        print(sign_jupiter.sign)
        print(sign_jupiter.meaning)
        jupitersign['signlon'] = conv(jupiter_obj.signlon)
        jupitersign['planetmeaning'] = PlanetIntroduction.objects.filter(planet='木星')[0].introduction
        jupitersign['chinesesign'] = sign_jupiter.sign
        jupitersign['englishsign'] = jupiter_obj.sign
        jupitersign['meaning'] = sign_jupiter.meaning
        data['JupiterSign'] = jupitersign

        saturnsign = {}
        saturn_obj = chart.get(const.SATURN)
        print('土星星座'+saturn_obj.sign)
        sign_saturn = findsign(SATURNSign, saturn_obj.sign)
        print(sign_saturn.sign)
        print(sign_saturn.meaning)
        saturnsign['signlon'] = conv(saturn_obj.signlon)
        saturnsign['planetmeaning'] = PlanetIntroduction.objects.filter(planet='土星')[0].introduction
        saturnsign['chinesesign'] = sign_saturn.sign
        saturnsign['englishsign'] = saturn_obj.sign
        saturnsign['meaning'] = sign_saturn.meaning
        data['SaturnSign'] = saturnsign

        uranussign = {}
        uranus_obj = chart.get(const.URANUS)
        print('天王星星座'+uranus_obj.sign)
        sign_uranus = findsign(URANUSSign, uranus_obj.sign)
        print(sign_uranus.sign)
        print(sign_uranus.meaning)
        uranussign['signlon'] = conv(uranus_obj.signlon)
        uranussign['planetmeaning'] = PlanetIntroduction.objects.filter(planet='天王星')[0].introduction
        uranussign['chinesesign'] = sign_uranus.sign
        uranussign['englishsign'] = uranus_obj.sign
        uranussign['meaning'] = sign_uranus.meaning
        data['UranusSign'] = uranussign

        neptunesign = {}
        neptune_obj = chart.get(const.NEPTUNE)
        print('海王星星座'+neptune_obj.sign)
        sign_neptune = findsign(NEPTUNESign, neptune_obj.sign)
        print(sign_neptune.sign)
        print(sign_neptune.meaning)
        neptunesign['signlon'] = conv(neptune_obj.signlon)
        neptunesign['planetmeaning'] = PlanetIntroduction.objects.filter(planet='海王星')[0].introduction
        neptunesign['chinesesign'] = sign_neptune.sign
        neptunesign['englishsign'] = neptune_obj.sign
        neptunesign['meaning'] = sign_neptune.meaning
        data['NeptuneSign'] = neptunesign

        plutosign = {}
        pluto_obj = chart.get(const.PLUTO)
        print('冥王星星座'+pluto_obj.sign)
        sign_pluto = findsign(PLUTOSign, pluto_obj.sign)
        print(sign_pluto.sign)
        print(sign_pluto.meaning)
        plutosign['signlon'] = conv(pluto_obj.signlon)
        plutosign['planetmeaning'] = PlanetIntroduction.objects.filter(planet='冥王星')[0].introduction
        plutosign['chinesesign'] = sign_pluto.sign
        plutosign['englishsign'] = pluto_obj.sign
        plutosign['meaning'] = sign_pluto.meaning
        data['PlutoSign'] = plutosign

        chironsign = {}
        chiron_obj = chart.get(const.CHIRON)
        print('凯龙星星座'+chiron_obj.sign)
        sign_chiron = findsign(CHIRONSign, chiron_obj.sign)
        print(sign_chiron.sign)
        print(sign_chiron.meaning)
        chironsign['signlon'] = conv(chiron_obj.signlon)
        chironsign['planetmeaning'] = PlanetIntroduction.objects.filter(planet='凯龙星')[0].introduction
        chironsign['chinesesign'] = sign_chiron.sign
        chironsign['englishsign'] = chiron_obj.sign
        chironsign['meaning'] = sign_chiron.meaning
        data['ChironSign'] = chironsign
        print(data)

        sunhouse = {}
        house_sun = findHouseOfPlanet(chart, sun_obj)
        if house_sun != None:
            print('太阳：'+house_sun.id)
            housesign_sun = findhousesign(SunSign, house_sun.id)
            print(housesign_sun.house_meaning)
            sunhouse['house'] = housetochinese(house_sun.id)
            sunhouse['introduction'] = housemeaning(house_sun.id)
            sunhouse['meaning'] = housesign_sun.house_meaning
            data['SunHouse'] = sunhouse

        moonhouse = {}
        house_moon = findHouseOfPlanet(chart, moon_obj)
        if house_moon != None:
            print('月亮：'+house_moon.id)
            housesign_moon = findhousesign(MOONSign, house_moon.id)
            print(housesign_moon.house_meaning)
            moonhouse['house'] = housetochinese(house_moon.id)
            moonhouse['introduction'] = housemeaning(house_moon.id)
            moonhouse['meaning'] = housesign_moon.house_meaning
            data['MoonHouse'] = moonhouse

        mercuryhouse = {}
        house_mercury = findHouseOfPlanet(chart, mercury_obj)
        if house_mercury != None:
            print('水星：'+house_mercury.id)
            housesign_mercury = findhousesign(MERCURYSign, house_mercury.id)
            print(housesign_mercury.house_meaning)
            mercuryhouse['house'] = housetochinese(house_mercury.id)
            mercuryhouse['introduction'] = housemeaning(house_mercury.id)
            mercuryhouse['meaning'] = housesign_mercury.house_meaning
            data['MercuryHouse'] = mercuryhouse

        venushouse = {}
        house_venus = findHouseOfPlanet(chart, venus_obj)
        if house_venus != None:
            print('金星：'+house_venus.id)
            housesign_venus = findhousesign(VENUSSign, house_venus.id)
            print(housesign_venus.house_meaning)
            venushouse['house'] = housetochinese(house_venus.id)
            venushouse['introduction'] = housemeaning(house_venus.id)
            venushouse['meaning'] = housesign_venus.house_meaning
            data['VenusHouse'] = venushouse

        marshouse = {}
        house_mars = findHouseOfPlanet(chart, mars_obj)
        if house_mars != None:
            print('火星：'+house_mars.id)
            housesign_mars = findhousesign(MARSSign, house_mars.id)
            print(housesign_mars.house_meaning)
            marshouse['house'] = housetochinese(house_mars.id)
            marshouse['introduction'] = housemeaning(house_mars.id)
            marshouse['meaning'] = housesign_mars.house_meaning
            data['MarsHouse'] = marshouse

        jupiterhouse = {}
        house_jupiter = findHouseOfPlanet(chart, jupiter_obj)
        if house_jupiter != None:
            print('木星：'+house_jupiter.id)
            housesign_jupiter = findhousesign(JUPITERSign, house_jupiter.id)
            print(housesign_jupiter.house_meaning)
            jupiterhouse['house'] = housetochinese(house_jupiter.id)
            jupiterhouse['introduction'] = housemeaning(house_jupiter.id)
            jupiterhouse['meaning'] = housesign_jupiter.house_meaning
            data['JupiterHouse'] = jupiterhouse

        saturnhouse = {}
        house_saturn = findHouseOfPlanet(chart, saturn_obj)
        if house_saturn != None:
            print('土星：'+house_saturn.id)
            housesign_saturn = findhousesign(SATURNSign, house_saturn.id)
            print(housesign_saturn.house_meaning)
            saturnhouse['house'] = housetochinese(house_saturn.id)
            saturnhouse['introduction'] = housemeaning(house_saturn.id)
            saturnhouse['meaning'] = housesign_saturn.house_meaning
            data['SaturnHouse'] = saturnhouse

        uranushouse = {}
        house_uranus = findHouseOfPlanet(chart, uranus_obj)
        if house_uranus != None:
            print('天王星：'+house_uranus.id)
            housesign_uranus = findhousesign(URANUSSign, house_uranus.id)
            print(housesign_uranus.house_meaning)
            uranushouse['house'] = housetochinese(house_uranus.id)
            uranushouse['introduction'] = housemeaning(house_uranus.id)
            uranushouse['meaning'] = housesign_uranus.house_meaning
            data['UranusHouse'] = uranushouse

        neptunehouse = {}
        house_neptune = findHouseOfPlanet(chart, neptune_obj)
        if house_neptune != None:
            print('海王星：'+house_neptune.id)
            housesign_neptune = findhousesign(NEPTUNESign, house_neptune.id)
            print(housesign_neptune.house_meaning)
            neptunehouse['house'] = housetochinese(house_neptune.id)
            neptunehouse['introduction'] = housemeaning(house_neptune.id)
            neptunehouse['meaning'] = housesign_neptune.house_meaning
            data['NeptuneHouse'] = neptunehouse

        plutohouse = {}
        house_pluto = findHouseOfPlanet(chart, pluto_obj)
        if house_pluto != None:
            print('冥王星：'+house_pluto.id)
            housesign_pluto = findhousesign(PLUTOSign, house_pluto.id)
            print(housesign_pluto.house_meaning)
            plutohouse['house'] = housetochinese(house_pluto.id)
            plutohouse['introduction'] = housemeaning(house_pluto.id)
            plutohouse['meaning'] = housesign_pluto.house_meaning
            data['PlutoHouse'] = plutohouse

        ascsign = {}
        asc_obj = chart.get(const.ASC)
        print('上升星座： ' + asc_obj.sign)
        sign_asc = findsign(AscSign, asc_obj.sign)
        if(sign_asc != None):
            print(sign_asc.sign)
            print(sign_asc.meaning)
            ascsign['signlon'] = conv(asc_obj.signlon)
            ascsign['introduction'] = AnglesIntroduction.objects.filter(angle='上升星座')[0].introduction
            ascsign['chinesesign'] = sign_asc.sign
            ascsign['englishsign'] = asc_obj.sign
            ascsign['meaning'] = sign_asc.meaning
            data['ASC'] = ascsign

        descsign = {}
        desc_obj = chart.get(const.DESC)
        print('下降星座： ' + desc_obj.sign)
        sign_desc = findsign(DesSign, desc_obj.sign)
        if(sign_desc != None):
            print(sign_desc.sign)
            print(sign_desc.meaning)
            descsign['signlon'] = conv(desc_obj.signlon)
            descsign['introduction'] = AnglesIntroduction.objects.filter(angle='下降星座')[0].introduction
            descsign['chinesesign'] = sign_desc.sign
            descsign['englishsign'] = desc_obj.sign
            descsign['meaning'] = sign_desc.meaning
            data['DESC'] = descsign

        mcsign = {}
        mc_obj = chart.get(const.MC)
        print('天顶星座： ' + mc_obj.sign)
        sign_mc = findsign(MCSign, mc_obj.sign)
        if(sign_mc != None):
            print(sign_mc.sign)
            print(sign_mc.meaning)
            mcsign['signlon'] = conv(mc_obj.signlon)
            mcsign['introduction'] = AnglesIntroduction.objects.filter(angle='天顶星座')[0].introduction
            mcsign['chinesesign'] = sign_mc.sign
            mcsign['englishsign'] = mc_obj.sign
            mcsign['meaning'] = sign_mc.meaning
            data['MC'] = mcsign

        icsign = {}
        ic_obj = chart.get(const.IC)
        print('天底星座： ' + ic_obj.sign)
        sign_ic = findsign(ICSign, ic_obj.sign)
        if(sign_ic != None):
            print(sign_ic.sign)
            print(sign_ic.meaning)
            icsign['signlon'] = conv(ic_obj.signlon)
            icsign['introduction'] = AnglesIntroduction.objects.filter(angle='天底星座')[0].introduction
            icsign['chinesesign'] = sign_ic.sign
            icsign['englishsign'] = ic_obj.sign
            icsign['meaning'] = sign_ic.meaning
            data['IC'] = icsign

        nodesign = {}
        nnode_obj = chart.get(const.NORTH_NODE)
        snode_obj = chart.get(const.SOUTH_NODE)
        print('北交点星座： ' + nnode_obj.sign)
        print('南交点星座： ' + snode_obj.sign)
        sign_nnode = findsign(NNodeSign, nnode_obj.sign)
        sign_snode = findsign(SNodeSign, snode_obj.sign)
        if (sign_nnode != None):
            print(sign_nnode.sign)
            print(sign_nnode.meaning)
            nodesign['signlon_nnode'] = conv(nnode_obj.signlon)
            nodesign['signlon_snode'] = conv(snode_obj.signlon)
            nodesign['introduction_nnode'] = NodeIntroduction.objects.filter(node='北交点')[0].introduction
            nodesign['introduction_snode'] = NodeIntroduction.objects.filter(node='南交点')[0].introduction
            nodesign['chinesesign_nnode'] = sign_nnode.sign
            nodesign['englishsign_nnode'] = nnode_obj.sign
            nodesign['chinesesign_snode'] = sign_snode.sign
            nodesign['englishsign_snode'] = snode_obj.sign
            nodesign['meaning'] = sign_nnode.meaning
            data['Node'] = nodesign

        astrologyinfo_form = AstrologyInfoForm(data=request.POST)

        if astrologyinfo_form.is_valid():
            cd = astrologyinfo_form.cleaned_data
            try:
                new_astrology = astrologyinfo_form.save(commit=False)
                if isinstance(request.user, AnonymousUser):
                    print('游客')
                else:
                    new_astrology.user = request.user
                # new_astrology.save()
                return HttpResponse(json.dumps(data))
            except:
                return HttpResponse("2")
        else:
            return HttpResponse("3")
    else:
        astrologyinfo_form = AstrologyInfoForm()
        astrologyinfo_form['date'].field.widget.attrs['style'] = 'width:600px'
        return render(request, "astrologychart/astrologychart.html", {"article_post_form": astrologyinfo_form})


def findsign(cls, sign):
    print(cls)
    print(cls.objects.filter(sign='双鱼座'))
    if sign == 'Aries':
        temp = cls.objects.filter(sign='白羊座')[0]
        return temp
    elif sign == 'Taurus':
        temp = cls.objects.filter(sign='金牛座')[0]
        return temp
    elif sign == 'Gemini':
        temp = cls.objects.filter(sign='双子座')[0]
        return temp
    elif sign == 'Cancer':
        temp = cls.objects.filter(sign='巨蟹座')[0]
        return temp
    elif sign == 'Leo':
        temp = cls.objects.filter(sign='狮子座')[0]
        return temp
    elif sign == 'Virgo':
        temp = cls.objects.filter(sign='处女座')[0]
        return temp
    elif sign == 'Libra':
        temp = cls.objects.filter(sign='天秤座')[0]
        return temp
    elif sign == 'Scorpio':
        temp = cls.objects.filter(sign='天蝎座')[0]
        return temp
    elif sign == 'Sagittarius':
        temp = cls.objects.filter(sign='射手座')[0]
        return temp
    elif sign == 'Capricorn':
        temp = cls.objects.filter(sign='摩羯座')[0]
        return temp
    elif sign == 'Aquarius':
        temp = cls.objects.filter(sign='水瓶座')[0]
        return temp
    elif sign == 'Pisces':
        temp = cls.objects.filter(sign='双鱼座')[0]
        return temp
    else:
        return None


def findHouseOfPlanet(chart, planet):
    house1 = chart.get(const.HOUSE1)
    house2 = chart.get(const.HOUSE2)
    house3 = chart.get(const.HOUSE3)
    house4 = chart.get(const.HOUSE4)
    house5 = chart.get(const.HOUSE5)
    house6 = chart.get(const.HOUSE6)
    house7 = chart.get(const.HOUSE7)
    house8 = chart.get(const.HOUSE8)
    house9 = chart.get(const.HOUSE9)
    house10 = chart.get(const.HOUSE10)
    house11 = chart.get(const.HOUSE11)
    house12 = chart.get(const.HOUSE12)
    if (house1.hasObject(planet)):
        return house1
    elif (house2.hasObject(planet)):
        return house2
    elif (house3.hasObject(planet)):
        return house3
    elif (house4.hasObject(planet)):
        return house4
    elif (house5.hasObject(planet)):
        return house5
    elif (house6.hasObject(planet)):
        return house6
    elif (house7.hasObject(planet)):
        return house7
    elif (house8.hasObject(planet)):
        return house8
    elif (house9.hasObject(planet)):
        return house9
    elif (house10.hasObject(planet)):
        return house10
    elif (house11.hasObject(planet)):
        return house11
    elif (house12.hasObject(planet)):
        return house12
    else:
        return None


def findhousesign(cls, id):
    if id == 'House1':
        temp = cls.objects.filter(sign='白羊座')[0]
        return temp
    elif id == 'House2':
        temp = cls.objects.filter(sign='金牛座')[0]
        return temp
    elif id == 'House3':
        temp = cls.objects.filter(sign='双子座')[0]
        return temp
    elif id == 'House4':
        temp = cls.objects.filter(sign='巨蟹座')[0]
        return temp
    elif id == 'House5':
        temp = cls.objects.filter(sign='狮子座')[0]
        return temp
    elif id == 'House6':
        temp = cls.objects.filter(sign='处女座')[0]
        return temp
    elif id == 'House7':
        temp = cls.objects.filter(sign='天秤座')[0]
        return temp
    elif id == 'House8':
        temp = cls.objects.filter(sign='天蝎座')[0]
        return temp
    elif id == 'House9':
        temp = cls.objects.filter(sign='射手座')[0]
        return temp
    elif id == 'House10':
        temp = cls.objects.filter(sign='摩羯座')[0]
        return temp
    elif id == 'House11':
        temp = cls.objects.filter(sign='水瓶座')[0]
        return temp
    elif id == 'House12':
        temp = cls.objects.filter(sign='双鱼座')[0]
        return temp

def housetochinese(house):
    if house=='House1':
        return '第一宫'
    elif house == 'House2':
        return '第二宫'
    elif house == 'House3':
        return '第三宫'
    elif house == 'House4':
        return '第四宫'
    elif house == 'House5':
        return '第五宫'
    elif house == 'House6':
        return '第六宫'
    elif house == 'House7':
        return '第七宫'
    elif house == 'House8':
        return '第八宫'
    elif house == 'House9':
        return '第九宫'
    elif house == 'House10':
        return '第十宫'
    elif house == 'House11':
        return '第十一宫'
    elif house == 'House12':
        return '第十二宫'

def housemeaning(house):
    if house =='House1':
        return HouseIntroduction.objects.filter(house='第一宫')[0].introduction
    elif house == 'House2':
        return HouseIntroduction.objects.filter(house='第二宫')[0].introduction
    elif house == 'House3':
        return HouseIntroduction.objects.filter(house='第三宫')[0].introduction
    elif house == 'House4':
        return HouseIntroduction.objects.filter(house='第四宫')[0].introduction
    elif house == 'House5':
        return HouseIntroduction.objects.filter(house='第五宫')[0].introduction
    elif house == 'House6':
        return HouseIntroduction.objects.filter(house='第六宫')[0].introduction
    elif house == 'House7':
        return HouseIntroduction.objects.filter(house='第七宫')[0].introduction
    elif house == 'House8':
        return HouseIntroduction.objects.filter(house='第八宫')[0].introduction
    elif house == 'House9':
        return HouseIntroduction.objects.filter(house='第九宫')[0].introduction
    elif house == 'House10':
        return HouseIntroduction.objects.filter(house='第十宫')[0].introduction
    elif house == 'House11':
        return HouseIntroduction.objects.filter(house='第十一宫')[0].introduction
    elif house == 'House12':
        return HouseIntroduction.objects.filter(house='第十二宫')[0].introduction


def convertlon(temp):
    print(temp)
    lst = temp.split('.')
    degree = lst[0]
    minute = float('0.'+lst[1])*60.0
    return degree + '°' + str(int(minute)) + '\''


def conv(num):
    '''
    bef0: 小数点前面的值
    aft0: 转换后小数点后面的数
    '''
    bef0, aft0 = int(num), int((num - int(num))*60.0)

    return "%s°%s\'" % (bef0, aft0)