''' Utilities for AWS Panorama application development. '''

import functools

def lazy_property(func):
    ''' Caches the return value of a function, and turns it into a property.

    Intended to be used as a function decorator::

        >>> class Foo:
        >>>     @lazy_property
        >>>     def bar(self):
        >>>         print('expensive calculation')
        >>>         return 'bar'
        >>> foo = Foo()
        >>> foo.bar()
        expensive calculation
        'bar'
        >>> foo.bar()
        'bar'
    '''
    attrib_name = '_' + func.__name__
    @property
    @functools.wraps(func)
    def lazy_wrapper(instance, *args, **kwargs):
        if hasattr(instance, attrib_name):
            return getattr(instance, attrib_name)
        value = func(instance, *args, **kwargs)
        object.__setattr__(instance, attrib_name, value)
        return value
    return lazy_wrapper
''' Backpack is a toolset that makes development for AWS Panorama hopefully more enjoyable.
AWS Panorama is a machine learning appliance and software development kit that can be used to
develop intelligent video analytics and computer vision applications deployed on an edge device.'''

__version__ = '0.1.6'
