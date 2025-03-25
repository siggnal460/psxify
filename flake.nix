{
  description = "PSXify, a simple script to turn any image file into a PS1 texture.";

  inputs =
    {
      nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
    };

  outputs = { nixpkgs, ... }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
    in
    {
      devShells.x86_64-linux.default =
        pkgs.mkShell
          {
            nativeBuildInputs = with pkgs; [
              python313
							python313Packages.pillow
							python313Packages.black
							python313Packages.flake8
							python313Packages.mypy
            ];

            shellHook = ''
              nu
            '';
          };
    };
}
