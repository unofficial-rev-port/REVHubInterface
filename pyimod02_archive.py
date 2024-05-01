# uncompyle6 version 3.9.1
# Python bytecode version base 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Aug 23 2022, 17:18:36) 
# [GCC 11.2.0]
# Embedded file name: c:\python27\Lib\site-packages\PyInstaller\loader\pyimod02_archive.py
# Compiled at: 1995-09-27 08:18:56
import marshal, struct, sys, zlib
if sys.version_info[0] == 2:
    import thread
else:
    import _thread as thread
CRYPT_BLOCK_SIZE = 16
PYZ_TYPE_MODULE = 0
PYZ_TYPE_PKG = 1
PYZ_TYPE_DATA = 2

class FilePos(object):
    """
    This class keeps track of the file object representing and current position
    in a file.
    """

    def __init__(self):
        self.file = None
        self.pos = 0
        return


class ArchiveFile(object):
    """
    File class support auto open when access member from file object
    This class is use to avoid file locking on windows
    """

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self._filePos = {}

    def local(self):
        """
        Return an instance of FilePos for the current thread. This is a crude
        # re-implementation of threading.local, which isn't a built-in module
        # and therefore isn't available.
        """
        ti = thread.get_ident()
        if ti not in self._filePos:
            self._filePos[ti] = FilePos()
        return self._filePos[ti]

    def __getattr__(self, name):
        """
        Make this class act like a file, by invoking most methods on its
        underlying file object.
        """
        file = self.local().file
        assert file
        return getattr(file, name)

    def __enter__(self):
        """
        Open file and seek to pos record from last close.
        """
        fp = self.local()
        assert not fp.file
        fp.file = open(*self.args, **self.kwargs)
        fp.file.seek(fp.pos)

    def __exit__(self, type, value, traceback):
        """
        Close file and record pos.
        """
        fp = self.local()
        assert fp.file
        fp.pos = fp.file.tell()
        fp.file.close()
        fp.file = None
        return


class ArchiveReadError(RuntimeError):
    pass


class ArchiveReader(object):
    """
    A base class for a repository of python code objects.
    The extract method is used by imputil.ArchiveImporter
    to get code objects by name (fully qualified name), so
    an enduser "import a.b" would become
      extract('a.__init__')
      extract('a.b')
    """
    MAGIC = 'PYL\x00'
    HDRLEN = 12
    TOCPOS = 8
    os = None
    _bincache = None

    def __init__(self, path=None, start=0):
        """
        Initialize an Archive. If path is omitted, it will be an empty Archive.
        """
        self.toc = None
        self.path = path
        self.start = start
        if sys.version_info[0] == 2:
            import imp
            self.pymagic = imp.get_magic()
        else:
            import _frozen_importlib
            if sys.version_info[1] == 4:
                self.pymagic = _frozen_importlib.MAGIC_NUMBER
            else:
                self.pymagic = _frozen_importlib._bootstrap_external.MAGIC_NUMBER
        if path is not None:
            self.lib = ArchiveFile(self.path, 'rb')
            with self.lib:
                self.checkmagic()
                self.loadtoc()
        return

    def loadtoc(self):
        """
        Overridable.
        Default: After magic comes an int (4 byte native) giving the
        position of the TOC within self.lib.
        Default: The TOC is a marshal-able string.
        """
        self.lib.seek(self.start + self.TOCPOS)
        offset, = struct.unpack('!i', self.lib.read(4))
        self.lib.seek(self.start + offset)
        self.toc = dict(marshal.loads(self.lib.read()))

    def is_package(self, name):
        ispkg, pos = self.toc.get(name, (0, None))
        if pos is None:
            return
        else:
            return bool(ispkg)

    def extract(self, name):
        """
        Get the object corresponding to name, or None.
        For use with imputil ArchiveImporter, object is a python code object.
        'name' is the name as specified in an 'import name'.
        'import a.b' will become:
        extract('a') (return None because 'a' is not a code object)
        extract('a.__init__') (return a code object)
        extract('a.b') (return a code object)
        Default implementation:
          self.toc is a dict
          self.toc[name] is pos
          self.lib has the code object marshal-ed at pos
        """
        ispkg, pos = self.toc.get(name, (0, None))
        if pos is None:
            return
        else:
            with self.lib:
                self.lib.seek(self.start + pos)
                obj = marshal.loads(self.lib.read())
            return (
             ispkg, obj)

    def contents(self):
        """
        Return a list of the contents
        Default implementation assumes self.toc is a dict like object.
        Not required by ArchiveImporter.
        """
        return list(self.toc.keys())

    def checkmagic(self):
        """
        Overridable.
        Check to see if the file object self.lib actually has a file
        we understand.
        """
        self.lib.seek(self.start)
        if self.lib.read(len(self.MAGIC)) != self.MAGIC:
            raise ArchiveReadError('%s is not a valid %s archive file' % (
             self.path, self.__class__.__name__))
        if self.lib.read(len(self.pymagic)) != self.pymagic:
            raise ArchiveReadError('%s has version mismatch to dll' % self.path)
        self.lib.read(4)


class Cipher(object):
    """
    This class is used only to decrypt Python modules.
    """

    def __init__(self):
        import pyimod00_crypto_key
        key = pyimod00_crypto_key.key
        assert type(key) is str
        if len(key) > CRYPT_BLOCK_SIZE:
            self.key = key[0:CRYPT_BLOCK_SIZE]
        else:
            self.key = key.zfill(CRYPT_BLOCK_SIZE)
        assert len(self.key) == CRYPT_BLOCK_SIZE
        self._aes = self._import_aesmod()

    def _import_aesmod(self):
        """
        Tries to import the AES module from PyCrypto.

        PyCrypto 2.4 and 2.6 uses different name of the AES extension.
        """
        modname = 'Crypto.Cipher._AES'
        if sys.version_info[0] == 2:
            from pyimod03_importers import CExtensionImporter
            importer = CExtensionImporter()
            mod = importer.find_module(modname)
            if not mod:
                modname = 'Crypto.Cipher.AES'
                mod = importer.find_module(modname)
                if not mod:
                    raise ImportError(modname)
            mod = mod.load_module(modname)
        else:
            kwargs = dict(fromlist=['Crypto', 'Cipher'])
            try:
                mod = __import__(modname, **kwargs)
            except ImportError:
                modname = 'Crypto.Cipher.AES'
                mod = __import__(modname, **kwargs)

        if modname in sys.modules:
            del sys.modules[modname]
        return mod

    def __create_cipher(self, iv):
        return self._aes.new(self.key, self._aes.MODE_CFB, iv)

    def decrypt(self, data):
        return self.__create_cipher(data[:CRYPT_BLOCK_SIZE]).decrypt(data[CRYPT_BLOCK_SIZE:])


class ZlibArchiveReader(ArchiveReader):
    """
    ZlibArchive - an archive with compressed entries. Archive is read
    from the executable created by PyInstaller.

    This archive is used for bundling python modules inside the executable.

    NOTE: The whole ZlibArchive (PYZ) is compressed so it is not necessary
          to compress single modules with zlib.
    """
    MAGIC = 'PYZ\x00'
    TOCPOS = 8
    HDRLEN = ArchiveReader.HDRLEN + 5

    def __init__(self, path=None, offset=None):
        if path is None:
            offset = 0
        elif offset is None:
            for i in range(len(path) - 1, -1, -1):
                if path[i] == '?':
                    try:
                        offset = int(path[i + 1:])
                    except ValueError:
                        continue

                    path = path[:i]
                    break
            else:
                offset = 0

        super(ZlibArchiveReader, self).__init__(path, offset)
        try:
            import pyimod00_crypto_key
            self.cipher = Cipher()
        except ImportError:
            self.cipher = None

        return

    def is_package(self, name):
        typ, pos, length = self.toc.get(name, (0, None, 0))
        if pos is None:
            return
        else:
            return typ == PYZ_TYPE_PKG

    def extract(self, name):
        typ, pos, length = self.toc.get(name, (0, None, 0))
        if pos is None:
            return
        else:
            with self.lib:
                self.lib.seek(self.start + pos)
                obj = self.lib.read(length)
            try:
                if self.cipher:
                    obj = self.cipher.decrypt(obj)
                obj = zlib.decompress(obj)
                if typ in (PYZ_TYPE_MODULE, PYZ_TYPE_PKG):
                    obj = marshal.loads(obj)
            except EOFError:
                raise ImportError("PYZ entry '%s' failed to unmarshal" % name)

            return (
             typ, obj)

# okay decompiling pyimod02_archive.pyc
