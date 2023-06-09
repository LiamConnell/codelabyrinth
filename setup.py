from setuptools import setup, find_packages

REQUIREMENTS = [
    'langchain~=0.0.161',
    'python-dotenv~=1.0.0',
    'openai[embeddings]~=0.27.6',
    'psycopg2-binary',
    'pytest~=7.3.1',
    'beautifulsoup4~=4.12.2',
    'requests~=2.30.0',
    'numpy~=1.24.3',
    'tiktoken',
    'faiss-cpu',
    'click',
    'pgvector',
    'fastapi',
    'uvicorn'
]

setup(
    name='coder',
    version='0.1',
    include_package_data=True,
    packages=find_packages(include="coder.*"),
    entry_points={
        'console_scripts': [
            'code = coder.__main__:code',
            'ingest = coder.__main__:ingest',
            'borges = coder.__main__:cli'
        ]
    },
    description="GPT based code assistant",
    install_requires=REQUIREMENTS
)
