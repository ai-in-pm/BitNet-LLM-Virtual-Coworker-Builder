# BitNet Virtual Co-worker Builder UI

This is the desktop application for BitNet Virtual Co-worker Builder, built with Tauri and React.

## Overview

The BitNet Virtual Co-worker Builder UI provides a user-friendly interface for creating, managing, and running BitNet virtual co-workers and teams. It communicates with the BitNet Virtual Co-worker Builder API server to perform operations on models, virtual co-workers, teams, and tasks.

## Features

- **Dashboard**: Overview of your virtual co-workers, teams, and tasks
- **Models**: Manage BitNet models
- **Virtual Co-workers**: Create and manage virtual co-workers
- **Teams**: Create and manage teams of virtual co-workers
- **Tasks**: Create, run, and monitor tasks
- **Tools**: Manage tools that virtual co-workers can use
- **Settings**: Configure the application

## Development

### Prerequisites

- Node.js (v14 or later)
- Rust (for Tauri)
- BitNet Virtual Co-worker Builder API server

### Setup

1. Install dependencies:

```bash
npm install
```

2. Start the development server:

```bash
npm run tauri:dev
```

### Building

To build the application:

```bash
npm run tauri:build
```

This will create platform-specific installers in the `src-tauri/target/release` directory.

## Architecture

The UI is built with:

- **Tauri**: Cross-platform framework for building desktop applications
- **React**: Frontend library for building user interfaces
- **Ant Design**: UI component library
- **React Router**: For navigation between pages

The application communicates with the BitNet Virtual Co-worker Builder API server to perform operations on models, virtual co-workers, teams, and tasks.

## Folder Structure

```
tauri-ui/
├── src/                  # React application source code
│   ├── components/       # Reusable React components
│   ├── pages/            # Page components
│   ├── utils/            # Utility functions
│   ├── App.js            # Main application component
│   └── index.js          # Entry point
├── src-tauri/            # Tauri application source code
│   ├── src/              # Rust source code
│   ├── Cargo.toml        # Rust dependencies
│   └── tauri.conf.json   # Tauri configuration
├── public/               # Static assets
└── package.json          # Node.js dependencies
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
