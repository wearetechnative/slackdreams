{
  description = "Nix development dependencies for crystal and gtk";

  inputs = {
    #nixpkgs.url = github:nixos/nixpkgs/nixos-22.11;
    nixpkgs.url = github:nixos/nixpkgs/nixos-unstable;
    flake-utils.url = github:numtide/flake-utils;
    crystal-flake.url = github:manveru/crystal-flake;
  };

  outputs = inputs:
  let
    utils = inputs.flake-utils.lib;
  in
  utils.eachSystem
  [
    "x86_64-linux"
  ]
  (system:
  let
    nixpkgs = import inputs.nixpkgs {
      inherit system;
    };
  in
  {

    devShells.default = nixpkgs.pkgs.mkShell {
      buildInputs = with nixpkgs.pkgs; [
        crystal_1_7
        shards
        pkg-config
        gnumake
        openssl
        vim
        conda
      ];
    };
  });
}

