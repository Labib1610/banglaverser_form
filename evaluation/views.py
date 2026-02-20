from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
import json
import random
import uuid
from .models import DialectData, PlausibilityData, DialectEvaluation, PlausibilityEvaluation


def home(request):
    """
    Homepage that displays the evaluation form.
    """
    dialects = DialectData.DIALECT_CHOICES
    return render(request, 'evaluation/home.html', {
        'dialects': dialects,
    })


@require_http_methods(["GET"])
def get_dialect_data(request):
    """
    API endpoint to get 10 random dialect data items for the selected dialect.
    """
    dialect = request.GET.get('dialect')
    
    if not dialect:
        return JsonResponse({'error': 'No dialect specified'}, status=400)
    
    # Get all items for this dialect
    all_items = list(DialectData.objects.filter(dialect_name=dialect).values(
        'id', 'original_standard_text', 'ai_generated_dialect_text'
    ))
    
    if len(all_items) < 10:
        return JsonResponse({
            'error': f'Not enough data for {dialect}. Found {len(all_items)} items, need at least 10.'
        }, status=400)
    
    # Randomly select 10 items
    selected_items = random.sample(all_items, 10)
    
    return JsonResponse({'data': selected_items})


@require_http_methods(["GET"])
def get_plausibility_data(request):
    """
    API endpoint to get random plausibility data for MCQ evaluation.
    """
    # Get all plausibility items
    all_items = list(PlausibilityData.objects.all().values(
        'id', 'question', 'correct_answer', 
        'wrong_option_1', 'wrong_option_2', 'wrong_option_3'
    ))
    
    if len(all_items) == 0:
        return JsonResponse({'error': 'No plausibility data available'}, status=400)
    
    # Select 10 random items or all if less than 10
    num_items = min(10, len(all_items))
    selected_items = random.sample(all_items, num_items)
    
    return JsonResponse({'data': selected_items})


@require_http_methods(["POST"])
@csrf_exempt
def submit_evaluation(request):
    """
    API endpoint to submit evaluation responses.
    """
    try:
        data = json.loads(request.body)
        session_id = data.get('session_id', str(uuid.uuid4()))
        evaluator_name = data.get('evaluator_name', '')
        evaluator_email = data.get('evaluator_email', '')
        
        # Check if this email has already submitted
        if evaluator_email:
            existing_dialect = DialectEvaluation.objects.filter(evaluator_email=evaluator_email).exists()
            existing_plaus = PlausibilityEvaluation.objects.filter(evaluator_email=evaluator_email).exists()
            if existing_dialect or existing_plaus:
                return JsonResponse({
                    'success': False,
                    'error': 'This email has already submitted an evaluation. Only one submission per email is allowed.'
                }, status=400)
        
        # Save dialect evaluations
        dialect_evaluations = data.get('dialect_evaluations', [])
        for eval_data in dialect_evaluations:
            DialectEvaluation.objects.create(
                dialect_data_id=eval_data['dialect_data_id'],
                evaluator_name=evaluator_name,
                evaluator_email=evaluator_email,
                accuracy_rating=eval_data['accuracy_rating'],
                naturalness_rating=eval_data['naturalness_rating'],
                comments=eval_data.get('comments', ''),
                session_id=session_id
            )
        
        # Save plausibility evaluations
        plausibility_evaluations = data.get('plausibility_evaluations', [])
        for eval_data in plausibility_evaluations:
            PlausibilityEvaluation.objects.create(
                plausibility_data_id=eval_data['plausibility_data_id'],
                evaluator_name=evaluator_name,
                evaluator_email=evaluator_email,
                option_1_plausibility=eval_data['option_1_plausibility'],
                option_2_plausibility=eval_data['option_2_plausibility'],
                option_3_plausibility=eval_data['option_3_plausibility'],
                comments=eval_data.get('comments', ''),
                session_id=session_id
            )
        
        return JsonResponse({
            'success': True,
            'message': 'Evaluation submitted successfully!',
            'session_id': session_id
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


def thank_you(request):
    """
    Thank you page after successful submission.
    """
    return render(request, 'evaluation/thank_you.html')


def export_data(request):
    """
    Export evaluation data as JSON file for download.
    """
    if not request.user.is_staff:
        return redirect('home')
    
    export_type = request.GET.get('type', 'all')
    
    if export_type == 'dialect_data':
        data = serializers.serialize('json', DialectData.objects.all(), indent=2)
        filename = 'dialect_data.json'
    elif export_type == 'plausibility_data':
        data = serializers.serialize('json', PlausibilityData.objects.all(), indent=2)
        filename = 'plausibility_data.json'
    elif export_type == 'dialect_evaluations':
        data = serializers.serialize('json', DialectEvaluation.objects.all(), indent=2)
        filename = 'dialect_evaluations.json'
    elif export_type == 'plausibility_evaluations':
        data = serializers.serialize('json', PlausibilityEvaluation.objects.all(), indent=2)
        filename = 'plausibility_evaluations.json'
    else:  # all
        all_data = {
            'dialect_data': json.loads(serializers.serialize('json', DialectData.objects.all())),
            'plausibility_data': json.loads(serializers.serialize('json', PlausibilityData.objects.all())),
            'dialect_evaluations': json.loads(serializers.serialize('json', DialectEvaluation.objects.all())),
            'plausibility_evaluations': json.loads(serializers.serialize('json', PlausibilityEvaluation.objects.all())),
        }
        data = json.dumps(all_data, indent=2)
        filename = 'all_evaluation_data.json'
    
    response = HttpResponse(data, content_type='application/json')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


def export_page(request):
    """
    Export page with download buttons.
    """
    if not request.user.is_staff:
        return redirect('home')
    
    return render(request, 'evaluation/export.html')
