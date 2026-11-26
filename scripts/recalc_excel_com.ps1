param(
    [Parameter(Mandatory=$true)]
    [string]$WorkbookPath
)
$ErrorActionPreference = "Stop"
$excel = $null
$wb = $null
try {
    $excel = New-Object -ComObject Excel.Application
    $excel.Visible = $false
    $excel.DisplayAlerts = $false
    $excel.AskToUpdateLinks = $false
    Write-Output ("EXCEL_COM_VERSION=" + $excel.Version)
    $wb = $excel.Workbooks.Open($WorkbookPath)
    $excel.CalculateFullRebuild()
    $wb.Save()
    $wb.Close($true)
    Write-Output "EXCEL_RECALC_SAVE_OK=True"
} finally {
    if ($wb -ne $null) { [System.Runtime.Interopservices.Marshal]::ReleaseComObject($wb) | Out-Null }
    if ($excel -ne $null) {
        $excel.Quit()
        [System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null
    }
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
}
