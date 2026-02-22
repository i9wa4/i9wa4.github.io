# Pre-commit hooks configuration (i9wa4.github.io-specific)
{
  perSystem = {pkgs, ...}: let
    # GitHub Actions workflow file pattern
    ghWorkflowFiles = "^\\.github/workflows/.*\\.(yml|yaml)$";
  in {
    pre-commit = {
      check.enable = true;
      settings.hooks = {
        # === General file checks (pre-commit-hooks package) ===
        end-of-file-fixer.enable = true;
        trim-trailing-whitespace.enable = true;
        check-added-large-files.enable = true;
        detect-private-keys.enable = true;
        check-merge-conflicts.enable = true;
        check-json.enable = true;
        check-yaml.enable = true;

        # === Secrets detection ===
        gitleaks = {
          enable = true;
          entry = "${pkgs.gitleaks}/bin/gitleaks protect --verbose --redact --staged";
          pass_filenames = false;
        };

        # === GitHub Actions linters ===
        actionlint.enable = true;

        ghalint = {
          enable = true;
          entry = "${pkgs.ghalint}/bin/ghalint run";
          files = ghWorkflowFiles;
        };

        ghatm = {
          enable = true;
          entry = "${pkgs.ghatm}/bin/ghatm set -t 5";
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

        # === Shell ===
        shellcheck.enable = true;

        # === i9wa4.github.io-specific ===
        ruff-check = {
          enable = true;
          entry = "${pkgs.ruff}/bin/ruff check --fix";
          types = ["python"];
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
}
