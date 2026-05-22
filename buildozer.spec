[app]
title = KarenAI
package.name = karenai
package.domain = org.homemaranha
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy,google-genai

orientation = portrait
fullscreen = 1
android.archs = arm64-v8a

# Deixando o buildozer escolher os links de download corretos automaticamente
# android.api = 33
# android.ndk_path = 

[buildozer]
log_level = 2
warn_on_root = 1
