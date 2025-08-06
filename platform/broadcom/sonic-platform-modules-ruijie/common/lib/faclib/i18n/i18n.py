#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import gettext
import os

appName = 'i18n_demo'
languageDir = os.path.abspath('locale')
filedir = os.path.dirname(os.path.realpath(__file__))
languageDir = os.path.join(filedir, 'locale')
print languageDir
gettext.bindtextdomain(appName, languageDir)
gettext.textdomain(appName)
#_ = gettext.gettext


def tr(s):
    return gettext.gettext(s)
