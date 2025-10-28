# Script: load-env.ps1
# Purpose: Load environment variables from .env file into current PowerShell session
# Usage: . ./load-env.ps1

param(
    # Optional parameter to specify .env file path (defaults to .env in current directory)
    [string]$EnvFile = ".env"
)

# Check if the .env file exists
if (Test-Path $EnvFile) {
    # Read the .env file line by line
    Get-Content $EnvFile | 
    
    # Filter out comments (lines starting with #) and empty lines
    Where-Object { $_ -notmatch '^\s*#' -and $_.Trim() } | 
    
    # Process each remaining line
    ForEach-Object {
        # Split each line at the first = sign into key and value
        # Example: "API_KEY=secret123" becomes $name="API_KEY", $value="secret123"
        $name, $value = $_ -split '=', 2
        
        # Remove leading/trailing whitespace from key
        $name = $name.Trim()
        
        # Remove leading/trailing whitespace and quotes from value
        $value = $value.Trim().Trim('"').Trim("'")
        
        # Set the environment variable in current process
        # Variables set this way are only available in current PowerShell session
        [Environment]::SetEnvironmentVariable($name, $value, "Process")
    }
    
    # Print success message with filename to confirm variables were loaded
    Write-Host "✓ Environment variables loaded from $EnvFile" -ForegroundColor Green
} else {
    # If .env file doesn't exist, print error message in red
    Write-Host "✗ $EnvFile not found" -ForegroundColor Red
    exit 1
}