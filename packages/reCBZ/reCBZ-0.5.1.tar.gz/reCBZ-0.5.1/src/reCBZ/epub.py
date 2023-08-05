# Copyright 2022 Aleksandar Erkalović, Gwyn Vales
# This program is free software: you can redistribute it and/or modify it under
# the terms of the Affero GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the Affero GNU General Public License for more
# details.
# You should have received a copy of the Affero GNU General Public License along
# with this program. If not, see <https://www.gnu.org/licenses/agpl-3.0.en.html>
#
# 'ebooklib', authored by Aleksandar Erkalović, is licensed under the AGPL, and we
# are linking to it, therefore AGPL applies to this module as well. You may NOT
# distirubte derivatives using this module (i.e. epub.py) without also
# distributing the source code, even over a network, and any modifications to
# either epub.py or ebooklib must be licensed under the AGPL as well.
# non-commerical private use is explicitly permitted.
# WORK IN PROGRESS
from pathlib import Path
from uuid import uuid4

# *must* use the git version until Aleksandar updates the pypi version
from ebooklib import epub

from reCBZ.util import human_sort, mylog


def single_volume_epub(name:str, pages:list, width='100%', height='100%') -> str:
    # I'm too sleep deprived to figure out why but the order is inverted
    pages = pages[::-1]
    book = epub.EpubBook()

    # attempt to distinguish author / title
    if '-' in name:
        title, author = name.split('-', 1)
    else:
        title = name
        author = 'Made with reCBZ'
    book.set_identifier(str(uuid4()))
    book.set_title(title)
    book.set_language('en')
    book.add_author(author)

    # do its best to sort alphanumerically TODO is it really necessary?
    # pages = human_sort(pages)
    covert_ops = f'cover{pages[0].fmt.ext[0]}'
    book.set_cover(covert_ops, open(pages[0].fp, 'rb').read())

    # one chapter = one page = one image = lotsa bytes
    chapters = []
    for i, page in enumerate(pages, start=1):
        # source_fp = page.fp
        # basename = page.name
        static_dest = f'static/{page.name}'
        mime_type = page.fmt.mime
        size_spec = f'width={page.size[0]} height={page.size[1]}'
        mylog(f'writing {page.fp} to {static_dest} as {mime_type}')

        chapter = epub.EpubHtml(title=f'Page {i}', file_name=f'page_{i}.xhtml',
                                lang='en')
        chapter.content=f'''<html>
                            <head></head>
                            <body>
                              <img src="{static_dest}" {size_spec}'/>
                            </body>
                            </html>'''

        # read bytes
        image_content = open(page.fp, 'rb').read()
        # store read content relative to zip
        static_img = epub.EpubImage(uid=f'image_{i}', file_name=static_dest,
                                    media_type=mime_type, content=image_content)
        book.add_item(chapter)
        book.add_item(static_img)
        chapters.append(chapter)

    # on a per volume basis, use the index of where each volume starts,
    # otherwise just the first page
    book.toc = (chapters[0],)

    # add navigation files
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # create spine
    book.spine = ['cover', 'nav', *(page for page in chapters)]

    # write epub file
    source_fp = f'{name}.epub'
    epub.write_epub(source_fp, book, {})
    return source_fp


def multiple_volume_epub(title:str, volumes:list) -> None:
    raise NotImplementedError
