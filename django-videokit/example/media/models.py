from __future__ import unicode_literals

from django.db import models

import subprocess

from videokit.models import VideoField
from videokit.models import VideoSpecField

def upload_to(instance, filename):
    return 'media_items/%s' % filename

class MediaItem(models.Model):
    video = VideoField( upload_to = upload_to,
                        width_field = 'video_width', height_field = 'video_height',
                        rotation_field = 'video_rotation',
                        mimetype_field = 'video_mimetype',
                        duration_field = 'video_duration',
                        thumbnail_field = 'video_thumbnail')
    video_width = models.IntegerField(null = True, blank = True)
    video_height = models.IntegerField(null = True, blank = True)
    video_rotation = models.FloatField(null = True, blank = True)
    video_mimetype = models.CharField(max_length = 32, null = True, blank = True)
    video_duration = models.IntegerField(null = True, blank = True)
    video_thumbnail = models.ImageField(null = True, blank = True)
    video_mp4 = VideoSpecField(source = 'video', format = 'mp4')
    video_ogg = VideoSpecField(source = 'video', format = 'ogg')

    def __unicode__(self):
        return self.video.name

    def video_specs_generated(self):
        if self.video_mp4.generated() and self.video_ogg.generated():
            return True

        return False


    def converter(self): 	   
        name1 = 'media-uploads/' + self.video.name 
        name2 =  name1[26:]    
        command1 = 'ffmpeg -i ./'+ name1 +' -vf scale=640:480 -strict -2 ./media-uploads/'+ name2 + ' &'
        #command2 = 'pwd &>output1234.txt; pwd &>output1234.txt'
        f = open(name2 +'_input.txt', 'w')
        f1 = open(name2+'_output.txt', 'w')
        print(name1)
        print(name2)
        response = subprocess.Popen(command1, shell = True, stdout = f, stderr = f1)
	
        return False
