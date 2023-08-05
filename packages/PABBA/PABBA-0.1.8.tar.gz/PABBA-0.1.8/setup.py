import logging
import setuptools
from distutils.errors import CCompilerError, DistutilsExecError, DistutilsPlatformError
from setuptools import Extension

try:
    from Cython.Distutils import build_ext
except ImportError as e:
    warnings.warn(e.args[0])
    from setuptools.command.build_ext import build_ext
    cython_is_installed = False
    
    
with open("README.rst", 'r') as f:
    long_description = f.read()


class CustomBuildExtCommand(build_ext):
    """build_ext command for use when numpy headers are needed."""

    def run(self):
        import numpy
        self.include_dirs.append(numpy.get_include())
        build_ext.run(self)
        
        
logging.basicConfig()
log = logging.getLogger(__file__)
ext_errors = (CCompilerError,
              DistutilsExecError, 
              DistutilsPlatformError,
              IOError, 
              SystemExit)

cython_is_installed = True 

compmem = Extension('PABBA.compmem',
                        sources=['PABBA/compmem.pyx'])

aggmem = Extension('PABBA.aggmem',
                        sources=['PABBA/aggmem.pyx'])

inversetc = Extension('PABBA.inversetc',
                        sources=['PABBA/inversetc.pyx'])

        
        
setup_args = {'name':"PABBA",
        'packages':setuptools.find_packages(),
        'version':"0.1.8",
        # 'setup_requires':["numpy", "cython"],
        'cmdclass': {'build_ext': CustomBuildExtCommand},
        'install_requires':["numpy>=1.17.3", "scipy>=1.2.1",
                            "joblib>=1.1.1",
                            "requests",
                            "pandas", 
                            "scikit-learn",
                            "matplotlib"],
        # 'package_data':{"PABBA": ["aggmem.pyx", "compmem.pyx", "inversetc.pyx"],
        #               },
        'packages': ['PABBA'],
        # 'include_dirs':[numpy.get_include()],
        'long_description':long_description,
        'author':"Xinye Chen, Stefan Güttel",
        'author_email':"xinye.chen@manchester.ac.uk, stefan.guettel@manchester.ac.uk",
        'classifiers':["Intended Audience :: Science/Research",
                    "Intended Audience :: Developers",
                    "Programming Language :: Python",
                    "Topic :: Software Development",
                    "Topic :: Scientific/Engineering",
                    "Operating System :: Microsoft :: Windows",
                    "Operating System :: Unix",
                    "Programming Language :: Python :: 3",
                    "Programming Language :: Python :: 3.6",
                    "Programming Language :: Python :: 3.7",
                    "Programming Language :: Python :: 3.8",
                    "Programming Language :: Python :: 3.9",
                    "Programming Language :: Python :: 3.10"
                    ],
        'description':"PABBA: A Unified ABBA Symbolic Representation Method",
        'long_description_content_type':'text/x-rst',
        'url':"https://github.com/nla-group/PABBA",
        'license':'BSD 3-Clause'
    }

if cython_is_installed:
    try:
        from Cython.Build import cythonize
        setuptools.setup(
            setup_requires=["cython", "numpy>=1.17.3"],
            **setup_args,
            # ext_modules=cythonize(["PABBA/aggmem.pyx", 
            #                       "PABBA/compmem.pyx", 
            #                       "PABBA/inversetc.pyx"], 
            #                      include_path=["PABBA"]),
            ext_modules=[
                 compmem,
                 aggmem,
                 inversetc
                ]
        )

    except ext_errors as ext_reason:
        log.warn(ext_reason)
        log.warn("The C extension could not be compiled.")
        if 'build_ext' in setup_args['cmdclass']:
            del setup_args['cmdclass']['build_ext']
        setuptools.setup(setup_requires=["numpy>=1.17.3"], **setup_args)
else:
    log.warn(ext_reason)
    log.warn("The C extension could not be compiled.")
    if 'build_ext' in setup_args['cmdclass']:
        del setup_args['cmdclass']['build_ext']
    setuptools.setup(setup_requires=["numpy>=1.17.3"], **setup_args)
