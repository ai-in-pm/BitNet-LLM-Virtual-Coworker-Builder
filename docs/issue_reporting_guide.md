# Issue Reporting Guide for BitNet_LLM_Virtual_Coworker_Builder

This guide provides instructions on how to effectively report issues with BitNet_LLM_Virtual_Coworker_Builder.

## Types of Issues

There are several types of issues you might encounter:

1. **Bugs**: Something isn't working as expected
2. **Feature Requests**: Suggestions for new features or improvements
3. **Production Issues**: Problems with the production setup
4. **Documentation Issues**: Errors or unclear information in the documentation

## Before Reporting an Issue

Before reporting an issue, please:

1. **Check existing issues**: Make sure the issue hasn't already been reported
2. **Update to the latest version**: Ensure you're using the latest version of BitNet_LLM_Virtual_Coworker_Builder
3. **Check the documentation**: The issue might be addressed in the documentation
4. **Try to reproduce the issue**: Make sure you can consistently reproduce the issue

## How to Report an Issue

### Step 1: Go to the GitHub Issues Page

Navigate to the [Issues page](https://github.com/ai-in-pm/BitNet-LLM-Virtual-Coworker-Builder/issues) of the BitNet_LLM_Virtual_Coworker_Builder repository.

### Step 2: Create a New Issue

Click the "New issue" button.

### Step 3: Select an Issue Template

Select the appropriate issue template:
- Bug report
- Feature request
- Production issue
- Documentation issue

### Step 4: Fill in the Template

Fill in all the required information in the template. The more details you provide, the easier it will be for us to address the issue.

#### For Bug Reports

- **Bug Description**: Clearly describe what the bug is
- **Steps to Reproduce**: Provide detailed steps to reproduce the bug
- **Expected Behavior**: Describe what you expected to happen
- **Actual Behavior**: Describe what actually happened
- **Environment**: Provide information about your environment (OS, Python version, etc.)
- **Screenshots**: Include screenshots if applicable
- **Logs**: Include relevant logs

#### For Feature Requests

- **Problem Statement**: Describe the problem you're trying to solve
- **Proposed Solution**: Describe your proposed solution
- **Alternative Solutions**: Describe any alternative solutions you've considered
- **Use Cases**: Describe how this feature would be used

#### For Production Issues

- **Issue Description**: Clearly describe the issue
- **Environment**: Provide information about your environment
- **Steps to Reproduce**: Provide detailed steps to reproduce the issue
- **Expected Behavior**: Describe what you expected to happen
- **Actual Behavior**: Describe what actually happened
- **Logs**: Include relevant logs
- **Screenshots**: Include screenshots if applicable

#### For Documentation Issues

- **Documentation Issue**: Clearly describe the issue
- **Location**: Specify where in the documentation the issue is
- **Current Content**: Describe what the documentation currently says
- **Suggested Improvement**: Describe how the documentation should be improved

### Step 5: Submit the Issue

Click the "Submit new issue" button to create the issue.

## After Submitting an Issue

After submitting an issue:

1. **Be responsive**: Be prepared to answer questions or provide additional information
2. **Be patient**: Issues are addressed based on priority and available resources
3. **Be helpful**: If you can provide a fix for the issue, consider submitting a pull request

## Collecting Logs

Logs are essential for diagnosing issues. Here's how to collect logs:

### API Server Logs

The API server logs are located at `C:\BitNet-VC-Builder\logs\api.log`. You can view them with:

```powershell
Get-Content -Path "C:\BitNet-VC-Builder\logs\api.log" -Tail 100
```

### Web UI Logs

The Web UI logs are located at `C:\BitNet-VC-Builder\logs\ui.log`. You can view them with:

```powershell
Get-Content -Path "C:\BitNet-VC-Builder\logs\ui.log" -Tail 100
```

### Monitoring Logs

The monitoring logs are located in the `C:\BitNet-VC-Builder\monitoring` directory. You can view them with:

```powershell
Get-Content -Path "C:\BitNet-VC-Builder\monitoring\monitoring_*.log" -Tail 100
```

### Backup Logs

The backup logs are included in each backup directory. You can view them with:

```powershell
Get-Content -Path "C:\BitNet-VC-Builder-Backups\BitNet-VC-Builder_Backup_*\backup.log" -Tail 100
```

## Taking Screenshots

Screenshots can be very helpful for diagnosing issues. Here's how to take screenshots:

### Windows

- Press `Windows + Shift + S` to open the Snipping Tool
- Select the area you want to capture
- Paste the screenshot into the issue

### macOS

- Press `Command + Shift + 4` to take a screenshot of a selected area
- The screenshot will be saved to your desktop
- Attach the screenshot to the issue

### Linux

- Use a screenshot tool like GNOME Screenshot or KDE Spectacle
- Save the screenshot
- Attach the screenshot to the issue

## Conclusion

By following this guide, you can help us address issues more effectively and improve BitNet_LLM_Virtual_Coworker_Builder for everyone. Thank you for your contributions!
