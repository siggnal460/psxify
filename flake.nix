{
  description = "PSXify, a simple script to turn any image file into a PS1 texture.";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.11";
  inputs.poetry2nix.url = "github:nix-community/poetry2nix";

  outputs = { self, nixpkgs, poetry2nix }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
      inherit (poetry2nix.lib.mkPoetry2Nix { inherit pkgs; }) mkPoetryApplication;
			psxify = mkPoetryApplication { projectDir = ./.; };
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        inputsFrom = [ self.packages.${system}.default ];
				nativeBuildInputs = with pkgs; [
				  python312Packages.black
				  python312Packages.mypy
				  python312Packages.flake8
				];
      };

      apps.${system}.default = {
				type = "app";
        program = "${psxify}/bin/psxify";
      };

      packages.${system}.default = psxify;
    };
}
