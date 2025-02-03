from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
# from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from . import models,serializers
from rest_framework import viewsets

#Query speed check
from django.db import connection

from django.core.mail import send_mail

def send_test_email(request):
    subject = 'Test Email'
    message = 'This is a test email sent from Django.'
    email_from = 'adilnaseem.pak@gmail.com'
    recipient_list = ['adilnaseem.pak@gmail.com',]
    send_mail(subject, message, email_from, recipient_list)
    return HttpResponse('Email sent successfully!')
#------------Celery----------start
from django.http import JsonResponse
from .tasks import add
from celery.result import AsyncResult
def trigger_task(request):
    result = add.delay(4, 4)
    return JsonResponse({'task_id': result.id})

def index(request):
    result = add.delay(4, 4)
    return HttpResponse(f'Task result: {result.get()}')

def get_task_status(request, task_id):
    result = AsyncResult(task_id)
    response_data = {
        'task_id': task_id,
        'status': result.status,
        'result': result.result if result.ready() else None
    }
    return JsonResponse(response_data)
#------------Celery----------end
@method_decorator(login_required, name='dispatch')
class EmployeeView(TemplateView):
    # our hybrid template, shown above
    template_name = 'myapp/employee_home.html'

    def get_context_data(self, **kwargs):
        # passing the department choices to the template in the context
        return {
            'department_choices': [{
                'id': c[0],
                'name': c[1]
            } for c in models.Employee.DEPARTMENT_CHOICES],
        }
class EmployeeViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.EmployeeSerializer

    def get_queryset(self):
        # filter queryset based on logged in user
        return self.request.user.employees.all()

    def perform_create(self, serializer):
        # ensure current user is correctly populated on new objects
        serializer.save(user=self.request.user)
#--------------------
from django.http import HttpResponse
from . import models
from .forms import LoginForm
from . import forms

from django.template import loader
from django.utils.html import format_html


#'manufacturer', 'made_in', 'serial_no', 'type__title', 'title', 'model', 'status__title',  'date_of_manufacturing', 'place_of_installation__sector','place_of_installation__duty_point', 'description'
# @method_decorator(login_required)
from django.views.generic import ListView
def home(request):
    result = add.delay(10, 4)
    print(result)
    new_dic={}
    hand_dic={}
    hold_dic={}
    data = models.Equipment.objects.values( 'status__title','model','type__title')
    hand_data = models.Equipment.objects.filter(type__title__icontains='Hand').values( 'status__title')
    hold_data = models.Equipment.objects.filter(type__title__icontains='Hold').values( 'status__title')
    # print((hold_data))
    for x in hand_data:
        if x['status__title'] not in hand_dic:
            hand_dic[x['status__title']]=1
        elif x['status__title'] in hand_dic:
            hand_dic[x['status__title']]=1+hand_dic[x['status__title']]
    hand_categories = list(hand_dic.keys())
    hand_values = list(hand_dic.values())

    for x1 in hold_data:
        # print(x1)
        if x1['status__title'] not in hold_dic:
            hold_dic[x1['status__title']]=1
        elif x1['status__title'] in hold_dic:
            hold_dic[x1['status__title']]=1+hold_dic[x1['status__title']]
        # print(hold_dic)
    hold_categories = list(hold_dic.keys())
    hold_values = list(hold_dic.values())
    # print(hold_data)
    try:
        for point1 in data:
            for point in point1:    
                if point not in new_dic:
                    new_dic[point] = {}
                    if point1[point] not in new_dic[point]:
                        new_dic[point][point1[point]] = 1
                elif point in new_dic:
                    
                    if point1[point] not in new_dic[point]:
                        new_dic[point][point1[point]] = 1
                    elif point1[point] in new_dic[point]:
                        new_dic[point][point1[point]] = new_dic[point][point1[point]]+1
    

        new_dic['model']=dict(sorted(new_dic['model'].items(), key=lambda x: x[1], reverse=True))        
        
        categories = list(new_dic['status__title'].keys())
    
        values = list(new_dic['status__title'].values())
        model_categories=list(new_dic['model'].keys())
        model_values=list(new_dic['model'].values())
        type_categories = list(new_dic['status__title'].keys())
    
        values = list(new_dic['status__title'].values())
    except:
        categories=[]
        values=[]
        model_categories=[]
        model_values=[]
    queries = connection.queries
    # for query in queries:
        # print(query)
    
    return render(request, 'home.html', {
        'categories': categories,
        'values': values,
        'hold_categories': hold_categories,
        'hold_values': hold_values,
        'hand_categories': hand_categories,
        'hand_values': hand_values,
        'model_categories':model_categories,
        'model_values':model_values,
    })
def airport_form(request):
    if request.method == 'POST':
        form = forms.Airport(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by = request.user
            
            instance.save()
            return redirect('home')
    else:
        form = forms.Airport()
    return render(request, 'airport_form.html', {'form': form})
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import Group, User
def Exap(request):
    admin_group = Group.objects.get(name='admin')
    # Get all users in the admin group
    admin_users = admin_group.user_set.all()

    # Add a user to the admin group
    user = User.objects.get(username='johndoe')
    user.groups.add(admin_group)

    
def eqp(request):
    # employee = get_object_or_404(models.Employee, user=request.user)
    # equipment = models.Equipment.objects.filter(airport=employee.airport)
    if request.method=="POST":
        field=request.POST.get('field')
        pram=request.POST.get('pram')
        query=request.POST.get('query')
        # print([field,query])
        querset=models.Equipment.objects.filter(**{f'{field}__{pram}':query}).values( 'id','manufacturer', 'made_in', 'serial_no', 'type__title', 'title', 'model', 'status__title',  'date_of_manufacturing', 'place_of_installation__sector','place_of_installation__duty_point', 'description')
        paginator = Paginator(querset, 40)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        queries = connection.queries
        # for query in queries:
            # print(query)
        return render(request,template_name='eqp.html',context={'page_obj':page_obj})
    
    else:
        querset = models.Equipment.objects.values()
        
        querset = models.Equipment.objects.values( 'id','manufacturer', 'made_in', 'serial_no', 'type__title', 'title', 'model', 'status__title', 'date_of_manufacturing', 'place_of_installation__sector','place_of_installation__duty_point', 'description')
        paginator = Paginator(querset, 40)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        queries = connection.queries
        # for query in queries:
            # print(query)
        return render(request,template_name='eqp.html',context={"page_obj": page_obj},)
        
@permission_required('home.can_add_equipment', raise_exception=True)
def data_entry_view(request):
    if request.method == 'POST':
        form = forms.EqptForm(request.POST)
        if form.is_valid():
            form.save()  # Only if using ModelForm
            return redirect('home')  # Redirect to a success page or another view
    else:
        form = forms.EqptForm()
    
    return render(request, 'eqptform.html', {'form': form})
def eqp_details(request,id):
    lis=[]
    ids=list(models.Repair.objects.filter(equipment__id=id).values_list('id',flat=True))
    for id2 in ids:
        staff_det = list(models.Repair.objects.filter(id=id2).values('staff__force_no','staff__name',))
        repair = list(models.Repair.objects.filter(id=id2).values('id', 'title', 'repair_type', 'equipment__title','description'))
        repair[0]['staff']=staff_det
        lis.append(repair[0])
    mymember = models.Equipment.objects.filter(id=id).values( 'manufacturer', 'made_in', 'serial_no', 'type__title', 'title', 'model', 'status__title',  'date_of_manufacturing', 'place_of_installation__sector','place_of_installation__duty_point', 'description')
    dic={}
    for x in mymember:
        for item in x:
            dic[item.split('__')[0].replace('_',' ').title()]=x[item]
    context = {
        'set': dic,
        'lis':lis,
        'pk':id
    }
    return render(request,template_name='eqp_detail.html',context=context)

# Update
@permission_required('home.can_change_equipment', raise_exception=True)
def equipment_update(request, id):
    equipment = get_object_or_404(models.Equipment, pk=id)
    if request.method == 'POST':
        form = forms.EqptForm(request.POST, instance=equipment)
        if form.is_valid():
            form.save()
            return redirect('eqp')
    else:
        form = forms.EqptForm(instance=equipment)
    return render(request, 'eqptform.html', {'form': form})
# Delete
@permission_required('home.can_delete_equipment', raise_exception=True)
def equipment_delete(request, id):
    equipment = get_object_or_404(models.Equipment, pk=id)
    if request.method == 'POST':
        equipment.delete()
        return redirect('eqp')
    return render(request, 'equipment_confirm_delete.html', {'equipment': equipment})
from django.core.exceptions import PermissionDenied

def custom_permission_denied_view(request, exception):
    return render(request, '403.html', status=403)


def staff(request):
    
    qset = models.Staff.objects.all()
    return render(request=request,template_name='staff.html', context={'set':qset})
# Create your views here.
def staff_form(request):
    # Get a group by name
    assign_group, created = Group.objects.get_or_create(name='Staff')
    
    if request.method == 'POST':
        form = forms.StaffForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.created_by = request.user
            instance.save()
            user = User.objects.get(username=instance.cnic)
            user.groups.add(assign_group)
            return redirect('staff')  # Redirect to a success page or another view
    else:
        form = forms.StaffForm()
    
    return render(request, 'form_repairs.html', {'form': form})

def sign_in(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('home')
  
        form = LoginForm()
        return render(request,'login.html', {'form': form})
    
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password=form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user:
                login(request, user)
                messages.success(request,f'Hi {username.title()}, welcome back!')
                return redirect('home')
        
        # either form not valid or user is not authenticated
        messages.error(request,f'Invalid username or password')
        return render(request,'login.html',{'form': form})

def sign_out(request):
    logout(request)
    messages.success(request,f'You have been logged out.')
    return redirect('home')  

# def eptFormView(request):
#     context = {}
#     context['form'] = forms.EqptForm()
#     return render(request, 'eqptform.html',context)

#--------------------

def repairs(request):
    lis=[]
    ids = list(models.Repair.objects.values_list('id',flat=True))
    for i in ids:
        
        repair_staff= models.Repair.objects.filter(pk=i).values('staff__force_no','staff__name',)
        repair = models.Repair.objects.filter(pk=i).values('id', 'title','date', 'repair_type','equipment__serial_no', 'equipment__title','description')
        for dic in repair:
            dic['staff']=list(repair_staff)

        
            lis.append(dic)
    return render(request,template_name='repairs.html',context={'set':lis})

def repair_form(request):
    if request.method == 'POST':
        form = forms.RepairForm(request.POST)
        if form.is_valid():
            form.save()  # Only if using ModelForm
            return redirect('home')  # Redirect to a success page or another view
    else:
        form = forms.RepairForm()
    # print(form.related_field.choices)
    
    return render(request, 'form_repairs.html', {'form': form})


#-------------
def search_view(request):
    all_people = models.Equipment.objects.all()
    context = {'count': all_people.count()}
    return render(request, 'search.html', context)


def search_results_view(request):
    query = request.GET.get('search', '')
    # print(f'{query = }')

    all_people = models.Equipment.objects.all()
    if query:
        people = all_people.filter(title__icontains=query)
        highlighted_people = [{'name': highlight_matched_text(models.Equipment.title, query), 'description': models.Equipment.serial_no}
                              for models.Equipment in people]
    else:
        highlighted_people = []

    context = {'people': highlighted_people, 'count': all_people.count()}
    return render(request, 'search_results.html', context)


def highlight_matched_text(text, query):
    """
    Inserts html around the matched text.
    """
    start = text.lower().find(query.lower())
    if start == -1:
        return text
    end = start + len(query)
    highlighted = format_html('<span class="highlight">{}</span>', text[start:end])
    return format_html('{}{}{}', text[:start], highlighted, text[end:])



def log_list(request):
    logs = models.ChangeLog.objects.all().order_by('-timestamp')
    return render(request, 'log_list.html', {'logs': logs})

#--------------Serializers--------
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from . import serializers
# class api(APIView):
#     # @api_view(['GET'])
#     def apiGet(self,request):
#         app = models.Equipment.objects.all()
#         serializer = serializers.EquipmentSerializer(app, many=True)
#         return Response(serializer.data)

#     # @api_view(['POST'])
#     def apiPost(self,request):
#         serializer = models.Equipment(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         return Response(serializer.data)
#     #-----===========================================
from rest_framework import viewsets, permissions
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from django_filters.rest_framework import DjangoFilterBackend
from .models import Equipment
from .serializers import EquipmentSerializer
from .filters import EquipmentFilter
class ItemViewSet(viewsets.ModelViewSet):
    queryset = models.Equipment.objects.all()
    serializer_class = EquipmentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = EquipmentFilter
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
class EqptTypeViewSet(viewsets.ModelViewSet):
    queryset = models.EqptType.objects.all()
    serializer_class = serializers.EquipmentTypeSerializer
#///////////////////////////////////////////

# @api_view(['GET', 'POST'])
# def snippet_list(request):
#     """
#     List all code snippets, or create a new snippet.
#     """
#     if request.method == 'GET':
#         snippets = models.Equipment.objects.all()
#         serializer = serializers.EquipmentSerializer (snippets, many=True)
#         return Response(serializer.data)

#     elif request.method == 'POST':
#         serializer = models.Equipment(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# def dropdownsearch(request):
  
    