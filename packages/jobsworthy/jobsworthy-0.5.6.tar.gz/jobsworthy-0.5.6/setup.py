# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jobsworthy',
 'jobsworthy.model',
 'jobsworthy.observer',
 'jobsworthy.observer.domain',
 'jobsworthy.observer.repo',
 'jobsworthy.performance',
 'jobsworthy.performance.repo',
 'jobsworthy.repo',
 'jobsworthy.spark_job',
 'jobsworthy.structure',
 'jobsworthy.util']

package_data = \
{'': ['*']}

install_requires = \
['PyMonad>=2.4.0,<3.0.0',
 'azure-identity>=1.11.0,<2.0.0',
 'azure-storage-file-datalake>=12.9.1,<13.0.0',
 'delta-spark>=2.1.1,<3.0.0',
 'dependency-injector>=4.40.0,<5.0.0',
 'pino>=0.6.0,<0.7.0',
 'pyspark>=3.3.0,<4.0.0',
 'rdflib>=6.2.0,<7.0.0',
 'validators>=0.20.0,<0.21.0']

entry_points = \
{'console_scripts': ['infra = databricker.infra:cli']}

setup_kwargs = {
    'name': 'jobsworthy',
    'version': '0.5.6',
    'description': '',
    'long_description': '# Jobsworth\n\nA set of utility functions and classes to aid in build Spark jobs on Azure databricks.\n\n## Job Configuration\n\n## Spark Job Module\n\nJob provides a decorator which wraps the execution of a spark job.  You use the decorator at the entry point for the job.\nAt the moment it performs 1 function; calling all the registered initialisers.\n\n```python\nfrom jobsworthy import spark_job\n```\n\n```python\n@spark_job.job()\ndef execute(args=None) -> monad.EitherMonad[value.JobState]:\n    pass\n```\n\nTo register initialisers (to be run just before the job function is called) do the following.\n\n```python\n@spark_job.register()\ndef some_initialiser():\n    ...\n```\n\nThe initialisers must be imported before the job function is called; to ensure they are registered.  To do that, either import them directly in the job module, or add them to a module `__init__.py` and import the module.\n\n\n## Model Library\n\n### Streamer\n\nThe `Streamer` module provides a fluent streaming abstraction on top of 2 hive repos (the from and to repos).  The Streamer runs a pipeline as follows:\n\n+ Read from the source repo.\n+ Perform a transformation.\n+ Write to the target repo.  This is where the stream starts and uses pyspark streaming to perform the read, transform and write.\n+ Wait for the stream to finish.\n\nTo setup a stream:\n\n```python\nfrom jobsworthy import model\n\nstreamer = (model.STREAMER()\n                 .stream_from(from_table)\n                 .stream_to(to_table)\n                 .with_transformer(transform_fn))\n\n# Execute the stream\nresult = streamer.run()\n\n# When successful it returns the Streamer wrapped in a Right.\n# When there is a failure, it returns the error (subtype of JobError) wrapped in a Left   \n\nassert result.is_right()\n```\n\nSome transformation functions require data from outside the input table.  You can configure the streamer with additional transformation context by passing in kwargs on the `with_transformer`.\n\n```python\nfrom dataclasses import dataclass\nfrom jobsworthy import model\n\n\n@dataclass\nclass TransformContext:\n    run_id: int\n\ndef transform_fn_with_ctx(df, **kwargs):\n    ...\n\n    \nstreamer = (model.Streamer()\n                 .stream_from(from_table)\n                 .stream_to(to_table)\n                 .with_transformer(transform_fn_with_ctx, run=TransformContext(run_id=1)))\n\n```\n\nWhen configuring the `stream_to` table, you can provide partition columns when writing the stream.  Provide a tuple of column names. \n\n```python\nstreamer = model.STREAMER().stream_to(to_table, (\'name\', ))\n```\n\n### Repository Module\n\nThe repo library offers a number of simple abstractions for managing Databrick/Spark databases and tables.  It is by no means an object-mapper.  Rather its a few classes with some simple functions we have found useful when working with Hive tables.\n\n```python\nfrom jobsworthy import repo\n```\n\n### SparkDB\n\n`Db` is the base class representing a Hive Database.  Once constructed it is provided to the hive table classes when they are constructed.\n\n`Db` takes a [spark session](#spark-session) and a [job config](#job-configuration).\n\n```python\ndb = repo.Db(session=spark_test_session.create_session(), config=job_config())\n```\n\nWhen intialised it checks that the database (defined in the config) exists and creates it if it doesn\'t.\n\n### Hive Table\n\n\n## Util Module\n\n### Spark Session\n\n### Secrets\n\nThe Secrets module obtains secrets using the Databricks DBUtils secrets utility.  The module acts as a wrapper for DButils.  This allows for secrets to be mocked in tests without needing DBUtils.  The CosmosDB repository is injected with the secrets provider to enable secured access to CosmosDB.\n\nThe provider requires access to the Spark session when running on Databricks.  However this is not required in test.  You also provide Secrets with a wrapper for DBUtils with also, optionally, takes a session.  Both test and production wrappers are available in the `util.databricks` module.\n\n```python\nfrom jobsworthy.util import secrets, databricks\n\nprovider = secrets.Secrets(session=di_container.session,\n                           config=job_config(),\n                           secrets_provider=databricks.DatabricksUtilsWrapper())\n```\n\nThe default secret scope name is defined from the `JobConfig` properties; `domain_name` and `data_product_name`, separated by a `.`.  This can be overridden by defining the scope on the `Secrets` constructor, or on the call to `get_secret`.  It looks like this on the constructor.\n\n```python\nprovider = secrets.Secrets(session=di_container.session,\n                           config=job_config(),\n                           secrets_provider=databricks.DatabricksUtilsWrapper(),\n                           default_scope_name="custom-scope-name")\n```\n\nGetting a secret.\n\n```python\nprovider.get_secret(secret_name="name-of-secret")  # returns an Either[secret-key]\n```\n\nSecrets is also able to return a `ClientCredential` using an Azure AD client credentials grant.  The grant requires that client id and secrets are obtainable via DBUtils through key-vault with the key names defined in `JobConfig` in the properties `client_id_key` and `client_secret_key` \n\n```python\nprovider.client_credential_grant()   # returns an Either[ClientCredential]\n```\n\nTesting using secrets.  DBUtils is not available as an open source project.  When creating the secrets provider, you can provide a DBUtils mock class which is available.  On this class you can also construct valid keys to be used for test (if required; the mock returns a dummy key response to any generic lookup).\n\nThe example below also shows how to use a non-default scope on the `get_secrets` function.\n\n```python\nfrom jobsworthy.util import secrets, databricks\n\ntest_secrets = {"my_domain.my_data_product_name": {\'my_secret\': \'a-secret\'},\n                "alt_scope": {\'my_secret\': \'b-secret\'}}\n\nprovider = secrets.Secrets(\n    session=di_container.session,\n    config=job_config(),\n    secrets_provider=databricks.DatabricksUtilMockWrapper(spark_test_session.MockPySparkSession, test_secrets))\n\nprovider.get_secret(non_default_scope_name="alt_scope", secret_name="my_secret")\n```',
    'author': 'Col Perks',
    'author_email': 'wild.fauve@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/wildfauve/jobsworth',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
