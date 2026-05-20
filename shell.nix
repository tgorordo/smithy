{ pkgs ? import <nixpkgs> {}}:

pkgs.mkShellNoCC {
    packages = with pkgs; [ just uv ];
}
