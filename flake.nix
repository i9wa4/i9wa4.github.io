{
  description = "i9wa4.github.io - Quarto blog";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-parts.url = "github:hercules-ci/flake-parts";

    # Common pre-commit/treefmt modules from dotfiles
    dotfiles = {
      url = "github:i9wa4/dotfiles";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    git-hooks = {
      url = "github:cachix/git-hooks.nix";
      inputs.nixpkgs.follows = "dotfiles/nixpkgs";
    };

    treefmt-nix = {
      url = "github:numtide/treefmt-nix";
      inputs.nixpkgs.follows = "dotfiles/nixpkgs";
    };
  };

  outputs = inputs @ {
    flake-parts,
    git-hooks,
    treefmt-nix,
    ...
  }:
    flake-parts.lib.mkFlake {inherit inputs;} {
      systems = ["aarch64-darwin" "x86_64-linux" "aarch64-linux"];

      imports = [
        git-hooks.flakeModule
        treefmt-nix.flakeModule
        # Common modules from dotfiles
        inputs.dotfiles.flakeModules.pre-commit-base
        inputs.dotfiles.flakeModules.treefmt-base
        # Repository-specific configuration
        ./nix/pre-commit.nix
        ./nix/treefmt.nix
      ];

      perSystem = {
        config,
        pkgs,
        ...
      }: {
        devShells = {
          # Local development (includes pre-commit hooks)
          default = pkgs.mkShell {
            packages = [
              pkgs.uv
            ];
            shellHook = ''
              uv sync --frozen
              ${config.pre-commit.installationScript}
            '';
          };

          # CI environment (includes gitleaks for history scan)
          ci = pkgs.mkShell {
            packages = [
              pkgs.gitleaks
              pkgs.uv
            ];
            shellHook = ''
              uv sync --frozen
            '';
          };
        };
      };
    };
}
