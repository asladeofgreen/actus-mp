# actus-mp

Actus protocol meta-programming library &amp; toolchain.  The toolchain is designed to forward engineer code assets in upstream repos.  

It does so by:

1.  Parsing the following assets:

    1.1.  `actus-dictionary.json`.

    1.2.  `actus-core` reference Java implementation.

2.  Invoking a code generator:

    2.1   `python` | `javascript` | `rust`

3.  Writing generated code to file system.

4.  Moving code files into relevant repository:

    4.1.  `python` -> `actus-core-py`

    4.2.  `javascript` -> `actus-core-js`

    4.3.  `rust` -> `actus-core-rs`
