import logging
import random

import pwnagotchi.plugins as plugins
import pwnagotchi.voice as voice_module


class TrashTalk(plugins.Plugin):
    __author__ = "you"
    __version__ = "1.0.0"
    __license__ = "GPL3"
    __description__ = "Override Pwnagotchi voice lines from config."

    def __init__(self):
        self._original_methods = {}

    def on_loaded(self):
        logging.info("[trashtalk] loaded")

        phrases = self.options.get("phrases", {})

        supported = [
            "on_starting",
            "on_keys_generation",
            "on_normal",
            "on_free_channel",
            "on_reading_logs",
            "on_bored",
            "on_motivated",
            "on_demotivated",
            "on_sad",
            "on_angry",
            "on_excited",
            "on_new_peer",
            "on_lost_peer",
            "on_miss",
            "on_grateful",
            "on_lonely",
            "on_napping",
            "on_shutdown",
            "on_awakening",
            "on_waiting",
            "on_assoc",
            "on_deauth",
            "on_handshakes",
            "on_unread_messages",
            "on_rebooting",
            "on_uploading",
            "on_downloading",
        ]

        for method_name in supported:
            custom_lines = phrases.get(method_name)
            if not custom_lines:
                continue

            if not hasattr(voice_module.Voice, method_name):
                logging.warning(f"[trashtalk] missing method: {method_name}")
                continue

            original = getattr(voice_module.Voice, method_name)
            self._original_methods[method_name] = original
            setattr(
                voice_module.Voice,
                method_name,
                self._make_override(method_name, custom_lines, original),
            )
            logging.info(f"[trashtalk] overriding {method_name}")

    def on_unload(self, ui):
        for method_name, original in self._original_methods.items():
            setattr(voice_module.Voice, method_name, original)
        logging.info("[trashtalk] restored original voice methods")

    def _make_override(self, method_name, custom_lines, original):
        def replacement(instance, *args, **kwargs):
            try:
                line = random.choice(custom_lines)
                context = self._build_context(method_name, *args, **kwargs)
                return line.format(**context)
            except Exception as e:
                logging.exception(f"[trashtalk] error in {method_name}: {e}")
                return original(instance, *args, **kwargs)

        return replacement

    def _build_context(self, method_name, *args, **kwargs):
        ctx = {}

        if method_name == "on_free_channel":
            ctx["channel"] = args[0]

        elif method_name == "on_reading_logs":
            ctx["lines_so_far"] = args[0] if args else 0

        elif method_name in ("on_motivated", "on_demotivated"):
            ctx["reward"] = args[0] if args else ""

        elif method_name == "on_new_peer":
            peer = args[0]
            ctx["name"] = peer.name()

        elif method_name == "on_lost_peer":
            peer = args[0]
            ctx["name"] = peer.name()

        elif method_name == "on_miss":
            ctx["name"] = args[0]

        elif method_name in ("on_napping", "on_waiting"):
            ctx["secs"] = args[0]

        elif method_name == "on_assoc":
            ap = args[0]
            ssid = ap.get("hostname", "")
            bssid = ap.get("mac", "")
            ctx["hostname"] = ssid
            ctx["mac"] = bssid
            ctx["what"] = ssid if ssid and ssid != "<hidden>" else bssid

        elif method_name == "on_deauth":
            sta = args[0]
            ctx["mac"] = sta.get("mac", "")

        elif method_name == "on_handshakes":
            num = args[0]
            ctx["num"] = num
            ctx["plural"] = "s" if num > 1 else ""

        elif method_name == "on_unread_messages":
            count = args[0]
            total = args[1]
            ctx["count"] = count
            ctx["total"] = total
            ctx["plural"] = "s" if count > 1 else ""

        elif method_name == "on_uploading":
            ctx["to"] = args[0]

        elif method_name == "on_downloading":
            ctx["name"] = args[0]

        return ctx
