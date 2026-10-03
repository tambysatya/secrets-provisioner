{

	description = "Secrets provisioner";
	inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-26.05";
	outputs = {self, nixpkgs}:
		let system ="x86_64-linux";
		    pkgs = import nixpkgs {inherit system;};
            lib = nixpkgs.lib;

            anycorn = pkgs.python3Packages.buildPythonPackage {
                  pname = "anycorn";
                  version = "0.18.6";

                  format = "wheel";

                  src = pkgs.fetchPypi {
                    pname = "anycorn";
                    version = "0.20.1";
                    format = "wheel";
                    python = "py3";
                    dist = "py3";
                    platform = "any";
                    hash="sha256-VpIMWa631uinngZ3PF9C/AB5kozS85pKkHIoX9kAcxY=";
                  };

                  dependencies = with pkgs.python3Packages; [
                    anyio
                    h2
                    h11
                    priority
                    wsproto
                    rich-click
                    sniffio
                  ];
                };
            pkg = pkgs.python3Packages.buildPythonApplication {
                    pname = "secrets-provisioner";
                    version = "0.1.0";
                    src = ./.;
                    pyproject = true;
                    build-system = [
                        pkgs.python3Packages.hatchling
                    ];
                    dependencies = with pkgs.python3Packages; [
                        fastapi anycorn cryptography 
                    ];

                    meta = {
                        mainProgram = "secrets-provisioner";
                    };
                };
		in {
            packages.${system}.default = pkg;
             /*
		     nixosModules.${system}.default = lib.evalModules {
                    modules = [import ./module.nix];
                };
             */
             hydraJobs = {
                inherit (self) packages;
             };
        };

}
