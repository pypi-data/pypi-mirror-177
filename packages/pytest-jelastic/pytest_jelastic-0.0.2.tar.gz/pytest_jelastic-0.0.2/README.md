# Pytest-jelastic

Adds the following command-line options to your pytests:

* `--jelastic-api-url`
* `--jelastic-access-token`
* `--jelastic-env-name`

and make a `jelastic_env_info` pytest fixture available. 

## Publish new package

The `Publish` teamcity build configuration is only triggered on new git tags. Whenever a new git tag is created, the build configuration is triggered and the package published to the package manager.

```bash
git tag -a 1.0.0 -m "my version 1.0.0"
git push origin 1.0.0
```

## Use plugin

In your python project, first

```bash
pip install pytest-jelastic
```

Then, when you run your tests, make sure to at least include

```bash
pytest -p pytest_jelastic <your other options>
```
