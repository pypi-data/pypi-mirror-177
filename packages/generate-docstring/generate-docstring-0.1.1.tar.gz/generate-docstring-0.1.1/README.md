# Docstring generator

## Install instruction

```bash
# Install docstring package
pip install .

# Copy vim plugin to vim pack
mkdir -p ~/.vim/packs/plugins/start
ln -s $PWD/plugins ~/.vim/packs/plugins/start/generate-docstring
```

## TODO:

* add tox support                       [ ]
* parse existing docstring              [ ]
* don't fail if no typing (annotation)  [X]
* recusrive subscipt (ex: typing.Dict)  [X]
* add raise on function                 [X]
* module attribute                      [ ]
* module name, extract filename         [X]

## Dev tools:

```
poetry run pylint --rcfile=.pylintrc ./src/
```
