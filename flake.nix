{
    description = "Dev shell converted from shell.nix";
    inputs = {
        nixpkgs.url = "github:NixOS/nixpkgs";
        dr57-svc = {
            url = "github:dataram57/scv";  # Change to your actual GitHub URL
            inputs.nixpkgs.follows = "nixpkgs";
        };
    };
    outputs = { self, nixpkgs, dr57-svc }:
    let
        system = "x86_64-linux";
        pkgs = import nixpkgs { inherit system; };
    in{
        packages = {
            run-repo-a = pkgs.writeShellApplication {
            name = "run-repo-a-hello";
            runtimeInputs = [ dr57-svc.packages.${system}.default ];
            text = ''
                echo "Repo B is about to run Repo A's script:"
                scv
            '';
          };
        };

        apps = {
            # Simple app that runs repo-a's script
            repo-a-hello = dr57-svc.apps.${system}.default;

            # Custom wrapper around repo-a's script
            run-repo-a = {
                type = "app";
                program = "${self.packages.${system}.run-repo-a}/bin/run-repo-a-hello";
            };

            default = self.apps.${system}.run-repo-a;
        };


        devShells.${system}.default = pkgs.mkShell {
            packages = [
                pkgs.python3
                pkgs.python3Packages.markdown
                pkgs.python3Packages.beautifulsoup4
                pkgs.python3Packages.requests
                dr57-svc.packages.${system}.default
            ];
        };
    };
}