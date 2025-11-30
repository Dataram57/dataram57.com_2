{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {

  buildInputs = [
    pkgs.python3
    pkgs.python3Packages.markdown
    pkgs.python3Packages.beautifulsoup4
    pkgs.python3Packages.requests
  ];

}
