from django.contrib.postgres.search import SearchVector
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from HouseListing.models import Properties
from .forms import *
import datetime
from django.db.models import Q


# listing views

# pending -> 0
# approved -> 1
# rejected -> 2


def listing_dashboard(request):

    approved_properties = Properties.objects.filter(user=request.user,managed_by_manyumba=False, approved_by_admin=1).count()
    pending_properties = Properties.objects.filter(user=request.user,managed_by_manyumba=False, approved_by_admin=0).count()
    active_listings = Properties.objects.filter(
        user=request.user, managed_by_manyumba=False, approved_by_admin=1, publish=True).count()
    off_market_properties = Properties.objects.filter(
        Q(user=request.user, managed_by_manyumba=False, approved_by_admin=0, publish=False) | Q(
            user=request.user, managed_by_manyumba=False, approved_by_admin=1, publish=False) | Q(user=request.user, managed_by_manyumba=False, approved_by_admin=0, publish=True)
    ).count()

    all_properties = Properties.objects.filter(
        user=request.user, managed_by_manyumba=False).count()
    try:
        approved_percentage = (approved_properties/all_properties) * 100
    except:
        approved_percentage = 0

    try:
        pending_percentage = (pending_properties/all_properties) * 100
    except:
        pending_percentage = 0

    try:
        active_listings_percentage = (active_listings/all_properties) * 100
    except:
        active_listings_percentage = 0

    try:
        off_market_properties_percentage = (off_market_properties/all_properties) * 100
    except:
        off_market_properties_percentage = 0

    context = {
        'approved_properties': approved_properties,
        'pending_properties': pending_properties,
        'active_listings': active_listings,
        'off_market_properties': off_market_properties,
        'approved_percentage': approved_percentage,
        'pending_percentage': pending_percentage,
        'active_listings_percentage': active_listings_percentage,
        'off_market_properties_percentage': off_market_properties_percentage,
        
    }

    
    return render(request, 'HouseListing/dashboard_listing.html', context)



def create_listing_listing(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        if request.method == 'GET':
            form = PropertiesForm(request.POST or None)
            try:
                land_id = Type.objects.get(name='Land').id
            
            except:
                land_ = Type.objects.create(
                    name = 'Land'
                )
                
            try:
                office_id = Type.objects.get(name='Office Space').id
            
            except:
                land_ = Type.objects.create(
                    name = 'Office Space'
                )

                office_id = land_.id
            context = {
                'form': form,
                'land_id':land_id,
                'office_id':office_id,
                'side': 'listing_side',
            }
            return render(request, 'HouseListing/create_listing_listing.html', context)

        else:
            # get the fields
            city = request.POST.get('city')
            prop_city = Cities.objects.get(id=city)

            street = request.POST.get('street')

            # page 2
            property_title = request.POST.get('property_title')
            description = request.POST.get('description')

            # get type instance
            type = request.POST.get('type')
            prop_type = Type.objects.get(id=type)

            # get status instance
            status = request.POST.get('status')
            prop_status = PropertyStatus.objects.get(id=status)


            # get landsize instance
           

            land_id = Type.objects.get(name='Land').id

            if int(type) == land_id:
                landsize = request.POST.get('landsize')
                prop_landsize = LandSizes.objects.get(id=landsize)
            else:
                prop_landsize = None
            
            area_size = request.POST.get('area_size')

            price = request.POST.get('price')
            price = int(price)

            # deposit = request.POST.get('deposit')
            # deposit = int(price)

            # fields for non-land properties
            rooms = request.POST.get('rooms')
            bedrooms = request.POST.get('bedrooms')
            bathrooms = request.POST.get('bathrooms')
            garages = request.POST.get('garages')

            publish = request.POST.get('publish')

            if publish == 'Yes':
                pre_publish = True
            else:
                pre_publish = False

            # amenities
            Water = request.POST.get('Water', False)
            if Water == 'on':
                Water = True
            Electricity = request.POST.get('Electricity', False)
            if Electricity == 'on':
                Electricity = True
            Wifi = request.POST.get('WIFI', False)
            if Wifi == 'on':
                Wifi = True

            Ac = request.POST.get('Ac', False)
            if Ac == 'on':
                Ac = True
            Gateman = request.POST.get('Gateman', False)
            if Gateman == 'on':
                Gateman = True
            Parking = request.POST.get('Parking', False)
            if Parking == 'on':
                Parking = True
            Swimming_Pool = request.POST.get('Swimming_Pool', False)
            if Swimming_Pool == 'on':
                Swimming_Pool = True
            Balcony = request.POST.get('Balcony', False)
            if Balcony == 'on':
                Balcony = True
            Gym = request.POST.get('Gym', False)
            if Gym == 'on':
                Gym = True
            Play_Area = request.POST.get('Play_Area', False)
            if Play_Area == 'on':
                Play_Area = True

            # land

            ElectricSupply = request.POST.get('ElectricSupply', False)
            if ElectricSupply == 'on':
                ElectricSupply = True
            WaterSupply = request.POST.get('WaterSupply', False)
            if WaterSupply == 'on':
                WaterSupply = True
            RainWaterDrainage = request.POST.get('RainWaterDrainage', False)
            if RainWaterDrainage == 'on':
                RainWaterDrainage = True
            DomesticSewage = request.POST.get('DomesticSewage', False)
            if DomesticSewage == 'on':
                DomesticSewage = True

            # bussiness

            BusinessLounge = request.POST.get('BusinessLounge', False)
            if BusinessLounge == 'on':
                BusinessLounge = True    
            Majortransportlinks = request.POST.get('Majortransportlinks', False)
            if Majortransportlinks == 'on':
                Majortransportlinks = True    
            MeetingRooms = request.POST.get('MeetingRooms', False)
            if MeetingRooms == 'on':
                MeetingRooms = True    
            cctv= request.POST.get('CCTV', False)
            if cctv== 'on':
                cctv= True    
            Elevator= request.POST.get('Elevator', False)
            if Elevator== 'on':
                Elevator= True   
            

            

            # media
            featured_image = request.FILES.get('featured_image')
            living_room_media = request.FILES.getlist('living_room_media')
            bedroom_media = request.FILES.getlist('bedroom_media')
            bathroom_media = request.FILES.getlist('bathroom_media')


            new_property = Properties.objects.create(
                user=request.user,
                property_title=property_title,
                description=description,
                type=prop_type,
                status=prop_status,
                publish=pre_publish,
                price=price,
                # security_deposit=deposit,
                area_size=area_size,
                landsize=prop_landsize,
                rooms=rooms,
                bedrooms=bedrooms,
                bathrooms=bathrooms,
                managed_by_manyumba=False,
                garages=garages,
                city=prop_city,
                street=street,
                featured_image=featured_image,
                # amenities

                Water=Water,
                Electricity=Electricity,
                WFI=Wifi,
                Ac=Ac,
                Gateman=Gateman,
                Parking=Parking,
                Swimming_Pool=Swimming_Pool,
                Balcony=Balcony,
                Gym=Gym,
                Play_Area=Play_Area,
                
                ElectricSupply=ElectricSupply,
                WaterSupply=WaterSupply,
                RainWaterDrainage=RainWaterDrainage,
                DomesticSewage=DomesticSewage,
                BusinessLounge=BusinessLounge,
                Majortransportlinks=Majortransportlinks,
                MeetingRooms=MeetingRooms,
                CCTV=cctv,
                Elevator=Elevator,

            )

            # save images for the property
            for media in living_room_media:
                PropertyImages.objects.create(
                    property=new_property,
                    image=media,
                    home_tag='living_room'
                )
            
            for media in bedroom_media:
                PropertyImages.objects.create(
                    property=new_property,
                    image=media,
                    home_tag='bed_room'
                )
            
            for media in bathroom_media:
                PropertyImages.objects.create(
                    property=new_property,
                    image=media,
                    home_tag='bathroom'
                )
            messages.success(request, 'Property created successfully')
            return redirect('HouseListing:listing_dashboard')


def my_listing(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        active_properties = Properties.objects.filter(user=request.user, managed_by_manyumba=False, approved_by_admin=1, publish=True)
        off_market_properties = Properties.objects.filter(
            Q(user=request.user, managed_by_manyumba=False, approved_by_admin=0, publish=False) | 
            Q(user=request.user, managed_by_manyumba=False, approved_by_admin=True, publish=False)|
            Q(user=request.user, managed_by_manyumba=False, approved_by_admin=0, publish=True) |
            Q(user=request.user, managed_by_manyumba=False, approved_by_admin=2, publish=False) |
            Q(user=request.user, managed_by_manyumba=False, approved_by_admin=2, publish=True)
        )
        context = {
            'active_properties': active_properties,
            'off_market_properties': off_market_properties,
        }
        return render(request, 'HouseListing/my_listings.html', context)


def mylisting_detail(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        this_property = Properties.objects.get(id=pk)
        all_associated_avatars = PropertyImages.objects.filter(
            property=this_property)
        context = {
            'property': this_property,           
            'all_associated_avatars': all_associated_avatars,
        }
        return render(request, 'HouseListing/mylisting_detail.html', context)



def mortgages_leads(request, price, pk):
    context = {
        'price': price,
        'pk': pk,
    }
    return render(request, 'HouseListing/mortgages_leads.html', context)


def create_morgage_lead(request, pk):
    if request.method == 'POST':
        # get fields

        redirect_property = Properties.objects.get(id=pk)
        slug = redirect_property.slug
        full_name = request.POST.get('Name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        employment_type = request.POST.get('employment_type')
        monthly_gross_income = request.POST.get('monthly_gross_income')
        convenient_time_to_be_contacted = request.POST.get('convenient_time_to_be_contacted')
        property_price = request.POST.get('property_price')

        # save
        MorgageLeads.objects.create(
            full_name=full_name,
            phone=phone,
            email=email,
            employment_type=employment_type,
            gross_income=monthly_gross_income,
            convinient_time=convenient_time_to_be_contacted,
            property_price=property_price
        )
        messages.success(request, 'Application sent successfully. Our team will get back to you in a short while.')
        return redirect('HouseListing:listing_details', slug=slug)
    else:
        messages.warning(request, 'Error 404')
        return redirect('HouseListing:home')


def listings_for_sale(request):
    all_listings = Properties.objects.filter(approved_by_admin=1, publish=True, status__property_status='For Sale')
    count = all_listings.count()
    context = {
        'all_listings': all_listings,
        'count': count,
    }

    return render(request, 'HouseListing/listings_for_sale.html', context)


def listings_for_rent(request):
    all_listings = Properties.objects.filter(approved_by_admin=1, publish=True, status__property_status='For Rent')
    count = all_listings.count()
    context = {
        'all_listings': all_listings,
        'count': count,
    }

    return render(request, 'HouseListing/listings_for_rent.html', context)




def search_property_for_sale(request):
    if request.method == 'GET':
        q = request.GET.get('for_sale_location', None)
        if q is None or q == '':
            return redirect('HouseListing:listings_for_sale')
        else:
            all_listings = Properties.objects.filter(
                Q(property_title__icontains=q,approved_by_admin=1, publish=True, status__property_status='For Sale') | 
                Q(type__name__icontains=q,approved_by_admin=1, publish=True, status__property_status='For Sale')|
                Q(city__city_name__icontains=q,approved_by_admin=1, publish=True, status__property_status='For Sale')|
                Q(street__icontains=q,approved_by_admin=1, publish=True, status__property_status='For Sale')
            )
            count = all_listings.count()
            result_header = ' for ' + str(q)
            context = {
                'all_listings': all_listings,
                'result_header': result_header,
                'count': count,
            }
            return render(request, 'HouseListing/listings_for_sale.html', context)

    else:
        messages.warning(request, 'Bad request 404')
        return redirect('HouseListing:home')


def search_property_for_rent(request):
    if request.method == 'GET':
        q = request.GET.get('for_rent_location', None)
        if q is None or q == '':
            return redirect('HouseListing:listings_for_rent')
        else:
            all_listings = Properties.objects.filter(
                Q(property_title__icontains=q,approved_by_admin=1, publish=True, status__property_status='For Rent') | 
                Q(type__name__icontains=q,approved_by_admin=1, publish=True, status__property_status='For Rent')|
                Q(city__city_name__icontains=q,approved_by_admin=1, publish=True, status__property_status='For Rent')|
                Q(street__icontains=q,approved_by_admin=1, publish=True, status__property_status='For Rent')
            )
            count = all_listings.count()
            result_header = ' for ' + str(q)
            context = {
                'all_listings': all_listings,
                'result_header': result_header,
                'count': count,
            }
            return render(request, 'HouseListing/listings_for_rent.html', context)

    else:
        messages.warning(request, 'Bad request 404')
        return redirect('HouseListing:home')


def search_property_for_lease(request):
    if request.method == 'GET':
        q = request.GET.get('for_lease_location', None)
        if q is None or q == '':
            return redirect('HouseListing:home')
        else:
            all_listings = Properties.objects.filter(
                Q(property_title__icontains=q,approved_by_admin=1, publish=True, status__property_status='For Lease') | 
                Q(type__name__icontains=q,approved_by_admin=1, publish=True, status__property_status='For Lease')|
                Q(city__city_name__icontains=q,approved_by_admin=1, publish=True, status__property_status='For Lease')|
                Q(street__icontains=q,approved_by_admin=1, publish=True, status__property_status='For Lease')
            )
            count = all_listings.count()
            result_header = ' for ' + str(q)
            context = {
                'all_listings': all_listings,
                'result_header': result_header,
                'count': count,
            }
            return render(request, 'HouseListing/listings_for_lease.html', context)

    else:
        messages.warning(request, 'Bad request 404')
        return redirect('HouseListing:home')


def search_listing_town(request, town):
    
    all_listings = Properties.objects.filter(
        approved_by_admin=1, publish=True,city__city_name=town
    )
    count = all_listings.count()
    result_header = ' for ' + str(town)
    context = {
        'all_listings': all_listings,
        'result_header': result_header,
        'count': count,
        'town': town,
    }
    return render(request, 'HouseListing/search_listing_town.html', context)



def togglePublish(request,pk):
    this_property = Properties.objects.get(id=pk)
    this_property.publish = not this_property.publish
    this_property.save()

    messages.success(request, 'Preference saved')
    return redirect(request.META.get('HTTP_REFERER'))



def listing_profile(request):
    return render(request, 'HouseListing/listing_profile.html')


def listing_delete_property(request, pk):
    target_property = Properties.objects.get(id=pk)
    target_property.delete()
    messages.success(request, 'Property deleted successfully')
    return redirect(request.META.get('HTTP_REFERER'))



# ends here


def approve_listing(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        properties = Properties.objects.filter(approved_by_admin=0)
        context = {
            'properties': properties,
        }
        return render(request, 'HouseListing/approve_properties.html', context)


def admin_morgage_leads(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        leads = MorgageLeads.objects.all()
        context = {
            'leads': leads,
        }
        return render(request, 'HouseListing/morgage_leads.html', context)



def approve_property_detail(request,pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:    
        this_property = Properties.objects.get(id=pk)
        property_houses = this_property.house_set.all()
        all_associated_avatars = PropertyImages.objects.filter(property=this_property)
        floor_plans = FloorPlans.objects.filter(property=this_property)
        context = {
            'property': this_property,
            'property_houses': property_houses,
            'all_associated_avatars': all_associated_avatars,
            'floor_plans': floor_plans,
            'is_approve': True,

        }
        return render(request, 'HouseListing/approve_property_detail.html', context)


def property_details(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        this_property = Properties.objects.get(id=pk)
        property_houses = this_property.house_set.all()
        all_associated_avatars = PropertyImages.objects.filter(property=this_property)
        floor_plans = FloorPlans.objects.filter(property=this_property)
        context = {
            'property': this_property,
            'property_houses': property_houses,
            'all_associated_avatars': all_associated_avatars,
            'floor_plans': floor_plans,
        }
        return render(request, 'HouseListing/approve_property_detail.html', context)



def approve_property(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:    
        this_property = Properties.objects.get(id=pk)
        this_property.approved_by_admin = 1
        this_property.save()
        messages.success(request, 'Property Approved successfully')
        return redirect('HouseListing:approve_listing')


def reject_property(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:    
        this_property = Properties.objects.get(id=pk)
        this_property.approved_by_admin = 2
        this_property.save()
        messages.success(request, 'Property Rejected')
        return redirect('HouseListing:approve_listing')


def home(request):
    all_listings = Properties.objects.filter(approved_by_admin=1, publish=True)
    all_cities = Cities.objects.all()

    
    context = {
        'all_listings':all_listings,
        'all_cities':all_cities,
    }
    return render(request, 'HouseListing/home-listing.html', context)


def listing_details(request, slug):

    property = Properties.objects.get(slug=slug)
    try:
        featured_image = PropertyImages.objects.get(property=property, featured=True)
    except ObjectDoesNotExist:
        featured_image = ''
    print('featured image above')
    print(featured_image)

    try:
        images = PropertyImages.objects.filter(property=property)
    except:
        images = ''
    context = {
        'property': property,
        'featured_image': featured_image,
        'images': images,
    }
    return render(request, 'HouseListing/listing-details.html', context)

def coming_soon(request):
    return render(request, 'HouseListing/coming_soon.html')



def dashboard(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        approved_properties = Properties.objects.filter(
            user=request.user, managed_by_manyumba=True, approved_by_admin=1).count()
        pending_properties = Properties.objects.filter(user=request.user,managed_by_manyumba=True, approved_by_admin=0).count()
        active_listings = Properties.objects.filter(user=request.user,managed_by_manyumba=True, approved_by_admin=1, publish=True).count()
        off_market_properties = Properties.objects.filter(
            Q(user=request.user, managed_by_manyumba=True, approved_by_admin=0, publish=False) | Q(
                user=request.user, managed_by_manyumba=True, approved_by_admin=1, publish=False) | Q(user=request.user, managed_by_manyumba=True, approved_by_admin=0, publish=True)
        ).count()

        all_properties = Properties.objects.filter(
            user=request.user, managed_by_manyumba=True).count()

        try:
            approved_percentage = (approved_properties/all_properties) * 100
        except:
            approved_percentage = 0

        try:
            pending_percentage = (pending_properties/all_properties) * 100
        except:
            pending_percentage = 0

        try:
            active_listings_percentage = (active_listings/all_properties) * 100
        except:
            active_listings_percentage = 0

        try:
            off_market_properties_percentage = (off_market_properties/all_properties) * 100
        except:
            off_market_properties_percentage = 0

        context = {
            'approved_properties': approved_properties,
            'pending_properties': pending_properties,
            'active_listings': active_listings,
            'off_market_properties': off_market_properties,
            'approved_percentage': approved_percentage,
            'pending_percentage': pending_percentage,
            'active_listings_percentage': active_listings_percentage,
            'off_market_properties_percentage': off_market_properties_percentage,
            
        }

        return render(request, 'HouseListing/dashboard.html', context)


def properties(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        if request.user.is_superuser:
            pass

        properties = Properties.objects.filter(user=request.user,managed_by_manyumba=True)
        context = {
            'properties': properties,
        }
        return render(request, 'HouseListing/properties.html', context)


def create_listing(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        if request.method == 'GET':
            try:
                apartment_id = Type.objects.get(name='Apartment').id
            except:
                apartment_ = Type.objects.create(
                    name = 'Apartment'
                )

                apartment_id = apartment_.id
            
            try:
                land_id = Type.objects.get(name='Land').id
            
            except:
                land_ = Type.objects.create(
                    name = 'Land'
                )

                land_id = land_.id

            try:
                for_rent = PropertyStatus.objects.get(property_status='For Rent').id
            except:
                for_rent_ = PropertyStatus.objects.create(
                    property_status = 'For Rent'
                )
                for_rent = for_rent_.id

            try:
                office_id = Type.objects.get(name='Office Space').id
            
            except:
                land_ = Type.objects.create(
                    name = 'Office Space'
                )

                office_id = land_.id

            form = ManagePropertiesForm(request.POST or None)
            context = {
                'form': form,
                'for_rent': for_rent,
                'apartment_id': apartment_id,
                'office_id': office_id,
                'land_id': land_id,
                'side': 'management_side'
            }
            return render(request, 'HouseListing/create-listing.html', context)
        else:
            # get the fields
            # try:
                property_title = request.POST.get('property_title')
                description = request.POST.get('description')

                type = request.POST.get('type')
                prop_type = Type.objects.get(id=type)

                status = request.POST.get('status')
                prop_status = PropertyStatus.objects.get(id=status)

                publish = request.POST.get('publish')

                if publish == 'Yes':
                    pre_publish = True
                else:
                    pre_publish = False
                
                price = request.POST.get('price', 0)
                price = int(price)


                area_size = request.POST.get('area_size')

                land_id = Type.objects.get(name='Land').id
                if int(type) == land_id and request.POST.get('landsize') != '':
                    landsize = request.POST.get('landsize')
                    prop_landsize = LandSizes.objects.get(id=landsize)
                else:
                    prop_landsize = None
                rooms = request.POST.get('rooms')
                bedrooms = request.POST.get('bedrooms')
                bathrooms = request.POST.get('bathrooms')
                garages = request.POST.get('garages')

                city = request.POST.get('city')
                prop_city = Cities.objects.get(id=city)

                street = request.POST.get('street')
                
                # amenities

                Water = request.POST.get('Water', False)
                if Water == 'on':
                    Water = True
                Electricity = request.POST.get('Electricity', False)
                if Electricity == 'on':
                    Electricity = True
                Wifi = request.POST.get('WIFI', False)
                if Wifi == 'on':
                    Wifi = True

                Ac = request.POST.get('Ac', False)
                if Ac == 'on':
                    Ac = True
                Gateman = request.POST.get('Gateman', False)
                if Gateman == 'on':
                    Gateman = True
                Parking = request.POST.get('Parking', False)
                if Parking == 'on':
                    Parking = True
                Swimming_Pool = request.POST.get('Swimming_Pool', False)
                if Swimming_Pool == 'on':
                    Swimming_Pool = True
                Balcony = request.POST.get('Balcony', False)
                if Balcony == 'on':
                    Balcony = True
                Gym = request.POST.get('Gym', False)
                if Gym == 'on':
                    Gym = True
                Play_Area = request.POST.get('Play_Area', False)
                if Play_Area == 'on':
                    Play_Area = True
                ElectricSupply = request.POST.get('ElectricSupply', False)
                if ElectricSupply == 'on':
                    ElectricSupply = True
                WaterSupply = request.POST.get('WaterSupply', False)
                if WaterSupply == 'on':
                    WaterSupply = True
                RainWaterDrainage = request.POST.get('RainWaterDrainage', False)
                if RainWaterDrainage == 'on':
                    RainWaterDrainage = True
                DomesticSewage = request.POST.get('DomesticSewage', False)
                if DomesticSewage == 'on':
                    DomesticSewage = True    
                BusinessLounge = request.POST.get('BusinessLounge', False)
                if BusinessLounge == 'on':
                    BusinessLounge = True    
                Majortransportlinks = request.POST.get('Majortransportlinks', False)
                if Majortransportlinks == 'on':
                    Majortransportlinks = True    
                MeetingRooms = request.POST.get('MeetingRooms', False)
                if MeetingRooms == 'on':
                    MeetingRooms = True    
                cctv= request.POST.get('CCTV', False)
                if cctv== 'on':
                    cctv= True    
                Elevator= request.POST.get('Elevator', False)
                if Elevator== 'on':
                    Elevator= True    

                # media
                featured_image = request.FILES.get('featured_image')
                living_room_media = request.FILES.getlist('living_room_media')
                bedroom_media = request.FILES.getlist('bedroom_media')
                bathroom_media = request.FILES.getlist('bathroom_media')


                # logic
                auto_house_id = request.POST.get('auto_house_id', False)
                is_managedbymanyumba = True
                
                single_units = request.POST.get('single')
                bed_sitter = request.POST.get('bed_sitters')
                one_bedroom = request.POST.get('One_Bedroom')
                Two_Bedroom = request.POST.get('Two_Bedroom')
                Three_Bedroom = request.POST.get('Three_Bedroom')

                single_rent = request.POST.get('single_rent')
                bed_sitters_rent = request.POST.get('bed_sitters_rent')
                one_bedroom_rent = request.POST.get('One_Bedroom_rent')
                Two_Bedroom_rent = request.POST.get('Two_Bedroom_rent')
                Three_Bedroom_rent = request.POST.get('Three_Bedroom_rent')

                total_units = int(single_units) + \
                                int(bed_sitter) + int(one_bedroom) + int(Two_Bedroom) + int(Three_Bedroom)
                                
                default_house_type = ''

                apartment_id = Type.objects.get(name='Apartment').id

                if type == apartment_id:
                    if int(single_units) > 0 and int(bed_sitter) == 0 and int(one_bedroom) == 0:
                        default_house_type = 'Single'
                    elif int(single_units) > 0 and int(bed_sitter) > 0 and int(one_bedroom) == 0:
                        default_house_type = 'Single, Bed-Sitter'
                    elif int(single_units) > 0 and int(bed_sitter) > 0 and int(one_bedroom) > 0:
                        default_house_type = 'Single, Bed-Sitter, One-Bedroom'

                else:
                    default_house_type = 'None'

                                
                # now save to the db.
                new_property = Properties.objects.create(
                    user = request.user,
                    property_title=property_title,
                    description = description,
                    units=int(total_units),
                    available_rooms=int(total_units),
                    default_house_type=default_house_type,
                    type=prop_type,
                    status=prop_status,
                    price = price,
                    area_size = area_size,
                    landsize=prop_landsize,
                    rooms = rooms,
                    bedrooms = bedrooms,
                    bathrooms = bathrooms,
                    garages = garages,
                    managed_by_manyumba = True,
                    publish=pre_publish,
                    city = prop_city,
                    street = street,
                    featured_image = featured_image,  

                         # amenities

                    Water=Water,
                    Electricity=Electricity,
                    WFI=Wifi,
                    Ac=Ac,
                    Gateman=Gateman,
                    Parking=Parking,
                    Swimming_Pool=Swimming_Pool,
                    Balcony=Balcony,
                    Gym=Gym,
                    Play_Area=Play_Area,
                    
                    ElectricSupply=ElectricSupply,
                    WaterSupply=WaterSupply,
                    RainWaterDrainage=RainWaterDrainage,
                    DomesticSewage=DomesticSewage,
                    BusinessLounge=BusinessLounge,
                    Majortransportlinks=Majortransportlinks,
                    MeetingRooms=MeetingRooms,
                    CCTV=cctv,
                    Elevator=Elevator,              
                )
                    
                    # create the houses
                print('we are displaying ids')
                print(type)
                print(apartment_id)
                if int(type) == apartment_id:
                    print('this is a rental aparment')
                    single_loops = int(single_units)
                    bed_sitter_loops = int(bed_sitter)
                    one_bedroom_loops = int(one_bedroom)
                    two_bedroom_loops = int(Two_Bedroom)
                    three_bedromm_loops = int(Three_Bedroom)

                    apartment_loop = Properties.objects.get(pk=new_property.id)

                    # single_loop
                    if auto_house_id:
                        for i in range(1, single_loops + 1):
                            House.objects.create(
                                apartment=apartment_loop,
                                house_code=i,
                                rent=single_rent,
                                deposit=single_rent,
                                house_type='Single',
                            )
                    else:
                        for i in range(1, single_loops + 1):
                            House.objects.create(
                                apartment=apartment_loop,
                                rent=single_rent,
                                deposit=single_rent,
                                house_type='Single',
                            )
                    if auto_house_id:
                        for i in range(single_loops + 1, single_loops + 1 + bed_sitter_loops):
                            House.objects.create(
                                apartment=apartment_loop,
                                house_code=i,
                                rent=bed_sitters_rent,
                                deposit=bed_sitters_rent,
                                house_type='Bed-Sitter',
                            )

                    else:
                        for i in range(0, bed_sitter_loops):
                            House.objects.create(
                                apartment=apartment_loop,
                                rent=bed_sitters_rent,
                                deposit=bed_sitters_rent,
                                house_type='Bed-Sitter',
                            )
                    if auto_house_id:
                        for i in range(single_loops + 1 + bed_sitter_loops,
                                    single_loops + 1 + bed_sitter_loops + one_bedroom_loops):
                            House.objects.create(
                                apartment=apartment_loop,
                                house_code=i,
                                rent=one_bedroom_rent,
                                deposit=one_bedroom_rent,
                                house_type='One Bedroom',
                            )
                    else:
                        for i in range(0, one_bedroom_loops):
                            House.objects.create(
                                apartment=apartment_loop,
                                rent=one_bedroom_rent,
                                deposit=one_bedroom_rent,
                                house_type='One Bedroom',
                            )
                    if auto_house_id:
                        for i in range(single_loops + 1 + bed_sitter_loops + one_bedroom_loops,
                                    single_loops + 1 + bed_sitter_loops + one_bedroom_loops + two_bedroom_loops):
                            House.objects.create(
                                apartment=apartment_loop,
                                house_code=i,
                                rent=Two_Bedroom_rent,
                                deposit=Two_Bedroom_rent,
                                house_type='Two Bedroom',
                            )
                    else:
                        for i in range(0, two_bedroom_loops):
                            House.objects.create(
                                apartment=apartment_loop,
                                rent=Two_Bedroom_rent,
                                deposit=Two_Bedroom_rent,
                                house_type='Two Bedroom',
                            )
                    if auto_house_id:
                        for i in range(single_loops + 1 + bed_sitter_loops + one_bedroom_loops + two_bedroom_loops,
                                    single_loops + 1 + bed_sitter_loops + one_bedroom_loops + two_bedroom_loops + three_bedromm_loops):
                            House.objects.create(
                                apartment=apartment_loop,
                                house_code=i,
                                rent=Three_Bedroom_rent,
                                deposit=Three_Bedroom_rent,
                                house_type='Three Bedroom',
                            )
                    else:
                        for i in range(0, two_bedroom_loops):
                            House.objects.create(
                                apartment=apartment_loop,
                                rent=Three_Bedroom_rent,
                                deposit=Three_Bedroom_rent,
                                house_type='Three Bedroom',
                            )
                else:
                    apartment_loop = Properties.objects.get(pk=new_property.id)
                    type_name = Type.objects.get(id=type).name
                    House.objects.create(
                        apartment=apartment_loop,
                        house_code=1,
                        rent=price,
                        deposit=price,
                        house_type=type_name
                    )

                # save images for the property
                for media in living_room_media:
                    PropertyImages.objects.create(
                        property=new_property,
                        image=media,
                        home_tag='living_room'
                    )
                
                for media in bedroom_media:
                    PropertyImages.objects.create(
                        property=new_property,
                        image=media,
                        home_tag='bed_room'
                    )
                
                for media in bathroom_media:
                    PropertyImages.objects.create(
                        property=new_property,
                        image=media,
                        home_tag='bathroom'
                    )

                # save successfully
                
                messages.success(request, 'Property created successfully')
                return redirect('HouseListing:properties')
            # except:
            #     messages.warning(request, 'There was a problem creating your Listing. Try again')
                
            #     return redirect('HouseListing:properties')



def house_details(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:    
        house = House.objects.get(id=pk)
        active_lease = Lease.objects.filter(house_id=pk, current_status=True)
        terminated_leases = Lease.objects.filter(house_id=pk, current_status=False)
        context = {
            'house': house,
            'active_leases': active_lease,
            'terminated_leases': terminated_leases,
        }
        return render(request, 'HouseListing/house_details.html', context)


def update_house(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:    
        t_house = House.objects.get(id=pk)

        if request.method == 'POST':
            house_code = request.POST.get('house_code')
            rent = request.POST.get('rent')

            parent_apartment = t_house.apartment
            property_houses = parent_apartment.house_set.all()

            for house in property_houses:
                if house.house_code == house_code:
                    t_house.rent = rent
                    t_house.save()
                    messages.success(request, 'Rent updated successfully.')
                    return redirect(request.META.get('HTTP_REFERER'))
                else:
                    t_house.house_code = house_code
                    t_house.rent = rent
                    t_house.save()
                    messages.success(request, 'House details updated successfully.')
                    return redirect(request.META.get('HTTP_REFERER'))
            print(property_houses)



def register_tenant(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        if request.method == 'GET':
            form = TenantRegistrationForm(request.POST or None)
            context = {
                'form': form
            }
            return render(request, 'HouseListing/register_tenant.html', context)
        if request.method == 'POST':
            if request.user.is_authenticated:
                form = TenantRegistrationForm(request.POST or None)
                first_name = form.data['first_name']
                last_name = form.data['last_name']
                phone = form.data['phone']
                gender = form.data['gender']
                id_number = form.data['id_number']
                email = form.data['email']

                Tenant.objects.create(
                    user = request.user,
                    first_name=first_name,
                    last_name=last_name,
                    id_number=id_number,
                    gender=gender,
                    email=email,
                    contact=phone
                )
                messages.success(request, 'Tenant created successfully')
                return redirect('HouseListing:dashboard')
            else:
                messages.warning(request, 'You have to be logged in to perform this action')
                return redirect('HouseListing:dashboard')



def tenants_list(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:    
        properties = Properties.objects.filter(user=request.user, managed_by_manyumba=True,approved_by_admin=1 )
        context = {
            'properties': properties,
        }
        return render(request, 'HouseListing/tenants_list.html', context)


def tenant_sub_list(request, pk):
    all_active_tenants = Lease.objects.filter(apartment__id=pk, current_status=True)
    all_terminated_tenants = Lease.objects.filter(apartment__id=pk, current_status=False)
    this_property = Properties.objects.get(id=pk)

    context = {
        'all_active_tenants': all_active_tenants,
        'all_terminated_tenants': all_terminated_tenants,
        'this_property': this_property,
    }
    return render(request, 'HouseListing/tenant_sub_list.html', context)
def tenant_details(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:    
        tenant = Tenant.objects.get(id=pk)
        all_leases = Lease.objects.filter(tenant=pk)
        # all_invoices = Invoice.objects.filter(tenant=pk)
        context = {
            'tenant': tenant,
            'all_leases': all_leases,
            # 'all_invoices': all_invoices,
        }
        return render(request, 'HouseListing/tenant_details.html', context)

def edit_tenant(request, pk):
    if request.method == 'GET':
        return redirect('HouseListing:dashboard')
    if request.method == 'POST':
        if request.user.is_authenticated:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            phone = request.POST.get('phone')
            gender = request.POST.get('gender')
            id_number = request.POST.get('id_number')
            email = request.POST.get('email')

            tenant_object = Tenant.objects.get(id=pk)
            tenant_object.first_name=first_name
            tenant_object.last_name=last_name
            tenant_object.id_number=id_number
            tenant_object.gender=gender
            tenant_object.email=email
            tenant_object.contact=phone

            tenant_object.save()
            
            messages.success(request, 'Tenant Updated successfully')
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.warning(
                request, 'You have to be logged in to perform this action')
            return redirect('HouseListing:dashboard')


def property_categories(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        if request.method == 'GET':
            categories = PropertyStatus.objects.all()
            context = {
                'categories': categories
            }
            return render(request, 'HouseListing/property_categories.html', context)
        else:
            property_status = request.POST.get('property_status')
            description = request.POST.get('description')

            PropertyStatus.objects.create(
                property_status=property_status,
                description = description,
            )
            messages.success(request, 'Configuration Saved Successfully')
            return redirect('HouseListing:property_categories')


def delete_property_category(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:    
        category = PropertyStatus.objects.get(id=pk)
        category.delete()
        messages.success(request, 'Configuration Deleted Successfully')
        return redirect('HouseListing:property_categories')


def edit_property_categories(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:    
        category = PropertyStatus.objects.get(id=pk)
        property_status = request.POST.get('property_status')
        description = request.POST.get('description')

        category.property_status = property_status
        category.description = description
        category.save()
        messages.success(request, 'Configuration Updated Successfully')
        return redirect('HouseListing:property_categories')


def property_type(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        if request.method == 'GET':
            property_types = Type.objects.all()
            context = {
                'property_types': property_types
            }
            return render(request, 'HouseListing/property_type.html', context)
        else:
            name = request.POST.get('name')
            name = name.capitalize()

            Type.objects.create(
                name=name,
            )
            messages.success(request, 'Configuration Saved Successfully')
            return redirect('HouseListing:property_type')


def delete_property_type(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:    
        type = Type.objects.get(id=pk)
        type.delete()
        messages.success(request, 'Configuration Deleted Successfully')
        return redirect('HouseListing:property_type')


def edit_property_edit(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        type = Type.objects.get(id=pk)
        
        name = request.POST.get('name')

        type.name = name
        type.save()
        messages.success(request, 'Configuration Updated Successfully')
        return redirect('HouseListing:property_type')


def property_cities(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        if request.method == 'GET':
            cities = Cities.objects.all()
            context = {
                'cities': cities
            }
            return render(request, 'HouseListing/property_cities.html', context)
        else:
            city_name = request.POST.get('city_name')

            Cities.objects.create(
                city_name=city_name,
            )
            messages.success(request, 'Configuration Saved Successfully')
            return redirect('HouseListing:property_cities')


def delete_property_city(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        city = Cities.objects.get(id=pk)
        city.delete()
        messages.success(request, 'City Deleted Successfully')
        return redirect('HouseListing:property_cities')


def edit_property_city(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        mycity = Cities.objects.get(id=pk)

        city = request.POST.get('city')

        mycity.city_name = city
        mycity.save()
        messages.success(request, 'City Updated Successfully')
        return redirect('HouseListing:property_cities')


def land_sizes(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        if request.method == 'GET':
            land_sizes = LandSizes.objects.all()
            context = {
                'land_sizes': land_sizes
            }
            return render(request, 'HouseListing/land_sizes.html', context)
        else:
            land_size = request.POST.get('land_size')

            LandSizes.objects.create(
                size=land_size,
            )
            messages.success(request, 'Configuration Saved Successfully')
            return redirect('HouseListing:land_sizes')


def edit_land_sizes(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        land_ = LandSizes.objects.get(id=pk)
        
        land_size = request.POST.get('land_size')

        land_.size = land_size
        land_.save()
        messages.success(request, 'Configuration Updated Successfully')
        return redirect('HouseListing:land_sizes')


def delete_land_size(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        land_ = LandSizes.objects.get(id=pk)
        land_.delete()
        messages.success(request, 'Land Deleted Successfully')
        return redirect('HouseListing:land_sizes')



def register_lease(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        if request.method == "GET":
            form = LeaseForm(request.POST or None)
            context = {
                'form': form,
            }
            return render(request, 'HouseListing/register_lease.html', context)
        if request.method == 'POST':
            form = LeaseForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                lease = form.save(commit=False)
                house = lease.house.id

                lease.lease_documents = request.FILES['lease_documents']
                selected_house = House.objects.get(id=house)
                print(selected_house)
                selected_house.vacant = False
                lease.apartment.available_rooms -= 1
                lease.apartment.save()
                selected_house.save()
                house_object = House.objects.get(id=house)
                rent = house_object.rent
                lease.running_balance = rent

                lease.save()

                lease_object = Lease.objects.filter(
                    house=house_object, current_status=True).first()
                tenant_object = lease_object.tenant
                # generate first invoice.
                apartment = lease.apartment
                amount_incurred = lease.house.rent
                date_generated = datetime.now()

                Invoice.objects.create(
                    apartment=apartment,
                    house=selected_house,
                    lease=lease_object,
                    tenant=tenant_object,
                    amount_incurred=amount_incurred,
                    amount_due=amount_incurred,
                    date_generated=date_generated,
                    previous_over_dues=0,
                )

                messages.success(request, 'Lease created successfully.')
                return redirect('HouseListing:dashboard')
            else:
                print(request.POST)
                print(form.errors)
                messages.warning(request, 'The form is invalid. Please retry.')
                return redirect('HouseListing:dashboard')



def load_houses(request):
    apartment_id = request.GET.get('apartment')
    houses = House.objects.filter(apartment_id=apartment_id, vacant=True)
    context = {
        'houses': houses,
    }
    return render(request, 'HouseListing/house_dropdown.html', context)



def lease_list(request):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        all_active_leases = Lease.objects.filter(current_status=True)
        all_terminated_leases = Lease.objects.filter(current_status=False)

        context = {
            'all_active_leases': all_active_leases,
            'all_terminated_leases': all_terminated_leases,
        }

        return render(request, 'HouseListing/lease_list.html', context)


def terminate_lease(request, pk):
    if not request.user.is_authenticated:
        messages.warning(request, 'Session expired. Please sign in again.')
        return redirect('HouseListing:home')
    else:
        house = House.objects.get(id=pk)
        lease = Lease.objects.filter(house_id=pk, current_status=True).first()
        if lease:
            lease.current_status = False
            lease.save()

            house.vacant = True
            lease.apartment.available_rooms += 1
            lease.apartment.save()
            house.save()
            messages.success(
                request, 'The Lease has been terminated successfully.')
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            messages.warning(request, 'unit has no associated lease.')
            return redirect(request.META.get('HTTP_REFERER'))




# invoices
# def invoice_list(request, pk):
#     all_invoices = Invoice.objects.filter(lease=pk).order_by('-date_generated')
#     all_payments = PaidRent.objects.filter(
#         lease=pk).order_by('-payment_for', '-date_paid')

#     context = {
#         'all_invoices': all_invoices,
#         'my_lease_pk': pk,
#         'all_payments': all_payments,
#     }

#     return render(request, 'Tenants/Invoice_list.html', context)


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        next = request.POST.get('next', None)

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                messages.success(
                    request, 'Logged in Successfully as ' + request.user.username)
                
                if next is not None and next == 'list':
                    return redirect('HouseListing:listing_dashboard')
                elif next is not None and next == 'manage':
                    return redirect('HouseListing:dashboard')
                elif next is not None and next == 'sale_home':
                    return redirect('HouseListing:create_listing_listing')
                else:
                    return redirect('HouseListing:home')


            else:
                messages.warning(request, 'Account not activated')
                return redirect('HouseListing:home')
        else:
            messages.warning(request, 'Invalid Username or Password!')
            return redirect('HouseListing:home')
    return redirect('HouseListing:home')


def logout_user(request):
    logout(request)
    messages.success(request, 'Successfully Logged out.')
    return redirect('HouseListing:home')


# user registration function
def register_user(request):
    if request.method == 'POST':
        next = request.POST.get('next_signup')
        form = UserLogForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print("======")
            print(next)
            username = username.lower()
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'Account Created Successfully')
                    if next is not None and next == 'list':
                        return redirect('HouseListing:listing_dashboard')
                    elif next is not None and next == 'manage':
                        return redirect('HouseListing:dashboard')
                    elif next is not None and next == 'sale_home':
                        return redirect('HouseListing:create_listing_listing')
                    else:
                        return redirect('HouseListing:home')
        context = {
            'form': form,
        }
        print(form.errors)
        messages.warning(request, 'Error. Username already Taken Try another.')
        return redirect('HouseListing:home')
    else:
        form = UserLogForm(request.POST or None)
        context = {
            'form': form,
        }
        return redirect('HouseListing:home')
