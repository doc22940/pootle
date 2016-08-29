# -*- coding: utf-8 -*-
#
# Copyright (C) Pootle contributors.
#
# This file is a part of the Pootle project. It is distributed under the GPL3
# or later license. See the LICENSE file for a copy of the license and the
# AUTHORS file for copyright and authorship information.

from contextlib import contextmanager

from pootle.core.signals import update_data


@contextmanager
def suppress_signal(signal):
    handlers = signal.receivers
    signal.receivers = []
    yield
    signal.receivers = handlers


@contextmanager
def keep_data(keep=True):
    if keep:
        with suppress_signal(update_data):
            yield
    else:
        yield


@contextmanager
def update_data_after(sender, **kwargs):
    with keep_data():
        yield
    if "kwargs" in kwargs:
        kwargs.update(kwargs.pop("kwargs"))
    update_data.send(
        sender.__class__,
        instance=sender,
        **kwargs)
