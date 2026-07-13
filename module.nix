
{inputs, config, lib, pkgs, ...}:

let cfg = config.services.secrets-provisioner;
in{

	options.services.secrets-provisioner = {
		enable = lib.mkEnableOption "Enables the secrets provisioning https server";
		tokenDir = lib.mkOption {
			type = lib.types.path;
			description = "Which directory to monitor";
		};
		package = lib.mkOption {
			type = lib.types.package;
			default = inputs.self.packages.${pkgs.system}.default;
		};
		
		url = lib.mkOption {type = lib.types.str;
				    description = "The hostname on which this service listens";};
		sslCert = lib.mkOption { type = lib.types.str; };
		sslKey = lib.mkOption {type = lib.type.str; };
	};

	config = lib.mkIf cfg.enable {
		systemd.services.secrets-provisioner = {
			description = "Secrets provisioning HTTPS server";	
			wantedBy = ["multi-user.target"];
			serviceConfig = {
				Environment = "TOKEN_DIR=${cfg.tokenDir}";
				ExecStart = "${cfg.package.default}";
				DynamicUser = true;
				StateDirectory = "secrets-provisioner";
				Restart = "on-failure";
			};
		};
	};
}


