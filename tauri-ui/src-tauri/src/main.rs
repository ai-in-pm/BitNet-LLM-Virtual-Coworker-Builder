#![cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
)]

use tauri::{Manager, Window};
use std::process::Command;
use std::sync::{Arc, Mutex};
use std::thread;
use serde::{Deserialize, Serialize};
use reqwest::Client;
use serde_json::{json, Value};

// Define API server state
struct ApiServerState {
    running: bool,
    port: u16,
}

// Define app state
struct AppState {
    api_server: Arc<Mutex<ApiServerState>>,
}

// Start API server
#[tauri::command]
async fn start_api_server(state: tauri::State<'_, AppState>, port: u16) -> Result<String, String> {
    let mut api_server = state.api_server.lock().unwrap();

    if api_server.running {
        return Err("API server is already running".to_string());
    }

    // Start API server in a separate process
    let python_command = if cfg!(target_os = "windows") {
        "python"
    } else {
        "python3"
    };

    let server_script = "../examples/api_server.py";

    match Command::new(python_command)
        .arg(server_script)
        .spawn() {
            Ok(_) => {
                api_server.running = true;
                api_server.port = port;
                Ok(format!("API server started on port {}", port))
            },
            Err(e) => Err(format!("Failed to start API server: {}", e)),
        }
}

// Stop API server
#[tauri::command]
async fn stop_api_server(state: tauri::State<'_, AppState>) -> Result<String, String> {
    let mut api_server = state.api_server.lock().unwrap();

    if !api_server.running {
        return Err("API server is not running".to_string());
    }

    // In a real implementation, we would need to track the process ID and kill it
    // For now, we'll just update the state
    api_server.running = false;

    Ok("API server stopped".to_string())
}

// Check API server status
#[tauri::command]
async fn check_api_server(state: tauri::State<'_, AppState>) -> Result<bool, String> {
    let api_server = state.api_server.lock().unwrap();
    Ok(api_server.running)
}

// Get API server port
#[tauri::command]
async fn get_api_server_port(state: tauri::State<'_, AppState>) -> Result<u16, String> {
    let api_server = state.api_server.lock().unwrap();
    Ok(api_server.port)
}

// Test a tool with given arguments
#[tauri::command]
async fn test_tool(
    state: tauri::State<'_, AppState>,
    name: String,
    args: Value
) -> Result<Value, String> {
    let api_server = state.api_server.lock().unwrap();

    if !api_server.running {
        return Err("API server is not running".to_string());
    }

    let client = Client::new();
    let url = format!("http://localhost:{}/tools/{}/test", api_server.port, name);

    match client.post(&url)
        .json(&json!({ "args": args }))
        .send()
        .await {
            Ok(response) => {
                if response.status().is_success() {
                    match response.json::<Value>().await {
                        Ok(result) => Ok(result),
                        Err(e) => Err(format!("Failed to parse response: {}", e))
                    }
                } else {
                    match response.text().await {
                        Ok(error_text) => Err(format!("API error: {}", error_text)),
                        Err(e) => Err(format!("Failed to get error details: {}", e))
                    }
                }
            },
            Err(e) => Err(format!("Failed to connect to API server: {}", e))
        }
}

fn main() {
    // Initialize app state
    let app_state = AppState {
        api_server: Arc::new(Mutex::new(ApiServerState {
            running: false,
            port: 8000,
        })),
    };

    tauri::Builder::default()
        .manage(app_state)
        .invoke_handler(tauri::generate_handler![
            start_api_server,
            stop_api_server,
            check_api_server,
            get_api_server_port,
            test_tool,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
