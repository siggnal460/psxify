{
  description = "PSXify, a simple script to turn any image file into a PS1 texture.";
  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.11";
  inputs.flake-utils.url = "github:numtide/flake-utils";

  inputs = {
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };
  outputs = { self, nixpkgs, flake-utils, poetry2nix }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        inherit (poetry2nix.lib.mkPoetry2Nix { inherit pkgs; }) mkPoetryApplication;

      in {
        devShells.default = pkgs.mkShell {
          inputsFrom = [ self.packages.${system}.default ];
        };

        packages.default = mkPoetryApplication {
          projectDir = self;
        };
      }
    );
}
