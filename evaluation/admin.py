from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from .models import DialectData, PlausibilityData, DialectEvaluation, PlausibilityEvaluation


class CustomAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('export/', lambda request: redirect('/export/'), name='export_redirect'),
        ]
        return custom_urls + urls


# Override default admin site
admin.site.__class__ = CustomAdminSite


@admin.register(DialectData)
class DialectDataAdmin(admin.ModelAdmin):
    list_display = ['dialect_name', 'original_text_preview', 'ai_text_preview', 'created_at']
    list_filter = ['dialect_name', 'created_at']
    search_fields = ['original_standard_text', 'ai_generated_dialect_text']
    
    def original_text_preview(self, obj):
        return obj.original_standard_text[:50] + "..." if len(obj.original_standard_text) > 50 else obj.original_standard_text
    original_text_preview.short_description = "Original Text"
    
    def ai_text_preview(self, obj):
        return obj.ai_generated_dialect_text[:50] + "..." if len(obj.ai_generated_dialect_text) > 50 else obj.ai_generated_dialect_text
    ai_text_preview.short_description = "AI Generated Text"


@admin.register(PlausibilityData)
class PlausibilityDataAdmin(admin.ModelAdmin):
    list_display = ['question_preview', 'correct_answer_preview', 'created_at']
    search_fields = ['question', 'correct_answer']
    
    def question_preview(self, obj):
        return obj.question[:60] + "..." if len(obj.question) > 60 else obj.question
    question_preview.short_description = "Question"
    
    def correct_answer_preview(self, obj):
        return obj.correct_answer[:40] + "..." if len(obj.correct_answer) > 40 else obj.correct_answer
    correct_answer_preview.short_description = "Correct Answer"


@admin.register(DialectEvaluation)
class DialectEvaluationAdmin(admin.ModelAdmin):
    list_display = ['dialect_data', 'evaluator_name', 'accuracy_rating', 'naturalness_rating', 'created_at']
    list_filter = ['created_at', 'accuracy_rating', 'naturalness_rating']
    search_fields = ['evaluator_name', 'evaluator_email', 'comments']
    readonly_fields = ['created_at']


@admin.register(PlausibilityEvaluation)
class PlausibilityEvaluationAdmin(admin.ModelAdmin):
    list_display = ['plausibility_data', 'evaluator_name', 'option_1_plausibility', 'option_2_plausibility', 'option_3_plausibility', 'created_at']
    list_filter = ['created_at']
    search_fields = ['evaluator_name', 'evaluator_email', 'comments']
    readonly_fields = ['created_at']
