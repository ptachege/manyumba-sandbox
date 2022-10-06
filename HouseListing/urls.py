
from django.urls import path
from . import views
app_name = 'HouseListing'
urlpatterns = [



     # listing urls
    path('listing_dashboard/', views.listing_dashboard, name='listing_dashboard'),
    path('create_listing_listing/', views.create_listing_listing, name='create_listing_listing'),
    path('my_listing/', views.my_listing, name='my_listing'),
    path('mylisting_detail/<int:pk>/', views.mylisting_detail, name='mylisting_detail'),
    path('togglePublish/<int:pk>/', views.togglePublish, name='togglePublish'),
    path('listing_profile/', views.listing_profile, name='listing_profile'),
    path('listing_delete_property/<int:pk>/', views.listing_delete_property, name='listing_delete_property'),

    
    

    path('approve_listing/', views.approve_listing, name='approve_listing'),
    path('admin_morgage_leads/', views.admin_morgage_leads, name='admin_morgage_leads'),
    path('approve_property_detail/<int:pk>/', views.approve_property_detail, name='approve_property_detail'),
    path('approve_property/<int:pk>/',
         views.approve_property, name='approve_property'),
    path('reject_property/<int:pk>/',
         views.reject_property, name='reject_property'),
    
    path('property_details/<int:pk>/', views.property_details, name='property_details'),
    path('', views.coming_soon, name='coming_soon'),
    path('home/', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('properties/', views.properties, name='properties'),
    path('create_listing/', views.create_listing, name='create_listing'),
    path('listing_details/<slug:slug>/',
         views.listing_details, name='listing_details'),
     path('listings_for_sale/', views.listings_for_sale, name='listings_for_sale'),
     path('listings_for_rent/', views.listings_for_rent, name='listings_for_rent'),


     # home page search tabs
     path('search_property_for_sale/', views.search_property_for_sale, name='search_property_for_sale'),
     path('search_property_for_rent/', views.search_property_for_rent, name='search_property_for_rent'),
     path('search_property_for_lease/', views.search_property_for_lease, name='search_property_for_lease'),
     path('search_listing_town/<str:town>/', views.search_listing_town, name='search_listing_town'),

    path('house_details/<int:pk>/', views.house_details, name='house_details'),
    path('update_house/<int:pk>/', views.update_house, name='update_house'),
    path('register_tenant/', views.register_tenant, name='register_tenant'),

     #   morgage lead
     path('mortgages_leads/<int:price>/<int:pk>/', views.mortgages_leads, name='mortgages_leads'),
     path('create_morgage_lead/<int:pk>/', views.create_morgage_lead, name='create_morgage_lead'),




    # categories
    path('property_categories/', views.property_categories,
         name='property_categories'),
    path('delete_property_category/<int:pk>/', views.delete_property_category, name='delete_property_category'),
    path('edit_property_categories/<int:pk>/', views.edit_property_categories, name='edit_property_categories'),

    # types
    path('property_type/', views.property_type, name='property_type'),
    path('delete_property_type/<int:pk>/', views.delete_property_type, name='delete_property_type'),
    path('edit_property_edit/<int:pk>/',
         views.edit_property_edit, name='edit_property_edit'),

     # cities
    path('property_cities/', views.property_cities, name='property_cities'),
    path('delete_property_city/<int:pk>/', views.delete_property_city, name='delete_property_city'),
    path('edit_property_city/<int:pk>/', views.edit_property_city, name='edit_property_city'),

    #     land_sizes
    path('land_sizes/', views.land_sizes, name='land_sizes'),
    path('edit_land_sizes/<int:pk>/', views.edit_land_sizes, name='edit_land_sizes'),
    path('delete_land_size/<int:pk>/',
         views.delete_land_size, name='delete_land_size'),


     #  lease
     path('register_lease/', views.register_lease, name='register_lease'),
     path('load_houses', views.load_houses, name='load_houses'),
     path('lease_list', views.lease_list, name='lease_list'),
     path('terminate_lease/<int:pk>/',
          views.terminate_lease, name='terminate_lease'),
     
     # invoice
     # path('invoice_list/<int:pk>/', views.invoice_list, name='invoice_list'),


     # tenants
     path('tenants_list/', views.tenants_list, name='tenants_list'),
     path('tenant_sub_list/<int:pk>/',
          views.tenant_sub_list, name='tenant_sub_list'),
     path('tenant_details/<int:pk>/', views.tenant_details, name='tenant_details'),
     path('edit_tenant/<int:pk>/', views.edit_tenant, name='edit_tenant'),



    # authentication
    path('login_user/', views.login_user, name='login_user'),
    path('logout_user/', views.logout_user, name='logout_user'),
    path('register_user/', views.register_user, name='register_user'),
]
