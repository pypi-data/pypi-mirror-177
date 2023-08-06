"""
Zenodo deposit record, as described by the DataCite Metadata Schema 4.0.

https://schema.datacite.org/meta/kernel-4.0/
"""
import io
import re
import html
import pathlib
import shutil
import zipfile
import tempfile
import xml.etree
import urllib.parse
import urllib.request

import attr
import html5lib
import nameparser
from clldutils import licenses
from pycldf import iter_datasets, Source, Dataset
from pycldf.ext.discovery import DatasetResolver

__all__ = ['Record', 'GithubRepos']

ZENODO_DOI_PATTERN = re.compile(r"10\.5281/zenodo\.[0-9]+")
ZENODO_DOI_FORMAT = '10.5281/zenodo.{}'
NS = dict(
    rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    adms="http://www.w3.org/ns/adms#",
    dc="http://purl.org/dc/elements/1.1/",
    dct="http://purl.org/dc/terms/",
    dctype="http://purl.org/dc/dcmitype/",
    dcat="http://www.w3.org/ns/dcat#",
    duv="http://www.w3.org/ns/duv#",
    foaf="http://xmlns.com/foaf/0.1/",
    frapo="http://purl.org/cerif/frapo/",
    geo="http://www.w3.org/2003/01/geo/wgs84_pos#",
    gsp="http://www.opengis.net/ont/geosparql#",
    locn="http://www.w3.org/ns/locn#",
    org="http://www.w3.org/ns/org#",
    owl="http://www.w3.org/2002/07/owl#",
    prov="http://www.w3.org/ns/prov#",
    rdfs="http://www.w3.org/2000/01/rdf-schema#",
    schema="http://schema.org/",
    skos="http://www.w3.org/2004/02/skos/core#",
    vcard="http://www.w3.org/2006/vcard/ns#",
    wdrs="http://www.w3.org/2007/05/powder-s#",
)


@attr.s
class GithubRepos:
    org = attr.ib()
    name = attr.ib()
    tag = attr.ib(default=None)

    @classmethod
    def from_url(cls, url):
        url = urllib.parse.urlparse(url)
        if url.netloc == 'github.com':
            path = url.path.split('/')
            return cls(
                org=path[1],
                name=path[2],
                tag=path[4] if len(path) > 4 and path[3] == 'tree' else None)

    @property
    def clone_url(self):
        return 'https://github.com/{0.org}/{0.name}.git'.format(self)

    @property
    def release_url(self):
        if self.tag:
            return 'https://github.com/{0.org}/{0.name}/archive/refs/tags/{0.tag}.zip'.format(self)


def get_doi(doi_or_url):
    url = urllib.parse.urlparse(doi_or_url)
    if not url.netloc:
        return url.path
    assert url.netloc == 'doi.org'
    return url.path[1:]


def get_creators(names):
    res = []
    for name in names:
        name = nameparser.HumanName(name)
        first = name.first
        if name.middle:
            first += ' ' + name.middle
        res.append('{}, {}'.format(name.last, first))
    return res


@attr.s
class Record:
    doi = attr.ib(
        converter=get_doi,
        validator=attr.validators.matches_re(r'10\.5281/zenodo\.[0-9]+'))
    title = attr.ib()
    creators = attr.ib(converter=get_creators, default=attr.Factory(list))
    year = attr.ib(default=None)
    license = attr.ib(default=None)
    download_urls = attr.ib(default=attr.Factory(list))
    keywords = attr.ib(default=attr.Factory(list))
    communities = attr.ib(default=attr.Factory(list), converter=lambda l: [i for i in l if i])
    github_repos = attr.ib(default=None)
    closed_access = attr.ib(default=False, validator=attr.validators.instance_of(bool))

    def __attrs_post_init__(self):
        if not self.download_url:
            assert self.closed_access, self.doi

    @property
    def download_url(self):
        return self.download_urls[0] if self.download_urls else None

    @property
    def id(self):
        return self.doi.replace('10.5281/zenodo.', '')

    @classmethod
    def from_dcat_element(cls, e):
        def qn(name):
            pref, _, lname = name.partition(':')
            return "{%s}%s" % (NS[pref], lname)

        def get(qname, attribute=None, parent=None):
            return [
                ee.attrib[qn(attribute)] if attribute else ee
                for ee in (parent or e).findall('.//{}'.format(qn(qname)))
                if not attribute or (ee.attrib.get(qn(attribute)))]

        def id_from_zenodo_url(url, type_='record'):
            url = urllib.parse.urlparse(url)
            path_comps = url.path.split('/')
            if url.netloc == 'zenodo.org' and path_comps[1] == type_:
                return path_comps[2]

        kw = dict(
            doi=get('rdf:Description', 'rdf:about')[0],
            title=get('dct:title')[0].text,
            year=get('dct:issued')[0].text.split('-')[0],
            keywords=[ee.text for ee in get('dcat:keyword')],
            # Note: We could store media-type info, but that's not always available and can
            # typically be derived from the file suffix.
            download_urls=get('dcat:downloadURL', 'rdf:resource'),
            communities=[
                id_from_zenodo_url(t, 'communities') for t in get('dct:isPartOf', 'rdf:resource')],
        )
        license = get('dct:license', 'rdf:resource')
        if license:
            kw['license'] = license[0]
        creators = []
        for c in get('dct:creator'):
            family = get('foaf:familyName', parent=c)
            if family:
                creators.append(
                    '{}, {}'.format(family[0].text, get('foaf:givenName', parent=c)[0].text))
            else:
                name = get('foaf:name', parent=c)
                assert name
                creators.append(name[0].text)
        kw['creators'] = creators
        for rs in get('dct:RightsStatement', 'rdf:about'):
            if rs == "info:eu-repo/semantics/closedAccess":
                kw['closed_access'] = True
                break
        for ri in get('dct:relation', 'rdf:resource'):
            gh = GithubRepos.from_url(ri)
            if gh:
                kw['github_repos'] = gh
                break
        return cls(**kw)

    @classmethod
    def from_doi(cls, doi):
        res = urllib.request.urlopen('https://doi.org/{}'.format(get_doi(doi)))
        url = urllib.parse.urlparse(res.url)
        if url.netloc == 'zenodo.org':
            doc = html5lib.parse(
                urllib.request.urlopen(res.url + '/export/dcat').read().decode('utf8'))
            for e in doc.findall('.//{http://www.w3.org/1999/xhtml}pre'):
                if 'style' in e.attrib:
                    return cls.from_dcat_element(xml.etree.ElementTree.fromstring(e.text))

    @staticmethod
    def _download(url, dest, log=None):
        urlpath = pathlib.Path(urllib.parse.urlparse(url).path)
        with urllib.request.urlopen(url) as res:
            if res.code == 200:
                if log:
                    log.info('Downloading {}'.format(url))
                if urlpath.suffix == '.zip':
                    zipfile.ZipFile(io.BytesIO(res.read())).extractall(path=dest)
                else:
                    dest.joinpath(urlpath.name).write_bytes(res.read())

    def download(self, dest, log=None) -> pathlib.Path:
        """
        Download the zipped file-content of the record to `dest`.

        :param dest:
        :param log:
        :return: The directory containing the unzipped files of the record.
        """
        dest = pathlib.Path(dest)
        is_empty = not dest.exists() or (len(list(dest.iterdir())) == 0)
        if not dest.exists():
            dest.mkdir()
        if not self.download_urls:
            raise ValueError('No downloadable resources')  # pragma: no cover
        # Preferentially download from github to not run into Zenodo's rate limit.
        if self.github_repos and self.github_repos.release_url:
            self._download(self.github_repos.release_url, dest, log=log)
        else:
            for url in self.download_urls:
                self._download(url, dest, log=log)
        inner = list(dest.iterdir())
        if is_empty and len(inner) == 1 and inner[0].is_dir():
            # Move the content of the inner-directory to dest:
            for p in inner[0].iterdir():
                shutil.move(str(p), str(dest))
            inner[0].rmdir()
        return dest

    def download_dataset(self, dest, condition=None, mdname=None, log=None):
        with tempfile.TemporaryDirectory() as tmpdirname:
            for ds in iter_datasets(self.download(tmpdirname, log=log)):
                if (condition is None) or condition(ds):
                    return Dataset.from_metadata(ds.copy(dest, mdname=mdname))

    @property
    def bibtex(self):
        src = Source(
            'misc',
            self.doi.split('/')[-1].replace('.', '-'),
            author=' and '.join(self.creators),
            title=self.title,
            keywords=', '.join(self.keywords),
            publisher='Zenodo',
            year=self.year,
            doi=self.doi,
            url='https://doi.org/{}'.format(self.doi),
        )
        if self.license:
            lic = licenses.find(self.license)
            src['copyright'] = lic.name if lic else self.license
        return src.bibtex()

    @property
    def citation(self):
        for line in urllib.request.urlopen(
                'https://zenodo.org/record/{}'.format(self.id)).read().decode('utf8').split('\n'):
            if 'vm.citationResult' in line:
                line = line.split("'", maxsplit=1)[1]
                line = ''.join(reversed(line)).split("'", maxsplit=1)[1]
                return html.unescape(''.join(reversed(line)))


class ZenodoResolver(DatasetResolver):
    def __call__(self, loc, download_dir):
        doi = None
        m = ZENODO_DOI_PATTERN.search(loc)
        if m:
            doi = loc[m.start():m.end()]
        else:
            m = re.search(r'zenodo\.org/record/(?P<number>[0-9]+)', loc)
            if m:
                doi = ZENODO_DOI_FORMAT.format(m.group('number'))
        if doi:
            return Record.from_doi(doi).download(download_dir)
