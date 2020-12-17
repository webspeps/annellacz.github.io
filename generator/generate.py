import datetime
import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

from dataclasses import dataclass

PATH_TO_TEMPLATES = Path('TEMPLATES/')
PATH_TO_RESOURCES = Path('../generator/RESOURCES/')
PATH_TO_OUTPUT = Path('../docs/')
URL_ROOT = "https://annella.cz/"

link_to_homepage = "/"  # TODO: always / in production
html_file_suffix = ".html"


@dataclass()
class Page(object):
    title: str
    keywords: str
    description: str
    content_file: str
    url: str
    language: str
    last_mod: datetime.datetime
    phone: str = '<i class="d-plus"></i><i class="d-four"></i><i class="d-two"></i><i class="d-zero"></i> <i class="d-seven"></i><i class="d-seven"></i><i class="d-seven"></i> <i class="d-two"></i><i class="d-five"></i><i class="d-six"></i> <i class="d-zero"></i><i class="d-six"></i><i class="d-eight"></i>'
    email: str = 'info<i class="ch-at"></i>annella<i class="ch-dot"></i>cz'

    def keys(self):
        """Get keys that allows conversion of this class to dictionary.

        Returns:
            List[str]: List of the keys to be passed to template.
        """
        return ['title', 'keywords', 'description', 'url', 'content_file',
                'language', 'phone', 'email']

    def __getitem__(self, key):
        """Allows conversion of this class to dictionary.
        """
        return getattr(self, key)

    def generate_site(self):
        with open(PATH_TO_TEMPLATES.joinpath('page.html')) as tem_han:
            template = Environment(
                loader=FileSystemLoader(PATH_TO_TEMPLATES)
            ).from_string(tem_han.read())
            html_str = template.render(
                **dict(self),
                link_to_homepage=link_to_homepage
            )
            return html_str

    @property
    def absolute_url(self):
        if self.url != 'index':
            return URL_ROOT + self.url + html_file_suffix
        return URL_ROOT

    @property
    def last_modified(self):
        if self.last_mod is None:
            return None
        return self.last_mod.strftime('%Y-%m-%d')


unified_description = "Kvalitní skupinová i individuální školení pro všechny typy zákazníků. Pomáháme vám najít cestu k úspěchu již 10 let. Poznejte s námi své silné stránky."
unified_keywords = "školení, kurzy, poradenství, průzkumy, řízení, komunikace"

pages = [
    Page(title="školení a kurzy",
         keywords=unified_keywords,
         description=unified_description,
         url="index",
         content_file='page_home.html',
         language="cs",
         last_mod=datetime.datetime(2020, 12, 10)
         ),
    Page(title="o nás",
         keywords=unified_keywords,
         description=unified_description,
         url="o-nas",
         content_file='page_o_nas.html',
         language="cs",
         last_mod=datetime.datetime(2020, 12, 10)
         ),
    Page(title="školení a kurzy",
         keywords=unified_keywords,
         description=unified_description,
         url="skoleni-a-kurzy",
         content_file='page_skoleni_kurzy.html',
         language="cs",
         last_mod=datetime.datetime(2020, 12, 10)
         ),
    Page(title="certifikáty",
         keywords=unified_keywords,
         description=unified_description,
         url="certifikaty",
         content_file='page_certifikaty.html',
         language="cs",
         last_mod=datetime.datetime(2020, 12, 10)
         ),
    Page(title="kontakt",
         keywords=unified_keywords,
         description=unified_description,
         url="kontakt",
         content_file='page_kontakt.html',
         language="cs",
         last_mod=datetime.datetime(2020, 12, 10)
         )
]

# Remove all existing resources
if PATH_TO_OUTPUT.exists():
    shutil.rmtree(PATH_TO_OUTPUT)

# Create new dir
PATH_TO_OUTPUT.mkdir()

for page in pages:
    content = page.generate_site()
    with PATH_TO_OUTPUT.joinpath(page.url + html_file_suffix).open('w') as fp:
        fp.write(content)

# Copy resources
shutil.copytree(PATH_TO_RESOURCES, PATH_TO_OUTPUT, dirs_exist_ok=True)

# Generate resource map:
with open(PATH_TO_TEMPLATES.joinpath('site_map.xml')) as tem_han:
    template = Environment(
        loader=FileSystemLoader(PATH_TO_TEMPLATES)
    ).from_string(tem_han.read())
    html_str = template.render(
        sites=pages
    )
    with PATH_TO_OUTPUT.joinpath('sitemap.xml').open('w') as f_xml:
        f_xml.write(html_str)

robots_txt_content = f"""User-agent: *
Allow: /
Sitemap: {URL_ROOT}sitemap.xml"""
with PATH_TO_OUTPUT.joinpath('robots.txt').open('w') as robots_txt_h:
    robots_txt_h.write(robots_txt_content)
