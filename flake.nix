{
  description = "TheKeys development environment";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
      python = pkgs.python3;
      pythonEnv = python.withPackages (ps: with ps; [
        pip
      ]);
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        packages = [
          (python.withPackages (ps: with ps; [
            pip
          ]))
        ];

        shellHook = ''
          if [ ! -d "$PWD/.venv" ]; then
            echo "→ Dependencies missing. Run: python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt -r requirements_test.txt"
          fi
        '';
      };
    };
}
