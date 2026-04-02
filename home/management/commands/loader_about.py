from django.core.management.base import BaseCommand
from home.models import ProfileCategory, ProfileContent


class Command(BaseCommand):
    help = 'Load sample about/profile data to database'

    def handle(self, *args, **options):
        self.stdout.write('Loading profile data...')

        categories_data = [
            {
                'name': 'About Box',
                'description': 'Main about section with introduction',
            },
            {
                'name': 'Education',
                'description': 'Educational background and qualifications',
            },
            {
                'name': 'Experience',
                'description': 'Work experience and professional history',
            },
            {
                'name': 'Skills',
                'description': 'Technical skills and expertise',
            },
        ]

        contents_data = [
            {
                'category': 'About Box',
                'title': 'About Me',
                'content': '<p>Hello! I am a passionate full-stack developer with expertise in building modern web applications. I love creating seamless user experiences and solving complex problems.</p>',
            },
            {
                'category': 'Education',
                'title': 'Academic Background',
                'content': '<p><strong>B.Sc. in Computer Science</strong><br>University of Technology<br>Graduated: 2020</p>',
            },
            {
                'category': 'Experience',
                'title': 'Work Experience',
                'content': '<p><strong>Senior Developer</strong><br>Tech Company<br>2020 - Present</p>',
            },
            {
                'category': 'Skills',
                'title': 'Technical Skills',
                'content': '<ul><li>Python/Django</li><li>JavaScript/React</li><li>PostgreSQL</li><li>AWS</li></ul>',
            },
        ]

        for cat_data in categories_data:
            cat, created = ProfileCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            if created:
                self.stdout.write(f'Created category: {cat.name}')

        for content_data in contents_data:
            category = ProfileCategory.objects.get(name=content_data['category'])
            content, created = ProfileContent.objects.get_or_create(
                category=category,
                title=content_data['title'],
                defaults={
                    'content': content_data['content']
                }
            )
            if created:
                self.stdout.write(f'Created content: {content.title}')

        self.stdout.write(self.style.SUCCESS('Profile data loaded successfully!'))
