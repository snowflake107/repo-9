# Changelog

## v0.6.0

## Breaking changes

- The crates have been prefixed with `informalsystems-`, but the library names have been kept the same, for drop-in compatibility with former versions.

  | Former crate    | New crate                       | Library name    |
  |-----------------|---------------------------------|-----------------|
  | `pbjson`        | `informalsystems-pbjson`        | `pbjson`        |
  | `pbjson-types`  | `informalsystems-pbjson-types`  | `pbjson_types`  |
  | `pbjson-build`  | `informalsystems-pbjson-build`  | `pbjson_build`  |
  | `pbjson-test`   | `informalsystems-pbjson-test`   | `pbjson_test`   |

## Features

- Add `no_std` support to the generated code ([#1](https://github.com/informalsystems/pbjson/pull/1))
  The `informal-pbjson-types` crate now has an `std` feature which is enabled by default.
  To enable `no_std` compatibility, disable the default features on that crate.

## Previous versions

There was no changelog for versions prior to 0.6.0.

