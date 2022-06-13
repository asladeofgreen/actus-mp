# actus-mp

Actus protocol meta-programming library &amp; toolchain.  The toolchain is designed to forward engineer code assets in upstream repos.  

It does so by:

1.  Parsing the following assets:

    1.1.  actus-dictionary.json.

    1.2.  actus-core reference Java implementation.

2.  Invoking code generators:

    2.1.  python -> actus-core-py

    2.2.  javascript -> actus-core-js

    2.3.  rust -> actus-core-rs

3.  Writing generated code to file system.

4.  Moving code files into relevant repository.