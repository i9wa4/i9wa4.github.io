# Treefmt configuration (i9wa4.github.io-specific formatters)
# Base configuration is inherited from dotfiles
{
  perSystem = {pkgs, ...}: {
    treefmt = {
      programs = {
        # Nix (minimal - only used in flake.nix)
        alejandra.enable = true;

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

        # Lua (uses .stylua.toml for configuration)
        # NOTE: Disabled to avoid Swift compilation (enable when cachix is available)
        # stylua.enable = true;

        # Markdown, YAML, JSON
        # NOTE: .qmd files are excluded (Quarto format, prettier cannot parse)
        prettier = {
          enable = true;
          includes = [
            "*.md"
            "*.json"
            "*.yaml"
            "*.yml"
          ];
        };
      };

      # Repository-specific excludes
      settings.global.excludes = [
        "zenn/raw/*" # Zenn articles (synced from external source)
      ];
    };
  };
}
