#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import tempfile
import shutil
from zipfile import ZipFile, ZIP_DEFLATED, ZIP_STORED, BadZipFile
from multiprocessing.pool import ThreadPool
from functools import partial
from pathlib import Path

from PIL import Image

from reCBZ.formats import *
from reCBZ.config import Config
from reCBZ.util import mylog, MP_run_tasks, SIGNINT_ctrl_c

# TODO:
# include docstrings

class Page():
    def __init__(self, file_name):
        self.fp = Path(file_name)
        self.name = str(self.fp.name)
        self.stem = str(self.fp.stem)
        self._source_fp = self.fp
        self._img:Image.Image
        self._fmt = None
        self._closed = True

    @property
    def fmt(self):
        if self._fmt is not None:
            return self._fmt
        else:
            PIL_fmt = self.img.format
            if PIL_fmt is None:
                raise KeyError(f"Image.format returned None")
            elif PIL_fmt == "PNG":
                return Png
            elif PIL_fmt == "JPEG":
                return Jpeg
            elif PIL_fmt == "WEBP":
                # https://github.com/python-pillow/Pillow/discussions/6716
                with open(self.fp, "rb") as file:
                    if file.read(16)[-1:] == b"L":
                        return WebpLossless
                    else:
                        return WebpLossy
            else:
                raise KeyError(f"'{PIL_fmt}': invalid format")

    @fmt.setter
    def fmt(self, new):
        self._fmt = new

    @property
    def img(self):
        if self._closed:
            self._img = Image.open(self.fp)
            self._closed = False
            return self._img
        else:
            return self._img

    @img.setter
    def img(self, new:Image.Image):
        self._img = new
        self._closed = False

    @property
    def size(self):
        return self.img.size

    def save(self, dest):
        self.fmt.save(self.img, dest)
        self.fp = Path(dest)
        self.name = str(self.fp.name)
        self.stem = str(self.fp.stem)
        self._img.close()
        self._closed = True

    def __reduce__(self):
        # pickle pee. pum pa rum
        # https://stackoverflow.com/q/19855156/
        return (self.__class__, (self.fp, ))


class Archive():
    source_id:str = 'Source'
    new_id:str = ' [reCBZ]'
    temp_prefix:str = f'reCBZCACHE_'
    validbookformats:tuple = ('cbz', 'zip', 'epub', 'mobi')

    def __init__(self, filename:str):
        mylog('Archive: __init__')
        if Path(filename).exists():
            self.source_path:Path = Path(filename)
        else:
            raise ValueError(f"{filename}: invalid path")
        self._source_stem = self.source_path.stem
        self.opt_parallel = Config.parallel
        self.opt_ignore = Config.ignore
        self._zip_compress = Config.compresszip
        self._fmt_blacklist = Config.blacklistedfmts
        self._fmt_samples = Config.samplescount
        self._pages_format = Config.imageformat
        self._pages_quality = Config.quality
        self._pages_size = Config.resolution
        self._pages_bw = Config.grayscale
        self._pages_noup = Config.noupscale
        self._pages_nodown = Config.nodownscale
        self._pages_filter = Config.resamplemethod
        self._index:list = []
        self.tempdir:Path = Path('.')

    def fetch_pages(self):
        if len(self._index) == 0:
            self._index = list(self.extract())
        return self._index

    def extract(self, count:int=0, raw:bool=False) -> tuple:
        # check and clean previous tempdirs
        prev_dirs = Path(tempfile.gettempdir()).glob(f'{self.temp_prefix}*')
        for path in prev_dirs:
            assert path != tempfile.gettempdir() # for the love of god
            mylog(f'{path} exists, cleaning up')
            shutil.rmtree(path)

        self.tempdir = Path(tempfile.mkdtemp(prefix=f'{self.temp_prefix}'))
        try:
            source_zip = ZipFile(self.source_path)
        except BadZipFile as err:
            raise ValueError(f"Fatal: '{self.source_path}': not a zip file")

        compressed_files = source_zip.namelist()
        assert len(compressed_files) >= 1, 'no files in archive'
        if count > 0:
            # select x images from the middle of the archive, in increments of 2
            if count * 2 > len(compressed_files):
                raise ValueError(f"{self.source_path} is smaller than samples * 2")
            delta = int(len(compressed_files) / 2)
            compressed_files = compressed_files[delta-count:delta+count:2]

        mylog(f'Extracting: {self.source_path}', progress=True)
        for file in compressed_files:
            source_zip.extract(file, self.tempdir)

        # god bless you Georgy https://stackoverflow.com/a/50927977/
        raw_files = tuple(filter(Path.is_file, Path(self.tempdir).rglob('*')))
        pages = tuple(Page(path) for path in raw_files)

        mylog('', progress=True)
        if raw: return raw_files
        else: return pages

    def write_archive(self, book_format='cbz', file_name:str='') -> str:
        if book_format not in Archive.validbookformats:
            raise ValueError(f"Invalid format '{book_format}'")
        if file_name != '':
            parent = Path(file_name).parents[0]
            if not (parent.exists() and parent.is_dir()):
                raise ValueError(f"Parent folder '{parent}' does not exist")
            new_path = Path(f'{file_name}.{book_format}')
        else:
            # write to current dir
            new_path = Path(f'{self._source_stem}.{book_format}')
        if new_path.exists():
            mylog(f'Write .{book_format}: {new_path}', progress=True)
            mylog(f'{new_path} exists, removing...')
            new_path.unlink()

        new_path = str(new_path)
        if book_format == 'cbz':
            return self._write_zip(new_path)
        elif book_format == 'zip':
            return self._write_zip(new_path)
        elif book_format == 'epub':
            return self._write_epub(new_path)
        elif book_format == 'mobi':
            raise NotImplementedError
        else:
            raise ValueError

    def convert_pages(self, fmt=None, quality=None, grayscale=None, size=None) -> tuple:
        if fmt is not None: self._pages_format = fmt
        if quality is not None: self._pages_quality = int(quality)
        if grayscale is not None: self._pages_bw = bool(grayscale)
        if size is not None: self._pages_size = size

        source_pages = self.fetch_pages()
        if self.opt_parallel:
            results = MP_run_tasks(self._convert_page, source_pages)
        else:
            results = map(self._convert_page, source_pages)
        self._index = [page for page in results if page]
        return tuple(self._index)

    def compute_fmt_sizes(self) -> tuple:
        def compute_single_fmt(sample_pages, tempdir, fmt) -> tuple:
            fmtdir = Path.joinpath(tempdir, fmt.name)
            Path.mkdir(fmtdir)

            pfunc = partial(self._convert_page, savedir=fmtdir, format=fmt)
            if self.opt_parallel:
                results = MP_run_tasks(pfunc, sample_pages)
            else:
                results = map(pfunc, sample_pages)

            converted_pages = [page for page in results if page]
            nbytes = sum(page.fp.stat().st_size for page in converted_pages)
            return nbytes, fmt.desc, fmt.name

        # extract images and compute their original size
        # manually call extract so we don't overwrite _pages cache
        source_pages = self.extract(count=self._fmt_samples)
        nbytes = sum(page.fp.stat().st_size for page in source_pages)
        source_fmt = source_pages[0].fmt
        source_fsize = [nbytes, f'{Archive.source_id} ({source_fmt.desc})',
                        source_fmt.name]

        # compute the size of each format after converting.
        # one thread per individual format. n processes per thread
        fmt_fsizes = []
        pfunc = partial(compute_single_fmt, source_pages, self.tempdir)
        if self.opt_parallel:
            with ThreadPool(processes=len(self._valid_page_formats)) as Tpool:
                fmt_fsizes.extend(Tpool.map(pfunc, self._valid_page_formats))
        else:
            fmt_fsizes.extend(map(pfunc, self._valid_page_formats))

        # finally, compare
        # in multidepth lists, sorted compares the first element by default :)
        sorted_fmts = list(sorted(fmt_fsizes))
        sorted_fmts.insert(0, source_fsize)
        mylog(str(sorted_fmts))
        mylog('', progress=True)
        return tuple(sorted_fmts)

    def _write_zip(self, savepath):
        new_zip = ZipFile(savepath,'w')
        for page in self.fetch_pages():
            try:
                dest = page.fp.relative_to(self.tempdir)
                if self._zip_compress:
                    new_zip.write(page.fp, dest, ZIP_DEFLATED, 9)
                else:
                    new_zip.write(page.fp, dest, ZIP_STORED)
            except ValueError:
                msg = 'Path is being screwy. Does tempdir exist? '
                msg += str(self.tempdir.exists())
                msg += '\nwe might not have joined paths correctly in trans img'
                raise ValueError(msg)
        new_zip.close()
        return savepath

    def _write_epub(self, savepath):
        from reCBZ.epub import single_volume_epub
        title = self._source_stem
        mylog(f'Write .epub: {title}.epub', progress=True)
        savepath = single_volume_epub(title, self.fetch_pages())
        return savepath

    def _write_mobi(self, savepath):
        # TODO not implemented
        pass

    def _create_pages_from_path(self, fp):
        # TODO make public as add_page, append to self._pages
        return Page(fp)

    @SIGNINT_ctrl_c
    def _convert_page(self, source:Page, savedir=None, format=None): #-> None | Str:
        start_t = time.perf_counter()
        LossyFmt.quality = self._pages_quality
        # page = copy.deepcopy(source)
        page = Page(source.fp) # create a copy

        try:
            # ensure file can be opened as image
            mylog(f'Read img: {page.name}', progress=True)
            log_buff = f'/open:  {page.fp}\n'
            source_fmt = page.fmt
            img = page.img
        except IOError as err:
            if self.opt_ignore:
                mylog(f"{page.fp}: can't open file as image, ignoring...'")
                return None
            else:
                raise err
        except KeyError as err:
            if self.opt_ignore:
                mylog(f"{page.fp}: invalid image format, ignoring...'")
                return None
            else:
                raise err

        # determine target format
        if format:
            new_fmt = format
        elif self._new_page_format is not None:
            new_fmt = self._new_page_format
        else:
            new_fmt = source_fmt
        page.fmt = new_fmt

        # apply format specific actions
        if new_fmt is Jpeg:
          if not img.mode == 'RGB':
              log_buff += '|trans: mode RGB\n'
              img = img.convert('RGB')

        # transform
        if self._pages_bw:
            log_buff += '|trans: mode L\n' # me lol
            img = img.convert('L')
        if all(self._new_page_size):
            log_buff += f'|trans: resize to {self._new_page_size}\n'
            width, height = img.size
            new_size = self._new_page_size
            # preserve aspect ratio for landscape images
            if width > height:
                new_size = new_size[::-1]
            n_width, n_height = new_size
            # downscaling
            if (width > n_width and height > n_height
                and not self._pages_nodown):
                img = img.resize((new_size), self._pages_filter)
            # upscaling
            elif not self._pages_noup:
                img = img.resize((new_size), self._pages_filter)

        # save
        page.img = img
        ext = page.fmt.ext[0]
        if savedir:
            new_fp = Path.joinpath(savedir, f'{page.stem}{ext}')
        else:
            new_fp = Path.joinpath(page.fp.parents[0], f'{page.stem}{ext}')
        log_buff += f'|trans: {source_fmt.name} -> {new_fmt.name}\n'
        page.save(new_fp)

        end_t = time.perf_counter()
        elapsed = f'{end_t-start_t:.2f}s'
        mylog(f'{log_buff}\\write: {new_fp}: took {elapsed}')
        mylog(f'Save img: {new_fp.name}', progress=True)
        return page

    @property
    def _new_page_format(self):
        if self._pages_format in (None, ''): return None
        elif self._pages_format == 'jpeg': return Jpeg
        elif self._pages_format == 'png': return Png
        elif self._pages_format == 'webp': return WebpLossy
        elif self._pages_format == 'webpll': return WebpLossless
        else: raise ValueError(f"Invalid format name '{self._pages_format}'")

    @property
    def _valid_page_formats(self) -> tuple:
        all_fmts = (Png, Jpeg, WebpLossy, WebpLossless)
        try:
            blacklist = self._fmt_blacklist.lower().split(' ')
        except AttributeError: # blacklist is None
            return all_fmts
        valid_fmts = tuple(fmt for fmt in all_fmts if fmt.name not in blacklist)
        assert len(valid_fmts) >= 1, "valid_formats is 0"
        return valid_fmts

    @property
    def _new_page_size(self) -> tuple:
        default_value = (0,0)
        newsize = self._pages_size.lower().strip()
        try:
            newsize = tuple(map(int,newsize.split('x')))
            assert len(newsize) == 2
            return newsize
        except (ValueError, AssertionError):
            return default_value
