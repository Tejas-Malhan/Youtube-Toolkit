# utils/config.py

import os
import json

def get_appdata_folder():
    return os.path.join(os.getenv("APPDATA"), "YouTubeToolkit")

def get_settings_path():
    return os.path.join(get_appdata_folder(), "settings.json")

def get_cookie_path():
    return os.path.join(get_appdata_folder(), "youtube_cookies.txt")

def get_settings():
    settings_path = get_settings_path()
    app_dir = get_appdata_folder()
    os.makedirs(app_dir, exist_ok=True)

    if not os.path.exists(settings_path):
        default_config = {
            "download_path": "",
            "theme": "System",
            "use_cookies": False
        }
        with open(settings_path, "w") as f:
            json.dump(default_config, f, indent=4)

    with open(settings_path, "r") as f:
        return json.load(f)
