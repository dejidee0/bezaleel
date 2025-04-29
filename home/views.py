from property import settings
from property.settings import SUPABASE_STORAGE_BUCKET

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from property.decorators import verified_user_required
from .models import Property, PropertyImage
from .forms import ContactForm, DirectContactForm
from django.contrib import messages
from django.core.mail import send_mail


def index(request):
    properties = Property.objects.all()
    
    return render(request, 'properties/index.html', {'properties': properties, })

def property_detail(request, property_id):
    property = get_object_or_404(Property, pk=property_id)
    images = PropertyImage.objects.filter(property=property)
    return render(request, 'properties/property-details.html', {'property': property, 'images': images})

@verified_user_required
def dashboard(request):
    user = request.user  # Get the currently logged-in user
    properties = Property.objects.filter(agent=user)

    # Count properties by status
    # approved_count = properties.filter(status='approved').count()
    sold_count = properties.filter(status='sold').count()
    rented_count = properties.filter(status='rented').count()
    # pending_count = properties.filter(status='pending').count()

    total_properties = sold_count + rented_count

    return render(request, 'properties/dashboard.html', {
        'user': user,
        'properties': properties,
        'total_properties': total_properties,
        # 'approved_count': approved_count,
        'sold_count': sold_count,
        'rented_count': rented_count,
        # 'pending_count': pending_count,
    })


@verified_user_required
def add_property(request):
    if request.method == 'POST':
        # Extract data from the request
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        address = request.POST.get('address', '').strip()
        zip_code = request.POST.get('zip_code', '').strip()
        country = request.POST.get('country', '').strip()
        state = request.POST.get('state', '').strip()
        label = request.POST.get('label', '').strip()
        size = request.POST.get('size', '').strip()
        land_area = request.POST.get('land_area', '').strip()
        rooms = request.POST.get('rooms', '').strip()
        bedrooms = request.POST.get('bedrooms', '').strip()
        bathrooms = request.POST.get('bathrooms', '').strip()
        year_built = request.POST.get('year_built', '').strip()
        video_url = request.POST.get('video_url', '').strip()
        price = request.POST.get('price', '').strip()
        images = request.FILES.getlist('images')  # Handle multiple images

        # Validation
        if not title or not description or not price:
            messages.error(request, 'Title, description, and price are required.')
            return render(request, 'properties/add-property.html', {'user': request.user})

        try:
            price = float(price)
            if price <= 0:
                raise ValueError("Price must be greater than zero.")
        except ValueError:
            messages.error(request, 'Invalid price. Please enter a positive number.')
            return render(request, 'properties/add-property.html', {'user': request.user})

        # Attempt to create the property
        try:
            user = request.user
            property_instance = Property.objects.create(
                title=title,
                description=description,
                address=address if address else None,
                zip_code=zip_code if zip_code else None,
                country=country if country else None,
                state=state if state else None,
                label=label if label else None,
                size=float(size) if size else None,
                land_area=float(land_area) if land_area else None,
                rooms=int(rooms) if rooms else None,
                bedrooms=int(bedrooms) if bedrooms else None,
                bathrooms=int(bathrooms) if bathrooms else None,
                year_built=int(year_built) if year_built else None,
                video_url=video_url if video_url else None,
                price=price,
                agent=user,
                status='approved'
            )

            file_url = None

            # Save images (if provided)
            if images:
                for image in images:

                    PropertyImage.objects.create(property=property_instance, image=images)

            # Success message
            messages.success(request, 'Property added successfully!')

            # Redirect to avoid re-posting form data
            return redirect('add_property')

        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
            return render(request, 'properties/add-property.html', {'user': request.user})

    return render(request, 'properties/add-property.html', {'user': request.user})


def all_properties(request):
    properties = Property.objects.all()
    latest = Property.objects.order_by('-created_at')[:4]

    # Filtering
    if 'title' in request.GET and request.GET['title']:
        properties = properties.filter(title__icontains=request.GET['title'])

    if 'keyword' in request.GET and request.GET['keyword']:
        properties = properties.filter(description__icontains=request.GET['keyword'])

    # Filter by address
    if 'address' in request.GET and request.GET['address']:
        properties = properties.filter(address__icontains=request.GET['address'])

    # Filter by price 
    if 'price' in request.GET and request.GET['price']:
        properties = properties.filter(price__gte=request.GET['price'])

    # Filter by bedrooms
    if 'bedrooms' in request.GET and request.GET['bedrooms']:
        properties = properties.filter(bedrooms=request.GET['bedrooms'])

    if 'rooms' in request.GET and request.GET['rooms']:
        properties = properties.filter(rooms=request.GET['rooms'])


    # Filter by bathrooms
    if 'bathrooms' in request.GET and request.GET['bathrooms']:
        properties = properties.filter(bathrooms=request.GET['bathrooms'])

    # Filter by size 
    if 'size' in request.GET and request.GET['size']:
        properties = properties.filter(size__gte=request.GET['size'])
   
    # Filter by label 
    if 'type' in request.GET and request.GET['type']:
        properties = properties.filter(label=request.GET['type'])
   


    # Pagination
    page = request.GET.get("page", 1)
    per_page = request.GET.get("per_page", 6)  # Default to 10 items per page

    paginator = Paginator(properties, per_page)

    try:
        properties_page = paginator.page(page)
    except PageNotAnInteger:
        properties_page = paginator.page(1)
    except EmptyPage:
        properties_page = paginator.page(paginator.num_pages)

    return render(request, "properties/all-properties.html", {"properties": properties_page, "latest": latest,})


@verified_user_required
def my_profile(request):
    user = request.user
    return render(request, 'properties/my-profile.html', {'user': user})   

# def verification_required(request):
#     return render(request, 'properties/verification_required.html')

# def pricing(request):
#     return render(request, 'properties/pricing.html')

def about(request):
    return render(request, 'properties/about-us.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Extract form data
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            # Send the email
            subject = f'Contact Form Submission from {name}'
            body = f'Message from {name} ({email}, {phone}):\n\n{message}'
            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [settings.DEFAULT_FROM_EMAIL])

            messages.success(request, 'Your enquiry has been successfully submitted. We will get back to you shortly.')

            # You can send a confirmation email to the user as well
            user_subject = 'Thank you for contacting us'
            user_body = f'Hello {name},\n\nThank you for your message. We will get back to you shortly.\n\nYour message:\n{message}'
            send_mail(user_subject, user_body, settings.DEFAULT_FROM_EMAIL, [email])
        else:
            messages.error(request, 'There was an error submitting your enquiry. Please try again.')


    else:
        form = ContactForm()

    return render(request, 'properties/contact.html', {'form': form})

def faq(request):
    return render(request, 'properties/faq.html')

def services(request):
    return render(request, 'properties/our-service.html')

def direct_contact(request):
    if request.method == 'POST':
        form = DirectContactForm(request.POST)
        if form.is_valid():
            # Process the form data, such as sending an email
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            phone = form.cleaned_data['phone']
            message = form.cleaned_data['message']
            
            # Send the email
            subject = f'IMPORTANT: Product Enquiry Submitted from {name}'
            body = f'Message from {name} ({email}, {phone}):\n\n{message}'
            send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [settings.DEFAULT_FROM_EMAIL])

            messages.success(request, 'Your enquiry has been successfully submitted. We will get back to you shortly.')

            # You can send a confirmation email to the user as well
            user_subject = 'Thank you for placing your enquiry'
            user_body = f'Hello {name},\n\nThank you for your message. We will get back to you shortly.\n\nYour message:\n{message}'
            send_mail(user_subject, user_body, settings.DEFAULT_FROM_EMAIL, [email])
        else:
            messages.error(request, 'There was an error submitting your enquiry. Please try again.')


    else:
        form = DirectContactForm()

    return render(request, 'properties/direct-contact.html', {'form': form})

def category_properties(request, category):
    if request.method == "GET":
        # Filter properties by category and approved status
        properties = Property.objects.filter(category=category, status="approved")

        # Convert queryset to list of dicts (not needed unless JSON response is required)
        property_list = list(properties.values())

        print(f"Length is {len(property_list)}")  # Fixed length() method error

        if len(property_list) > 0:
            page = request.GET.get("page", 1)
            per_page = request.GET.get("per_page", 12)  # Default to 12 items per page

            paginator = Paginator(properties, per_page)

            try:
                properties_page = paginator.page(page)
            except PageNotAnInteger:
                properties_page = paginator.page(1)
            except EmptyPage:
                properties_page = paginator.page(paginator.num_pages)

            return render(request, "properties/category.html", {"properties": properties_page})

    return render(request, "properties/category.html")