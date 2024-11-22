from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Course, Subtitle, Notes
import json

def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/courses.html', {'courses': courses})

def course_detail(request, id):
    course = get_object_or_404(Course, id=id)
    subtitles = Subtitle.objects.filter(course=course)

    if request.method == "POST":
        try:
            # Parse the data from the request
            data = json.loads(request.body)
            content = data.get('content')
            subtitle_id = data.get('subtitle_id')
            note_id = data.get('note_id')  # For updates, note_id will be provided

            if not content:
                return JsonResponse({'success': False, 'error': 'Content cannot be empty'})

            if note_id:
                # Update existing note
                note = get_object_or_404(Notes, id=note_id)
                note.content = content
                note.save()
                return JsonResponse({'success': True, 'message': 'Note updated successfully'})
            else:
                # Create a new note
                subtitle = get_object_or_404(Subtitle, id=subtitle_id)
                note = Notes.objects.create(
                    subtitle=subtitle,
                    title=f"{subtitle.name} Notes",
                    content=content,
                )
                return JsonResponse({'success': True, 'message': 'Note created successfully'})

        except Exception as e:
            print(f"Error processing request: {e}")  # Debugging info
            return JsonResponse({'success': False, 'error': str(e)})

    return render(request, 'courses/course_detail.html', {'course': course, 'subtitles': subtitles})

def delete_note(request):
    if request.method == "POST":
        try:
            # Parse the data from the request
            data = json.loads(request.body)
            note_id = data.get('note_id')

            if not note_id:
                return JsonResponse({'success': False, 'error': 'Note ID is required'})

            # Delete the note
            note = get_object_or_404(Notes, id=note_id)
            note.delete()
            return JsonResponse({'success': True, 'message': 'Note deleted successfully'})

        except Exception as e:
            print(f"Error deleting note: {e}")  # Debugging info
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def update_note(request):
    if request.method == "POST":
        try:
            # Parse the data from the request
            data = json.loads(request.body)
            note_id = data.get('note_id')
            content = data.get('content')

            if not note_id or not content:
                return JsonResponse({'success': False, 'error': 'Note ID and content are required'})

            # Update the note
            note = get_object_or_404(Notes, id=note_id)
            note.content = content
            note.save()
            return JsonResponse({'success': True, 'message': 'Note updated successfully'})

        except Exception as e:
            print(f"Error updating note: {e}")  # Debugging info
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Subtitle, Notes
import json

def create_note(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            subtitle_id = data.get("subtitle_id")
            content = data.get("content")

            if not content or not subtitle_id:
                return JsonResponse({'success': False, 'error': 'Invalid data'})

            subtitle = get_object_or_404(Subtitle, id=subtitle_id)

            note = Notes.objects.create(
                subtitle=subtitle,
                title=f"{subtitle.name} Notes",  # Default title
                content=content,
            )

            return JsonResponse({'success': True, 'message': 'Note created successfully'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})
