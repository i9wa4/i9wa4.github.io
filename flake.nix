{
  description = "i9wa4.github.io - Quarto blog";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-25.11-darwin";
    flake-parts.url = "github:hercules-ci/flake-parts";

    git-hooks = {
      url = "github:cachix/git-hooks.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    treefmt-nix = {
      url = "github:numtide/treefmt-nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs =
    inputs@{
      flake-parts,
      git-hooks,
      treefmt-nix,
      ...
    }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      systems = [
        "aarch64-darwin"
        "x86_64-linux"
        "aarch64-linux"
      ];

      imports = [
        git-hooks.flakeModule
        treefmt-nix.flakeModule
      ];

      perSystem =
        {
          config,
          pkgs,
          ...
        }:
        let
          ghWorkflowFiles = "^\\.github/workflows/.*\\.(yml|yaml)$";
        in
        {
          # === Dev shells ===
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

          # === Treefmt (nix fmt) ===
          treefmt = {
            projectRootFile = "flake.nix";

            programs = {
              # Nix
              nixfmt.enable = true;

              # Shell
              shfmt = {
                enable = true;
                indent_size = 2;
              };

              # Python
              ruff = {
                enable = true;
                format = true;
              };

              # Lua
              stylua.enable = true;
            };

            settings = {
              formatter = {
                stylua.options = [
                  "--column-width=120"
                  "--line-endings=Unix"
                  "--indent-type=Spaces"
                  "--indent-width=2"
                  "--quote-style=AutoPreferDouble"
                  "--call-parentheses=Always"
                ];
              };
              global.excludes = [
                ".direnv"
                ".git"
                "*.lock"
                "zenn/raw/*" # Zenn articles (synced from external source)
              ];
            };
          };

          # === Pre-commit hooks ===
          pre-commit = {
            check.enable = true;
            settings.hooks = {
              # General file checks
              end-of-file-fixer.enable = true;
              trim-trailing-whitespace.enable = true;
              check-added-large-files.enable = true;
              detect-private-keys.enable = true;
              check-merge-conflicts.enable = true;
              check-json.enable = true;
              check-yaml.enable = true;

              # Secrets detection
              gitleaks = {
                enable = true;
                entry = "${pkgs.gitleaks}/bin/gitleaks protect --verbose --redact --staged";
                pass_filenames = false;
              };

              # GitHub Actions linters
              actionlint.enable = true;

              ghalint = {
                enable = true;
                entry = "${pkgs.ghalint}/bin/ghalint run";
                files = ghWorkflowFiles;
              };

              pinact = {
                enable = true;
                entry = "${pkgs.pinact}/bin/pinact run";
                files = ghWorkflowFiles;
              };

              zizmor = {
                enable = true;
                entry = "${pkgs.zizmor}/bin/zizmor";
                files = ghWorkflowFiles;
              };

              # Shell
              shellcheck.enable = true;

              # Project-specific
              ruff-check = {
                enable = true;
                entry = "${pkgs.ruff}/bin/ruff check --fix";
                types = [ "python" ];
              };

              rumdl-check = {
                enable = true;
                entry = "${pkgs.rumdl}/bin/rumdl check";
                files = "\\.(md|qmd)$";
              };

              convert-drawio-to-png = {
                enable = true;
                entry = "bash .github/scripts/convert-drawio-to-png.sh";
                files = "assets/.*\\.drawio$";
              };

              # NOTE: uv-dependent hooks - local only (skip in CI)
              sync-zenn = {
                enable = true;
                entry = "bash -c 'if [ -z \"$NIX_BUILD_TOP\" ]; then uv run python bin/sync-zenn.py && uv run python bin/update-categories.py zenn; fi'";
                files = "^zenn/raw/articles/.*\\.md$";
                pass_filenames = false;
              };

              update-categories = {
                enable = true;
                entry = "bash -c 'if [ -z \"$NIX_BUILD_TOP\" ]; then uv run python bin/update-categories.py auto blog slides; fi'";
                files = "^(auto|blog|slides)/.*\\.qmd$";
                pass_filenames = false;
              };
            };
          };
        };
    };
}
