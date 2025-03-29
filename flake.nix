{
  description = "PSXify, a simple script to turn any image file into a PS1 texture.";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.11";
  inputs.poetry2nix.url = "github:nix-community/poetry2nix";

  outputs = { self, nixpkgs, poetry2nix }:
    let
      supportedSystems = [ "x86_64-linux" "aarch64-linux" ];
      forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
      currentSystem = "x86_64-linux";
			pkgs = forAllSystems (system: nixpkgs.legacyPackages.${system});
    in
    {
      devShells.${currentSystem}.default = pkgs.mkShell {
        inputsFrom = [ self.packages.${currentSystem}.default ];
				nativeBuildInputs = with pkgs; [
				  python312Packages.black
				  python312Packages.mypy
				  python312Packages.flake8
				];
      };

      packages = forAllSystems (system: let
        inherit (poetry2nix.lib.mkPoetry2Nix { pkgs = pkgs.${system}; }) mkPoetryApplication;
      in {
        default = mkPoetryApplication { projectDir = self; };
      });
    };
}
