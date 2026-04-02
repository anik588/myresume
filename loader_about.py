import os
import sys
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myresume.settings")

django.setup()

from home.models import ProfileCategory, ProfileContent


def load_data():
    print('Loading profile data...')

    categories_data = [
        {'name': 'About', 'description': 'Personal introduction'},
        {'name': 'Education', 'description': 'Academic background'},
        {'name': 'Research', 'description': 'Research interests'},
    ]

    contents_data = [
        {
            'category': 'About',
            'title': 'About Me',
            'content': '''<p style="font-size: 16px; line-height: 1.7;" data-aos="fade-up" data-aos-duration="1200">
  Hi, I'm <strong>Sajjad Ahmed Anik</strong> — a passionate full-stack developer with a solid academic background in 
  <strong>Physics</strong> from the <strong>University of Dhaka</strong>. During my studies, I explored <em>Computational Physics</em> 
  and <em>Quantum Mechanics</em>, which helped sharpen my problem-solving and analytical thinking.
</p>

<p style="font-size: 16px; line-height: 1.7;" data-aos="fade-up" data-aos-delay="100">
  I work with modern tools like <strong>React.js</strong>, <strong>Next.js</strong>, and <strong>Django</strong>, and I'm experienced 
  in using platforms such as <strong>GitHub</strong>, <strong>Railway</strong>, <strong>Cloudinary</strong>, and <strong>PostgreSQL</strong> 
  for building and deploying responsive web applications.
</p>

<p style="font-size: 16px; line-height: 1.7;" data-aos="fade-up" data-aos-delay="200">
  I'm currently learning <strong>NumPy</strong> to dive into projects that combine <strong>Physics</strong> and 
  <strong>Machine Learning</strong>. I aim to use scientific computing and ML to create intelligent, data-driven solutions.
</p>

<p style="font-size: 16px; line-height: 1.7;" data-aos="fade-up" data-aos-delay="300">
  Alongside development, I also do <strong>graphic design</strong> — from logos to educational posters — and have worked with 
  global clients through <strong>Fiverr</strong> and <strong>Upwork</strong>. I'm always excited to learn, build, and collaborate 
  on meaningful projects that make an impact.
</p>'''
        },
        {
            'category': 'Education',
            'title': 'Academic Background',
            'content': '''<h3 style="font-size: 18px; margin-bottom: 6px;">BSc in Physics</h3>
<p style="font-size: 14px; margin-bottom: 12px;">University of Dhaka | Dept. of Physics</p>

<div class="row">
  <div class="col-md-6 d-flex flex-column">
    <span style="font-size: 14px; font-weight: 600; line-height: 1;">HSC – GPA 5.00</span>
    <span style="font-size: 13px; line-height: 1.4;">Science, Dhaka Imperial College</span>
  </div>
  <div class="col-md-6 d-flex flex-column">
    <span style="font-size: 14px; font-weight: 600; line-height: 1;">SSC – GPA 5.00</span>
    <span style="font-size: 13px; line-height: 1.4;">Science, Motijheel Model School & College</span>
  </div>
</div>'''
        },
        {
            'category': 'Research',
            'title': 'Research Interests',
            'content': '''🧠 Currently researching in AI, Quantum Computing, and Computational Physics. I am learning how to apply Python libraries like NumPy for data analysis and mathematical modeling. I'm excited about the future of technology and its integration with physics.'''
        },
    ]

    for cat_data in categories_data:
        cat, created = ProfileCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        if created:
            print(f'Created category: {cat.name}')

    for content_data in contents_data:
        category = ProfileCategory.objects.get(name=content_data['category'])
        content, created = ProfileContent.objects.get_or_create(
            category=category,
            title=content_data['title'],
            defaults={'content': content_data['content']}
        )
        if created:
            print(f'Created content: {content.title}')

    print('Profile data loaded successfully!')


if __name__ == '__main__':
    load_data()