use zed_extension_api::{
    self as zed, Command, ContextServerConfiguration, ContextServerId, Project, Result,
};

const MCP_REMOTE_PACKAGE: &str = "mcp-remote";
const MCP_REMOTE_VERSION: &str = "0.16.0";
const FAIRVALID_ENDPOINT: &str = "https://mcp.fairvalid.com/mcp";

struct FairValidExtension;

// Zed explicitly sets WASI PWD to the extension's designated absolute work directory.
// The spawned MCP process instead uses the open project as cwd, so relative cache
// or script paths would be unsafe here. Do not accept a project-configured path.
fn extension_paths(work_dir: &str) -> Result<(String, String)> {
    let bytes = work_dir.as_bytes();
    let unix_absolute = work_dir.starts_with('/');
    let windows_drive_absolute = bytes.len() >= 3
        && bytes[0].is_ascii_alphabetic()
        && bytes[1] == b':'
        && (bytes[2] == b'/' || bytes[2] == b'\\');
    let windows_unc_absolute = work_dir.starts_with("\\\\");
    if work_dir.is_empty()
        || work_dir.contains('\0')
        || !(unix_absolute || windows_drive_absolute || windows_unc_absolute)
    {
        return Err("Zed did not provide an absolute extension work directory; refusing to store OAuth data in a project.".into());
    }
    let base = work_dir.trim_end_matches(['/', '\\']);
    Ok((
        format!("{base}/node_modules/mcp-remote/dist/proxy.js"),
        format!("{base}/fairvalid-oauth"),
    ))
}

fn bridge_command(node: String, work_dir: &str) -> Result<Command> {
    let (proxy, auth_dir) = extension_paths(work_dir)?;
    Ok(Command {
        command: node,
        args: vec![
            proxy,
            FAIRVALID_ENDPOINT.into(),
            "--transport".into(),
            "http-only".into(),
        ],
        env: vec![("MCP_REMOTE_CONFIG_DIR".into(), auth_dir)],
    })
}

impl zed::Extension for FairValidExtension {
    fn new() -> Self {
        Self
    }

    fn context_server_command(
        &mut self,
        _context_server_id: &ContextServerId,
        _project: &Project,
    ) -> Result<Command> {
        let work_dir = std::env::var("PWD")
            .map_err(|_| "Zed did not provide its extension work directory".to_string())?;
        // Validate the boundary before downloading or starting anything.
        extension_paths(&work_dir)?;
        if zed::npm_package_installed_version(MCP_REMOTE_PACKAGE)?.as_deref()
            != Some(MCP_REMOTE_VERSION)
        {
            zed::npm_install_package(MCP_REMOTE_PACKAGE, MCP_REMOTE_VERSION)?;
        }
        if zed::npm_package_installed_version(MCP_REMOTE_PACKAGE)?.as_deref()
            != Some(MCP_REMOTE_VERSION)
        {
            return Err("Could not install the pinned FairValid transport bridge version".into());
        }
        bridge_command(zed::node_binary_path()?, &work_dir)
    }

    fn context_server_configuration(
        &mut self,
        _context_server_id: &ContextServerId,
        _project: &Project,
    ) -> Result<Option<ContextServerConfiguration>> {
        Ok(Some(ContextServerConfiguration {
            installation_instructions: include_str!(
                "../configuration/installation_instructions.md"
            )
            .into(),
            default_settings: "{}".into(),
            settings_schema: r#"{"type":"object","properties":{},"additionalProperties":false}"#
                .into(),
        }))
    }
}

zed::register_extension!(FairValidExtension);

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn refuses_missing_or_relative_cache_boundaries() {
        for path in ["", ".", "project", "../project", "C:relative", "bad\0path"] {
            assert!(extension_paths(path).is_err(), "accepted {path:?}");
        }
    }

    #[test]
    fn uses_absolute_extension_paths_for_unix_and_windows() {
        for root in [
            "/Users/reviewer/Zed/work/fairvalid",
            "C:\\Users\\reviewer\\Zed\\fairvalid",
            "\\\\server\\share\\fairvalid",
        ] {
            let (proxy, auth) = extension_paths(root).unwrap();
            assert_eq!(
                proxy,
                format!("{root}/node_modules/mcp-remote/dist/proxy.js")
            );
            assert_eq!(auth, format!("{root}/fairvalid-oauth"));
        }
    }

    #[test]
    fn command_has_fixed_endpoint_http_transport_and_isolated_auth_cache() {
        let command = bridge_command("/vendor/node".into(), "/extension/work/").unwrap();
        assert_eq!(command.command, "/vendor/node");
        assert_eq!(
            command.args,
            vec![
                "/extension/work/node_modules/mcp-remote/dist/proxy.js",
                FAIRVALID_ENDPOINT,
                "--transport",
                "http-only"
            ]
        );
        assert_eq!(
            command.env,
            vec![(
                "MCP_REMOTE_CONFIG_DIR".into(),
                "/extension/work/fairvalid-oauth".into()
            )]
        );
    }
}
