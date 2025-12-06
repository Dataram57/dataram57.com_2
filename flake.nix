{
    description = "Dev shell converted from shell.nix";
    inputs = {
        nixpkgs.url = "github:NixOS/nixpkgs";
        flake-utils.url = "github:numtide/flake-utils";
        dr57-github-scv = {
            url = "github:dataram57/scv";  # Change to your actual GitHub URL
            #inputs.nixpkgs.follows = "nixpkgs";
        };
    };
    outputs = { self, nixpkgs, flake-utils, dr57-github-scv }:
    flake-utils.lib.eachDefaultSystem (system:
        let
            system = "x86_64-linux";
            pkgs = nixpkgs.legacyPackages.${system};
            dr57-scv = dr57-github-scv.packages.${system};
        in{
            packages = {};
            devShells.default = pkgs.mkShell {
                packages = [
                    pkgs.python3
                    pkgs.python3Packages.markdown
                    pkgs.python3Packages.beautifulsoup4
                    pkgs.python3Packages.requests
                    dr57-scv.default
                ];
            };
            
        }
    );
}