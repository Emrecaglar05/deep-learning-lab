"""
Bu kod, bir Python paketini dağıtıma hazır hale getirmek için setuptools ile paket bilgilerini tanımlar. 
Paket adı, sürüm, yazar bilgileri, proje URL’si ve bug tracker gibi bilgiler eklenir, 
src klasörü altındaki modüller otomatik olarak paketlenir ve README.md dosyası uzun açıklama olarak kullanılır. 
Böylece paket, PyPI veya GitHub üzerinden kolayca yüklenip kullanılabilir hale gelir.

"""
import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()


__version__ = "0.0.0"

REPO_NAME = "DataScience-E2E"
AUTHOR_USER_NAME = "entbappy"
SRC_REPO = "cnnClassifier"
AUTHOR_EMAIL = "entbappy73@gmail.com"


setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="A small python package for CNN app",
    long_description=long_description,
    long_description_content="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues",
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src")
)