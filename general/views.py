from django.views.generic.create_update import update_object
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response
from django.http import Http404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext

from django.contrib.auth.models import User
import general.models as models
import general.forms as forms

def nope(request) :
    return render_to_response('general/need_more_privs.html', locals(), context_instance=RequestContext(request))

def view_profile(request, username):
    view_user = get_object_or_404(User, username=username)
    datadict = locals()

    profile = view_user.get_profile()
    privacyok = False
    if profile.privacy_groupsonly :
        if request.user.is_authenticated() :
            lu = request.user
            for org in view_user.organizations.all() :
                if lu in org.members.all() :
                    privacyok = True
                    break
    else :
        privacyok = True

    datadict['privacyok'] = privacyok
    return render_to_response('general/userprofile_detail.html', datadict, context_instance=RequestContext(request))

@csrf_protect
@login_required
def edit_profile(request):
    return update_object(request, form_class=forms.UserProfileForm, object_id=request.user.get_profile().pk, extra_context={'user':request.user, })

def view_workinggroup(request, id):
    workinggroup = get_object_or_404(models.WorkingGroup, id=id)
    return render_to_response('general/workinggroup_detail.html', locals(), context_instance=RequestContext(request))

def view_project(request, id):
    project = get_object_or_404(models.Project, id=id)
    
    if not project.can_user(request.user, models.Project.P_READ) :
        return nope(request)
    
    return render_to_response('general/project_detail.html', locals(), context_instance=RequestContext(request))

@csrf_protect
@login_required
def leave_organization(request, object_id):
    if request.method == "POST":
        org = get_object_or_404(models.Organization, id = object_id)
        org.members.remove(request.user)
        messages.add_message(request, messages.INFO, 'You have left %s' % org.name)
    return HttpResponseRedirect(reverse('organization_detail', kwargs={'object_id':org.id}))

@csrf_protect
@login_required
def join_organization(request, object_id):
    if request.method == "POST":
        org = get_object_or_404(models.Organization, id = object_id)
        org.members.add(request.user)
        messages.add_message(request, messages.INFO, 'You have joined %s' % org.name)
    return HttpResponseRedirect(reverse('organization_detail', kwargs={'object_id':org.id}))

@csrf_protect
@login_required
def remove_resource(request, resource_id):
    if request.method == "POST":
        org = get_object_or_404(models.Organization, id = request.POST.get('org_id', 0))
        resource = get_object_or_404(models.Resource, id = resource_id)
        org.resources.remove(resource)
        messages.add_message(request, messages.INFO, 'You have removed your %s from your inventory' % resource.name)
    return HttpResponseRedirect(reverse('resource_detail', kwargs={'object_id':resource.id}))

@csrf_protect
@login_required
def add_resource(request, resource_id):
    if request.method == "POST":
        org = get_object_or_404(models.Organization, id = request.POST.get('org_id', 0))
        resource = get_object_or_404(models.Resource, id = resource_id)
        org.resources.add(resource)
        messages.add_message(request, messages.INFO, 'You have added %s to your inventory' % resource.name)
    return HttpResponseRedirect(reverse('resource_detail', kwargs={'object_id':resource.id}))

@csrf_protect
@login_required
def add_skill(request, object_id):
    skill = get_object_or_404(models.Skill, id = object_id)
    profile = request.user.get_profile()
    profile.skills.add(skill)
    messages.add_message(request, messages.INFO, 'You have added %s to your skills' % skill.title)
    return HttpResponseRedirect(reverse('skill_detail', kwargs={'object_id':skill.id}))

@csrf_protect
@login_required
def remove_skill(request, object_id):
    skill = get_object_or_404(models.Skill, id = object_id)
    profile = request.user.get_profile()
    profile.skills.remove(skill)
    messages.add_message(request, messages.INFO, 'You have removed %s from your skills' % skill.title)
    return HttpResponseRedirect(reverse('skill_detail', kwargs={'object_id':skill.id}))

def search(request):
    q = request.GET.get('q', '')
    results = [
        ('Groups', models.Organization.search(q)),
        ('Resources', models.Resource.search(q)),
        ('Skills', models.Skill.search(q)),
        ('Working Groups', models.WorkingGroup.search(q)),
        ('Projects', models.Project.search(q)),
    ]

    results = filter(lambda x: x[1].count() > 0, results)

    return render_to_response('general/search_results.html', locals(), context_instance=RequestContext(request))

