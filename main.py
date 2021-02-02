import os
import cv2


class RenameVideoFiles:
    """
    Renomme une video au format : <titre-de-la-video>_<longueur>x<largeur>_<VOSTFR>_<poid du fichier>
    """
    def __init__(self):
        self.full_path = ""
        self.title = ""
        self.lang = ""

    def _check(self):
        """ Check if attributes are OK """

        self.checked = False

        if not self.full_path:
            print("Add path (full_path)")
        if not self.title:
            print("Add title (title)")
        if not self.lang:
            print("Add language (lang)")
        
        if self.full_path and self.title and self.lang:
            self.checked=True

    def _get_file_infos(self):
        """ Get infos about the video file """

        self._check()

        if self.checked:
            cv2video = cv2.VideoCapture(self.full_path)
            self.height = str(int(cv2video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            self.width = str(int(cv2video.get(cv2.CAP_PROP_FRAME_WIDTH)))
            self.size_mb = str(int(os.path.getsize(self.full_path) / 10**6))
            self.video_type = self.full_path.split(".")[-1]

            self.old_file_name = os.path.basename(self.full_path)

    def _rename(self):
        """ Rename the file """
        
        if self.checked:
            self.new_title = "-".join(self.title.split(" ")).lower()
            self.new_file_name = self.new_title + "_" + self.width + "x" + self.height + "_" + self.lang + "_" + self.size_mb + "MB" + "." + self.video_type
            print(self.old_file_name)
            print(self.new_file_name)

    def rename(self):
        """ Rename method which can be call """

        self._get_file_infos()
        self._rename()

if __name__ == "__main__":
    f = RenameVideoFiles()
    f.full_path = "/home/mathias/Documents/videos/Kimi no na wa (2016)/Kimi no Na wa. (Your Name) [BDRip 1920x1080 x264 AAC] VOSTFR V2.mkv"
    f.title = "Kimi no Na wa"
    f.lang = "VOSTFR"
    f.rename()
