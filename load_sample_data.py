"""
Sample script to load data into the database.
Modify this script with your actual data and run: python manage.py shell < load_sample_data.py
"""

from evaluation.models import DialectData, PlausibilityData

# Sample Dialect Data
# You should replace these with your actual 50 items per dialect

dialect_samples = {
    'chittagonian': [
        {
            'original': 'আমি ভাত খাই',
            'generated': 'আঁই ভাত খাঁই'
        },
        {
            'original': 'তুমি কোথায় যাও?',
            'generated': 'তুঁই কুন্ঠে যাঁও?'
        },
        {
            'original': 'সে বই পড়ছে',
            'generated': 'তিনি বই পড়তে'
        },
        # Add 47 more items to reach 50
    ],
    'sylheti': [
        {
            'original': 'আমি ভাত খাই',
            'generated': 'আমি ভাত খাই'  # Replace with actual Sylheti
        },
        # Add 49 more items
    ],
    'noakhali': [
        {
            'original': 'আমি ভাত খাই',
            'generated': 'আমি ভাত খাইগা'  # Replace with actual Noakhali
        },
        # Add 49 more items
    ],
    'barishal': [
        {
            'original': 'আমি ভাত খাই',
            'generated': 'আমি ভাত খাইয়্যা'  # Replace with actual Barishal
        },
        # Add 49 more items
    ],
    'rangpur': [
        {
            'original': 'আমি ভাত খাই',
            'generated': 'আমি ভাত খাইরাম'  # Replace with actual Rangpur
        },
        # Add 49 more items
    ]
}

# Load dialect data
print("Loading dialect data...")
for dialect_name, samples in dialect_samples.items():
    for sample in samples:
        DialectData.objects.get_or_create(
            dialect_name=dialect_name,
            original_standard_text=sample['original'],
            ai_generated_dialect_text=sample['generated']
        )
    print(f"Loaded {len(samples)} samples for {dialect_name}")

# Sample Plausibility Data
# Replace with your actual data

plausibility_samples = [
    {
        'question': 'বাংলাদেশের রাজধানী কোথায়?',
        'correct': 'ঢাকা',
        'wrong_1': 'চট্টগ্রাম',
        'wrong_2': 'সিলেট',
        'wrong_3': 'রাজশাহী'
    },
    {
        'question': 'পদ্মা সেতুর দৈর্ঘ্য কত কিলোমিটার?',
        'correct': '৬.১৫ কিলোমিটার',
        'wrong_1': '৫.৫ কিলোমিটার',
        'wrong_2': '৭.২ কিলোমিটার',
        'wrong_3': '৮.০ কিলোমিটার'
    },
    {
        'question': 'বাংলা ভাষা আন্দোলন কত সালে হয়েছিল?',
        'correct': '১৯৫২',
        'wrong_1': '১৯৪৮',
        'wrong_2': '১৯৫৬',
        'wrong_3': '১৯৭১'
    },
    # Add more items (you can add up to any number, 10 will be randomly selected)
]

# Load plausibility data
print("\nLoading plausibility data...")
for sample in plausibility_samples:
    PlausibilityData.objects.get_or_create(
        question=sample['question'],
        correct_answer=sample['correct'],
        wrong_option_1=sample['wrong_1'],
        wrong_option_2=sample['wrong_2'],
        wrong_option_3=sample['wrong_3']
    )
print(f"Loaded {len(plausibility_samples)} plausibility questions")

print("\n✅ Data loading complete!")
print(f"Total Dialect Data: {DialectData.objects.count()}")
print(f"Total Plausibility Data: {PlausibilityData.objects.count()}")
