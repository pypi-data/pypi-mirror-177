#! /usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from airtest.core.api import *
from airtest.aircv import cv2, np


class TemplateOnline(Template):
    """Online picture for Template Class."""

    def _imread(self):
        """Read Online picture."""

        content = requests.get(self.filename).content
        return cv2.imdecode(np.frombuffer(content, np.uint8), 1)
