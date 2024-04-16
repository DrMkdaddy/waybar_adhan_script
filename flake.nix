{
  description = "Script for managing my waybar adhans";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
    poetry2nix,
  }:
    flake-utils.lib.eachDefaultSystem (system: let
      # see https://github.com/nix-community/poetry2nix/tree/master#api for more functions and examples.
      pkgs = nixpkgs.legacyPackages.${system};
      inherit (poetry2nix.lib.mkPoetry2Nix {inherit pkgs;}) mkPoetryScriptsPackage;
    in {
      packages = {
        waybar_adhan_script = mkPoetryScriptsPackage {projectDir = self;};
        default = self.packages.${system}.waybar_adhan_script;
      };

      devShells.default = pkgs.mkShell {
        inputsFrom = [self.packages.${system}.waybar_adhan_script];
        packages = [pkgs.poetry];
      };
    });
}
