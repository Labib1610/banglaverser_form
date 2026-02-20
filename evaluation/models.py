from django.db import models


class DialectData(models.Model):
    """
    Model for storing dialect translation pairs.
    Each dialect has 50 pairs of original and AI-generated text.
    """
    DIALECT_CHOICES = [
        ('chittagonian', 'Chittagonian'),
        ('sylheti', 'Sylheti'),
        ('noakhali', 'Noakhali'),
        ('barishal', 'Barishal'),
        ('rangpur', 'Rangpur'),
    ]
    
    dialect_name = models.CharField(max_length=50, choices=DIALECT_CHOICES)
    original_standard_text = models.TextField(help_text="Original standard Bangla text")
    ai_generated_dialect_text = models.TextField(help_text="AI-generated dialectal version")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Dialect Data"
        verbose_name_plural = "Dialect Data"
        ordering = ['dialect_name', 'created_at']
    
    def __str__(self):
        return f"{self.get_dialect_name_display()} - {self.original_standard_text[:50]}..."


class PlausibilityData(models.Model):
    """
    Model for storing MCQ plausibility evaluation data.
    Includes human-made question and correct answer with 3 AI-generated wrong options.
    """
    question = models.TextField(help_text="Human-made question")
    correct_answer = models.TextField(help_text="Human-made correct answer")
    wrong_option_1 = models.TextField(help_text="AI-generated wrong option 1")
    wrong_option_2 = models.TextField(help_text="AI-generated wrong option 2")
    wrong_option_3 = models.TextField(help_text="AI-generated wrong option 3")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Plausibility Data"
        verbose_name_plural = "Plausibility Data"
        ordering = ['created_at']
    
    def __str__(self):
        return f"MCQ: {self.question[:50]}..."


class DialectEvaluation(models.Model):
    """
    Model for storing evaluator responses for dialect data.
    """
    dialect_data = models.ForeignKey(DialectData, on_delete=models.CASCADE, related_name='evaluations')
    evaluator_name = models.CharField(max_length=100, blank=True, null=True)
    evaluator_email = models.EmailField(blank=True, null=True)
    
    # Rating fields (1-5 scale)
    accuracy_rating = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)],
        help_text="How accurate is the dialect translation? (1=Poor, 5=Excellent)"
    )
    naturalness_rating = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)],
        help_text="How natural does the dialect sound? (1=Unnatural, 5=Very Natural)"
    )
    
    comments = models.TextField(blank=True, null=True, help_text="Additional comments")
    created_at = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=100, help_text="Session identifier for grouping responses")
    
    class Meta:
        verbose_name = "Dialect Evaluation"
        verbose_name_plural = "Dialect Evaluations"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Evaluation of {self.dialect_data.dialect_name} by {self.evaluator_name or 'Anonymous'}"


class PlausibilityEvaluation(models.Model):
    """
    Model for storing evaluator responses for plausibility data.
    """
    plausibility_data = models.ForeignKey(PlausibilityData, on_delete=models.CASCADE, related_name='evaluations')
    evaluator_name = models.CharField(max_length=100, blank=True, null=True)
    evaluator_email = models.EmailField(blank=True, null=True)
    
    # Plausibility ratings for each wrong option (1-5 scale)
    option_1_plausibility = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)],
        help_text="How plausible is wrong option 1? (1=Not plausible, 5=Highly plausible)"
    )
    option_2_plausibility = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)],
        help_text="How plausible is wrong option 2? (1=Not plausible, 5=Highly plausible)"
    )
    option_3_plausibility = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)],
        help_text="How plausible is wrong option 3? (1=Not plausible, 5=Highly plausible)"
    )
    
    comments = models.TextField(blank=True, null=True, help_text="Additional comments")
    created_at = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=100, help_text="Session identifier for grouping responses")
    
    class Meta:
        verbose_name = "Plausibility Evaluation"
        verbose_name_plural = "Plausibility Evaluations"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Plausibility evaluation by {self.evaluator_name or 'Anonymous'}"
