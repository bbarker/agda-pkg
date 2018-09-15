from ..config import ( AGDA_DEFAULTS_PATH
                     , AGDA_DIR_PATH
                     , AGDA_LIBRARIES_PATH
                     , AGDA_PKG_PATH
                     , AGDA_VERSION
                     , DATABASE_FILE_NAME
                     , DATABASE_FILE_PATH
                     , DATABASE_SEARCH_INDEXES_PATH
                     , GITHUB_USER
                     , PACKAGE_SOURCES_PATH
                     , INDEX_REPOSITORY_BRANCH
                     , INDEX_REPOSITORY_NAME
                     , INDEX_REPOSITORY_PATH
                     , INDEX_REPOSITORY_URL
                     , REPO
                     )

from ..service.readLibFile import readLibFile
from ..service.database import db, pw
from ..service.database import ( Library
                               , LibraryVersion
                               , Keyword
                               , TestedWith
                               , Dependency
                               )
from pprint   import pprint
from pony.orm import *
from pathlib import Path

@db_session
def writeAgdaDirFiles():
  header = "-- File generated by Agda-Pkg\n"
  # libraries file
  libVersions = select(l for l in LibraryVersion if l.installed)[:]
  path_libraries = header + \
    '\n'.join(
          Path(PACKAGE_SOURCES_PATH)
          .joinpath(libVer.library.name + "@" + libVer.name)
          .as_posix()
        for libVer in libVersions)
  AGDA_LIBRARIES_PATH.write_text(path_libraries)

  # defaults file
  defaults = select(l for l in Library if l.installed and l.default)[:]
  default_libraries = header + '\n'.join( lib.name for lib in defaults) + '\n'
  AGDA_DEFAULTS_PATH.write_text(default_libraries)