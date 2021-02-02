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
        self.type = ""
        self.season_number = 0

    def _check(self):
        """ Check if attributes are OK """

        self.checked = True

        # Check the path
        if not os.path.exists(self.full_path):
            print(f"Add a valid path (full_path), '{self.full_path}' does not exist")
            self.checked = False

        # Check the title
        if not self.title or len(self.title) > 100:
            print("Add a valid title (title)")
            self.checked = False
        
        # Check the language
        if not self.lang or len(self.lang) > 10:
            print("Add a valid language (lang)")
            self.checked = False

        # Check the type 
        if self.type not in ["movie", "serie"]:
            print("Add a valid video type serie/movie (type)")
            self.checked = False

        # Check the season number
        if self.type == "serie" and self.season_number < 1:
            print("Add a valid season number (season_number)")
            self.checked = False 

    def _get_files_infos(self):
        """ Get infos about the video file """

        self._check()

        if self.checked:
            cv2video = cv2.VideoCapture(self.full_path)
            self.height = str(int(cv2video.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            self.width = str(int(cv2video.get(cv2.CAP_PROP_FRAME_WIDTH)))
            self.size_mb = str(int(os.path.getsize(self.full_path) / 10**6))
            self.video_format = self.full_path.split(".")[-1]

            self.old_file_name = os.path.basename(self.full_path)
            self.new_title = "-".join(self.title.split(" ")).lower()
            self.lang = self.lang.upper()
            self.season_number = int(self.season_number)

    def _rename(self):
        """ Rename the file """
        
        if self.checked:
            self.new_file_name = self.new_title + "_" + self.width + "x" + self.height + "_" + self.lang + "_" + self.size_mb + "MB" + "." + self.video_format
            print(self.old_file_name)
            print(self.new_file_name)

    def rename(self):
        """ Rename method which can be call """

        self._get_files_infos()
        self._rename()


if __name__ == "__main__":
    f = RenameVideoFiles()
    f.full_path = "/home/mathias/Documents/videos/Kimi no na wa (2016)/Kimi no Na wa. (Your Name) [BDRip 1920x1080 x264 AAC] VOSTFR V2.mkv"
    f.title = "Kimi no Na wa"
    f.lang = "VOSTFR"
    f.type = "movie"
    f.rename()
