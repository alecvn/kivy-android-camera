# Kivy example for Android camera

I struggled quite a bit to get the Android camera to work with Kivy, so here is a repo that can be used as a starting point for that.

## Setup

	virtualenv -p python3 --no-site-packages venv
	. venv/bin/activate
	pip install -r requirements.txt
	
You will need to clone [`python-for-android`](https://github.com/kivy/python-for-android) in order to add `FileProvider` declarations to the manifest.  The version of `python-for-android` I cloned according to `pythonforandroid/__init__.py` was:
	
    __version__ = '2019.08.09.1.dev0'

Then add the following to `pythonforandroid/bootstraps/sdl2/build/templates/AndroidManifest.tmpl.xml`:

	<provider
		android:name="android.support.v4.content.FileProvider"
		android:authorities="org.test.takepicture.fileprovider"
		android:exported="false"
		android:grantUriPermissions="true">
	  <meta-data
        android:name="android.support.FILE_PROVIDER_PATHS"
        android:resource="@xml/file_paths" />
	</provider>
	
Note:
In Android 10 the `FileProvider` library now sits at `androidx.core.content.FileProvider`.

Also, create the directory and file at `pythonforandroid/bootstraps/sdl2/build/src/main/res/xml/file_paths.xml` with the following contents:

    <?xml version="1.0" encoding="utf-8"?>
	<paths xmlns:android="http://schemas.android.com/apk/res/android">
        <external-path name="external_files" path="." />
	</paths>

## Implementation details

`support-compat-28.0.0.aar` is required to provide `FileProvider`, this is also why we have to target API version 28.

You will also need to specify where you cloned `python-for-android` in your `buildozer.spec` file, which, in this repo, is set to:

	p4a.source_dir = ../python-for-android

Depending on - I believe - your version of `buildozer`, you might need to target Android NDK version 19b.

## Deploy to device
	
	buildozer android debug deploy run logcat
