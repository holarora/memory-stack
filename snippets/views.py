from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.template import loader
from .models import Task
from .forms import SearchForm, TaskForm, StepForm, EditTaskForm


# Create your views here.
def alltasks(request):
    search_form = SearchForm(request.GET or None)
    mytasks = Task.objects.all().order_by("duedate")  ##or "-duedate" for reverse
    num_tasks = mytasks.count()

    if search_form.is_valid():
        query = search_form.cleaned_data["query"]
        mytasks = Task.objects.filter(taskName__icontains=query)
        num_tasks = mytasks.count()

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            print(form.cleaned_data)
            return redirect("alltasks")
    else:
        form = TaskForm()
    template = loader.get_template("snippets/alltasks.html")
    context = {
        "mytasks": mytasks,
        "total_number_of_tasks": num_tasks,
        "form": form,
        "search_form": search_form,
    }
    return HttpResponse(template.render(context, request))


def onetask(request, slug):
    task = get_object_or_404(Task, slug=slug)

    if request.method == "POST":
        form = StepForm(request.POST)
        if form.is_valid():
            new_step = form.save(commit=False)
            new_step.task = task
            new_step.save()
            print(form.cleaned_data)
            return redirect("onetask", slug=slug)
    else:
        form = StepForm()

    context = {
        "content": task.memo,
        "name": task.taskName,
        "steps": task.step_set.all(),
        "form": form,
    }
    return render(request, "snippets/task.html", context)


def edit_task(request, slug):
    task = get_object_or_404(Task, slug=slug)

    if request.method == "POST":
        form = EditTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            print(form.cleaned_data)
            return redirect("alltasks")
    else:
        form = EditTaskForm(instance=task)

    context = {
        "form": form,
        "task": task,
    }
    return render(request, "snippets/editTask.html", context)
