from __future__ import absolute_import
import os
import sys

DOMAIN = "localhost"
PORT = 8009
HOME_DIR = os.path.expanduser("~")
try : 
    ROOT_DIR = sys._MEIPASS
except : 
    ROOT_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
CLI_PATH = os.path.abspath(os.path.dirname(__file__))
try : 
    APP_DIR = os.path.dirname( sys.executable ) 
    if not APP_DIR.endswith('blendedcli') and not APP_DIR.endswith('Blended_CLI') :
        APP_DIR = os.path.join( APP_DIR, 'blendedcli')  # in linux executable is placed outside of APP directory so executable parent directory is not same as APP directory
    BLENDED_DATA_DIR = os.path.join(APP_DIR, '.blended_data_dir')
except:
    BLENDED_DATA_DIR = os.path.join(HOME_DIR,'Documents','.blended_data_dir')
try : 
    # sys._MEIPASS is available only when running using executable made by pyinstaller, otherwise throw Exception
    tmp_dir = sys._MEIPASS   
    if not os.path.exists(BLENDED_DATA_DIR):
        os.mkdir(BLENDED_DATA_DIR)
except: 
    pass
try : 
    tmp_dir = sys._MEIPASS
    BLENDED_DIR = os.path.join(HOME_DIR,'Documents','themes')
except: 
    BLENDED_DIR = os.path.join( os.path.abspath(os.curdir), 'themes')
SRC = "src"
LIB = "lib"
ANONYMOUS = "anonymous"
IMAGE_CACHE_DIR = os.path.join(ROOT_DIR, "media")
COMPILE_DIR = os.path.join(ROOT_DIR,'compiled')
DOT_BLENDED = ".blended"
BLENDED_RC = os.path.join(DOT_BLENDED, "blendedrc")
USER_RC = ".userrc"
PACKAGE_LIST_RC = ".packagelistrc"
PREVIEW_THEME = os.path.join(os.path.abspath(os.path.dirname(__file__)), ".previewtheme")
CACHED_THEME  = os.path.join(os.path.abspath(os.path.dirname(__file__)), "previewthemes")
PREVIEWCACHEDCONTEXT = os.path.join(os.path.abspath(os.path.dirname(__file__)), ".previewcachedcontext")
INDEX_JSON = "_index.json"
PROJECT_JSON = "_package.json"
DEFAULT_ALIAS = "parent"
PACKAGES_TYPE = ["theme", "layout", "other"]
BLOG = 'blog'
BUSINESS = 'business'
CONTRACTING = 'contracting'
FOOD = 'food'
MEDICAL = 'medical'
PORTFOLIO = 'portfolio'
NON_PROFIT = 'non_profit'
TRAVEL = 'travel'
LAYOUT = 'layout'
PACKAGE_CATEGORIES = [
    BLOG, BUSINESS, CONTRACTING, 
    FOOD, MEDICAL, PORTFOLIO, 
    NON_PROFIT, TRAVEL
]
