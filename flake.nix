{
  description = "i9wa4.github.io - Quarto blog";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  };

  outputs = {
    self,
    nixpkgs,
  }: let
    systems = ["aarch64-darwin" "x86_64-linux" "aarch64-linux"];
    forAllSystems = nixpkgs.lib.genAttrs systems;
  in {
    # nix fmt
    formatter = forAllSystems (system: nixpkgs.legacyPackages.${system}.alejandra);

    devShells = forAllSystems (system: let
      pkgs = nixpkgs.legacyPackages.${system};
    in {
      default = pkgs.mkShell {
        packages = [
          pkgs.actionlint
          pkgs.ghalint
          pkgs.ghatm
          pkgs.gitleaks
          pkgs.pinact
          pkgs.rumdl
          # NOTE: pre-commit is managed via `uv run pre-commit` to avoid Swift build dependency
          pkgs.shellcheck
          pkgs.shfmt
          pkgs.stylua
          pkgs.uv
          pkgs.zizmor
        ];
      };
    });
  };
}
