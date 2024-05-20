from setuptools import setup, find_packages

setup(
    name='MusicDataAI',
    version='0.1.0',
    author='Mike Petersen',
    author_email='petersenm375@gmail.com',
    description='A music data AI application to demonstrate generative AI and microservices.',
    package_dir={"": "flask-backend"},
    packages=find_packages(where="flask-backend"),
    include_package_data=True,
    install_requires=[
        'Flask',
        'requests',
        'python-dotenv',
        'Werkzeug',
        'tensorflow',
        'magenta',
        'pyfluidsynth',
        'pretty_midi',
        # Add any other library dependencies you might need for your Flask services
        # Example:
        # 'flask-cors==3.0.10',  # If you need CORS for your services
        # 'pandas==1.3.3',       # If you process data within the services
        # 'sqlalchemy==1.4.23',  # If using SQL databases
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'run-ai-service=musicdata.ai_service.api:main',
            'run-data-service=musicdata.data_service.api:main',
            'run-auth-service=musicdata.auth_service.api:main',
        ],
    },
)
