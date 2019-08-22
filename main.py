__version__ = '0.1'

from kivy.app import App
from os.path import exists
from jnius import autoclass, cast
from android import activity, mActivity
from functools import partial
from kivy.clock import Clock
from kivy.uix.scatter import Scatter
from kivy.properties import StringProperty
from kivy.logger import Logger
from kivy.config import Config
Config.set('kivy', 'log_level', 'debug')
Config.set('kivy', 'log_dir', 'logs')
Config.set('kivy', 'log_name', 'kivy_%y-%m-%d_%_.txt')
Config.set('kivy', 'log_enable', 1)
Config.write()

#import cv2
from PIL import Image

Intent = autoclass('android.content.Intent')
MediaStore = autoclass('android.provider.MediaStore')
Uri = autoclass('android.net.Uri')
Environment = autoclass('android.os.Environment')
Context = autoclass("android.content.Context")
FileProvider = autoclass('android.support.v4.content.FileProvider')
PythonActivity = autoclass("org.kivy.android.PythonActivity").mActivity

class Picture(Scatter):
    source = StringProperty(None)


class TakePictureApp(App):
    def build(self):
        pass
        #self.index = 0
        #activity.bind(on_activity_result=self.on_activity_result)

    def take_picture(self):
        def create_img_file():
            File = autoclass('java.io.File')
            storageDir = Context.getExternalFilesDir(Environment.DIRECTORY_PICTURES)

            imageFile = File(
                storageDir,
                "temp.jpg"
            )
            imageFile.createNewFile()

            return imageFile

        intent = Intent(MediaStore.ACTION_IMAGE_CAPTURE)

        photoFile = create_img_file()
        photoUri = FileProvider.getUriForFile(
            Context.getApplicationContext(),
            "org.test.takepicture.fileprovider",
            photoFile
        )

        parcelable = cast('android.os.Parcelable', photoUri)

        intent.putExtra(MediaStore.EXTRA_OUTPUT, parcelable)
        mActivity.startActivityForResult(intent, 0x123)

    # def on_activity_result(self, requestCode, resultCode, intent):
    #     if requestCode == 0x123:
    #         Clock.schedule_once(partial(self.add_picture, self.last_fn), 0)

    # def add_picture(self, fn, *args):
    #     im = Image.open(fn)
    #     width, height = im.size
    #     im.thumbnail((width / 4, height / 4), Image.ANTIALIAS)
    #     im.save(fn, quality=95)
    #     self.root.add_widget(Picture(source=fn, center=self.root.center))

    def on_pause(self):
        return True


TakePictureApp().run()
PythonActivity.requestPermissions(["android.permission.CAMERA"])
