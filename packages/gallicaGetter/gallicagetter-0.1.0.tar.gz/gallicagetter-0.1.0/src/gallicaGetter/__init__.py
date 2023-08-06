from gallicaGetter.gallicaWrapper import SRUWrapper
from gallicaGetter.gallicaWrapper import IssuesWrapper
from gallicaGetter.gallicaWrapper import ContentWrapper
from gallicaGetter.gallicaWrapper import PapersWrapper
from gallicaGetter.gallicaWrapper import FullTextWrapper


def connect(gallicaAPIselect, **kwargs):
    apiWrappers = {
        'sru': SRUWrapper,
        'issues': IssuesWrapper,
        'content': ContentWrapper,
        'papers': PapersWrapper,
        'text': FullTextWrapper
    }
    api = gallicaAPIselect.lower()
    if api not in apiWrappers:
        raise ValueError(f'API "{api}" not supported. Options are {apiWrappers.keys()}')
    return apiWrappers[api](**kwargs)
