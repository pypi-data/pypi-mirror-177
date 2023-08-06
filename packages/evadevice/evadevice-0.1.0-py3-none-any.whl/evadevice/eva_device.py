#! /usr/bin/env python
# -*- coding: utf-8 -*-
import re
import tidevice
import adbutils
import platform
import threading
import uiautomator2 as ui2
from airtest.core import api
from airtest.core.api import *
from evatidevice import EvaTidevice
from inspect import getmembers, isfunction
from .utils.logger import get_logger
from .utils.wrapper import retry_wrapper
from .airtest_plus.template_online import TemplateOnline
from .airtest_plus.android import init_device as _init_device


logger = get_logger("evadevice")
# iOS device test automation powered by usbmuxd.
usbmux = tidevice.Usbmux()
# Android device test automation powered by adb.
adb = adbutils.AdbClient()
adb_path = adbutils.adb_path()
device_list = {"android": [], "ios": []}


def udid(_udid: str, direct: bool):
    """Compatible udid in Linux.

    :param _udid: udid for iOS.
    :param direct: udid conversion direction.
    """

    if platform.system() == "Linux":
        if direct:
            return _udid.replace('-', '')
        else:
            return tidevice.Device(_udid).device_info()["UniqueDeviceID"]
    else:
        return _udid


class EvaDevice:
    """Automated Testing Tools for Android and iOS."""

    @retry_wrapper()
    def __init__(self, serial: str = None, airtest: bool = False):
        """Initializes a New Device Client.

        :param serial: serial for target device, e.g. serialno for Android, udid for iOS.
        :param airtest:  Enable of Disable Airtest.
        """

        global device_list
        self.device_id_map = {}
        self._auto_confirm_flag = None

        if serial is None:
            self.device_list(refresh=True)
        elif serial in device_list["ios"]:
            self.type = "ios"
            self.serial = udid(serial, True)
            self.d = tidevice.Device(udid=self.serial)
            self.d.push = self._push_ios
            self.d.pull = self._pull_ios
            self.d.app_current = None
            self.d.start_recording = None
            self.d.stop_recording = None
            self.d.app_list = self._app_list_ios
            if airtest:
                self.airtest = connect_device(f"iOS:///http+usbmux://{serial}")
        elif serial in device_list["android"]:
            self.type = "android"
            self.serial = serial
            self.d = adb.device(serial=self.serial)
            self.d.app_install = self.d.install
            self.d.app_uninstall = self.d.uninstall
            self.d.app_list = self.d.list_packages
            self.d.device_info = self._device_info_android
            if airtest:
                self.airtest = _init_device(serial, adb_path=adb_path)
        else:
            self.device_list(refresh=True)
            raise Exception(f"{serial} maybe offline")

    @staticmethod
    def device_list(refresh: bool = False):
        """Return device list.

        :param refresh: refresh global device list.
        """

        if refresh:
            try:
                ios_list = usbmux.device_udid_list()
                device_list["ios"] = [udid(i, False) for i in ios_list]
            except Exception as e:
                logger.warn(f"iOS Environment Config Error: {e.args}")
            device_list["android"] = [i.serial for i in adb.device_list()]
        return device_list

    @retry_wrapper()
    def _watch_device_ios(self, callback):
        """Report iOS device state when changes.

        :param callback: Attaches a callable that will be called when the device state changes.
        """

        for info in usbmux.watch_device():
            if info["MessageType"] == "Attached":
                _udid = udid(info["Properties"]["SerialNumber"], False)
                self.device_id_map[info["DeviceID"]] = _udid
                callback({"serial": _udid, "status": 1})
            elif info["MessageType"] == "Detached":
                _udid = self.device_id_map[info["DeviceID"]]
                callback({"serial": _udid, "status": 0})

    @retry_wrapper()
    def _watch_device_android(self, callback):
        """Report Android device state when changes.

        :param callback: Attaches a callable that will be called when the device state changes.
        """

        for event in adb.track_devices():
            if event.status == "device":
                self.device_id_map[event.serial] = 1
                callback({"serial": event.serial, "status": 1})
            elif event.status == "absent" and self.device_id_map[event.serial] == 1:
                self.device_id_map[event.serial] = 0
                callback({"serial": event.serial, "status": 0})

    def start_watch_device(self, callback, system: str = "all"):
        """Report device state when changes.

        :param callback: Attaches a callable that will be called when the device state changes.
        :param system: ios or android, default all.
        """

        if system in ["all", "ios"]:
            t1 = threading.Thread(target=self._watch_device_ios,
                                  args=(callback,))
            t1.setDaemon(True)
            t1.start()
        if system in ["all", "android"]:
            t2 = threading.Thread(target=self._watch_device_android,
                                  args=(callback,))
            t2.setDaemon(True)
            t2.start()

    def _device_info_android(self):
        """Return device info for Android."""

        getprop = self.d.prop.get
        device_info = {
            "UniqueDeviceID": self.serial,
            "DeviceName": getprop("ro.product.manufacturer") + " " + getprop("ro.product.model"),
            "ProductName": getprop("ro.product.name"),
            "ProductType": getprop("ro.product.model"),
            "DeviceClass": getprop("ro.product.brand"),
            "CPUArchitecture": getprop("ro.product.cpu.abi"),
            "BuildVersion": getprop("ro.build.version.release"),
        }
        return device_info

    def _auto_confirm_android(self, _d, text_pattern: str):
        """Auto confirm powered by ui2 for Android.

        :param text_pattern: pattern to search for.
        """

        if text_pattern is None:
            text_pattern = "完成|关闭|好|好的|确定|确认|安装|继续安装|下次再说|暂不删除|允许|以后都允许|知道了"
        while not self._auto_confirm_flag.is_set():
            try:
                if not _d.uiautomator.running():
                    _d.uiautomator.start()
                if _d(text="安装").count < 3:   # 防止应用市场推荐
                    _d(textMatches=text_pattern).click_exists()
            except Exception as e:
                logger.error(e.args)
            time.sleep(0.5)

    def _auto_confirm_ios(self, text_pattern: str):
        """Auto confirm powered by airtest for iOS.

        :param text_pattern: pattern to search for.
        """

        if text_pattern is None:
            text_pattern = "信任|安装|确定|允许|以后|以后都允许|稍后|稍后提醒我|不再提醒|取消|否"
        while not self._auto_confirm_flag.is_set():
            try:
                if self.airtest.alert_exists():
                    self.airtest.alert_click(text_pattern.split('|'))
            except Exception as e:
                logger.error(e.args)
            time.sleep(0.5)

    def start_auto_confirm(self, text_pattern: str = None):
        """Start auto confirm for iOS/Android.

        :param text_pattern: pattern to search for.
        """

        self._auto_confirm_flag = threading.Event()
        t = None
        if self.type == "android":
            _d = ui2.connect(self.serial)
            t = threading.Thread(target=self._auto_confirm_android,
                                 args=(_d, text_pattern,))
        elif self.type == "ios":
            t = threading.Thread(target=self._auto_confirm_ios,
                                 args=(text_pattern,))
        t.setDaemon(True)
        t.start()

    def stop_auto_confirm(self):
        """Stop auto confirm."""

        self._auto_confirm_flag.set()

    def _app_list_ios(self):
        """Return app list for iOS."""

        session = self.d.connect_instruments()
        return [i for i in session.app_list() if i["Type"] == "User"]

    def _push_ios(self, src: str, dst: str, bundle_id: str):
        """Push recursive dir and files for iOS.

        :param src: source path.
        :param dst: destination path.
        :param bundle_id: bundle_id for iOS.
        """

        eva_tidevice = EvaTidevice(self.serial, bundle_id=bundle_id)
        eva_tidevice.pushtree(src, dst)

    def _pull_ios(self, src: str, dst: str, bundle_id: str):
        """Pull recursive dir and files for iOS.

        :param src: source path.
        :param dst: destination path.
        :param bundle_id: bundle_id for iOS.
        """

        eva_tidevice = EvaTidevice(self.serial, bundle_id=bundle_id)
        eva_tidevice.pulltree(src, dst)

    def device_info(self):
        """Return device info."""

        keys = "UniqueDeviceID|DeviceName|ProductName|ProductType|DeviceClass|CPUArchitecture|BuildVersion"
        return {key: val for key, val in self.d.device_info().items() if key in keys.split('|')}

    def app_list(self):
        """Return application list."""

        return self.d.app_list()

    def app_install(self, path_or_url: str, *args, **kwargs):
        """Install application.

        :param path_or_url: local path or url.
        :param nolaunch: do not launch app after install.
        """

        self.d.app_install(path_or_url, *args, **kwargs)

    def app_uninstall(self, pkg_name: str):
        """Uninstall application.

        :param pkg_name: package name for Android, bundle_id for iOS.
        """

        self.d.app_uninstall(pkg_name)

    def app_start(self, pkg_name: str):
        """Launch application.

        :param pkg_name: package name for Android, bundle_id for iOS.
        """

        self.d.app_start(pkg_name)

    def app_stop(self, pkg_name: str):
        """Stop application.

        :param pkg_name: package name for Android, bundle_id for iOS.
        """

        self.d.app_stop(pkg_name)

    def app_current(self):
        """Return the currently active application."""

        return self.d.app_current()

    def push(self, src: str, dst: str, *args, **kwargs):
        """Push dir and files for iOS/Android.

        :param src: source path.
        :param dst: destination path.
        :param bundle_id: bundle_id for iOS, None for Android.
        """

        self.d.push(src, dst, *args, **kwargs)

    def pull(self, src: str, dst: str, *args, **kwargs):
        """Pull dir and files for iOS/Android.

        :param src: source path.
        :param dst: destination path.
        :param bundle_id: bundle_id for iOS, None for Android.
        """

        self.d.pull(src, dst, *args, **kwargs)

    def start_recording(self, filename: str):
        """Start video recording.

        :param filename: local filname path.
        """

        self.d.start_recording(filename)

    def stop_recording(self):
        """Stop video recording."""

        self.d.stop_recording()

    def unlock_screen(self, password: str):
        """Unlock Screen for Android.

        :param password: unlock screen password.
        """

        if not self.d.is_screen_on():
            self.d.keyevent(26)
        self.d.swipe(550, 1200, 550, 550, 0.5)
        self.d.send_keys(password)

    @staticmethod
    def airtest_template(path_or_url: str, *args, **kwargs):
        """Picture as touch/swipe/wait/exists target and extra info for cv match.

        :param path_or_url: pic path or url.
        :param target_pos: ret which pos in the pic.
        :param record_pos: pos in screen when recording.
        :param resolution: screen resolution when recording.
        :param rgb: 识别结果是否使用rgb三通道进行校验.
        :param scale_max: 多尺度模板匹配最大范围.
        :param scale_step: 多尺度模板匹配搜索步长.
        """

        if re.match(r"^https?://", path_or_url):
            template = TemplateOnline(filename=path_or_url, *args, **kwargs)
        else:
            template = Template(filename=path_or_url, *args, **kwargs)
        return template

    def airtest_fast_wait(self, path_or_url: str, timeout: int = 20):
        """Wait to match the Template on the device screen.

        :param path_or_url: pic path or url.
        :param timeout: time interval to wait for the match, default is 20.
        """

        template = self.airtest_template(path_or_url)
        return wait(template, timeout=timeout)

    def airtest_fast_click(self,  path_or_url: str, timeout: int = 20):
        """Perform the touch action on the device screen.

        :param path_or_url: pic path or url.
        :param timeout: time interval to wait for the match, default is 20.
        """

        pos = self.airtest_fast_wait(path_or_url, timeout=timeout)
        touch(pos)


d = EvaDevice()


def define_method(cls, method_name, dst_method):
    def inner_method(self, *args, **kwargs):
        return dst_method(*args, **kwargs)
    setattr(cls, method_name, inner_method)


for (k, v) in [i for i in getmembers(api) if isfunction(i[1])]:
    define_method(EvaDevice, "airtest_" + k, v)
