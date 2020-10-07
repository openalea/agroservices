##################  import python package #######################
import appdirs
import colorlog
from configparser import ConfigParser
import copy
import logging
import os
import platform
import requests        
from requests.models import Response
import requests_cache
import time

################ defaultParams, ConfigReadOnly, BioServicesConfig Class issue from easydev.config_tools of Thomas coeklear########################

class DynamicConfigParser(ConfigParser, object):
    """Enhanced version of Config Parser
    Provide some aliases to the original ConfigParser class and
    new methods such as :meth:`save` to save the config object in a file.
    .. code-block:: python
        >>> from easydev.config_tools import ConfigExample
        >>> standard_config_file = ConfigExample().config
        >>> c = DynamicConfigParser(standard_config_file)
        >>>
        >>> # then to get the sections, simply type as you would normally do with ConfigParser
        >>> c.sections()
        >>> # or for the options of a specific sections:
        >>> c.get_options('General')
    You can now also directly access to an option as follows::
        c.General.tag
    Then, you can add or remove sections (:meth:`remove_section`, :meth:`add_section`),
    or option from a section :meth:`remove_option`. You can save the instance into a file
    or print it::
        print(c)
    .. warning:: if you set options manually (e.G. self.GA.test =1 if GA is a
        section and test one of its options), then the save/write does not work
        at the moment even though if you typoe self.GA.test, it has the correct value
    Methods inherited from ConfigParser are available:
    ::
        # set value of an option in a section
        c.set(section, option, value=None)
        # but with this class, you can also use the attribute
        c.section.option = value
        # set value of an option in a section
        c.remove_option(section, option)
        c.remove_section(section)
    """
    def __init__(self, config_or_filename=None, *args, **kargs):

        object.__setattr__(self, '_filename', config_or_filename)
        # why not a super usage here ? Maybe there were issues related
        # to old style class ?
        ConfigParser.__init__(self, *args, **kargs)

        if isinstance(self._filename, str) and os.path.isfile(self._filename):
            self.read(self._filename)
        elif isinstance(config_or_filename, ConfigParser):
            self._replace_config(config_or_filename)
        elif config_or_filename == None:
            pass
        else:
            raise TypeError("config_or_filename must be a valid filename or valid ConfigParser instance")

    def read(self, filename):
        """Load a new config from a filename (remove all previous sections)"""
        if os.path.isfile(filename)==False:
            raise IOError("filename {0} not found".format(filename))

        config = ConfigParser()
        config.read(filename)

        self._replace_config(config)

    def _replace_config(self, config):
        """Remove all sections and add those from the input config file
        :param config:
        """
        for section in self.sections():
            self.remove_section(section)

        for section in config.sections():
            self.add_section(section)
            for option in config.options(section):
                data = config.get(section, option)
                self.set(section, option, data)

    def get_options(self, section):
        """Alias to get all options of a section in a dictionary
        One would normally need to extra each option manually::
            for option in config.options(section):
                config.get(section, option, raw=True)#
        then, populate a dictionary and finally take care of the types.
        .. warning:: types may be changed .For instance the string "True"
            is interpreted as a True boolean.
        ..  seealso:: internally, this method uses :meth:`section2dict`
        """
        return self.section2dict(section)

    def section2dict(self, section):
        """utility that extract options of a ConfigParser section into a dictionary
        :param ConfigParser config: a ConfigParser instance
        :param str section: the section to extract
        :returns: a dictionary where key/value contains all the
            options/values of the section required
        Let us build up  a standard config file:
        .. code-block:: python
            >>> # Python 3 code
            >>> from configparser import ConfigParser
            >>> c = ConfigParser()
            >>> c.add_section('general')
            >>> c.set('general', 'step', str(1))
            >>> c.set('general', 'verbose', 'True')
        To access to the step options, you would write::
            >>> c.get('general', 'step')
        this function returns a dictionary that may be manipulated as follows::
            >>> d_dict.general.step
        .. note:: a value (string) found to be True, Yes, true,
            yes is transformed to True
        .. note:: a value (string) found to be False, No, no,
            false is transformed to False
        .. note:: a value (string) found to be None; none,
            "" (empty string) is set to None
        .. note:: an integer is cast into an int
        """
        options = {}
        for option in self.options(section): # pragma no cover
            data = self.get(section, option, raw=True)
            if data.lower() in ['true', 'yes']:
                options[option] = True
            elif data.lower() in ['false', 'no']:
                options[option] = False
            elif data in ['None', None, 'none', '']:
                options[option] = None
            else:
                try: # numbers
                    try:
                        options[option] = self.getint(section, option)
                    except:
                        options[option] = self.getfloat(section, option)
                except: #string
                    options[option] = self.get(section, option, raw=True)
        return options

    def save(self, filename):
        """Save all sections/options to a file.
        :param str filename: a valid filename
        ::
            config = ConfigParams('config.ini') #doctest: +SKIP
            config.save('config2.ini') #doctest: +SKIP
        """
        try:
            if os.path.exists(filename) == True:
                print("Warning: over-writing %s " % filename)
            fp = open(filename,'w')
        except Exception as err: #pragma: no cover
            print(err)
            raise Exception('filename could not be opened')


        self.write(fp)
        fp.close()

    def add_option(self, section, option, value=None):
        """add an option to an existing section (with a value)
        .. code-block:: python
            >>> c = DynamicConfigParser()
            >>> c.add_section("general")
            >>> c.add_option("general", "verbose", True)
        """
        assert section in self.sections(), "unknown section"
        #TODO I had to cast to str with DictSection
        self.set(section, option, value=str(value))

    def __str__(self):
        str_ = ""
        for section in self.sections():
            str_ += '[' + section + ']\n'
            for option in self.options(section):
                 data = self.get(section, option, raw=True)
                 str_ += option + ' = ' + str(data)+'\n'
            str_ += '\n\n'

        return str_

    def __getattr__(self, key):
        return _DictSection(self, key)
    __getitem__ = __getattr__

    def __setattr__(self, attr, value):
        if attr.startswith('_') or attr:
            object.__setattr__(self, attr, value)
        else:
            self.__setitem__(attr, value)

    def __setitem__(self, attr, value):
        if isinstance(value, dict):
            section = self[attr]
            for k, v in value.items():
                section[k] = v
        else:
            raise TypeError('value must be a valid dictionary')

    def __delattr__(self, attr):
        if attr in self:
            self.remove_section(attr)
    def __contains__(self, attr):
        return self.has_section(attr)

    def __eq__(self, data):
        # FIXME if you read file, the string "True" is a string
        # but you may want it to be converted to a True boolean value
        if sorted(data.sections()) != sorted(self.sections()):
            print("Sections differ")
            return False
        for section in self.sections():

            for option in self.options(section):
                try:
                    if str(self.get(section, option,raw=True)) != \
                        str(data.get(section,option, raw=True)):
                        print("option %s in section %s differ" % (option, section))
                        return False
                except: # pragma: no cover
                    return False
        return True


################ defaultParams, ConfigReadOnly, BioServicesConfig Class issue from Bioservices.settings of Thomas coeklear########################
defaultParams = {
    'user.email': ["unknown", (str), "email addresss that may be used in some utilities (e.g. EUtils)"],
    'general.timeout': [30, (int,float), ""],
    'general.max_retries': [3, int, ''],
    'general.async_concurrent': [50, int, ''],
    'general.async_threshold': [10, int, 'when to switch to asynchronous requests'],
    'cache.tag_suffix': ["_agroservice_database",str, 'suffix to append for cache databases'],
    'cache.on': [False, bool, 'CACHING on/off'],
    'cache.fast': [True, bool, "FAST_SAVE option"],
    'chemspider.token': [None, (str, type(None)), 'token see http://www.chemspider.com'],
}

class ConfigReadOnly(object):
    """A generic Config file handler

    Uses appdirs from ypi to handle the XDG protocol

    Read the configuration in the XDG directory. If not found, the
    config and cache directories are created. Then, reads the configuration
    file. If not found, nothing happens. A dictionary should be provided
    to initialise the default parameters. This dictionary is updated
    wit the content of the user config file if any. Reset the parameters
    to the default values is possible at any time. Re-read the user
    config file is possible at any time (meth:`read_`)

    """
    def __init__(self, name=None, default_params={}):
        """name is going to be the generic name of the config folder

        e.g., /home/user/.config/<name>/<name>.cfg

        """
        if name is None:
            raise Exception("Name parameter must be provided")
        else:
            # use input parameters
            self.name = name
            self._default_params = copy.deepcopy(default_params)
            self.params = copy.deepcopy(default_params)

            # useful tool to handle XDG config file, path and parameters
            self.appdirs = appdirs.AppDirs(self.name)

            # useful tool to handle the config ini file
            self.config_parser = DynamicConfigParser()

            # Now, create the missing directories if needed
            self.init() # and read the user config file updating params if needed

    def read_user_config_file_and_update_params(self):
        """Read the configuration file and update parameters

        Read the configuration file (file with extension cfg and name of your
        app). Section and option found will be used to update the :attr:`params`.

        If a set of section/option is not correct (not in the :attr:`params`) then
        it is ignored.

        The :attr:`params` is a dictionary with keys being labelled as <section>.<option>
        For instance, the key "cache.on" should be written in the configuration file as::

            [cache]
            on = True

        where True is the expected value.


        """
        try:
            self.config_parser.read(self.user_config_file_path)
        except IOError:

            msg = "Welcome to %s" % self.name.capitalize()
            print(underline(msg))
            print("It looks like you do not have a configuration file.")
            print("We are creating one with default values in %s ." % self.user_config_file_path)
            print("Done")
            self.create_default_config_file()

        # now, update the params attribute if needed
        for section in self.config_parser.sections():
            dic = self.config_parser.section2dict(section)
            for key in dic.keys():
                value = dic[key]
                newkey = section + '.' + key
                if newkey in self.params.keys():
                    # the type should be self.params[newkey][1]
                    cast = self.params[newkey][1]
                    # somehow
                    if isinstance(value, cast) is True:
                        self.params[newkey][0] = value
                    else:
                        print("Warning:: found an incorrect type while parsing {} file. In section '{}', the option '{}' should be a {}. Found value {}. Trying a cast...".format(self.user_config_file_path, section, key, cast, value))
                        self.params[newkey][0] = cast(value)
                else:
                    print("Warning:: found invalid option or section in %s (ignored):" % self.user_config_file_path)
                    print("   %s %s" % (section, option))

    def _get_home(self):
        # This function should be robust
        # First, let us try with expanduser
        try:
            homedir = os.path.expanduser("~")
        except ImportError:
            # This may happen.
            pass
        else:
            if os.path.isdir(homedir):
                return homedir
        # Then, with getenv
        for this in ('HOME', 'USERPROFILE', 'TMP'):
            # getenv is same as os.environ.get
            homedir = os.environ.get(this)
            if homedir is not None and os.path.isdir(homedir):
                return homedir
        return None
    home = property(_get_home)

    def _mkdirs(self, newdir, mode=0o777):
        """from matplotlib mkdirs

        make directory *newdir* recursively, and set *mode*.  Equivalent to ::

        > mkdir -p NEWDIR
        > chmod MODE NEWDIR
        """
        try:
            if not os.path.exists(newdir):
                parts = os.path.split(newdir)
                for i in range(1, len(parts) + 1):
                    thispart = os.path.join(*parts[:i])
                    if not os.path.exists(thispart):
                        os.makedirs(thispart, mode)

        except OSError as err:
            # Reraise the error unless it's about an already existing directory
            if err.errno != errno.EEXIST or not os.path.isdir(newdir):
                raise

    def _get_and_create(self, sdir):
        if not os.path.exists(sdir):
            print("Creating directory %s " % sdir)
            try:
                self._mkdirs(sdir)
            except Exception:
                print("Could not create the path %s " % sdir)
                return None
        return sdir

    def _get_config_dir(self):
        sdir = self.appdirs.user_config_dir
        return self._get_and_create(sdir)
    user_config_dir = property(_get_config_dir,
            doc="return directory of this configuration file")

    def _get_cache_dir(self):
        sdir = self.appdirs.user_cache_dir
        return self._get_and_create(sdir)
    user_cache_dir = property(_get_cache_dir,
            doc="return directory of the cache")

    def _get_config_file_path(self):
        return self.user_config_dir + os.sep +self.config_file
    user_config_file_path = property(_get_config_file_path,
            doc="return configuration filename (with fullpath)")

    def _get_config_file(self):
        return self.name + ".cfg"
    config_file = property(_get_config_file,
            doc="config filename (without path)")

    def init(self):
        """Reads the user_config_file and update params.
        Creates the directories for config and cache if they do not exsits

        """
        # Let us create the directories by simply getting these 2 attributes:
        try:
            _ = self.user_config_dir
        except:
            print("Could not retrieve or create the config file and/or directory in %s" % self.name)
        try:
            _ = self.user_cache_dir
        except:
            print("Could not retrieve or create the cache file and/or directory in %s" % self.name)
        self.read_user_config_file_and_update_params()

    def create_default_config_file(self, force=False):

        # if the file already exists, we should save the file into
        # a backup file
        if os.path.exists(self.user_config_file_path):
            # we need to copy the file into a backup file
            filename = self.user_config_file_path + '.bk'
            if os.path.exists(filename) and force is False:
                print("""Trying to save the current config file {} into a backup file {}\n but it exists already. Please remove the backup file first or set the 'force' parameter to True""".format(self.user_config_file_path, filename))
                return
            else:
                shutil.copy(self.user_config_file_path, filename)

        # Now, we can rewrite the configuration file
        sections = sorted(set([x.split(".")[0] for x in self._default_params.keys()]))
        if 'general' in sections:
            sections = ["general"] + [x for x in sections if x!="general"]

        fh = open(self.user_config_file_path, "w") # open and delete content
        for section in sections:
            fh.write("[" + section +"]\n")
            options = [x.split(".")[1] for x in self._default_params.keys() if x.startswith(section+".")]
            for option in options:
                key = section + '.' + option
                value = self._default_params[key]
                try:
                    fh.write("# {}\n{} = {}\n".format(value[2], 
                        option, value[0]))
                except:
                    print('Could not write this value/option. skipped')
                    print(value, option)

            fh.write("\n")
        fh.close()

    def reload_default_params(self):
        self.params = copy.deepcopy(self._default_params)

class BioServicesConfig(ConfigReadOnly):
    def __init__(self):
        super(BioServicesConfig, self).__init__(name="agroservice",
                default_params=defaultParams)

    # some aliases
    def _get_caching(self):
        return self.params['cache.on'][0]
    def _set_caching(self, value):
        self.params['cache.on'][0] = value
    CACHING = property(_get_caching)

    def _get_fast_save(self):
        return self.params['cache.fast'][0]
    FAST_SAVE = property(_get_fast_save)

    def _get_async_concurrent(self):
        return self.params['general.async_concurrent'][0]
    CONCURRENT = property(_get_async_concurrent)

    def _get_async_threshold(self):
        return self.params['general.async_threshold'][0]
    ASYNC_THRESHOLD = property(_get_async_threshold)

    def _get_timeout(self):
        return self.params['general.timeout'][0]
    def _set_timeout(self, timeout):
        self.params['general.timeout'][0] = timeout
    TIMEOUT = property(_get_timeout, _set_timeout)

    def _get_max_retries(self):
        return self.params['general.max_retries'][0]
    def _set_max_retries(self, max_retries):
        self.params['general.max_retries'][0] = max_retries
    MAX_RETRIES = property(_get_max_retries, _set_max_retries)

################ DevTolls Class issue from easydev.tools of Thomas coeklear########################

class DevTools(object):
    """Aggregate of easydev.tools functions.
    """
    def check_range(self, value, a, b):
        """wrapper around :func:`easydev.check_range`"""
        check_range(value, a, b, strict=False)

    def check_param_in_list(self, param, valid_values):
        """wrapper around :func:`easydev.check_param_in_list`"""
        param = self.to_list(param)
        for name in param:
            check_param_in_list(name, list(valid_values))

    def swapdict(self, d):
        """wrapper around :func:`easydev.swapdict`"""
        return swapdict(d)

    def to_list(self, query):
        """Cast to a list if possible
        'a' ->['a']
        1 -> [1]
        """
        from easydev import codecs
        return codecs.to_list(query)

    def list2string(self, query, sep=",", space=False):
        """
        see :func:`easydev.tools.list2string`
        """
        from easydev import codecs
        return codecs.list2string(query, sep=sep, space=space)

    def to_json(self, dictionary):
        """Transform a dictionary to a json object"""
        return json.dumps(dictionary)

    def mkdir(self, dirname):
        """Create a directory if it does not exists; pass without error otherwise"""
        try:
            os.mkdir(dirname)
        except OSError:
            pass # exists already
        except Exception as err:
            raise(err)

    def shellcmd(self, cmd, show=False, verbose=False, ignore_errors=False):
        """See :func:`shellcmd`"""
        return shellcmd(cmd, show=show, verbose=verbose, ignore_errors=ignore_errors)

    def check_exists(self, filename):
        """Raise error message if the file does not exists"""
        if os.path.exists(filename) is False:
            raise ValueError("This file %s does not exists" % filename)

    def mkdirs(self, dirname, mode=0o777):
        mkdirs(dirname, mode=mode)

################ Logging Class issue from easydev.logging_tools of Thomas coeklear########################

colors = {
    'DEBUG':    'cyan',
    'INFO':     'green',
    'WARNING':  'yellow',
    'ERROR':    'red',
    'CRITICAL': 'bold_red'}

class Logging(object):
    """logging utility.
    ::
        >>> l = Logging("root", "INFO")
        >>> l.info("test")
        INFO:root:test
        >>> l.level = "WARNING"
        >>> l.info("test")
    """
    def __init__(self, name="root", level="WARNING"):
        self.default = name
        self._name = name
        self.formatter = colorlog.ColoredFormatter(
             "%(log_color)s%(levelname)-8s[%(name)s]: %(reset)s %(blue)s%(message)s",
             datefmt=None,
             reset=True,
             log_colors=colors,
             secondary_log_colors={},
             style='%'
        )
        self._set_name(name)


    def _set_name(self, name):
        self._name = name
        logger = colorlog.getLogger(self._name)
        if len(logger.handlers) == 0:
            handler = colorlog.StreamHandler()
            handler.setFormatter(self.formatter)
            logger.addHandler(handler)
            if self.level == 0:
                self.level = "WARNING"
            else:
                self._set_level(self.level)
    def _get_name(self):
        return self._name
    name = property(_get_name, _set_name)

    def _set_level(self, level):
        if isinstance(level, bool):
            if level is True:
                level = "INFO"
            if level is False:
                level = "ERROR"
        assert level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],\
            "you provided {}".format(level)
        logging_level = getattr(colorlog.logging.logging, level)
        colorlog.getLogger(self.name).setLevel(level)

    def _get_level(self):
        level = colorlog.getLogger(self.name).level
        if level == 10:
            return "DEBUG"
        elif level == 20:
            return "INFO"
        elif level == 30:
            return "WARNING"
        elif level == 40:
            return "ERROR"
        elif level == 50:
            return "CRITICAL"
        else:
            return level
    level = property(_get_level, _set_level)

    def debug(self, msg):
        colorlog.getLogger(self.name).debug(msg)
    def info(self, msg):
        colorlog.getLogger(self.name).info(msg)
    def warning(self, msg):
        colorlog.getLogger(self.name).warning(msg)
    def critical(self, msg):
        colorlog.getLogger(self.name).critical(msg)
    def error(self, msg):
        colorlog.getLogger(self.name).error(msg)

################ Service,Restbase,REST Class issue from bioservice.services of Thomas coeklear########################
class Service(object):
    """Base class for WSDL and REST classes

    .. seealso:: :class:`REST`, :class:`WSDLService`
    """

    #: some useful response codes
    response_codes = {
        200: 'OK',
        201: 'Created',
        400: 'Bad Request. There is a problem with your input',
        404: 'Not found. The resource you requests does not exist',
        405: 'Method not allowed',
        406: "Not Acceptable. Usually headers issue",
        410:  'Gone. The resource you requested was removed.',
        415: "Unsupported Media Type",
        500: 'Internal server error. Most likely a temporary problem',
        503: 'Service not available. The server is being updated, try again later'
        }

    def __init__(self, name, url=None, verbose=True, requests_per_sec=10,
            url_defined_later=False):
        """.. rubric:: Constructor

        :param str name: a name for this service
        :param str url: its URL
        :param bool verbose: prints informative messages if True (default is
            True)
        :param requests_per_sec: maximum number of requests per seconds
            are restricted to 3. You can change that value. If you reach the
            limit, an error is raise. The reason for this limitation is
            that some services (e.g.., NCBI) may black list you IP.
            If you need or can do more (e.g., ChEMBL does not seem to have
            restrictions), change the value. You can also have several instance
            but again, if you send too many requests at the same, your future
            requests may be retricted. Currently implemented for REST only


        All instances have an attribute called :attr:`~Service.logging` that
        is an instanceof the :mod:`logging` module. It can be used to print
        information, warning, error messages::

            self.logging.info("informative message")
            self.logging.warning("warning message")
            self.logging.error("error message")

        The attribute :attr:`~Service.debugLevel`  can be used to set the behaviour
        of the logging messages. If the argument verbose is True, the debugLebel
        is set to INFO. If verbose if False, the debugLevel is set to WARNING.
        However, you can use the :attr:`debugLevel` attribute to change it to
        one of DEBUG, INFO, WARNING, ERROR, CRITICAL. debugLevel=WARNING means
        that only WARNING, ERROR and CRITICAL messages are shown.

        """
        super(Service, self).__init__()
        self.requests_per_sec = requests_per_sec
        self.name = name
        self.logging = Logging("agroservice:%s" % self.name, verbose)

        self._url = url
        try:
            if self.url is not None:
                urlopen(self.url)
        except Exception as err:
            if url_defined_later is False:
                self.logging.warning("The URL (%s) provided cannot be reached." % self.url)
        self._easyXMLConversion = True

        # used by HGNC where some XML contains non-utf-8 characters !!
        # should be able to fix it with requests once HGNC works again
        #self._fixing_unicode = False
        #self._fixing_encoding = "utf-8"

        self.devtools = DevTools()
        self.settings = BioServicesConfig()

        self._last_call = 0

    def _calls(self):
        time_lapse = 1. / self.requests_per_sec
        current_time = time.time()
        dt = current_time - self._last_call
        
        if self._last_call == 0:
            self._last_call = current_time
            return
        else:
            self._last_call = current_time
            if dt > time_lapse:
                return
            else:
                time.sleep(time_lapse - dt)
        


    def _get_caching(self):
        return self.settings.params['cache.on'][0]
    def _set_caching(self, caching):
        self.devtools.check_param_in_list(caching, [True, False])
        self.settings.params['cache.on'][0] = caching
        # reset the session, which will be automatically created if we
        # access to the session attribute
        self._session = None
    CACHING = property(_get_caching, _set_caching)

    def _get_url(self):
        return self._url

    def _set_url(self, url):
        # something more clever here to check the URL e.g. starts with http
        if url is not None:
            url = url.rstrip("/")
            self._url = url
    url = property(_get_url, _set_url, doc="URL of this service")

    def _get_easyXMLConversion(self):
        return self._easyXMLConversion

    def _set_easyXMLConversion(self, value):
        if isinstance(value, bool) is False:
            raise TypeError("value must be a boolean value (True/False)")
        self._easyXMLConversion = value
    easyXMLConversion = property(_get_easyXMLConversion,
            _set_easyXMLConversion,
            doc="""If True, xml output from a request are converted to easyXML object (Default behaviour).""")

    def easyXML(self, res):
        """Use this method to convert a XML document into an
            :class:`~bioservices.xmltools.easyXML` object

        The easyXML object provides utilities to ease access to the XML
        tag/attributes.

        Here is a simple example starting from the following XML

        .. doctest::

            >>> from bioservices import *
            >>> doc = "<xml> <id>1</id> <id>2</id> </xml>"
            >>> s = Service("name")
            >>> res = s.easyXML(doc)
            >>> res.findAll("id")
            [<id>1</id>, <id>2</id>]

        """
        #from bioservices import xmltools
        return xmltools.easyXML(res)

    def __str__(self):
        txt = "This is an instance of %s service" % self.name
        return txt

    def pubmed(self, Id):
        """Open a pubmed Id into a browser tab

        :param Id: a valid pubmed Id in string or integer format.

        The URL is a concatenation of the pubmed URL
        http://www.ncbi.nlm.nih.gov/pubmed/ and the provided Id.

        """
        url = "http://www.ncbi.nlm.nih.gov/pubmed/"
        import webbrowser
        webbrowser.open(url + str(Id))

    def on_web(self, url):
        """Open a URL into a browser"""
        import webbrowser
        webbrowser.open(url)

    def save_str_to_image(self, data, filename):
        """Save string object into a file converting into binary"""
        with open(filename,'wb') as f:
            import binascii
            try:
                #python3
                newres = binascii.a2b_base64(bytes(data, "utf-8"))
            except:
                newres = binascii.a2b_base64(data)
            f.write(newres)


class RESTbase(Service):
    _service = "REST"
    def __init__(self, name, url=None, verbose=True, requests_per_sec=3,
                 url_defined_later=False):
        super(RESTbase, self).__init__(name, url, verbose=verbose,
            requests_per_sec=requests_per_sec,
            url_defined_later=url_defined_later)
        self.logging.info("Initialising %s service (REST)" % self.name)
        self.last_response = None

    def http_get(self):
        # should return unicode
        raise NotImplementedError

    def http_post(self):
        raise NotImplementedError

    def http_put(self):
        raise NotImplementedError

    def http_delete(self):
        raise NotImplementedError

class REST(RESTbase):
    """

    The ideas (sync/async) and code using requests were inspired from the chembl
    python wrapper but significantly changed.

    Get one value::

        >>> from bioservices import REST
        >>> s = REST("test", "https://www.ebi.ac.uk/chemblws")
        >>> res = s.get_one("targets/CHEMBL2476.json", "json")
        >>> res['organism']
        u'Homo sapiens'

    The caching has two major interests. First one is that it speed up requests if
    you repeat requests. ::


        >>> s = REST("test", "https://www.ebi.ac.uk/chemblws")
        >>> s.CACHING = True
        >>> # requests will be stored in a local sqlite database
        >>> s.get_one("targets/CHEMBL2476")
        >>> # Disconnect your wiki and any network connections.
        >>> # Without caching you cannot fetch any requests but with
        >>> # the CACHING on, you can retrieve previous requests:
        >>> s.get_one("targets/CHEMBL2476")


    Advantages of requests over urllib

    requests length is not limited to 2000 characters
    http://www.g-loaded.eu/2008/10/24/maximum-url-length/


    There is no need for authentication if the web services available
    in bioservices except for a few exception. In such case, the username and
    password are to be provided with the method call. However,
    in the future if a services requires authentication, one can set the
    attribute :attr:`authentication` to a tuple::

        s = REST()
        s.authentication = ('user', 'pass')


    Note about headers and content type. The Accept header is 
    used by HTTP clients to tell the server what content types 
    they will accept. The server will then send back a
    response, which will include a Content-Type header telling 
    the client what the content type of the returned content 
    actually is. When using the :meth:`get__headers`, you can see
    the User-Agent, the Accept and Content-Type keys. So, here the 
    HTTP requests also contain Content-Type headers. In POST or PUT requests
    the client is actually sendingdata to the server as part of the
    request, and the Content-Type header tells the server what the data actually is
    For a POST request resulting from an HTML form submission, the
    Content-Type of the request should be one of the standard form content
    types: application/x-www-form-urlencoded (default, older, simpler) or 
    multipart/form-data (newer, adds support for file uploads)

    """
    content_types = {
        'bed': 'text/x-bed',
        'default': "application/x-www-form-urlencoded",
        'gff3': 'text/x-gff3',
        'fasta': 'text/x-fasta',
        'json': 'application/json',
        "jsonp": "text/javascript",
        "nh": "text/x-nh",
        'phylip': 'text/x-phyloxml+xml',
        'phyloxml': 'text/x-phyloxml+xml',
        'seqxml': 'text/x-seqxml+xml',
        'png': 'image/png',
        'jpg': 'image/jpg',
        'svg': 'image/svg',
        'gif': 'image/gif',
        'jpeg': 'image/jpg',
        'txt': 'text/plain',
        'text': 'text/plain',
        'xml': 'application/xml',
        'yaml': 'text/x-yaml'
    }
    #special_characters = ['/', '#', '+']

    def __init__(self, name, url=None, verbose=True, cache=False,
        requests_per_sec=3, proxies=[], cert=None, url_defined_later=False):
        super(REST, self).__init__(name, url, verbose=verbose,
            requests_per_sec=requests_per_sec,
            url_defined_later=url_defined_later)
        self.proxies = proxies
        self.cert = cert

        bspath = self.settings.user_config_dir
        self.CACHE_NAME = bspath + os.sep + self.name + "_agroservice_db"

        self._session = None

        self.settings.params['cache.on'][0] = cache

        if self.CACHING:
            #import requests_cache
            self.logging.info("Using local cache %s" % self.CACHE_NAME)
            requests_cache.install_cache(self.CACHE_NAME)

    def delete_cache(self):
        cache_file = self.CACHE_NAME + '.sqlite'
        if os.path.exists(cache_file):
            msg = "You are about to delete this agroservice cache: %s. Proceed? (y/[n]) "
            res = input(msg % cache_file)
            if res == "y":
                os.remove(cache_file)
                self.logging.info("Removed cache")
            else:
                self.logging.info("Reply 'y' to delete the file")

    def clear_cache(self):
        from requests_cache import clear
        clear()

    def _build_url(self, query):
        url = None

        if query is None:
            url = self.url
        else:
            if query.startswith("http"):
                # assume we do want to use self.url
                url = query
            else:
                url = '%s/%s' % (self.url, query)

        return url

    def _get_session(self):
        if self._session is None:
            if self.CACHING is True:
                self._session = self._create_cache_session()
            else:
                self._session = self._create_session()
        return self._session
    session = property(_get_session)

    def _create_session(self):
        """Creates a normal session using HTTPAdapter

        max retries is defined in the :attr:`MAX_RETRIES`
        """
        self.logging.debug("Creating session (uncached version)")
        self._session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(max_retries=self.settings.MAX_RETRIES)
        #, pool_block=True does not work with asynchronous requests
        self._session.mount('http://', adapter)
        self._session.mount('https://', adapter)
        return self._session

    def _create_cache_session(self):
        """Creates a cached session using requests_cache package"""
        self.logging.debug("Creating session (cache version)")
        if not self._session:
            #import requests_cache
            self.logging.debug("No cached session created yet. Creating one")
            self._session = requests_cache.CachedSession(self.CACHE_NAME,
                         backend='sqlite', fast_save=self.settings.FAST_SAVE)
        return self._session

    def _get_timeout(self):
        return self.settings.TIMEOUT
    def _set_timeout(self, value):
        self.settings.TIMEOUT = value
    TIMEOUT = property(_get_timeout, _set_timeout)

    def _process_get_request(self, url, session, frmt, data=None, **kwargs):
        try:
            res = session.get(url, **kwargs)
            self.last_response = res
            res = self._interpret_returned_request(res, frmt)
            return res
        except Exception:
            return None

    def _interpret_returned_request(self, res, frmt):
        # must be a Response
        if isinstance(res, Response) is False:
            return res
        # if a response, there is a status code that should be ok
        if not res.ok:
            reason = res.reason
            self.logging.warning("status is not ok with {0}".format(reason))
            return res.status_code
        if frmt == "json":
            try:
                return res.json()
            except:
                return res
        # finally
        return res.content

    def _apply(self, iterable, fn, *args, **kwargs):
        return [fn(x, *args, **kwargs) for x in iterable if x is not None]

    def _get_async(self, keys, frmt='json', params={}):
        # does not work under pyhon3 so local import
        import grequests
        session = self._get_session()
        try:
            # build the requests
            urls = self._get_all_urls(keys, frmt)
            self.logging.debug("grequests.get processing")
            rs = (grequests.get(url, session=session, params=params)  for key,url in zip(keys, urls))
            # execute them
            self.logging.debug("grequests.map call")
            ret = grequests.map(rs, size=min(self.settings.CONCURRENT, len(keys)))
            self.last_response = ret
            self.logging.debug("grequests.map call done")
            return ret
        except Exception as err:
            self.logging.warning("Error caught in async. " + err.message)
            return []

    def _get_all_urls(self, keys, frmt=None):
        return ('%s/%s' % (self.url, query) for query in keys)

    def get_async(self, keys, frmt='json', params={}, **kargs):
        ret = self._get_async(keys, frmt, params=params, **kargs)
        return self._apply(ret, self._interpret_returned_request, frmt)

    def get_sync(self, keys, frmt='json', **kargs):
        return [self.get_one(key, frmt=frmt, **kargs) for key in keys]

    def http_get(self, query, frmt='json', params={}, **kargs):
        """

        * query is the suffix that will be appended to the main url attribute.
        * query is either a string or a list of strings.
        * if list is larger than ASYNC_THRESHOLD, use asynchronous call.

        """
        if isinstance(query, list) and len(query) > self.settings.ASYNC_THRESHOLD:
            self.logging.debug("Running async call for a list")
            return self.get_async(query, frmt, params=params, **kargs)

        if isinstance(query, list) and len(query) <= self.settings.ASYNC_THRESHOLD:
            self.logging.debug("Running sync call for a list")
            return [self.get_one(key, frmt, params=params, **kargs) for key in query]
            #return self.get_sync(query, frmt)

        # OTHERWISE
        self.logging.debug("Running http_get (single call mode)")
        #return self.get_one(**{'frmt': frmt, 'query': query, 'params':params})


        # if user provide a content, let us use it, otherwise, it will be the
        # same as the frmt provided
        content = kargs.get("content", self.content_types[frmt])

        # if user provide a header, we use it otherwise, we use the header from
        # bioservices and the content defined here above
        headers = kargs.get("headers")
        if headers is None:
            headers = {}
            headers['User-Agent'] = self.getUserAgent()
            if content is None:
                headers['Accept'] = self.content_types[frmt]
            else:
                headers['Accept'] = content
        kargs.update({"headers": headers})

        return self.get_one(query, frmt=frmt, params=params,  **kargs)

    def get_one(self, query=None, frmt='json', params={}, **kargs):
        """

        if query starts with http:// do not use self.url
        """
        self._calls()
        url = self._build_url(query)

        if url.count('//') >1:
            self.logging.warning("URL of the services contains a double //." +
                "Check your URL and remove trailing /")
        self.logging.debug(url)
        try:
            kargs['params'] = params
            kargs['timeout'] = self.TIMEOUT
            kargs['proxies'] = self.proxies
            kargs['cert'] = self.cert
            # Used only in biomart with cosmic database
            # See doc/source/biomart.rst for an example
            if hasattr(self, 'authentication'):
                kargs['auth'] = self.authentication

            #res = self.session.get(url, **{'timeout':self.TIMEOUT, 'params':params})
            res = self.session.get(url, **kargs)

            self.last_response = res
            res = self._interpret_returned_request(res, frmt)
            try:
                # for python 3 compatibility
                res = res.decode()
            except:
                pass
            return res
        except Exception as err:
            self.logging.critical(err)
            self.logging.critical("""Query unsuccesful. Maybe too slow response.
    Consider increasing it with settings.TIMEOUT attribute {}""".format(self.settings.TIMEOUT))

    def http_post(self, query, params=None, data=None,
                    frmt='xml', headers=None, files=None, content=None, **kargs):
        # query and frmt are bioservices parameters. Others are post parameters
        # NOTE in requests.get you can use params parameter
        # BUT in post, you use data
        # only single post implemented for now unlike get that can be asynchronous
        # or list of queries


        # if user provide a header, we use it otherwise, we use the header from
        # bioservices and the content defined here above
        if headers is None:
            headers = {}
            headers['User-Agent'] = self.getUserAgent()
            if content is None:
                headers['Accept'] = self.content_types[frmt]
            else:
                headers['Accept'] = content

        self.logging.debug("Running http_post (single call mode)")
        kargs.update({'query':query})
        kargs.update({'headers':headers})
        kargs.update({'files':files})
        kargs['proxies'] = self.proxies
        kargs['cert'] = self.cert
        kargs.update({'params':params})
        kargs.update({'data':data})
        kargs.update({'frmt':frmt})
        return self.post_one(**kargs)

    def post_one(self, query=None, frmt='json', **kargs):
        self._calls()
        self.logging.debug("Agroservice:: Entering post_one function")
        if query is None:
            url = self.url
        else:
            url = '%s/%s' % (self.url, query)
        self.logging.debug(url)
        try:
            res = self.session.post(url, **kargs)
            self.last_response = res
            res = self._interpret_returned_request(res, frmt)
            try:
                return res.decode()
            except:
                self.logging.debug("Agroservice:: Could not decode the response")
                return res
        except Exception as err:
            traceback.print_exc()
            return None

    def getUserAgent(self):
        #self.logging.info('getUserAgent: Begin')
        urllib_agent = 'Python-requests/%s' % requests.__version__
        #clientRevision = ''
        from agroservice import version
        clientVersion = version
        user_agent = 'Agroservice/%s (Agroservice.%s; Python %s; %s) %s' % (
            clientVersion, os.path.basename(__file__),
            platform.python_version(), platform.system(),
            urllib_agent
        )
        #self.logging.info('getUserAgent: user_agent: ' + user_agent)
        #self.logging.info('getUserAgent: End')
        return user_agent

    def get_headers(self, content='default'):
        """
        :param str content: set to default that is application/x-www-form-urlencoded
            so that it has the same behaviour as urllib2 (Sept 2014)

        """
        headers = {}
        headers['User-Agent'] = self.getUserAgent()
        headers['Accept'] = self.content_types[content]
        headers['Content-Type'] = self.content_types[content]
        #"application/json;odata=verbose" required in reactome
        #headers['Content-Type'] = "application/json;odata=verbose" required in reactome
        return headers

    def debug_message(self):
        print(self.last_response.content)
        print(self.last_response.reason)
        print(self.last_response.status_code)

    def http_delete(self, query, params=None,
                    frmt='xml', headers=None,  **kargs):
        kargs.update({'query': query})
        kargs.update({'params': params})
        kargs.update({'frmt': frmt})


        return self.delete_one(**kargs)

    def delete_one(self, query, frmt='json', **kargs):
        self._calls()
        self.logging.debug("Agroservice:: Entering delete_one function")
        if query is None:
            url = self.url
        else:
            url = '%s/%s' % (self.url, query)
        self.logging.debug(url)
        try:
            res = self.session.delete(url, **kargs)
            self.last_response = res
            res = self._interpret_returned_request(res, frmt)
            try:
                return res.decode()
            except:
                self.debug("Agroservice:: Could not decode the response")
                return res
        except Exception as err:
            print(err)
            return None
        except:
            pass