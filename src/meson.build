pkgdatadir = join_paths(get_option('prefix'), get_option('datadir'), meson.project_name())
moduledir = join_paths(pkgdatadir, 'rosetta')
gnome = import('gnome')

python = import('python')

configure_file(
  input: 'rosetta.in',
  output: 'rosetta',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'r-xr--r--'
)

configure_file(
  input: 'constants.py.in',
  output: 'constants.py',
  configuration: conf,
  install: true,
  install_dir: moduledir
)

rosetta_sources = [
  '__init__.py',
  'main.py',
  'preferences.py',
  'window.py',
]

PY_INSTALLDIR.install_sources(rosetta_sources, subdir: moduledir)

subdir('provider')