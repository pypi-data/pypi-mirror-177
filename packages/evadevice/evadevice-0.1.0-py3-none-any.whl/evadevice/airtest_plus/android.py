#! /usr/bin/env python
# -*- coding: utf-8 -*-
from airtest.core.helper import G
from airtest.core.android.adb import ADB
from airtest.core.android.ime import YosemiteIme
from airtest.core.android.android import Android
from airtest.core.android.recorder import Recorder
from airtest.core.android.rotation import RotationWatcher
from airtest.core.android.constant import CAP_METHOD, TOUCH_METHOD, IME_METHOD, ORI_METHOD, \
    SDK_VERISON_ANDROID10


class _Android(Android):
    """Add adb_path for Android Device Class."""

    def __init__(self, serialno=None, host=None,
                 cap_method=CAP_METHOD.MINICAP,
                 touch_method=TOUCH_METHOD.MINITOUCH,
                 ime_method=IME_METHOD.YOSEMITEIME,
                 ori_method=ORI_METHOD.MINICAP,
                 display_id=None,
                 input_event=None,
                 adb_path=None):
        super(Android, self).__init__()
        self.serialno = serialno  # or self.get_default_device()
        self._cap_method = cap_method.upper()
        self._touch_method = touch_method.upper()
        self.ime_method = ime_method.upper()
        self.ori_method = ori_method.upper()
        self.display_id = display_id
        self.input_event = input_event
        # init adb
        self.adb = ADB(self.serialno, adb_path=adb_path, server_addr=host,
                       display_id=self.display_id, input_event=self.input_event)
        self.adb.wait_for_device()
        self.sdk_version = self.adb.sdk_version
        if self.sdk_version >= SDK_VERISON_ANDROID10 and self._touch_method == TOUCH_METHOD.MINITOUCH:
            self._touch_method = TOUCH_METHOD.MAXTOUCH
        self._display_info = {}
        self._current_orientation = None
        # init components
        self.rotation_watcher = RotationWatcher(self.adb, self.ori_method)
        self.yosemite_ime = YosemiteIme(self.adb)
        self.recorder = Recorder(self.adb)
        self._register_rotation_watcher()

        self._touch_proxy = None
        self._screen_proxy = None


def init_device(serial: str, adb_path: str):
    """Initialize android device if not yet, and set as current device.

    :param serial: serialno for Android.
    :param adb_path: adb path.
    :return: device instance.
    """

    dev = _Android(serialno=serial, adb_path=adb_path)
    G.add_device(dev)
    return dev
