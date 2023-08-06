import collections
import difflib
import errno
import functools
import os
import string
import tempfile

import torf

from . import __project_name__, _debug
from ._combinator import Combinator
from ._errors import FindError


class FindDownloadLocation:
    """
    Find download path for a torrent, linking existing files

    :param torrent: Path to torrent file
    :param locations: Sequence of directory paths that are searched for files in
        `torrent`
    :param default: Default download directory if none of the files in `torrent`
        are found

    :raise: :class:`~.FindDownloadLocation` if anything goes wrong
    """

    def __init__(self, *, torrent, locations, default=None):
        self._torrent_filepath = str(torrent)
        self._torrent = None
        # Ugly hack to deduplicate locations while preserving order
        self._locations = tuple(
            dict.fromkeys(str(loc) for loc in locations)
        )
        if len(self._locations) < 1:
            raise RuntimeError('You must provide at least one potential download location')
        self._default_location = str(default) if default else None
        self._torrent_files = ()
        self._found_files = set()
        self._matching_files = {}

    def find(self):
        try:
            self._torrent = torf.Torrent.read(self._torrent_filepath)
        except torf.TorfError as e:
            raise FindError(e)
        else:
            self._torrent_files = tuple(self._torrent.files)

            download_location = self._search_download_location()
            if download_location is not None:
                _debug('Found location: %r', download_location)
                return download_location
            elif self._default_location:
                _debug('Default location: %r', self._default_location)
                return self._default_location
            else:
                _debug('First location: %r', self._locations[0])
                return self._locations[0]

    def _search_download_location(self):
        download_locations = []

        # Fast file discovery that works for unrenamed files
        unrenamed_candidates = self._get_unrenamed_candidates()
        _debug('Unrenamed candidates: %r', unrenamed_candidates)
        download_locations.append(
            self._get_download_location(unrenamed_candidates)
        )
        _debug('Download location from unrenamed candidates: %r', download_locations[-1])

        if self._unfound_files:
            # File discovery based on file size
            size_matching_candidates = self._get_size_matching_candidates()
            _debug('Size-matching candidates: %r', size_matching_candidates)
            download_locations.append(
                self._get_download_location(size_matching_candidates)
            )
            _debug('Download location from size-matching candidates: %r', download_locations[-1])

        # Use the first download_location where any file was found
        _debug('Possible download locations: %r', download_locations)
        for dl in download_locations:
            if dl:
                return dl

    def _get_size_matching_candidates(self):
        # Map each relative file path from the torrent to a list of candidates.
        # A candidate is a dictionary that stores information about an existing
        # file with the expected size.
        candidates = collections.defaultdict(lambda: [])
        for filepath, location in self._each_file(*self._locations):
            for file in self._unfound_files:
                if self._is_size_match(file, filepath):
                    # Candidates are dictionaries:
                    #         file: torf.File object (relative file path in torrent)
                    #     location: Download path to pass to the BitTorrent
                    #               client along with the torrent file
                    #     filepath: Existing file path with same size as `file`
                    # filepath_rel: `filepath` without `location`
                    #               (`location` / `filepath` is the same as `filepath`)
                    #   similarity: How close `file` is to `filepath_rel` as
                    #               float from 0.0 to 1.0
                    filepath_rel = filepath[len(location):].lstrip(os.sep)
                    candidates[file].append({
                        'location': location,
                        'filepath': filepath,
                        'filepath_rel': filepath_rel,
                        'similarity': self._get_path_similarity(filepath_rel, str(file)),
                    })

        candidates = self._sort_candidates(candidates)
        candidates = self._limit_candidates(candidates)
        return candidates

    def _get_unrenamed_candidates(self):
        # Same as _get_size_matching_candidates(), but instead of finding
        # candidates by size, we just look for each torrent file at each
        # location.
        candidates = collections.defaultdict(lambda: [])

        for file in self._unfound_files:
            for location in self._locations:
                filepath = os.path.join(location, file)
                filepath_rel = str(file)
                if self._is_size_match(file, filepath):
                    candidates[file].append({
                        'location': location,
                        'filepath': filepath,
                        'filepath_rel': filepath_rel,
                        'similarity': self._get_path_similarity(filepath_rel, str(file)),
                    })

        return dict(candidates)

    def _get_download_location(self, candidates):
        download_location = None

        # `paths` maps relative file paths expected by torrent to a candidate
        # dictionary from `candidates`.
        for paths in self._each_set_of_linked_candidates(candidates):
            _debug('%d / %d files', len(self._found_files), len(self._torrent_files))
            for file, candidate in paths.items():
                if file not in self._found_files:
                    if self._verify_file(file, location=candidate['temporary_location']):
                        # Use download location of first matching file.
                        if download_location is None:
                            _debug('Setting download location: %r', candidate['location'])
                            download_location = candidate['location']

                        _debug('  %s: Using %r', file, candidate['filepath'])
                        self._matching_files[file] = candidate['filepath']
                        self._found_files.add(file)

                    else:
                        _debug('  %s: Not using %r', file, candidate['filepath'])
                else:
                    _debug('  %s: Already found %r', file, self._matching_files[file])

            if len(self._found_files) == len(self._torrent_files):
                _debug('All files found: %r', tuple(self._matching_files))
                break

        return download_location

    def _each_set_of_linked_candidates(self, candidates):
        _debug('Iterating over combinations of temporary symlinks:')
        for file, cands in sorted(candidates.items()):
            _debug('  * %s -> %s', [c['filepath'] for c in cands], file)

        combinator = Combinator(candidates)
        for pairs in combinator:
            with self._temporary_directory as location:
                # Create temporary links as they are expected by the torrent.
                for file, candidate in pairs:
                    candidate['temporary_location'] = location
                    source = os.path.abspath(candidate['filepath'])
                    target = os.path.join(location, file)
                    self._create_symlink(source, target)

                # Map torrent file path to other relevant information that is
                # needed for matching.
                yield {file: candidate for file, candidate in pairs}

                # Do not iterate over new combinations of files we already
                # found.
                for file in sorted(self._found_files):
                    if file in combinator.keys:
                        combinator.lock(file)

            # Ensure temporary links are removed.
            assert not os.path.exists(location), location

    def _sort_candidates(self, candidates):
        # Sort candidates by file path similarity.
        return {
            file: sorted(cands, key=lambda c: c['similarity'], reverse=True)
            for file, cands in candidates.items()
        }

    _max_candidates_per_file = 3

    def _limit_candidates(self, candidates):
        # Sort size-matching files by file path similarity.
        return {
            file: cands[:self._max_candidates_per_file]
            for file, cands in candidates.items()
        }

    @staticmethod
    def _get_path_similarity(a, b, _is_junk=lambda x: x in '. -/'):
        return difflib.SequenceMatcher(_is_junk, a, b, autojunk=False).ratio()

    def _each_file(self, *paths):
        # Yield (filepath, path) tuples where the first item is a file (more
        # specifically: a non-directory) beneath the second item. The second
        # item is a path from `paths`. If there is a file path in `paths`, it is
        # yielded as both items of the tuple.
        for path in paths:
            _debug('Searching %s', path)
            if not os.path.isdir(path):
                yield (str(path), str(path))
            else:
                for root, dirnames, filenames in os.walk(path, followlinks=True):
                    for filename in filenames:
                        yield (str(os.path.join(root, filename)), str(path))

    @property
    def _unfound_files(self):
        return sorted(set(self._torrent_files).difference(self._found_files))

    @functools.lru_cache(maxsize=None)
    def _is_size_match(self, torrentfile, filepath):
        # Return whether a file in a torrent and an existing file are the same
        # size.
        return torrentfile.size == self._get_file_size(filepath)

    def _get_file_size(self, filepath):
        # os.path.getsize("path/to/directory") returns 4096
        if not os.path.isdir(filepath):
            try:
                return os.path.getsize(filepath)
            except OSError:
                pass
        return None

    def _verify_file(self, file, location):
        _debug('  Verifying %s at %s', file, location)
        content_path = os.path.join(location, self._torrent.name)
        with torf.TorrentFileStream(self._torrent, content_path=content_path) as tfs:
            # Don't check the first and the last piece of a file as they likely
            # overlap with another file that might be invalid or missing.
            file_piece_indexes = tfs.get_absolute_piece_indexes(file, (1, -2))
            _debug('    Verifying pieces: %r', file_piece_indexes)
            for piece_index in file_piece_indexes:
                piece_ok = tfs.verify_piece(piece_index)
                if piece_ok is True:
                    _debug('    Piece %d is valid', piece_index)
                elif piece_ok is False:
                    _debug('    Piece %d is invalid', piece_index)
                    return False
                elif piece_ok is None:
                    _debug('    Piece %d is unverifiable; probably non-existing file', piece_index)
                    return None
        return True

    def _create_hardlink(self, source, target):
        return self._create_link(self._hardlink_or_symlink, source, target)

    def _hardlink_or_symlink(self, source, target):
        # Try hard link and default to symlink.
        try:
            os.link(source, target)
        except OSError as e:
            if e.errno == errno.EXDEV:
                # Invalid cross-device link (`source` and `target` are on
                # different file systems)
                os.symlink(source, target)
            else:
                raise

    def _create_symlink(self, source, target):
        return self._create_link(os.symlink, source, target)

    def _create_link(self, create_link_function, source, target):
        if not os.path.exists(target):
            # Create parent directory if it doesn't exist.
            target_parent = os.path.dirname(target)
            try:
                os.makedirs(target_parent, exist_ok=True)
            except OSError as e:
                msg = e.strerror if e.strerror else e
                raise FindError(f'Failed to create directory {target_parent}: {msg}')
            else:
                # Create link.
                _debug(f'{create_link_function.__qualname__}({source!r}, {target!r})')
                try:
                    create_link_function(source, target)
                except OSError as e:
                    msg = e.strerror if e.strerror else e
                    raise FindError(f'Failed to link {source} to {target}: {msg}')
        else:
            _debug('Already exists: %r', target)

    def create_links(self, download_location):
        for target, source in self._matching_files.items():
            target_path = os.path.join(download_location, target)
            self._create_hardlink(source, target_path)

    @property
    def _temporary_directory(self):
        # Avoid illegal characters.
        name = ''.join(
            c if c in self._allowed_filename_characters else '_'
            for c in self._torrent.name
        )
        # TemporaryDirectory is a context manager that automatically deletes the
        # directory when leaving the context.
        return tempfile.TemporaryDirectory(prefix=f'{__project_name__}.{name}.')

    _allowed_filename_characters = (
        string.ascii_letters
        + string.digits
        + " ',.-"
    )
