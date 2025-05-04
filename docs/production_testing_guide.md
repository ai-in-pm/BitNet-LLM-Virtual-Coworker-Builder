# Production Testing Guide for BitNet_LLM_Virtual_Coworker_Builder

This guide provides a comprehensive approach to testing the production setup of BitNet_LLM_Virtual_Coworker_Builder on a clean system.

## Prerequisites

Before testing the production setup, ensure you have the following:

- A clean Windows system (physical machine or virtual machine)
- Administrator access
- Internet connection
- Git installed
- Python 3.8 or higher installed
- Node.js 14 or higher installed
- npm installed

## Test Environment Setup

1. Create a test directory:
   ```powershell
   mkdir C:\BitNet-Test
   cd C:\BitNet-Test
   ```

2. Clone the repository:
   ```powershell
   git clone https://github.com/ai-in-pm/BitNet-LLM-Virtual-Coworker-Builder.git
   cd BitNet-LLM-Virtual-Coworker-Builder
   ```

## Test Plan

### 1. Basic Production Setup Test

1. Run the production setup script:
   ```powershell
   .\setup_production.ps1
   ```

2. Verify that the setup completed successfully:
   ```powershell
   .\test_production_setup.ps1
   ```

3. Check that the following directories were created:
   - `C:\BitNet-VC-Builder`
   - `C:\BitNet-VC-Builder\logs`
   - `C:\BitNet-VC-Builder\config`
   - `C:\BitNet-VC-Builder\data`
   - `C:\BitNet-VC-Builder\data\models`
   - `C:\BitNet-VC-Builder\data\cache`
   - `C:\BitNet-VC-Builder\data\memory`

4. Check that the following files were created:
   - `C:\BitNet-VC-Builder\config\config.yaml`
   - `C:\BitNet-VC-Builder\start.bat`

5. Check that the following shortcuts were created on the desktop:
   - "BitNet VC Builder - API Server"
   - "BitNet VC Builder - Web UI"
   - "Start BitNet VC Builder"

### 2. API Server Test

1. Start the API server:
   - Double-click the "BitNet VC Builder - API Server" shortcut on the desktop, or
   - Run the following command:
     ```powershell
     & "C:\BitNet-VC-Builder\venv\Scripts\python.exe" -m bitnet_vc_builder.api.server --config "C:\BitNet-VC-Builder\config\config.yaml"
     ```

2. Verify that the API server is running:
   - Open a web browser and navigate to http://localhost:8000
   - Check that the API documentation is available at http://localhost:8000/docs

3. Test API endpoints:
   - Use the Swagger UI at http://localhost:8000/docs to test the API endpoints
   - Test the following endpoints:
     - GET /health
     - GET /models
     - GET /virtual-coworkers
     - GET /teams

4. Check the API server logs:
   - Open `C:\BitNet-VC-Builder\logs\api.log`
   - Verify that there are no errors

### 3. Web UI Test

1. Start the Web UI:
   - Double-click the "BitNet VC Builder - Web UI" shortcut on the desktop, or
   - Run the following command:
     ```powershell
     & "C:\BitNet-VC-Builder\venv\Scripts\python.exe" -m bitnet_vc_builder.ui.web.app --config "C:\BitNet-VC-Builder\config\config.yaml"
     ```

2. Verify that the Web UI is running:
   - Open a web browser and navigate to http://localhost:8501
   - Check that the Web UI is displayed correctly

3. Test Web UI functionality:
   - Navigate to different pages
   - Create a virtual co-worker
   - Create a team
   - Run a task

4. Check the Web UI logs:
   - Open `C:\BitNet-VC-Builder\logs\ui.log`
   - Verify that there are no errors

### 4. Desktop Application Test

1. Start the Desktop Application:
   - Double-click the "BitNet VC Builder - Desktop App" shortcut on the desktop, or
   - Run the following command:
     ```powershell
     & "C:\BitNet-VC-Builder\BitNet-VC-Builder.exe"
     ```

2. Verify that the Desktop Application is running:
   - Check that the application window opens
   - Check that the application displays correctly

3. Test Desktop Application functionality:
   - Navigate to different pages
   - Create a virtual co-worker
   - Create a team
   - Run a task

### 5. Monitoring Setup Test

1. Run the monitoring setup script:
   ```powershell
   cd monitoring
   .\setup_monitoring.ps1
   ```

2. Verify that the monitoring setup completed successfully:
   - Check that the monitoring service is running
   - Check that the monitoring dashboard shortcut was created on the desktop

3. Start the monitoring dashboard:
   - Double-click the "BitNet VC Builder - Monitoring Dashboard" shortcut on the desktop, or
   - Run the following command:
     ```powershell
     powershell -ExecutionPolicy Bypass -File "C:\BitNet-VC-Builder\monitoring\dashboard.ps1"
     ```

4. Verify that the monitoring dashboard is running:
   - Check that the dashboard displays correctly
   - Check that it shows the status of the API server and Web UI
   - Check that it shows system resource usage

5. Test the web-based monitoring dashboard:
   ```powershell
   cd monitoring
   python web_dashboard.py
   ```
   - Open a web browser and navigate to http://localhost:8502
   - Check that the dashboard displays correctly

### 6. Backup Setup Test

1. Run the backup setup script:
   ```powershell
   cd backup
   .\setup_backup.ps1
   ```

2. Verify that the backup setup completed successfully:
   - Check that the backup task was created in Task Scheduler
   - Check that the backup management shortcut was created on the desktop

3. Start the backup management interface:
   - Double-click the "BitNet VC Builder - Backup Management" shortcut on the desktop, or
   - Run the following command:
     ```powershell
     powershell -ExecutionPolicy Bypass -File "C:\BitNet-VC-Builder\backup\manage_backups.ps1"
     ```

4. Verify that the backup management interface is running:
   - Check that the interface displays correctly
   - Create a new backup
   - List available backups

5. Test backup and restore:
   - Create a backup
   - Modify some files
   - Restore from the backup
   - Verify that the files were restored correctly

### 7. Integration Test

1. Start all components:
   - Double-click the "Start BitNet VC Builder" shortcut on the desktop, or
   - Run the following command:
     ```powershell
     & "C:\BitNet-VC-Builder\start.bat"
     ```

2. Verify that all components are running:
   - Check that the API server is running
   - Check that the Web UI is running
   - Check that the monitoring is running

3. Test end-to-end functionality:
   - Create a virtual co-worker
   - Create a team
   - Run a task
   - Check the monitoring dashboard
   - Create a backup
   - Restore from the backup

### 8. Performance Test

1. Run a performance test:
   - Create multiple virtual co-workers
   - Create multiple teams
   - Run multiple tasks simultaneously
   - Monitor system resource usage

2. Check the performance metrics:
   - CPU usage
   - Memory usage
   - Disk usage
   - Response time

### 9. Security Test

1. Test authentication:
   - Try to access the API without authentication
   - Try to access the Web UI without authentication
   - Try to access the monitoring dashboard without authentication

2. Test authorization:
   - Try to access resources with insufficient permissions
   - Try to access resources with the correct permissions

3. Test input validation:
   - Try to submit invalid input to the API
   - Try to submit invalid input to the Web UI

### 10. Update Test

1. Make a change to the codebase:
   - Modify a file
   - Add a new file
   - Delete a file

2. Run the setup script again:
   ```powershell
   .\setup_production.ps1
   ```

3. Verify that the update completed successfully:
   - Check that the changes were applied
   - Check that the application still works correctly

## Test Documentation

For each test, document the following:

1. Test name
2. Test description
3. Test steps
4. Expected results
5. Actual results
6. Pass/Fail status
7. Issues encountered
8. Screenshots or logs

## Issue Reporting

If you encounter any issues during testing:

1. Document the issue:
   - Issue description
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Environment information
   - Screenshots or logs

2. Create an issue on GitHub:
   - Go to https://github.com/ai-in-pm/BitNet-LLM-Virtual-Coworker-Builder/issues
   - Click "New issue"
   - Fill in the issue template
   - Submit the issue

## Conclusion

By following this testing guide, you can ensure that the production setup of BitNet_LLM_Virtual_Coworker_Builder works correctly on a clean system. If you encounter any issues, please report them so they can be fixed.
