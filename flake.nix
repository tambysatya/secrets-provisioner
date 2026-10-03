{

	description = "Secrets provisioner";
	inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-26.05";
	outputs = {self, nixpkgs}:
		let system ="x86_64-linux";
		    pkgs = import nixpkgs {inherit system;};
            lib = nixpkgs.lib;
            pkg = pkgs.python3Packages.buildPythonApplication {
                    pname = "secrets-provisioner";
                    version = "0.1.0";
                    src = ./.;
                    pyproject = true;
                    build-system = [
                        pkgs.python3Packages.hatchling
                    ];
                    dependencies = with pkgs.python3Packages; [
                        fastapi hypercorn cryptography 
                    ];
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
