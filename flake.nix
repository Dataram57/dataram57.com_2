{
    description = "Dev shell converted from shell.nix";

    inputs = {
        nixpkgs.url = "github:NixOS/nixpkgs";
    };

    outputs = { self, nixpkgs }:
    let
        system = "x86_64-linux"; # adjust if needed
        pkgs = import nixpkgs { inherit system; };
    in
    {
        devShells.${system}.default = pkgs.mkShell {
            buildInputs = [
                pkgs.python3
                pkgs.python3Packages.markdown
                pkgs.python3Packages.beautifulsoup4
                pkgs.python3Packages.requests
            ];
        };
    };
}
