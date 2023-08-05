import mutagen
import os.path
import re
import requests
import shutil
import sys

import musicbrainzngs

from mutagen.id3 import APIC, TIT2, TALB, TPE1, TPE2, TRCK, TDRC, TPOS, TCON
from mutagen.mp4 import MP4Cover

import pylast


class TruMusic:
    supported_file_extensions = ['mp3', 'm4a']

    field_maps = {
        'MP4': {
            "artist": "\xa9ART",
            "album_artist": "aART",
            "album": "\xa9alb",
            "title": "\xa9nam",
            "year": "\xa9day",
            "track": "trkn",
            "disk": "disk",
            "cover": "covr",
        },
        "MP3": {
            "artist": TPE1,
            "album_artist": TPE2,
            "album": TALB,
            "title": TIT2,
            "year": TDRC,
            "track": TRCK,
            "disk": TPOS,
            "cover": APIC,
            # "genre": TCON,
        }
    }

    def __init__(
            self,
            lastfm_api_key: str,
            lastfm_api_secret: str,
            ext: str = '.mp3',
            dry_run: bool = False,
            quiet: bool = False,
            verbose: bool = False,
    ):
        musicbrainzngs.set_useragent("TruMusic", 1.0)
        if lastfm_api_key is None or lastfm_api_secret is None:
            raise Exception("Must provide last.fm api key and secret")
        self.ext = ext
        self.dry_run = dry_run
        self.quiet = quiet
        self.verbose = verbose

        self._log_prefix: str = ""
        self.log_prefix: str = None

        self._image_file: str = None

        self.album_info: dict = {}

    @property
    def log_prefix(self):
        return self._log_prefix if not self.dry_run else f"[ DRY RUN ]{self._log_prefix}"

    @log_prefix.setter
    def log_prefix(self, prefix=None):
        if prefix is not None:
            self._log_prefix = prefix
        else:
            self._log_prefix = ""

    @property
    def image_file(self):
        if self._image_file is None:
            album_art_file = f"{self.album_info['path']}/art.jpg"
            album_art_url = self.album_info['image_url']
            try:
                if album_art_url is not None:
                    r = requests.get(album_art_url, stream=True)
                    if r.status_code == 200:
                        # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
                        r.raw.decode_content = True
                        with open(album_art_file, 'wb') as f:
                            shutil.copyfileobj(r.raw, f)
                            self._image_file = album_art_file
            except pylast.WSError as err:
                print(err)
        return self._image_file

    @staticmethod
    def _clean_string(title):
        return re.sub(' +', ' ', re.sub('[/|⧸]', '', title))

    @staticmethod
    def _clean_search_string(title):
        return title.replace('⧸', '/')

    def log(self, msg):
        """
        Add the given message to the log, with the prefix
        :param msg:
        :return:
        """
        if self.verbose:
            print(f"{self.log_prefix} {msg}")

    def _cleanup(self):
        if self.image_file is not None and os.path.exists(self.image_file):
            os.remove(self.image_file)
            self._image_file = None
            self.album_info = {}

    def _get_album_info(self, album_artist: str, album_title: str):
        network = pylast.LastFMNetwork(
            api_key=os.environ.get('LASTFM_API_KEY', None),
            api_secret=os.environ.get('LASTFM_API_SECRET', None),
        )

        album = network.get_album(
            album_artist,
            self._clean_search_string(album_title),
        )

        release = musicbrainzngs.get_release_by_id(id=album.get_mbid())
        # get tracks and sort them by title length, preserving track number
        album_tracks = {num: track.title for num, track in enumerate(album.get_tracks(), start=1)}
        album_tracks_list = sorted(list(album_tracks.items()), key=lambda key: len(key[1]), reverse=True)
        album_tracks_sorted = {track[0]: {"title": self._clean_string(track[1])} for track in album_tracks_list}

        release_date = release['release']['date']
        if not self.quiet:
            rd_input = input(f"Enter '{album_artist}: {album_title}' release date ({release['release']['date']}): ")
            if rd_input:
                release_date = rd_input

        self.album_info = {
            "artist": album_artist,
            "title": self._clean_string(album_title),
            "release_date": release_date,
            "image_url": album.get_cover_image().replace("300x300", "1000x1000").replace(".png", ".jpg"),
            "tracks": album_tracks_sorted,
            "path": f"{album_artist}/{album_title}",
        }

    def tag_files(self, artist: str, album: str, track_files: list):
        """
        Tag audio files based on directory structure
        :param artist:
        :param album:
        :param track_files:
        :return:
        """
        self._get_album_info(artist, album)

        if len(track_files) == 0:
            self.log("No tracks to tag")
            return False

        album_tags = {
            "artist": artist,
            "album": album,
            "album_artist": artist,
            "year": self.album_info['release_date'],
            "cover": self.image_file
        }

        track_count = len(self.album_info['tracks'])
        for num, track in self.album_info['tracks'].items():
            num = str(num).zfill(2)
            for track_file in track_files:
                if track["title"].lower() in self._clean_string(track_file.lower()):
                    track_file_path = f"{self.album_info['path']}/{track_file}"
                    new_track_file_path = f"{self.album_info['path']}/{num} - {track['title']}{self.ext}"
                    if track_file_path != new_track_file_path:
                        if os.path.exists(new_track_file_path):
                            self.log(f"[ ERROR ] File already exists: {track_file_path}")
                        else:
                            self.log(f"[ RENAMING ] '{track_file_path}' to '{new_track_file_path}'")
                            if self.dry_run:
                                new_track_file_path = track_file_path
                            else:
                                os.rename(track_file_path, new_track_file_path)
                    self.log(f"TAGGING: {new_track_file_path}")
                    track_tags = {
                        "title": track["title"],
                        "track": (int(num), track_count),
                        "disk": (1, 1),
                    }
                    track_tags.update(album_tags)
                    track_files.remove(track_file)

                    audiofile = mutagen.File(new_track_file_path)

                    if hasattr(audiofile, "tags"):
                        del audiofile.tags
                    audiofile.add_tags()

                    file_type = audiofile.__class__.__name__
                    if file_type not in self.field_maps:
                        self.log(f"[ ERROR ] Unsupported file type: {file_type}")
                        return False
                    else:
                        field_map = self.field_maps[file_type]
                        for field in field_map:
                            if field in track_tags:
                                _field = field_map[field]
                                if field == "cover":
                                    if os.path.exists(track_tags[field]):
                                        with open(track_tags[field], "rb") as f:
                                            if file_type == "MP4":
                                                audiofile.tags[_field] = [
                                                    MP4Cover(f.read(), imageformat=MP4Cover.FORMAT_JPEG)
                                                ]
                                            elif file_type == "MP3":
                                                audiofile.tags.add(
                                                    APIC(mime='image/jpeg', type=3, desc=u'Cover', data=f.read()))
                                            else:
                                                self.log(f"[ WARNING ] Unsupported file type (cover art): {file_type}")
                                    else:
                                        self.log(f"[ WARNING ] album art is missing: {track_tags[field]}")
                                else:
                                    if file_type == "MP3":
                                        if field == "track" or field == "disk":
                                            track_tags[field] = f"{track_tags[field][0]}/{track_tags[field][1]}"
                                        audiofile.tags[_field] = field_map[field](encoding=3, text=track_tags[field])
                                    elif file_type == "MP4":
                                        audiofile.tags[_field] = [track_tags[field]]
                            else:
                                self.log(f"[ WARNING ] Field not found in data: {field}")

                        if not self.dry_run:
                            audiofile.save()
        if len(track_files) > 0:
            print(self.album_info['tracks'])
            self.log(f"[ WARNING ] {len(track_files)} files not processed:\n{track_files}")
        self._cleanup()
        return True

    def clean_tags(self, _file_path):
        """
        Tag audio files based on directory structure
        :param _file_path:
        :return:
        """

        self.log(f"CLEANING TAGS: {_file_path}")

        audiofile = mutagen.File(_file_path)

        file_type = audiofile.__class__.__name__
        if file_type not in self.field_maps:
            self.log(f"ERROR: Unsupported file type: {file_type}")
            return False

        field_map = self.field_maps[file_type]
        if hasattr(audiofile, "tags"):
            tags = {}
            for field, _field in field_map.items():
                if _field in audiofile.tags:
                    field_data = audiofile.tags[_field]
                    if field == "cover":
                        if file_type == "MP4":
                            audiofile.tags[_field] = [
                                MP4Cover(field_data, imageformat=MP4Cover.FORMAT_JPEG)
                            ]
                        elif file_type == "MP3":
                            tags[_field] = field_data
                            #audiofile.tags.add(
                            #    APIC(mime='image/jpeg', type=3, desc=u'Cover', data=field_data))
                        else:
                            self.log(f"WARNING: Unsupported file type (cover art): {file_type}")
                    else:
                        if file_type == "MP3":
                            module = getattr(sys.modules[__name__], field_map[field])
                            if field == "track" or field == "disk":
                                if str(field_data).endswith("/0") or str(field_data).startswith("0/"):
                                    field_data = "1/1"
                            tags[_field] = module(encoding=3, text=str(field_data))
                        elif file_type == "MP4":
                            tags[_field] = [field_data]
                else:
                    self.log(f"WARNING: Field not found in data: {field}/{_field}")
                    if field == "disk":
                        self.log(f"INFO: Populating field with default value: {field}/{_field} :: 1/1")
                        if file_type == "MP3":
                            module = getattr(sys.modules[__name__], field_map[field])
                            tags[_field] = module(encoding=3, text="1/1")
                        elif file_type == "MP4":
                            tags[_field] = ["1/1"]
            del audiofile.tags
            audiofile.add_tags()
            for tag in tags.values():
                audiofile.tags.add(tag)
            if not self.dry_run:
                audiofile.save()
        return True
