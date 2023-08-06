#!/usr/bin/env python
""" rss feed
"""
import traceback
from abc import ABC, abstractmethod

from codefast import logger as cf
from codefast.exception import get_exception_str


def get_exception_str(e: Exception) -> str:
    return str(e) + '\n' + traceback.format_exc()


class Component(ABC):
    @abstractmethod
    def process(self, *args, **kwargs):
        pass

    def exec(self, *args, **kwargs):
        class_name = self.__class__.__name__
        file_name = self.__class__.__module__.split('.')[-1]
        cf.info('pipeline starts exec [{}], args {}, kwargs {}'.format(
            file_name + "." + class_name, args, kwargs))
        results = self.process(*args, **kwargs)
        cf.info('pipeline finish exec [{}], results: {}'.format(
            class_name, results))
        return results


class Pipeline(object):
    def add(self, component: Component):
        self.components.append(component)
        return self

    def __init__(self) -> None:
        self.components = []
        self.source_input = None

    def set_source_input(self, source_input):
        self.source_input = source_input
        return self

    def process(self):
        results = self.source_input
        try:
            for c in self.components:
                if results is not None:
                    results = c.exec(results)
                else:
                    results = c.exec()
        except Exception as e:
            cf.error(get_exception_str(e))
        return results
