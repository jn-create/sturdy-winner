from PIL import Image
import os, math

import sys
#print(sys.executable)

class SpriteSheetFromRenders:
    def __init__(self,PathToImageSequence,max_frames_row = 10.0):
        self.PathToImageSequence = PathToImageSequence
        self.max_frames_row = max_frames_row
        
    def imageSize(self):
        frames = self.fetchImageSequence()
        tile_width = 0
        tile_height = 0
        spritesheet_width = 0
        spritesheet_height = 0
        tile_width = frames[0].size[0]
        tile_height = frames[0].size[1]

        if len(frames) > self.max_frames_row :
            spritesheet_width = tile_width * self.max_frames_row
            required_rows = math.ceil(len(frames)/self.max_frames_row)
            spritesheet_height = tile_height * required_rows
        else:
            spritesheet_width = tile_width*len(frames)
            spritesheet_height = tile_height

        return spritesheet_width,spritesheet_height,tile_width,tile_height 

    def fetchImageSequence(self):
        frames = []
        if os.path.isdir(self.PathToImageSequence):
            try:
                files = os.listdir(self.PathToImageSequence)
                files.sort()
                #print(files)      
            except:
                print("path to image sequence does not contain any images!")
                
            for current_file in files :
                try:
                    with Image.open(self.PathToImageSequence + current_file) as im :
                        frames.append(im.getdata())
                except:
                    print(current_file + " is not a valid image")   

        return frames

    def makeSpriteSheet(self,outPutFileName):
        #print(sys.executable)
        self.outPutSpriteImageName = outPutFileName
        
        spritesheet_width,spritesheet_height,tile_width,tile_height = self.imageSize()
        frames = self.fetchImageSequence()

        spritesheet = Image.new("RGBA",(int(spritesheet_width), int(spritesheet_height)))

        for current_frame in frames :
            top = tile_height * math.floor((frames.index(current_frame))/self.max_frames_row)
            left = tile_width * (frames.index(current_frame) % self.max_frames_row)
            bottom = top + tile_height
            right = left + tile_width

            box = (left,top,right,bottom)
            box = [int(i) for i in box]
            cut_frame = current_frame.crop((0,0,tile_width,tile_height))

            spritesheet.paste(cut_frame, box)

        path_to_output_sprtieImage = self.outPutSpriteImageName
        spritesheet.save(path_to_output_sprtieImage)
        print("created SprtieImage from an image sequence! path to the outPut-> {}".format(path_to_output_sprtieImage)) 


if __name__ == '__main__':
    crt = SpriteSheetFromRenders("\\spTest\\",10).makeSpriteSheet("\\spTest\\Hover.png")       

