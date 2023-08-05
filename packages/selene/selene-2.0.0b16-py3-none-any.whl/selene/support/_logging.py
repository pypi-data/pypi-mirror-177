from functools import reduce
from typing import Tuple, ContextManager, Dict, Any, Iterable
from typing_extensions import Protocol

from selenium.webdriver import Keys


class _ContextManagerFactory(Protocol):
    def __call__(
        self, *, title: str, params: Dict[str, Any], **kwargs
    ) -> ContextManager:
        ...


class _default_translations:
    remove_verbosity = (
        ('browser.element', 'element'),
        ('browser.all', 'all'),
        ("'css selector', ", ""),
        ('((', '('),
        ('))', ')'),
    )
    identify_assertions = (
        (': has ', ': have '),
        (': have ', ': should have '),
        (': is ', ': should be '),
        (' and is ', ' and be '),
        (' and has ', ' and have '),
    )
    key_codes_to_names = [
        (f"({repr(value)},)", key)
        for key, value in Keys.__dict__.items()
        if not key.startswith('__')
    ]


def wait_with(
    *,
    context: _ContextManagerFactory,
    translations: Iterable[Tuple[str, str]] = (
        *_default_translations.remove_verbosity,
        *_default_translations.identify_assertions,
        *_default_translations.key_codes_to_names,
    ),
):
    """
    :return:
        Decorator factory to pass to Selene's config._wait_decorator
        for logging commands with waiting built in
    :param context:
        Allure-like ContextManager factory
        (i.e. a type/class or function to return python context manager),
        that builds a context manager based on title string and params dict
    :param translations:
        Iterable of translations as (from, to) substitution pairs
        to apply to final title string to log
    """

    def decorator_factory(wait):
        def decorator(for_):
            def decorated(fn):

                title = f'{wait.entity}: {fn}'

                def translate(initial: str, item: Tuple[str, str]):
                    old, new = item
                    return initial.replace(old, new)

                translated_title = reduce(
                    translate,
                    translations,
                    title,
                )

                with context(title=translated_title, params={}):
                    return for_(fn)

            return decorated

        return decorator

    return decorator_factory
