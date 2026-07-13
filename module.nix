
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
		sslCertificate = lib.mkOption { type = lib.types.str; };
		sslCertificateKey = lib.mkOption {type = lib.types.str; };
	};

	config = lib.mkIf cfg.enable {
		systemd.services.secrets-provisioner = {
			description = "Secrets provisioning HTTPS server";	
			wantedBy = ["multi-user.target"];
			serviceConfig = {
				Environment = "TOKEN_DIR=${cfg.tokenDir}";
				ExecStart = "${cfg.package}/bin/secrets-provisioner";
				#DynamicUser = true;
				StateDirectory = "secrets-provisioner";
				Restart = "on-failure";
			};
		};
		services.nginx = {
			enable = true;	
			virtualHosts."${cfg.url}" = {
				sslCertificate = cfg.sslCertificate;
				sslCertificateKey = cfg.sslCertificateKey;
				forceSSL = true;

				locations."/" = {
					proxyPass = "http://localhost:8080";
					extraConfig = ''
						proxy_set_header Host $host;
						proxy_set_header X-Real-IP $remote_addr;
						proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
						proxy_set_header X-Forwarded-Proto $scheme;
					'';
				};

			};

			
		};
	};
}


