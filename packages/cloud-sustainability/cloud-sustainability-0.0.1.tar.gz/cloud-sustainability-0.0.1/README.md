
```shell
python setup.py sdist
TOKEN=pypi-AgEIcHlwaS5vcmcCJGM1ZDNjOTY0LTRlMzgtNDUwMi05OGVkLTVhMmY2NjNhNzlhMQACHFsxLFsiY2xvdWQtc3VzdGFpbmFiaWxpdHkiXV0AAixbMixbImQzNjllMmRiLWU1YzgtNDk5MS05ZjFiLWQzYTE5MTQ5MDA4ZiJdXQAABiA2-wfoVhLlqv3ZAjD_3LS9geuadFQOenU9Y0UCZSs0jQ
twine upload -u "__token__" -p "${TOKEN}" dist/*
```