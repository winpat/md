{ pkgs ? import <unstable> {} }:

pkgs.mkShell {
  buildInputs = with pkgs; [
    python310
    python310Packages.pytest
    python310Packages.pytest-black
    python310Packages.pytest-flake8
    python310Packages.pytest-mypy
  ];
}
