# Pre-commit hooks configuration (i9wa4.github.io-specific)
# Common hooks (gitleaks, actionlint, etc.) are inherited from dotfiles
{
  perSystem = {pkgs, ...}: {
    pre-commit.settings.hooks = {
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
        entry = "bash -c 'if [ -z \"$NIX_BUILD_TOP\" ]; then uv run python bin/update-categories.py blog slides; fi'";
        files = "^(blog|slides)/.*\\.qmd$";
        pass_filenames = false;
      };
    };
  };
}
