import setuptools

description = 'Python module for captcha generation'

setuptools.setup(
    name="CaptchaMS",
    version="0.0.3",
    author="KirillMonster",
    author_email="k1rill_monster@mail.ru",
    packages=["CaptchaMS"],
    description=description,
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/KirillMonster/CaptchaMS",
    license='MIT',
    python_requires='>=3.8',
    install_requires=['pillow']
)
