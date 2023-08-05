# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import errno
from setuptools import setup, find_packages
from setuptools.command.install import install
from subprocess import check_call


VERSION = "1.86.0a1668608050"
PLUGIN_VERSION = "1.86.0-alpha.1668608050+6e56d19f"

class InstallPluginCommand(install):
    def run(self):
        install.run(self)
        try:
            check_call(['pulumi', 'plugin', 'install', 'resource', 'azure-native', PLUGIN_VERSION])
        except OSError as error:
            if error.errno == errno.ENOENT:
                print(f"""
                There was an error installing the azure-native resource provider plugin.
                It looks like `pulumi` is not installed on your system.
                Please visit https://pulumi.com/ to install the Pulumi CLI.
                You may try manually installing the plugin by running
                `pulumi plugin install resource azure-native {PLUGIN_VERSION}`
                """)
            else:
                raise


def readme():
    try:
        with open('README.md', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return "azure-native Pulumi Package - Development Version"


setup(name='pulumi_azure_native',
      version=VERSION,
      description="A native Pulumi package for creating and managing Azure resources.",
      long_description=readme(),
      long_description_content_type='text/markdown',
      cmdclass={
          'install': InstallPluginCommand,
      },
      keywords='pulumi azure azure-native category/cloud kind/native',
      url='https://pulumi.com',
      project_urls={
          'Repository': 'https://github.com/pulumi/pulumi-azure-native'
      },
      license='Apache-2.0',
      packages=find_packages(),
      package_data={
          'pulumi_azure_native': [
              'py.typed',
              'pulumi-plugin.json',
          ]
      },
      install_requires=[
          'parver>=0.2.1',
          'pulumi>=3.35.0,<4.0.0',
          'semver>=2.8.1'
      ],
      zip_safe=False)
