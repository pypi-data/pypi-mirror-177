# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['quara',
 'quara.creds',
 'quara.creds.cli',
 'quara.creds.cli.commands',
 'quara.creds.cli.subcommands',
 'quara.creds.cli.subcommands.authorities',
 'quara.creds.cli.subcommands.ca',
 'quara.creds.cli.subcommands.cert',
 'quara.creds.cli.subcommands.config',
 'quara.creds.cli.subcommands.csr',
 'quara.creds.cli.subcommands.key',
 'quara.creds.manager',
 'quara.creds.manager.adapters.keystores',
 'quara.creds.manager.adapters.storages',
 'quara.creds.manager.interfaces',
 'quara.creds.nebula',
 'quara.creds.nebula.api',
 'quara.creds.nebula.interfaces',
 'quara.creds.nebula.proto']

package_data = \
{'': ['*'], 'quara.creds.cli.subcommands.config': ['data/*']}

install_requires = \
['Jinja2',
 'azure-identity',
 'azure-keyvault-secrets',
 'cryptography',
 'protobuf<3.21',
 'rich',
 'typer']

entry_points = \
{'console_scripts': ['pync = quara.creds.cli:app']}

setup_kwargs = {
    'name': 'quara-creds',
    'version': '0.10.2',
    'description': '',
    'long_description': '# QUARA Creds\n\n## CLI usage\n\n### Display help\n\nSeveral subcommands are available. The `--help` option is available at different levels:\n\n```bash\n# General help\npync --help\n# cert command group help\npync cert --help\n# cert sign subcommand help\npync cert sign --help\n```\n\n### Initialize environment\n\n- Initialize with default configuration\n\n```bash\npync init\n```\n\n- Reset configuration\n\n```bash\npync init --force\n```\n\n- Configure authorities from a JSON file (either a path or an URL):\n\n```bash\npync init --authorities https://example.com/authorities.json\n```\n\n\n### Manage keypairs\n\n- Create a new keypair for current user:\n\n```bash\npync key gen\n```\n\n- Create a new keypair for a different user:\n\n```bash\npync key gen -n test\n```\n\n- List available keypairs\n\n```bash\npync key list\n```\n\n- Display a public key\n\n```bash\npync key show -n test\n```\n\n- Display a private key\n\n```bash\npync key show -n test --private\n```\n\n### Manager certificate authorities\n\n- List available authorities:\n\n```bash\npync ca list\n```\n\n- Show authorities details:\n\n```bash\npync ca show\n```\n\n- Show authorities certificates:\n\n```bash\npync ca show --pem\n```\n\n\n## Nebula certs examples\n\n#### Create a new CA and a sign a new certificate\n\n```python\nfrom quara.creds.nebula import (\n    EncryptionKeyPair,\n    SigningCAOptions,\n    SigningOptions,\n    sign_ca_certificate,\n    sign_certificate,\n    verify_certificate,\n)\n\n# Create a new CA\nca_keypair, ca_crt = sign_ca_certificate(options=SigningCAOptions(Name="test"))\n# Create a new keypair for the certificate\nenc_keypair = EncryptionKeyPair()\n# Sign a new certificate\nnew_crt = sign_certificate(\n    ca_key=ca_keypair,\n    ca_crt=ca_crt,\n    public_key=enc_keypair,\n    options=SigningOptions(\n        Name="test",\n        Ip="10.100.100.10/24",\n    ),\n)\n# Write files to disk\nca_crt.write_pem_file("ca.crt")\nca_keypair.write_private_key("ca.key")\nnew_crt.write_pem_file("node.crt")\nenc_keypair.write_private_key("node.key")\nenc_keypair.write_public_key("node.pub")\n# Verify that the certificate is valid\nverify_certificate(ca_crt=ca_crt, crt=new_crt)\n```\n\nThis example generates 5 files:\n- `ca.crt`: The CA certificate created during the first step.\n- `ca.key`: The private key of the CA. The public key is also present within this file.\n- `node.crt`: The certificate created during the second step.\n- `node.key`: The private key associated with the certificate. Unlike CA private keys, the public key is not present within the file.\n- `node.pub`: The public key associated with the certificate. The public key is also embedded within the certificate.\n\n#### Load an existing CA and sign a new certificate\n\n```python\nfrom quara.creds.nebula import (\n    Certificate,\n    EncryptionKeyPair,\n    SigningKeyPair,\n    SigningOptions,\n    sign_certificate,\n    verify_certificate,\n)\n\n# Load CA certificate\nca_crt = Certificate.from_file("ca.crt")\n# Load CA keypair\nca_keypair = SigningKeyPair.from_file("ca.key")\n# Create a new keypair for the certificate\nenc_keypair = EncryptionKeyPair()\n# Sign a new certificate\nnew_crt = sign_certificate(\n    ca_key=ca_keypair,\n    ca_crt=ca_crt,\n    public_key=enc_keypair,\n    options=SigningOptions(\n        Name="test",\n        Ip="10.100.100.10/24",\n    ),\n)\n# Write files to disk\nnew_crt.write_pem_file("node.crt")\nenc_keypair.write_private_key("node.key")\nenc_keypair.write_public_key("node.pub")\n# Verify that the certificate is valid\nverify_certificate(ca_crt=ca_crt, crt=new_crt)\n```\n\nIn this case, only 3 files are created, as the CA certificate and the CA key already existed before.\n\n#### Load an existing CA, an existing public key, and sign a new certificate\n\n```python\nfrom quara.creds.nebula import (\n    Certificate,\n    PublicEncryptionKey,\n    SigningKeyPair,\n    SigningOptions,\n    sign_certificate,\n    verify_certificate,\n)\n\n# Load CA certificate\nca_crt = Certificate.from_file("ca.crt")\n# Load CA keypair\nca_keypair = SigningKeyPair.from_file("ca.key")\n# Load public key from file\npub_key = PublicEncryptionKey.from_file("node.pub")\n# Sign a new certificate\nnew_crt = sign_certificate(\n    ca_key=ca_keypair,\n    ca_crt=ca_crt,\n    public_key=pub_key,\n    options=SigningOptions(\n        Name="test",\n        Ip="10.100.100.10/24",\n    ),\n)\n# Write files to disk\nnew_crt.write_pem_file("node.crt")\n# Verify that the certificate is valid\nverify_certificate(ca_crt=ca_crt, crt=new_crt)\n```\n\nIn this case, only the certificate file is written to disk, as all other information was known before issuing the certificate.\n',
    'author': 'charbonnierg',
    'author_email': 'guillaume.charbonnier@araymond.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
